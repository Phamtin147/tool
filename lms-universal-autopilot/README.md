# LMS Universal AutoPilot Pro (Canvas, Moodle, Blackboard & University LMS)

> **Tác giả:** Amtia / Phamtin147  
> **Repository:** [Phamtin147/tool](https://github.com/Phamtin147/tool)

Trình mở rộng (Browser Extension) tương thích **Google Chrome, Brave, MS Edge và Mozilla Firefox** (Manifest V3), tự động nhận diện câu hỏi trắc nghiệm, trích xuất đề bài và giải đáp án chuẩn xác bằng **Google Gemini AI** trên các nền tảng LMS phổ biến nhất.

---

## 🌟 Nền Tảng Hỗ Trợ

- **Canvas LMS** (`*.instructure.com` hoặc portal trường)
- **Moodle** (Hệ thống LMS của hầu hết các trường ĐH tại Việt Nam và quốc tế)
- **Blackboard Learn**
- **Google Forms** (Trắc nghiệm bài tập nhanh)
- **Generic LMS** (Tự động nhận diện cấu trúc thẻ câu hỏi và lựa chọn radio/checkbox tiêu chuẩn)

---

## 🚀 Tính Năng Chính

1. **Chế Độ Siêu Kín (Stealth Underline):**
   - Không tự động click đáp án nếu bạn không muốn.
   - Chỉ gạch chân nét đứt mờ màu xanh lá (`border-bottom: 2px dashed #10b981`) hoặc chấm nhỏ `•` cạnh phương án đúng để bạn tự bấm, chống giám sát từ camera và người đứng sau.
2. **Chế Độ Tự Động Điền (Auto Select):**
   - Tự động click vào đáp án đúng với độ trễ ngẫu nhiên mô phỏng người thật (`1.5s - 3.5s`), tránh bị hệ thống LMS phát hiện thao tác bot siêu tốc.
3. **Floating HUD Tiện Dụng:**
   - Widget nổi góc dưới màn hình hiển thị trực tiếp số câu hỏi tìm thấy và tiến độ giải theo thời gian thực.
4. **Hỗ Trợ Đa Dạng Model:**
   - Tương thích `gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-1.5-flash`.

---

## 📦 Hướng Dẫn Cài Đặt

### Trên Chrome / Edge / Brave / Cốc Cốc
1. Mở trình duyệt và truy cập: `chrome://extensions/`
2. Bật công tắc **Developer mode** (Chế độ dành cho nhà phát triển) ở góc trên bên phải.
3. Bấm **Load unpacked** (Tải tiện ích đã giải nén) và chọn thư mục:
   ```
   tool/lms-universal-autopilot
   ```
4. Click vào icon tiện ích trên thanh công cụ, nhập **Gemini API Key** và bấm **Lưu Cài Đặt**.

### Trên Firefox
1. Truy cập `about:debugging#/runtime/this-firefox`.
2. Bấm **Load Temporary Add-on...** và chọn file [manifest.json](file:///Users/amtia/tool/lms-universal-autopilot/manifest.json).
