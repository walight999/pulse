"""Gmail usage parser — captures cross-machine AI usage via invoice emails.

Problem: Pulse parses local `~/.claude/projects/*.jsonl` for Claude Code usage,
but the user might also use Claude on another machine, ChatGPT via API on a
server, Cursor on a laptop they don't track, etc. Those don't show up locally.

Solution: parse Gmail invoices that providers email monthly. Extract:
- Provider name (anthropic, openai, cursor, github, etc.)
- Period (which month)
- Total spend ($X.XX)
- Approximate token count if mentioned

Insert as synthetic `token_usage` rows with `source='gmail-invoice'`. These show
up alongside local data in the dashboard, tagged so the user can distinguish.

Requires Gmail MCP (same as `discover_subscriptions.py`).

Status: scaffold — full implementation lands in v1.1 (M+1).
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable, Optional


@dataclass
class ExternalUsageRow:
    """Synthetic token_usage row sourced from a Gmail invoice email."""
    provider: str               # 'anthropic' | 'openai' | 'cursor' | 'github-copilot' | etc.
    model: str                  # 'external-{provider}' if not parsable
    period_start: str           # ISO date — start of invoice period
    period_end: str             # ISO date — end of invoice period
    cost_usd: float
    approx_tokens: Optional[int] = None
    invoice_id: Optional[str] = None
    email_sender: Optional[str] = None
    raw_subject: Optional[str] = None


# ────────────────── Invoice pattern matchers ──────────────────

# Each pattern below matches a specific provider's invoice email format.
# Add new providers as we encounter them. Tested examples in docstrings.

_PATTERNS: dict[str, dict] = {
    "anthropic": {
        # Subject: "Your Anthropic API invoice — May 2026"
        # Body: "$127.50 in API usage for the period 2026-05-01 to 2026-05-31"
        "sender_contains": ["@anthropic.com", "billing@anthropic.com"],
        "subject_regex": re.compile(
            r"Anthropic.+invoice.+([A-Z][a-z]+) (\d{4})",
            re.IGNORECASE,
        ),
        "amount_regex": re.compile(
            r"\$([\d,]+\.\d{2}).+(?:API|usage|charges?)",
            re.IGNORECASE,
        ),
    },
    "openai": {
        # Subject: "Your monthly OpenAI invoice"
        # Body: "Total: $89.23 ... Period: May 1 - May 31, 2026"
        "sender_contains": ["@openai.com", "@invoice.stripe.com"],
        "subject_regex": re.compile(
            r"(?:OpenAI|ChatGPT).+(?:invoice|receipt|usage)",
            re.IGNORECASE,
        ),
        "amount_regex": re.compile(
            r"(?:Total|Amount|Subtotal)[\s:]+\$([\d,]+\.\d{2})",
            re.IGNORECASE,
        ),
    },
    "cursor": {
        # Subject: "Cursor — Monthly billing statement"
        "sender_contains": ["@cursor.com", "@cursor.so"],
        "subject_regex": re.compile(r"Cursor.+(?:invoice|billing|statement)", re.IGNORECASE),
        "amount_regex": re.compile(r"\$([\d,]+\.\d{2})", re.IGNORECASE),
    },
    "github-copilot": {
        # Subject: "GitHub Copilot — usage receipt"
        "sender_contains": ["@github.com", "noreply@github.com"],
        "subject_regex": re.compile(r"Copilot.+(?:usage|invoice|subscription)", re.IGNORECASE),
        "amount_regex": re.compile(r"\$([\d,]+\.\d{2})", re.IGNORECASE),
    },
    "gemini": {
        # Subject: "Google AI Studio — Billing notification"
        "sender_contains": ["@google.com", "billing-noreply@google.com"],
        "subject_regex": re.compile(r"(?:Gemini|AI Studio|Google AI).+billing", re.IGNORECASE),
        "amount_regex": re.compile(r"\$([\d,]+\.\d{2})", re.IGNORECASE),
    },
    "perplexity": {
        "sender_contains": ["@perplexity.ai", "billing@perplexity.ai"],
        "subject_regex": re.compile(r"Perplexity.+(?:invoice|receipt|billing)", re.IGNORECASE),
        "amount_regex": re.compile(r"\$([\d,]+\.\d{2})", re.IGNORECASE),
    },
}


def parse_invoice_email(sender: str, subject: str, body: str,
                         received_date: str) -> Optional[ExternalUsageRow]:
    """Try to match the email against known invoice patterns.
    Returns None if no provider matches."""
    sender_lower = (sender or "").lower()
    subject_lower = (subject or "").lower()

    for provider, pattern in _PATTERNS.items():
        sender_match = any(s in sender_lower for s in pattern["sender_contains"])
        subject_match = pattern["subject_regex"].search(subject) is not None
        if not (sender_match or subject_match):
            continue

        # Extract amount
        amount_match = pattern["amount_regex"].search(body)
        if not amount_match:
            continue
        try:
            cost = float(amount_match.group(1).replace(",", ""))
        except (ValueError, IndexError):
            continue
        if cost <= 0:
            continue

        # Period: use received_date as proxy if subject doesn't specify
        period_end = received_date[:10] if received_date else datetime.now(timezone.utc).date().isoformat()
        period_start = _back_one_month(period_end)

        return ExternalUsageRow(
            provider=provider,
            model=f"external-{provider}",
            period_start=period_start,
            period_end=period_end,
            cost_usd=cost,
            email_sender=sender,
            raw_subject=subject,
        )

    return None


def _back_one_month(iso_date: str) -> str:
    """Approximate first-of-the-period 30 days back from the given date."""
    try:
        d = datetime.fromisoformat(iso_date).date()
    except Exception:
        d = datetime.now(timezone.utc).date()
    if d.month == 1:
        return d.replace(year=d.year - 1, month=12, day=1).isoformat()
    return d.replace(month=d.month - 1, day=1).isoformat()


# ────────────────── Gmail MCP integration (high-level) ──────────────────

def discover_from_gmail(months_back: int = 6) -> list[ExternalUsageRow]:
    """Query Gmail via MCP for invoice emails in the last N months.
    Returns list of parsed ExternalUsageRow.

    NOT YET IMPLEMENTED — requires Gmail MCP wiring (Phase 2).

    Implementation plan:
    1. Use Gmail MCP `search_threads` with query:
       `from:(anthropic.com OR openai.com OR cursor.com OR github.com) after:YYYY/MM/DD`
    2. For each thread, fetch headers + body via `get_thread`
    3. Call `parse_invoice_email(sender, subject, body, received_date)`
    4. Filter out duplicates by `(provider, period_end, cost_usd)` triple
    5. Return list of parsed rows
    """
    raise NotImplementedError(
        "Gmail MCP integration lands in v1.1. Currently use discover_subscriptions.py "
        "for subscription detection only."
    )


def insert_external_usage(rows: list[ExternalUsageRow]) -> int:
    """Bulk-insert parsed rows into the `token_usage` table.
    Returns count inserted. Dedup'd via (provider, period_end, cost_usd) on a
    synthetic `request_id` field."""
    from db import get_conn
    conn = get_conn()
    n = 0
    for r in rows:
        # Synthetic request_id ensures dedup across re-syncs of the same invoice
        request_id = f"gmail-invoice:{r.provider}:{r.period_end}:{r.cost_usd:.2f}"
        try:
            conn.execute(
                "INSERT INTO token_usage "
                "(timestamp, provider, model, cost_usd, source, request_id, project_tag) "
                "VALUES (?, ?, ?, ?, 'gmail-invoice', ?, ?)",
                (
                    r.period_end + "T00:00:00",
                    r.provider,
                    r.model,
                    r.cost_usd,
                    request_id,
                    f"external-{r.provider}",
                ),
            )
            n += 1
        except Exception:
            # UNIQUE violation = already imported, skip silently
            continue
    conn.commit()
    return n


def is_external_usage_enabled() -> bool:
    """User toggle in Settings → Data → 'Include external AI usage from Gmail'."""
    from db import get_setting
    return get_setting("external_usage_gmail_enabled", "0") == "1"
