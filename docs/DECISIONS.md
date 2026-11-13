# DECISIONS: protocol biên soạn (đã chốt 2026-11-13)

13 quyết định dưới đây là protocol chính thức của dự án, chốt bởi người sở hữu sau góp ý tư vấn. Mọi thay đổi sau này phải qua cổng duyệt (issue + review) và ghi lý do tại cuối file này. Nguyên tắc bao trùm: **không bịa**, mọi gloss truy vết được về sense gốc.

## Matrix quyết định

| # | Quyết định | Chốt |
| --- | --- | --- |
| D1 | Đầy đủ hay rút gọn? | **Hai sản phẩm tách bạch**: bản đầy đủ là tài nguyên gốc; `dict.js` rút gọn sinh ra TỪ bản đầy đủ theo tần suất. Không để hai cái tự phát triển độc lập |
| D2 | Thứ tự sense? | Bản đầy đủ giữ tuyệt đối thứ tự lịch sử của LSJ (đối chiếu học thuật quốc tế); bản rút gọn sắp theo tần suất hiện đại |
| D3 | Citations (Pl., Ar., Hdt., NT, LXX...)? | **Giữ nguyên viết tắt Latin chuẩn quốc tế**, kèm bảng chú giải tiếng Việt trong termbase. Không dịch citations |
| D4 | Markers ngữ pháp? | **Bảng thuật ngữ bắt buộc EN→VN áp dụng 100% đồng nhất** (`data/termbase-grammar.tsv`); linter từ chối lô vi phạm |
| D5 | Ai dịch, ai kiểm? | **Hybrid theo cụm tần suất**: top-500 review tay 100%; top-5.000 review nhanh từng sense; còn lại spot-check 5% + review toàn bộ entry trúng gold set. LLM draft không bao giờ vào bản final không qua review |
| D6 | Sense không chắc chắn? | **Không bịa**: giữ tiếng Anh trong ngoặc + tag `[chưa dịch]`. Thà để trống còn hơn dịch sai dây chuyền |
| D7 | Tên riêng trong gloss? | Phiên âm tiếng Việt theo whitelist + Latinh quốc tế trong ngoặc ở lần đầu xuất hiện (bản đầy đủ); bản rút gọn chỉ phiên âm Việt |
| D8 | Tiếng Anh 1889 cổ? | **Dịch theo nghĩa hiện đại đã kiểm định** (qua decoder `data/decoder-1889.tsv`, tra chéo LSJ9/Bailly khi cần); không dịch word-by-word các từ cổ gây lệch nghĩa |
| D9 | Phân tầng sense I/II/III + A/B/C? | **Giữ nguyên phân tầng** trong bản đầy đủ; bản rút gọn phẳng hoá + ghi số sense gốc để truy vết |
| D10 | Metadata nguồn? | **Bắt buộc**: mỗi sense VI mang sense-ID gốc (alignment); không có alignment thì không thể kiểm thử tự động |
| D11 | Repo nào? | **Repo riêng mới** `graecum-lexicon`, chứa bản đầy đủ + term base + whitelist + linter + CI; satzanalyse/graecum chỉ nhận dict.js rút gọn sinh từ đây |
| D12 | Định dạng dữ liệu? | **TSV 6 cột** cho term base/cẩm nang (schema: `docs/FORMAT-SPEC.md`), đồng phong cách hệ sinh thái, đọc được bởi người lẫn AI agent, là dữ liệu đầu vào trực tiếp của linter |
| D13 | Phiên âm tên riêng? | **SỬA ĐỔI 2026-11-13 (cuối ngày)**: phiên âm hoàn toàn theo bảng hệ thống `docs/TRANSLIT.md`, KHÔNG whitelist ngoại lệ, KHÔNG tách theo register; mọi tên (Attic, Homer, Koine) sinh từ cùng một bảng, letter-faithful, đuôi không rút gọn (-ς → s). Quyết định đầu ngày (register + whitelist) bị thay: ngoại lệ dẫn đến confusion và không kiểm thử tự động được |

## Nguyên tắc vận hành kèm theo

1. **Term base là luật, không phải gợi ý**; bổ sung thuật ngữ mới chỉ qua cổng duyệt.
2. **Không dịch theo alphabet**; P0/P1 dịch theo cụm tri thức (họ từ, ngành); từ P2 kèm coverage assertion (mỗi headword đúng một lô, tổng phủ 100%).
3. **Phiên âm không có ngoại lệ**: mọi tên sinh từ `docs/TRANSLIT.md`; sai khác với dạng sinh từ bảng = lỗi linter.
4. Trọng âm Greek → thanh sắc; mọi chữ cái được phiên âm, không rút gọn đuôi (chi tiết bảng TRANSLIT).

## Lịch sử thay đổi

- 2026-11-13 (cuối ngày): **D13 bị thay thế**: bỏ whitelist ngoại lệ và bỏ tách register; phiên âm thuần hệ thống theo `docs/TRANSLIT.md`. Lý do: ngoại lệ dẫn đến confusion; chỉ hệ thống letter-faithful mới deterministic và kiểm thử tự động được.
- 2026-11-13: chốt D1-D13 (nguyên bản theo khuyến nghị + góp ý tư vấn; D11-D13 chốt qua hỏi đáp với người sở hữu).
