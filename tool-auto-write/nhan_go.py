#!/usr/bin/env python3
"""
nhan_go.py - Nhấn phím bất kỳ -> tự động gõ đúng 1 ký tự trong dapan.txt.
Cơ chế Grab bàn phím thật + UInput tầng kernel (tàng hình trước camera & giám thị).

Cải tiến & Tính năng:
- ⚡ Tối ưu hiệu năng: Khởi tạo 1 UInput instance dùng lại xuyên suốt, không tạo/hủy thiết bị liên tục.
- 🔄 Hỗ trợ phím Backspace: Lùi lại 1 ký tự trong đáp án đồng thời xóa ký tự trên màn hình đích.
- 🔤 Chuẩn hóa Unicode & Tiếng Việt: Tự động chuyển dấu tiếng Việt và ký tự đặc biệt sang bảng mã an toàn, không văng lỗi.
- ⏸️ Phím nóng F12 (hoặc Pause/Break): Tạm dừng (nhả bàn phím dùng bình thường) và Tiếp tục gõ.
- 🛑 Phím nóng F10 (hoặc Ctrl+C): Dừng khẩn cấp, thoát ngay lập tức và ungrab an toàn.
- 🛡️ Tự động kiểm tra quyền truy cập (/dev/uinput, evdev) và tự động gọi sudo nếu thiếu quyền.

Developed by: Amtia / Phamtin147 (https://github.com/Phamtin147)
"""

import os
import sys
import time
import signal
import select
import unicodedata
from pathlib import Path

# Kiểm tra & import evdev
try:
    import evdev
    from evdev import UInput, ecodes
except ImportError:
    print("[!] Chưa cài đặt evdev. Đang cài đặt...", file=sys.stderr)
    os.system(f"{sys.executable} -m pip install evdev")
    import evdev
    from evdev import UInput, ecodes

DEFAULT_FILE_DAP_AN = Path(__file__).resolve().parent / "dapan.txt"

# Bảng mã ánh xạ ký tự -> (keycode, can_shift)
KEY_MAP = {}
for c in 'abcdefghijklmnopqrstuvwxyz':
    KEY_MAP[c] = (getattr(ecodes, f'KEY_{c.upper()}'), False)
for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    KEY_MAP[c] = (getattr(ecodes, f'KEY_{c}'), True)

KEY_MAP.update({
    '0': (ecodes.KEY_0, False), '1': (ecodes.KEY_1, False),
    '2': (ecodes.KEY_2, False), '3': (ecodes.KEY_3, False),
    '4': (ecodes.KEY_4, False), '5': (ecodes.KEY_5, False),
    '6': (ecodes.KEY_6, False), '7': (ecodes.KEY_7, False),
    '8': (ecodes.KEY_8, False), '9': (ecodes.KEY_9, False),
    ' ': (ecodes.KEY_SPACE, False), '\n': (ecodes.KEY_ENTER, False),
    '\t': (ecodes.KEY_TAB, False),
    '-': (ecodes.KEY_MINUS, False), '_': (ecodes.KEY_MINUS, True),
    '=': (ecodes.KEY_EQUAL, False), '+': (ecodes.KEY_EQUAL, True),
    '[': (ecodes.KEY_LEFTBRACE, False), '{': (ecodes.KEY_LEFTBRACE, True),
    ']': (ecodes.KEY_RIGHTBRACE, False), '}': (ecodes.KEY_RIGHTBRACE, True),
    '\\': (ecodes.KEY_BACKSLASH, False), '|': (ecodes.KEY_BACKSLASH, True),
    ';': (ecodes.KEY_SEMICOLON, False), ':': (ecodes.KEY_SEMICOLON, True),
    "'": (ecodes.KEY_APOSTROPHE, False), '"': (ecodes.KEY_APOSTROPHE, True),
    '`': (ecodes.KEY_GRAVE, False), '~': (ecodes.KEY_GRAVE, True),
    ',': (ecodes.KEY_COMMA, False), '<': (ecodes.KEY_COMMA, True),
    '.': (ecodes.KEY_DOT, False), '>': (ecodes.KEY_DOT, True),
    '/': (ecodes.KEY_SLASH, False), '?': (ecodes.KEY_SLASH, True),
    '!': (ecodes.KEY_1, True), '@': (ecodes.KEY_2, True),
    '#': (ecodes.KEY_3, True), '$': (ecodes.KEY_4, True),
    '%': (ecodes.KEY_5, True), '^': (ecodes.KEY_6, True),
    '&': (ecodes.KEY_7, True), '*': (ecodes.KEY_8, True),
    '(': (ecodes.KEY_9, True), ')': (ecodes.KEY_0, True),
})

