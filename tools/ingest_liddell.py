#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ingest_liddell.py — B7: parse Middle Liddell TEI (Perseus 1999.04.0058) sang TSV sense-aligned.

Nguồn trục (D14-thực-tế, chốt 2026-11-13): blinskey/middle-liddell, file
Perseus_text_1999.04.0058.xml (fork nguyên bản Perseus, chỉ vá typo; repo archived).
  https://raw.githubusercontent.com/blinskey/middle-liddell/master/Perseus_text_1999.04.0058.xml
Nguồn phụ (CHỈ tra chéo, không ingest): helmadik/MiddleLiddell (đã Unicode hoá nhưng
thêm morph info thỉnh thoảng sai + edit hoà nhập LSJ, vi phạm nguyên tắc en_gloss nguyên bản).

Output TSV (schema docs/FORMAT-SPEC.md §4.1):
  entry_id  headword  sense_id  level  en_gloss  citations  src
- headword: Unicode NFC, đủ dấu (accent + breathing), Greek giữ nguyên.
- sense_id: <latinized>#<label>, label do cấu trúc TEI sinh (D10):
    level 2 (I, II, III...)      -> "II"
    level 3 (1, 2, 3...)         -> "II.3"   (prefix = Roman hiện hành)
    level 4 (a, b, c...)         -> "II.3.b" (prefix = number hiện hành)
    level 1 (A, B, C...)         -> "A" hoặc "II.A" nếu đã có Roman
    level 0 (không đánh số)      -> "0"; lặp lại thì "0.2", "0.3" theo vị trí
- en_gloss: text sense PHÛNG HOÀ (không sửa), Greek beta code -> Unicode NFC;
  phần tử <usg> tách sang cột citations (D3 giữ nguyên Latin).
- citations: các <usg> theo thứ tự, nối "; ".
- src: ML.
Chỉ stdlib. Python 3.8+.

Cách chạy:
  python3 tools/ingest_liddell.py --input Perseus_text_1999.04.0058.xml \
      --output data/source/ml-senses.tsv [--limit N] [--stats]
