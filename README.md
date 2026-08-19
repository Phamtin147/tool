# 🛠️ Bộ Công Cụ Tự Động Hóa & Hỗ Trợ Học Tập (Tool Suite)

Tổng hợp các công cụ tự động hóa, giải bài tập AI và điều khiển trình duyệt/máy ảo.

---

## 📂 Danh sách các Tool trong Repository

| Thư mục | Tên Tool | Nền tảng | Chức năng chính |
| :--- | :--- | :---: | :--- |
| **[`tool-cousera/`](./tool-cousera/README.md)** | **Coursera AutoPilot Pro** | Chrome / Firefox Extension | Tự động giải & click đáp án Quiz bằng Gemini AI; Tự động skip Video, Reading, Labs, Discussions; Tự động nhảy tuần; Skip toàn khóa 1-Click. |
| **[`quiz-led-solver/`](./quiz-led-solver/README.md)** | **Quiz LED Solver** | Python CLI (Linux) | Tự động quét ảnh chụp màn hình câu hỏi, gọi Vision AI giải đáp án và báo tín hiệu bằng nháy đèn bàn phím (Caps Lock LED). |
| **[`tool-auto-write/`](./tool-auto-write/README.md)** | **Tool Auto Write** | Bash / Python (`ydotool`) | Tự động gõ nội dung văn bản/code từ file vào các cửa sổ máy ảo VM, trình duyệt chống paste. |
| **[`firefox-video-control/`](./firefox-video-control/README.md)** | **LevelUp Video Control** | Firefox Extension | Điều khiển phát video, tăng tốc 1.5x/2x/4x, tự động chuyển tab khi video kết thúc trên nền tảng LevelUp Akajob. |

---

## 🚀 Hướng dẫn nhanh cho từng Tool

### 1. [Coursera AutoPilot Pro](./tool-cousera/README.md)
* **Cài đặt:** Nạp thư mục `tool-cousera/` vào `chrome://extensions/` (chế độ Developer mode).
* **Sử dụng:** Vào khóa học Coursera, bấm **`Skip & Next Week`** hoặc **`Skip Full Course`** ở widget góc dưới bên phải.

### 2. [Quiz LED Solver](./quiz-led-solver/README.md)
* **Cài đặt key:** Tạo file `quiz-led-solver/.config/gemini.env` chứa `GEMINI_API_KEY=...`
* **Chạy tool:**
  ```bash
  cd /home/amtia/tool/quiz-led-solver
  python3 quiz_led.py --watch
  ```
* **Mã nháy đèn:** A=1 lần, B=2 lần, C=3 lần, D=4 lần, E=5 lần, F=6 lần.

### 3. [Tool Auto Write](./tool-auto-write/README.md)
* **Chuẩn bị:** Điền đáp án/code vào `tool-auto-write/dapan.txt`
* **Chạy tool:**
  ```bash
  cd /home/amtia/tool/tool-auto-write
  ./nap_da.sh
  ```
* **Thao tác:** Click chuột vào ô nhập liệu cần gõ trong vòng 5 giây đếm ngược.

### 4. [LevelUp Video Control](./firefox-video-control/README.md)
* **Cài đặt:** Nạp `firefox-video-control/manifest.json` trong `about:debugging#/runtime/this-firefox`.
* **Phím tắt nhanh:** `Alt+Shift+P` (Play/Pause), `Alt+Shift+Up` (Tăng tốc 1.5x/2x), `Alt+Shift+N` (Auto-next tab).

---

## 📄 Chi tiết tài liệu
Nhấp vào tên thư mục của từng tool ở bảng trên để xem file **`README.md`** chi tiết với đầy đủ hướng dẫn cấu hình và xử lý lỗi.
