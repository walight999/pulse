"""OpenAI Admin API adapter — Phase 3 stub.

User pastes their admin key in Settings. Daily sync pulls usage from
the OpenAI org-level usage endpoint.
"""
from __future__ import annotations


# OpenAI pricing (USD per million tokens, as of 2026 estimates — update if drifted)
PRICING = {
    "gpt-5":              {"input": 5.0,  "output": 15.0},
    "gpt-5-mini":         {"input": 0.25, "output": 1.25},
    "gpt-4o":             {"input": 2.50, "output": 10.0},
    "gpt-4o-mini":        {"input": 0.15, "output": 0.60},
    "o1":                 {"input": 15.0, "output": 60.0},
    "o3-mini":            {"input": 1.10, "output": 4.40},
}


def sync(admin_key: str) -> dict:
    """Sync OpenAI org usage. Returns {rows_added, rows_skipped, error}."""
    raise NotImplementedError(
        "Phase 3 — call https://api.openai.com/v1/organization/usage/completions"
    )
