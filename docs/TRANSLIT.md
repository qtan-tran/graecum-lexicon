# TRANSLIT: quy tắc phiên âm Hy Lạp cổ → tiếng Việt (hệ thống, KHÔNG ngoại lệ)

Người sở hữu chốt 2026-11-13: bỏ toàn bộ whitelist ngoại lệ; mọi tên riêng SINH từ bảng dưới đây. Bảng là nguồn chân lý duy nhất: dạng nào không khớp với bảng là lỗi (từ P0, linter kiểm tra bằng generator sinh dạng kỳ vọng rồi so sánh). Không phân biệt register: Attic, Homer, Koine dùng chung một bảng.

## 1. Phụ âm

| Greek | VI | Ghi chú |
| --- | --- | --- |
| β | b | |
| γ | g | γγ → ng; γκ → nk |
| δ | đ | |
| ζ | z | |
| θ | th | |
| κ | c | mọi vị trí, kể cả trước e/ê/i |
| λ | l | |
| μ | m | |
| ν | n | |
| ξ | x | |
| π | p | |
| ρ | r | ῥ đầu từ → rh |
| σ, ς | s | |
| τ | t | |
| φ | ph | |
| χ | kh | |
| ψ | ps | viết liền, kể cả đầu từ (Ψαμαθώ → Psamathô) |
| ἁ (rough breathing) | h | đầu từ đứng trước nguyên âm |

## 2. Nguyên âm

| Greek | VI | Ghi chú |
| --- | --- | --- |
| α | a | dấu dài/ngắn (ᾱ, ᾰ) bỏ |
| ε | e | |
| η | ê | |
| ι | i | |
| ο | o | |
| υ | y | khi đứng độc lập hoặc cuối từ |
| ω | ô | |

**Đôi:** αι → ai · ει → i · οι → oi · υι → ui · αυ → au · ευ → eu · ου → u.
**Iota dưới** (ᾳ, ῃ, ῳ): KHÔNG phiên âm (di sản hình thái của bản số hoá, không phải lỗi âm).

## 3. Thanh điệu

Trọng âm (acute/grave/circumflex xử như nhau) → **thanh sắc** trên nguyên âm của âm tiết mang trọng âm. Âm tiết không trọng âm → không dấu. Đặt dấu trên NGUYÊN ÂM của âm tiết (không phải trên phụ âm).

## 4. Đuôi

**Không rút gọn:** mọi chữ cái của tên gốc đều được phiên âm, kể cả `-ς` cuối từ. Không có quy tắc đặc biệt cho -ης/-ων/-ος; chúng đi qua bảng chữ cái như thường.

| Greek | Dạng sinh từ bảng | Dạng cũ kiểu Pháp (đã bỏ) |
| --- | --- | --- |
| Σωκράτης | Sôcrátês | Sôcrát |
| Σοφοκλῆς | Sôphôclês | Sôphôclês |
| Πλάτων | Platôn | Platôn |
| Ξενοφῶν | Xênôphôn | Xênôphông |
| Δημοσθένης | Dêmôstênês | Dêmôxtên |
| Θουκυδίδης | Thucudídês | Tucidit |
| Ἡρόδοτος | Hêródotos | Hêrôđôt |
| Ὅμηρος | Hômerôs | Hôme |
| Ἰωάννης | Iôánnês | Giăng |
| Ἀθῆναι | Athênai | Aten |
| Σπάρτη | Spártê | Spác-ta |
| Πειραιεύς | Peiraieús | Pirê |
| Δελφοί | Delphoí | Đelfoi |

(Nguyên tắc chọn letter-faithful: các dạng rút gọn kiểu Pháp không suy ngược được từ một quy tắc duy nhất; chỉ letter-faithful mới deterministic và kiểm thử tự động được.)

## 5. Áp dụng trong từ điển

1. Headword luôn giữ dạng Greek (NFC, đủ dấu); phiên âm chỉ là thông tin phụ.
2. Tên riêng trong gloss: chỉ dùng dạng sinh từ bảng. Bản đầy đủ ghi kèm Latinh quốc tế trong ngoặc ở lần đầu xuất hiện; bản rút gọn chỉ ghi dạng tiếng Việt.
3. Citations (Pl., Ar., Hdt., NT, LXX...) KHÔNG phiên âm (quyết định D3).
4. Tên riêng chỉ biết dạng Latinh (không có headword Greek): giữ nguyên Latinh trong ngoặc, KHÔNG tự phiên âm theo phán đoán; cập nhật khi xác định được dạng Greek gốc.
5. Sai khác giữa tên trong gloss và dạng sinh từ bảng = lỗi linter, từ chối lô.
6. Bảng chỉ được sửa qua cổng duyệt; mọi sửa đổi phải kèm bảng so sánh hệ quả (ví dụ mục 4).
