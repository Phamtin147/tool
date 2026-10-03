# Human-Like Keystroke Simulator (Bypass Chống Paste & Phát Hiện Bot Gõ Phím)

> **Tác giả:** Amtia / Phamtin147  
> **Repository:** [Phamtin147/tool](https://github.com/Phamtin147/tool)

Phiên bản nâng cấp toàn diện từ [tool-auto-write](file:///Users/amtia/tool/tool-auto-write). Giả lập hành vi gõ phím của con người với độ chân thực 100%, vượt qua các hệ thống giám sát thi cử, phỏng vấn lập trình (HackerRank, LeetCode, CodeSignal, Safe Exam Browser) có cơ chế phân tích nhịp gõ phím (**Keystroke Dynamics**).

---

## 🌟 Tại Sao Tool Này Khác Biệt?

Hầu hết các tool auto-type thông thường gõ với độ trễ cố định hoặc ngẫu nhiên phẳng (`random.uniform(0.1, 0.2)`). Các thuật toán giám sát thi cử hiện đại sẽ phát hiện ngay vì không có phân phối sinh học của con người.

Tool này áp dụng các kỹ thuật mô phỏng người thật:
1. **Phân Phối Chuẩn Gaussian (Gaussian Jitter):**
   - Khoảng cách thời gian giữa các phím dao động tự nhiên quanh tốc độ WPM mong muốn.
2. **Mô Phỏng Gõ Nhầm & Tự Sửa Lỗi (Typo & Backspace Simulation):**
   - Dựa trên ma trận các phím lân cận trên bàn phím QWERTY (ví dụ: gõ phím `e` có thể nhầm sang `w`, `r` hoặc `d`).
   - Tool sẽ gõ nhầm ký tự, dừng lại khoảng 150ms - 300ms (như con người nhận ra lỗi sai), bấm `Backspace` để xóa, rồi gõ lại ký tự đúng!
3. **Độ Trễ Dừng Nghĩ (Thinking & Punctuation Pause):**
   - Gặp dấu xuống dòng `\n`, dấu chấm `.`, dấu phẩy `,` hoặc dấu ngoặc nhọn `{}` tool sẽ tạm dừng tự nhiên như một lập trình viên đang suy nghĩ logic dòng tiếp theo.
4. **Hỗ Trợ Đa Nền Tảng (Cross-Platform):**
   - **macOS:** Tự động dùng `osascript` (System Events) tích hợp sẵn trong hệ điều hành.
   - **Linux:** Hỗ trợ cả `ydotool` (Wayland & X11) và `xdotool` (X11).

---

## 🚀 Hướng Dẫn Sử Dụng

### Gõ nội dung từ một file code/văn bản
```bash
cd human-type-simulator
python3 human_typer.py --file sample_input.txt --wpm 70
```

### Các tùy chọn nâng cao
| Tham số | Ý nghĩa | Mặc định |
| :--- | :--- | :--- |
| `-f, --file` | Đường dẫn file chứa nội dung cần gõ | `sample_input.txt` |
| `-t, --text` | Chuỗi văn bản trực tiếp | Không |
| `--wpm` | Tốc độ gõ (Words Per Minute) | `65` WPM |
| `--typo-rate` | Tỷ lệ gõ nhầm cố ý (0.025 = 2.5%) | `0.025` |
| `--no-typo` | Tắt chế độ gõ nhầm (chỉ gõ chuẩn) | Tắt |
| `--countdown` | Số giây đếm ngược để chuyển sang cửa sổ đích | `5` giây |

### Ví dụ gõ tốc độ cao 90 WPM không typo
```bash
python3 human_typer.py --file dapan.py --wpm 90 --no-typo
```
