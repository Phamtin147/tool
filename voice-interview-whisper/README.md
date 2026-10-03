# Voice Interview Whisper (Trợ Lý Phỏng Vấn Kỹ Thuật & Vấn Đáp Âm Thanh)

> **Tác giả:** Amtia / Phamtin147  
> **Repository:** [Phamtin147/tool](https://github.com/Phamtin147/tool)

Trợ lý hỗ trợ phỏng vấn kỹ thuật trực tuyến (Live Coding, System Design, Thuật toán) và thi vấn đáp. Ứng dụng công nghệ **Gemini Multimodal Audio** phân tích trực tiếp luồng âm thanh câu hỏi từ người phỏng vấn/giám thị mà **không cần cài đặt thư viện Whisper nặng nề**, trả lời ngay sau ~1.5 giây với các **Gạch đầu dòng cốt lõi (Talking Points)** và code mẫu để bạn nhìn lướt và trả lời trôi chảy.

---

## 🌟 Tính Năng Nổi Bật

1. **Gemini Multimodal Audio Siêu Tốc:**
   - Đọc trực tiếp các định dạng âm thanh `.wav`, `.m4a`, `.mp3`, `.ogg`, `.flac`.
   - Vừa phiên âm (STT), vừa hiểu ngữ cảnh kỹ thuật, vừa sinh câu trả lời trong cùng 1 lần gọi API duy nhất.
2. **Cấu Trúc Câu Trả Lời Chuẩn Phỏng Vấn (Talking Points):**
   - Không đưa ra một đoạn văn dài dòng khó đọc khi đang nói chuyện.
   - Trả về đúng **3 ý chính cốt lõi (Điểm 1, Điểm 2, Điểm 3)** kèm thuật ngữ kỹ thuật và code snippet tối ưu.
3. **Đa Ngôn Ngữ Tự Động:**
   - Tự động nhận diện câu hỏi bằng Tiếng Việt hoặc Tiếng Anh và phản hồi đúng ngôn ngữ đó.
4. **Không Cần Cài Đặt Package:**
   - Chạy 100% bằng thư viện chuẩn Python 3.

---

## 🚀 Hướng Dẫn Sử Dụng

### 1. Cấu hình API Key
Sao chép và điền Gemini API Key:
```bash
cp .config/gemini.env.example .config/gemini.env
```

### 2. Các Chế Độ Chạy

#### Chế độ 1: Phân tích file ghi âm câu hỏi (.wav, .m4a, .mp3)
```bash
python3 whisper_assistant.py --file cau_hoi_interview.m4a
```

#### Chế độ 2: Chế độ tương tác nhanh (Console Loop)
```bash
python3 whisper_assistant.py
```
Trong chế độ này, bạn có thể gõ nhanh câu hỏi hoặc kéo thả đường dẫn file audio vào cửa sổ dòng lệnh để AI phân tích ngay tức thì.

#### Chế độ 3: Nhập trực tiếp câu hỏi bằng text
```bash
python3 whisper_assistant.py --question "Explain how Kafka ensures message ordering and fault tolerance"
```

---

## 💡 Mẹo Thiết Lập Audio Kín Đáo
- Trên **macOS**: Cài đặt **BlackHole 2ch** (Virtual Audio Cable miễn phí) để chuyển luồng âm thanh đầu ra từ Zoom/Google Meet vào một microphone ảo mà tool có thể ghi lại mà người phỏng vấn hoàn toàn không biết.
- Trên **Windows**: Bật **Stereo Mix** hoặc cài **VB-CABLE Virtual Audio Device**.
