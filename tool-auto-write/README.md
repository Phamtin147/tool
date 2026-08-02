
chmod +x /home/amtia/tool/tool-auto-write/nap_da.sh

sudo ydotoold --socket-path /tmp/.ydotool_socket --socket-perm 0666

cd /home/amtia/tool
./nap_da.sh

python3 nhan_go.py
python3 tu_dong_go.py

## Ghi chú

- Nếu thấy lỗi `Connection refused` → daemon chưa chạy, quay lại Bước 1
- Nếu thấy lỗi `Permission denied` (socket) → chắc chắn chạy đúng lệnh ở Bước 1 với `sudo`
- Nếu muốn thay đổi thời gian chờ, sửa `SLEEP_TIME=5` trong `nap_da.sh`
