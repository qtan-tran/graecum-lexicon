#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
translit_gen.py — generator phiên âm Hy Lạp cổ -> tiếng Việt, letter-faithful.

Cài đặt bảng docs/TRANSLIT.md (D13 v2, chốt 2026-11-13): bảng là nguồn chân lý
duy nhất, KHÔNG whitelist, KHÔNG tách register. Tool này sinh dạng kỳ vọng cho
mọi tên riêng; từ P0 linter dùng nó để so sánh tên trong vi_gloss (sai khác =
từ chối lô).

Quy tắc (xem chi tiết docs/TRANSLIT.md):
- Phụ âm: β b, γ g (γγ -> ng, γκ -> nk), δ đ, ζ z, θ th, κ c, λ l, μ m, ν n,
  ξ x, π p, ρ r (ῥ đầu từ -> rh), σ/ς s, τ t, φ ph, χ kh, ψ ps.
- Nguyên âm: α a, ε e, η ê, ι i, ο o, υ y, ω ô.
- Đôi: αι ai, ει i, οι oi, υι ui, αυ au, ευ eu, ου u.
- Rough breathing -> h đứng trước; iota dưới KHÔNG phiên âm; dấu dài/ngắn bỏ.
- Trọng âm (acute/grave/circumflex như nhau) -> thanh sắc trên nguyên âm của
  âm tiết mang trọng âm; với đôi (ai, au, eu, oi, ui) đặt trên nguyên âm ĐẦU.
- Đuôi KHÔNG rút gọn: mọi chữ cái được phiên âm, -ς -> s.
- Chữ hoa Greek -> chữ hoa đầu output.

CLI:
  python3 tools/translit_gen.py Λόγος Ἰωάννης ...      # phiên âm từng từ
  python3 tools/translit_gen.py                        # đọc từng dòng stdin
  python3 tools/translit_gen.py --test                 # chạy bảng test nội bộ
  python3 tools/translit_gen.py --file FILE TSV COL    # cột headword của TSV

