#!/usr/bin/env python3
"""Human-Like Keystroke Simulator (Anti-Paste & Keystroke Dynamics Bypass).
Developed by: Amtia / Phamtin147 (https://github.com/Phamtin147)

Simulates genuine human typing with:
1. Gaussian inter-key delay (WPM variation)
2. QWERTY keyboard neighbor typos & automatic Backspace self-corrections
3. Punctuation & newline thinking pauses
4. Cross-platform support (macOS osascript/CoreGraphics, Linux ydotool/xdotool)
"""

from __future__ import annotations

import argparse
import os
import platform
import random
import subprocess
import sys
import time
from pathlib import Path
from typing import List

# Adjacent keys on standard US QWERTY layout
QWERTY_NEIGHBORS = {
    'a': ['q', 'w', 's', 'z'],
    'b': ['v', 'g', 'h', 'n'],
    'c': ['x', 'd', 'f', 'v'],
    'd': ['s', 'e', 'r', 'f', 'c', 'x'],
    'e': ['w', 'r', 'd', 's', '3', '4'],
    'f': ['d', 'r', 't', 'g', 'v', 'c'],
    'g': ['f', 't', 'y', 'h', 'b', 'v'],
    'h': ['g', 'y', 'u', 'j', 'n', 'b'],
    'i': ['u', 'o', 'k', 'j', '8', '9'],
    'j': ['h', 'u', 'i', 'k', 'm', 'n'],
    'k': ['j', 'i', 'o', 'l', 'm'],
    'l': ['k', 'o', 'p', ';'],
    'm': ['n', 'j', 'k'],
    'n': ['b', 'h', 'j', 'm'],
    'o': ['i', 'p', 'l', 'k', '9', '0'],
    'p': ['o', '[', ';', 'l', '0', '-'],
    'q': ['1', '2', 'w', 'a'],
    'r': ['e', '4', '5', 't', 'f', 'd'],
    's': ['a', 'w', 'e', 'd', 'x', 'z'],
    't': ['r', '5', '6', 'y', 'g', 'f'],
    'u': ['y', '7', '8', 'i', 'j', 'h'],
    'v': ['c', 'f', 'g', 'b'],
    'w': ['q', '2', '3', 'e', 's', 'a'],
    'x': ['z', 's', 'd', 'c'],
    'y': ['t', '6', '7', 'u', 'h', 'g'],
    'z': ['a', 's', 'x'],
}

SHIFT_SYMBOLS = set('~!@#$%^&*()_+{}|:"<>?')


class KeyDriver:
    """Unified cross-platform typing interface."""

    def __init__(self) -> None:
        self.system = platform.system()
        self.driver_type = self._detect_driver()

    def _detect_driver(self) -> str:
        # Check if pynput is available
        try:
            import pynput
            return "pynput"
        except ImportError:
            pass

        if self.system == "Darwin":
            return "macos_osascript"
        elif self.system == "Linux":
            # Check ydotool or xdotool
            if subprocess.run(["which", "ydotool"], capture_output=True).returncode == 0:
                return "linux_ydotool"
            if subprocess.run(["which", "xdotool"], capture_output=True).returncode == 0:
                return "linux_xdotool"
            return "linux_generic"
        elif self.system == "Windows":
            return "windows_ctypes"
        return "generic"

    def type_char(self, char: str) -> None:
        if self.driver_type == "macos_osascript":
            if char == "\n":
                subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 36'], capture_output=True)
            elif char == "\t":
                subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 48'], capture_output=True)
            elif char == "\\":
                subprocess.run(["osascript", "-e", 'tell application "System Events" to keystroke "\\\\"'], capture_output=True)
            elif char == '"':
                subprocess.run(["osascript", "-e", 'tell application "System Events" to keystroke "\\\""'], capture_output=True)
            else:
                escaped = char.replace("\\", "\\\\").replace('"', '\\"')
                subprocess.run(["osascript", "-e", f'tell application "System Events" to keystroke "{escaped}"'], capture_output=True)

        elif self.driver_type == "linux_ydotool":
            if char == "\n":
                subprocess.run(["ydotool", "key", "28:1", "28:0"], capture_output=True)
            elif char == "\t":
                subprocess.run(["ydotool", "key", "15:1", "15:0"], capture_output=True)
            else:
                subprocess.run(["ydotool", "type", "--", char], capture_output=True)

        elif self.driver_type == "linux_xdotool":
            if char == "\n":
                subprocess.run(["xdotool", "key", "Return"], capture_output=True)
            elif char == "\t":
                subprocess.run(["xdotool", "key", "Tab"], capture_output=True)
            else:
                subprocess.run(["xdotool", "type", "--", char], capture_output=True)

        elif self.driver_type == "windows_ctypes":
            try:
                import ctypes
                import ctypes.wintypes
                # SendInput via ctypes
                user32 = ctypes.windll.user32
                for ch in char:
                    # VK_RETURN
                    if ch == '\n':
                        user32.keybd_event(0x0D, 0, 0, 0)
                        user32.keybd_event(0x0D, 0, 2, 0)
                    else:
                        user32.keybd_event(ord(ch.upper()), 0, 0, 0)
                        user32.keybd_event(ord(ch.upper()), 0, 2, 0)
            except Exception:
                pass

        else:
            print(f"[!] Driver fallback: cannot type '{char}'", file=sys.stderr)

    def type_backspace(self) -> None:
        if self.driver_type == "macos_osascript":
            subprocess.run(["osascript", "-e", 'tell application "System Events" to key code 51'], capture_output=True)
        elif self.driver_type == "linux_ydotool":
            subprocess.run(["ydotool", "key", "14:1", "14:0"], capture_output=True)
        elif self.driver_type == "linux_xdotool":
            subprocess.run(["xdotool", "key", "BackSpace"], capture_output=True)
        elif self.driver_type == "windows_ctypes":
            try:
                import ctypes
                ctypes.windll.user32.keybd_event(0x08, 0, 0, 0)
                ctypes.windll.user32.keybd_event(0x08, 0, 2, 0)
            except Exception:
                pass