"""

import argparse
import sys
import unicodedata
import xml.etree.ElementTree as ET

# ---------------------------------------------------------------------------
# Beta code (Perseus/TLG) -> Unicode
# ---------------------------------------------------------------------------

BETA_LETTERS = {
    'a': 'α', 'b': 'β', 'g': 'γ', 'd': 'δ', 'e': 'ε', 'z': 'ζ',
    'h': 'η', 'q': 'θ', 'i': 'ι', 'k': 'κ', 'l': 'λ', 'm': 'μ',
    'n': 'ν', 'c': 'ξ', 'o': 'ο', 'p': 'π', 'r': 'ρ', 's': 'σ',
    't': 'τ', 'u': 'υ', 'f': 'φ', 'x': 'χ', 'y': 'ψ', 'w': 'ω',
    'j': 'ς',   # final sigma (biến thể hiếm trong bản số hoá)
    'v': 'ϝ',   # digamma
}

COMBINING = {
    '(': '\u0314',   # rough breathing
    ')': '\u0313',   # smooth breathing
    '/': '\u0301',   # acute
    '\\': '\u0300',  # grave
    '=': '\u0342',   # circumflex (perispomeni)
    '_': '\u0304',   # macron
    '^': '\u0306',   # breve
    '|': '\u0345',   # iota subscript
    '+': '\u0308',   # diaeresis
}

# ký tự beta không phải chữ/dấu: giữ nguyên như punctuation
# (U+02B9 numeral sign, U+0375 lower numeral sign, U+00AF/U+02D8 macron/breve,
#  U+2014 em dash + U+2020 dagger có sẵn trong bản số hoá, [] biên tập)
PASSTHROUGH = set(" ,.;:?!'\"-[]#\u2014\u2020\u02b9\u0375\u00af\u02d8")


class BetaConverter:
    def __init__(self):
        self.warnings = []
        self.n_warn = 0

    def warn(self, msg):
        self.n_warn += 1
        if len(self.warnings) < 50:
            self.warnings.append(msg)

    def convert(self, s):
        """Chuyển một chuỗi beta code sang Unicode Greek NFC."""
        out = []
        last = -1            # chỉ số chữ Greek gần nhất trong out (dấu thường gán vào đây)
        pre = []             # dấu cho chữ HOA sắp tới (beta: dấu đứng TRƯỚC chữ hoa)
        caps = False
        i = 0
        n = len(s)
        while i < n:
            ch = s[i]
            if ch == '*':
                caps = True
                i += 1
                continue
            if ch in COMBINING:
                if caps:
                    # chữ hoa: dấu đứng trước chữ trong beta code
                    pre.append(COMBINING[ch])
                elif last < 0:
                    # beta code: dấu thường theo SAU chữ nó biến đổi
                    self.warn('dấu %r không có chữ trước: %r' % (ch, s[:40]))
                else:
                    out[last] += COMBINING[ch]
                i += 1
                continue
            if ch in BETA_LETTERS:
                g = BETA_LETTERS[ch]
                if ch == 's' and self._word_final(s, i):
                    g = 'ς'
                if caps:
                    g = g.upper()
                    caps = False
                out.append(g + ''.join(pre))
                pre = []
                last = len(out) - 1
                i += 1
                continue
            if ch in PASSTHROUGH:
                if ch == "'":
                    ch = '\u2019'   # apostrophe Hy Lạp
                out.append(ch)
                i += 1
                continue
            # số hiệu homograph (a)/atos1): giữ nguyên, latinize sẽ dùng
            if ch.isdigit():
                out.append(ch)
                i += 1
                continue
            self.warn('unknown beta char %r in %r' % (ch, s[:40]))
            i += 1
        text = ''.join(out)
        return unicodedata.normalize('NFC', text)

    @staticmethod
    def _word_final(s, i):
        return i + 1 >= len(s) or not (s[i + 1].isalpha() or s[i + 1] in COMBINING)


# ---------------------------------------------------------------------------
# Latin hoá (cho sense_id; phiên âm đầy đủ là tools/translit_gen.py)
# ---------------------------------------------------------------------------

LATIN = {
    'a': 'a', 'b': 'b', 'g': 'g', 'd': 'd', 'e': 'e', 'z': 'z',
    'h': 'e', 'q': 'th', 'i': 'i', 'k': 'k', 'l': 'l', 'm': 'm',
    'n': 'n', 'c': 'x', 'o': 'o', 'p': 'p', 'r': 'r', 's': 's',
    't': 't', 'u': 'u', 'f': 'ph', 'x': 'ch', 'y': 'ps', 'w': 'o',
    'j': 's', 'v': 'v',
}


def latinize_beta(key):
    """beta key -> dạng Latin không dấu cho sense_id (vd 'lo/gos' -> 'logos')."""
    out = []
    for ch in key:
        if ch in LATIN:
            out.append(LATIN[ch])
        elif ch.isdigit():
            out.append(ch)   # số homograph Perseus: giữ để sense_id duy nhất
    return ''.join(out).lower()


# ---------------------------------------------------------------------------
# Flatten sense content
# ---------------------------------------------------------------------------

GREEK_EL_TAGS = {'foreign', 'orth', 'ref', 'quote', 'note', 'head', 'label'}



def _clean(s):
    # gọn khoảng trắng, giữ nguyên mọi ký tự khác (không sửa nội dung)
    import re
    s = re.sub(r'[ \t]+', ' ', s).strip()
    # gỡ artefact do tách <usg> khỏi gloss: " ,", ", ,", dấu câu treo cuối
    s = re.sub(r'\s*,\s*(?=[,.;:])', '', s)
    s = re.sub(r'(?:\s*,\s*){2,}', ', ', s)
    s = re.sub(r'\s+([,.;:?!])', r'\1', s)
    s = re.sub(r'[ ,;:]+$', '', s)
    return s


def flatten_sense(sense, converter):
    """Trả về (en_gloss, citations) của một <sense>."""
    usgs = []

    def walk(el, greek=False):
        parts = []
        if el.tag == 'form':
            return ''   # không lặp headword vào gloss (khi flatten cả entry)
        is_greek = greek or (el.get('lang') == 'greek' and el.tag in GREEK_EL_TAGS)
        if el.tag == 'usg':
            for sub in el.iter():
                t = (sub.text or '').strip()
                if t:
                    usgs.append(t)
                if sub.tail and sub.tag != 'usg':
                    pass
            return ''
        if el.text:
            parts.append(converter.convert(el.text) if is_greek else el.text)
        for child in el:
            parts.append(walk(child, is_greek))
            if child.tail:
                parts.append(converter.convert(child.tail) if is_greek else child.tail)
        return ''.join(parts)

    gloss = _clean(walk(sense))
    cites = []
    seen = set()
    for u in usgs:
        if u not in seen:
            seen.add(u)
            cites.append(u)
    return gloss, '; '.join(cites)


# ---------------------------------------------------------------------------
# Parser chính
# ---------------------------------------------------------------------------

ROMAN_LETTERS = set('IVX')


def sense_labels(senses):
    """Sinh label sense_id cho danh sách sense của 1 entry (theo level).

    Cấu trúc thực tế của bản TEI (sense là anh em phẳng, phân cấp qua @level):
      level 2 (I, II, ...)   -> "II"            (đặt parent)
      level 1 (A, B, ...)    -> "II.A" / "A"    (đặt parent nếu chưa có Roman)
      level 3 (1, 2, ...)    -> parent + ".n"   (vd "A.2", "II.3")
      level 4 (a, b, ...)    -> level3 + ".n"   (vd "II.3.b")
      level 0 (không số)      -> "0"; lặp thì "0.2", "0.3" theo vị trí
    Lặp label bất kỳ -> thêm ".<vị trí>" để duy nhất trong entry.
    """
    labels = []
    p12 = ''     # parent gần nhất từ level 1 hoặc 2
    l3 = ''      # label level-3 gần nhất (cha của level 4)
    counts = {}
    for s in senses:
        lvl = (s.get('level') or '0').strip()
        n = (s.get('n') or '0').strip()
        if lvl == '2':
            label = n
            p12 = n
            l3 = ''
        elif lvl == '1':
            label = (p12 + '.' if p12 else '') + n
            p12 = label
            l3 = ''
        elif lvl == '3':
            label = (p12 + '.' if p12 else '') + n
            l3 = label
        elif lvl == '4':
            base12 = l3 or p12
            label = (base12 + '.' if base12 else '') + n
        else:  # level 0
            label = n if n and n != '0' else '0'
        base = label
        if base in counts:
            counts[base] += 1
            label = '%s.%d' % (base, counts[base])
        else:
            counts[base] = 1
        labels.append((base, label))
    return labels


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--limit', type=int, default=0, help='giới hạn số entry (debug)')
    ap.add_argument('--stats', action='store_true')
    args = ap.parse_args()

    conv = BetaConverter()
    tree = ET.parse(args.input)
    root = tree.getroot()

    rows = []
    n_entries = 0
    n_senses = 0
    n_xref = 0
    for entry in root.iter('entry'):
        n_entries += 1
        if args.limit and n_entries > args.limit:
            n_entries -= 1
            break
        key = entry.get('key') or ''
        latin = latinize_beta(key)
        hw = conv.convert(''.join(ch for ch in key if not ch.isdigit()))
        senses = list(entry.iter('sense'))
        if not senses:
            # entry tham chiếu thuần (= xem từ khác): phát thành dòng xref,
            # không bịa sense (nguyên tắc không-bịa)
            xref_gloss, xref_cites = flatten_sense(entry, conv)
            rows.append((
                entry.get('id') or '',
                hw,
                '%s#xref' % latin,
                'xref',
                xref_gloss,
                xref_cites,
                'ML',
            ))
            n_xref += 1
            continue
        labels = sense_labels(senses)
        for s, (_base, label) in zip(senses, labels):
            gloss, cites = flatten_sense(s, conv)
            if not gloss and not cites:
                # sense tự đóng / chỉ có citation: vẫn giữ dòng để coverage
                # alignment (D10) khớp 100% sense gốc; đánh dấu qua cột src
                rows.append((
                    entry.get('id') or '',
                    hw,
                    '%s#%s' % (latin, label),
                    (s.get('n') or '0'),
                    '',
                    '',
                    'ML-EMPTY',
                ))
                continue
            rows.append((
                entry.get('id') or '',
                hw,
                '%s#%s' % (latin, label),
                (s.get('n') or '0'),
                gloss,
                cites,
                'ML',
            ))
            n_senses += 1

    # kiểm tra sense_id duy nhất toàn cục (alignment bắt buộc, D10)
    seen = {}
    n_dup = 0
    for r in rows:
        sid = r[2]
        if sid in seen:
            n_dup += 1
            if n_dup <= 10:
                conv.warn('sense_id trùng: %s (%s vs %s)' % (sid, seen[sid], r[0]))
        else:
            seen[sid] = r[0]
    if n_dup:
        # gắn entry_id vào đuôi để vẫn duy nhất + truy vết được
        emitted = set()
        for i, r in enumerate(rows):
            if r[2] in emitted:
                rows[i] = (r[0], r[1], '%s@%s' % (r[2], r[0]), r[3], r[4],
                           r[5], r[6])
            else:
                emitted.add(r[2])

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write('entry_id\theadword\tsense_id\tlevel\ten_gloss\tcitations\tsrc\n')
        for r in rows:
            f.write('\t'.join(c.replace('\t', ' ').replace('\n', ' ') for c in r))
            f.write('\n')

    if args.stats:
        print('entries: %d' % n_entries)
        print('senses written: %d' % n_senses)
        print('xref entries: %d' % n_xref)
        print('rows written: %d' % len(rows))
        print('unique sense_id: %d' % len(seen))
        print('sense_id duplicates (đã gắn @entry_id): %d' % n_dup)
        print('beta warnings: %d' % conv.n_warn)
        for w in conv.warnings[:10]:
            print('  WARN:', w)


if __name__ == '__main__':
    main()
