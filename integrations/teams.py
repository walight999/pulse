"""Microsoft Teams integration — incoming webhook digest sender.

Teams uses Adaptive Cards via incoming webhooks (Office 365 Connector).
User creates a webhook in Teams: Channel -> Connectors -> Incoming Webhook.

Simpler API than Slack — JSON-only, no signature required.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Optional


def send_webhook(webhook_url: str, payload: dict, timeout: int = 8) -> dict:
    req = urllib.request.Request(
        webhook_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return {"ok": resp.status < 300, "status": resp.status}
    except urllib.error.HTTPError as e:
        return {"ok": False, "status": e.code, "error": str(e)}
    except Exception as e:
        return {"ok": False, "status": 0, "error": str(e)}


def adaptive_card(title: str, body_text: str,
                   facts: Optional[list[tuple[str, str]]] = None,
                   action_url: Optional[str] = None) -> dict:
    """Build an Adaptive Card payload."""
    body = [
        {"type": "TextBlock", "size": "Large", "weight": "Bolder", "text": title},
        {"type": "TextBlock", "wrap": True, "text": body_text},
    ]
    if facts:
        body.append({
            "type": "FactSet",
            "facts": [{"title": k, "value": v} for k, v in facts],
        })
    card = {
        "type": "AdaptiveCard",
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.4",
        "body": body,
    }
    if action_url:
        card["actions"] = [
            {"type": "Action.OpenUrl", "title": "Open Pulse", "url": action_url},
        ]
    return {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": card,
            },
        ],
    }


def format_daily_digest(date_iso: str, token_cost_usd: float, msgs: int,
                          symbol: str = "$") -> dict:
    return adaptive_card(
        title=f"Pulse — {date_iso}",
        body_text="Your AI day at a glance",
        facts=[
            ("AI spend", f"{symbol}{token_cost_usd:,.2f}"),
            ("Messages", f"{msgs:,}"),
        ],
        action_url="https://pulse.app",
    )


def format_spike_alert(today_cost: float, avg_cost: float, multiplier: float,
                        symbol: str = "$") -> dict:
    return adaptive_card(
        title="AI spend spike detected",
        body_text=(
            f"Today's {symbol}{today_cost:,.2f} is {multiplier:.1f}x your "
            f"recent average of {symbol}{avg_cost:,.2f}."
        ),
        action_url="https://pulse.app",
    )
