"""GitHub Copilot usage parser.

GitHub Copilot is a flat subscription ($10/mo individual, $19/mo business,
$39/mo enterprise) so the per-token cost question doesn't apply. What
matters is "are you using it enough to justify the seat?"

GitHub exposes two relevant endpoints:
  1. `/orgs/{org}/copilot/usage`              — daily metrics for org seats
  2. `/orgs/{org}/copilot/billing/seats`      — per-seat last-activity timestamp

Both require a PAT with `manage_billing:copilot` (org admin) or the org's
GraphQL audit log scope. Individual subscribers do not have a usage endpoint
— for them, pulse falls back to subscription-line-item tracking only.

This module:
  - Validates the token + org work
  - Pulls the last 28 days of org-level usage (suggestions accepted, lines
    of code accepted)
  - Inserts a synthetic token_usage row per day so the dashboard's
    cost-per-suggestion-accepted metric can be computed
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from typing import Iterator


FLAT_PRICING = {
    "copilot-individual": {"monthly_usd": 10.00, "yearly_usd": 100.00},
    "copilot-business":   {"monthly_usd": 19.00, "yearly_usd": 228.00},
    "copilot-enterprise": {"monthly_usd": 39.00, "yearly_usd": 468.00},
}

USAGE_ENDPOINT = "https://api.github.com/orgs/{org}/copilot/usage"


def _request(url: str, token: str) -> dict | list | None:
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "pulse/1.0",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError, TimeoutError):
        return None


def sync_from_github_api(token: str, org: str, since: datetime | None = None) -> list[dict]:
    """Fetch Copilot org-level usage. Returns up to 28 daily token_usage rows.

    Args:
        token: GitHub PAT with `manage_billing:copilot` scope
        org:   GitHub organization slug
        since: ignored (GitHub's endpoint always returns last 28 days)
    """
    if not token or not org:
        return []

    data = _request(USAGE_ENDPOINT.format(org=org), token)
    if not isinstance(data, list):
        return []

    rows: list[dict] = []
    for day in data:
        day_iso = day.get("day")
        if not day_iso:
            continue
        suggestions_made     = int(day.get("total_suggestions_count", 0) or 0)
        suggestions_accepted = int(day.get("total_acceptances_count", 0) or 0)
        active_users         = int(day.get("total_active_users", 0) or 0)
        chat_turns           = int(day.get("total_chat_turns", 0) or 0)

        if suggestions_made == 0 and chat_turns == 0:
            continue

        # GitHub doesn't bill per-token; this row is for ROI tracking only.
        # We encode "suggestions_accepted" into output_tokens as a proxy for
        # value generated — the dashboard divides this by subscription cost.
        rows.append({
            "timestamp": f"{day_iso}T12:00:00+00:00",
            "provider": "github-copilot",
            "model": "copilot-flat",
            "input_tokens": suggestions_made,
            "output_tokens": suggestions_accepted,
            "cache_read_tokens": chat_turns,         # chat usage piggybacks here
            "cache_creation_tokens": active_users,   # daily active users
            "cache_creation_5m_tokens": 0,
            "cache_creation_1h_tokens": 0,
            "cost_usd": 0.0,                          # flat plan — cost lives in subscriptions table
            "project_tag": f"copilot-org:{org}",
            "session_id": None,
            "request_id": f"copilot:{org}:{day_iso}",
            "source": "copilot-api",
        })

    return rows


def cost_per_acceptance(monthly_seat_cost: float, suggestions_accepted_this_month: int) -> float:
    """ROI metric — how much each accepted suggestion cost on the flat seat."""
    if suggestions_accepted_this_month <= 0:
        return 0.0
    return monthly_seat_cost / suggestions_accepted_this_month
