"""Leaderboard — friend rankings across 5 AI usage categories.

Privacy: opt-in only. Server only stores aggregate metrics, never raw token data.
Friend graph via referral codes (referrals.py).

5 categories:
1. Best ROI       — (API equivalent value) / (plan cost)
2. Longest streak — consecutive days with AI activity
3. Token wizard   — output tokens / input tokens ratio (efficient prompting)
4. Power day      — highest single-day useful spend
5. Project depth  — distinct project_tag count
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Literal

from db import get_conn


Category = Literal["best_roi", "longest_streak", "token_wizard", "power_day", "project_depth"]
Window = Literal["weekly", "monthly", "all_time"]


@dataclass
class LeaderboardEntry:
    user_id: str
    display_name: str
    metric_value: float
    metric_unit: str    # "x", "days", "ratio", "USD", "projects"
    rank: int


def compute_local_metrics(window: Window = "monthly") -> dict[Category, float]:
    """Compute the user's own metric values for each category from local data.
    These are what get uploaded to the leaderboard if user opts in."""
    conn = get_conn()
    now = datetime.now(timezone.utc)
    if window == "weekly":
        since = (now - timedelta(days=7)).isoformat()
    elif window == "monthly":
        since = (now - timedelta(days=30)).isoformat()
    else:
        since = "1970-01-01T00:00:00Z"

    # 1. Best ROI — needs plan_monthly_usd from settings
    from db import get_setting
    plan_monthly = float(get_setting("plan_monthly_usd", "200") or 200)
    days_in_window = {"weekly": 7, "monthly": 30, "all_time": 365}[window]
    plan_cost = plan_monthly * (days_in_window / 30.0)
    api_cost = float(conn.execute(
        "SELECT COALESCE(SUM(cost_usd), 0) FROM token_usage WHERE timestamp >= ?",
        (since,),
    ).fetchone()[0] or 0)
    roi = api_cost / max(plan_cost, 0.01) if plan_cost > 0 else 0

    # 2. Longest streak — consecutive days with at least 1 message
    streak = _compute_streak(conn)

    # 3. Token wizard — output/input ratio
    tok_row = conn.execute(
        "SELECT COALESCE(SUM(input_tokens), 0) AS i, COALESCE(SUM(output_tokens), 0) AS o "
        "FROM token_usage WHERE timestamp >= ?",
        (since,),
    ).fetchone()
    wizard_ratio = (tok_row["o"] or 0) / max(tok_row["i"] or 1, 1)

    # 4. Power day — max single-day cost
    pd_row = conn.execute(
        "SELECT MAX(daily) FROM (SELECT DATE(timestamp) AS d, SUM(cost_usd) AS daily "
        "FROM token_usage WHERE timestamp >= ? GROUP BY d)",
        (since,),
    ).fetchone()
    power_day = float(pd_row[0] or 0)

    # 5. Project depth — distinct project_tag count
    pd_count = conn.execute(
        "SELECT COUNT(DISTINCT project_tag) FROM token_usage "
        "WHERE timestamp >= ? AND project_tag IS NOT NULL",
        (since,),
    ).fetchone()[0]

    return {
        "best_roi": roi,
        "longest_streak": float(streak),
        "token_wizard": wizard_ratio,
        "power_day": power_day,
        "project_depth": float(pd_count or 0),
    }


def _compute_streak(conn) -> int:
    days_with_data = [
        r[0] for r in conn.execute(
            "SELECT DISTINCT DATE(timestamp) FROM token_usage ORDER BY 1 DESC LIMIT 365"
        ).fetchall()
    ]
    if not days_with_data:
        return 0
    today = datetime.now(timezone.utc).date()
    streak = 0
    cursor = today
    for d in days_with_data:
        target = datetime.fromisoformat(d).date()
        if target == cursor or target == cursor - timedelta(days=1):
            streak += 1
            cursor = target - timedelta(days=1)
        else:
            break
    return streak


def upload_my_rankings(window: Window = "monthly") -> dict:
    """Push the user's current metrics to the leaderboard table (opt-in only)."""
    from cloud import auth
    from db import get_setting
    if get_setting("leaderboard_optin", "0") != "1":
        return {"ok": False, "error": "leaderboard_not_opted_in"}
    session = auth.current_session()
    if not session:
        return {"ok": False, "error": "not_signed_in"}
    client = auth._client()
    if not client:
        return {"ok": False, "error": "cloud_not_configured"}
    metrics = compute_local_metrics(window)
    visibility = get_setting("leaderboard_visibility", "friends")
    display_name = get_setting("leaderboard_display_name", session.email.split("@")[0])
    try:
        client.table("leaderboard_entries").upsert({
            "user_id": session.account_id,
            "display_name": display_name,
            "window": window,
            "visibility": visibility,
            "metrics": metrics,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }).execute()
        return {"ok": True, "metrics": metrics}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def fetch_rankings(category: Category, window: Window = "monthly",
                    scope: str = "friends") -> list[LeaderboardEntry]:
    """Fetch top 10 entries for a category, scoped to friends or public."""
    from cloud import auth
    session = auth.current_session()
    if not session:
        return []
    client = auth._client()
    if not client:
        return []
    try:
        resp = client.rpc(
            "pulse_leaderboard",
            {
                "p_user_id": session.account_id,
                "p_category": category,
                "p_window": window,
                "p_scope": scope,
                "p_limit": 10,
            },
        ).execute()
        return [
            LeaderboardEntry(
                user_id=r["user_id"],
                display_name=r["display_name"],
                metric_value=float(r["value"]),
                metric_unit=r["unit"],
                rank=int(r["rank"]),
            )
            for r in (resp.data or [])
        ]
    except Exception:
        return []
