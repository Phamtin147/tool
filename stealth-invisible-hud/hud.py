#!/usr/bin/env python3
"""Stealth Invisible HUD - Screen-Capture Immune AI Assistant & Quiz Solver.
Developed by: Amtia / Phamtin147 (https://github.com/Phamtin147)
"""

from __future__ import annotations

import base64
import json
import os
import platform
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

CONFIG_ENV_PATHS = [
    Path(__file__).resolve().parent / ".config" / "gemini.env",
    Path.home() / ".config" / "gemini.env",
    Path(__file__).resolve().parent.parent / "quiz-led-solver" / ".config" / "gemini.env",
    Path.home() / ".env",
    Path(__file__).resolve().parent / ".env",
]

import ssl

DEFAULT_MODELS = [
    "gemini-flash-latest",
    "gemini-3.6-flash",
    "gemini-3.1-flash-lite",
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
]

SYSTEM_PROMPT = (
    "You are a multiple-choice exam & quiz assistant. "
    "Given an image of a question, extract the question and answer choices. "
    "Output in this exact format:\n"
    "ANSWER: <Option Letter(s), e.g., A or B or C,D>\n"
    "SUMMARY: <Concise explanation in Vietnamese/English, max 2 short sentences>\n"
    "CONFIDENCE: <Percentage, e.g., 95%>\n"
    "Do not add markdown formatting or extra greetings."
)


def load_env_file() -> None:
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
                break
            except Exception:
                pass


def get_api_key() -> str:
    load_env_file()
    return os.environ.get("GEMINI_API_KEY", "").strip()


def set_macos_capture_protection(enable: bool) -> bool:
    """Toggle screen-capture immunity on macOS Cocoa via NSWindow.setSharingType."""
    if platform.system() != "Darwin":
        return False
    try:
        import ctypes
        objc = ctypes.cdll.LoadLibrary("/usr/lib/libobjc.dylib")
        ctypes.cdll.LoadLibrary("/System/Library/Frameworks/AppKit.framework/AppKit")

        objc.objc_getClass.restype = ctypes.c_void_p
        objc.objc_getClass.argtypes = [ctypes.c_char_p]
        objc.sel_registerName.restype = ctypes.c_void_p
        objc.sel_registerName.argtypes = [ctypes.c_char_p]

        cls = objc.objc_getClass(b"NSApplication")
        shared_sel = objc.sel_registerName(b"sharedApplication")
        win_sel = objc.sel_registerName(b"windows")
        count_sel = objc.sel_registerName(b"count")
        get_win_sel = objc.sel_registerName(b"objectAtIndex:")
        set_share_sel = objc.sel_registerName(b"setSharingType:")

        objc.objc_msgSend.restype = ctypes.c_void_p
        objc.objc_msgSend.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        app = objc.objc_msgSend(cls, shared_sel)
        if not app:
            return False

        wins = objc.objc_msgSend(app, win_sel)
        if not wins:
            return False

        count = objc.objc_msgSend(wins, count_sel)
        # NSWindowSharingNone = 0, NSWindowSharingReadOnly = 1
        sharing_type = 0 if enable else 1

        objc.objc_msgSend.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulonglong]
        for i in range(count):
            w = objc.objc_msgSend(wins, get_win_sel, i)
            objc.objc_msgSend(w, set_share_sel, sharing_type)
        return True
    except Exception as e:
        print(f"[StealthHUD] Capture protection warning: {e}", file=sys.stderr)
        return False


def set_windows_capture_protection(hwnd: int, enable: bool) -> bool:
    if platform.system() != "Windows":
        return False
    try:
        import ctypes
        # WDA_EXCLUDEFROMCAPTURE = 0x00000011, WDA_NONE = 0x00000000
        affinity = 0x00000011 if enable else 0x00000000
        return bool(ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, affinity))
    except Exception:
        return False


