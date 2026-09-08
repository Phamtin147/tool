#!/usr/bin/env python3
"""CLI tool: newest screenshot -> Vision AI (Gemini 2.5 / 2.0 / Ollama) -> blink Caps Lock answer code.

Developed by: Amtia / Phamtin147 (https://github.com/Phamtin147)

Answer encoding:
A=1 blink, B=2 blinks, C=3 blinks, D=4 blinks, E=5 blinks, F=6 blinks.
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
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Iterable

import requests

SCREENSHOT_DIR = Path.home() / "Pictures" / "screenshots"
CONFIG_ENV_PATHS = [
    Path(__file__).resolve().parent / ".config" / "gemini.env",
    Path.home() / ".config" / "gemini.env",
    Path.home() / ".config" / "ryoku" / "gemini.env",
    Path(__file__).resolve().parent / ".env",
    Path.home() / ".env",
]
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
ANSWER_RE = re.compile(r"[A-Z]", re.IGNORECASE)
CAPS_LOCK_KEYCODE = 58

SYSTEM_INSTRUCTION = (
    "You are a precise multiple-choice quiz solver. You will be provided with an image of a quiz question. "
    "Carefully identify the OUTER answer choices/labels (e.g. A, B, C, D, E, F...) and determine which outer choice label(s) "
    "correspond to the correct option(s). Do NOT confuse inner statement letters (e.g. A. Statement 1, B. Statement 2...) with the outer answer choices. "
    "Respond ONLY with the uppercase outer answer choice letter(s) (e.g. 'A', 'B', 'C', 'AC', 'ABD'). "
    "Sort the letters alphabetically with no spaces, explanations, markdown, or punctuation."
)

PROMPT = "Identify and return ONLY the correct outer choice letter(s) (A-Z) for this quiz question."

DEFAULT_GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-2.5-pro",
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash",
]


def load_config_env() -> None:
    """Load KEY=VALUE lines from known config env paths into os.environ."""
    for config_path in CONFIG_ENV_PATHS:
        if not config_path.exists():
            continue
        try:
            for line in config_path.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip("'\"")
                if key and key not in os.environ:
                    os.environ[key] = value
        except Exception:
            pass


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
    # Remove common filler words to prevent matching letters inside words like "AND", "OPTION", etc.
    cleaned_text = re.sub(
        r"\b(AND|OR|OPTION|OPTIONS|CHOICE|CHOICES|IS|ARE|CORRECT|ANSWER|THE)\b",
        " ",
        text,
        flags=re.IGNORECASE,
    )
    matches = ANSWER_RE.findall(cleaned_text)
    if not matches:
        matches = ANSWER_RE.findall(text)
    if not matches:
        raise ValueError(f"Could not parse A-Z answer from: {text!r}")

    # Restrict to reasonable quiz choices A-F (or A-Z if multiple)
    valid_letters = [letter.upper() for letter in matches if "A" <= letter.upper() <= "Z"]
    if not valid_letters:
        raise ValueError(f"No valid choice letters found in: {text!r}")

    unique_sorted = sorted(set(valid_letters))
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
        "systemInstruction": {
            "parts": [{"text": SYSTEM_INSTRUCTION}]
        },
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
            "temperature": 0.0,
            "maxOutputTokens": 128,
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

    # Filter for visible text parts, excluding reasoning-only thought parts in Gemini 2.5/Thinking models
    text_parts = [
        part.get("text", "")
        for part in parts
        if not part.get("thought", False) and "text" in part
    ]
    if not text_parts:
        text_parts = [part.get("text", "") for part in parts if "text" in part]

    text = "".join(text_parts).strip()
    if not text:
        raise RuntimeError(f"Empty Gemini response: {json.dumps(data)[:500]}")
    return parse_answer(text)


def ask_openrouter(path: Path, model: str, timeout: float) -> str:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENROUTER_API_KEY")

    b64_img = image_to_base64(path)
    mime = mime_type(path)
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/Phamtin147/tool",
        "X-Title": "Quiz LED Solver",
    }
    payload = {
        "model": model,
        "temperature": 0.0,
        "max_tokens": 64,
        "messages": [
            {"role": "system", "content": SYSTEM_INSTRUCTION},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime};base64,{b64_img}"},
                    },
                ],
            },
        ],
    }
    response = requests.post(url, headers=headers, json=payload, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    text = data["choices"][0]["message"]["content"]
    return parse_answer(text)


def ask_ollama(path: Path, model: str, timeout: float) -> str:
    host = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
    payload = {
        "model": model,
        "prompt": f"{SYSTEM_INSTRUCTION}\n\n{PROMPT}",
        "images": [image_to_base64(path)],
        "stream": False,
        "options": {
            "temperature": 0.0,
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
        order = ["gemini"]
        if os.environ.get("OPENROUTER_API_KEY"):
            order.append("openrouter")
        order.append("ollama")
        return order
    return [provider]


def solve(
    path: Path,
    provider: str,
    gemini_models: list[str],
    openrouter_model: str,
    ollama_model: str,
    timeout: float,
    race: bool = True,
) -> tuple[str, str]:
    errors: list[str] = []
    for name in provider_order(provider):
        if name == "gemini":
            if race and len(gemini_models) > 1:
                print(
                    f"[ai] racing {len(gemini_models)} Gemini models in parallel: {', '.join(gemini_models)}...",
                    file=sys.stderr,
                )
                t_start = time.time()
                executor = ThreadPoolExecutor(max_workers=len(gemini_models))
                futures = {
                    executor.submit(ask_gemini, path, model, timeout): model
                    for model in gemini_models
                }
                try:
                    for future in as_completed(futures):
                        model = futures[future]
                        try:
                            ans = future.result()
                            dt = time.time() - t_start
                            print(
                                f"[ai] fastest response from gemini:{model} in {dt:.2f}s -> answer {ans}",
                                file=sys.stderr,
                            )
                            executor.shutdown(wait=False, cancel_futures=True)
                            return ans, f"gemini:{model}"
                        except Exception as exc:  # noqa: BLE001
                            errors.append(f"gemini:{model}: {exc}")
                            print(f"[ai] gemini:{model} failed: {exc}", file=sys.stderr)
                finally:
                    executor.shutdown(wait=False, cancel_futures=True)
            else:
                for model in gemini_models:
                    try:
                        print(f"[ai] trying gemini:{model}...", file=sys.stderr)
                        return ask_gemini(path, model, timeout), f"gemini:{model}"
                    except Exception as exc:  # noqa: BLE001
                        errors.append(f"gemini:{model}: {exc}")
                        print(f"[ai] gemini:{model} failed: {exc}", file=sys.stderr)
            continue

        if name == "openrouter":
            try:
                print(f"[ai] trying openrouter:{openrouter_model}...", file=sys.stderr)
                return ask_openrouter(path, openrouter_model, timeout), f"openrouter:{openrouter_model}"
            except Exception as exc:  # noqa: BLE001
                errors.append(f"openrouter: {exc}")
                print(f"[ai] openrouter failed: {exc}", file=sys.stderr)
            continue

        if name == "ollama":
            try:
                print(f"[ai] trying ollama:{ollama_model}...", file=sys.stderr)
                return ask_ollama(path, ollama_model, timeout), f"ollama:{ollama_model}"
            except Exception as exc:  # noqa: BLE001
                errors.append(f"ollama: {exc}")
                print(f"[ai] ollama failed: {exc}", file=sys.stderr)
            continue

        raise ValueError(f"Unknown provider: {name}")

    raise RuntimeError("All providers failed:\n" + "\n".join(errors))


def blink_count(letter: str) -> int:
    return ord(letter.upper()) - ord("A") + 1


def is_caps_on() -> bool:
    """Check if any Caps Lock LED is currently active in sysfs."""
    import glob
    for p in glob.glob("/sys/class/leds/*::capslock/brightness"):
        try:
            with open(p) as f:
                if int(f.read().strip()) > 0:
                    return True
        except Exception:
            pass
    return False


def find_capslock_leds() -> list[str]:
    """Find all hardware Caps Lock LED device names."""
    import glob
    led_paths = glob.glob("/sys/class/leds/*::capslock")
    return [Path(p).name for p in led_paths]


def set_led_brightness(devices: list[str], brightness: int) -> bool:
    """Set brightness on all Caps Lock LED devices using brightnessctl."""
    success = False
    for dev in devices:
        res = subprocess.run(
            ["brightnessctl", f"--device={dev}", "set", str(brightness)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if res.returncode == 0:
            success = True
    return success


def run_ydotool_key(keycode: int) -> None:
    subprocess.run(
        ["ydotool", "key", "-d", "60", f"{keycode}:1", f"{keycode}:0"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )


def ensure_caps_off(led_devices: list[str]) -> None:
    """Ensure Caps Lock is in OFF state before/after blinking."""
    if is_caps_on():
        try:
            run_ydotool_key(CAPS_LOCK_KEYCODE)
            time.sleep(0.05)
        except Exception:
            pass
    if led_devices:
        set_led_brightness(led_devices, 0)


def blink_caps(
    answer: str,
    interval: float,
    group_interval: float,
    dry_run: bool,
    backend: str = "auto",
) -> None:
    letters = list(answer)
    print(f"[led] answer={answer} -> letters={letters!r}", file=sys.stderr)

    led_devices = find_capslock_leds() if backend in ("auto", "brightnessctl") else []

    for idx, letter in enumerate(letters):
        count = blink_count(letter)
        if dry_run:
            print(f"[led] (dry-run) letter {letter}: Caps Lock blink count={count}", file=sys.stderr)
        else:
            ensure_caps_off(led_devices)
            time.sleep(0.05)
            for index in range(count):
                # Turn ON
                try:
                    run_ydotool_key(CAPS_LOCK_KEYCODE)
                except Exception:
                    pass
                if led_devices:
                    set_led_brightness(led_devices, 1)
                print(f"[led] letter {letter} blink {index + 1}/{count} (ON)", file=sys.stderr)
                time.sleep(interval)

                # Turn OFF
                try:
                    run_ydotool_key(CAPS_LOCK_KEYCODE)
                except Exception:
                    pass
                if led_devices:
                    set_led_brightness(led_devices, 0)
                print(f"[led] letter {letter} blink {index + 1}/{count} (OFF)", file=sys.stderr)
                time.sleep(interval)

            ensure_caps_off(led_devices)

        if idx < len(letters) - 1 and group_interval > 0:
            time.sleep(group_interval)


def wait_for_stable_file(path: Path, checks: int = 2, delay: float = 0.1) -> None:
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
        answer, used_provider = solve(
            image,
            args.provider,
            args.gemini_models,
            args.openrouter_model,
            args.ollama_model,
            args.timeout,
            race=args.race,
        )
        print(f"[answer] {answer} via {used_provider}")
        blink_caps(answer, args.interval, args.group_interval, args.dry_run, backend=args.led_backend)
        return True
    except Exception as exc:  # noqa: BLE001
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
    print("[Quiz LED Solver] v2.5 - Gemini 2.5/2.0 Vision by Amtia / Phamtin147", file=sys.stderr)
    parser = argparse.ArgumentParser(
        description="Newest screenshot -> Gemini 2.5/2.0 Vision AI answer A-F -> Caps Lock LED signal (by Amtia / Phamtin147)"
    )
    parser.add_argument("--dir", type=Path, default=SCREENSHOT_DIR, help="Screenshot directory (default: ~/Pictures/screenshots)")
    parser.add_argument("--image", "--file", type=Path, dest="image", help="Specific image file. Defaults to newest image in --dir")
    parser.add_argument("--provider", choices=["auto", "gemini", "openrouter", "ollama"], default="auto")
    parser.add_argument(
        "--gemini-model",
        action="append",
        help="Gemini model in fallback/race order. Default: gemini-2.5-flash, gemini-2.0-flash, gemini-2.5-pro, gemini-2.0-flash-lite, gemini-1.5-flash",
    )
    parser.add_argument(
        "--openrouter-model",
        default=os.environ.get("OPENROUTER_MODEL", "google/gemini-2.5-flash"),
        help="OpenRouter model (default: google/gemini-2.5-flash)",
    )
    parser.add_argument("--ollama-model", default=os.environ.get("OLLAMA_MODEL", "qwen2.5vl:7b"))
    parser.add_argument("--timeout", type=float, default=12.0, help="Per-model API timeout in seconds")
    parser.add_argument("--interval", "--blink-ms", type=float, default=0.20, help="Delay between Caps Lock key/LED events in seconds")
    parser.add_argument("--group-interval", "--gap-ms", type=float, default=0.8, help="Delay between multiple answer letters")
    parser.add_argument(
        "--led-backend",
        choices=["auto", "brightnessctl", "ydotool"],
        default="auto",
        help="LED signaling backend (default: auto)",
    )
    parser.add_argument(
        "--race",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Query multiple Gemini models concurrently and take the fastest result (default: True)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Do not blink LED, only output answer")
    parser.add_argument("--watch", action="store_true", help="Watch screenshot folder and solve every new image")
    parser.add_argument("--poll", "--poll-interval", type=float, default=0.4, help="Watch polling interval in seconds")
    parser.add_argument("--process-existing", action="store_true", help="In watch mode, process current newest image immediately")
    args = parser.parse_args(argv)

    if args.gemini_model:
        gemini_models = args.gemini_model
    elif "GEMINI_MODELS" in os.environ:
        gemini_models = [m.strip() for m in os.environ["GEMINI_MODELS"].split(",") if m.strip()]
    else:
        gemini_models = [
            os.environ.get("GEMINI_MODEL_1", "gemini-2.5-flash"),
            os.environ.get("GEMINI_MODEL_2", "gemini-2.0-flash"),
            os.environ.get("GEMINI_MODEL_3", "gemini-2.5-pro"),
            os.environ.get("GEMINI_MODEL_4", "gemini-2.0-flash-lite"),
            os.environ.get("GEMINI_MODEL_5", "gemini-1.5-flash"),
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