def simulate_human_typing(
    text: str,
    target_wpm: int = 65,
    typo_rate: float = 0.025,
    enable_typos: bool = True
) -> None:
    driver = KeyDriver()
    print(f"[*] Engine Initialized: {driver.driver_type} on {driver.system}")
    print(f"[*] Target Speed: ~{target_wpm} WPM | Typo Rate: {typo_rate * 100:.1f}%\n")

    # 1 word = ~5 chars on average.
    # WPM 60 => 300 chars/min => 5 chars/sec => 0.2s/char.
    mean_delay = 60.0 / (max(10, target_wpm) * 5.0)
    std_dev = mean_delay * 0.35

    total_chars = len(text)
    typo_count = 0

    print("Typing in progress (Do NOT touch keyboard/mouse)...")
    for idx, char in enumerate(text):
        # 1. Determine if a human typo occurs
        is_typo = (
            enable_typos
            and (char.lower() in QWERTY_NEIGHBORS)
            and (random.random() < typo_rate)
            and (idx < total_chars - 1)
        )

        if is_typo:
            typo_count += 1
            # Pick adjacent key
            wrong_char = random.choice(QWERTY_NEIGHBORS[char.lower()])
            if char.isupper():
                wrong_char = wrong_char.upper()

            # Type mistake
            driver.type_char(wrong_char)

            # Human hesitation / realization pause (120ms - 320ms)
            time.sleep(random.uniform(0.12, 0.32))

            # Backspace to fix
            driver.type_backspace()

            # Post-correction pause (70ms - 160ms)
            time.sleep(random.uniform(0.07, 0.16))

            # Type correct char
            driver.type_char(char)
        else:
            # Type normal character
            driver.type_char(char)

        # 2. Calculate dynamic Gaussian delay
        delay = random.gauss(mean_delay, std_dev)
        delay = max(0.025, min(delay, 0.45))

        # Adjust for special characters
        if char in SHIFT_SYMBOLS or char.isupper():
            delay += random.uniform(0.04, 0.09)  # Shift-key penalty
        elif char in {'.', ',', ';', ':', '!', '?'}:
            delay += random.uniform(0.15, 0.35)  # Clause pause
        elif char == '\n':
            delay += random.uniform(0.40, 0.90)  # Thinking pause between lines

        time.sleep(delay)

        # Progress display
        if (idx + 1) % 15 == 0 or idx == total_chars - 1:
            pct = (idx + 1) / total_chars * 100
            sys.stdout.write(f"\rProgress: [{idx + 1}/{total_chars}] {pct:.1f}% | Typos Simulated: {typo_count}")
            sys.stdout.flush()

    print("\n\n✓ Finished typing successfully!")


def countdown(seconds: int = 5) -> None:
    print(f"⚠️  GET READY: Click inside your target VM / input field now!")
    for s in range(seconds, 0, -1):
        sys.stdout.write(f"\r⏱️  Starting in {s} seconds... ")
        sys.stdout.flush()
        time.sleep(1.0)
    sys.stdout.write("\r🚀 TYPING STARTED NOW!                       \n")
    sys.stdout.flush()


def main() -> None:
    parser = argparse.ArgumentParser(description="Human-Like Keystroke Simulator for anti-paste VM / exam environments.")
    parser.add_argument("-f", "--file", type=Path, help="Path to text or code file to type")
    parser.add_argument("-t", "--text", type=str, help="Direct text string to type")
    parser.add_argument("--wpm", type=int, default=65, help="Typing speed in Words Per Minute (default: 65)")
    parser.add_argument("--typo-rate", type=float, default=0.025, help="Chance of typing error (default: 0.025 = 2.5%)")
    parser.add_argument("--no-typo", action="store_true", help="Disable intentional typo simulation")
    parser.add_argument("--countdown", type=int, default=5, help="Countdown seconds before start (default: 5)")
    args = parser.parse_args()

    content = ""
    if args.file:
        if not args.file.exists():
            print(f"[!] Error: File '{args.file}' not found.", file=sys.stderr)
            sys.exit(1)
        content = args.file.read_text(encoding="utf-8")
    elif args.text:
        content = args.text
    else:
        # Default sample file
        sample_path = Path(__file__).resolve().parent / "sample_input.txt"
        if sample_path.exists():
            print(f"[*] No input specified. Using sample: {sample_path.name}")
            content = sample_path.read_text(encoding="utf-8")
        else:
            print("[!] Please provide --file <path> or --text <string>", file=sys.stderr)
            sys.exit(1)

    countdown(args.countdown)
    simulate_human_typing(
        text=content,
        target_wpm=args.wpm,
        typo_rate=args.typo_rate,
        enable_typos=not args.no_typo
    )


if __name__ == "__main__":
    main()
