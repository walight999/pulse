"""OpenAI / ChatGPT usage parser — production implementation.

Three signal sources for OpenAI usage:

1. **API key usage** — calls `/v1/usage` for paid API users. Requires API key
   in env `OPENAI_API_KEY` or Settings. Returns daily breakdown per model.

2. **ChatGPT Plus / Team subscription** — flat-rate, detected from Gmail
   receipts (handled by `discover_subscriptions.py`). Not parsed here.

3. **Manual export** — user exports ChatGPT conversation archive from
   Settings → Data Controls → Export. ZIP contains `conversations.json`.
   We extract metadata only (model, timestamp, ~tokens via char count).
"""
from __future__ import annotations

import json
import os
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable, Iterator, Optional
from urllib.parse import urlencode
import urllib.error
import urllib.request


# OpenAI pricing (USD per million tokens) — keep current with public pricing
PRICING = {
    # GPT-5 family
    "gpt-5":              {"input": 5.0,   "output": 15.0,  "cache_read": 0.50},
    "gpt-5-mini":         {"input": 0.50,  "output": 2.0,   "cache_read": 0.05},
    "gpt-5-nano":         {"input": 0.10,  "output": 0.40,  "cache_read": 0.01},
    # GPT-4o family (legacy but still used)
    "gpt-4o":             {"input": 2.50,  "output": 10.0,  "cache_read": 1.25},
    "gpt-4o-mini":        {"input": 0.15,  "output": 0.60,  "cache_read": 0.075},
    "gpt-4-turbo":        {"input": 10.0,  "output": 30.0,  "cache_read": 5.0},
    # o-series reasoning
    "o3":                 {"input": 15.0,  "output": 60.0,  "cache_read": 7.50},
    "o3-mini":            {"input": 1.10,  "output": 4.40,  "cache_read": 0.55},
    "o1":                 {"input": 15.0,  "output": 60.0,  "cache_read": 7.50},
    "o1-mini":            {"input": 3.0,   "output": 12.0,  "cache_read": 1.50},
}


# ────────────────── API key sync ──────────────────

USAGE_ENDPOINT = "https://api.openai.com/v1/usage"


