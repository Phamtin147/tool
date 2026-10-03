#!/usr/bin/env python3
"""Smartwatch Exam Notifier - AI Quiz Solver & Push Alert to Apple Watch / Wearables.
Developed by: Amtia / Phamtin147 (https://github.com/Phamtin147)

Captures screenshots of quiz questions, solves via Gemini Vision AI,
and delivers ultra-compact answer notifications to your smartwatch via Telegram Bot or ntfy.sh.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import platform
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional

CONFIG_ENV_PATHS = [
    Path(__file__).resolve().parent / ".config" / "config.env",
    Path.home() / ".config" / "smartwatch_notifier.env",
    Path.home() / ".config" / "gemini.env",
    Path(__file__).resolve().parent.parent / "quiz-led-solver" / ".config" / "gemini.env",
    Path.home() / ".env",
]

DEFAULT_SCREENSHOT_DIRS = [
    Path.home() / "Pictures" / "screenshots",
    Path.home() / "Desktop",
    Path.home() / "Pictures",
]

import ssl

DEFAULT_MODELS = [
    "gemini-flash-latest",
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.5-flash",
    "gemini-3.6-flash",
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
]

PROMPT_SMARTWATCH = (
    "You are an expert exam quiz solver. Inspect this question image. "
    "Give the result in this exact compact format (maximum 3 lines, fitting on a small smartwatch screen):\n"
    "ANS: [Option Letter(s), e.g., A, B, C, D]\n"
    "WHY: [1 very short punchy sentence]\n"
    "CONF: [Percentage, e.g. 98%]"
)


def load_env() -> None:
    for path in CONFIG_ENV_PATHS:
        if path.is_file():
            try:
                for line in path.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k, v = k.strip(), v.strip().strip("'\"")
                        if k and not os.environ.get(k):
                            os.environ[k] = v
            except Exception:
                pass


def send_telegram_alert(token: str, chat_id: str, message: str) -> bool:
    """Send alert via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_notification": False  # Vibrate on watch
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception as e:
        print(f"[Notifier] Telegram error: {e}", file=sys.stderr)
        return False


def send_ntfy_alert(topic: str, message: str, title: str = "Quiz Result") -> bool:
    """Send alert via ntfy.sh public or private push topic."""
    url = f"https://ntfy.sh/{topic}"
    headers = {
        "Title": title,
        "Priority": "high",
        "Tags": "zap,bulb"
    }
    req = urllib.request.Request(url, data=message.encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception as e:
        print(f"[Notifier] ntfy error: {e}", file=sys.stderr)
        return False


def query_gemini(image_path: Path, api_key: str, model_name: str = "gemini-2.5-flash") -> str:
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    ext = image_path.suffix.lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": PROMPT_SMARTWATCH},
                    {
                        "inline_data": {
                            "mime_type": mime,
                            "data": img_b64,
                        }
                    }
                ]
            }
        ],
        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 200}
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    ssl_ctx = ssl._create_unverified_context()
    with urllib.request.urlopen(req, timeout=15, context=ssl_ctx) as resp:
        body = json.loads(resp.read().decode("utf-8"))
        candidates = body.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts:
                return parts[0].get("text", "").strip()
    return "No answer from AI"


def dispatch_alert(text: str) -> None:
    """Send formatted answer to configured notification channel."""
    tg_token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    tg_chat = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    ntfy_topic = os.environ.get("NTFY_TOPIC", "").strip()

    sent = False
    if tg_token and tg_chat:
        formatted_tg = f"⚡ <b>AI QUIZ ALERT</b>\n<pre>{text}</pre>"
        if send_telegram_alert(tg_token, tg_chat, formatted_tg):
            print("✓ Pushed to Telegram Bot (Wrist notification sent!)")
            sent = True

    if ntfy_topic:
        if send_ntfy_alert(ntfy_topic, text):
            print(f"✓ Pushed to ntfy.sh/{ntfy_topic}")
            sent = True

    if not sent:
        print("[!] No notification channels configured. Printing result to stdout:")
        print("------------------------------------------")
        print(text)
        print("------------------------------------------")


def process_image(img_path: Path, api_key: str) -> None:
    print(f"\n[*] Processing image: {img_path.name}...")
    ans = ""
    for model in DEFAULT_MODELS:
        try:
            ans = query_gemini(img_path, api_key, model)
            if ans:
                break
        except Exception as e:
            print(f"[-] Model {model} failed: {e}")

    if ans:
        print(f"[+] Solved:\n{ans}")
        dispatch_alert(ans)
    else:
        print("[-] Failed to solve question.")


def snip_screen() -> Optional[Path]:
    """Capture selected screen region."""
    system = platform.system()
    tmp_path = Path(tempfile.gettempdir()) / f"smartwatch_snip_{int(time.time())}.png"

    if system == "Darwin":
        print("[*] Select question region on screen (Crosshair)...")
        res = subprocess.run(["screencapture", "-i", str(tmp_path)])
        if res.returncode == 0 and tmp_path.exists() and tmp_path.stat().st_size > 0:
            return tmp_path
    elif system == "Linux":
        print("[*] Select question region (import/scrot)...")
        res = subprocess.run(["import", str(tmp_path)])
        if res.returncode == 0 and tmp_path.exists():
            return tmp_path
    else:
        print(f"[-] Interactive snip not supported directly on {system}")
    return None


def watch_directory(watch_dir: Path, api_key: str) -> None:
    print(f"[*] Watching for new screenshots in: {watch_dir}")
    print("[*] Whenever you take a screenshot (e.g. Cmd+Shift+4 or PrintScreen), answer is pushed to your watch!")
    known_files = set(watch_dir.glob("*"))

    try:
        while True:
            time.sleep(1.0)
            current_files = set(watch_dir.glob("*"))
            new_files = current_files - known_files
            for f in sorted(new_files, key=lambda p: p.stat().st_mtime):
                if f.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
                    time.sleep(0.5)  # Wait for file write to complete
                    process_image(f, api_key)
            known_files = current_files
    except KeyboardInterrupt:
        print("\n[*] Stopped watcher.")


def main() -> None:
    load_env()
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()

    parser = argparse.ArgumentParser(description="Push AI Quiz answers straight to your Smartwatch.")
    parser.add_argument("--snip", action="store_true", help="Interactive screen region capture & solve")
    parser.add_argument("--watch", type=Path, nargs="?", const=Path.home() / "Desktop", help="Watch folder for new screenshots")
    parser.add_argument("--image", type=Path, help="Path to single image file to solve")
    args = parser.parse_args()

    if not api_key:
        print("[ERROR] GEMINI_API_KEY not found! Please set in .config/config.env", file=sys.stderr)
        sys.exit(1)

    if args.snip:
        snip_file = snip_screen()
        if snip_file:
            try:
                process_image(snip_file, api_key)
            finally:
                snip_file.unlink(missing_ok=True)
        else:
            print("[*] Snip canceled.")
    elif args.image:
        if args.image.exists():
            process_image(args.image, api_key)
        else:
            print(f"[!] Image file not found: {args.image}", file=sys.stderr)
    elif args.watch:
        target_dir = args.watch.expanduser()
        if not target_dir.exists():
            target_dir.mkdir(parents=True, exist_ok=True)
        watch_directory(target_dir, api_key)
    else:
        # Default action: run interactive snip
        print("[*] No mode specified. Running interactive snip...")
        snip_file = snip_screen()
        if snip_file:
            try:
                process_image(snip_file, api_key)
            finally:
                snip_file.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
