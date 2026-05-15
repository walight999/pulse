"""Tools the 'Ask pulse' assistant exposes to Claude.

Each function returns a JSON-serializable dict. The assistant ships these as
Anthropic SDK `tools` and lets Claude decide when to call them based on the
user's natural-language query. All queries are read-only against the local
SQLite DB; nothing leaves the machine.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any

from db import get_conn, get_setting


# ───────────────────────── tool schemas ─────────────────────────

TOOLS_SCHEMA: list[dict[str, Any]] = [
    {
        "name": "query_subscriptions",
        "description": (
            "Get the user's subscriptions matching filters. Use when the user asks "
            "about their subs, plans, recurring charges, or what they're paying for. "
            "Returns name, price (in user's currency), billing cycle, vendor, active state."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "active_only":       {"type": "boolean", "default": True, "description": "Only currently-active subscriptions"},
                "include_cancelled": {"type": "boolean", "default": False, "description": "Also include cancelled ones"},
                "vendor_contains":   {"type": "string", "description": "Case-insensitive substring filter on vendor"},
                "name_contains":     {"type": "string", "description": "Case-insensitive substring filter on subscription name"},
            },
        },
    },
    {
        "name": "query_token_usage",
        "description": (
            "Get AI token usage and cost for a date range, optionally grouped by "
            "project/model/provider/day. Use for questions about AI costs, ROI, "
            "specific models, or trend over time."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "start_date": {"type": "string", "format": "date", "description": "YYYY-MM-DD inclusive start"},
                "end_date":   {"type": "string", "format": "date", "description": "YYYY-MM-DD inclusive end"},
                "group_by":   {"type": "string", "enum": ["project", "model", "provider", "day", "month"], "description": "How to aggregate the result"},
                "provider":   {"type": "string", "description": "Filter to a single provider (anthropic / openai / cursor / github-copilot)"},
            },
            "required": ["start_date", "end_date"],
        },
    },
    {
        "name": "compute_savings",
        "description": (
            "Calculate hypothetical savings from a scenario: cancelling a subscription, "
            "switching to yearly billing, or capping monthly AI spend. Returns the "
            "projected dollar amount."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "scenario": {"type": "string", "enum": ["cancel_subscription", "switch_to_yearly", "cap_monthly_spend"]},
                "params":   {"type": "object", "description": "Scenario-specific parameters"},
            },
            "required": ["scenario", "params"],
        },
    },
    {
        "name": "predict_monthly_total",
        "description": (
            "Forecast end-of-month AI token spend based on month-to-date pace. "
            "Linear projection only — does not account for upcoming weekends or holidays."
        ),
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "activity_summary",
        "description": (
            "Foreground app activity summary for a date range — total hours per app, "
            "useful for cost-per-active-hour questions. Returns 0 rows if activity tracking is off."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "start_date": {"type": "string", "format": "date"},
                "end_date":   {"type": "string", "format": "date"},
                "top_n":      {"type": "integer", "default": 10, "description": "Return only the top N apps by hours"},
            },
            "required": ["start_date", "end_date"],
        },
    },
]


# ───────────────────────── implementations ─────────────────────────

def query_subscriptions(active_only: bool = True, include_cancelled: bool = False,
                        vendor_contains: str | None = None,
                        name_contains: str | None = None) -> dict[str, Any]:
    """`vendor_contains` is matched against the `tag` column (closest analogue to a
    vendor field in the real schema)."""
    conn = get_conn()
    clauses: list[str] = []
    params: list[Any] = []
    if active_only and not include_cancelled:
        clauses.append("active = 1")
    if vendor_contains:
        clauses.append("LOWER(COALESCE(tag, '')) LIKE ?")
        params.append(f"%{vendor_contains.lower()}%")
    if name_contains:
        clauses.append("LOWER(name) LIKE ?")
        params.append(f"%{name_contains.lower()}%")
    where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
    sql = (
        "SELECT name, cost, currency, billing_cycle, next_billing_date, tag, "
        "linked_process, active, cancelled_at "
        f"FROM subscriptions {where} ORDER BY cost DESC"
    )
    try:
        rows = conn.execute(sql, params).fetchall()
    except Exception as e:
        return {"error": f"query failed: {e}", "subscriptions": []}

    out = []
    total_monthly = 0.0
    for r in rows:
        cost = float(r["cost"] or 0)
        cycle = (r["billing_cycle"] or "monthly").lower()
        monthly_equiv = cost / 12.0 if cycle == "yearly" else cost * 4.33 if cycle == "weekly" else cost
        if r["active"]:
            total_monthly += monthly_equiv
        out.append({
            "name": r["name"],
            "tag": r["tag"],
            "linked_process": r["linked_process"],
            "cost": cost,
            "currency": r["currency"] or "USD",
            "billing_cycle": cycle,
            "monthly_equivalent_usd": round(monthly_equiv, 2),
            "next_billing_date": r["next_billing_date"],
            "active": bool(r["active"]),
            "cancelled_at": r["cancelled_at"],
        })
    return {
        "count": len(out),
        "total_monthly_equivalent_usd": round(total_monthly, 2),
        "subscriptions": out,
    }


def query_token_usage(start_date: str, end_date: str,
                      group_by: str | None = None,
                      provider: str | None = None) -> dict[str, Any]:
    conn = get_conn()
    clauses = ["DATE(timestamp) >= DATE(?)", "DATE(timestamp) <= DATE(?)"]
    params: list[Any] = [start_date, end_date]
    if provider:
        clauses.append("provider = ?")
        params.append(provider)

    if group_by == "model":
        select = "model AS bucket, SUM(input_tokens + output_tokens) AS tokens, SUM(cost_usd) AS cost, COUNT(*) AS requests"
        group_clause = "GROUP BY model ORDER BY cost DESC"
    elif group_by == "provider":
        select = "provider AS bucket, SUM(input_tokens + output_tokens) AS tokens, SUM(cost_usd) AS cost, COUNT(*) AS requests"
        group_clause = "GROUP BY provider ORDER BY cost DESC"
    elif group_by == "project":
        select = "COALESCE(project_tag, '(no project)') AS bucket, SUM(input_tokens + output_tokens) AS tokens, SUM(cost_usd) AS cost, COUNT(*) AS requests"
        group_clause = "GROUP BY project_tag ORDER BY cost DESC LIMIT 25"
    elif group_by == "day":
        select = "DATE(timestamp) AS bucket, SUM(input_tokens + output_tokens) AS tokens, SUM(cost_usd) AS cost, COUNT(*) AS requests"
        group_clause = "GROUP BY DATE(timestamp) ORDER BY bucket"
    elif group_by == "month":
        select = "SUBSTR(timestamp, 1, 7) AS bucket, SUM(input_tokens + output_tokens) AS tokens, SUM(cost_usd) AS cost, COUNT(*) AS requests"
        group_clause = "GROUP BY SUBSTR(timestamp, 1, 7) ORDER BY bucket"
    else:
        select = "'total' AS bucket, SUM(input_tokens + output_tokens) AS tokens, SUM(cost_usd) AS cost, COUNT(*) AS requests"
        group_clause = ""

    sql = f"SELECT {select} FROM token_usage WHERE {' AND '.join(clauses)} {group_clause}"
    try:
        rows = conn.execute(sql, params).fetchall()
    except Exception as e:
        return {"error": f"query failed: {e}", "buckets": []}

    buckets = [
        {"bucket": r["bucket"], "tokens": int(r["tokens"] or 0),
         "cost_usd": round(float(r["cost"] or 0), 4), "requests": int(r["requests"] or 0)}
        for r in rows
    ]
    return {
        "start_date": start_date, "end_date": end_date,
        "provider_filter": provider, "group_by": group_by or "total",
        "buckets": buckets,
        "total_cost_usd": round(sum(b["cost_usd"] for b in buckets), 4),
        "total_tokens":   sum(b["tokens"] for b in buckets),
        "total_requests": sum(b["requests"] for b in buckets),
    }


def compute_savings(scenario: str, params: dict[str, Any]) -> dict[str, Any]:
    if scenario == "cancel_subscription":
        name = params.get("subscription_name", "")
        if not name:
            return {"error": "params.subscription_name required"}
        conn = get_conn()
        row = conn.execute(
            "SELECT name, cost, billing_cycle, currency FROM subscriptions "
            "WHERE LOWER(name) = LOWER(?) AND active = 1 LIMIT 1",
            (name,),
        ).fetchone()
        if not row:
            return {"error": f"no active subscription named '{name}' found"}
        cost = float(row["cost"] or 0)
        cycle = (row["billing_cycle"] or "monthly").lower()
        monthly = cost / 12.0 if cycle == "yearly" else cost
        return {
            "scenario": "cancel_subscription",
            "subscription": row["name"],
            "monthly_savings_usd":  round(monthly, 2),
            "yearly_savings_usd":   round(monthly * 12, 2),
            "five_year_savings_usd": round(monthly * 60, 2),
        }

    if scenario == "switch_to_yearly":
        name = params.get("subscription_name", "")
        discount_pct = float(params.get("discount_pct", 15))  # most yearly tiers ~15% off
        conn = get_conn()
        row = conn.execute(
            "SELECT name, cost FROM subscriptions WHERE LOWER(name) = LOWER(?) AND active = 1 LIMIT 1",
            (name,),
        ).fetchone()
        if not row:
            return {"error": f"no active subscription named '{name}' found"}
        monthly = float(row["cost"] or 0)
        annual_at_monthly = monthly * 12
        annual_at_yearly = annual_at_monthly * (1 - discount_pct / 100)
        return {
            "scenario": "switch_to_yearly",
            "subscription": row["name"],
            "monthly_cost_usd": monthly,
            "annual_cost_at_monthly_usd": round(annual_at_monthly, 2),
            "annual_cost_at_yearly_usd":  round(annual_at_yearly, 2),
            "annual_savings_usd":         round(annual_at_monthly - annual_at_yearly, 2),
            "discount_pct_assumed": discount_pct,
        }

    if scenario == "cap_monthly_spend":
        cap = float(params.get("cap_usd", 0))
        if cap <= 0:
            return {"error": "params.cap_usd must be > 0"}
        from datetime import date as _date
        today = _date.today()
        start = today.replace(day=1).isoformat()
        end = today.isoformat()
        usage = query_token_usage(start, end)
        mtd = usage["total_cost_usd"]
        days_elapsed = today.day
        days_in_month = 30  # rough
        projected = mtd / max(days_elapsed, 1) * days_in_month
        return {
            "scenario": "cap_monthly_spend",
            "cap_usd": cap,
            "month_to_date_usd": mtd,
            "projected_eom_usd": round(projected, 2),
            "would_blow_cap": projected > cap,
            "overage_if_blow_usd": round(max(projected - cap, 0), 2),
        }

    return {"error": f"unknown scenario '{scenario}'"}


def predict_monthly_total() -> dict[str, Any]:
    from datetime import date as _date
    today = _date.today()
    start = today.replace(day=1).isoformat()
    end = today.isoformat()
    usage = query_token_usage(start, end)
    days_elapsed = today.day
    if days_elapsed < 1:
        return {"error": "no days elapsed yet"}
    # naive end-of-month projection
    # find days in month
    if today.month == 12:
        next_month = today.replace(year=today.year + 1, month=1, day=1)
    else:
        next_month = today.replace(month=today.month + 1, day=1)
    days_in_month = (next_month - timedelta(days=1)).day
    mtd = usage["total_cost_usd"]
    projected = mtd / days_elapsed * days_in_month
    return {
        "month": today.strftime("%Y-%m"),
        "days_elapsed": days_elapsed,
        "days_in_month": days_in_month,
        "month_to_date_cost_usd": mtd,
        "projected_eom_cost_usd": round(projected, 2),
        "method": "linear projection of MTD pace — does not account for weekends or upcoming holidays",
    }


def activity_summary(start_date: str, end_date: str, top_n: int = 10) -> dict[str, Any]:
    conn = get_conn()
    try:
        rows = conn.execute(
            """
            SELECT process_name AS app,
                   SUM(duration_seconds) / 3600.0 AS hours,
                   COUNT(*) AS sessions
            FROM app_activity
            WHERE DATE(started_at) >= DATE(?) AND DATE(started_at) <= DATE(?)
              AND process_name IS NOT NULL
            GROUP BY process_name
            ORDER BY hours DESC
            LIMIT ?
            """,
            (start_date, end_date, top_n),
        ).fetchall()
    except Exception as e:
        return {"error": f"query failed: {e}", "apps": []}

    apps = [{"app": r["app"], "hours": round(float(r["hours"] or 0), 2),
             "sessions": int(r["sessions"] or 0)} for r in rows]
    total_hours = round(sum(a["hours"] for a in apps), 2)
    return {
        "start_date": start_date, "end_date": end_date,
        "tracking_enabled": get_setting("activity_tracking_enabled", "0") == "1",
        "top_n": top_n,
        "apps": apps,
        "total_hours_in_top_n": total_hours,
    }


# ───────────────────────── dispatcher ─────────────────────────

def execute_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Single entry point the Ask-pulse chat loop uses to dispatch tool calls."""
    funcs = {
        "query_subscriptions":   query_subscriptions,
        "query_token_usage":     query_token_usage,
        "compute_savings":       compute_savings,
        "predict_monthly_total": predict_monthly_total,
        "activity_summary":      activity_summary,
    }
    fn = funcs.get(name)
    if not fn:
        return {"error": f"unknown tool '{name}'"}
    try:
        return fn(**arguments) if arguments else fn()
    except TypeError as e:
        return {"error": f"bad arguments for {name}: {e}"}
    except Exception as e:
        return {"error": f"tool {name} crashed: {e}"}
