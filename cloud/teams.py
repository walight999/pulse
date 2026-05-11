"""Team tier — shared dashboard with per-user attribution.

Schema (server-side, via Supabase):
- teams (id, name, owner_id, plan, created_at)
- team_members (team_id, user_id, role: 'admin'|'member'|'viewer', joined_at)
- team_invites (id, team_id, email, code, expires_at, used_by)

The team's aggregated token_usage view is computed server-side, never
combining encrypted user blobs. Only opted-in metrics (cost, msgs,
project) flow into the team view.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass
class Team:
    id: str
    name: str
    owner_id: str
    plan: str       # 'team' | 'enterprise'
    seat_count: int


@dataclass
class TeamMember:
    user_id: str
    display_name: str
    role: str       # 'admin' | 'member' | 'viewer'
    joined_at: str


def create_team(name: str) -> dict:
    """Owner creates a team (Stripe seat purchase happens separately)."""
    from cloud import auth
    session = auth.current_session()
    if not session:
        return {"ok": False, "error": "not_signed_in"}
    client = auth._client()
    if not client:
        return {"ok": False, "error": "cloud_not_configured"}
    try:
        resp = client.table("teams").insert({
            "name": name,
            "owner_id": session.account_id,
            "plan": "team",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }).execute()
        team_id = resp.data[0]["id"]
        # Owner is auto-admin
        client.table("team_members").insert({
            "team_id": team_id,
            "user_id": session.account_id,
            "role": "admin",
        }).execute()
        return {"ok": True, "team_id": team_id}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def invite_member(team_id: str, email: str, role: str = "member") -> dict:
    """Generate an invite code + email it to the user."""
    from cloud import auth
    from referrals import generate_code
    session = auth.current_session()
    if not session:
        return {"ok": False, "error": "not_signed_in"}
    client = auth._client()
    if not client:
        return {"ok": False, "error": "cloud_not_configured"}
    code = generate_code()
    try:
        client.table("team_invites").insert({
            "team_id": team_id,
            "email": email,
            "role": role,
            "code": code,
            "invited_by": session.account_id,
        }).execute()
        # Trigger transactional email via Supabase Edge Function
        return {"ok": True, "code": code}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def accept_invite(code: str) -> dict:
    from cloud import auth
    session = auth.current_session()
    if not session:
        return {"ok": False, "error": "not_signed_in"}
    client = auth._client()
    if not client:
        return {"ok": False, "error": "cloud_not_configured"}
    try:
        resp = client.rpc("pulse_accept_team_invite",
                          {"p_code": code, "p_user_id": session.account_id}).execute()
        return {"ok": True, "team_id": resp.data}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def list_my_teams() -> list[Team]:
    from cloud import auth
    session = auth.current_session()
    if not session:
        return []
    client = auth._client()
    if not client:
        return []
    try:
        resp = client.rpc("pulse_my_teams", {"p_user_id": session.account_id}).execute()
        return [Team(**r) for r in (resp.data or [])]
    except Exception:
        return []


def team_dashboard_data(team_id: str, window: str = "monthly") -> dict:
    """Aggregated team metrics — total spend, per-member breakdown, top projects."""
    client = _client_or_none()
    if not client:
        return {}
    try:
        resp = client.rpc(
            "pulse_team_dashboard",
            {"p_team_id": team_id, "p_window": window},
        ).execute()
        return resp.data or {}
    except Exception:
        return {}


def _client_or_none():
    from cloud import auth
    return auth._client() if auth.is_configured() else None
