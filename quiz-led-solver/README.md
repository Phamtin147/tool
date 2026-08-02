# Quiz LED Solver

## Chạy tool

```bash
sudo ydotoold -p /run/user/$(id -u)/.ydotool_socket -P 0660 -o $(id -u):$(id -g) &
cd /home/amtia/tool/quiz-led-solver
python3 quiz_led.py --watch
```

Sau đó cứ chụp màn hình. Khi có ảnh mới trong `/home/amtia/Pictures/screenshots`, tool tự gửi Gemini và nháy Caps Lock đáp án.

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