def bring_app_to_front() -> None:
    if platform.system() == "Darwin":
        try:
            pid = os.getpid()
            subprocess.run(
                ["osascript", "-e", f'tell application "System Events" to set frontmost of first process whose unix id is {pid} to true'],
                capture_output=True,
                timeout=1
            )
        except Exception:
            pass


def query_gemini_vision(image_path: str, api_key: str, model_name: str = "gemini-2.5-flash") -> str:
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    ext = Path(image_path).suffix.lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": SYSTEM_PROMPT},
                    {
                        "inline_data": {
                            "mime_type": mime,
                            "data": img_b64,
                        }
                    },
                    {"text": "Solve the quiz question shown in this image accurately."}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": 300,
        }
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
    return "No answer received from Gemini."


class StealthHUDApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("🛡️ Stealth Invisible HUD")
        self.root.geometry("400x330+180+120")
        self.root.minsize(360, 300)
        self.root.configure(bg="#0f1117")

        # Keep on top
        self.root.attributes("-topmost", True)
        self.root.lift()

        # Opacity
        self.opacity = 0.95
        self.set_opacity(self.opacity)

        self.api_key = get_api_key()
        self.is_snapping = False
        self.is_hidden = False
        self.anti_capture_enabled = tk.BooleanVar(value=True)

        self.setup_ui()

        # Bring to front & enable protection after window is mapped
        self.root.after(200, bring_app_to_front)
        self.root.after(350, self.update_capture_protection)

        # Global Hotkeys within Tkinter
        self.root.bind("<Escape>", lambda e: self.toggle_hide())
        self.root.bind("<Control-s>", lambda e: self.trigger_snip())
        self.root.bind("<Command-s>", lambda e: self.trigger_snip())

    def set_opacity(self, val: float) -> None:
        try:
            self.root.attributes("-alpha", val)
        except Exception:
            pass

    def update_capture_protection(self) -> None:
        enabled = self.anti_capture_enabled.get()
        if platform.system() == "Darwin":
            ok = set_macos_capture_protection(enabled)
            status = "Bảo vệ tàng hình: BẬT" if (enabled and ok) else "Bảo vệ tàng hình: TẮT"
            self.lbl_stealth_status.config(
                text=f"🛡️ {status}",
                fg="#2ed573" if enabled else "#747d8c"
            )
        elif platform.system() == "Windows":
            ok = set_windows_capture_protection(self.root.winfo_id(), enabled)
            status = "Bảo vệ tàng hình: BẬT" if (enabled and ok) else "Bảo vệ tàng hình: TẮT"
            self.lbl_stealth_status.config(
                text=f"🛡️ {status}",
                fg="#2ed573" if enabled else "#747d8c"
            )
        else:
            self.lbl_stealth_status.config(text="🛡️ Chế độ tiêu chuẩn (Linux)", fg="#70a1ff")

    def toggle_hide(self) -> None:
        if self.is_hidden:
            self.root.deiconify()
            self.root.attributes("-topmost", True)
            self.root.lift()
            bring_app_to_front()
            self.is_hidden = False
        else:
            self.root.withdraw()
            self.is_hidden = True

    def setup_ui(self) -> None:
        # Header banner
        header = tk.Frame(self.root, bg="#1a1e29", padx=12, pady=8)
        header.pack(fill=tk.X)

        title_lbl = tk.Label(
            header,
            text="⚡ Stealth HUD Pro",
            bg="#1a1e29",
            fg="#38bdf8",
            font=("Helvetica", 12, "bold")
        )
        title_lbl.pack(side=tk.LEFT)

        self.lbl_stealth_status = tk.Label(
            header,
            text="🛡️ Tàng hình: Đang kích hoạt...",
            bg="#1a1e29",
            fg="#2ed573",
            font=("Helvetica", 9)
        )
        self.lbl_stealth_status.pack(side=tk.RIGHT)

        # Body container
        body = tk.Frame(self.root, bg="#0f1117", padx=12, pady=10)
        body.pack(fill=tk.BOTH, expand=True)

        # Answer Card
        self.card = tk.Frame(body, bg="#1a1f2c", bd=1, relief=tk.SOLID)
        self.card.pack(fill=tk.X, pady=(0, 10))

        self.ans_label = tk.Label(
            self.card,
            text="ĐÁP ÁN: SẴN SÀNG",
            bg="#1a1f2c",
            fg="#4ade80",
            font=("Helvetica", 15, "bold"),
            pady=6
        )
        self.ans_label.pack(fill=tk.X)

        self.summary_box = tk.Text(
            self.card,
            bg="#1a1f2c",
            fg="#cbd5e1",
            font=("Helvetica", 10),
            height=4,
            wrap=tk.WORD,
            bd=0,
            padx=10,
            pady=4
        )
        self.summary_box.insert(tk.END, "Bấm [✂️ Snip Question] để chọn vùng câu hỏi trên màn hình.\nCửa sổ HUD này được bảo vệ chống lộ khi share screen.")
        self.summary_box.config(state=tk.DISABLED)
        self.summary_box.pack(fill=tk.X)

        # Action Buttons
        btn_row = tk.Frame(body, bg="#0f1117")
        btn_row.pack(fill=tk.X, pady=(0, 10))

        self.btn_snip = tk.Button(
            btn_row,
            text="✂️ Snip Question (Cmd+S)",
            bg="#0284c7",
            fg="#ffffff",
            activebackground="#0369a1",
            activeforeground="#ffffff",
            font=("Helvetica", 10, "bold"),
            bd=0,
            pady=6,
            cursor="hand2",
            command=self.trigger_snip
        )
        self.btn_snip.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))

        btn_key = tk.Button(
            btn_row,
            text="🔑 API Key",
            bg="#334155",
            fg="#ffffff",
            font=("Helvetica", 9),
            bd=0,
            pady=6,
            padx=10,
            cursor="hand2",
            command=self.prompt_key
        )
        btn_key.pack(side=tk.RIGHT)

        # Options Row: Anti-Screen Capture Checkbox
        opt_row = tk.Frame(body, bg="#0f1117")
        opt_row.pack(fill=tk.X, pady=(0, 8))

        chk_anti = tk.Checkbutton(
            opt_row,
            text="Tàng hình trước Screen Share / Zoom / Meet",
            variable=self.anti_capture_enabled,
            command=self.update_capture_protection,
            bg="#0f1117",
            fg="#94a3b8",
            activebackground="#0f1117",
            activeforeground="#38bdf8",
            selectcolor="#1e293b",
            font=("Helvetica", 9)
        )
        chk_anti.pack(side=tk.LEFT)

        # Bottom Bar: Opacity & Status
        bottom_bar = tk.Frame(body, bg="#0f1117")
        bottom_bar.pack(fill=tk.X, side=tk.BOTTOM)

        lbl_op = tk.Label(bottom_bar, text="Độ mờ:", bg="#0f1117", fg="#64748b", font=("Helvetica", 8))
        lbl_op.pack(side=tk.LEFT)

        self.scale_op = tk.Scale(
            bottom_bar,
            from_=0.25,
            to=1.0,
            resolution=0.05,
            orient=tk.HORIZONTAL,
            showvalue=0,
            bg="#0f1117",
            fg="#38bdf8",
            highlightthickness=0,
            command=lambda val: self.set_opacity(float(val)),
            length=90
        )
        self.scale_op.set(self.opacity)
        self.scale_op.pack(side=tk.LEFT, padx=4)

        self.lbl_status = tk.Label(bottom_bar, text="ESC để ẩn nhanh", bg="#0f1117", fg="#64748b", font=("Helvetica", 8))
        self.lbl_status.pack(side=tk.RIGHT)

    def prompt_key(self) -> None:
        win = tk.Toplevel(self.root)
        win.title("Gemini API Key")
        win.geometry("340x130+220+180")
        win.configure(bg="#1a1e29")
        win.attributes("-topmost", True)

        lbl = tk.Label(win, text="Nhập Google Gemini API Key:", bg="#1a1e29", fg="#ffffff", font=("Helvetica", 10))
        lbl.pack(pady=(12, 6))

        entry = tk.Entry(win, width=32, show="*")
        entry.insert(0, self.api_key)
        entry.pack(pady=4)

        def save() -> None:
            self.api_key = entry.get().strip()
            os.environ["GEMINI_API_KEY"] = self.api_key
            env_file = Path(__file__).resolve().parent / ".config" / "gemini.env"
            env_file.parent.mkdir(parents=True, exist_ok=True)
            env_file.write_text(f"GEMINI_API_KEY={self.api_key}\n", encoding="utf-8")
            win.destroy()

        btn = tk.Button(win, text="Lưu Key", command=save, bg="#0ea5e9", fg="#ffffff", bd=0, padx=12, pady=4)
        btn.pack(pady=8)

    def trigger_snip(self) -> None:
        if self.is_snapping:
            return

        if not self.api_key:
            messagebox.showwarning("Thiếu API Key", "Vui lòng nhập Gemini API Key trước khi giải.")
            self.prompt_key()
            return

        self.is_snapping = True
        self.lbl_status.config(text="Đang chọn vùng...", fg="#facc15")
        threading.Thread(target=self._worker_snip, daemon=True).start()

    def _worker_snip(self) -> None:
        tmp_img = os.path.join(tempfile.gettempdir(), f"stealth_snip_{int(time.time())}.png")
        try:
            current_os = platform.system()
            if current_os == "Darwin":
                # screencapture with interactive region
                subprocess.run(["screencapture", "-i", tmp_img], check=True)
            elif current_os == "Linux":
                subprocess.run(["import", tmp_img], check=True)
            else:
                self.root.after(0, lambda: self.lbl_status.config(text="OS chưa hỗ trợ auto-snip", fg="#f87171"))
                return

            if not os.path.exists(tmp_img) or os.path.getsize(tmp_img) == 0:
                self.root.after(0, lambda: self.lbl_status.config(text="Đã hủy chọn", fg="#64748b"))
                return

            self.root.after(0, lambda: self.lbl_status.config(text="Gemini đang giải...", fg="#38bdf8"))

            res = ""
            used_model = "AI"
            for model in DEFAULT_MODELS:
                try:
                    res = query_gemini_vision(tmp_img, self.api_key, model)
                    if res:
                        used_model = model
                        break
                except Exception as err:
                    print(f"Model {model} failed: {err}")

            if not res:
                res = "Lỗi: Không nhận được phản hồi từ Gemini API."

            self.root.after(0, lambda: self.update_result(res, used_model))

        except Exception as e:
            self.root.after(0, lambda: self.lbl_status.config(text=f"Lỗi: {e}", fg="#f87171"))
        finally:
            self.is_snapping = False
            if os.path.exists(tmp_img):
                try:
                    os.remove(tmp_img)
                except Exception:
                    pass

    def update_result(self, raw_text: str, model_used: str = "AI") -> None:
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        ans = "ĐÁP ÁN: ?"
        for line in lines:
            if line.upper().startswith("ANSWER:") or line.upper().startswith("ĐÁP ÁN:"):
                ans = line
                break

        self.ans_label.config(text=ans)
        self.summary_box.config(state=tk.NORMAL)
        self.summary_box.delete("1.0", tk.END)
        self.summary_box.insert(tk.END, raw_text)
        self.summary_box.config(state=tk.DISABLED)
        self.lbl_status.config(text=f"✓ Đã giải xong ({model_used})", fg="#4ade80")


def main() -> None:
    root = tk.Tk()
    app = StealthHUDApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
