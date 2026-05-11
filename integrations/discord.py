"""Discord integration — webhook digest sender.

Simplest of the three (Slack/Teams/Discord). Plain JSON POST.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Optional


def send_webhook(webhook_url: str, content: str,
                  embeds: Optional[list[dict]] = None, timeout: int = 8) -> dict:
    payload = {"content": content}
    if embeds:
        payload["embeds"] = embeds
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


def daily_digest_embed(date_iso: str, token_cost_usd: float, msgs: int,
                        symbol: str = "$") -> dict:
    return {
        "title": f"Pulse — {date_iso}",
        "color": 0x6366f1,
        "fields": [
            {"name": "AI spend",  "value": f"{symbol}{token_cost_usd:,.2f}", "inline": True},
            {"name": "Messages",  "value": f"{msgs:,}", "inline": True},
        ],
        "footer": {"text": "pulse.app"},
    }
