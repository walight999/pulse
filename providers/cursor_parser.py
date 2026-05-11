"""Cursor IDE usage parser — Phase 2.

Cursor stores usage state in `~/.cursor/` and tracks per-model spend in
its internal SQLite DB. We read read-only and aggregate into TokenUsageRow.

Note: Cursor's data format changes between versions; expect to maintain
this parser regularly.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Iterator

CURSOR_DATA_DIRS = [
    Path.home() / ".cursor",
    Path.home() / "AppData" / "Roaming" / "Cursor",       # Windows
    Path.home() / "Library" / "Application Support" / "Cursor",  # macOS
]


def find_cursor_db() -> Path | None:
    for base in CURSOR_DATA_DIRS:
        if base.exists():
            for candidate in base.rglob("state.vscdb"):
                return candidate
    return None


def parse_cursor_usage(db_path: Path) -> Iterator[dict]:
    """Yield TokenUsageRow dicts from Cursor's local state DB."""
    raise NotImplementedError("Phase 2 — needs current Cursor schema reverse-engineered")
