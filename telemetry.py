"""Opt-in anonymous telemetry — local-first.

Currently writes events to a local file only. When cloud is ready (Phase 1),
events with `opted_in=True` will be batched + sent to the analytics endpoint.

Privacy promise: no personal data, no email, no DB content. Just feature names
+ counts + the anonymous account UUID.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from db import get_setting

EVENTS_PATH = Path(__file__).parent / "data" / "telemetry.jsonl"


def is_opted_in() -> bool:
    return get_setting("telemetry_opt_in", "0") == "1"


def track(event: str, props: dict[str, Any] | None = None) -> None:
    """Log an event. Silent no-op if user has not opted in."""
    if not is_opted_in():
        return
    EVENTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "event": event,
        "props": props or {},
    }
    try:
        with open(EVENTS_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass


def all_events(limit: int = 100) -> list[dict]:
    if not EVENTS_PATH.exists():
        return []
    out = []
    try:
        with open(EVENTS_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()[-limit:]
        for line in lines:
            try:
                out.append(json.loads(line))
            except Exception:
                continue
    except Exception:
        pass
    return out
