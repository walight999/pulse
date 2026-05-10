"""Background tracker — logs foreground app + periodic system snapshots."""
import time
import ctypes
from ctypes import wintypes
from datetime import datetime
from pathlib import Path

import psutil

from db import init_db, get_setting
from idle import idle_seconds

POLL_INTERVAL = 5
SNAPSHOT_INTERVAL = 300
IDLE_THRESHOLD_SEC = 120  # don't count foreground time after 2 min of no input
LOG_PATH = Path(__file__).parent / "logs" / "tracker.log"

user32 = ctypes.windll.user32


def log(msg: str) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    line = f"[{datetime.now().isoformat(timespec='seconds')}] {msg}\n"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line)


def get_foreground_app():
    hwnd = user32.GetForegroundWindow()
    if not hwnd:
        return None, None

    length = user32.GetWindowTextLengthW(hwnd)
    title_buf = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, title_buf, length + 1)
    title = title_buf.value

    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))

    try:
        proc = psutil.Process(pid.value)
        return proc.name(), title
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None, title


def system_snapshot():
    rows = []
    for proc in psutil.process_iter(["name", "memory_info", "cpu_percent"]):
        try:
            info = proc.info
            mem = info.get("memory_info")
            mem_mb = (mem.rss / 1024 / 1024) if mem else 0
            if mem_mb < 50:
                continue
            rows.append(
                (info["name"], info.get("cpu_percent") or 0, round(mem_mb, 1))
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return rows


def main():
    conn = init_db()
    cursor = conn.cursor()

    current_app = None
    current_id = None
    current_started = None
    last_snapshot = 0.0
    last_setting_check = 0.0
    idle_threshold = IDLE_THRESHOLD_SEC

    log(f"Tracker started")
    print(f"Tracker started — logging to {LOG_PATH.parent / 'tracker.log'}")

    while True:
        try:
            now_iso = datetime.now().isoformat(timespec="seconds")

            # Refresh idle_threshold from settings every 60s (no restart needed)
            if time.time() - last_setting_check > 60:
                raw = get_setting("idle_threshold_sec", str(IDLE_THRESHOLD_SEC))
                try:
                    idle_threshold = max(30, int(raw))
                except (ValueError, TypeError):
                    idle_threshold = IDLE_THRESHOLD_SEC
                last_setting_check = time.time()

            # Idle detection — pause foreground tracking when user inactive
            user_idle = idle_seconds() > idle_threshold
            app, title = (None, None) if user_idle else get_foreground_app()

            if app and app != current_app:
                if current_id is not None:
                    started_dt = datetime.fromisoformat(current_started)
                    duration = max(0, int((datetime.now() - started_dt).total_seconds()))
                    cursor.execute(
                        "UPDATE app_activity SET ended_at = ?, duration_seconds = ? WHERE id = ?",
                        (now_iso, duration, current_id),
                    )

                cursor.execute(
                    "INSERT INTO app_activity (started_at, process_name, window_title) VALUES (?, ?, ?)",
                    (now_iso, app, title),
                )
                current_id = cursor.lastrowid
                current_app = app
                current_started = now_iso
                conn.commit()

            if time.time() - last_snapshot > SNAPSHOT_INTERVAL:
                rows = system_snapshot()
                cursor.executemany(
                    "INSERT INTO system_snapshots (timestamp, process_name, cpu_pct, memory_mb) VALUES (?, ?, ?, ?)",
                    [(now_iso, r[0], r[1], r[2]) for r in rows],
                )
                conn.commit()
                last_snapshot = time.time()
                log(f"Snapshot: {len(rows)} processes")

            time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            break
        except Exception as e:
            log(f"Error: {e}")
            time.sleep(POLL_INTERVAL)

    if current_id is not None:
        started_dt = datetime.fromisoformat(current_started)
        duration = max(0, int((datetime.now() - started_dt).total_seconds()))
        cursor.execute(
            "UPDATE app_activity SET ended_at = ?, duration_seconds = ? WHERE id = ?",
            (datetime.now().isoformat(timespec="seconds"), duration, current_id),
        )
        conn.commit()

    conn.close()
    log("Tracker stopped")


if __name__ == "__main__":
    main()
