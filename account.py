"""Local Pulse account — anonymous UUID per install.

Used for:
  - Telemetry correlation (opt-in)
  - Cloud sync identification (when Phase 1 ships)
  - Referral codes
  - Migration to cloud auth without losing data
"""
from __future__ import annotations

import uuid
from datetime import datetime

from db import get_setting, set_setting, init_db


def get_account_id() -> str:
    """Return this install's anonymous UUID. Generated once on first call."""
    init_db()
    aid = get_setting("pulse_account_id", "")
    if not aid:
        aid = str(uuid.uuid4())
        set_setting("pulse_account_id", aid)
        set_setting("pulse_account_created_at",
                    datetime.utcnow().isoformat(timespec="seconds") + "Z")
    return aid


def get_account_age_days() -> int:
    raw = get_setting("pulse_account_created_at", "")
    if not raw:
        return 0
    try:
        created = datetime.fromisoformat(raw.rstrip("Z"))
        return (datetime.utcnow() - created).days
    except Exception:
        return 0


def short_id() -> str:
    """First 8 chars of account UUID — for display."""
    return get_account_id().split("-")[0]


if __name__ == "__main__":
    print("Account ID:", get_account_id())
    print("Short ID:  ", short_id())
    print("Age:       ", get_account_age_days(), "days")
