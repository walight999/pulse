"""OpenAI / ChatGPT usage parser — Phase 2.

ChatGPT Plus / Team / Enterprise don't expose a public per-user usage API,
so we use multiple signals:

1. API key usage (paid API users) — calls /v1/usage with stored key
2. Browser-history scrape (chat.openai.com visits) — if user opts in
3. Subscription detection from Gmail (handled by discover_subscriptions.py)
4. Manual import — user exports their ChatGPT conversation archive (JSON)

This file ships parser stubs; UI hooks land in dashboard once Phase 2 begins.
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Iterator

# OpenAI pricing (USD per million tokens) — keep in sync with public pricing
PRICING = {
    # GPT-5 family
    "gpt-5":              {"input": 5.0,   "output": 15.0,  "cache_read": 0.50},
    "gpt-5-mini":         {"input": 0.50,  "output": 2.0,   "cache_read": 0.05},
    "gpt-5-nano":         {"input": 0.10,  "output": 0.40,  "cache_read": 0.01},
    # GPT-4o family (legacy)
    "gpt-4o":             {"input": 2.50,  "output": 10.0,  "cache_read": 1.25},
    "gpt-4o-mini":        {"input": 0.15,  "output": 0.60,  "cache_read": 0.075},
    # o3 reasoning
    "o3":                 {"input": 15.0,  "output": 60.0,  "cache_read": 7.50},
    "o3-mini":            {"input": 1.10,  "output": 4.40,  "cache_read": 0.55},
}


def parse_export_archive(archive_path: Path) -> Iterator[dict]:
    """Yield TokenUsageRow dicts from a ChatGPT conversation export JSON file.
    User exports via Settings -> Data Controls -> Export Data."""
    raise NotImplementedError("Implement when Phase 2 begins")


def sync_from_api(api_key: str, since: datetime | None = None) -> list[dict]:
    """Fetch usage from /v1/usage for users with an OpenAI API key configured."""
    raise NotImplementedError("Phase 2")
