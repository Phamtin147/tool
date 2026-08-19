#!/bin/bash

# Setup auto-start service for ydotoold on boot (Systemd)

echo "=== Cấu hình tự động chạy ydotoold khi mở máy ==="

YDOTOOLD_PATH=$(which ydotoold)

if [ -z "$YDOTOOLD_PATH" ]; then
    echo "Lỗi: Không tìm thấy ydotoold. Hãy cài đặt: sudo apt install -y ydotool"
    exit 1
fi

# 1. Tạo file service cho systemd
SERVICE_FILE="/etc/systemd/system/ydotool.service"
echo "Đang tạo file service tại $SERVICE_FILE..."

sudo bash -c "cat <<EOF > $SERVICE_FILE
[Unit]
Description=ydotool background daemon
Documentation=man:ydotoold(8)
After=network.target

[Service]
Type=simple
ExecStart=$YDOTOOLD_PATH --socket-path=/tmp/.ydotool_socket --socket-perm=0666
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF"

# 2. Reload systemd và kích hoạt service khởi động cùng máy
echo "Đang kích hoạt service tự chạy cùng máy..."
sudo pkill ydotoold 2>/dev/null
sudo systemctl daemon-reload
sudo systemctl enable ydotool.service
sudo systemctl restart ydotool.service

# 3. Thêm biến môi trường vào ~/.bashrc và ~/.zshrc
ENV_LINE='export YDOTOOL_SOCKET=/tmp/.ydotool_socket'

if [ -f "$HOME/.bashrc" ] && ! grep -q "YDOTOOL_SOCKET" "$HOME/.bashrc"; then
    echo "$ENV_LINE" >> "$HOME/.bashrc"
    echo "Đã thêm YDOTOOL_SOCKET vào ~/.bashrc"
fi

if [ -f "$HOME/.zshrc" ] && ! grep -q "YDOTOOL_SOCKET" "$HOME/.zshrc"; then
    echo "$ENV_LINE" >> "$HOME/.zshrc"
    echo "Đã thêm YDOTOOL_SOCKET vào ~/.zshrc"
fi

export YDOTOOL_SOCKET=/tmp/.ydotool_socket
sleep 1
sudo chmod 666 /tmp/.ydotool_socket 2>/dev/null

# 4. Kiểm tra trạng thái
if sudo systemctl is-active --quiet ydotool.service; then
    echo ""
    echo "Thành công! ydotoold đã được cài đặt tự động chạy khi bật máy."
    echo "Trạng thái service: ACTIVE (Đang chạy)"
    echo "Từ giờ mỗi khi mở máy lên, bạn chỉ cần chạy trực tiếp ./nap_da.sh mà không cần gõ lệnh gì thêm!"
else
    echo "Cảnh báo: Service chưa chạy thành công. Kiểm tra lại bằng: sudo systemctl status ydotool.service"
fi
