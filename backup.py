"""SQLite backup — uses backup API for live, consistent snapshots."""
from __future__ import annotations

import gzip
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

from db import DB_PATH, get_conn, init_db

BACKUPS_DIR = Path(__file__).parent / "backups"
KEEP_LAST = 7


def backup_now(label: str = "manual") -> Path:
    """Create a gzipped SQLite snapshot. Returns the backup file path."""
    init_db()  # ensure schema/migrations applied
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"tracker_{ts}_{label}.db"
    raw_path = BACKUPS_DIR / name
    gz_path = BACKUPS_DIR / (name + ".gz")

    # Use sqlite3 backup API for a safe snapshot even while DB is in use
    src = sqlite3.connect(DB_PATH)
    dst = sqlite3.connect(raw_path)
    with dst:
        src.backup(dst)
    dst.close()
    src.close()

    # gzip and remove the raw file
    with open(raw_path, "rb") as fin, gzip.open(gz_path, "wb", compresslevel=6) as fout:
        shutil.copyfileobj(fin, fout)
    raw_path.unlink()

    # Log to DB
    size = gz_path.stat().st_size
    conn = get_conn()
    conn.execute("INSERT INTO backup_log (file_path, size_bytes) VALUES (?, ?)",
                 (str(gz_path), size))
    conn.commit()

    _prune_old()
    return gz_path


def _prune_old() -> None:
    """Keep only the last N backups."""
    if not BACKUPS_DIR.exists():
        return
    files = sorted(BACKUPS_DIR.glob("tracker_*.db.gz"), key=lambda p: p.stat().st_mtime)
    while len(files) > KEEP_LAST:
        oldest = files.pop(0)
        try:
            oldest.unlink()
        except OSError:
            pass


def list_backups() -> list[dict]:
    if not BACKUPS_DIR.exists():
        return []
    out = []
    for p in sorted(BACKUPS_DIR.glob("tracker_*.db.gz"), reverse=True):
        st = p.stat()
        out.append({
            "name": p.name,
            "path": str(p),
            "size_kb": st.st_size / 1024,
            "created": datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
        })
    return out


def restore_from_backup(backup_path: Path) -> None:
    """Restore DB from a .db.gz snapshot. Uses sqlite3 backup API in reverse so it
    works while connections are open. Caller should advise user to refresh."""
    backup_path = Path(backup_path)
    if not backup_path.exists():
        raise FileNotFoundError(str(backup_path))

    # First make a safety backup of the current state
    backup_now("pre-restore")

    # Decompress to a temp file
    temp = DB_PATH.parent / "_restore_tmp.db"
    with gzip.open(backup_path, "rb") as fin, open(temp, "wb") as fout:
        shutil.copyfileobj(fin, fout)

    # Use sqlite3 backup API to overwrite the live DB
    src = sqlite3.connect(temp)
    dst = sqlite3.connect(DB_PATH)
    with dst:
        src.backup(dst)
    dst.close()
    src.close()
    try:
        temp.unlink()
    except OSError:
        pass


def auto_backup_if_due() -> Path | None:
    """Backup if the last one was >= 24h ago (or never). Used by app daemon."""
    files = sorted(BACKUPS_DIR.glob("tracker_*.db.gz"), key=lambda p: p.stat().st_mtime) if BACKUPS_DIR.exists() else []
    if files:
        last = files[-1]
        age_h = (datetime.now().timestamp() - last.stat().st_mtime) / 3600
        if age_h < 24:
            return None
    return backup_now("daily")


if __name__ == "__main__":
    p = backup_now("test")
    print(f"backup -> {p}")
    print(f"all backups: {list_backups()}")