# Bảng chuyển đổi dấu tiếng Việt sang không dấu (bảo đảm an toàn cho code/văn bản)
VIETNAMESE_MAP = {
    'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
    'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
    'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
    'đ': 'd',
    'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
    'ê': 'e', 'ề': 'e', 'ế': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
    'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
    'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
    'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
    'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
    'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
    'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
    'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
    'À': 'A', 'Á': 'A', 'Ả': 'A', 'Ã': 'A', 'Ạ': 'A',
    'Ă': 'A', 'Ằ': 'A', 'Ắ': 'A', 'Ẳ': 'A', 'Ẵ': 'A', 'Ặ': 'A',
    'Â': 'A', 'Ầ': 'A', 'Ấ': 'A', 'Ẩ': 'A', 'Ẫ': 'A', 'Ậ': 'A',
    'Đ': 'D',
    'È': 'E', 'É': 'E', 'Ẻ': 'E', 'Ẽ': 'E', 'Ẹ': 'E',
    'Ê': 'E', 'Ề': 'E', 'Ế': 'E', 'Ể': 'E', 'Ễ': 'E', 'Ệ': 'E',
    'Ì': 'I', 'Í': 'I', 'Ỉ': 'I', 'Ĩ': 'I', 'Ị': 'I',
    'Ò': 'O', 'Ó': 'O', 'Ỏ': 'O', 'Õ': 'O', 'Ọ': 'O',
    'Ô': 'O', 'Ồ': 'O', 'Ố': 'O', 'Ổ': 'O', 'Ỗ': 'O', 'Ộ': 'O',
    'Ơ': 'O', 'Ờ': 'O', 'Ớ': 'O', 'Ở': 'O', 'Ỡ': 'O', 'Ợ': 'O',
    'Ù': 'U', 'Ú': 'U', 'Ủ': 'U', 'Ũ': 'U', 'Ụ': 'U',
    'Ư': 'U', 'Ừ': 'U', 'Ứ': 'U', 'Ử': 'U', 'Ữ': 'U', 'Ự': 'U',
    'Ỳ': 'Y', 'Ý': 'Y', 'Ỷ': 'Y', 'Ỹ': 'Y', 'Ỵ': 'Y',
}

# Ký tự đặc biệt hay gặp khi copy từ web / tài liệu Word
SPECIAL_CHAR_MAP = {
    '“': '"', '”': '"', '„': '"', '«': '"', '»': '"',
    '‘': "'", '’': "'", '‚': "'", '‹': "'", '›': "'",
    '–': '-', '—': '-', '−': '-',
    '…': '...',
    '\xa0': ' ', '\u200b': '', '\ufeff': '',
}

