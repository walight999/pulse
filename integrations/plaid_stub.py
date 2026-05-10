"""Plaid bank integration — Phase 4 stub.

US/CA/UK/EU bank-account auto-import of recurring charges.
For Thai users (no Plaid coverage): use bank-statement CSV import wizard
(separate module, simpler).
"""
from __future__ import annotations


def create_link_token(user_account_id: str) -> str:
    """Server-side: ask Plaid for a Link token to open the connect flow."""
    raise NotImplementedError("Phase 4 — `plaid.PlaidApi.link_token_create(...)`")


def exchange_public_token(public_token: str) -> str:
    """After user completes Plaid Link, exchange the public_token for an access_token."""
    raise NotImplementedError("Phase 4 — `plaid.PlaidApi.item_public_token_exchange(...)`")


def fetch_transactions(access_token: str, since: str) -> list[dict]:
    """Pull transactions for a linked account."""
    raise NotImplementedError("Phase 4 — `plaid.PlaidApi.transactions_get(...)`")


def detect_recurring(transactions: list[dict]) -> list[dict]:
    """Group + analyze transactions to identify recurring patterns.
    Returns candidate subscriptions for user approval."""
    # Algorithm sketch:
    # 1. Group by merchant_name (Plaid normalizes)
    # 2. For each merchant: compute deltas between consecutive charge dates
    # 3. Flag as recurring if deltas cluster around 28-31d / 89-93d / 360-372d
    #    AND at least 3 charges
    # 4. Suggest billing_cycle based on the cluster
    raise NotImplementedError("Phase 4 — pure algorithmic detection")
