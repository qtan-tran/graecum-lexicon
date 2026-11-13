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
- Mục tiêu Phase T ≥ 500 dòng: ĐÃ ĐẠT, 794 dòng dữ liệu (285 marker, 281 term, 228 citation); bổ sung tiếp qua cổng duyệt.

## 2. Cẩm nang dịch giả: `data/decoder-1889.tsv`

Schema giống termbase (`key,type,meaning_mod,xlate_vi,src,note`), `type` = `idiom | term | prefix`. Chứa tiếng Anh Victorian 1889 có nghĩa lệch hiện đại (wont to, betake oneself, make away with...). Khi dịch gặp từ không nằm trong decoder và không chắc nghĩa 1889 → tra chéo LSJ9/Bailly tra tay, rồi THÊM vào decoder (qua cổng duyệt), không dịch theo phán đoán.

## 3. Phiên âm tên riêng: `docs/TRANSLIT.md`

Không còn file whitelist. Mọi tên riêng sinh từ bảng hệ thống letter-faithful trong `docs/TRANSLIT.md` (không ngoại lệ, không register). Linter kiểm tra bằng generator, hiện thực từ Phase T pilot: cổng E trong `tools/linter.py` sinh dạng kỳ vọng từ headword Greek (chữ HOA) rồi so với tên dùng trong `vi_gloss`; sai khác = từ chối lô.

## 4. Lô dịch: `data/batches/<PHASE>-<cluster>.tsv`

```
headword	sense_id	level	en_gloss	vi_gloss	citations	status	src
λόγος	logos#I.1	I	one of several meanings...	một trong vài nghĩa...	Hom. etc.	done	ML
```

- `headword`: Greek NFC, giữ nguyên bản gốc.
- `sense_id`: `<latinized-headword>#<Roman>.<number>` (ví dụ `logos#II.3`); do parser TEI sinh, người dịch không tự đánh số.
- `level`: giữ nguyên cột `level` từ source TSV ingest (§4.1), tức attribute `n` gốc của sense trong TEI: `0` (sense không đánh số), số con (`1`-`5`...), Roman (`I`-`VIII`), chữ (`A`-`C`, `a`-`c`), hoặc `xref`. Phân cấp đầy đủ nằm trong `sense_id` (D9).
- `en_gloss`: nguyên bản English 1889 (không sửa).
- `vi_gloss`: bản dịch; không chắc → giữ English trong ngoặc + `status = chua-dich`.
- `citations`: giữ nguyên viết tắt Latin (D3).
- `status`: `done | chua-dich | src-err` (ASCII; `chua-dich` hiển thị trong bản đọc là `[chưa dịch]`).
- `src`: `ML` (toàn bộ Phase T-P3 đều trục ML).

### 4.1. Source TSV ingest: `data/source/ml-senses.tsv` (local, không commit)

Output của `tools/ingest_liddell.py` từ TEI Middle Liddell (Perseus_text_1999.04.0058.xml, 36.490 entry). File nguồn TEI và TSV này KHÔNG commit vào repo (đã có trong `.gitignore`: `data/source/`, `*.xml`); ingest lại bằng tool khi cần.

```
entry_id\theadword\tsense_id\tlevel\ten_gloss\tcitations\tsrc
aatos1\tἆθλος\taatos#0\t0\trace of contest...\tIl.\tML
```

- `entry_id`: `<latin><số homograph>` (số giữ từ TEI, headword bỏ số); homograph khác dấu được tách entry.
- `sense_id`: `<latin>#<label>`, do parser sinh theo vị trí sense gốc trong entry: level 0 → `0`, `0.2`...; level 1 → `A`, `B`... hoặc `II.A` (nếu cha là `II`); level 2 → `I`, `II`, `III`...; level 3 → `II.A.2` dạng `<parent>.<số>`; level 4 → `<parent>.<chữ>`. Người dịch KHÔNG tự đánh số sense.
- `xref`: entry tham chiếu thuần (không gloss) → `level = xref`, label `xref`.
- `ML-EMPTY`: sense rỗng hoặc chỉ có citation → giữ dòng để alignment đủ, `src = ML-EMPTY`.
- `en_gloss`: giữ nguyên văn 1889; chỉ gỡ artefact dấu phẩy thừa của bản số hoá khi sense trống sau cleanup (documented trong tool).
- `citations`: usg/ nguồn trích tách từ gloss, join bằng `; `.
- Chạy toàn file cho 56.893 dòng sense (55.109 sense + 1.773 xref), 485 sense_id trùng giữa homograph được gắn thêm `@entry_id` để duy nhất.

## 5. Manifest: `data/batches/manifest.tsv`

```
batch	file	headwords	phase	status
P0-core	P0-core.tsv	100	P0	open
```

- Coverage assertion (linter): mỗi headword xuất hiện đúng 1 batch; file batch phải tồn tại; tổng headwords mọi batch = tổng khai báo. Từ P2 không batch nào được ghi kép headword.

## 6. Quy tắc ký tự (cổng 4)

- NFC toàn bộ; 0 U+FFFD; 0 em dash trong nội dung biên soạn (`vi_gloss`, termbase, decoder, docs, README); apostrophe Hy Lạp là ’ (U+2019); không CJK/Cyrillic ngoài chủ đích. Cột `en_gloss` nguyên văn 1889 (trong batch và `data/source/`) giữ em dash của bản gốc: linter loại cột này và thư mục `data/source/` khỏi sweep.
- Greek giữ đủ dấu (accent + breathing); phiên âm chỉ là thông tin phụ, sinh từ bảng docs/TRANSLIT.md.
