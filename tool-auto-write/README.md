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

## Hướng dẫn sử dụng từng bước

### Bước 1: Khởi động dịch vụ gõ phím `ydotoold` (Bắt buộc)

Trước khi gõ phím, cần bật daemon `ydotoold` chạy nền bằng lệnh:

```bash
sudo ydotoold --socket-path /tmp/.ydotool_socket --socket-perm 0666 &
sudo chmod 666 /tmp/.ydotool_socket
export YDOTOOL_SOCKET=/tmp/.ydotool_socket
```

> **Ghi chú:** Sau khi chạy lệnh trên, `ydotoold` sẽ chạy nền trong suốt phiên làm việc của bạn.

---

### Bước 2: Chuẩn bị nội dung đáp án / code

Mở file `dapan.txt` và dán nội dung văn bản hoặc code bạn muốn tool gõ vào:

```bash
nano /home/amtia/tool/tool-auto-write/dapan.txt
```
*(Sau khi dán xong, bấm `Ctrl + O` -> `Enter` để lưu và `Ctrl + X` để thoát).*

---

### Bước 3: Chạy script bắn phím tự động (`nap_da.sh`)

Chạy script:
```bash
cd /home/amtia/tool/tool-auto-write
chmod +x nap_da.sh
./nap_da.sh
```

**Cách hoạt động:**
1. Script hiện đếm ngược **5 giây**.
2. Bạn dùng chuột **click vào ô nhập liệu / cửa sổ máy ảo** cần gõ trong 5 giây này.
3. Sau 5 giây, tool sẽ tự động gõ toàn bộ nội dung trong `dapan.txt` vào vị trí con trỏ chuột với tốc độ cao.

---

### Bước 4: Sử dụng các script Python bổ trợ (Tùy chọn)

Nếu bạn muốn tùy biến nâng cao bằng Python:

* **`python3 auto_go.py`**: Tự động gõ với độ trễ từng ký tự có thể tùy chỉnh trong file code.
* **`python3 nhan_go.py`**: Lắng nghe phím tắt kích hoạt tự động gõ (bấm phím nóng để kích hoạt).
* **`python3 tu_dong_go.py`**: Chế độ gõ lặp lại tự động.

---

## Khắc phục sự cố thường gặp

### 1. Lỗi `Connection refused` hoặc `Cannot open socket`
Nguyên nhân do daemon `ydotoold` chưa chạy hoặc socket bị mất. Khởi động lại bằng:
```bash
sudo pkill ydotoold
sudo ydotoold --socket-path /tmp/.ydotool_socket --socket-perm 0666 &
sudo chmod 666 /tmp/.ydotool_socket
export YDOTOOL_SOCKET=/tmp/.ydotool_socket
```

### 2. Lỗi `Permission denied`
Cấp quyền đọc ghi cho socket:
```bash
sudo chmod 666 /tmp/.ydotool_socket
```

### 3. Điều chỉnh tốc độ gõ hoặc thời gian chờ
* **Thay đổi thời gian chờ click:** Mở file `nap_da.sh`, sửa dòng `SLEEP_TIME=5` thành số giây bạn muốn.
* **Thay đổi tốc độ gõ:** Trong file `nap_da.sh`, sửa `--key-delay 60` (giảm xuống 30 nếu muốn gõ nhanh hơn, hoặc tăng lên 100 để gõ chậm hơn).
