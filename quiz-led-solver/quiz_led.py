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
ANSWER_RE = re.compile(r"[A-Z]", re.IGNORECASE)
CAPS_LOCK_KEYCODE = 58

PROMPT = """You are solving a multiple-choice or multiple-select quiz question from a screenshot.
Carefully identify the OUTER answer choices/labels (e.g. A, B, C, D, E, F...) and determine which outer choice label(s) correspond to the correct option(s).
Do NOT confuse inner statement letters (e.g. A. Sao Thủy, B. Sao Kim...) with the outer answer choices (e.g. A. D, B. A, C. B...). Always select the OUTER answer choice letter(s) that point to the correct answer.

Respond ONLY with the uppercase outer answer choice letter(s) (e.g., A, B, C, D, A B, etc.).
Sort the letters alphabetically with no spaces, explanations, or punctuation (e.g. "A", "AC", "ABD").
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
    # Remove common words to prevent matching letters inside words like "AND", "OR", "CHOICE"
    cleaned_text = re.sub(r"\b(AND|OR|OPTION|OPTIONS|CHOICE|CHOICES|IS|ARE|CORRECT)\b", " ", text, flags=re.IGNORECASE)
    matches = ANSWER_RE.findall(cleaned_text)
    if not matches:
        matches = ANSWER_RE.findall(text)
    if not matches:
        raise ValueError(f"Could not parse A-Z answer from: {text!r}")

    unique_sorted = sorted(set(letter.upper() for letter in matches))
    return "".join(unique_sorted)


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
            "maxOutputTokens": 1024,
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

    # Filter for visible text parts, excluding reasoning-only thought parts if present
    text_parts = [
        part.get("text", "")
        for part in parts
        if not part.get("thought", False) and "text" in part
    ]
    if not text_parts:
        text_parts = [part.get("text", "") for part in parts if "text" in part]

    text = "".join(text_parts)
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
            "num_predict": 16,
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


def solve(path: Path, provider: str, gemini_models: list[str], ollama_model: str, timeout: float) -> tuple[str, str]:
    errors: list[str] = []
    for name in provider_order(provider):
        if name == "gemini":
            for model in gemini_models:
                try:
                    print(f"[ai] trying gemini:{model}...", file=sys.stderr)
                    return ask_gemini(path, model, timeout), f"gemini:{model}"
                except Exception as exc:  # noqa: BLE001 - CLI should show all model failures
                    errors.append(f"gemini:{model}: {exc}")
                    print(f"[ai] gemini:{model} failed: {exc}", file=sys.stderr)
            continue
        if name == "ollama":
            try:
                print(f"[ai] trying ollama...", file=sys.stderr)
                return ask_ollama(path, ollama_model, timeout), "ollama"
            except Exception as exc:  # noqa: BLE001 - CLI should show all provider failures
                errors.append(f"ollama: {exc}")
                print(f"[ai] ollama failed: {exc}", file=sys.stderr)
            continue
        raise ValueError(f"Unknown provider: {name}")

    raise RuntimeError("All providers failed:\n" + "\n".join(errors))


def blink_count(letter: str) -> int:
    return (ord(letter) - ord("A") + 1) * 2


def run_ydotool_key(keycode: int) -> None:
    subprocess.run(
        ["ydotool", "key", f"{keycode}:1", f"{keycode}:0"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )


def blink_caps(answer: str, interval: float, group_interval: float, dry_run: bool) -> None:
    letters = list(answer)
    print(f"[led] answer={answer} -> letters={letters!r}", file=sys.stderr)

    for idx, letter in enumerate(letters):
        count = blink_count(letter)
        if dry_run:
            print(f"[led] (dry-run) letter {letter}: Caps Lock key events={count}", file=sys.stderr)
        else:
            for index in range(count):
                try:
                    run_ydotool_key(CAPS_LOCK_KEYCODE)
                except subprocess.CalledProcessError as exc:
                    raise RuntimeError(
                        "ydotool failed. Make sure ydotoold is running and socket is accessible. "
                        f"stderr={exc.stderr.strip()!r}"
                    ) from exc
                print(f"[led] letter {letter} blink {index + 1}/{count}", file=sys.stderr)
                time.sleep(interval)

        if idx < len(letters) - 1 and group_interval > 0:
            time.sleep(group_interval)


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
        answer, used_provider = solve(image, args.provider, args.gemini_models, args.ollama_model, args.timeout)
        print(f"[answer] {answer} via {used_provider}")
        blink_caps(answer, args.interval, args.group_interval, args.dry_run)
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
    parser.add_argument("--gemini-model", action="append", help="Gemini model in fallback order (repeatable). Default: gemini-3.7-flash, gemini-flash-latest, gemini-3.5-flash, gemini-flash-lite-latest")
    parser.add_argument("--ollama-model", default=os.environ.get("OLLAMA_MODEL", "qwen2.5vl:7b"))
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--interval", type=float, default=0.22, help="Delay between Caps Lock key events")
    parser.add_argument("--group-interval", type=float, default=1.0, help="Delay between multiple answer letters")
    parser.add_argument("--dry-run", action="store_true", help="Do not blink LED")
    parser.add_argument("--watch", action="store_true", help="Watch screenshot folder and solve every new image")
    parser.add_argument("--poll", type=float, default=0.5, help="Watch polling interval in seconds")
    parser.add_argument("--process-existing", action="store_true", help="In watch mode, process current newest image immediately")
    args = parser.parse_args(argv)

    if args.gemini_model:
        gemini_models = args.gemini_model
    elif "GEMINI_MODELS" in os.environ:
        gemini_models = [m.strip() for m in os.environ["GEMINI_MODELS"].split(",") if m.strip()]
    else:
        gemini_models = [
            os.environ.get("GEMINI_MODEL_1", "gemini-3.7-flash"),
            os.environ.get("GEMINI_MODEL_2", "gemini-flash-latest"),
            os.environ.get("GEMINI_MODEL_3", "gemini-3.5-flash"),
            os.environ.get("GEMINI_MODEL_4", "gemini-flash-lite-latest"),
        ]
    args.gemini_models = gemini_models

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
