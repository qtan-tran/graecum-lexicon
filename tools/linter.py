#!/usr/bin/env python3
"""graecum-lexicon linter: QA gates tu dong cho du lieu bien soan.

Cac nhom kiem tra (docs/ROADMAP.md):
  A. Encoding sweep  : NFC, 0 U+FFFD, 0 em dash, khong CJK/Cyrillic ngoai chu dich
  B. Termbase        : schema, key duy nhat, xlate_viet du; batch vi_gloss khong chua marker EN
  C. Batches         : schema, sense_id day du + duy nhat, status enum, nguyen tac khong-bia
  D. Coverage        : moi headword thuoc dung 1 batch, file ton tai, tong khop khai bao

Exit code 1 neu co bat ky vi pham nao. CI chay file nay, bao do = chan merge.
Chi dung stdlib Python 3.9+.
"""
import sys
import re
import unicodedata
from pathlib import Path

# ---------------------------------------------------------------- helpers

EM_DASH = "\u2014"
FFFD = "\uFFFD"
CJK = re.compile(r"[\u3400-\u4DBF\u4E00-\u9FFF]")
CYRILLIC = re.compile(r"[\u0400-\u04FF]")

BATCH_SCHEMA = ["headword", "sense_id", "level", "en_gloss", "vi_gloss",
                "citations", "status", "src"]
BATCH_STATUS = {"done", "chua-dich", "src-err"}
TB_SCHEMA = ["key", "type", "meaning_mod", "xlate_vi", "src", "note"]
MANIFEST_SCHEMA = ["batch", "file", "headwords", "phase", "status"]


class Report:
    def __init__(self):
        self.violations = []

    def fail(self, gate, path, msg):
        self.violations.append("[%s] %s: %s" % (gate, path, msg))

    def ok(self, gate, path, msg):
        print("  PASS %s %s" % (gate, msg))

    @property
    def is_clean(self):
        return not self.violations


def load_tsv(path, schema, rep, gate):
    """Doc TSV, kiem tra so cot. Tra ve list dict (bo qua header)."""
    rows = []
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    if not lines:
        rep.fail(gate, path, "file rong")
        return rows
    header = lines[0].split("\t")
    if header != schema:
        rep.fail(gate, path, "header sai: %s (ky vong %s)" % (header, schema))
        return rows
    for n, line in enumerate(lines[1:], start=2):
        if line == "":
            rep.fail(gate, path, "dong %d rong" % n)
            continue
        cells = line.split("\t")
        if len(cells) != len(schema):
            rep.fail(gate, path,
                     "dong %d co %d cot, ky vong %d" % (n, len(cells), len(schema)))
            continue
        rows.append(dict(zip(schema, cells)))
    return rows


# ---------------------------------------------------------------- gates

def gate_encoding(root, rep):
    """A. Sweep ky tu tren moi file du lieu + docs."""
    targets = list((root / "data").rglob("*.tsv")) + list((root / "docs").glob("*.md"))
    for p in sorted(targets):
        rel = p.relative_to(root)
        text = p.read_text(encoding="utf-8")
        if FFFD in text:
            rep.fail("A", rel, "chua U+FFFD")
        if EM_DASH in text:
            rep.fail("A", rel, "chua em dash U+2014")
        if CJK.search(text):
            rep.fail("A", rel, "chua ky tu CJK ngoai chu dich")
        if CYRILLIC.search(text):
            rep.fail("A", rel, "chua ky tu Cyrillic ngoai chu dich")
        nfc = unicodedata.normalize("NFC", text)
        if nfc != text:
            rep.fail("A", rel, "khong phai NFC")
    rep.ok("A", "encoding", "%d file quet" % len(targets))
    return len(targets)


def _marker_regex(keys):
    parts = sorted((re.escape(k) for k in keys), key=len, reverse=True)
    return re.compile("(?<![A-Za-z])(%s)(?![A-Za-z])" % "|".join(parts))


