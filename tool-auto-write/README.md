# Tool Auto Write (VM & Browser Keystroke Injector)

Công cụ hỗ trợ **tự động gõ phím / bắn nội dung văn bản (code, đáp án)** từ file vào các cửa sổ máy ảo (VMware, VirtualBox, RDP, Web Browser) mà không bị chặn clipboard hoặc chống paste.

---

## Mục đích sử dụng

* Sử dụng trên các hệ thống thi trắc nghiệm, máy ảo VM, trình duyệt hoặc môi trường thi khóa tính năng Copy/Paste.
* Công cụ mô phỏng gõ phím phần cứng thật thông qua **`ydotool`** với độ trễ phím tự nhiên, không thể bị phát hiện bởi JavaScript chặn paste.

---

## Cài đặt công cụ

Cài đặt package `ydotool` trên Linux:
```bash
sudo apt update && sudo apt install -y ydotool
```

---

## Cài đặt tự động chạy cùng hệ thống (Khuyên dùng - Chỉ cần làm 1 lần)

Để `ydotoold` **tự động chạy ngầm mỗi khi mở máy tính** (không cần phải gõ lệnh bật daemon thủ công mỗi lần dùng), chạy script cài đặt:

```bash
cd /home/amtia/tool/tool-auto-write
./setup_autostart.sh
```

> **Sau khi chạy xong:** Dịch vụ `ydotool` sẽ tự động khởi động cùng hệ điều hành ở chế độ nền vĩnh viễn. Mọi terminal mới mở đều tự nhận biến môi trường `YDOTOOL_SOCKET`.

---

## Hướng dẫn sử dụng hàng ngày

Khi đã cài đặt autostart xong, mỗi lần sử dụng bạn chỉ cần làm 2 bước cực kỳ đơn giản:

### Bước 1: Chuẩn bị nội dung đáp án / code
Mở file `dapan.txt` và dán nội dung văn bản hoặc code bạn muốn tool gõ vào:

```bash
nano /home/amtia/tool/tool-auto-write/dapan.txt
```
*(Bấm `Ctrl + O` -> `Enter` để lưu và `Ctrl + X` để thoát).*

---

### Bước 2: Bắn phím tự động (`nap_da.sh`)

Chạy script:
```bash
cd /home/amtia/tool/tool-auto-write
./nap_da.sh
```

**Cách hoạt động:**
1. Script hiện đếm ngược **5 giây**.
2. Bạn dùng chuột **click vào ô nhập liệu / cửa sổ máy ảo** cần gõ trong 5 giây này.
3. Sau 5 giây, tool sẽ tự động gõ toàn bộ nội dung trong `dapan.txt` vào vị trí con trỏ chuột.

---

## Các script Python bổ trợ (Tùy chọn)

* **`python3 auto_go.py`**: Tự động gõ với độ trễ từng ký tự có thể tùy chỉnh trong file code.
* **`python3 nhan_go.py`**: Lắng nghe phím tắt kích hoạt tự động gõ (bấm phím nóng để kích hoạt).
* **`python3 tu_dong_go.py`**: Chế độ gõ lặp lại tự động.

---

## Khắc phục sự cố & Tùy chỉnh

### 1. Khởi động thủ công (nếu không dùng autostart)
```bash
sudo pkill ydotoold
sudo ydotoold --socket-path /tmp/.ydotool_socket --socket-perm 0666 &
sudo chmod 666 /tmp/.ydotool_socket
export YDOTOOL_SOCKET=/tmp/.ydotool_socket
```

### 2. Điều chỉnh tốc độ gõ hoặc thời gian chờ
* **Thay đổi thời gian chờ click:** Mở file `nap_da.sh`, sửa dòng `SLEEP_TIME=5` thành số giây bạn muốn.
* **Thay đổi tốc độ gõ:** Trong file `nap_da.sh`, sửa `--key-delay 60` (giảm xuống 30 nếu muốn gõ nhanh hơn, hoặc tăng lên 100 để gõ chậm hơn).

---

## 👤 Tác giả (Author)
* **Amtia / Phamtin147**
* GitHub: [@Phamtin147](https://github.com/Phamtin147)
* Email: [huhume147@gmail.com](mailto:huhume147@gmail.com)

