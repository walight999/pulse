"""Cursor IDE usage parser — production implementation.

Cursor stores per-conversation state in a local SQLite DB (`state.vscdb`)
under its app-data directory. We read it (read-only), extract chat
session metadata, and compute approximate cost using public pricing.

Note: Cursor's schema changes between versions. We try several known keys
and fall back gracefully. Expect to maintain this when Cursor updates.
"""
from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator, Optional


CURSOR_DATA_DIRS = [
    Path.home() / "AppData" / "Roaming" / "Cursor",       # Windows
    Path.home() / "Library" / "Application Support" / "Cursor",  # macOS
    Path.home() / ".cursor",                                # legacy
    Path.home() / ".config" / "Cursor",                     # Linux
]


# Cursor uses GPT-4 / Claude / Sonnet for completions — pricing roughly Sonnet-equiv
# We attribute generically as "cursor-completion" since Cursor abstracts the model
PRICING_FALLBACK = {"input": 3.0, "output": 15.0}  # USD per million tokens (Sonnet-like)


def find_cursor_db() -> Optional[Path]:
    """Locate Cursor's local state DB across known OS paths."""
    for base in CURSOR_DATA_DIRS:
        if not base.exists():
            continue
        # Cursor stores under User/globalStorage/state.vscdb
        candidates = [
            base / "User" / "globalStorage" / "state.vscdb",
            base / "user" / "globalStorage" / "state.vscdb",
            base / "globalStorage" / "state.vscdb",
        ]
        for c in candidates:
            if c.exists():
                return c
    return None


def parse_cursor_db(db_path: Optional[Path] = None) -> Iterator[dict]:
    """Read Cursor's state DB and yield TokenUsageRow dicts.

    Looks at the `cursorDiskKV` table — Cursor's main per-key storage.
    Filters for chat-history keys and decodes session metadata.

    Args:
        db_path: Override path. If None, auto-detect.
    """
    db_path = db_path or find_cursor_db()
    if not db_path or not db_path.exists():
        return

    # Open read-only to avoid corrupting Cursor's live state
    uri = f"file:{db_path}?mode=ro"
    try:
        conn = sqlite3.connect(uri, uri=True, check_same_thread=False)
        conn.row_factory = sqlite3.Row
    except sqlite3.OperationalError:
        return

    try:
        # Cursor 2024+: cursorDiskKV table with key/value blobs
        cursor = conn.execute(
            "SELECT key, value FROM cursorDiskKV "
            "WHERE key LIKE 'composerData:%' OR key LIKE 'aichat-%' "
            "   OR key LIKE 'conversation-%' OR key LIKE 'cursorAgent:%'"
        )
        rows = cursor.fetchall()
    except sqlite3.OperationalError:
        # Schema changed — try alternate table
        try:
            cursor = conn.execute(
                "SELECT key, value FROM ItemTable WHERE key LIKE '%conversation%' OR key LIKE '%chat%'"
            )
            rows = cursor.fetchall()
        except sqlite3.OperationalError:
            conn.close()
            return
    conn.close()

    for row in rows:
        try:
            value = row["value"]
            if isinstance(value, bytes):
                value = value.decode("utf-8", errors="ignore")
            data = json.loads(value)
        except (ValueError, UnicodeDecodeError):
            continue

        # Cursor stores conversations with arrays of messages
        messages = data.get("messages") or data.get("conversation") or []
        if not isinstance(messages, list):
            continue

        for msg in messages:
            if not isinstance(msg, dict):
                continue
            role = msg.get("role") or msg.get("type")
            if role not in ("assistant", "completion", "agent"):
                continue

            text = msg.get("content") or msg.get("text") or ""
            if isinstance(text, list):
                text = "".join(t.get("text", "") if isinstance(t, dict) else str(t) for t in text)
            if not text:
                continue

            # Rough token approximation (1 token ≈ 4 chars)
            approx_tokens = max(len(text) // 4, 1)

            ts = msg.get("timestamp") or msg.get("createdAt") or msg.get("created_at")
            if isinstance(ts, (int, float)):
                ts_iso = datetime.fromtimestamp(ts / 1000 if ts > 1e12 else ts,
                                                  tz=timezone.utc).isoformat(timespec="seconds")
            elif isinstance(ts, str):
                ts_iso = ts
            else:
                ts_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")

            cost = (approx_tokens * PRICING_FALLBACK["output"]) / 1_000_000
            msg_id = msg.get("id") or msg.get("messageId")

            yield {
                "timestamp": ts_iso,
                "provider": "cursor",
                "model": msg.get("model") or "cursor-completion",
                "input_tokens": 0,
                "output_tokens": approx_tokens,
                "cache_read_tokens": 0,
                "cache_creation_tokens": 0,
                "cache_creation_5m_tokens": 0,
                "cache_creation_1h_tokens": 0,
                "cost_usd": cost,
                "project_tag": "cursor",
                "session_id": row["key"][:200],   # truncate long keys
                "request_id": f"cursor:{row['key']}:{msg_id or ts_iso}",
                "source": "cursor-local",
            }


def is_cursor_installed() -> bool:
    return find_cursor_db() is not None


def sync() -> list[dict]:
    """High-level: detect Cursor + parse all available chat history."""
    if not is_cursor_installed():
        return []
    return list(parse_cursor_db())
