"""Mistral La Plateforme usage parser — stub.

Mistral exposes /v1/usage similar to OpenAI for API users. Le Chat Pro
is a flat-rate consumer subscription.
"""
from __future__ import annotations

PRICING = {
    # Mistral models (USD per million tokens, approx)
    "mistral-large-2":   {"input": 2.0,  "output": 6.0},
    "mistral-large":     {"input": 3.0,  "output": 9.0},
    "mistral-medium-3":  {"input": 0.4,  "output": 2.0},
    "mistral-small-3.1": {"input": 0.10, "output": 0.30},
    "codestral":         {"input": 0.3,  "output": 0.9},
    "pixtral-12b":       {"input": 0.15, "output": 0.15},
}

FLAT_PRICING = {
    "le-chat-pro":  {"monthly_usd": 14.99},
    "le-chat-team": {"monthly_usd": 24.99},
}


def sync_from_api(api_key: str, since=None) -> list[dict]:
    raise NotImplementedError("Phase 2 — implement when API key UX lands in Settings")
