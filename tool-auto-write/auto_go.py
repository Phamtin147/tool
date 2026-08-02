#!/usr/bin/env python3
"""auto_go.py - Tu dong go toan bo dapan.txt qua ydotool (evdev -> QEMU)."""
import sys, os, time, signal, subprocess, tempfile, string

FILE_DAP_AN = "/home/amtia/tool/tool-auto-write/dapan.txt"
YDOTOOL_SOCKET = "/tmp/.ydotool_socket"
DELAY_START = 3
DELAY_BETWEEN_CHARS = 0.12

CHARS = set(string.printable) | {"\n", "\t"}

def cleanup(sig=None, frame=None):
    print("\n[!] Thoat.")
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def ydotool_char(ch):
    env = os.environ.copy()
    env["YDOTOOL_SOCKET"] = YDOTOOL_SOCKET
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as f:
        f.write(ch)
        tmppath = f.name
    try:
        subprocess.run(["ydotool", "type", "--key-delay", "0", "--file", tmppath], env=env, capture_output=True)
    finally:
        try: os.unlink(tmppath)
        except: pass

def ydotool_key(key):
    env = os.environ.copy()
    env["YDOTOOL_SOCKET"] = YDOTOOL_SOCKET
    subprocess.run(["ydotool", "key", key], env=env, capture_output=True)

def main():
    if not os.path.exists(FILE_DAP_AN):
        print(f"[!] Khong tim thay: {FILE_DAP_AN}"); sys.exit(1)
    with open(FILE_DAP_AN, "r", encoding="utf-8") as f:
        content = f.read()
    if not content.strip():
        print("[!] File rong!"); sys.exit(1)

    chars = list(content)
    unsupported = sorted({c for c in chars if c not in CHARS})
    if unsupported:
        print(f"[!] Ky tu chua ho tro: {unsupported}"); sys.exit(1)
    total = len(chars)
    print(f"[+] Load {total} ky tu tu dapan.txt")

    env = os.environ.copy()
    env["YDOTOOL_SOCKET"] = YDOTOOL_SOCKET
    if subprocess.run(["ydotool", "key", "0"], env=env, capture_output=True).returncode != 0:
        print("[!] ydotoold chua chay. Chay: sudo ydotoold --socket-path /tmp/.ydotool_socket --socket-perm 0666")
        sys.exit(1)
    print("[+] Dau ra: ydotool")

    print(f"[*] Bat dau sau {DELAY_START}s... Click vao noi muon go ngay!")
    for i in range(DELAY_START, 0, -1):
        print(f"    {i}...", end="\r", flush=True)
        time.sleep(1)

    ydotool_key("KEY_ESC")
    time.sleep(0.1)

    print(f"\n[►] Dang go {total} ky tu...")
    for idx, ch in enumerate(chars):
        ydotool_char(ch)
        print(f"  [{idx+1}/{total}]", end="\r", flush=True)
        if DELAY_BETWEEN_CHARS > 0:
            time.sleep(DELAY_BETWEEN_CHARS)

    print(f"\n[✓] Xong! Da go {total} ky tu.")

if __name__ == "__main__":
    main()