# Phím chức năng & điều khiển
PAUSE_KEYS = {ecodes.KEY_F12, ecodes.KEY_PAUSE, ecodes.KEY_SCROLLLOCK}
EXIT_KEYS = {ecodes.KEY_F10}
MODIFIER_KEYS = {
    ecodes.KEY_LEFTCTRL, ecodes.KEY_RIGHTCTRL,
    ecodes.KEY_LEFTALT, ecodes.KEY_RIGHTALT,
    ecodes.KEY_LEFTSHIFT, ecodes.KEY_RIGHTSHIFT,
    ecodes.KEY_LEFTMETA, ecodes.KEY_RIGHTMETA,
    ecodes.KEY_CAPSLOCK,
}
NAV_KEYS = {
    ecodes.KEY_UP, ecodes.KEY_DOWN, ecodes.KEY_LEFT, ecodes.KEY_RIGHT,
    ecodes.KEY_HOME, ecodes.KEY_END, ecodes.KEY_PAGEUP, ecodes.KEY_PAGEDOWN,
}

# Biến toàn cục quản lý tài nguyên
grabbed_devices: list[evdev.InputDevice] = []
global_uinput: UInput | None = None
is_paused = False


def check_and_elevate() -> None:
    """Kiểm tra quyền truy cập /dev/uinput và evdev. Tự động gọi sudo nếu thiếu quyền."""
    needs_sudo = False
    try:
        if not os.access("/dev/uinput", os.W_OK):
            needs_sudo = True
        else:
            devs = evdev.list_devices()
            if not devs:
                needs_sudo = True
            else:
                test_dev = evdev.InputDevice(devs[0])
                test_dev.close()
    except (PermissionError, OSError):
        needs_sudo = True

    if needs_sudo and os.geteuid() != 0:
        print("[*] Thiếu quyền truy cập bàn phím & /dev/uinput.", file=sys.stderr)
        print("[*] Đang tự động nâng quyền chạy với sudo...", file=sys.stderr)
        try:
            os.execvp("sudo", ["sudo", sys.executable, *sys.argv])
        except Exception as err:
            print(f"[!] Không thể tự động chạy sudo: {err}", file=sys.stderr)
            print("[*] Hãy chạy lệnh: sudo python3 nhan_go.py", file=sys.stderr)
            sys.exit(1)


def cleanup(sig=None, frame=None) -> None:
    """Giải phóng toàn bộ bàn phím và đóng thiết bị UInput an toàn."""
    global grabbed_devices, global_uinput
    for dev in grabbed_devices:
        try:
            dev.ungrab()
        except Exception:
            pass
    grabbed_devices.clear()

    if global_uinput:
        try:
            global_uinput.close()
        except Exception:
            pass
        global_uinput = None

    print("\n\n[✓] Đã nhả toàn bộ bàn phím và thoát an toàn.")
    sys.exit(0)


signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)


def normalize_content(raw_text: str) -> list[str]:
    """Chuẩn hóa ký tự lạ, tiếng Việt, quotes sang ký tự gõ an toàn."""
    text = raw_text.replace('\r\n', '\n').replace('\r', '\n')
    for old, new in SPECIAL_CHAR_MAP.items():
        text = text.replace(old, new)

    result = []
    converted_count = 0
    for ch in text:
        if ch in KEY_MAP:
            result.append(ch)
        elif ch in VIETNAMESE_MAP:
            result.append(VIETNAMESE_MAP[ch])
            converted_count += 1
        else:
            # Thử phân rã Unicode NFKD
            decomposed = unicodedata.normalize('NFKD', ch)
            sub = [c for c in decomposed if c in KEY_MAP]
            if sub:
                result.extend(sub)
                converted_count += 1
            elif ch.isspace():
                result.append(' ')
            else:
                # Bỏ qua ký tự không hỗ trợ thay vì làm sập tool
                pass

    if converted_count > 0:
        print(f"[i] Đã tự động chuẩn hóa {converted_count} ký tự Unicode/Tiếng Việt sang ký tự an toàn.")
    return result


