# LevelUp Video Control for Firefox

Extension Firefox này hỗ trợ điều khiển video thủ công trên `https://levelup.akajob.io/*`:

- Play/pause video trên tab hiện tại.
- Tua lùi/tới 10 giây bằng nút hoặc phím tắt.
- Tăng/giảm tốc độ phát, gồm các mức thường dùng như 1.5x và 2x.
- Tự chuyển sang tab kế tiếp chỉ sau khi video phát hết thật sự và browser nhận event `ended` từ thẻ `<video>`.

Extension này không tự tua video tới cuối và không bỏ qua nội dung bắt buộc.

## Cài tạm trong Firefox

1. Mở Firefox.
2. Vào `about:debugging#/runtime/this-firefox`.
3. Bấm `Load Temporary Add-on...`.
4. Chọn file:

   ```text
   /home/amtia/tool/firefox-video-control/manifest.json
   ```

5. Mở trang `https://levelup.akajob.io/` có video và thử popup extension hoặc phím tắt.

Lưu ý: temporary add-on sẽ mất sau khi tắt Firefox. Muốn dùng lâu dài thì cần đóng gói và ký add-on theo quy trình của Mozilla.

## Phím tắt mặc định

| Lệnh | Phím tắt |
| --- | --- |
| Play/pause | `Alt+Shift+P` |
| Tua lùi 10 giây | `Alt+Shift+Left` |
| Tua tới 10 giây | `Alt+Shift+Right` |
| Tăng tốc độ | `Alt+Shift+Up` |
| Giảm tốc độ | `Alt+Shift+Down` |
| Reset tốc độ về 1x | `Alt+Shift+R` |
| Bật/tắt auto-next sau khi video kết thúc | `Alt+Shift+N` |

Có thể đổi phím tắt tại:

```text
about:addons -> Manage Extension Shortcuts
```

## Dùng tốc độ 1.5x / 2x

Cách 1: bấm icon extension, dùng nút `Speed +` cho tới khi overlay hiện `Speed 1.5x` hoặc `Speed 2x`.

Cách 2: dùng phím `Alt+Shift+Up` để tăng tốc. Dùng `Alt+Shift+Down` để giảm tốc, `Alt+Shift+R` để quay lại 1x.

Các mức đang hỗ trợ:

```text
0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.5, 3, 3.5, 4
```

## Auto-next hoạt động thế nào

Khi bật `Tự chuyển tab khi video kết thúc thật`, content script lắng nghe event `ended` trên thẻ `<video>`. Khi video tự phát đến cuối, background script sẽ active tab kế tiếp trong cùng cửa sổ Firefox.

Nó không chuyển tab nếu:

- Không có video trên trang.
- Video chưa phát hết thật.
- Trang dùng player custom không phát event `ended` trên thẻ `<video>` thông thường.
- Tab kế tiếp không nằm trong cùng cửa sổ.

## Checklist debug cho hệ thống nội bộ

Dùng checklist này nếu đây là hệ thống nội bộ của bạn và bạn cần test player/training flow:

1. Xác nhận trang có thẻ `<video>` thật:

   ```javascript
   document.querySelectorAll("video")
   ```

2. Kiểm tra video có nhận lệnh play/pause không:

   ```javascript
   const video = document.querySelector("video");
   video.paused ? video.play() : video.pause();
   ```

3. Kiểm tra chỉnh tốc độ có bị player chặn không:

   ```javascript
   const video = document.querySelector("video");
   video.playbackRate = 1.5;
   video.playbackRate;
   ```

4. Kiểm tra event kết thúc video:

   ```javascript
   const video = document.querySelector("video");
   video.addEventListener("ended", () => console.log("video ended"));
   ```

5. Nếu extension không chạy, mở Browser Console bằng `Ctrl+Shift+J` và tìm log bắt đầu bằng `LevelUp Video Control`.
6. Nếu popup gửi lệnh nhưng trang không phản hồi, kiểm tra URL có khớp `https://levelup.akajob.io/*` không.
7. Nếu video nằm trong iframe khác domain, cần thêm host permission tương ứng vào `manifest.json`.

## Cấu trúc file

```text
firefox-video-control/
├── manifest.json
├── service-worker.js
├── content.js
├── popup.html
├── popup.css
├── popup.js
├── README.md
└── icon.png
```

---

## 👤 Tác giả (Author)
* **Amtia / Phamtin147**
* GitHub: [@Phamtin147](https://github.com/Phamtin147)
* Email: [huhume147@gmail.com](mailto:huhume147@gmail.com)

