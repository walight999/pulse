"""Smoke tests — every key module imports without error."""
import importlib
import pytest


CORE_MODULES = [
    "db",
    "theme",
    "fx",
    "quips",
    "sync_tokens",
    "categories",
    "ics_export",
    "export",
    "platform_compat",
    "account",
    "waitlist",
    "referrals",
    "telemetry",
]

OPTIONAL_MODULES = [
    "cloud.crypto",
    "cloud.auth",
    "cloud.sync",
    "cloud.leaderboard",
    "cloud.teams",
    "cloud.sso",
    "cloud.billing",
    "providers.openai_parser",
    "providers.cursor_parser",
    "providers.gemini_parser",
    "providers.copilot_parser",
    "providers.gmail_usage_parser",
    "integrations.slack",
    "integrations.teams",
    "integrations.discord",
    "api.server",
]


@pytest.mark.parametrize("mod", CORE_MODULES)
def test_core_modules_import(mod):
    importlib.import_module(mod)


@pytest.mark.parametrize("mod", OPTIONAL_MODULES)
def test_optional_modules_import(mod):
    # Optional modules may fail to import if their deps aren't installed
    # in CI. Skip rather than fail in that case.
    try:
        importlib.import_module(mod)
    except (ImportError, SystemExit) as e:
        pytest.skip(f"{mod}: optional dependency missing — {e}")
