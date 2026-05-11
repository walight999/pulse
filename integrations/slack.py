"""Slack integration — incoming webhook digest sender.

User pastes their Incoming Webhook URL in Settings -> Integrations.
Pulse posts a daily/weekly digest with spend totals + alerts.

Works for personal Slack workspaces (free webhook) and Team tier
deployments (admin sets workspace-wide webhook).
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from datetime import date
from typing import Optional


def send_webhook(webhook_url: str, payload: dict, timeout: int = 8) -> dict:
    """POST JSON to a Slack incoming webhook URL. Returns {ok, status}."""
    req = urllib.request.Request(
        webhook_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return {"ok": resp.status < 300, "status": resp.status, "body": body[:200]}
    except urllib.error.HTTPError as e:
        return {"ok": False, "status": e.code, "error": str(e)}
    except Exception as e:
        return {"ok": False, "status": 0, "error": str(e)}


def format_daily_digest(date_iso: str, token_cost_usd: float, msgs: int,
                          top_project: Optional[str], renewals_due: list[dict],
                          symbol: str = "$") -> dict:
    """Build a Slack Block Kit payload for the daily digest."""
    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": f"Pulse — {date_iso}", "emoji": False},
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*AI spend*\n{symbol}{token_cost_usd:,.2f}"},
                {"type": "mrkdwn", "text": f"*Messages*\n{msgs:,}"},
            ],
        },
    ]
    if top_project:
        blocks.append({
            "type": "context",
            "elements": [
                {"type": "mrkdwn", "text": f"Top project today: *{top_project}*"},
            ],
        })
    if renewals_due:
        renewal_lines = "\n".join(
            f"• *{r['name']}* — {symbol}{r['cost']:.2f} in {r['days_left']}d"
            for r in renewals_due[:5]
        )
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*Upcoming renewals*\n{renewal_lines}"},
        })
    blocks.append({
        "type": "context",
        "elements": [
            {"type": "mrkdwn", "text": "<https://pulse.app|Open Pulse dashboard>"},
        ],
    })
    return {"blocks": blocks}


def format_spike_alert(today_cost: float, avg_cost: float, multiplier: float,
                        symbol: str = "$") -> dict:
    """Block Kit payload for a cost-spike alert."""
    return {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"⚠️ *AI spend spike*\n"
                        f"Today: *{symbol}{today_cost:,.2f}* — "
                        f"that's *{multiplier:.1f}x* your average of "
                        f"{symbol}{avg_cost:,.2f}."
                    ),
                },
            },
        ],
    }


def format_renewal_reminder(name: str, days_left: int, cost: float,
                             cancel_url: Optional[str] = None,
                             symbol: str = "$") -> dict:
    """Block Kit payload for a renewal reminder."""
    text = (
        f"📅 *{name}* renews in *{days_left} day{'s' if days_left != 1 else ''}* "
        f"for {symbol}{cost:.2f}."
    )
    if cancel_url:
        text += f"\n<{cancel_url}|Cancel / manage subscription>"
    return {"blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": text}}]}
