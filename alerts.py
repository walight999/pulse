"""Background alert daemon — checks renewal/spike/dead-sub conditions and
sends Windows toast (or no-ops if user disabled)."""
from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path

from db import get_conn, get_setting, init_db
from notifications import toast


def _setting_int(key: str, default: int) -> int:
    raw = get_setting(key, "")
    try:
        return int(raw) if raw else default
    except ValueError:
        return default


def _setting_float(key: str, default: float) -> float:
    raw = get_setting(key, "")
    try:
        return float(raw) if raw else default
    except ValueError:
        return default


def _setting_bool(key: str, default: bool) -> bool:
    raw = get_setting(key, "")
    if not raw:
        return default
    return raw.lower() in ("1", "true", "yes", "on")


def _already_sent_today(kind: str, target_id: str) -> bool:
    conn = get_conn()
    today = date.today().isoformat()
    row = conn.execute(
        "SELECT id FROM alert_log WHERE kind = ? AND target_id = ? AND sent_at >= ?",
        (kind, target_id, today)
    ).fetchone()
    return row is not None


def _record(kind: str, target_id: str, body: str) -> None:
    conn = get_conn()
    try:
        conn.execute(
            "INSERT INTO alert_log (kind, target_id, body) VALUES (?, ?, ?)",
            (kind, target_id, body)
        )
        conn.commit()
    except Exception:
        pass


def check_upcoming_renewals() -> int:
    """Notify N days before each subscription renewal. Returns count fired."""
    if not _setting_bool("alerts_renewals_enabled", True):
        return 0
    days_ahead = _setting_int("alerts_renewals_days_ahead", 3)
    today = date.today()
    target_window = today + timedelta(days=days_ahead)

    conn = init_db()
    rows = conn.execute(
        "SELECT id, name, cost, currency, billing_cycle, next_billing_date "
        "FROM subscriptions WHERE active = 1 AND next_billing_date IS NOT NULL"
    ).fetchall()

    fired = 0
    for r in rows:
        try:
            nb = datetime.fromisoformat(r["next_billing_date"]).date()
        except Exception:
            continue
        if nb < today or nb > target_window:
            continue
        days_left = (nb - today).days
        target_id = f"renewal:{r['id']}:{nb.isoformat()}"
        if _already_sent_today("renewal", target_id):
            continue
        body = f"{r['name']} renews in {days_left} day(s) ({r['cost']:.2f} {r['currency']})"
        if toast("Subscription renewing soon", body):
            _record("renewal", target_id, body)
            fired += 1
    return fired


def check_token_spike() -> int:
    """Notify if today's token cost exceeds threshold% of daily average."""
    if not _setting_bool("alerts_token_spike_enabled", True):
        return 0
    multiplier = _setting_float("alerts_token_spike_multiplier", 3.0)
    daily_budget_usd = _setting_float("token_daily_budget_usd", 0.0)

    conn = init_db()
    today = date.today().isoformat()

    today_cost_row = conn.execute(
        "SELECT COALESCE(SUM(cost_usd), 0) AS c FROM token_usage WHERE DATE(timestamp) = ?",
        (today,)
    ).fetchone()
    today_cost = float(today_cost_row["c"] or 0)

    avg_row = conn.execute(
        """
        SELECT COALESCE(AVG(daily), 0) AS avg_cost
        FROM (
          SELECT DATE(timestamp) AS d, SUM(cost_usd) AS daily
          FROM token_usage
          WHERE DATE(timestamp) >= DATE('now', '-30 days') AND DATE(timestamp) < ?
          GROUP BY d
        )
        """,
        (today,)
    ).fetchone()
    avg_cost = float(avg_row["avg_cost"] or 0)

    fired = 0
    target_id = f"spike:{today}"
    if _already_sent_today("spike", target_id):
        return 0

    triggered = False
    msg = None
    if avg_cost > 0 and today_cost > avg_cost * multiplier:
        triggered = True
        msg = f"Today: ${today_cost:.2f} = {today_cost/avg_cost:.1f}x your 30d avg (${avg_cost:.2f})"
    if daily_budget_usd > 0 and today_cost >= daily_budget_usd:
        triggered = True
        msg = f"Today: ${today_cost:.2f} hit your daily budget (${daily_budget_usd:.2f})"

    if triggered and msg:
        if toast("Token cost spike", msg):
            _record("spike", target_id, msg)
            fired = 1
    return fired


def check_dead_subscriptions() -> int:
    """Notify weekly about subscriptions that look unused (red status)."""
    if not _setting_bool("alerts_dead_subs_enabled", True):
        return 0

    conn = init_db()
    today = date.today()
    today_str = today.isoformat()

    rows = conn.execute(
        "SELECT id, name, billing_cycle, last_charge_date, cost, currency "
        "FROM subscriptions WHERE active = 1"
    ).fetchall()

    dead = []
    for r in rows:
        if not r["last_charge_date"]:
            continue
        try:
            d = (today - datetime.fromisoformat(r["last_charge_date"]).date()).days
        except Exception:
            continue
        cycle = (r["billing_cycle"] or "").lower()
        # "dead" = monthly with >200d gap, yearly with >380d
        if cycle == "monthly" and d > 200:
            dead.append((r["id"], r["name"], d))
        elif cycle == "yearly" and d > 380:
            dead.append((r["id"], r["name"], d))

    # Send a single weekly summary
    if not dead:
        return 0
    target_id = f"dead:{today_str[:7]}"  # one per month max
    if _already_sent_today("dead_sub", target_id):
        return 0

    summary = ", ".join(f"{name} ({d}d)" for _, name, d in dead[:3])
    body = f"{len(dead)} subscription(s) likely cancelled — verify: {summary}"
    if toast("Possibly cancelled subs", body):
        _record("dead_sub", target_id, body)
        return 1
    return 0


def run_all_checks() -> dict:
    return {
        "renewals": check_upcoming_renewals(),
        "spike": check_token_spike(),
        "dead": check_dead_subscriptions(),
    }


if __name__ == "__main__":
    print(run_all_checks())
