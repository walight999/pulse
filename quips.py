"""Playful one-liner generator — adds personality to the dashboard.

Pick a quip based on what the data is doing. Keeps things fun without being annoying.
Returns None if no condition triggers (no quip is better than a forced one).

Stability: a quip stays the same all day for a given category, even across reruns.
Seeded by today's date + category — picks differ between days, not between clicks.
"""
from __future__ import annotations

import random
import datetime


def _pick(items: list[str], category: str) -> str:
    """Stable pick — same value across reruns within the same day."""
    seed = hash(f"{datetime.date.today().isoformat()}:{category}")
    return random.Random(seed).choice(items)


# Quips for high AI spend — teasing tone
HIGH_SPEND_DAY = [
    "Spending like a SaaS founder today.",
    "Opus called — wanted to thank you personally.",
    "Today's AI bill is bigger than most people's lunch budget.",
    "We see you cooking.",
    "Big day for Anthropic shareholders.",
    "Receipts are going to be embarrassing.",
    "The AI is doing fine, thanks for asking.",
]

# Spike: today way above average
SPIKE = [
    "Whoa — today's spend is well above your usual. Something fun?",
    "Either you found a new project, or you really hate Sonnet.",
    "Inflation hit your conversation — that's a lot of tokens.",
    "Hope it's worth it (it usually is).",
    "Big spike today. Hope you're shipping something cool.",
]

# Heavy Opus user
OPUS_HEAVY = [
    "Opus is doing the heavy lifting today.",
    "When in doubt, throw Opus at it (you know the way).",
    "The Opus-to-Sonnet ratio is… aggressive.",
]

# Healthy ROI
ROI_HEALTHY = [
    "ROI {n}× — you're getting away with murder on this plan.",
    "{n}× return — Anthropic should be calling you, not the other way around.",
    "{n}× value — buy the plan, profit on tokens.",
]

# Streak achievements
STREAK_LOW = [
    "{n}-day streak. The habit is forming.",
    "{n} days in. Keep going.",
]
STREAK_HIGH = [
    "{n}-day streak. You don't quit.",
    "{n} days. AI is officially your sidekick.",
    "{n}-day streak — at this point it's a relationship.",
]

# Subscription stack growing
MANY_SUBS = [
    "{n} subscriptions. You're collecting them like Pokémon.",
    "Stack: {n}. Time to audit?",
    "{n} subs going. Hope you remember what they all do.",
]

# Wasted subscriptions detected
WASTED = [
    "Money flying out the window: {amount}/mo on stuff you don't use.",
    "{amount}/mo just disappearing. Yikes.",
    "{amount}/mo to ghosts. Maybe say goodbye?",
]

# Unused-but-paid (over 60 days no use)
UNUSED_APP = [
    "Haven't opened {app} in {days} days. Pretty sure you're dating a different tool.",
    "{app} sat untouched for {days} days. Time to break up?",
    "{app} is feeling lonely ({days}d unused).",
]

# All clean
HEALTHY = [
    "Stack looks clean.",
    "Everything's tidy. Suspicious.",
    "0 wasted, 0 issues. Chef's kiss.",
    "Healthy stack. Keep it that way.",
]

# No subscriptions yet
EMPTY_STATE = [
    "Nothing here yet. Lucky you.",
    "Clean slate. Don't ruin it.",
    "Pulse is bored. Add a subscription to spark joy.",
]


def for_today_spend(today_usd: float, plan_per_day: float) -> str | None:
    """Today's AI spend quip."""
    if today_usd > 100:
        return _pick(HIGH_SPEND_DAY, "high_spend")
    if plan_per_day > 0 and today_usd > plan_per_day * 5:
        return _pick(HIGH_SPEND_DAY, "high_spend")
    return None


def for_spike(today_usd: float, avg_usd: float) -> str | None:
    if avg_usd <= 0:
        return None
    if today_usd >= avg_usd * 3:
        return _pick(SPIKE, "spike")
    return None


def for_roi(roi: float) -> str | None:
    if roi >= 10:
        return _pick(ROI_HEALTHY, "roi").format(n=f"{roi:.0f}")
    return None


def for_streak(days: int) -> str | None:
    if days >= 30:
        return _pick(STREAK_HIGH, "streak_high").format(n=days)
    if days >= 7:
        return _pick(STREAK_LOW, "streak_low").format(n=days)
    return None


def for_sub_count(active_count: int) -> str | None:
    if active_count >= 8:
        return _pick(MANY_SUBS, "many_subs").format(n=active_count)
    return None


def for_wasted(monthly_amount_str: str, has_wasted: bool) -> str | None:
    if not has_wasted:
        return None
    return _pick(WASTED, "wasted").format(amount=monthly_amount_str)


def for_unused_app(app_name: str, days_since: int) -> str | None:
    if days_since >= 60:
        return _pick(UNUSED_APP, f"unused_{app_name}").format(app=app_name, days=days_since)
    return None


def for_healthy_stack(active_count: int, wasted: float, attention: int) -> str | None:
    if active_count >= 2 and wasted == 0 and attention == 0:
        return _pick(HEALTHY, "healthy")
    return None


def for_empty() -> str:
    return _pick(EMPTY_STATE, "empty")
