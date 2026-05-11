"""CSV + PDF export for subscriptions, token usage, and activity.

CSV: stdlib only, always available.
PDF: requires `reportlab` (graceful fallback to CSV+HTML if missing).
"""
from __future__ import annotations

import csv
import io
from datetime import date, datetime
from pathlib import Path
from typing import Optional

import pandas as pd

from db import get_conn


# ────────────────── CSV exports ──────────────────

def export_subscriptions_csv() -> str:
    """Return subscription table as CSV string."""
    conn = get_conn()
    df = pd.read_sql_query(
        "SELECT name, cost, currency, billing_cycle, next_billing_date, "
        "last_charge_date, active, tag, notes, cancel_url, "
        "cancelled_at, cancelled_monthly_usd, is_trial, trial_ends_at "
        "FROM subscriptions ORDER BY active DESC, cost DESC",
        conn,
    )
    out = io.StringIO()
    df.to_csv(out, index=False)
    return out.getvalue()


def export_token_usage_csv(since: Optional[str] = None) -> str:
    conn = get_conn()
    query = (
        "SELECT timestamp, provider, model, "
        "input_tokens, output_tokens, "
        "cache_creation_tokens, cache_read_tokens, "
        "cost_usd, project_tag, session_id "
        "FROM token_usage"
    )
    params = []
    if since:
        query += " WHERE timestamp >= ?"
        params.append(since)
    query += " ORDER BY timestamp DESC"
    df = pd.read_sql_query(query, conn, params=params)
    out = io.StringIO()
    df.to_csv(out, index=False)
    return out.getvalue()


def export_activity_csv(since: Optional[str] = None) -> str:
    conn = get_conn()
    query = (
        "SELECT started_at, ended_at, process_name, window_title, duration_seconds "
        "FROM app_activity"
    )
    params = []
    if since:
        query += " WHERE started_at >= ?"
        params.append(since)
    query += " ORDER BY started_at DESC"
    df = pd.read_sql_query(query, conn, params=params)
    out = io.StringIO()
    df.to_csv(out, index=False)
    return out.getvalue()


def export_all_zip() -> bytes:
    """Bundle all CSVs + a manifest into a single ZIP."""
    import zipfile
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("subscriptions.csv", export_subscriptions_csv())
        zf.writestr("token_usage.csv", export_token_usage_csv())
        zf.writestr("app_activity.csv", export_activity_csv())
        zf.writestr("README.txt",
                    f"Pulse data export\nGenerated: {datetime.now().isoformat()}\n\n"
                    "subscriptions.csv  — recurring services + costs + status\n"
                    "token_usage.csv     — AI usage logs with per-message cost\n"
                    "app_activity.csv    — foreground app sessions with duration\n")
    return buf.getvalue()


# ────────────────── PDF report ──────────────────

def export_monthly_pdf(month_iso: str) -> bytes:
    """Generate a one-page PDF summary for a given month (YYYY-MM)."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        )
    except ImportError:
        # Fallback — return HTML that the user can print to PDF
        return _html_report(month_iso).encode("utf-8")

    conn = get_conn()
    start = f"{month_iso}-01"
    next_month = (datetime.fromisoformat(start) + pd.Timedelta(days=32)).strftime("%Y-%m-01")

    # Pull data
    token_total = float(conn.execute(
        "SELECT COALESCE(SUM(cost_usd), 0) FROM token_usage "
        "WHERE timestamp >= ? AND timestamp < ?",
        (start, next_month),
    ).fetchone()[0] or 0)
    n_msgs = int(conn.execute(
        "SELECT COUNT(*) FROM token_usage WHERE timestamp >= ? AND timestamp < ?",
        (start, next_month),
    ).fetchone()[0] or 0)
    subs = pd.read_sql_query(
        "SELECT name, cost, currency, billing_cycle FROM subscriptions "
        "WHERE active = 1 ORDER BY cost DESC LIMIT 20",
        conn,
    )

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        leftMargin=0.6 * inch, rightMargin=0.6 * inch,
        topMargin=0.7 * inch, bottomMargin=0.6 * inch,
    )
    styles = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontSize=22,
                         textColor=colors.HexColor("#0f172a"), spaceAfter=6)
    h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontSize=14,
                         textColor=colors.HexColor("#475569"), spaceAfter=4)
    body = styles["Normal"]

    story = [
        Paragraph(f"Pulse Monthly Report — {month_iso}", h1),
        Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", body),
        Spacer(1, 12),
        Paragraph("AI usage", h2),
        Paragraph(f"Total spend: <b>${token_total:,.2f}</b> across {n_msgs:,} messages", body),
        Spacer(1, 12),
        Paragraph("Active subscriptions (top 20)", h2),
    ]
    if not subs.empty:
        sub_data = [["Name", "Cost", "Currency", "Cycle"]]
        for _, r in subs.iterrows():
            sub_data.append([r["name"], f"{r['cost']:.2f}", r["currency"], r["billing_cycle"]])
        tbl = Table(sub_data, colWidths=[3.0 * inch, 1.0 * inch, 1.0 * inch, 1.0 * inch])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eef2ff")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, colors.HexColor("#f8fafc")]),
        ]))
        story.append(tbl)
    else:
        story.append(Paragraph("No active subscriptions recorded.", body))

    story.extend([
        Spacer(1, 18),
        Paragraph(
            "Generated by Pulse — your personal AI finance dashboard. "
            "Visit <a href='https://pulse.app'>pulse.app</a>.",
            body,
        ),
    ])
    doc.build(story)
    return buf.getvalue()


def _html_report(month_iso: str) -> str:
    """Fallback HTML report when reportlab is not installed."""
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Pulse {month_iso}</title>
<style>body{{font-family:system-ui;max-width:720px;margin:40px auto;padding:20px;color:#0f172a;}}
h1{{font-size:24px;margin:0 0 4px;}}h2{{color:#475569;}}</style></head>
<body><h1>Pulse Monthly Report — {month_iso}</h1>
<p>reportlab not installed — install with: <code>pip install reportlab</code></p>
</body></html>"""
