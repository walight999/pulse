"""Life Tracker — system tray launcher.

Manages 3 things from a single tray icon:
  1. tracker.py subprocess (background data collection)
  2. streamlit dashboard subprocess
  3. on-click → opens dashboard in Edge --app mode (no browser chrome)
"""
import os
import sys
import socket
import subprocess
import threading
import time
import webbrowser
from pathlib import Path

import pystray
from PIL import Image, ImageDraw

PROJECT_DIR = Path(__file__).parent
PYTHON_EXE = sys.executable
PYTHONW_EXE = Path(sys.executable).parent / "pythonw.exe"
if not PYTHONW_EXE.exists():
    PYTHONW_EXE = Path(sys.executable)

DASHBOARD_PORT = 8501
DASHBOARD_URL = f"http://localhost:{DASHBOARD_PORT}"
LOCK_PORT = 8500  # bind here as a single-instance lock

EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

# Hide Windows console windows when spawning subprocesses
NO_WINDOW = 0x08000000  # subprocess.CREATE_NO_WINDOW

processes: dict[str, subprocess.Popen] = {}
_lock_socket: socket.socket | None = None

TOKEN_SYNC_INTERVAL_SEC = 6 * 60 * 60  # every 6 hours
TOKEN_SYNC_INITIAL_DELAY_SEC = 60      # let dashboard boot first


def background_token_sync_loop() -> None:
    """Periodically sync token usage from Claude Code logs (and Admin API if key set)."""
    time.sleep(TOKEN_SYNC_INITIAL_DELAY_SEC)
    while True:
        try:
            from sync_tokens import sync_all
            sync_all()
        except Exception:
            pass
        time.sleep(TOKEN_SYNC_INTERVAL_SEC)


def background_alerts_loop() -> None:
    """Run renewal/spike/dead-sub checks every 30 minutes."""
    time.sleep(180)  # let app boot
    while True:
        try:
            from alerts import run_all_checks
            run_all_checks()
        except Exception:
            pass
        time.sleep(30 * 60)


def background_backup_loop() -> None:
    """Auto-backup once a day."""
    time.sleep(120)
    while True:
        try:
            from backup import auto_backup_if_due
            auto_backup_if_due()
        except Exception:
            pass
        time.sleep(6 * 60 * 60)  # check every 6h


def background_maintenance_loop() -> None:
    """Weekly DB vacuum + daily log rotation. Keeps Pulse's footprint small."""
    import sqlite3
    from db import DB_PATH

    LOG_DIR = PROJECT_DIR / "logs"
    MAX_LOG_BYTES = 5 * 1024 * 1024   # 5 MB per file before rotation
    MAX_LOG_KEEP = 3                  # keep last 3 rotated copies

    last_vacuum = 0.0

    time.sleep(300)  # wait 5 min after boot
    while True:
        try:
            # ---- log rotation ----
            if LOG_DIR.exists():
                for log_file in LOG_DIR.glob("*.log"):
                    try:
                        if log_file.stat().st_size > MAX_LOG_BYTES:
                            # Shift existing rotations: .2 -> .3, .1 -> .2, .log -> .1
                            for i in range(MAX_LOG_KEEP, 0, -1):
                                src = log_file.with_suffix(f".log.{i}")
                                dst = log_file.with_suffix(f".log.{i+1}")
                                if src.exists():
                                    if i == MAX_LOG_KEEP:
                                        src.unlink()  # drop oldest
                                    else:
                                        src.rename(dst)
                            log_file.rename(log_file.with_suffix(".log.1"))
                    except OSError:
                        pass

            # ---- weekly DB vacuum ----
            if time.time() - last_vacuum > 7 * 24 * 60 * 60:
                try:
                    conn = sqlite3.connect(DB_PATH)
                    conn.execute("VACUUM")
                    conn.close()
                    last_vacuum = time.time()
                except Exception:
                    pass
        except Exception:
            pass
        time.sleep(24 * 60 * 60)  # daily cycle


def acquire_single_instance_lock() -> bool:
    """Bind a localhost port to act as a mutex. Returns False if another instance owns it."""
    global _lock_socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", LOCK_PORT))
        s.listen(1)
        _lock_socket = s
        return True
    except OSError:
        s.close()
        return False


def find_edge() -> str | None:
    for c in EDGE_PATHS:
        if os.path.exists(c):
            return c
    return None


