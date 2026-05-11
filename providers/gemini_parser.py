"""Gemini / Google AI Studio usage parser — Phase 2.

Sources:
- Google AI Studio API key usage (REST: aistudio.google.com)
- Gemini app subscription (consumer) — derived from Gmail receipts via
  discover_subscriptions.py
- Vertex AI usage via gcloud billing export
"""
from __future__ import annotations

from datetime import datetime
from typing import Iterator

PRICING = {
    # Gemini 2.x pricing per million tokens
    "gemini-2.5-pro":       {"input": 1.25,  "output": 10.0,  "cache_read": 0.31},
    "gemini-2.5-flash":     {"input": 0.075, "output": 0.30,  "cache_read": 0.019},
    "gemini-2.0-flash":     {"input": 0.10,  "output": 0.40,  "cache_read": 0.025},
}


def sync_from_api(api_key: str, since: datetime | None = None) -> list[dict]:
    """Fetch usage from Google AI Studio."""
    raise NotImplementedError("Phase 2")
