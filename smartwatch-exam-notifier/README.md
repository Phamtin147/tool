# Smartwatch Exam Notifier (Đẩy Đáp Án Lên Apple Watch / Mi Band / Wearables)

> **Tác giả:** Amtia / Phamtin147  
> **Repository:** [Phamtin147/tool](https://github.com/Phamtin147/tool)

Công cụ hỗ trợ thi kín đáo: Tự động chụp / quét màn hình câu hỏi $\to$ giải bằng **Gemini Vision AI** $\to$ bắn thông báo rung siêu ngắn gọn (khoảng 3 dòng) thẳng về **Apple Watch, Mi Band, Amazfit, Galaxy Watch** qua Telegram Bot hoặc kênh `ntfy.sh`.

---

## 🌟 Tại Sao Nên Dùng Tool Này?

- **Siêu kín đáo:** Thay vì nhìn màn hình máy tính hay nhìn đèn Caps Lock (như trong [quiz-led-solver](file:///Users/amtia/tool/quiz-led-solver)), bạn chỉ cần đeo đồng hồ thông minh trên tay. Khi có câu hỏi khó, đồng hồ khẽ rung nhẹ và hiện đáp án trên cổ tay.
- **Tối ưu hiển thị mặt đồng hồ:** Format rút gọn tối đa:
  ```text
  ANS: [ B ]
  WHY: Mergesort average O(n log n)
  CONF: 98%
  ```
- **Hai kênh thông báo:**
  1. **Telegram Bot:** Đẩy tin nhắn có rung qua ứng dụng Telegram trên điện thoại & đồng hồ.
  2. **ntfy.sh:** Dịch vụ push notification miễn phí, không cần tạo tài khoản hay bot token.

---

## 🚀 Hướng Dẫn Thiết Lập

### 1. Cấu hình Telegram Bot (Cách khuyên dùng cho Apple Watch)
1. Mở Telegram, tìm bot `@BotFather`, gửi lệnh `/newbot` và làm theo hướng dẫn để lấy `TELEGRAM_BOT_TOKEN`.
2. Tìm bot `@userinfobot` hoặc `@getmyid_bot` để lấy số `TELEGRAM_CHAT_ID` của bạn.
3. Gửi 1 tin nhắn bất kỳ cho con bot mới tạo để kích hoạt trò chuyện.
4. Copy file cấu hình:
   ```bash
   cp .config/config.env.example .config/config.env
   ```
5. Điền thông tin vào `.config/config.env`:
   ```env
   GEMINI_API_KEY=AIzaSy...
   TELEGRAM_BOT_TOKEN=123456789:ABC...
   TELEGRAM_CHAT_ID=987654321
   ```

---

## 💻 Cách Chạy Tool

### Chế độ 1: Chọn vùng câu hỏi trực tiếp (Snip & Solve)
```bash
python3 notifier.py --snip
```
Con trỏ chuột chuyển thành dấu chữ thập, bạn chỉ cần kéo chọn vùng câu hỏi trên màn hình. Trong 1.5 giây, đáp án sẽ rung trên đồng hồ!

### Chế độ 2: Tự động theo dõi thư mục ảnh màn hình (Watcher)
```bash
python3 notifier.py --watch ~/Desktop
```
Mỗi khi bạn bấm chụp màn hình (ví dụ `Cmd+Shift+4` trên Mac hoặc `Win+Shift+S` trên Windows), tool sẽ tự động bắt lấy ảnh mới nhất, giải và đẩy đáp án về đồng hồ ngay lập tức.

### Chế độ 3: Giải 1 file ảnh có sẵn
```bash
python3 notifier.py --image test_cau_hoi.png
```
