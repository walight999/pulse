"""Subscription discovery — documents the Gmail-based discovery process.

This is NOT auto-runnable from the dashboard (Streamlit can't access Gmail MCP).
Instead, you re-run discovery by asking Claude in a chat:

    "Scan my Gmail for new subscriptions and update life-tracker"

Claude will use the Gmail MCP tool with the queries below, parse the results, and
call `bulk_import_subscriptions(...)` from this module.

The seed dict at the bottom captures everything that was discovered on the
initial scan (2026-05-10).
"""
from __future__ import annotations

import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

from db import get_conn, init_db


# Gmail queries used for discovery (re-run these via Gmail MCP):
DISCOVERY_QUERIES = [
    # 1. Explicit subscription emails
    'subject:(subscription OR renewal OR "auto-renew") newer_than:1y',
    # 2. Receipts and invoices (excluding shipping)
    'subject:(receipt OR invoice) newer_than:1y -subject:(order OR shipped OR delivery)',
    # 3. Payment confirmations
    'subject:("payment received" OR "thank you for your payment" OR "your payment") newer_than:1y',
    # 4. Trials (often turn into recurring)
    'subject:("trial" OR "free trial") newer_than:1y',
    # 5. Common payment processors
    'from:(stripe.com OR paddle.net OR paypal.com OR app.lemonsqueezy.com) newer_than:1y',
    # 6. Major SaaS providers (extend as needed)
    'from:(@anthropic.com OR @openai.com OR @cursor.com OR @github.com OR @vercel.com '
        'OR @notion.so OR @figma.com OR @slack.com OR @linear.app) newer_than:1y',
    'from:(@tradingview.com OR @suno.com OR @apify.com OR @make.com OR @zoom.us '
        'OR @canva.com OR @adobe.com OR @microsoft.com OR @netflix.com OR @spotify.com '
        'OR @youtube.com OR @apple.com) newer_than:1y',
    # 7. Google Play / Google One
    'from:(googleplay-noreply@google.com OR googleone-noreply@google.com OR googleone-updates-noreply@google.com) newer_than:1y',
    # 8. Thai e-tax / bank
    'subject:("ใบเสร็จ" OR "ใบกำกับภาษี" OR "ค่าบริการ") newer_than:1y',
]


