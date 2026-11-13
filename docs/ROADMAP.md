# ROADMAP: pipeline gated

Mỗi phase chỉ mở khi phase trước qua đủ cổng QA. Trạng thái cập nhật sau mỗi push.

| Phase | Nội dung | Cổng QA để sang phase sau | Trạng thái |
| --- | --- | --- | --- |
| **T** | ~~Term base (≥500 + 4 nhóm chuyên ngành)~~ ✅ 786 dòng · ~~decoder 1889~~ ✅ 246 dòng · ~~bảng phiên âm hệ thống~~ ✅ (docs/TRANSLIT.md + generator 15/15) · ~~linter + CI~~ ✅ · ~~ingest TEI nguồn~~ ✅ (36.490 entry → 56.893 sense) · còn: cổng 1-4 chạy xanh trên pilot nội bộ; linter tích hợp đối chiếu generator (mở từ P0) | Cổng 1-4 chạy xanh trên seed + pilot nội bộ | 🔄 in progress |
| **P0** | Pilot 100 từ thông dụng nhất (đủ loại: động từ đa nghĩa, danh từ chuyên ngành, tên riêng, tiểu từ) | 5 cổng QA + duyệt người sở hữu 100% | ⏸ |
| **P1** | 1.000 từ theo cụm tri thức (5 cụm: tư duy/lời nói · chính trị/pháp lý · cho/nhận/đặt/đứng · tên riêng · tiểu từ/chuyên ngành) | 5 cổng + chỉ số nhất quán ổn định | ⏸ |
| **P2** | 10.000 từ (cụm tri thức + phần còn lại theo tần suất, có coverage assertion) | 5 cổng + spot-check 5% + back-translate 200 sense | ⏸ |
| **P3** | 40.000 từ còn lại + sweep + build `dict-core.js`/`dict-full.js` tự động từ bản đầy đủ | 6 cổng kiểm thử của báo cáo dict (round-trip paradigm ≥ 99,5%) | ⏸ |

## 5 cổng QA mỗi lô (fail một = không nhập lô)

Cổng 1, 2, 4 là linter tự động trong CI (báo đỏ = chặn merge); cổng 3 tự động phần phát hiện nhưng cảnh báo do người duyệt; cổng 5 chạy trên gold set corpus (John 1-5, Iliad 1, Anabasis 1).

1. **Termbase enforcement**: 100% khớp, 0 marker English sót trong gloss VI.
2. **Alignment**: 100% sense dịch gắn đúng sense-ID gốc; số sense gốc = số sense dịch + số sense `[chưa dịch]`.
3. **Back-translation spot-check**: ≥ 95% giữ nghĩa (LLM dịch VI → EN, so với EN gốc).
4. **Sweep**: NFC toàn bộ, 0 U+FFFD, 0 em dash, không CJK ngoài chủ đích.
5. **Gold-set check**: sense được dùng trong câu corpus mẫu phải dịch đúng theo phân tích tay.

## Chỉ số nhất quán công khai theo lô

Tỷ lệ khớp termbase · số sense `[chưa dịch]` · số cảnh báo alignment · số cảnh báo back-translation. Các chỉ số phải ổn định trước khi mở rộng lô sau.

## Lịch sử

- 2026-11-13 (batch 3): term base mở rộng lên 786 dòng (thêm 669 sau khi bỏ 4 key trùng: 190 marker/term ngữ pháp + 228 citations + 251 thuật ngữ chuyên ngành: quân sự, pháp lý Athens, y học, thực vật, hàng hải, tôn giáo, tu từ/chính trị); decoder 1889 lên 246 dòng (thêm 211 Victorian traps + từ cổ + idiom). Tool mới: `ingest_liddell.py` (TEI → ml-senses.tsv 56.893 dòng) và `translit_gen.py` (generator phiên âm, 15/15). Bảng ví dụ TRANSLIT.md §4 được đối chiếu và sửa lại 10/13 tên cho khớp generator (cổng duyệt §5.6). Format-SPEC thêm §4.1 (source TSV ingest).
- 2026-11-13: term base + decoder build-out batch 2 (117 + 35 dòng). Phiên âm chuyển sang thuần hệ thống (docs/TRANSLIT.md), bỏ whitelist ngoại lệ (D13 sửa đổi). Phase T mở đầu.