def gate_termbase(root, rep):
    """B. Termbase + decoder hop le; batch vi_gloss khong chua marker EN."""
    tb_path = root / "data" / "termbase-grammar.tsv"
    dc_path = root / "data" / "decoder-1889.tsv"
    keys = []
    for label, path in (("termbase", tb_path), ("decoder", dc_path)):
        rows = load_tsv(path, TB_SCHEMA, rep, "B")
        seen = set()
        for r in rows:
            if not r["key"] or not r["xlate_vi"]:
                rep.fail("B", path.name, "key hoac xlate_vi rong: %r" % r["key"])
            if r["key"] in seen:
                rep.fail("B", path.name, "key trung: %r" % r["key"])
            seen.add(r["key"])
        keys.extend(r["key"] for r in rows)
    rep.ok("B", "termbase", "termbase %d dong + decoder hop le" % len(keys))

    pat = _marker_regex(keys)
    for b in sorted((root / "data" / "batches").glob("*.tsv")):
        if b.name == "manifest.tsv":
            continue
        rows = load_tsv(b, BATCH_SCHEMA, rep, "B")
        for i, r in enumerate(rows, start=2):
            m = pat.search(r["vi_gloss"])
            if m:
                rep.fail("B", b.name,
                         "dong %d vi_gloss chua marker EN %r (phai dung xlate_viet)" % (i, m.group(0)))




def gate_batches(root, rep):
    """C. Batch dich: sense_id, status, nguyen tac khong-bia."""
    bdir = root / "data" / "batches"
    batches = [b for b in sorted(bdir.glob("*.tsv")) if b.name != "manifest.tsv"]
    for b in batches:
        rows = load_tsv(b, BATCH_SCHEMA, rep, "C")
        seen = set()
        for i, r in enumerate(rows, start=2):
            sid = r["sense_id"]
            if not sid:
                rep.fail("C", b.name, "dong %d thieu sense_id" % i)
            elif sid in seen:
                rep.fail("C", b.name, "dong %d sense_id trung: %r" % (i, sid))
            seen.add(sid)
            if r["status"] not in BATCH_STATUS:
                rep.fail("C", b.name, "dong %d status khong hop le: %r" % (i, r["status"]))
            if r["status"] == "chua-dich" and not r["vi_gloss"]:
                rep.fail("C", b.name, "dong %d chua-dich phai giu nguyen ban EN trong vi_gloss" % i)
            if r["status"] == "done" and not r["vi_gloss"]:
                rep.fail("C", b.name, "dong %d done nhung vi_gloss rong" % i)
    rep.ok("C", "batches", "%d file batch" % len(batches))
    return batches


def gate_coverage(root, rep, batches):
    """D. Coverage assertion: moi headword dung 1 batch, tong khop manifest."""
    mpath = root / "data" / "batches" / "manifest.tsv"
    mrows = load_tsv(mpath, MANIFEST_SCHEMA, rep, "D")
    for m in mrows:
        f = root / "data" / "batches" / m["file"]
        if not f.exists():
            rep.fail("D", m["file"], "file batch khai trong manifest khong ton tai")
    for m in mrows:
        f = root / "data" / "batches" / m["file"]
        if f.exists():
            rows = load_tsv(f, BATCH_SCHEMA, rep, "D")
            real = len(set(r["headword"] for r in rows))
            decl = m["headwords"]
            if decl.isdigit() and int(decl) != real:
                rep.fail("D", m["file"],
                         "manifest khai %s headwords, thuc te %d" % (decl, real))
    # moi headword chi duoc phep thuoc mot batch (khac file)
    per_batch = []
    for b in batches:
        rows = load_tsv(b, BATCH_SCHEMA, rep, "D")
        per_batch.append((b.name, set(r["headword"] for r in rows)))
    seen = {}
    for name, hset in per_batch:
        for h in hset:
            if h in seen and seen[h] != name:
                rep.fail("D", h, "headword nam o 2 batch: %s va %s" % (seen[h], name))
            else:
                seen[h] = name
    rep.ok("D", "coverage", "%d headwords, %d batch" % (len(seen), len(batches)))


# ---------------------------------------------------------------- main

def main(argv=None):
    argv = argv or sys.argv[1:]
    root = Path(argv[0]).resolve() if argv else Path(__file__).resolve().parent.parent
    print("graecum-lexicon linter (root: %s)" % root)
    if not (root / "data").is_dir():
        print("FATAL: khong tim thay thu muc data/")
        return 2
    rep = Report()
    gate_encoding(root, rep)
    gate_termbase(root, rep)
    batches = gate_batches(root, rep)
    gate_coverage(root, rep, batches)
    print()
    if rep.is_clean:
        print("RESULT: PASS (0 vi pham)")
        return 0
    for v in rep.violations:
        print("VI PHAM " + v)
    print("RESULT: FAIL (%d vi pham) -> CI chan merge" % len(rep.violations))
    return 1


if __name__ == "__main__":
    sys.exit(main())
