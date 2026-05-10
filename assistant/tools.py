"""Tools the assistant exposes to Claude — Phase 3 stub.

Implements the JSON-schema tool-use pattern. The assistant calls these
functions; Claude decides when based on the user's natural-language query.
"""
from __future__ import annotations


# Schema definitions — pass to Anthropic SDK as the `tools` parameter
TOOLS_SCHEMA = [
    {
        "name": "query_subscriptions",
        "description": "Get subscriptions matching filters. Use when the user asks about their subs.",
        "input_schema": {
            "type": "object",
            "properties": {
                "active_only": {"type": "boolean", "default": True},
                "tag":         {"type": "string"},
                "billing_cycle": {"type": "string", "enum": ["monthly", "yearly", "weekly", "daily", "one-time"]},
                "include_cancelled": {"type": "boolean", "default": False},
            },
        },
    },
    {
        "name": "query_token_usage",
        "description": "Get AI token usage for a date range, optionally grouped.",
        "input_schema": {
            "type": "object",
            "properties": {
                "start_date":  {"type": "string", "format": "date"},
                "end_date":    {"type": "string", "format": "date"},
                "group_by":    {"type": "string", "enum": ["project", "model", "day", "hour"]},
            },
            "required": ["start_date", "end_date"],
        },
    },
    {
        "name": "compute_savings",
        "description": "Calculate hypothetical savings: cancel a sub, switch model, etc.",
        "input_schema": {
            "type": "object",
            "properties": {
                "scenario": {"type": "string", "enum": [
                    "cancel_subscription",
                    "switch_model_for_project",
                    "switch_to_yearly_billing",
                ]},
                "params":   {"type": "object"},
            },
            "required": ["scenario", "params"],
        },
    },
    {
        "name": "predict_monthly_total",
        "description": "Forecast end-of-month AI spend based on current pace.",
        "input_schema": {"type": "object"},
    },
]


def query_subscriptions(active_only=True, tag=None, billing_cycle=None,
                         include_cancelled=False) -> list[dict]:
    raise NotImplementedError("Phase 3 — read from local subscriptions table")


def query_token_usage(start_date: str, end_date: str, group_by: str | None = None) -> dict:
    raise NotImplementedError("Phase 3 — read from local token_usage table")


def compute_savings(scenario: str, params: dict) -> dict:
    raise NotImplementedError("Phase 3 — pure math on local data")


def predict_monthly_total() -> dict:
    raise NotImplementedError("Phase 3 — linear projection from current MTD")
