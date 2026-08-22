#!/usr/bin/env python3
"""
nhan_go.py - Nhan phim -> ra 1 ky tu trong dapan.txt.
Grab ban phim + UInput 1-2 key cho tung ky tu (ko gioi han 20 key).

Developed by: Amtia / Phamtin147 (https://github.com/Phamtin147)
"""
import evdev
from evdev import UInput, ecodes
import sys, os, signal, select, string

FILE_DAP_AN = "/home/amtia/tool/tool-auto-write/dapan.txt"

CHAR_MAP = {c: c for c in string.printable}
CHAR_MAP['\n'] = '\n'
CHAR_MAP['\t'] = '\t'

# Map ky tu -> (keycode, can_shift)
KEY_MAP = {}
for c in 'abcdefghijklmnopqrstuvwxyz':
    KEY_MAP[c] = (getattr(ecodes, f'KEY_{c.upper()}'), False)
for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    KEY_MAP[c] = (getattr(ecodes, f'KEY_{c}'), True)
KEY_MAP.update({
    '0':(ecodes.KEY_0,False),'1':(ecodes.KEY_1,False),
    '2':(ecodes.KEY_2,False),'3':(ecodes.KEY_3,False),
    '4':(ecodes.KEY_4,False),'5':(ecodes.KEY_5,False),
    '6':(ecodes.KEY_6,False),'7':(ecodes.KEY_7,False),
    '8':(ecodes.KEY_8,False),'9':(ecodes.KEY_9,False),
    ' ':(ecodes.KEY_SPACE,False),'\n':(ecodes.KEY_ENTER,False),
    '\t':(ecodes.KEY_TAB,False),
    '-':(ecodes.KEY_MINUS,False),'_':(ecodes.KEY_MINUS,True),
    '=':(ecodes.KEY_EQUAL,False),'+':(ecodes.KEY_EQUAL,True),
    '[':(ecodes.KEY_LEFTBRACE,False),'{':(ecodes.KEY_LEFTBRACE,True),
    ']':(ecodes.KEY_RIGHTBRACE,False),'}':(ecodes.KEY_RIGHTBRACE,True),
    '\\':(ecodes.KEY_BACKSLASH,False),'|':(ecodes.KEY_BACKSLASH,True),
    ';':(ecodes.KEY_SEMICOLON,False),':':(ecodes.KEY_SEMICOLON,True),
    "'":(ecodes.KEY_APOSTROPHE,False),'"':(ecodes.KEY_APOSTROPHE,True),
    '`':(ecodes.KEY_GRAVE,False),'~':(ecodes.KEY_GRAVE,True),
    ',':(ecodes.KEY_COMMA,False),'<':(ecodes.KEY_COMMA,True),
    '.':(ecodes.KEY_DOT,False),'>':(ecodes.KEY_DOT,True),
    '/':(ecodes.KEY_SLASH,False),'?':(ecodes.KEY_SLASH,True),
    '!':(ecodes.KEY_1,True),'@':(ecodes.KEY_2,True),
    '#':(ecodes.KEY_3,True),'$':(ecodes.KEY_4,True),
    '%':(ecodes.KEY_5,True),'^':(ecodes.KEY_6,True),
    '&':(ecodes.KEY_7,True),'*':(ecodes.KEY_8,True),
    '(':(ecodes.KEY_9,True),')':(ecodes.KEY_0,True),
})

PASS_THROUGH = {
    ecodes.KEY_LEFTMETA, ecodes.KEY_RIGHTMETA,
    ecodes.KEY_LEFTCTRL, ecodes.KEY_RIGHTCTRL,
    ecodes.KEY_LEFTALT,  ecodes.KEY_RIGHTALT,
    ecodes.KEY_LEFTSHIFT,ecodes.KEY_RIGHTSHIFT,
    ecodes.KEY_CAPSLOCK, ecodes.KEY_ESC,
    ecodes.KEY_F1,ecodes.KEY_F2,ecodes.KEY_F3,ecodes.KEY_F4,
    ecodes.KEY_F5,ecodes.KEY_F6,ecodes.KEY_F7,ecodes.KEY_F8,
    ecodes.KEY_F9,ecodes.KEY_F10,ecodes.KEY_F11,ecodes.KEY_F12,
    ecodes.KEY_UP,ecodes.KEY_DOWN,ecodes.KEY_LEFT,ecodes.KEY_RIGHT,
    ecodes.KEY_HOME,ecodes.KEY_END,ecodes.KEY_PAGEUP,ecodes.KEY_PAGEDOWN,
    ecodes.KEY_DELETE,ecodes.KEY_INSERT,
}

