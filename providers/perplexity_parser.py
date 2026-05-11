"""Perplexity Pro / API usage parser — stub.

Perplexity Pro is flat-rate ($20/mo). The browser extension captures web
session counts (see `browser-ext/providers/perplexity.js`).

For paid API users (sonar models), the /usage endpoint returns per-day spend.
"""
from __future__ import annotations

from typing import Optional

PRICING = {
    # Perplexity sonar models (USD per million tokens)
    "sonar":          {"input": 1.0,  "output": 1.0},
    "sonar-pro":      {"input": 3.0,  "output": 15.0},
    "sonar-reasoning": {"input": 1.0, "output": 5.0},
    "sonar-deep-research": {"input": 2.0, "output": 8.0},
}

FLAT_PRICING = {
    "perplexity-pro": {"monthly_usd": 20.00},
}


def sync_from_api(api_key: str, since=None) -> list[dict]:
    raise NotImplementedError("Phase 2 — implement /v1/usage when Perplexity opens public API analytics")


def parse_from_browser_ext_buffer(events: list[dict]) -> list[dict]:
    """Convert browser-ext capture events into TokenUsageRow dicts."""
    rows = []
    for ev in events or []:
        if ev.get("provider") != "perplexity":
            continue
        ts = ev.get("timestamp")
        rows.append({
            "timestamp": ts,
            "provider": "perplexity",
            "model": ev.get("model", "perplexity-web"),
            "input_tokens": 0,
            "output_tokens": 1,
            "cache_read_tokens": 0,
            "cache_creation_tokens": 0,
            "cache_creation_5m_tokens": 0,
            "cache_creation_1h_tokens": 0,
            "cost_usd": 0.0,
            "project_tag": "perplexity-web",
            "session_id": None,
            "request_id": f"perplexity-web:{ts}",
            "source": "browser-ext",
        })
    return rows
