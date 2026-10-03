# Bộ Công Cụ Tự Động Hóa & Hỗ Trợ Học Tập

> **Tác giả (Author):** **Amtia / Phamtin147**  
> **Repository:** [Phamtin147/tool](https://github.com/Phamtin147/tool)

Tổng hợp các công cụ tự động hóa, giải bài tập AI, hỗ trợ thi cử kín đáo và điều khiển trình duyệt/máy ảo do **Amtia / Phamtin147** phát triển.

---

## Danh sách các Tool trong Repository

| Thư mục | Tên Tool | Nền tảng | Chức năng chính |
| :--- | :--- | :--- | :--- |
| **[`tool-cousera/`](./tool-cousera/README.md)** | **Coursera AutoPilot Pro** | Chrome / Firefox Extension | Tự động giải & click đáp án Quiz theo lô bằng Gemini AI; Tự động skip Video, Reading, Labs, Discussions; Tự động nhảy tuần; Skip toàn khóa 1-Click. |
| **[`stealth-invisible-hud/`](./stealth-invisible-hud/README.md)** | **Stealth Invisible HUD** | Python / macOS / Windows / Linux | Cửa sổ HUD đáp án tàng hình trước Screen Share / Quay màn hình (Zoom, Meet, Teams, Safe Exam Browser); Snip & Solve bằng Gemini Vision AI. |
| **[`lms-universal-autopilot/`](./lms-universal-autopilot/README.md)** | **LMS AutoPilot Pro** | Chrome / Firefox Extension | Tự động quét và giải bài tập trắc nghiệm trên Canvas, Moodle, Blackboard, Google Forms & LMS các trường ĐH; Hỗ trợ chế độ siêu kín (Stealth Underline). |
| **[`smartwatch-exam-notifier/`](./smartwatch-exam-notifier/README.md)** | **Smartwatch Exam Notifier** | Python CLI | Tự động bắt ảnh chụp câu hỏi, gọi Vision AI giải đáp án và bắn thông báo rung siêu gọn qua Telegram Bot / ntfy.sh về Apple Watch, Mi Band, Amazfit. |
| **[`human-type-simulator/`](./human-type-simulator/README.md)** | **Human-Like Keystroke Simulator** | Python CLI (Cross-platform) | Giả lập gõ phím người thật với phân phối chuẩn Gaussian, tự gõ nhầm & backspace sửa lỗi để bypass kiểm tra nhịp gõ phím (Keystroke Dynamics) và chống paste. |
| **[`voice-interview-whisper/`](./voice-interview-whisper/README.md)** | **Voice Interview Whisper** | Python CLI | Trợ lý phỏng vấn kỹ thuật & thi vấn đáp trực tiếp; Phân tích âm thanh câu hỏi từ người phỏng vấn bằng Gemini Multimodal Audio và gợi ý 3 ý chính + code mẫu. |
| **[`quiz-led-solver/`](./quiz-led-solver/README.md)** | **Quiz LED Solver** | Python CLI (Linux) | Tự động quét ảnh chụp màn hình câu hỏi, gọi Vision AI giải đáp án và báo tín hiệu bằng nháy đèn bàn phím (Caps Lock LED). |
| **[`tool-auto-write/`](./tool-auto-write/README.md)** | **Tool Auto Write** | Bash / Python (`ydotool`) | Tự động gõ nội dung văn bản/code từ file vào các cửa sổ máy ảo VM, trình duyệt chống paste. |
| **[`firefox-video-control/`](./firefox-video-control/README.md)** | **LevelUp Video Control** | Firefox Extension | Điều khiển phát video, tăng tốc 1.5x/2x/4x, tự động chuyển tab khi video kết thúc trên nền tảng LevelUp Akajob. |

---

## Hướng dẫn nhanh cho các Tool mới

### 1. [Stealth Invisible HUD](./stealth-invisible-hud/README.md)
* **Khởi chạy:**
  ```bash
  cd stealth-invisible-hud
  python3 hud.py
  ```
* **Phím tắt:** `Cmd+S` để chọn vùng câu hỏi cần giải; `ESC` để ẩn cửa sổ khẩn cấp.

### 2. [LMS Universal AutoPilot Pro](./lms-universal-autopilot/README.md)
* **Cài đặt:** Nạp thư mục `lms-universal-autopilot/` vào `chrome://extensions/` (hoặc `about:debugging` trên Firefox).
* **Sử dụng:** Mở trang bài tập Canvas / Moodle / Blackboard, click `Quét & Giải Đề Này` trên widget nổi.

### 3. [Smartwatch Exam Notifier](./smartwatch-exam-notifier/README.md)
* **Khởi chạy:**
  ```bash
  cd smartwatch-exam-notifier
  python3 notifier.py --snip
  # Hoặc tự động quét khi chụp màn hình:
  python3 notifier.py --watch ~/Desktop
  ```
* **Kết quả:** Đẩy thông báo rung kèm đáp án trực tiếp về Telegram trên Apple Watch / Mi Band.

### 4. [Human-Like Keystroke Simulator](./human-type-simulator/README.md)
* **Khởi chạy:**
  ```bash
  cd human-type-simulator
  python3 human_typer.py --file sample_input.txt --wpm 70
  ```
* **Thao tác:** Chuyển sang cửa sổ máy ảo hoặc trang thi trong 5 giây đếm ngược.

### 5. [Voice Interview Whisper](./voice-interview-whisper/README.md)
* **Khởi chạy:**
  ```bash
  cd voice-interview-whisper
  python3 whisper_assistant.py --file question.m4a
  # Hoặc chế độ nhập câu hỏi nhanh:
  python3 whisper_assistant.py
  ```

---

## Chi tiết tài liệu
Nhấp vào tên thư mục của từng tool ở bảng trên để xem file **`README.md`** chi tiết với đầy đủ hướng dẫn cấu hình và xử lý lỗi.

---

## 👤 Tác giả (Author)
* **Amtia / Phamtin147**
* GitHub: [@Phamtin147](https://github.com/Phamtin147)
* Email: [huhume147@gmail.com](mailto:huhume147@gmail.com)
