#!/bin/bash

export YDOTOOL_SOCKET=/tmp/.ydotool_socket
FILE_DAP_AN="/home/amtia/tool/tool-auto-write/dapan.txt"
SLEEP_TIME=5

if [ ! -f "$FILE_DAP_AN" ]; then
    echo "Lỗi: File $FILE_DAP_AN không tồn tại!"
    exit 1
fi

# Đảm bảo socket có quyền ghi
if [ -S "$YDOTOOL_SOCKET" ]; then
    sudo chmod 666 "$YDOTOOL_SOCKET" 2>/dev/null
fi

# Tự động start ydotoold nếu chưa chạy
if ! ydotool key 0 &>/dev/null; then
    echo "Đang khởi động ydotoold..."
    sudo ydotoold --socket-path /tmp/.ydotool_socket --socket-perm 0666 &
    sleep 1.5
    sudo chmod 666 /tmp/.ydotool_socket 2>/dev/null

    if ! ydotool key 0 &>/dev/null; then
        echo "Lỗi: Không thể kết nối ydotoold."
        echo "Hãy chạy thủ công lệnh sau trên Terminal trước khi chạy script:"
        echo "  sudo ydotoold --socket-path /tmp/.ydotool_socket --socket-perm 0666 &"
        echo "  sudo chmod 666 /tmp/.ydotool_socket"
        exit 1
    fi
    echo "ydotoold đã sẵn sàng!"
fi

echo "Chuẩn bị... Bạn có $SLEEP_TIME giây để click vào cửa sổ máy ảo / ô nhập liệu!"
for ((i=SLEEP_TIME; i>0; i--)); do
    echo "Bắt đầu gõ sau: $i giây..."
    sleep 1
done

echo "Đang tự động gõ nội dung..."
ydotool type --key-delay 60 --file "$FILE_DAP_AN"

echo "Đã gõ xong toàn bộ nội dung trong dapan.txt!"