grabbed_devices = []

def cleanup(sig=None, frame=None):
    for dev in grabbed_devices:
        try: dev.ungrab()
        except: pass
    print("\n[!] Thoat.")
    sys.exit(0)

def type_char_via_uinput(ch):
    if ch not in KEY_MAP:
        return
    keycode, need_shift = KEY_MAP[ch]
    keys = [keycode]
    if need_shift:
        keys.append(ecodes.KEY_LEFTSHIFT)
    ui = UInput({ecodes.EV_KEY: keys}, name='nhan-go-char')
    if need_shift:
        ui.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 1); ui.syn()
    ui.write(ecodes.EV_KEY, keycode, 1); ui.syn()
    ui.write(ecodes.EV_KEY, keycode, 0); ui.syn()
    if need_shift:
        ui.write(ecodes.EV_KEY, ecodes.KEY_LEFTSHIFT, 0); ui.syn()
    ui.close()

def find_keyboards():
    keyboards = []
    for path in evdev.list_devices():
        try:
            dev = evdev.InputDevice(path)
            name = dev.name.lower()
            if 'ydotool' in name:
                continue
            caps = dev.capabilities()
            if ecodes.EV_KEY in caps:
                keys = caps[ecodes.EV_KEY]
                if ecodes.KEY_A in keys and ecodes.KEY_SPACE in keys:
                    keyboards.append(dev)
        except: pass
    return keyboards

def main():
    if not os.path.exists(FILE_DAP_AN):
        print(f"[!] Khong tim thay: {FILE_DAP_AN}"); sys.exit(1)
    with open(FILE_DAP_AN, "r", encoding="utf-8") as f:
        content = f.read()
    if not content.strip():
        print("[!] File rong!"); sys.exit(1)
    chars = list(content)
    unsupported = sorted({c for c in chars if c not in CHAR_MAP})
    if unsupported:
        print(f"[!] Ky tu chua ho tro: {unsupported}"); sys.exit(1)
    print(f"[+] Load {len(chars)} ky tu")

    keyboards = find_keyboards()
    if not keyboards:
        print("[!] Khong tim thay ban phim."); sys.exit(1)

    for dev in keyboards:
        try:
            dev.grab()
            grabbed_devices.append(dev)
            print(f"[+] Grab: {dev.name}")
        except:
            print(f"[!] Bo qua: {dev.name}")

    if not grabbed_devices:
        print("[!] Khong grab duoc!"); sys.exit(1)

    print("=== [Tool Auto Write] nhan_go.py - Developed by Amtia / Phamtin147 ===")
    print(f"\n[►] Click vao QEMU, roi nhan phim bat ky.")
    print(f"    Ctrl+C de thoat.\n")

    idx = 0
    fd_map = {dev.fd: dev for dev in grabbed_devices}
    ctrl_down = False

    while idx < len(chars):
        r, _, _ = select.select(fd_map.keys(), [], [])
        for fd in r:
            dev = fd_map[fd]
            try: events = list(dev.read())
            except: continue
            for ev in events:
                if ev.type != ecodes.EV_KEY: continue
                code = ev.code
                if code in (ecodes.KEY_LEFTCTRL, ecodes.KEY_RIGHTCTRL):
                    ctrl_down = ev.value != 0
                    continue
                if ctrl_down and code == ecodes.KEY_C:
                    cleanup()
                if code in PASS_THROUGH:
                    continue
                if ev.value != 1:
                    continue
                ch = chars[idx]
                type_char_via_uinput(ch)
                display = repr(ch) if ch in ('\n', '\t') else ch
                print(f"  [{idx+1}/{len(chars)}] '{display}'", end="\r", flush=True)
                idx += 1
                break

    print(f"\n[✓] Xong! Da go {len(chars)} ky tu.")
    cleanup()

if __name__ == "__main__":
    main()
