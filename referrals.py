"""Referral code system — earn credits when friends sign up.

Local stub for now. When Phase 1 cloud ships, codes are validated server-side
and credits are tracked there.
"""
from __future__ import annotations

import json
import string
import secrets
from datetime import datetime, timezone
from pathlib import Path

from account import get_account_id

REFERRALS_PATH = Path(__file__).parent / "data" / "referrals.json"

# Code format: 8 uppercase alphanumeric (no confusables: 0/O, 1/I/L)
ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"
CODE_LEN = 8


def _new_code() -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(CODE_LEN))


def my_code() -> str:
    """Return this account's referral code, generating once if needed."""
    REFERRALS_PATH.parent.mkdir(parents=True, exist_ok=True)
    state = _load()
    if not state.get("my_code"):
        state["my_code"] = _new_code()
        state["my_account_id"] = get_account_id()
        state["created_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        _save(state)
    return state["my_code"]


def used_codes() -> list[dict]:
    """Codes the current user has redeemed (entered)."""
    return _load().get("used", [])


def redeem(code: str) -> dict:
    """Mark a code as used by this account. Local-only stub."""
    code = (code or "").strip().upper()
    if not code or len(code) != CODE_LEN:
        return {"ok": False, "error": "invalid_format"}
    if code == my_code():
        return {"ok": False, "error": "cannot_redeem_own_code"}
    state = _load()
    used = state.get("used", [])
    if any(u.get("code") == code for u in used):
        return {"ok": False, "error": "already_redeemed"}
    used.append({
        "code": code,
        "redeemed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    })
    state["used"] = used
    _save(state)
    return {"ok": True, "code": code,
            "note": "Stored locally. Will be validated when Pro/cloud ships."}


def _load() -> dict:
    if not REFERRALS_PATH.exists():
        return {}
    try:
        return json.loads(REFERRALS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save(state: dict) -> None:
    REFERRALS_PATH.parent.mkdir(parents=True, exist_ok=True)
    REFERRALS_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")


if __name__ == "__main__":
    print("My code:", my_code())
    print("Used:   ", used_codes())
