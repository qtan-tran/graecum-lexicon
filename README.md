# graecum-lexicon

Từ điển học Hy Lạp cổ – tiếng Việt: dự án dịch *An Intermediate Greek-English Lexicon* (Middle Liddell 1889, ~40.000 mục, public domain) sang tiếng Việt, và từ đó sinh ra các sản phẩm dữ liệu cho hệ sinh thái graecum/satzanalyse.

## Hai sản phẩm (tách bạch)

1. **Bản đầy đủ**: từ điển tham khảo Hy Lạp cổ – tiếng Việt, sense-aligned với bản gốc (giữ thứ tự sense, citations Latin, phân tầng I/II/III + A/B/C), lưu dạng TSV trong repo này.
2. **Bản rút gọn** `dict-core.js`/`dict-full.js`: chỉ gồm gloss VI ngắn, sinh TỰ ĐỘNG từ bản đầy đủ, đóng gói cho tool (satzanalyse, graecum-vn). Hai sản phẩm không được tự phát triển độc lập.

## Nguồn và giấy phép

- Trục dịch: Middle Liddell 1889 (PD, bản TEI Perseus số hoá). LSJ 9th và Bailly chỉ dùng tra tay khi sense mơ hồ, không đưa vào pipeline tự động (chi tiết: `docs/COPYRIGHT.md`).
- Bản dịch tiếng Việt là tác phẩm phái sinh: người dự án giữ bản quyền dịch, cấp **CC BY-SA 4.0** (nội dung) + **MIT** (code linter). Xem `LICENSE`.

## Cấu trúc repo

```
graecum-lexicon/
├── docs/                # DECISIONS (protocol D1-D13) · ROADMAP · FORMAT-SPEC · COPYRIGHT · TRANSLIT
├── data/
│   ├── termbase-grammar.tsv   # term base markers ngữ pháp EN→VN (luật cứng)
│   ├── decoder-1889.tsv       # cẩm nang dịch giả: tiếng Anh Victorian → nghĩa hiện đại → VI
│   └── batches/               # các lô dịch P0-P3 + manifest (coverage assertion)
└── tools/linter.py      # QA gates tự động (mã hoá, termbase, alignment, coverage)
```

## QA tự động

Linter chạy trong CI (`.github/workflows/lint.yml`): lô nào báo đỏ thì GitHub chặn merge. Chạy local:

```
python3 tools/linter.py
```

5 cổng QA mỗi lô (chi tiết `docs/ROADMAP.md`): termbase enforcement · sense-ID alignment · back-translation spot-check · sweep ký tự · gold-set corpus.

## Nguyên tắc cốt lõi

**Không bịa**: sense không chắc → giữ tiếng Anh trong ngoặc + tag `[chưa dịch]`, tuyệt đối không đoán. Mọi gloss truy vết được về sense-ID gốc. Phiên âm tên riêng hoàn toàn theo bảng hệ thống `docs/TRANSLIT.md`, không có ngoại lệ. Quy ước biên soạn đầy đủ: `docs/DECISIONS.md` (13 quyết định đã chốt) và `docs/FORMAT-SPEC.md` (schema dữ liệu).
