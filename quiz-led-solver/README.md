# 💡 Quiz LED Solver

Công cụ tự động giải bài trắc nghiệm từ ảnh chụp màn hình bằng **Vision AI** và phát tín hiệu đáp án bằng **nháy đèn bàn phím (Caps Lock LED)**.

---

## 🎯 Cơ chế hoạt động

1. **Theo dõi ảnh chụp:** Tự động phát hiện ảnh chụp màn hình mới nhất trong thư mục `~/Pictures/screenshots`.
2. **AI Vision phân tích:** Gửi ảnh câu hỏi tới **Google Gemini Vision API** (chạy đua song song các model `gemini-2.5-flash`, `gemini-2.0-flash` để lấy kết quả nhanh nhất ~0.5s - 1.2s).
3. **Báo đáp án qua đèn LED:** Nháy đèn Caps Lock trên bàn phím phần cứng theo số lần tương ứng với chữ cái đáp án.

---

## 🔢 Quy ước mã nháy đèn LED

| Đáp án | Số lần đèn nháy | Mô tả |
| :---: | :---: | :--- |
| **A** | **1 lần** | Nháy 1 cái |
| **B** | **2 lần** | Nháy 2 cái |
| **C** | **3 lần** | Nháy 3 cái |
| **D** | **4 lần** | Nháy 4 cái |
| **E** | **5 lần** | Nháy 5 cái |
| **F** | **6 lần** | Nháy 6 cái |

> [!NOTE]
> **Đối với câu hỏi chọn nhiều đáp án (Multi-select):**
> Ví dụ đáp án là **AC**: Tool sẽ nháy **1 lần** (cho chữ A), nghỉ ngắn 0.5s, sau đó nháy tiếp **3 lần** (cho chữ C).

---

## ⚙️ Cấu hình API Key

Tạo file cấu hình tại `.config/gemini.env`:

```bash
mkdir -p /home/amtia/tool/quiz-led-solver/.config
echo "GEMINI_API_KEY=your_gemini_api_key_here" > /home/amtia/tool/quiz-led-solver/.config/gemini.env
```

*(Hoặc xuất biến môi trường `export GEMINI_API_KEY="your_key"`)*.

---

## 🚀 Hướng dẫn sử dụng

### 1. Chế độ theo dõi tự động (`--watch` - Khuyên dùng)
Tool sẽ chạy nền, mỗi khi bạn chụp màn hình (ví dụ bằng phím `PrtScn` hoặc `Spectacle/Flameshot` lưu vào `~/Pictures/screenshots`), tool sẽ lập tức giải và nháy đèn:

```bash
cd /home/amtia/tool/quiz-led-solver
python3 quiz_led.py --watch
```

### 2. Giải một ảnh cụ thể:
```bash
python3 quiz_led.py --file /path/to/screenshot.png
```

### 3. Chạy thử nghiệm không nháy đèn (`--dry-run`):
```bash
python3 quiz_led.py --watch --dry-run
```

---

## 🛠️ Các tùy chọn nâng cao (CLI Options)

```text
Tùy chọn:
  --watch              Chạy chế độ lắng nghe ảnh chụp mới liên tục
  --file FILE          Chỉ định file ảnh câu hỏi cần giải
  --dry-run            In đáp án ra terminal, không nháy đèn
  --engine {gemini,ollama} Chọn engine AI (mặc định: gemini)
  --model MODEL        Chỉ định model AI cụ thể
  --blink-ms MS        Thời gian bật đèn mỗi lần nháy (mặc định: 120ms)
  --gap-ms MS          Thời gian tắt giữa các lần nháy (mặc định: 150ms)
  --poll-interval S    Tần số quét ảnh mới (mặc định: 0.3 giây)
```

---

## 📌 Lưu ý về điều khiển đèn bàn phím
* Tool ưu tiên dùng **`brightnessctl`** để điều khiển trực tiếp bóng đèn LED phần cứng bàn phím mà **không làm thay đổi trạng thái gõ chữ hoa/thường** của phím Caps Lock.
* Nếu hệ thống không có `brightnessctl`, tool tự động fallback sang `ydotool`.