"""Cloud auth — Phase 1 stub.

Interface the desktop client uses for sign-up, sign-in, and JWT refresh.
Implementation calls Supabase Auth (or your chosen provider).
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AuthSession:
    account_id: str        # server-side UUID (different from local Pulse account_id)
    email: str
    plan: str              # 'free' | 'pro' | 'team'
    pro_until: str | None  # ISO timestamp; None if free
    jwt: str
    refresh_token: str


def signup(email: str, password: str, pulse_account_id: str) -> AuthSession:
    """Create a new cloud account and migrate the local pulse_account_id."""
    raise NotImplementedError("Phase 1 — implement against Supabase Auth")


def signin(email: str, password: str) -> AuthSession:
    raise NotImplementedError("Phase 1 — implement against Supabase Auth")


def refresh(refresh_token: str) -> AuthSession:
    raise NotImplementedError("Phase 1 — implement against Supabase Auth")


def signout(jwt: str) -> None:
    raise NotImplementedError("Phase 1 — implement against Supabase Auth")


def current_session() -> AuthSession | None:
    """Return current cached session, refreshing if expired. None if signed out."""
    return None  # local app starts with no session
