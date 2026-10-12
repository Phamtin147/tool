# 💡 Quiz LED Solver

Công cụ tự động giải bài trắc nghiệm từ ảnh chụp màn hình bằng **Vision AI** và phát tín hiệu đáp án bằng **nháy đèn bàn phím (Caps Lock LED)**.

---

## 🎯 Cơ chế hoạt động

1. **Theo dõi ảnh chụp chống trùng lặp (Anti-Duplicate Watch):** Tự động phát hiện ảnh chụp màn hình mới nhất trong thư mục `~/Pictures/screenshots`, đợi file ghi hoàn tất (`st_size` + `st_mtime_ns` ổn định) và kiểm tra chữ ký `SHA-256` để đảm bảo mỗi ảnh chỉ giải và nháy đèn **đúng 1 lần**.
2. **AI Vision phân tích (Ưu tiên Gemini 3.5):**
   - **Mặc định chủ lực:** Gọi thẳng **`gemini-3.5-flash-lite`** (hạn mức Free Tier rộng rãi **500 requests/ngày, 15 requests/phút**, tốc độ phản hồi nhanh và độ chính xác cao trên đề trắc nghiệm).
   - **Fallback thông minh & Cooldown tự động:** Chỉ khi model chính bị nghẽn mạng (`HTTP 503` / timeout) hoặc hết hạn mức (`HTTP 429`), hệ thống mới tự động chuyển tiếp tuần tự sang `gemini-3.5-flash` $\rightarrow$ `gemini-3-flash-preview` $\rightarrow$ `gemini-3.1-flash-lite`, đồng thời tạm nghỉ (cooldown) model lỗi để không gọi lặp gây chậm.
   - **Mở khóa suy luận (`maxOutputTokens: 1024`):** Đảm bảo các model có cơ chế Thinking suy luận trọn vẹn trước khi xuất chữ cái đáp án cuối cùng.
3. **Báo đáp án qua đèn LED an toàn:** Bộ lọc nghiêm ngặt chỉ chấp nhận đáp án hợp lệ từ **A–F** (tối đa 4 lựa chọn cho câu hỏi multi-select), tự động ép tắt đèn (`ensure_caps_off`) trong khối `try...finally` sau mỗi lần nháy hoặc khi dừng chương trình.

---

## 🔢 Quy ước mã nháy đèn LED

| Đáp án / Trạng thái | Số lần đèn nháy | Mô tả |
| :---: | :---: | :--- |
| **A** | **1 lần** | Nháy 1 cái |
| **B** | **2 lần** | Nháy 2 cái |
| **C** | **3 lần** | Nháy 3 cái |
| **D** | **4 lần** | Nháy 4 cái |
| **E** | **5 lần** | Nháy 5 cái |
| **F** | **6 lần** | Nháy 6 cái |
| **⚠️ Lỗi API / Ảnh không có câu hỏi** | **Chớp nhanh 3 cái (0.06s)** | Chớp siêu nhanh trong ~0.35s rồi tự động tắt hẳn đèn (chống treo/nháy loạn) |

> [!NOTE]
> **Đối với câu hỏi chọn nhiều đáp án (Multi-select):**
> Ví dụ đáp án là **AC**: Tool sẽ nháy **1 lần** (cho chữ A), nghỉ ngắn 1.0s, sau đó nháy tiếp **3 lần** (cho chữ C). Tối đa giới hạn ở các lựa chọn **A–F** (tối đa 4 đáp án) để chống nháy đèn liên tục khi AI trả về văn bản lỗi.

---

## ⚙️ Cấu hình API Key

Tạo file cấu hình tại `.config/gemini.env`:

```bash
mkdir -p /home/amtia/tool/quiz-led-solver/.config
echo "GEMINI_API_KEY=your_gemini_api_key_here" > /home/amtia/tool/quiz-led-solver/.config/gemini.env
```

> [!TIP]
> **Hỗ trợ xoay vòng nhiều API Key (Multi-Key Rotation):**
> Bạn có thể truyền nhiều key ngăn cách bằng dấu phẩy trong `GEMINI_API_KEY="key1,key2"` hoặc thêm `GEMINI_API_KEY_2`, `GEMINI_API_KEY_3` trong file `.config/gemini.env` để tự động đổi key khi hết quota.

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
  --watch                     Chạy chế độ lắng nghe ảnh chụp mới liên tục
  --image, --file FILE        Chỉ định file ảnh câu hỏi cần giải
  --dry-run                   In đáp án ra terminal, không nháy đèn
  --provider {auto,gemini,openrouter,ollama}
                              Chọn provider AI (mặc định: auto)
  --gemini-model MODEL        Chỉ định model Gemini cụ thể (mặc định: gemini-3.5-flash-lite)
  --race / --no-race          Bật/tắt chế độ bắn song song nhiều model (mặc định: --no-race)
  --error-blink / --no-error-blink
                              Bật/tắt chớp nhanh 3 lần khi lỗi API/ảnh không có câu hỏi (mặc định: bật)
  --interval, --blink-ms S    Thời gian bật/tắt đèn mỗi nhịp nháy tính bằng giây (mặc định: 0.35s)
  --group-interval, --gap-ms S Thời gian nghỉ giữa các chữ cái đáp án nhiều lựa chọn (mặc định: 1.0s)
  --poll, --poll-interval S   Tần số quét ảnh mới (mặc định: 0.4s)
```

---

## 📌 Lưu ý về điều khiển đèn bàn phím
* Tool ưu tiên dùng **`brightnessctl`** để điều khiển trực tiếp bóng đèn LED phần cứng bàn phím mà **không làm thay đổi trạng thái gõ chữ hoa/thường** của phím Caps Lock.
* Nếu hệ thống không có `brightnessctl`, tool tự động fallback sang `ydotool`.

---

## 👤 Tác giả (Author)
* **Amtia / Phamtin147**
* GitHub: [@Phamtin147](https://github.com/Phamtin147)
* Email: [huhume147@gmail.com](mailto:huhume147@gmail.com)