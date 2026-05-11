"""Cloud auth — Supabase Auth client.

Magic-link signup + sign-in flow. JWT cached locally; refreshed transparently
when expired. No password stored on disk.

Requires SUPABASE_URL + SUPABASE_ANON_KEY env vars at runtime.

Falls back gracefully if `supabase-py` is not installed — UI offers
"Pulse Cloud requires installation: pip install supabase".
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

try:
    from supabase import create_client, Client
    _SUPABASE_AVAILABLE = True
except ImportError:
    _SUPABASE_AVAILABLE = False
    Client = None  # type: ignore


_SESSION_PATH = Path(__file__).parent.parent / "data" / "cloud_session.json"


@dataclass
class AuthSession:
    account_id: str        # server-side UUID
    email: str
    plan: str              # 'free' | 'pro' | 'team' | 'enterprise'
    pro_until: Optional[str]   # ISO timestamp; None if free
    jwt: str
    refresh_token: str
    expires_at: int        # unix seconds


def _client() -> Optional["Client"]:
    if not _SUPABASE_AVAILABLE:
        return None
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_ANON_KEY")
    if not (url and key):
        return None
    return create_client(url, key)


def _save_session(session: AuthSession) -> None:
    _SESSION_PATH.parent.mkdir(parents=True, exist_ok=True)
    _SESSION_PATH.write_text(json.dumps(asdict(session), indent=2), encoding="utf-8")


def _load_session() -> Optional[AuthSession]:
    if not _SESSION_PATH.exists():
        return None
    try:
        d = json.loads(_SESSION_PATH.read_text(encoding="utf-8"))
        return AuthSession(**d)
    except Exception:
        return None


def clear_session() -> None:
    if _SESSION_PATH.exists():
        _SESSION_PATH.unlink()


def is_configured() -> bool:
    """True if SUPABASE_URL + SUPABASE_ANON_KEY are set and supabase-py installed."""
    return _client() is not None


def signup_with_magic_link(email: str, pulse_account_id: str) -> dict:
    """Send a magic link to email. User clicks it → completes via callback."""
    client = _client()
    if not client:
        return {"ok": False, "error": "cloud_not_configured"}
    try:
        client.auth.sign_in_with_otp(
            {"email": email, "options": {"data": {"pulse_account_id": pulse_account_id}}}
        )
        return {"ok": True, "message": "Check your email for the sign-in link."}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def signin_with_magic_link(email: str) -> dict:
    """Same magic-link flow for returning users."""
    client = _client()
    if not client:
        return {"ok": False, "error": "cloud_not_configured"}
    try:
        client.auth.sign_in_with_otp({"email": email})
        return {"ok": True, "message": "Check your email for the sign-in link."}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def complete_magic_link(token_hash: str, type_: str = "magiclink") -> Optional[AuthSession]:
    """User opened the link → exchange the token for a session."""
    client = _client()
    if not client:
        return None
    try:
        resp = client.auth.verify_otp({"token_hash": token_hash, "type": type_})
        session = resp.session
        user = resp.user
        if not session:
            return None
        # Plan + pro_until come from user_metadata or a profiles table lookup
        plan = (user.user_metadata or {}).get("plan", "free")
        pro_until = (user.user_metadata or {}).get("pro_until")
        s = AuthSession(
            account_id=user.id,
            email=user.email or "",
            plan=plan,
            pro_until=pro_until,
            jwt=session.access_token,
            refresh_token=session.refresh_token,
            expires_at=int(time.time() + session.expires_in),
        )
        _save_session(s)
        return s
    except Exception:
        return None


def refresh(refresh_token: str) -> Optional[AuthSession]:
    client = _client()
    if not client:
        return None
    try:
        resp = client.auth.refresh_session(refresh_token)
        if not resp.session:
            return None
        cached = _load_session()
        if not cached:
            return None
        cached.jwt = resp.session.access_token
        cached.refresh_token = resp.session.refresh_token
        cached.expires_at = int(time.time() + resp.session.expires_in)
        _save_session(cached)
        return cached
    except Exception:
        return None


def signout() -> None:
    """Sign out locally + on the server if a session exists."""
    cached = _load_session()
    client = _client()
    if cached and client:
        try:
            client.auth.sign_out()
        except Exception:
            pass
    clear_session()


def current_session() -> Optional[AuthSession]:
    """Return current session, refreshing if expired. None if not signed in."""
    s = _load_session()
    if not s:
        return None
    if s.expires_at - 60 < time.time():
        return refresh(s.refresh_token)
    return s
