# Quiz LED Solver

## Chạy tool

```bash
cd /home/amtia/tool/quiz-led-solver
python3 quiz_led.py --watch
```

> **Lưu ý**: Tool tự động điều khiển trực tiếp đèn phần cứng bàn phím (`brightnessctl`), không làm thay đổi trạng thái gõ chữ hoa/thường của Caps Lock. Nếu hệ thống không có `brightnessctl`, tool tự fallback sang `ydotool`.

## Mã nháy

```
A = 2 lần
B = 4 lần
C = 6 lần
D = 8 lần
E = 10 lần
F = 12 lần
```

## Test không nháy đèn

```bash
python3 quiz_led.py --watch --dry-run
```
