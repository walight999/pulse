"""Cross-platform compatibility shim — Windows / macOS / Linux.

Pulse was Windows-first (Win32 APIs for foreground window + idle detection).
This module abstracts platform-specific calls so the rest of the codebase
works unchanged on macOS and Linux.

Usage:
    from platform_compat import get_foreground_window, get_idle_seconds, send_toast
"""
from __future__ import annotations

import os
import platform
import subprocess
from typing import Optional


SYSTEM = platform.system()   # 'Windows' | 'Darwin' | 'Linux'
IS_WINDOWS = SYSTEM == "Windows"
IS_MACOS   = SYSTEM == "Darwin"
IS_LINUX   = SYSTEM == "Linux"


# ────────────────── Foreground app ──────────────────

def get_foreground_window() -> tuple[str, str]:
    """Returns (process_name, window_title). Empty strings if unavailable."""
    if IS_WINDOWS:
        return _foreground_windows()
    if IS_MACOS:
        return _foreground_macos()
    if IS_LINUX:
        return _foreground_linux()
    return ("", "")


def _foreground_windows() -> tuple[str, str]:
    try:
        import ctypes
        from ctypes import wintypes
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32
        hwnd = user32.GetForegroundWindow()
        if not hwnd:
            return ("", "")
        # Window title
        length = user32.GetWindowTextLengthW(hwnd)
        buf = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buf, length + 1)
        title = buf.value
        # Process name
        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        try:
            import psutil
            process = psutil.Process(pid.value)
            name = process.name()
        except Exception:
            name = ""
        return (name, title)
    except Exception:
        return ("", "")


def _foreground_macos() -> tuple[str, str]:
    """macOS: use osascript (AppleScript) to query frontmost app."""
    try:
        script = (
            'tell application "System Events" '
            'to get {name, title of front window} of (first process whose frontmost is true)'
        )
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=2,
        )
        if result.returncode == 0:
            parts = [p.strip() for p in result.stdout.strip().split(",")]
            name = parts[0] if parts else ""
            title = parts[1] if len(parts) > 1 else ""
            return (name, title)
    except Exception:
        pass
    return ("", "")


def _foreground_linux() -> tuple[str, str]:
    """Linux: try xdotool (X11) or hyprctl (Hyprland)."""
    # X11 via xdotool
    try:
        wid = subprocess.run(["xdotool", "getactivewindow"],
                               capture_output=True, text=True, timeout=1).stdout.strip()
        if wid:
            title = subprocess.run(["xdotool", "getwindowname", wid],
                                     capture_output=True, text=True, timeout=1).stdout.strip()
            pid = subprocess.run(["xdotool", "getwindowpid", wid],
                                   capture_output=True, text=True, timeout=1).stdout.strip()
            name = ""
            try:
                with open(f"/proc/{pid}/comm") as f:
                    name = f.read().strip()
            except Exception:
                pass
            return (name, title)
    except FileNotFoundError:
        pass
    return ("", "")


# ────────────────── Idle detection ──────────────────

def get_idle_seconds() -> int:
    """Seconds since last user input across keyboard + mouse."""
    if IS_WINDOWS:
        return _idle_windows()
    if IS_MACOS:
        return _idle_macos()
    if IS_LINUX:
        return _idle_linux()
    return 0


def _idle_windows() -> int:
    try:
        import ctypes
        from ctypes import wintypes
        class LASTINPUTINFO(ctypes.Structure):
            _fields_ = [("cbSize", wintypes.UINT), ("dwTime", wintypes.DWORD)]
        lii = LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(lii)
        ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        return int(millis / 1000)
    except Exception:
        return 0


def _idle_macos() -> int:
    """macOS: parse `ioreg -c IOHIDSystem` for HIDIdleTime."""
    try:
        out = subprocess.run(
            ["ioreg", "-c", "IOHIDSystem"],
            capture_output=True, text=True, timeout=2,
        ).stdout
        for line in out.splitlines():
            if "HIDIdleTime" in line:
                ns = int(line.rsplit("=", 1)[1].strip())
                return ns // 1_000_000_000
    except Exception:
        pass
    return 0


def _idle_linux() -> int:
    """Linux: xprintidle gives ms; install with `apt install xprintidle`."""
    try:
        ms = subprocess.run(["xprintidle"], capture_output=True, text=True, timeout=1).stdout.strip()
        return int(ms) // 1000
    except Exception:
        return 0


# ────────────────── Notifications ──────────────────

def send_toast(title: str, body: str, app_id: Optional[str] = None) -> bool:
    """Show a desktop notification. Returns True if delivered."""
    if IS_WINDOWS:
        return _toast_windows(title, body, app_id)
    if IS_MACOS:
        return _toast_macos(title, body)
    if IS_LINUX:
        return _toast_linux(title, body)
    return False


def _toast_windows(title: str, body: str, app_id: Optional[str]) -> bool:
    """Existing notifications.py handles this — wrapper for compat."""
    try:
        from notifications import send_toast as _send
        _send(title, body)
        return True
    except Exception:
        return False


def _toast_macos(title: str, body: str) -> bool:
    """macOS: terminal-notifier or osascript fallback."""
    try:
        # Prefer terminal-notifier (better, requires brew install terminal-notifier)
        subprocess.run(["terminal-notifier", "-title", title, "-message", body],
                        timeout=3, check=False)
        return True
    except FileNotFoundError:
        pass
    try:
        # Fallback to osascript (always available)
        script = f'display notification "{body}" with title "{title}"'
        subprocess.run(["osascript", "-e", script], timeout=3, check=False)
        return True
    except Exception:
        return False


def _toast_linux(title: str, body: str) -> bool:
    try:
        subprocess.run(["notify-send", title, body], timeout=3, check=False)
        return True
    except FileNotFoundError:
        return False


# ────────────────── User-data paths ──────────────────

def app_data_dir() -> str:
    """Platform-appropriate persistent data directory for Pulse."""
    if IS_WINDOWS:
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    elif IS_MACOS:
        base = os.path.expanduser("~/Library/Application Support")
    else:
        base = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))
    return os.path.join(base, "Pulse")
