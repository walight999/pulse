"""Replit / Replit Agent usage parser — stub.

Replit Core ($15/mo) bundles AI usage. For overage or pure-API users,
Replit publishes invoice receipts via Stripe — parsed in
`providers/gmail_usage_parser.py`.
"""
from __future__ import annotations

FLAT_PRICING = {
    "replit-core":       {"monthly_usd": 15.0},
    "replit-teams":      {"monthly_usd": 33.0},
}


def sync_from_gmail_invoice(receipts: list[dict]) -> list[dict]:
    """Replit usage shows up only in Gmail invoices. Defer to gmail_usage_parser."""
    raise NotImplementedError("Use providers.gmail_usage_parser.parse_invoice_email instead")
