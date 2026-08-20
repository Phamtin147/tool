# Coursera AutoPilot Pro (v1.4.0)

Tiện ích mở rộng (Browser Extension) hỗ trợ tự động hóa học tập, tua nhanh tiến độ và tự động giải bài tập trắc nghiệm / bài thi kiểm tra (Exam & Quiz) bằng Google Gemini AI trên nền tảng Coursera.

---

## Tính năng chính

* **AI Solve Quiz (Giải Quiz & Exam 1-Click):** Tự động bóc tách toàn bộ câu hỏi (kể cả trên trang bài thi bảo mật, CDS form, Tunnel Vision Exam, mã nguồn code, công thức toán), gửi sang Gemini AI trong 1 batch duy nhất và tự động click chọn thẳng vào các đáp án đúng trên màn hình (viền xanh nổi bật).
* **Phím tắt nhanh (`Alt + S` hoặc `Ctrl + Shift + S`):** Bấm phím tắt để tự động quét & giải bài thi ngay lập tức mà không cần click vào bảng điều khiển.
* **Tàng hình chống phát hiện (Anti-Cheat / Focus Spoofing):** Giữ trạng thái luôn Focus (`document.hasFocus() = true`, `visibilityState = visible`), chặn hoàn toàn các bộ bắt sự kiện chuyển tab, rời chuột hoặc mất tiêu điểm của Coursera, mở khóa chuột phải và copy/paste trên trang thi.
* **Skip & Next Week:** Tự động hoàn thành toàn bộ Video, Reading, Ungraded Lab, Discussion trong tuần hiện tại và tự động chuyển sang tuần tiếp theo (`/home/week/X`).
* **Skip Full Course:** Tự động hoàn thành tất cả các Module/Week trong toàn bộ khóa học từ đầu đến cuối chỉ với 1 lần bấm.
* **Nhận diện phiên học tự động:** Tự động lấy User ID, Course ID và cấu trúc khóa học qua API Coursera.
* **Copy Questions & Download Result:** Xuất đề thi Quiz chưa làm hoặc tải đáp án bài Quiz 100% điểm về máy tính dạng file JSON.
* **Auto Grade & Fill Peer:** Tự động chấm điểm bài nộp của học viên khác và tự động nộp bài tập Peer Assignment.
* **Console thời gian thực:** Xem chi tiết tiến độ xử lý từng bài học ngay trên giao diện widget nổi.

---

## Hướng dẫn cài đặt

### 1. Trên Google Chrome / Brave / Microsoft Edge / Cốc Cốc:
1. Mở trình duyệt và truy cập: `chrome://extensions/`
2. Bật công tắc **Developer mode (Chế độ dành cho nhà phát triển)** ở góc trên bên phải.
3. Bấm nút **Load unpacked (Tải tiện ích đã giải nén)** (hoặc bấm Reload nếu đã cài trước đó).
4. Chọn thư mục:
   ```text
   /home/amtia/tool/tool-cousera
   ```
5. Tiện ích **Coursera AutoPilot Pro v1.4.0** sẽ xuất hiện trên thanh công cụ.

### 2. Trên Mozilla Firefox:
1. Mở Firefox và truy cập: `about:debugging#/runtime/this-firefox`
2. Bấm nút **Load Temporary Add-on...**
3. Chọn file:
   ```text
   /home/amtia/tool/tool-cousera/manifest.json
   ```

---

## Cấu hình Gemini API Key & Model

1. Lấy API Key miễn phí tại [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Trên trang Coursera, bấm vào biểu tượng bánh răng (Cài đặt) ở góc trên bảng điều khiển nổi của tool.
3. Dán API Key vào ô `Gemini API Key`.
4. Chọn Model mong muốn tại ô `Gemini Model` (mặc định: `Gemini 3.7 Flash`).
5. Bấm **Save changes**. Key và Model sẽ được lưu vào bộ nhớ trình duyệt.

---

## Bảng chức năng & Phím tắt

Khi truy cập vào khóa học trên Coursera, bảng điều khiển của tool sẽ hiển thị ở góc dưới bên phải màn hình.

| Thao tác | Chức năng | Hướng dẫn chi tiết |
| :--- | :--- | :--- |
| **`Alt + S`** *(Phím tắt)* | **Giải bài nhanh (1-Click)** | Bấm phím tắt ở bất kỳ trang Quiz/Exam nào để tự động gửi toàn bộ câu hỏi sang AI và chọn đáp án. |
| `AI Solve Quiz` | Tự động giải Quiz bằng AI | Bấm nút trên widget để gửi câu hỏi đến Gemini AI và tự động click chọn các đáp án đúng trên màn hình. |
| `Skip & Next Week` | Skip tuần hiện tại & Chuyển tuần mới | Skip toàn bộ nội dung trong tuần hiện tại, đếm ngược 2.5s rồi chuyển sang tuần tiếp theo. |
| `Skip Full Course` | Skip toàn bộ khóa học | Gửi API hoàn thành toàn bộ các tuần từ Module 1 đến hết khóa học. |
| `Download result` | Tải đáp án Quiz | Khi đang ở trang kết quả Quiz đạt 100%, tải file JSON lưu câu hỏi và đáp án về máy. |
| `Copy questions` | Copy câu hỏi Quiz | Khi đang ở trang làm bài Quiz, copy toàn bộ câu hỏi và đáp án vào Clipboard. |
| `Auto grade` | Chấm điểm Peer Review | Tự động chấm điểm tối đa và điền nhận xét khi chấm bài học viên khác. |
| `Fill Peer` | Nộp bài Peer Assignment | Tự động tạo file và điền form nộp bài mẫu cho bài tập Peer. |
| `Disable AI Grader` | Tắt AI Grader | Vô hiệu hóa bộ chấm tự động bằng AI của khóa học (nếu có). |
| `Review URL` | Lấy link bài nộp Peer | Copy đường dẫn bài nộp của bạn để gửi nhờ chấm chéo. |

---

## Lưu ý
* Tính năng `AI Solve Quiz` chỉ click chọn đáp án trên màn hình và đóng viền xanh lá để bạn kiểm tra, không tự động bấm Submit.
* Tiện ích đã tích hợp sẵn cơ chế chống phát hiện chuyển tab / mất focus trên các bài thi khóa màn hình.

