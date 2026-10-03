#!/usr/bin/env python3
"""Voice & Interview Whisper - Real-Time AI Interview & Oral Exam Co-Pilot.
Developed by: Amtia / Phamtin147 (https://github.com/Phamtin147)

Listens to interview questions (mic/system audio/file), transcribes,
and generates concise, punchy bullet points and code snippets via Gemini Multimodal Audio.
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
import urllib.request
from pathlib import Path
from typing import Optional

CONFIG_ENV_PATHS = [
    Path(__file__).resolve().parent / ".config" / "gemini.env",
    Path.home() / ".config" / "gemini.env",
    Path(__file__).resolve().parent.parent / "stealth-invisible-hud" / ".config" / "gemini.env",
    Path(__file__).resolve().parent.parent / "quiz-led-solver" / ".config" / "gemini.env",
    Path.home() / ".env",
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

INTERVIEW_PROMPT = (
    "You are a secret live technical interview & oral exam assistant. "
    "Listen carefully to the audio or read the question. "
    "Respond in the same language as the speaker (Vietnamese or English). "
    "Structure your response strictly as follows:\n\n"
    "🎯 CÂU HỎI / QUESTION:\n"
    "<1 clear sentence summarizing what was asked>\n\n"
    "💡 GỢI Ý NÓI (TALKING POINTS):\n"
    "- Điểm 1: <Ý cốt lõi mạnh mẽ nhất để trả lời ngay lập tức>\n"
    "- Điểm 2: <Giải thích cơ chế hoạt động / so sánh / trade-off>\n"
    "- Điểm 3: <Kinh nghiệm thực tế hoặc ví dụ ngắn>\n\n"
    "💻 CODE / KEYWORDS (Nếu liên quan đến lập trình):\n"
    "<Mã nguồn ngắn nhất hoặc danh sách keyword công nghệ>\n\n"
    "Keep it concise so the user can glance and speak naturally without hesitation."
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


def get_mime_type(file_path: Path) -> str:
    ext = file_path.suffix.lower()
    mimes = {
        ".wav": "audio/wav",
        ".mp3": "audio/mp3",
        ".m4a": "audio/m4a",
        ".ogg": "audio/ogg",
        ".flac": "audio/flac",
        ".aac": "audio/aac",
    }
    return mimes.get(ext, "audio/wav")


def query_gemini_audio(audio_path: Path, api_key: str, model_name: str = "gemini-2.5-flash") -> str:
    """Send raw audio directly to Gemini Multimodal Audio model."""
    with open(audio_path, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode("utf-8")

    mime = get_mime_type(audio_path)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": INTERVIEW_PROMPT},
                    {
                        "inline_data": {
                            "mime_type": mime,
                            "data": audio_b64,
                        }
                    },
                    {"text": "Analyze the question in this audio clip and provide the talking points."}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 600,
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    ssl_ctx = ssl._create_unverified_context()
    with urllib.request.urlopen(req, timeout=20, context=ssl_ctx) as resp:
        body = json.loads(resp.read().decode("utf-8"))
        candidates = body.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts:
                return parts[0].get("text", "").strip()
    return "No response from Gemini Audio API."


def query_gemini_text(question_text: str, api_key: str, model_name: str = "gemini-2.5-flash") -> str:
    """Fallback text question mode."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": INTERVIEW_PROMPT},
                    {"text": f"Question:\n{question_text}"}
                ]
            }
        ],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 600}
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
    return "No response."


def record_audio_cli(output_path: Path) -> bool:
    """Record audio using available CLI recorder."""
    system = platform.system()

    # Check ffmpeg
    if subprocess.run(["which", "ffmpeg"], capture_output=True).returncode == 0:
        if system == "Darwin":
            # AVFoundation input on macOS
            cmd = ["ffmpeg", "-y", "-f", "avfoundation", "-i", ":0", "-t", "10", str(output_path)]
        elif system == "Linux":
            cmd = ["ffmpeg", "-y", "-f", "pulse", "-i", "default", "-t", "10", str(output_path)]
        else:
            cmd = ["ffmpeg", "-y", "-f", "dshow", "-i", "audio=virtual-audio-capturer", "-t", "10", str(output_path)]

        print(f"[*] Recording 10s audio with ffmpeg...")
        res = subprocess.run(cmd, capture_output=True)
        return res.returncode == 0 and output_path.exists()

    # Check sox / rec
    if subprocess.run(["which", "rec"], capture_output=True).returncode == 0:
        print("[*] Recording 10s audio with rec...")
        res = subprocess.run(["rec", "-q", str(output_path), "trim", "0", "10"], capture_output=True)
        return res.returncode == 0 and output_path.exists()

    # Check arecord (Linux ALSA)
    if subprocess.run(["which", "arecord"], capture_output=True).returncode == 0:
        print("[*] Recording 10s audio with arecord...")
        res = subprocess.run(["arecord", "-d", "10", "-f", "cd", "-t", "wav", str(output_path)], capture_output=True)
        return res.returncode == 0 and output_path.exists()

    print("[!] No CLI audio recorder found (ffmpeg / rec / arecord).", file=sys.stderr)
    return False


