# FORMAT-SPEC: schema dữ liệu

Mọi file TSV: tab-separated, UTF-8, NFC, dòng header đầu tiên, không quoted fields (nội dung cột không chứa tab và xuống dòng). Giá trị enum dùng ASCII không dấu.

## 1. Term base markers: `data/termbase-grammar.tsv`

```
key	type	meaning_mod	xlate_vi	src	note
c. gen.	marker	governs the genitive case	+ sở hữu cách	ML/LSJ	
```

- `key`: marker đúng như in trong Middle Liddell (giữ viết tắt, giữ dấu chấm).
- `type`: `marker | term` (`marker` = viết tắt ngữ pháp; `term` = thuật ngữ).
- `meaning_mod`: diễn giải tiếng Anh hiện đại (đã kiểm định).
- `xlate_vi`: dịch tiếng Việt chuẩn, áp dụng 100%.
- `src`: `ML | LSJ | decoder` (nghĩa kiểm định qua nguồn nào).
- Mục tiêu Phase T: ≥ 500 dòng (seed hiện tại là phần lõi; bổ sung qua cổng duyệt).

## 2. Cẩm nang dịch giả: `data/decoder-1889.tsv`

Schema giống termbase (`key,type,meaning_mod,xlate_vi,src,note`), `type` = `idiom | term | prefix`. Chứa tiếng Anh Victorian 1889 có nghĩa lệch hiện đại (wont to, betake oneself, make away with...). Khi dịch gặp từ không nằm trong decoder và không chắc nghĩa 1889 → tra chéo LSJ9/Bailly tra tay, rồi THÊM vào decoder (qua cổng duyệt), không dịch theo phán đoán.

## 3. Phiên âm tên riêng: `docs/TRANSLIT.md`

Không còn file whitelist. Mọi tên riêng sinh từ bảng hệ thống letter-faithful trong `docs/TRANSLIT.md` (không ngoại lệ, không register). Từ P0, linter kiểm tra bằng generator: sinh dạng kỳ vọng từ headword Greek rồi so với tên dùng trong `vi_gloss`; sai khác = từ chối lô.

## 4. Lô dịch: `data/batches/<PHASE>-<cluster>.tsv`

```
headword	sense_id	level	en_gloss	vi_gloss	citations	status	src
λόγος	logos#I.1	I	one of several meanings...	một trong vài nghĩa...	Hom. etc.	done	ML
```

- `headword`: Greek NFC, giữ nguyên bản gốc.
- `sense_id`: `<latinized-headword>#<Roman>.<number>` (ví dụ `logos#II.3`); do parser TEI sinh, người dịch không tự đánh số.
- `level`: `I | II | III | A | B | C` (phân tầng sense gốc, D9).
- `en_gloss`: nguyên bản English 1889 (không sửa).
- `vi_gloss`: bản dịch; không chắc → giữ English trong ngoặc + `status = chua-dich`.
- `citations`: giữ nguyên viết tắt Latin (D3).
- `status`: `done | chua-dich | src-err` (ASCII; `chua-dich` hiển thị trong bản đọc là `[chưa dịch]`).
- `src`: `ML` (toàn bộ Phase T-P3 đều trục ML).

## 5. Manifest: `data/batches/manifest.tsv`

```
batch	file	headwords	phase	status
P0-core	P0-core.tsv	100	P0	open
```

- Coverage assertion (linter): mỗi headword xuất hiện đúng 1 batch; file batch phải tồn tại; tổng headwords mọi batch = tổng khai báo. Từ P2 không batch nào được ghi kép headword.

## 6. Quy tắc ký tự (cổng 4)

- NFC toàn bộ; 0 U+FFFD; 0 em dash trong nội dung; apostrophe Hy Lạp là ’ (U+2019); không CJK/Cyrillic ngoài chủ đích.
- Greek giữ đủ dấu (accent + breathing); phiên âm chỉ là thông tin phụ trong whitelist.