def init_uinput() -> UInput:
    """Khởi tạo 1 instance UInput duy nhất với đầy đủ các phím cần thiết."""
    all_keys = set()
    for keycode, _ in KEY_MAP.values():
        all_keys.add(keycode)
    all_keys.add(ecodes.KEY_LEFTSHIFT)
    all_keys.add(ecodes.KEY_BACKSPACE)
    all_keys.update(NAV_KEYS)
    return UInput({ecodes.EV_KEY: list(all_keys)}, name="nhan-go-uinput")


def send_key(ui: UInput, keycode: int, need_shift: bool = False) -> None:
    if need_shift:
        ui.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 1)
        ui.syn()
    ui.write(ecodes.EV_KEY, keycode, 1)
    ui.syn()
    ui.write(ecodes.EV_KEY, keycode, 0)
    ui.syn()
    if need_shift:
        ui.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 0)
        ui.syn()


def send_backspace(ui: UInput) -> None:
    ui.write(ecodes.EV_KEY, ecodes.KEY_BACKSPACE, 1)
    ui.syn()
    ui.write(ecodes.EV_KEY, ecodes.KEY_BACKSPACE, 0)
    ui.syn()


def forward_key(ui: UInput, code: int, value: int) -> None:
    ui.write(ecodes.EV_KEY, code, value)
    ui.syn()


def find_keyboards() -> list[evdev.InputDevice]:
    keyboards = []
    for path in evdev.list_devices():
        try:
            dev = evdev.InputDevice(path)
            name = dev.name.lower()
            # Bỏ qua thiết bị ảo của tool hoặc ydotool
            if 'ydotool' in name or 'nhan-go' in name:
                continue
            caps = dev.capabilities()
            if ecodes.EV_KEY in caps:
                keys = caps[ecodes.EV_KEY]
                if ecodes.KEY_A in keys and ecodes.KEY_SPACE in keys:
                    keyboards.append(dev)
        except Exception:
            pass
    return keyboards


def toggle_pause(current_idx: int, total_chars: int) -> None:
    global is_paused, grabbed_devices
    is_paused = not is_paused
    if is_paused:
        for dev in grabbed_devices:
            try:
                dev.ungrab()
            except Exception:
                pass
        print(f"\n⏸️  [TẠM DỪNG] Đã nhả bàn phím! Bạn có thể chat, gõ lệnh, chuyển tab bình thường.")
        print(f"👉 Bấm [F12] (hoặc Pause/Break) bất kỳ lúc nào để TIẾP TỤC gõ ({current_idx}/{total_chars})...\n")
    else:
        for dev in grabbed_devices:
            try:
                dev.grab()
            except Exception:
                pass
        print(f"\n▶️  [TIẾP TỤC] Đã khóa bàn phím! Nhấn phím bất kỳ để tiếp tục gõ ({current_idx + 1}/{total_chars})...\n")