def print_colored_result(result_text: str) -> None:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    print("\n" + "=" * 60)
    print(f"{BOLD}{CYAN}🎙️  AI INTERVIEW COPILOT - GỢI Ý TRẢ LỜI:{RESET}")
    print("=" * 60 + "\n")

    for line in result_text.splitlines():
        if "CÂU HỎI" in line or "QUESTION" in line:
            print(f"{BOLD}{YELLOW}{line}{RESET}")
        elif "GỢI Ý" in line or "TALKING" in line:
            print(f"{BOLD}{GREEN}{line}{RESET}")
        elif "CODE" in line or "KEYWORD" in line:
            print(f"{BOLD}{CYAN}{line}{RESET}")
        elif line.strip().startswith("-"):
            print(f"  {BOLD}•{RESET} {line.strip()[1:].strip()}")
        else:
            print(line)

    print("\n" + "=" * 60 + "\n")


def main() -> None:
    load_env()
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()

    parser = argparse.ArgumentParser(description="Real-Time AI Voice Interview Assistant.")
    parser.add_argument("-f", "--file", type=Path, help="Audio file to analyze (.wav, .m4a, .mp3)")
    parser.add_argument("-q", "--question", type=str, help="Direct text question input")
    parser.add_argument("-r", "--record", action="store_true", help="Record audio snippet from microphone")
    args = parser.parse_args()

    if not api_key:
        print("[ERROR] GEMINI_API_KEY not configured. Set in .config/gemini.env", file=sys.stderr)
        sys.exit(1)

    if args.file:
        if not args.file.exists():
            print(f"[!] Audio file not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        print(f"[*] Analyzing audio file: {args.file.name} with Gemini Multimodal Audio...")
        res = query_gemini_audio(args.file, api_key)
        print_colored_result(res)

    elif args.question:
        print(f"[*] Processing question: {args.question}...")
        res = query_gemini_text(args.question, api_key)
        print_colored_result(res)

    elif args.record:
        tmp_wav = Path(tempfile.gettempdir()) / f"interview_record_{int(time.time())}.wav"
        try:
            ok = record_audio_cli(tmp_wav)
            if ok:
                print("[*] Uploading audio to Gemini AI...")
                res = query_gemini_audio(tmp_wav, api_key)
                print_colored_result(res)
            else:
                print("[!] Recording failed. Tip: pass an existing audio file via --file <path> or use --question <text>")
        finally:
            tmp_wav.unlink(missing_ok=True)

    else:
        # Interactive loop: user can type question or press Enter to record
        print("\n" + "=" * 55)
        print("🎧 Voice Interview Whisper - Interactive Console Mode")
        print("=" * 55)
        print("Tùy chọn thao tác:")
        print("1. Nhập câu hỏi phỏng vấn trực tiếp bằng chữ")
        print("2. Nhập đường dẫn file audio (.wav/.m4a/.mp3) vừa ghi âm")
        print("3. Gõ 'exit' hoặc 'q' để thoát\n")

        while True:
            try:
                user_input = input(">> Câu hỏi / File audio: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in {"exit", "quit", "q"}:
                    print("Goodbye!")
                    break

                target_path = Path(user_input).expanduser()
                if target_path.exists() and target_path.suffix.lower() in {".wav", ".mp3", ".m4a", ".ogg", ".flac"}:
                    print(f"[*] Phân tích âm thanh: {target_path.name}...")
                    res = query_gemini_audio(target_path, api_key)
                else:
                    print(f"[*] Phân tích câu hỏi...")
                    res = query_gemini_text(user_input, api_key)

                print_colored_result(res)

            except KeyboardInterrupt:
                print("\nStopped.")
                break


if __name__ == "__main__":
    main()
