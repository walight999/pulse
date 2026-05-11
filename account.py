"""Local Pulse account — anonymous UUID per install + tier feature gating.

Used for:
  - Telemetry correlation (opt-in)
  - Cloud sync identification (when Phase 1 ships)
  - Referral codes
  - Migration to cloud auth without losing data
  - Tier feature gating (free / pro / team / enterprise)
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Literal

from db import get_setting, set_setting, init_db

Tier = Literal["free", "pro", "team", "enterprise"]

# Each tier owns its own marginal flags. Higher tiers inherit lower ones via
# _resolved_features() so we never have to repeat flags in multiple sets.
TIER_FEATURES: dict[Tier, set[str]] = {
    "free": {
        "subscription_tracker",
        "ai_usage_local",
        "activity_tracking",
        "browser_extension",
        "multi_currency",
        "csv_export",
        "ics_export",
    },
    "pro": {
        "cloud_sync",
        "mobile_pwa",
        "multi_provider_live",
        "friend_leaderboard",
        "ai_assistant",
        "extended_audit_log",
        "priority_support",
    },
    "team": {
        "team_dashboard",
        "per_user_attribution",
        "slack_integration",
        "teams_integration",
        "discord_integration",
        "admin_controls",
        "audit_log_1yr",
    },
    "enterprise": {
        "sso_saml",
        "sso_oidc",
        "custom_roles",
        "audit_log_7yr",
        "data_residency",
        "soc2_report",
        "dedicated_csm",
        "on_prem_deploy",
    },
}

TIER_ORDER: list[Tier] = ["free", "pro", "team", "enterprise"]

TIER_DISPLAY: dict[Tier, dict] = {
    "free":       {"name": "Free",       "price_label": "$0 forever",       "next_tier": "pro"},
    "pro":        {"name": "Pro",        "price_label": "$9 /mo",            "next_tier": "team"},
    "team":       {"name": "Team",       "price_label": "$19 /seat/mo",      "next_tier": "enterprise"},
    "enterprise": {"name": "Enterprise", "price_label": "Custom",            "next_tier": None},
}


def _resolved_features(tier: Tier) -> set[str]:
    out: set[str] = set()
    for t in TIER_ORDER:
        out |= TIER_FEATURES[t]
        if t == tier:
            break
    return out


def get_tier() -> Tier:
    """Current tier. Defaults to free. Cloud sync overrides this from server when signed in."""
    init_db()
    raw = (get_setting("pulse_tier", "free") or "free").strip().lower()
    if raw not in TIER_FEATURES:
        return "free"
    return raw  # type: ignore[return-value]


def set_tier(tier: Tier) -> None:
    """Persist tier. Cloud module sets this after server confirmation."""
    if tier not in TIER_FEATURES:
        raise ValueError(f"unknown tier: {tier}")
    init_db()
    set_setting("pulse_tier", tier)


def feature_enabled(flag: str) -> bool:
    """True if current tier (or any inherited tier) includes `flag`."""
    return flag in _resolved_features(get_tier())


def tier_for_feature(flag: str) -> Tier | None:
    """Lowest tier that unlocks `flag`. None if flag is unknown."""
    for t in TIER_ORDER:
        if flag in TIER_FEATURES[t]:
            return t
    return None


def tier_display(tier: Tier | None = None) -> dict:
    return TIER_DISPLAY[tier or get_tier()]


def get_account_id() -> str:
    """Return this install's anonymous UUID. Generated once on first call."""
    init_db()
    aid = get_setting("pulse_account_id", "")
    if not aid:
        aid = str(uuid.uuid4())
        set_setting("pulse_account_id", aid)
        set_setting("pulse_account_created_at",
                    datetime.utcnow().isoformat(timespec="seconds") + "Z")
    return aid


def get_account_age_days() -> int:
    raw = get_setting("pulse_account_created_at", "")
    if not raw:
        return 0
    try:
        created = datetime.fromisoformat(raw.rstrip("Z"))
        return (datetime.utcnow() - created).days
    except Exception:
        return 0


def short_id() -> str:
    """First 8 chars of account UUID — for display."""
    return get_account_id().split("-")[0]


if __name__ == "__main__":
    print("Account ID:", get_account_id())
    print("Short ID:  ", short_id())
    print("Age:       ", get_account_age_days(), "days")
    print("Tier:      ", get_tier())
    print("Cloud sync:", feature_enabled("cloud_sync"))
    print("SSO:       ", feature_enabled("sso_saml"))
