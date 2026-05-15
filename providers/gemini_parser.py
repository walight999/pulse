"""Gemini / Google AI Studio usage parser.

Honest status (2026-05-15):
- Google AI Studio does NOT expose a retrospective per-key usage endpoint
  (unlike OpenAI's /v1/usage or Anthropic's Admin API). The closest thing is
  Vertex AI's gcloud billing export, which requires a paid Google Cloud
  project — out of scope for individual users.
- This module:
    1. Validates the API key works (single test call to the models endpoint)
    2. Returns 0 historical rows because there's nothing retrospective to fetch
    3. Documents what to do instead: install the browser extension to capture
       Gemini sessions going forward
- For Vertex AI users with billing export, see future Phase 4 integration.

Pricing is kept current here so the browser-extension capture and any future
push-based ingestion can compute cost.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from datetime import datetime
from typing import Iterator


# USD per million tokens — keep current with https://ai.google.dev/pricing
PRICING = {
    "gemini-2.5-pro":       {"input": 1.25,  "output": 10.0,  "cache_read": 0.31},
    "gemini-2.5-flash":     {"input": 0.075, "output": 0.30,  "cache_read": 0.019},
    "gemini-2.0-flash":     {"input": 0.10,  "output": 0.40,  "cache_read": 0.025},
    "gemini-2.0-flash-lite": {"input": 0.075, "output": 0.30,  "cache_read": 0.019},
    "gemini-1.5-pro":       {"input": 1.25,  "output": 5.0,   "cache_read": 0.31},
    "gemini-1.5-flash":     {"input": 0.075, "output": 0.30,  "cache_read": 0.019},
}

VALIDATE_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models"


def validate_api_key(api_key: str) -> bool:
    """Single GET to the models endpoint to confirm the key is valid.
    Returns True if the API responds with a 200 + a non-empty model list."""
    if not api_key:
        return False
    try:
        req = urllib.request.Request(
            f"{VALIDATE_ENDPOINT}?key={api_key}",
            headers={"User-Agent": "pulse/1.0"},
            method="GET",
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            if resp.status != 200:
                return False
            data = json.loads(resp.read().decode("utf-8"))
            return bool(data.get("models"))
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError, TimeoutError):
        return False


def sync_from_api(api_key: str, since: datetime | None = None) -> list[dict]:
    """Returns [] — Google AI Studio has no retrospective usage endpoint.

    This is documented behavior, not a bug. To track Gemini usage going forward:
      1. Install the pulse browser extension (browser-ext/), which captures
         gemini.google.com / aistudio.google.com sessions client-side.
      2. Or use Vertex AI with gcloud billing export (Phase 4).
    """
    return []


def compute_cost(model: str, input_tokens: int, output_tokens: int,
                 cached_tokens: int = 0) -> float:
    """Apply current PRICING. Used by browser-extension captured rows."""
    model_key = model.lower()
    for known, rates in PRICING.items():
        if model_key.startswith(known):
            non_cached_in = max(input_tokens - cached_tokens, 0)
            return (
                non_cached_in * rates["input"]
                + output_tokens * rates["output"]
                + cached_tokens * rates["cache_read"]
            ) / 1_000_000
    # Unknown model — fall back to Flash rates (cheapest)
    rates = PRICING["gemini-2.5-flash"]
    return (input_tokens * rates["input"] + output_tokens * rates["output"]) / 1_000_000