def bulk_import_subscriptions(items: list[dict], replace_existing: bool = False) -> dict:
    """Insert/update discovered subscriptions.

    Each item should have at least: name, cost, currency, billing_cycle.
    Optional: next_billing_date (ISO), linked_process, notes, active (1/0).

    By default, won't overwrite a subscription with the same name. Pass
    replace_existing=True to deactivate the old row first then add the new one.
    """
    conn = init_db()
    added = 0
    skipped = 0
    updated = 0

    for it in items:
        name = it["name"]
        cur = conn.execute("SELECT id FROM subscriptions WHERE name = ? AND active = 1", (name,))
        existing = cur.fetchone()

        if existing and not replace_existing:
            skipped += 1
            continue

        if existing and replace_existing:
            conn.execute("UPDATE subscriptions SET active = 0 WHERE id = ?", (existing[0],))
            updated += 1

        conn.execute(
            """
            INSERT INTO subscriptions
              (name, cost, currency, billing_cycle, next_billing_date, linked_process, notes, active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                float(it["cost"]),
                it.get("currency", "USD"),
                it["billing_cycle"],
                it.get("next_billing_date"),
                it.get("linked_process"),
                it.get("notes"),
                int(it.get("active", 1)),
            ),
        )
        added += 1

    conn.commit()
    return {"added": added, "updated_replaced": updated, "skipped_existing": skipped}


def days_from_today(d_iso: str | None) -> int | None:
    if not d_iso:
        return None
    try:
        return (datetime.fromisoformat(d_iso).date() - date.today()).days
    except Exception:
        return None


# ============================================================
# Seed list — discovered from Gmail scan on 2026-05-10
# ============================================================
DISCOVERED_2026_05_10: list[dict] = [
    # --- Confirmed active recurring (verified amounts in receipts) ---
    {
        "name": "Anthropic Claude Max (20x)",
        "cost": 200.00,
        "currency": "USD",
        "billing_cycle": "monthly",
        "next_billing_date": "2026-06-04",
        "linked_process": "Claude.exe",
        "notes": "Receipt #2410-8672-4949 May 4, 2026. Paid $52.13 this cycle (plan upgrade credit). Base $200/mo.",
    },
    {
        "name": "Apify",
        "cost": 29.00,
        "currency": "USD",
        "billing_cycle": "monthly",
        "next_billing_date": "2026-06-04",
        "linked_process": None,
        "notes": "Invoice #202605041861 paid May 4, 2026. Personal account exciting_irritant.",
    },
    {
        "name": "CHART-IMG.COM Pro",
        "cost": 7.00,
        "currency": "USD",
        "billing_cycle": "monthly",
        "next_billing_date": "2026-06-05",
        "linked_process": None,
        "notes": "Receipt #2879-1496 May 5, 2026. Pro plan.",
    },
    {
        "name": "Suno Pro",
        "cost": 10.00,
        "currency": "USD",
        "billing_cycle": "monthly",
        "next_billing_date": "2026-06-06",
        "linked_process": None,
        "notes": "Last verified receipt Nov 6, 2025. CHECK if still active — no recent receipt found.",
    },

    # --- Just cancelled (will move to free plan soon) ---
    {
        "name": "Make.com Core (cancelled)",
        "cost": 10.59,
        "currency": "USD",
        "billing_cycle": "monthly",
        "next_billing_date": "2026-05-24",
        "linked_process": None,
        "notes": "CANCELLED May 7, 2026. Org GOLD NEWS moves to Free plan on 2026-05-24. 10000 ops/mo.",
        "active": 0,
    },

    # --- Status uncertain (need user confirmation) ---
    {
        "name": "TradingView (Yearly?)",
        "cost": 0.00,
        "currency": "USD",
        "billing_cycle": "yearly",
        "next_billing_date": "2027-04-14",
        "linked_process": None,
        "notes": "Receipt April 14, 2026 — amount not in plain-text body. UPDATE COST manually.",
    },
    {
        "name": "Zoom (past due?)",
        "cost": 171.09,
        "currency": "USD",
        "billing_cycle": "monthly",
        "next_billing_date": None,
        "linked_process": "Zoom.exe",
        "notes": "Invoice INV337826596 was 7 days past due Jan 22, 2026. Card expiring Apr 15. May be downgraded — verify in Zoom account.",
    },

    # --- Cancelled / expired (logged for history, marked inactive) ---
    {
        "name": "Google AI Pro / Google One 2TB (ended)",
        "cost": 19.99,
        "currency": "USD",
        "billing_cycle": "monthly",
        "next_billing_date": "2025-10-17",
        "linked_process": None,
        "notes": "Cancelled Oct 1, 2025. Plan ended Oct 17, 2025.",
        "active": 0,
    },
    {
        "name": "ChatGPT Plus (likely lapsed)",
        "cost": 20.00,
        "currency": "USD",
        "billing_cycle": "monthly",
        "next_billing_date": None,
        "linked_process": None,
        "notes": "Multiple 'payment failed' emails Aug 2025. Likely on Free now — verify in OpenAI account.",
        "active": 0,
    },
    {
        "name": "Perplexity Pro (cancelled)",
        "cost": 20.00,
        "currency": "USD",
        "billing_cycle": "monthly",
        "next_billing_date": None,
        "linked_process": None,
        "notes": "Explicitly cancelled Feb 2, 2026.",
        "active": 0,
    },

    # --- Pay-as-you-go (not really a subscription, but worth tracking) ---
    {
        "name": "OpenAI API (credit top-ups)",
        "cost": 5.35,
        "currency": "USD",
        "billing_cycle": "monthly",
        "next_billing_date": None,
        "linked_process": None,
        "notes": "Pay-as-you-go API credits. Last top-up May 10, 2026 ($5.35). Tracks as monthly avg — adjust if usage grows.",
    },
]


def run_initial_import() -> dict:
    """One-time import of the 2026-05-10 discovery batch."""
    return bulk_import_subscriptions(DISCOVERED_2026_05_10, replace_existing=False)


if __name__ == "__main__":
    print("=== Discovery queries (use these via Gmail MCP) ===")
    for i, q in enumerate(DISCOVERY_QUERIES, 1):
        print(f"  {i}. {q}")
    print()
    print("=== Importing initial discovered batch ===")
    result = run_initial_import()
    print(f"  Added:    {result['added']}")
    print(f"  Replaced: {result['updated_replaced']}")
    print(f"  Skipped:  {result['skipped_existing']} (already exists with same name)")
