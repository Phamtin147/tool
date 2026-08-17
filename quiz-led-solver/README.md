# Quiz LED Solver

## Chạy tool

```bash
cd /home/amtia/tool/quiz-led-solver
python3 quiz_led.py --watch
```

> **Lưu ý**: Tool tự động điều khiển trực tiếp đèn phần cứng bàn phím (`brightnessctl`), không làm thay đổi trạng thái gõ chữ hoa/thường của Caps Lock. Nếu hệ thống không có `brightnessctl`, tool tự fallback sang `ydotool`.

## Mã nháy

```
A = 1 lần
B = 2 lần
C = 3 lần
D = 4 lần
E = 5 lần
F = 6 lần
```

## Test không nháy đèn

```bash
python3 quiz_led.py --watch --dry-run
```