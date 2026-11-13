# ROADMAP: pipeline gated

Mỗi phase chỉ mở khi phase trước qua đủ cổng QA. Trạng thái cập nhật sau mỗi push.

| Phase | Nội dung | Cổng QA để sang phase sau | Trạng thái |
| --- | --- | --- | --- |
| **T** | Term base (≥500 + 4 nhóm chuyên ngành) · decoder 1889 (~200) · whitelist đối chiếu chuẩn VN · linter + CI · ingest TEI nguồn → sense-ID | Cổng 1-4 chạy xanh trên seed + pilot nội bộ; whitelist đối chiếu xong | 🔄 skeleton |
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

- 2026-11-13: skeleton Phase T (README, LICENSE, 4 docs, 4 TSV seed, linter.py, CI). Phase T mở đầu.
