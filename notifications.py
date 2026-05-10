"""Windows toast notifications — zero external dependencies.

Uses winsdk if available (modern Win11 toast API), falls back to PowerShell
BurntToast-free approach via Win32 BalloonTip, finally writes to log only.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from datetime import datetime

LOG_PATH = Path(__file__).parent / "logs" / "notifications.log"


def _log(level: str, msg: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat(timespec='seconds')}] {level}: {msg}\n")


def _xml_escape(s: str) -> str:
    """Escape for inclusion in toast XML (which is wrapped in PS double-quoted heredoc)."""
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
         .replace("'", "&apos;")
         # PowerShell metachars in double-quoted strings
         .replace("`", "``")
         .replace("$", "`$")
    )


def _powershell_toast(title: str, body: str) -> bool:
    """Use Windows.UI.Notifications via PowerShell — no extra deps required."""
    safe_title = _xml_escape(title)
    safe_body = _xml_escape(body)
    ps = f"""
$AppId = 'Pulse.Dashboard'
$null = [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime]
$null = [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime]
$Template = @"
<toast><visual><binding template="ToastGeneric"><text>{safe_title}</text><text>{safe_body}</text></binding></visual></toast>
"@
$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml($Template)
$toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($AppId).Show($toast)
"""
    try:
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", ps],
            timeout=10, capture_output=True, text=True,
            creationflags=0x08000000,  # CREATE_NO_WINDOW
        )
        if proc.returncode == 0:
            return True
        _log("WARN", f"toast PS rc={proc.returncode}, stderr={proc.stderr[:200]}")
        return False
    except Exception as e:
        _log("ERROR", f"toast PS failed: {e}")
        return False


def toast(title: str, body: str) -> bool:
    """Send a Windows toast notification. Returns True on success.

    Always logs the message regardless of whether the toast itself displayed.
    """
    _log("INFO", f"{title} | {body}")
    return _powershell_toast(title, body)


if __name__ == "__main__":
    # quick test
    ok = toast("Life Tracker", "Test notification — if you see this, toasts work!")
    print(f"toast result: {ok}")
