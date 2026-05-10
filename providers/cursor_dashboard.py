"""Cursor usage adapter — Phase 3 stub.

Cursor exposes per-user usage at https://cursor.com/api/dashboard/usage
behind a session cookie. User pastes their cookie value in Settings.
"""
from __future__ import annotations


def sync(session_cookie: str) -> dict:
    raise NotImplementedError(
        "Phase 3 — fetch /api/dashboard/usage with the cookie, "
        "parse fast-requests + slow-requests, normalize to token_usage schema"
    )