def _fetch_usage_day(api_key: str, day: date) -> Optional[dict]:
    """Fetch a single day's usage from /v1/usage."""
    params = urlencode({"date": day.isoformat()})
    req = urllib.request.Request(
        f"{USAGE_ENDPOINT}?{params}",
        headers={
            "Authorization": f"Bearer {api_key}",
            "User-Agent": "pulse/1.0",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 429:
            # Rate limited; back off — caller should retry later
            return {"_rate_limited": True}
        return None
    except Exception:
        return None


def _compute_cost(model: str, prompt_tokens: int, completion_tokens: int,
                   cached_tokens: int = 0) -> float:
    """Apply current PRICING to token counts."""
    model_key = model.split(":")[0] if ":" in model else model
    # Match against known prefixes
    for known, rates in PRICING.items():
        if model_key.startswith(known):
            non_cached_in = max(prompt_tokens - cached_tokens, 0)
            cost = (
                (non_cached_in * rates["input"]
                 + completion_tokens * rates["output"]
                 + cached_tokens * rates["cache_read"]) / 1_000_000
            )
            return cost
    # Unknown model — fall back to gpt-4o-mini rates (cheapest plausible)
    rates = PRICING["gpt-4o-mini"]
    return (prompt_tokens * rates["input"] + completion_tokens * rates["output"]) / 1_000_000


def sync_from_api(api_key: str, since: Optional[datetime] = None,
                   on_progress=None) -> list[dict]:
    """Fetch usage from /v1/usage for the given API key.
    Returns list of TokenUsageRow dicts ready to insert into `token_usage`.

    Args:
        api_key: OpenAI API key starting with sk-...
        since: Earliest date to fetch (default: 30 days ago)
        on_progress: Optional callable(day, total_days) for progress UI

    Returns:
        List of dicts with keys matching `token_usage` table columns.
    """
    if not api_key or not api_key.startswith("sk-"):
        return []

    end_day = date.today()
    if since:
        start_day = since.date() if isinstance(since, datetime) else since
    else:
        start_day = end_day - timedelta(days=30)

    days = (end_day - start_day).days + 1
    rows: list[dict] = []

    for i in range(days):
        day = start_day + timedelta(days=i)
        if on_progress:
            on_progress(i + 1, days)
        data = _fetch_usage_day(api_key, day)
        if not data or data.get("_rate_limited"):
            continue

        # /v1/usage returns: {"data": [{"aggregation_timestamp": ..., "snapshot_id": "gpt-4o",
        #                              "n_requests": ..., "n_context_tokens_total": ...,
        #                              "n_generated_tokens_total": ..., ...}], ...}
        for entry in data.get("data", []):
            model = entry.get("snapshot_id") or entry.get("model", "gpt-unknown")
            prompt_toks = int(entry.get("n_context_tokens_total", 0) or 0)
            output_toks = int(entry.get("n_generated_tokens_total", 0) or 0)
            cached_toks = int(entry.get("n_cached_context_tokens_total", 0) or 0)
            n_requests = int(entry.get("n_requests", 0) or 0)

            if prompt_toks + output_toks == 0:
                continue

            cost = _compute_cost(model, prompt_toks, output_toks, cached_toks)
            ts = entry.get("aggregation_timestamp")
            if isinstance(ts, (int, float)):
                ts_iso = datetime.fromtimestamp(ts, tz=timezone.utc).isoformat(timespec="seconds")
            else:
                ts_iso = f"{day.isoformat()}T00:00:00+00:00"

            rows.append({
                "timestamp": ts_iso,
                "provider": "openai",
                "model": model,
                "input_tokens": prompt_toks,
                "output_tokens": output_toks,
                "cache_read_tokens": cached_toks,
                "cache_creation_tokens": 0,
                "cache_creation_5m_tokens": 0,
                "cache_creation_1h_tokens": 0,
                "cost_usd": cost,
                "project_tag": "openai-api",
                "session_id": None,
                "request_id": f"openai-api:{day.isoformat()}:{model}:{n_requests}",
                "source": "openai-api",
            })

    return rows


# ────────────────── Conversation export parser ──────────────────

def parse_export_archive(archive_path: Path) -> Iterator[dict]:
    """Yield TokenUsageRow dicts from a ChatGPT conversation export.

    User generates via: Settings → Data Controls → Export Data.
    Receives a ZIP via email, extracts to a folder containing:
        conversations.json   (the chat history)
        ...other files...

    We approximate token counts from character length / 4 (rough heuristic).
    """
    if archive_path.is_dir():
        json_path = archive_path / "conversations.json"
    elif archive_path.suffix.lower() == ".zip":
        import zipfile
        with zipfile.ZipFile(archive_path) as z:
            with z.open("conversations.json") as f:
                conversations = json.load(f)
        yield from _parse_conversations(conversations)
        return
    else:
        json_path = archive_path

    if not json_path.exists():
        return

    with open(json_path, encoding="utf-8") as f:
        conversations = json.load(f)
    yield from _parse_conversations(conversations)


def _parse_conversations(conversations: list) -> Iterator[dict]:
    """Convert OpenAI export JSON into TokenUsageRow dicts."""
    for conv in conversations or []:
        conv_id = conv.get("id") or conv.get("conversation_id")
        mapping = conv.get("mapping") or {}
        for node_id, node in mapping.items():
            msg = node.get("message")
            if not msg:
                continue
            author = (msg.get("author") or {}).get("role")
            if author != "assistant":
                continue
            content = msg.get("content") or {}
            parts = content.get("parts") or []
            text_chars = sum(len(p) if isinstance(p, str) else 0 for p in parts)
            if text_chars == 0:
                continue

            ts = msg.get("create_time")
            if isinstance(ts, (int, float)):
                ts_iso = datetime.fromtimestamp(ts, tz=timezone.utc).isoformat(timespec="seconds")
            else:
                ts_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")

            model = (msg.get("metadata") or {}).get("model_slug", "gpt-unknown")
            # Rough token approximation: 1 token ≈ 4 chars
            approx_tokens = max(text_chars // 4, 1)
            # No input/output split available from export — count as output
            cost = _compute_cost(model, prompt_tokens=0, completion_tokens=approx_tokens)

            yield {
                "timestamp": ts_iso,
                "provider": "openai",
                "model": model,
                "input_tokens": 0,
                "output_tokens": approx_tokens,
                "cache_read_tokens": 0,
                "cache_creation_tokens": 0,
                "cache_creation_5m_tokens": 0,
                "cache_creation_1h_tokens": 0,
                "cost_usd": cost,
                "project_tag": "chatgpt-export",
                "session_id": conv_id,
                "request_id": f"openai-export:{msg.get('id') or node_id}",
                "source": "openai-export",
            }


# ────────────────── Settings helpers ──────────────────

def get_api_key() -> Optional[str]:
    """Read API key from env first, then Settings (encrypted at rest TODO)."""
    if env := os.environ.get("OPENAI_API_KEY"):
        return env
    try:
        from db import get_setting
        return get_setting("openai_api_key", "") or None
    except Exception:
        return None


def is_configured() -> bool:
    return bool(get_api_key())
