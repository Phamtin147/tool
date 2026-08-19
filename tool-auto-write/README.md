# ⌨️ Tool Auto Write (VM & Browser Keystroke Injector)

Công cụ hỗ trợ **tự động gõ phím / bắn nội dung văn bản (code, đáp án)** từ file vào các cửa sổ máy ảo (VMware, VirtualBox, RDP, Web Browser) mà không bị chặn clipboard hoặc chống paste.

---

## 🎯 Mục đích sử dụng

* Sử dụng trên các hệ thống thi trắc nghiệm, máy ảo VM, trình duyệt hoặc môi trường thi khóa tính năng Copy/Paste.
* Công cụ mô phỏng gõ phím phần cứng thật thông qua **`ydotool`** với độ trễ phím tự nhiên, không thể bị phát hiện bởi JavaScript chặn paste.

---

## 📋 Yêu cầu hệ thống

Cài đặt `ydotool`:
```bash
sudo apt install -y ydotool
```

---

## 🚀 Hướng dẫn sử dụng từng bước

### Bước 1: Chuẩn bị nội dung đáp án
Mở file `dapan.txt` và dán nội dung văn bản hoặc code bạn muốn tool gõ vào:

```bash
nano /home/amtia/tool/tool-auto-write/dapan.txt
```

---

### Bước 2: Cấp quyền thực thi và chạy bắn phím (`nap_da.sh`)

Chạy script:
```bash
cd /home/amtia/tool/tool-auto-write
chmod +x nap_da.sh
./nap_da.sh
```

**Cách hoạt động của script:**
1. Script sẽ kiểm tra và tự khởi động background daemon `ydotoold` (nếu chưa chạy).
2. Hiện thông báo đếm ngược **5 giây**.
3. Bạn dùng chuột **click vào ô nhập liệu / cửa sổ máy ảo** cần gõ trong 5 giây này.
4. Sau 5 giây, tool sẽ tự động gõ toàn bộ nội dung trong `dapan.txt` vào ô nhập liệu với tốc độ cao.

---

### Bước 3: Sử dụng các script Python bổ trợ

* **`python3 auto_go.py`**: Tự động gõ với độ trễ từng ký tự có thể tùy chỉnh trong code.
* **`python3 nhan_go.py`**: Lắng nghe phím tắt kích hoạt tự động gõ.
* **`python3 tu_dong_go.py`**: Chế độ gõ lặp lại tự động.

---

## ⚠️ Khắc phục sự cố thường gặp

* **Lỗi `Connection refused`**: Daemon `ydotoold` chưa chạy. Khởi động thủ công bằng:
  ```bash
  sudo ydotoold --socket-path /tmp/.ydotool_socket --socket-perm 0666 &
  ```
* **Lỗi `Permission denied (socket)`**: Chạy lệnh cấp quyền socket:
  ```bash
  sudo chmod 666 /tmp/.ydotool_socket
  ```
* **Muốn tăng/giảm thời gian chờ trước khi gõ:** Mở file `nap_da.sh`, sửa biến `SLEEP_TIME=5` (mặc định 5 giây) thành thời gian bạn muốn.
