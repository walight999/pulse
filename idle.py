"""Idle detection for Windows — uses GetLastInputInfo."""
import ctypes
from ctypes import wintypes


class _LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", wintypes.UINT), ("dwTime", wintypes.DWORD)]


_user32 = ctypes.windll.user32
_kernel32 = ctypes.windll.kernel32


def idle_seconds() -> float:
    """Seconds since the last user input (mouse/keyboard) on Windows."""
    info = _LASTINPUTINFO()
    info.cbSize = ctypes.sizeof(info)
    if not _user32.GetLastInputInfo(ctypes.byref(info)):
        return 0.0
    millis_since = _kernel32.GetTickCount() - info.dwTime
    return millis_since / 1000.0


if __name__ == "__main__":
    print(f"idle: {idle_seconds():.1f} seconds")