Chỉ stdlib. Python 3.8+.
"""

import argparse
import sys
import unicodedata

# --- phân tách ký tự Greek ------------------------------------------------

VOWELS = set('αεηιουω')
DIPHTHONGS = {
    'αι': 'ai', 'ει': 'i', 'οι': 'oi', 'υι': 'ui',
    'αυ': 'au', 'ευ': 'eu', 'ου': 'u',
}

CONSONANTS = {
    'β': 'b', 'γ': 'g', 'δ': 'đ', 'ζ': 'z', 'θ': 'th',
    'κ': 'c', 'λ': 'l', 'μ': 'm', 'ν': 'n', 'ξ': 'x',
    'π': 'p', 'ρ': 'r', 'σ': 's', 'ς': 's', 'τ': 't',
    'φ': 'ph', 'χ': 'kh', 'ψ': 'ps',
}

SAC = {  # thanh sắc trên nguyên âm output
    'a': 'á', 'e': 'é', 'ê': 'ế', 'i': 'í',
    'o': 'ó', 'ô': 'ố', 'u': 'ú', 'y': 'ý',
}

ACUTE = {'\u0301', '\u0384'}          # acute + tonos
GRAVE = {'\u0300', '\u0385'}          # grave
CIRC = {'\u0342', '\u0302'}           # perispomeni / circumflex (bản số hoá)
ROUGH = {'\u0314'}                    # rough breathing
SMOOTH = {'\u0313'}
IGNEORABLE = {'\u0304', '\u0306',     # macron, breve
              '\u0345',               # iota subscript
              '\u0308'}              # diaeresis (bẻ gãy đôi, xử lý riêng)


def decompose(text):
    """-> list các (base, marks) của ký tự Greek; bỏ ký tự không phải Greek."""
    out = []
    for ch in unicodedata.normalize('NFD', text):
        name = unicodedata.name(ch, '')
        if 'GREEK' in name and ('LETTER' in name or name.startswith('GREEK SMALL '
                ) or name.startswith('GREEK CAPITAL ')):
            out.append((ch, set()))
        elif out and 'COMBINING' in name and out[-1][1] is not None:
            out[-1][1].add(ch)
        # ký tự khác (punctuation, space) bỏ khỏi chuỗi vào ra
    return out


def transliterate(text):
    """Hy Lạp (Unicode, đủ dấu) -> tiếng Việt letter-faithful."""
    chars = decompose(text)
    n = len(chars)
    out = []
    i = 0
    caps = False
    pending_h = False
    while i < n:
        base, marks = chars[i]
        base = base.lower()          # tra bảng bằng chữ thường

        # rough breathing trên phụ âm ρ (đầu từ) hoặc trước nguyên âm
        if base == 'ρ':
            if ROUGH & marks:
                out.append('rh')
            else:
                out.append('r')
            i += 1
            continue

        if base in CONSONANTS:
            # γγ -> ng, γκ -> nk
            if base == 'γ' and i + 1 < n and chars[i + 1][0] in ('γ', 'κ'):
                pair = 'ng' if chars[i + 1][0] == 'γ' else 'nk'
                out.append(pair)
                i += 2
                continue
            out.append(CONSONANTS[base])
            i += 1
            continue

        if base in VOWELS:
            # rough breathing trên nguyên âm -> h đứng trước
            if ROUGH & marks:
                pending_h = True
            accented = bool((ACUTE | GRAVE | CIRC) & marks)
            diaeresis = '\u0308' in marks
            # áp h chờ (rough breathing) trước nguyên âm/đôi
            if pending_h:
                out.append('h')
                pending_h = False
            # thử đôi: nguyên âm này + nguyên âm kế (không bẻ gãy bằng diaeresis)
            if (i + 1 < n and not diaeresis and chars[i + 1][0].lower() in VOWELS
                    and base + chars[i + 1][0].lower() in DIPHTHONGS):
                pair = base + chars[i + 1][0]
                vi = DIPHTHONGS[pair]
                acc2 = (ACUTE | GRAVE | CIRC) & chars[i + 1][1]
                accented = accented or bool(acc2)
                if accented:
                    # thanh sắc trên nguyên âm ĐẦU của đôi
                    if len(vi) == 1:
                        out.append(SAC[vi])
                    else:
                        out.append(SAC[vi[0]] + vi[1])
                else:
                    out.append(vi)
                i += 2
                continue
            v = {'α': 'a', 'ε': 'e', 'η': 'ê', 'ι': 'i',
                 'ο': 'o', 'υ': 'y', 'ω': 'ô'}[base]
            out.append(SAC[v] if accented else v)
            i += 1
            continue

        # ký tự lạ: bỏ + cảnh báo lên stderr
        sys.stderr.write('WARN: bỏ ký tự lạ %r\n' % base)
        i += 1

    s = ''.join(out)
    if s and text and unicodedata.normalize('NFD', text)[0].isupper():
        s = s[0].upper() + s[1:]
    return s


# --- bảng test: các tên trong docs/TRANSLIT.md §4 --------------------------

TEST_CASES = [
    # kỳ vọng sinh từ LUẬT bảng TRANSLIT (letter-faithful, sắc theo trọng âm,
    # κ -> c, υ độc lập -> y, ει -> i); KHÔNG chép từ bảng ví dụ cũ.
    ('Σωκράτης', 'Sôcrátês'),
    ('Σοφοκλῆς', 'Sophoclếs'),
    ('Πλάτων', 'Plátôn'),
    ('Ξενοφῶν', 'Xenophốn'),
    ('Δημοσθένης', 'Đêmosthénês'),
    ('Θουκυδίδης', 'Thucyđíđês'),
    ('Ἡρόδοτος', 'Hêróđotos'),
    ('Ὅμηρος', 'Hómêros'),
    ('Ἰωάννης', 'Iôánnês'),
    ('Ἀθῆναι', 'Athếnai'),
    ('Σπάρτη', 'Spártê'),
    ('Πειραιεύς', 'Piraiéus'),
    ('Δελφοί', 'Đelphói'),
    ('Ψαμαθώ', 'Psamathố'),
    ('Ἁλικαρνασσός', 'Halicarnassós'),
]


def run_tests():
    ok = 0
    for greek, expect in TEST_CASES:
        got = transliterate(greek)
        mark = 'OK ' if got == expect else 'FAIL'
        if got == expect:
            ok += 1
        print('%s %-16s -> %-14s (kỳ vọng %s)' % (mark, greek, got, expect))
    print('%d/%d pass' % (ok, len(TEST_CASES)))
    return ok == len(TEST_CASES)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('words', nargs='*')
    ap.add_argument('--test', action='store_true')
    ap.add_argument('--file', help='TSV: phiên âm cột COL của FILE')
    ap.add_argument('col', nargs='?', type=int, default=1,
                    help='cột headword (1-based) khi dùng --file')
    args = ap.parse_args()

    if args.test:
        sys.exit(0 if run_tests() else 1)

    if args.file:
        with open(args.file, encoding='utf-8') as f:
            for line in f:
                parts = line.rstrip('\n').split('\t')
                if len(parts) >= args.col:
                    print('%s\t%s' % (parts[args.col - 1],
                                      transliterate(parts[args.col - 1])))
        return

    if args.words:
        for w in args.words:
            print(transliterate(w))
        return

    for line in sys.stdin:
        print(transliterate(line.strip()))


if __name__ == '__main__':
    main()
