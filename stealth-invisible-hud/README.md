# Stealth Invisible HUD (Cửa Sổ Đáp Án Tàng Hình Trước Screen Share & Proctoring)

> **Tác giả:** Amtia / Phamtin147  
> **Repository:** [Phamtin147/tool](https://github.com/Phamtin147/tool)

Cửa sổ HUD nổi (Always-On-Top) hiển thị đáp án và tóm tắt bài thi bằng AI, tích hợp cơ chế bảo vệ cấp hệ điều hành giúp **hoàn toàn tàng hình** trước các phần mềm quay/chụp màn hình và chia sẻ màn hình (Zoom, Google Meet, Microsoft Teams, QuickTime Player, Safe Exam Browser).

---

## 🌟 Tính Năng Nổi Bật

1. **Cơ chế Tàng hình Tuyệt đối (Screen-Capture Immunity):**
   - **macOS:** Sử dụng Cocoa API `NSWindow.setSharingType_(0)` (`NSWindowSharingNone`). Khi chia sẻ toàn màn hình hoặc quay video màn hình, cửa sổ HUD này sẽ tự động biến mất khỏi video stream.
   - **Windows:** Sử dụng Win32 API `SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)`.
2. **Snip & Solve Siêu Tốc:**
   - Bấm `Cmd+S` (macOS) hoặc click `Snip Question` để quét nhanh vùng câu hỏi trắc nghiệm trên màn hình.
   - Tự động gửi ảnh lên Gemini Vision AI giải đáp án trong ~1.5 giây.
3. **Phím Khẩn Cấp (Panic Key):**
   - Bấm `ESC` để ẩn cửa sổ HUD ngay lập tức khi giám thị hoặc người khác bước đến.
4. **Tùy Chỉnh Độ Trong Suốt (Opacity):**
   - Thanh trượt chỉnh độ mờ linh hoạt từ 20% đến 100%.
5. **Không Phụ Thuộc Thư Viện Ngoài:**
   - Chạy hoàn toàn trên Python 3 Standard Library (`tkinter`, `ctypes`, `urllib`). Không bắt buộc cài bất kỳ package nặng nào.

---

## 🚀 Hướng Dẫn Sử Dụng

### 1. Cấu hình Gemini API Key
Tạo file cấu hình `.config/gemini.env`:
```bash
cp .config/gemini.env.example .config/gemini.env
```
Mở file và dán key của bạn:
```env
GEMINI_API_KEY=AIzaSy...
```
*(Hoặc có thể nhập trực tiếp trên nút `🔑 API Key` của giao diện)*

### 2. Khởi chạy Tool
```bash
cd stealth-invisible-hud
python3 hud.py
```

### 3. Phím Tắt Tiện Dụng
| Phím tắt | Chức năng |
| :--- | :--- |
| `Cmd + S` / `Ctrl + S` | Bật công cụ chọn vùng màn hình để giải câu hỏi |
| `ESC` | Ẩn nhanh cửa sổ HUD (Panic Mode) |
| Click giữ thanh tiêu đề | Kéo thả di chuyển HUD đến bất kỳ vị trí nào trên màn hình |
