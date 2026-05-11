"""GitHub Copilot usage parser — Phase 2.

GitHub Copilot is a flat subscription ($10/mo individual, $19/mo business)
so most users care about value, not per-token cost. We derive:

- Subscription cost from Gmail receipts (discover_subscriptions.py)
- Approximate usage via GitHub API (suggestions accepted, lines of code)
- Cost-per-suggestion-accepted ROI metric

For API-billed Copilot (enterprise GraphQL), we can read the audit log.
"""
from __future__ import annotations

from datetime import datetime
from typing import Iterator

FLAT_PRICING = {
    "copilot-individual": {"monthly_usd": 10.00, "yearly_usd": 100.00},
    "copilot-business":   {"monthly_usd": 19.00, "yearly_usd": 228.00},
    "copilot-enterprise": {"monthly_usd": 39.00, "yearly_usd": 468.00},
}


def sync_from_github_api(token: str, since: datetime | None = None) -> list[dict]:
    """Fetch Copilot usage from GitHub's API (suggestions, acceptance rate)."""
    raise NotImplementedError("Phase 2")
