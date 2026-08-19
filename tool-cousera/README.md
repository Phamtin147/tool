# 🚀 Coursera AutoPilot Pro (v1.3.0)

Tiện ích mở rộng (Browser Extension) hỗ trợ tự động hóa học tập, tua nhanh tiến độ và hỗ trợ giải bài tập trên **Coursera**.

---

## 🌟 Tính năng nổi bật

* ⏭️ **Skip & Next Week (Tự động nhảy tuần):** Tự động hoàn thành toàn bộ Video, Reading, Ungraded Lab, Discussion trong tuần hiện tại và **tự động chuyển sang tuần tiếp theo** (`/home/week/X`).
* ⚡ **Skip Full Course (1-Click toàn khóa):** Tự động hoàn thành tất cả các Module/Week trong toàn bộ khóa học từ đầu đến cuối chỉ với 1 lần bấm.
* 🤖 **Nhận diện thông minh:** Tự động lấy User ID, Course ID và cấu trúc khóa học qua API Coursera (không lo bị lỗi `"Environment search failed"`).
* 📋 **Copy Questions & Download Result:** Xuất đề thi Quiz chưa làm hoặc tải đáp án bài Quiz 100% điểm về máy tính dạng file JSON.
* ✍️ **Auto Grade & Fill Peer:** Tự động chấm điểm bài nộp của học viên khác và tự động nộp bài tập Peer Assignment.
* 🖥️ **Console thời gian thực:** Xem chi tiết tiến độ xử lý từng bài học ngay trên giao diện widget nổi.

---

## 📦 Hướng dẫn cài đặt

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

## 🎮 Hướng dẫn sử dụng

Khi truy cập vào bất kỳ khóa học nào trên Coursera (ví dụ: `https://www.coursera.org/learn/<tên_khóa_học>/...`), bảng điều khiển của tool sẽ xuất hiện ở **góc dưới cùng bên phải màn hình**.

### Chi tiết các nút chức năng:

| Nút bấm | Chức năng | Hướng dẫn chi tiết |
| :--- | :--- | :--- |
| **`Skip & Next Week`** | **Skip tuần hiện tại & Tự nhảy tuần mới** | Skip toàn bộ nội dung học trong tuần hiện tại, sau đó tự đếm ngược 2.5s và điều hướng sang tuần kế tiếp rồi tiếp tục chạy. |
| **`Skip Full Course`** | **Skip toàn bộ khóa học** | Gửi API hoàn thành toàn bộ các tuần/module từ Module 1 đến hết khóa học chỉ trong vài giây. |
| **`Download result`** | **Tải đáp án Quiz** | Khi đang ở trang kết quả Quiz đạt 100%, bấm nút này để tải file JSON lưu câu hỏi và đáp án. |
| **`Copy questions`** | **Copy câu hỏi Quiz** | Khi đang ở trang làm bài Quiz chưa giải, bấm nút này để copy toàn bộ câu hỏi vào Clipboard. |
| **`Auto grade`** | **Chấm điểm Peer Review** | Khi đang ở trang chấm bài bạn học, tự động chọn điểm tối đa và điền nhận xét tích cực. |
| **`Fill Peer`** | **Nộp bài Peer Assignment** | Khi đang ở trang nộp bài tập Peer, tự động tạo file và điền form nộp bài mẫu. |
| **`Disable grader`** | **Tắt AI Grader** | Ẩn và vô hiệu hóa bộ chấm tự động bằng AI (nếu khóa học có áp dụng). |
| **`Review URL`** | **Lấy link bài nộp Peer** | Copy đường dẫn bài nộp của bạn để nhờ bạn bè chấm chéo. |

---

## 💡 Lưu ý quan trọng
* Tool chỉ tự động hoàn thành các nội dung học tập không tính điểm (*Video, Reading, Ungraded Labs, Widgets, Discussions*).
* Các bài **Graded Quiz / Exam** sẽ được giữ nguyên để bạn tự làm hoặc dùng AI giải nhằm đảm bảo điểm số 100%.
