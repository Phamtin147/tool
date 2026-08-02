#!/usr/bin/env python3
"""CLI tool: newest screenshot -> Vision AI -> blink Caps Lock answer code.

Answer encoding:
A=2 key events, B=4, C=6, D=8, E=10, F=12.

Requirements:
- ydotoold running and user-accessible socket for LED/key event signaling
- optional Gemini API key via GEMINI_API_KEY or GOOGLE_API_KEY
- optional Ollama server at OLLAMA_HOST or http://127.0.0.1:11434
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterable

import requests

SCREENSHOT_DIR = Path("/home/amtia/Pictures/screenshots")
CONFIG_ENV = Path(__file__).resolve().parent / ".config" / "gemini.env"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
ANSWER_RE = re.compile(r"\b([A-F])\b", re.IGNORECASE)
CAPS_LOCK_KEYCODE = 58

PROMPT = """You are solving a multiple-choice question from a screenshot.
Find the correct answer option.
Respond with exactly ONE uppercase letter from A, B, C, D, E, F.
Do not explain. Do not include punctuation. If unsure, choose the most likely option.
""".strip()


def load_config_env() -> None:
    """Load KEY=VALUE lines from .config/gemini.env into os.environ (if not already set)."""
    if not CONFIG_ENV.exists():
        return
    for line in CONFIG_ENV.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if key and key not in os.environ:
            os.environ[key] = value


def newest_image(directory: Path) -> Path:
    if not directory.exists():
        raise FileNotFoundError(f"Screenshot directory does not exist: {directory}")

    images = [p for p in directory.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS]
    if not images:
        raise FileNotFoundError(f"No image files found in {directory}")

    return max(images, key=lambda p: p.stat().st_mtime)


def image_to_base64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def parse_answer(text: str) -> str:
    clean = text.strip().upper()
    if clean in {"A", "B", "C", "D", "E", "F"}:
        return clean

    match = ANSWER_RE.search(clean)
    if match:
        return match.group(1).upper()

    compact = re.sub(r"[^A-F]", "", clean)
    if compact:
        return compact[0]

    raise ValueError(f"Could not parse A-F answer from: {text!r}")


def mime_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".png":
        return "image/png"
    if suffix in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if suffix == ".webp":
        return "image/webp"
    return "application/octet-stream"


def ask_gemini(path: Path, model: str, timeout: float) -> str:
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY or GOOGLE_API_KEY")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    params = {"key": api_key}
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": PROMPT},
                    {
                        "inline_data": {
                            "mime_type": mime_type(path),
                            "data": image_to_base64(path),
                        }
                    },
                ],
            }
        ],
        "generationConfig": {
            "temperature": 0,
            "maxOutputTokens": 256,
        },
    }

    response = requests.post(url, params=params, json=payload, timeout=timeout)
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        body = response.text[:500]
        raise RuntimeError(f"Gemini HTTP {response.status_code}: {body}") from exc
    data = response.json()

    try:
        parts = data["candidates"][0]["content"]["parts"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"Unexpected Gemini response: {json.dumps(data)[:500]}") from exc

    text = "".join(part.get("text", "") for part in parts)
    if not text.strip():
        raise RuntimeError(f"Empty Gemini response: {json.dumps(data)[:500]}")
    return parse_answer(text)


def ask_ollama(path: Path, model: str, timeout: float) -> str:
    host = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
    payload = {
        "model": model,
        "prompt": PROMPT,
        "images": [image_to_base64(path)],
        "stream": False,
        "options": {
            "temperature": 0,
            "num_predict": 4,
        },
    }
    response = requests.post(f"{host}/api/generate", json=payload, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    text = data.get("response", "")
    if not text.strip():
        raise RuntimeError(f"Empty Ollama response: {json.dumps(data)[:500]}")
    return parse_answer(text)


def provider_order(provider: str) -> list[str]:
    if provider == "auto":
        return ["gemini", "ollama"]
    return [provider]


def solve(path: Path, provider: str, gemini_model: str, ollama_model: str, timeout: float) -> tuple[str, str]:
    errors: list[str] = []
    for name in provider_order(provider):
        try:
            print(f"[ai] trying {name}...", file=sys.stderr)
            if name == "gemini":
                return ask_gemini(path, gemini_model, timeout), name
            if name == "ollama":
                return ask_ollama(path, ollama_model, timeout), name
            raise ValueError(f"Unknown provider: {name}")
        except Exception as exc:  # noqa: BLE001 - CLI should show all provider failures
            errors.append(f"{name}: {exc}")
            print(f"[ai] {name} failed: {exc}", file=sys.stderr)

    raise RuntimeError("All providers failed:\n" + "\n".join(errors))


def blink_count(answer: str) -> int:
    return (ord(answer) - ord("A") + 1) * 2


def run_ydotool_key(keycode: int) -> None:
    subprocess.run(
        ["ydotool", "key", f"{keycode}:1", f"{keycode}:0"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )


def blink_caps(answer: str, interval: float, dry_run: bool) -> None:
    count = blink_count(answer)
    print(f"[led] answer={answer} -> Caps Lock key events={count}", file=sys.stderr)
    if dry_run:
        return

    for index in range(count):
        try:
            run_ydotool_key(CAPS_LOCK_KEYCODE)
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(
                "ydotool failed. Make sure ydotoold is running and socket is accessible. "
                f"stderr={exc.stderr.strip()!r}"
            ) from exc
        print(f"[led] blink {index + 1}/{count}", file=sys.stderr)
        time.sleep(interval)


def wait_for_stable_file(path: Path, checks: int = 3, delay: float = 0.2) -> None:
    previous_size = -1
    stable_count = 0
    while stable_count < checks:
        size = path.stat().st_size
        if size == previous_size and size > 0:
            stable_count += 1
        else:
            stable_count = 0
            previous_size = size
        time.sleep(delay)


def process_image(image: Path, args: argparse.Namespace) -> bool:
    try:
        wait_for_stable_file(image)
        print(f"[image] {image}", file=sys.stderr)
        answer, used_provider = solve(image, args.provider, args.gemini_model, args.ollama_model, args.timeout)
        print(f"[answer] {answer} via {used_provider}")
        blink_caps(answer, args.interval, args.dry_run)
        return True
    except Exception as exc:  # noqa: BLE001 - CLI entry point
        print(f"[error] {exc}", file=sys.stderr)
        return False


def watch_screenshots(args: argparse.Namespace) -> int:
    args.dir.mkdir(parents=True, exist_ok=True)
    last_key: tuple[int, str] | None = None
    if not args.process_existing:
        try:
            image = newest_image(args.dir)
            last_key = (image.stat().st_mtime_ns, str(image))
            print(f"[watch] baseline {image}", file=sys.stderr)
        except FileNotFoundError:
            print(f"[watch] no existing screenshots in {args.dir}", file=sys.stderr)
    print(f"[watch] watching {args.dir}", file=sys.stderr)

    while True:
        try:
            image = newest_image(args.dir)
            key = (image.stat().st_mtime_ns, str(image))
            if key != last_key:
                last_key = key
                process_image(image, args)
        except FileNotFoundError as exc:
            print(f"[watch] {exc}", file=sys.stderr)
        time.sleep(args.poll)


def main(argv: Iterable[str] | None = None) -> int:
    load_config_env()
    parser = argparse.ArgumentParser(description="Newest screenshot -> AI answer A-F -> Caps Lock LED signal")
    parser.add_argument("--dir", type=Path, default=SCREENSHOT_DIR, help="Screenshot directory")
    parser.add_argument("--image", type=Path, help="Specific image file. Defaults to newest image in --dir")
    parser.add_argument("--provider", choices=["auto", "gemini", "ollama"], default="auto")
    parser.add_argument("--gemini-model", default=os.environ.get("GEMINI_MODEL", "gemini-3.5-flash"))
    parser.add_argument("--ollama-model", default=os.environ.get("OLLAMA_MODEL", "qwen2.5vl:7b"))
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--interval", type=float, default=0.22, help="Delay between Caps Lock key events")
    parser.add_argument("--dry-run", action="store_true", help="Do not blink LED")
    parser.add_argument("--watch", action="store_true", help="Watch screenshot folder and solve every new image")
    parser.add_argument("--poll", type=float, default=0.5, help="Watch polling interval in seconds")
    parser.add_argument("--process-existing", action="store_true", help="In watch mode, process current newest image immediately")
    args = parser.parse_args(argv)

    if args.watch:
        try:
            return watch_screenshots(args)
        except KeyboardInterrupt:
            print("\n[watch] stopped", file=sys.stderr)
            return 0

    image = args.image or newest_image(args.dir)
    return 0 if process_image(image, args) else 1


if __name__ == "__main__":
    raise SystemExit(main())
