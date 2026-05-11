"""v0.dev (Vercel) usage parser — stub.

v0 Pro/Team are flat-rate subs. Per-message usage is rate-limited rather
than billed per-token, so we track subscription cost only.
"""
from __future__ import annotations

FLAT_PRICING = {
    "v0-free":   {"monthly_usd": 0.0,  "messages_per_month": 200},
    "v0-pro":    {"monthly_usd": 20.0, "messages_per_month": 1000},
    "v0-team":   {"monthly_usd": 30.0, "messages_per_month": 4000},
    "v0-enterprise": {"monthly_usd": 50.0, "messages_per_month": 50000},
}


def sync_from_gmail_invoice(receipts: list[dict]) -> list[dict]:
    raise NotImplementedError("Use providers.gmail_usage_parser instead")
