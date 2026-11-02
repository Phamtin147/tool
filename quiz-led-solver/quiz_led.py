#!/usr/bin/env python3
"""CLI tool: newest screenshot -> Vision AI (Gemini 3.8 / 3.7 / 3.5 / Ollama) -> blink Caps Lock answer code.

Developed by: Amtia / Phamtin147 (https://github.com/Phamtin147)

Answer encoding:
A=1 blink, B=2 blinks, C=3 blinks, D=4 blinks, E=5 blinks, F=6 blinks.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import signal
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
VALID_CHOICES = set("ABCDEF")
MAX_MULTI_CHOICES = 4
CAPS_LOCK_KEYCODE = 58

SYSTEM_INSTRUCTION = (
    "You are a precise multiple-choice quiz solver. You will be provided with an image of a quiz question. "
    "Carefully identify the OUTER answer choices/labels (e.g. A, B, C, D, E, F) and determine which outer choice label(s) "
    "correspond to the correct option(s). Do NOT confuse inner statement letters (e.g. A. Statement 1, B. Statement 2...) with the outer answer choices. "
    "If the image does NOT contain a quiz question or cannot be solved, respond ONLY with 'NONE'. "
    "Otherwise, respond ONLY with the uppercase outer answer choice letter(s) from A to F (e.g. 'A', 'B', 'C', 'AC'). "
    "Sort the letters alphabetically with no spaces, explanations, markdown, or punctuation."
)

PROMPT = "Identify and return ONLY the correct outer choice letter(s) (A-F) for this quiz question, or NONE if no quiz question is present."

DEFAULT_GEMINI_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-3-flash-preview",
    "gemini-3.1-flash-lite",
]

FALLBACK_GEMINI_MODELS: list[str] = []


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
                if key:
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


class NoQuizFoundError(ValueError):
    """Raised when the AI explicitly determines the image has no quiz question."""


def parse_answer(text: str) -> str:
    """Strictly parse quiz choice letters (A-F) and reject prose/error messages."""
    raw = text.strip()
    if not raw:
        raise ValueError("Empty response text")

    # Check if AI explicitly indicated no quiz / error
    upper_raw = raw.upper()
    if upper_raw in {"NONE", "N/A", "NULL", "ERROR", "UNKNOWN"} or any(
        phrase in upper_raw
        for phrase in (
            "THIS IMAGE",
            "CANNOT",
            "UNABLE",
            "NO QUIZ",
            "NO QUESTION",
            "NOT CONTAIN",
            "SORRY",
            "I DON'T SEE",
            "APOLOGIZE",
        )
    ):
        raise NoQuizFoundError(f"Non-quiz or refusal response from AI: {raw!r}")

    # Case 1: Clean compact response like "B", "AC", "A, C", "A and C", "**B**"
    compact = re.sub(r"[\s,*_`\"'()\[\].:-]+", "", upper_raw)
    if 1 <= len(compact) <= MAX_MULTI_CHOICES and all(ch in VALID_CHOICES for ch in compact):
        return "".join(sorted(set(compact)))

    # Case 2: Look for explicit "Answer: X" / "Option X" pattern at the end
    explicit_match = re.search(
        r"(?:ANSWER|OPTION|CHOICE|IS)\s*[:=-]?\s*\**([A-F](?:\s*(?:,|AND|&|\s)\s*[A-F])*)\**\s*\.?\s*$",
        upper_raw,
    )
    if explicit_match:
        letters = [ch for ch in explicit_match.group(1) if ch in VALID_CHOICES]
        unique_sorted = sorted(set(letters))
        if 1 <= len(unique_sorted) <= MAX_MULTI_CHOICES:
            return "".join(unique_sorted)

    # Case 3: Standalone single choice letters (A-F) separated by punctuation/spaces, only if total text is short
    if len(raw) <= 24:
        tokens = re.findall(r"\b([A-F])\b", upper_raw)
        unique_sorted = sorted(set(tokens))
        if 1 <= len(unique_sorted) <= MAX_MULTI_CHOICES:
            return "".join(unique_sorted)

    raise ValueError(f"Could not parse valid A-F answer from: {raw!r}")


def mime_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".png":
        return "image/png"
    if suffix in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if suffix == ".webp":
        return "image/webp"
    return "application/octet-stream"


MODEL_COOLDOWN_UNTIL: dict[tuple[str, str], float] = {}


def get_gemini_api_keys() -> list[str]:
    """Return list of configured Gemini API keys (supports comma-separated or numbered keys)."""
    raw_keys: list[str] = []
    for var in ("GEMINI_API_KEYS", "GEMINI_API_KEY", "GOOGLE_API_KEY"):
        val = os.environ.get(var, "").strip()
        if val:
            raw_keys.extend(k.strip() for k in val.split(",") if k.strip())
    for idx in range(1, 10):
        val = os.environ.get(f"GEMINI_API_KEY_{idx}", "").strip()
        if val:
            raw_keys.append(val)
    # Deduplicate while preserving order
    seen: set[str] = set()
    keys: list[str] = []
    for k in raw_keys:
        if k not in seen:
            seen.add(k)
            keys.append(k)
    return keys


def ask_gemini(path: Path, model: str, timeout: float) -> str:
    api_keys = get_gemini_api_keys()
    if not api_keys:
        raise RuntimeError("Missing GEMINI_API_KEY or GOOGLE_API_KEY")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    b64_data = image_to_base64(path)
    mime = mime_type(path)

    last_err: Exception | None = None
    now = time.time()

    # Try available API keys not currently in cooldown for this model
    active_keys = [k for k in api_keys if MODEL_COOLDOWN_UNTIL.get((k, model), 0.0) <= now]
    if not active_keys:
        active_keys = api_keys

    for api_key in active_keys:
        params = {"key": api_key}
        gen_config: dict[str, object] = {
            "temperature": 0.0,
            "maxOutputTokens": 1024,
        }

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
                                "mime_type": mime,
                                "data": b64_data,
                            }
                        },
                    ],
                }
            ],
            "generationConfig": gen_config,
        }

        try:
            response = requests.post(url, params=params, json=payload, timeout=timeout)

            if response.status_code == 429:
                MODEL_COOLDOWN_UNTIL[(api_key, model)] = time.time() + 1800.0
                body = response.text[:300]
                last_err = RuntimeError(f"Gemini HTTP 429 (Quota exhausted, cooling down {model} for 30m): {body}")
                continue
            if response.status_code == 404:
                MODEL_COOLDOWN_UNTIL[(api_key, model)] = time.time() + 86400.0
            elif response.status_code >= 500:
                MODEL_COOLDOWN_UNTIL[(api_key, model)] = time.time() + 45.0

            try:
                response.raise_for_status()
            except requests.HTTPError as exc:
                body = response.text[:500]
                raise RuntimeError(f"Gemini HTTP {response.status_code}: {body}") from exc
        except requests.Timeout as exc:
            MODEL_COOLDOWN_UNTIL[(api_key, model)] = time.time() + 45.0
            last_err = exc
            continue
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            continue

        data = response.json()
        try:
            parts = data["candidates"][0]["content"]["parts"]
        except (KeyError, IndexError, TypeError) as exc:
            last_err = RuntimeError(f"Unexpected Gemini response: {json.dumps(data)[:500]}")
            continue

        text_parts = [
            part.get("text", "")
            for part in parts
            if not part.get("thought", False) and "text" in part
        ]
        if not text_parts:
            text_parts = [part.get("text", "") for part in parts if "text" in part]

        text = "".join(text_parts).strip()
        if not text:
            last_err = RuntimeError(f"Empty Gemini response: {json.dumps(data)[:500]}")
            continue
        return parse_answer(text)

    if last_err is not None:
        raise last_err
    raise RuntimeError(f"Gemini failed for model {model}")


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


def _available_gemini_models(models: list[str]) -> list[str]:
    """Return models not currently in 429/503 cooldown (fallback to all if all are cooling)."""
    now = time.time()
    api_keys = get_gemini_api_keys()
    if not api_keys:
        return models
    ready = [
        m
        for m in models
        if any(MODEL_COOLDOWN_UNTIL.get((k, m), 0.0) <= now for k in api_keys)
    ]
    return ready if ready else models


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
            ordered_models = _available_gemini_models(gemini_models)
            if race and len(ordered_models) > 1:
                print(
                    f"[ai] racing {len(ordered_models)} Gemini models in parallel: {', '.join(ordered_models)}...",
                    file=sys.stderr,
                )
                t_start = time.time()
                executor = ThreadPoolExecutor(max_workers=len(ordered_models))
                futures = {
                    executor.submit(ask_gemini, path, model, timeout): model
                    for model in ordered_models
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
                for model in ordered_models:
                    try:
                        print(f"[ai] trying gemini:{model}...", file=sys.stderr)
                        t0 = time.perf_counter()
                        ans = ask_gemini(path, model, timeout)
                        dt = time.perf_counter() - t0
                        print(f"[ai] response from gemini:{model} in {dt:.2f}s -> answer {ans}", file=sys.stderr)
                        return ans, f"gemini:{model}"
                    except NoQuizFoundError:
                        raise
                    except Exception as exc:  # noqa: BLE001
                        errors.append(f"gemini:{model}: {exc}")
                        print(f"[ai] gemini:{model} failed: {exc}", file=sys.stderr)

            for fb_model in _available_gemini_models(FALLBACK_GEMINI_MODELS):
                if fb_model in ordered_models:
                    continue
                try:
                    print(f"[ai] fallback trying gemini:{fb_model}...", file=sys.stderr)
                    t0 = time.perf_counter()
                    ans = ask_gemini(path, fb_model, timeout)
                    dt = time.perf_counter() - t0
                    print(f"[ai] response from gemini:{fb_model} in {dt:.2f}s -> answer {ans}", file=sys.stderr)
                    return ans, f"gemini:{fb_model}"
                except Exception as exc:  # noqa: BLE001
                    errors.append(f"gemini:{fb_model}: {exc}")
                    print(f"[ai] gemini:{fb_model} failed: {exc}", file=sys.stderr)
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
    if led_devices:
        set_led_brightness(led_devices, 0)
    elif is_caps_on():
        try:
            run_ydotool_key(CAPS_LOCK_KEYCODE)
            time.sleep(0.05)
        except Exception:
            pass


def set_caps_state(led_devices: list[str], on: bool) -> None:
    """Set Caps Lock LED state using brightnessctl if available, otherwise ydotool."""
    if led_devices:
        set_led_brightness(led_devices, 1 if on else 0)
    else:
        try:
            run_ydotool_key(CAPS_LOCK_KEYCODE)
        except Exception:
            pass


def blink_error(dry_run: bool = False, backend: str = "auto", flashes: int = 3, flash_interval: float = 0.06) -> None:
    """Emit a brief rapid strobe (default: 3 ultra-fast flashes in ~0.35s) to signal API/parse error, then force LED off."""
    if dry_run:
        print(f"[led] (dry-run) error signal: {flashes} rapid flashes", file=sys.stderr)
        return

    led_devices = find_capslock_leds() if backend in ("auto", "brightnessctl") else []
    try:
        ensure_caps_off(led_devices)
        time.sleep(0.04)
        for _ in range(flashes):
            set_caps_state(led_devices, True)
            time.sleep(flash_interval)
            set_caps_state(led_devices, False)
            time.sleep(flash_interval)
    finally:
        ensure_caps_off(led_devices)


def blink_caps(
    answer: str,
    interval: float,
    group_interval: float,
    dry_run: bool,
    backend: str = "auto",
) -> None:
    # Hard safety filter: only allow A-F and at most MAX_MULTI_CHOICES letters
    letters = [ch.upper() for ch in answer if ch.upper() in VALID_CHOICES][:MAX_MULTI_CHOICES]
    if not letters:
        print(f"[led] no valid A-F letters to blink from answer={answer!r}", file=sys.stderr)
        return

    print(f"[led] answer={answer} -> letters={letters!r}", file=sys.stderr)

    led_devices = find_capslock_leds() if backend in ("auto", "brightnessctl") else []

    try:
        for idx, letter in enumerate(letters):
            count = min(blink_count(letter), 6)  # Hard cap at 6 blinks per letter (F)
            if dry_run:
                print(f"[led] (dry-run) letter {letter}: Caps Lock blink count={count}", file=sys.stderr)
            else:
                ensure_caps_off(led_devices)
                time.sleep(0.05)
                for index in range(count):
                    # Turn ON
                    set_caps_state(led_devices, True)
                    print(f"[led] letter {letter} blink {index + 1}/{count} (ON)", file=sys.stderr)
                    time.sleep(interval)

                    # Turn OFF
                    set_caps_state(led_devices, False)
                    print(f"[led] letter {letter} blink {index + 1}/{count} (OFF)", file=sys.stderr)
                    time.sleep(interval)

                ensure_caps_off(led_devices)

            if idx < len(letters) - 1 and group_interval > 0:
                time.sleep(group_interval)
    finally:
        if not dry_run:
            ensure_caps_off(led_devices)


def wait_for_stable_file(path: Path, checks: int = 3, delay: float = 0.1) -> None:
    previous_size = -1
    previous_mtime = -1
    stable_count = 0
    while stable_count < checks:
        st = path.stat()
        if st.st_size > 0 and st.st_size == previous_size and st.st_mtime_ns == previous_mtime:
            stable_count += 1
        else:
            stable_count = 0
            previous_size = st.st_size
            previous_mtime = st.st_mtime_ns
        time.sleep(delay)


def file_signature(path: Path) -> tuple[str, str]:
    """Return (resolved_path, sha256_hex) to prevent double-processing the same screenshot."""
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return (str(path.resolve()), digest)


def process_image(image: Path, args: argparse.Namespace) -> bool:
    try:
        load_config_env()
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
        if getattr(args, "error_blink", True):
            blink_error(dry_run=args.dry_run, backend=args.led_backend)
        return False


def watch_screenshots(args: argparse.Namespace) -> int:
    args.dir.mkdir(parents=True, exist_ok=True)
    last_key: tuple[int, str] | None = None
    seen_signatures: set[tuple[str, str]] = set()
    if not args.process_existing:
        try:
            image = newest_image(args.dir)
            wait_for_stable_file(image)
            last_key = (image.stat().st_mtime_ns, str(image))
            seen_signatures.add(file_signature(image))
            print(f"[watch] baseline {image}", file=sys.stderr)
        except FileNotFoundError:
            print(f"[watch] no existing screenshots in {args.dir}", file=sys.stderr)
    print(f"[watch] watching {args.dir}", file=sys.stderr)

    while True:
        try:
            image = newest_image(args.dir)
            key = (image.stat().st_mtime_ns, str(image))
            if key != last_key:
                wait_for_stable_file(image)
                sig = file_signature(image)
                last_key = (image.stat().st_mtime_ns, str(image))
                if sig not in seen_signatures:
                    seen_signatures.add(sig)
                    process_image(image, args)
                    if image.exists():
                        last_key = (image.stat().st_mtime_ns, str(image))
        except FileNotFoundError as exc:
            print(f"[watch] {exc}", file=sys.stderr)
        time.sleep(args.poll)


def main(argv: Iterable[str] | None = None) -> int:
    load_config_env()
    print("[Quiz LED Solver] v3.8 - Gemini 3.8/3.7/3.5 Vision by Amtia / Phamtin147", file=sys.stderr)
    parser = argparse.ArgumentParser(
        description="Newest screenshot -> Gemini 3.8/3.7/3.5 Vision AI answer A-F -> Caps Lock LED signal (by Amtia / Phamtin147)"
    )
    parser.add_argument("--dir", type=Path, default=SCREENSHOT_DIR, help="Screenshot directory (default: ~/Pictures/screenshots)")
    parser.add_argument("--image", "--file", type=Path, dest="image", help="Specific image file. Defaults to newest image in --dir")
    parser.add_argument("--provider", choices=["auto", "gemini", "openrouter", "ollama"], default="auto")
    parser.add_argument(
        "--gemini-model",
        action="append",
        help="Gemini model in fallback order. Default: gemini-3.5-flash-lite, gemini-3.5-flash, gemini-3-flash-preview, gemini-3.1-flash-lite",
    )
    parser.add_argument(
        "--openrouter-model",
        default=os.environ.get("OPENROUTER_MODEL", "google/gemini-3.8-flash"),
        help="OpenRouter model (default: google/gemini-3.8-flash)",
    )
    parser.add_argument("--ollama-model", default=os.environ.get("OLLAMA_MODEL", "qwen2.5vl:7b"))
    parser.add_argument("--timeout", type=float, default=10.0, help="Per-model API timeout in seconds")
    parser.add_argument(
        "--interval",
        "--blink-ms",
        type=float,
        default=float(os.environ.get("BLINK_INTERVAL", "0.35")),
        help="Delay between Caps Lock key/LED events in seconds (default: 0.35s)",
    )
    parser.add_argument(
        "--group-interval",
        "--gap-ms",
        type=float,
        default=float(os.environ.get("GROUP_INTERVAL", "1.0")),
        help="Delay between multiple answer letters in seconds (default: 1.0s)",
    )
    parser.add_argument(
        "--led-backend",
        choices=["auto", "brightnessctl", "ydotool"],
        default="auto",
        help="LED signaling backend (default: auto)",
    )
    parser.add_argument(
        "--race",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Query multiple Gemini models concurrently and take the fastest result (default: False)",
    )
    parser.add_argument(
        "--error-blink",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Emit 3 ultra-fast flashes (~0.35s) when API or answer parsing fails (default: True)",
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
            os.environ.get("GEMINI_MODEL_1", "gemini-3.5-flash-lite"),
            os.environ.get("GEMINI_MODEL_2", "gemini-3.5-flash"),
            os.environ.get("GEMINI_MODEL_3", "gemini-3-flash-preview"),
            os.environ.get("GEMINI_MODEL_4", "gemini-3.1-flash-lite"),
        ]
    args.gemini_models = gemini_models

    if args.watch:
        try:
            return watch_screenshots(args)
        except KeyboardInterrupt:
            ensure_caps_off(find_capslock_leds())
            print("\n[watch] stopped", file=sys.stderr)
            return 0

    try:
        image = args.image or newest_image(args.dir)
        return 0 if process_image(image, args) else 1
    except KeyboardInterrupt:
        ensure_caps_off(find_capslock_leds())
        print("\n[!] Dừng tiến trình bởi người dùng (Ctrl+C). Đã tắt đèn LED an toàn.", file=sys.stderr)
        return 0


def _sigint_handler(sig=None, frame=None):
    try:
        ensure_caps_off(find_capslock_leds())
    except Exception:
        pass
    print("\n[!] Đã nhận tín hiệu dừng (Ctrl+C). Đã tắt đèn LED an toàn.", file=sys.stderr)
    sys.exit(0)


signal.signal(signal.SIGINT, _sigint_handler)
signal.signal(signal.SIGTERM, _sigint_handler)


if __name__ == "__main__":
    raise SystemExit(main())
