# Coursera AutoPilot Pro (v1.3.0)

Tiện ích mở rộng (Browser Extension) hỗ trợ tự động hóa học tập, tua nhanh tiến độ và tự động giải bài tập trắc nghiệm bằng Google Gemini AI trên nền tảng Coursera.

---

## Tính năng chính

* **AI Solve Quiz (Giải Quiz 1-Click):** Tự động đóng gói toàn bộ câu hỏi và đáp án trên trang Quiz gửi sang Gemini AI trong 1 request duy nhất, nhận đáp án và tự động click chọn thẳng vào các nút Radio/Checkbox trên màn hình.
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
3. Bấm nút **Load unpacked (Tải tiện ích đã giải nén)**.
4. Chọn thư mục:
   ```text
   /home/amtia/tool/tool-cousera
   ```
5. Tiện ích **Coursera AutoPilot Pro v1.3.0** sẽ xuất hiện trên thanh công cụ.

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

## Bảng chức năng

Khi truy cập vào khóa học trên Coursera, bảng điều khiển của tool sẽ hiển thị ở góc dưới bên phải màn hình.

| Nút bấm | Chức năng | Hướng dẫn chi tiết |
| :--- | :--- | :--- |
| `AI Solve Quiz` | Tự động giải Quiz bằng AI | Gửi toàn bộ câu hỏi trong 1 request duy nhất đến Gemini AI và tự động click chọn các đáp án đúng trên màn hình. |
| `Skip & Next Week` | Skip tuần hiện tại & Chuyển tuần mới | Skip toàn bộ nội dung trong tuần hiện tại, đếm ngược 2.5s rồi chuyển sang tuần tiếp theo. |
| `Skip Full Course` | Skip toàn bộ khóa học | Gửi API hoàn thành toàn bộ các tuần từ Module 1 đến hết khóa học. |
| `Download result` | Tải đáp án Quiz | Khi đang ở trang kết quả Quiz đạt 100%, tải file JSON lưu câu hỏi và đáp án về máy. |
| `Copy questions` | Copy câu hỏi Quiz | Khi đang ở trang làm bài Quiz, copy toàn bộ câu hỏi và đáp án vào Clipboard. |
| `Auto grade` | Chấm điểm Peer Review | Tự động chấm điểm tối đa và điền nhận xét khi chấm bài học viên khác. |
| `Fill Peer` | Nộp bài Peer Assignment | Tự động tạo file và điền form nộp bài mẫu cho bài tập Peer. |
| `Disable grader` | Tắt AI Grader | Vô hiệu hóa bộ chấm tự động bằng AI của khóa học (nếu có). |
| `Review URL` | Lấy link bài nộp Peer | Copy đường dẫn bài nộp của bạn để gửi nhờ chấm chéo. |

---

## Lưu ý
* Tính năng `AI Solve Quiz` chỉ click chọn đáp án trên màn hình và đóng viền xanh lá để bạn kiểm tra, không tự động bấm Submit.

---

## 👤 Tác giả (Author)
* **Amtia / Phamtin147**
* GitHub: [@Phamtin147](https://github.com/Phamtin147)
* Email: [huhume147@gmail.com](mailto:huhume147@gmail.com)