def make_icon(size: int = 64) -> Image.Image:
    """Modern fluent-style icon — stacked subscription cards with check.

    Three offset rounded rects (purple → blue → green), front card has a
    bold white check. Reads as 'managed subscriptions, all good' at a glance.
    """
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Background — rounded square, deep slate
    pad = max(int(size * 0.06), 1)
    d.rounded_rectangle(
        (pad, pad, size - pad, size - pad),
        radius=int(size * 0.22),
        fill=(15, 23, 42, 255),
    )

    # Three offset cards (back → front)
    cw = size * 0.50
    ch = size * 0.30
    base_x = size * 0.22
    base_y = size * 0.36
    r = max(int(size * 0.06), 2)

    # Back card — purple, faded
    d.rounded_rectangle(
        (base_x + size * 0.10, base_y - size * 0.10,
         base_x + size * 0.10 + cw, base_y - size * 0.10 + ch),
        radius=r, fill=(168, 85, 247, 200),
    )
    # Middle card — blue
    d.rounded_rectangle(
        (base_x + size * 0.05, base_y - size * 0.05,
         base_x + size * 0.05 + cw, base_y - size * 0.05 + ch),
        radius=r, fill=(59, 130, 246, 230),
    )
    # Front card — emerald
    d.rounded_rectangle(
        (base_x, base_y, base_x + cw, base_y + ch),
        radius=r, fill=(34, 197, 94, 255),
    )

    # Bold check inside front card
    cx = base_x + cw / 2
    cy = base_y + ch / 2
    stroke = max(int(size * 0.07), 2)
    d.line(
        [
            (cx - cw * 0.22, cy + ch * 0.02),
            (cx - cw * 0.05, cy + ch * 0.22),
            (cx + cw * 0.26, cy - ch * 0.22),
        ],
        fill=(255, 255, 255, 255),
        width=stroke,
        joint="curve",
    )
    return img


def port_open(port: int, host: str = "127.0.0.1") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.4)
        return s.connect_ex((host, port)) == 0


def wait_for_port(port: int, timeout: float = 30.0) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if port_open(port):
            return True
        time.sleep(0.4)
    return False


def start_tracker() -> None:
    if "tracker" in processes and processes["tracker"].poll() is None:
        return
    p = subprocess.Popen(
        [str(PYTHONW_EXE), str(PROJECT_DIR / "tracker.py")],
        cwd=str(PROJECT_DIR),
        creationflags=NO_WINDOW,
    )
    processes["tracker"] = p


def start_dashboard() -> None:
    if "dashboard" in processes and processes["dashboard"].poll() is None:
        return
    p = subprocess.Popen(
        [
            str(PYTHON_EXE),
            "-m",
            "streamlit",
            "run",
            str(PROJECT_DIR / "dashboard.py"),
            "--server.headless",
            "true",
            "--server.port",
            str(DASHBOARD_PORT),
            "--browser.gatherUsageStats",
            "false",
        ],
        cwd=str(PROJECT_DIR),
        creationflags=NO_WINDOW,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    processes["dashboard"] = p


def open_window(icon=None, item=None) -> None:
    if not port_open(DASHBOARD_PORT):
        start_dashboard()
        if not wait_for_port(DASHBOARD_PORT, timeout=30):
            try:
                if icon:
                    icon.notify("Dashboard failed to start", "Life Tracker")
            except Exception:
                pass
            return

    edge = find_edge()
    if edge:
        subprocess.Popen(
            [
                edge,
                f"--app={DASHBOARD_URL}",
                "--window-size=1280,860",
                f"--user-data-dir={PROJECT_DIR / 'data' / 'edge_profile'}",
            ],
            creationflags=NO_WINDOW,
        )
    else:
        webbrowser.open(DASHBOARD_URL)


def open_in_browser(icon=None, item=None) -> None:
    if not port_open(DASHBOARD_PORT):
        start_dashboard()
        wait_for_port(DASHBOARD_PORT, timeout=30)
    webbrowser.open(DASHBOARD_URL)


def restart_services(icon=None, item=None) -> None:
    for name in ("dashboard", "tracker"):
        p = processes.get(name)
        if p and p.poll() is None:
            try:
                p.terminate()
                p.wait(timeout=5)
            except Exception:
                try:
                    p.kill()
                except Exception:
                    pass
        processes.pop(name, None)
    start_tracker()
    start_dashboard()
    if icon:
        try:
            icon.notify("Tracker + dashboard restarted", "Life Tracker")
        except Exception:
            pass


def quit_app(icon, item) -> None:
    for p in processes.values():
        try:
            p.terminate()
        except Exception:
            pass
    for p in processes.values():
        try:
            p.wait(timeout=4)
        except Exception:
            try:
                p.kill()
            except Exception:
                pass
    if _lock_socket:
        try:
            _lock_socket.close()
        except Exception:
            pass
    icon.stop()


def main() -> None:
    if not acquire_single_instance_lock():
        # Another instance is running — open its window instead
        open_window()
        return

    # Start background services
    start_tracker()
    threading.Thread(target=start_dashboard, daemon=True).start()
    threading.Thread(target=background_token_sync_loop, daemon=True).start()
    threading.Thread(target=background_alerts_loop, daemon=True).start()
    threading.Thread(target=background_backup_loop, daemon=True).start()
    threading.Thread(target=background_maintenance_loop, daemon=True).start()

    image = make_icon()
    menu = pystray.Menu(
        pystray.MenuItem("Show dashboard", open_window, default=True),
        pystray.MenuItem("Open in browser", open_in_browser),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Restart services", restart_services),
        pystray.MenuItem("Quit", quit_app),
    )
    icon = pystray.Icon("Pulse", image, "Pulse — money & time, in rhythm", menu)
    icon.run()


if __name__ == "__main__":
    main()
