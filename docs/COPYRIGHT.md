# COPYRIGHT: nguồn và giấy phép

## Nguồn biên soạn

| Nguồn | Trạng thái bản quyền | Cách dùng trong dự án |
| --- | --- | --- |
| *An Intermediate Greek-English Lexicon* (Middle Liddell), 1889, dựng trên LSJ 7th ed.; bản TEI Perseus số hoá | **Public domain** | Trục dịch chính; duy nhất nguồn được đưa vào pipeline tự động |
| LSJ 9th ed. (119k headwords, các bản số hoá lưu hành) | Coi là còn bản quyền cho tới khi xác minh từng kênh | Chỉ tra tay khi sense mơ hồ; không trích, không dịch tự động từ đây |
| Bailly 2020 (latin-dict.github.io) | CC có điều khoản NC-ND | Chỉ tra tay; không đưa vào pipeline (NC cấm phân phái repo công khai CC BY-SA) |
| DGE (Diccionario Griego-Español) | Bản quyền thương mại | Chỉ tra tay |
| Autenrieth (Homeric), Dodson (Koine, CC0), Thayer (PD), Middle Liddell bản khác | PD / CC0 | Tra chéo cụm Homer/Koine khi build term base |

## Giấy phép của dự án

- **Code** (tools/linter.py, build scripts): MIT (xem LICENSE).
- **Nội dung** (bản dịch tiếng Việt, term base, decoder, whitelist, mọi file trong data/): **CC BY-SA 4.0**. Bản dịch là tác phẩm phái sinh của nguồn public domain: người dự án giữ bản quyền bản dịch và cấp CC BY-SA 4.0 như toàn hệ sinh thái graecum/satzanalyse.
- **Sản phẩm phái sinh**: `dict-core.js`/`dict-full.js` sinh từ repo này cấp cho graecum-vn và satzanalyse kèm attribution nguồn (Middle Liddell PD + bản dịch CC BY-SA 4.0).

## Attribution bắt buộc khi tái sử dụng dữ liệu

> Dữ liệu phiên dịch từ *An Intermediate Greek-English Lexicon* (1889), public domain; bản tiếng Việt theo dự án graecum-lexicon, CC BY-SA 4.0.
