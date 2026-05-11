"""Lovable usage parser — stub.

Lovable uses message-credit pricing. Plus/Pro/Business tiers, each with
a monthly credit allowance. Invoices come via Stripe → Gmail.
"""
from __future__ import annotations

FLAT_PRICING = {
    "lovable-free":     {"monthly_usd": 0.0,   "credits": 5},
    "lovable-plus":     {"monthly_usd": 20.0,  "credits": 100},
    "lovable-pro":      {"monthly_usd": 50.0,  "credits": 250},
    "lovable-business": {"monthly_usd": 200.0, "credits": 1500},
}


def sync_from_gmail_invoice(receipts: list[dict]) -> list[dict]:
    raise NotImplementedError("Use providers.gmail_usage_parser instead")
