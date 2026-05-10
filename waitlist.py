"""Waitlist — collect emails for Pro launch notifications.

Local-only for now (writes to data/waitlist.json). When Phase 1 ships,
the cloud sync agent will upload these to the server.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

WAITLIST_PATH = Path(__file__).parent / "data" / "waitlist.json"

EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")


def is_valid_email(email: str) -> bool:
    return bool(email and EMAIL_RE.match(email.strip()))


def signup(email: str, source: str = "in-app", interest: str = "pro") -> dict:
    """Add an email to the waitlist. Returns status dict."""
    email = (email or "").strip().lower()
    if not is_valid_email(email):
        return {"ok": False, "error": "invalid_email"}

    WAITLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    existing = list_signups()
    if any(s.get("email") == email for s in existing):
        return {"ok": False, "error": "already_signed_up"}

    entry = {
        "email": email,
        "source": source,
        "interest": interest,
        "signed_up_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    existing.append(entry)
    WAITLIST_PATH.write_text(json.dumps(existing, indent=2), encoding="utf-8")
    return {"ok": True, "entry": entry}


def list_signups() -> list[dict]:
    if not WAITLIST_PATH.exists():
        return []
    try:
        return json.loads(WAITLIST_PATH.read_text(encoding="utf-8"))
    except Exception:
        return []


def count() -> int:
    return len(list_signups())


def remove(email: str) -> bool:
    email = (email or "").strip().lower()
    items = [s for s in list_signups() if s.get("email") != email]
    WAITLIST_PATH.write_text(json.dumps(items, indent=2), encoding="utf-8")
    return True


if __name__ == "__main__":
    print(f"Signups: {count()}")
    for s in list_signups():
        print(f"  {s.get('email')} ({s.get('signed_up_at')[:10]})")
