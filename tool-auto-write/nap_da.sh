#!/bin/bash

export YDOTOOL_SOCKET=/tmp/.ydotool_socket
FILE_DAP_AN="/home/amtia/tool/tool-auto-write/dapan.txt"
SLEEP_TIME=5

if [ ! -f "$FILE_DAP_AN" ]; then
    echo "Lỗi: File $FILE_DAP_AN không tồn tại!"
    exit 1
fi

# Tự động start ydotoold nếu chưa chạy
if ! ydotool key 0 &>/dev/null; then
    echo "Đang khởi động ydotoold..."
    sudo ydotoold --socket-path /tmp/.ydotool_socket --socket-perm 0666 &
    sleep 1  # Chờ daemon sẵn sàng

    # Kiểm tra lại
    if ! ydotool key 0 &>/dev/null; then
        echo "Lỗi: Không thể khởi động ydotoold."
        echo "Thử chạy thủ công: sudo usermod -aG input \$USER rồi logout/login lại"
        exit 1
    fi
    echo "ydotoold đã sẵn sàng!"
fi

echo "Chuẩn bị... Bạn có $SLEEP_TIME giây để click vào máy ảo!"
sleep $SLEEP_TIME

# Kiểm tra ydotoold có đang chạy không
if ! ydotool key 0 &>/dev/null; then
    echo "Lỗi: ydotoold chưa chạy! Hãy chạy: sudo ydotoold --socket-path /tmp/.ydotool_socket --socket-perm 0666"
    exit 1
fi

ydotool type --key-delay 80 --file "$FILE_DAP_AN"

echo "Đã bắn xong đáp án!"