def main() -> None:
    global global_uinput, grabbed_devices, is_paused

    check_and_elevate()

    # Nhận đường dẫn file từ tham số dòng lệnh nếu có, mặc định dapan.txt
    file_path = Path(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else DEFAULT_FILE_DAP_AN
    if not file_path.exists():
        print(f"[!] Không tìm thấy file: {file_path}", file=sys.stderr)
        sys.exit(1)

    raw_content = file_path.read_text(encoding="utf-8")
    if not raw_content.strip():
        print("[!] File đáp án đang rỗng!", file=sys.stderr)
        sys.exit(1)

    chars = normalize_content(raw_content)
    total = len(chars)

    print("=== [Tool Auto Write] nhan_go.py v2.0 - Developed by Amtia / Phamtin147 ===")
    print(f"[+] File: {file_path.name} | Đã nạp: {total} ký tự")

    # Mở 1 UInput instance duy nhất
    global_uinput = init_uinput()

    # Quét bàn phím
    keyboards = find_keyboards()
    if not keyboards:
        print("[!] Không tìm thấy bàn phím phần cứng phù hợp.", file=sys.stderr)
        sys.exit(1)

    for dev in keyboards:
        try:
            dev.grab()
            grabbed_devices.append(dev)
            print(f"[+] Đã khóa (Grab): {dev.name}")
        except Exception as e:
            print(f"[!] Bỏ qua {dev.name}: {e}")

    if not grabbed_devices:
        print("[!] Không thể grab được bàn phím nào!", file=sys.stderr)
        cleanup()

    print("\n" + "=" * 65)
    print("🎮 HƯỚNG DẪN ĐIỀU KHIỂN:")
    print("  • Nhấn phím bừa bất kỳ : Gõ lần lượt từng ký tự trong đáp án")
    print("  • Phím [Backspace]     : Lùi lại 1 ký tự (đồng thời xóa chữ trên màn hình)")
    print("  • Phím [F12] / Pause   : TẠM DỪNG / TIẾP TỤC (nhả bàn phím dùng bình thường)")
    print("  • Phím [F10] / Ctrl+C  : DỪNG KHẨN CẤP & THOÁT NGAY LẬP TỨC")
    print("=" * 65 + "\n")
    print("[►] Click chuột vào cửa sổ cần gõ (máy ảo / trình duyệt) và bắt đầu bấm phím!\n")

    idx = 0
    fd_map = {dev.fd: dev for dev in grabbed_devices}
    ctrl_down = False

    while idx < total:
        r, _, _ = select.select(fd_map.keys(), [], [])
        for fd in r:
            dev = fd_map[fd]
            try:
                events = list(dev.read())
            except Exception:
                continue

            for ev in events:
                if ev.type != ecodes.EV_KEY:
                    continue

                code = ev.code
                val = ev.value  # 0: nhả, 1: nhấn, 2: giữ

                # Theo dõi trạng thái Ctrl
                if code in (ecodes.KEY_LEFTCTRL, ecodes.KEY_RIGHTCTRL):
                    ctrl_down = (val != 0)
                    continue

                # Chỉ xử lý khi nhấn phím (val == 1)
                if val != 1:
                    continue

                # 1. Thoát khẩn cấp
                if code in EXIT_KEYS or (ctrl_down and code == ecodes.KEY_C):
                    cleanup()

                # 2. Tạm dừng / Tiếp tục
                if code in PAUSE_KEYS:
                    toggle_pause(idx, total)
                    continue

                # Nếu đang ở chế độ Tạm dừng, không xử lý gì thêm
                if is_paused:
                    continue

                # 3. Phím Backspace: Lùi lại và xóa trên màn hình
                if code == ecodes.KEY_BACKSPACE:
                    if idx > 0:
                        idx -= 1
                        send_backspace(global_uinput)
                        erased_char = chars[idx]
                        disp_erased = repr(erased_char) if erased_char in ('\n', '\t') else erased_char
                        print(f"  [{idx}/{total}] ⬅️  (Lùi lại: '{disp_erased}')       ", end="\r", flush=True)
                    else:
                        send_backspace(global_uinput)
                    continue

                # 4. Phím điều hướng con trỏ (pass-through trực tiếp không tăng idx)
                if code in NAV_KEYS:
                    forward_key(global_uinput, code, 1)
                    forward_key(global_uinput, code, 0)
                    continue

                # 5. Phím bổ trợ (Shift, Alt, Win, CapsLock): Không tăng idx
                if code in MODIFIER_KEYS:
                    continue

                # 6. Gõ ký tự tiếp theo trong đáp án
                ch = chars[idx]
                if ch in KEY_MAP:
                    keycode, need_shift = KEY_MAP[ch]
                    send_key(global_uinput, keycode, need_shift)

                idx += 1
                display = repr(ch) if ch in ('\n', '\t') else ch
                print(f"  [{idx}/{total}] Đang gõ: '{display}'                    ", end="\r", flush=True)

    print(f"\n\n[✓] Hoàn thành! Đã gõ toàn bộ {total} ký tự thành công.")
    cleanup()


if __name__ == "__main__":
    main()
