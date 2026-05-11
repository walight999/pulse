"""Pulse REST API — FastAPI server.

Exposes the user's own data for SDK / 3rd-party integrations / Pulse Pro
mobile app. JWT auth (Supabase Auth tokens) — same as cloud sync.

Run locally for dev:
    uvicorn api.server:app --reload --port 8000

Endpoints:
    GET  /v1/me                       — current user profile + plan
    GET  /v1/subscriptions             — list active + cancelled subs
    GET  /v1/token_usage?since=...     — token usage rows
    GET  /v1/stats/monthly             — aggregated monthly stats
    GET  /v1/leaderboard/{category}    — friend leaderboard (opt-in only)
    POST /v1/export                    — generate CSV/PDF export
"""
from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, timezone
from typing import Optional

try:
    from fastapi import FastAPI, HTTPException, Header, Query
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import Response
except ImportError:
    raise SystemExit("FastAPI not installed — run: pip install fastapi uvicorn")

import pandas as pd

from db import get_conn, get_setting
import export


app = FastAPI(
    title="Pulse API",
    description="Personal AI finance dashboard — REST API for SDK + mobile + 3rd party",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten for production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


def _require_auth(authorization: Optional[str]) -> dict:
    """Verify Supabase JWT. For local dev, accept any header.
    Production deployment must verify via Supabase JWKS."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing_bearer_token")
    token = authorization[7:]
    # TODO: verify against SUPABASE_JWT_SECRET or JWKS
    return {"user_id": "local-dev", "token": token}


@app.get("/v1/me")
def get_me(authorization: Optional[str] = Header(None)) -> dict:
    user = _require_auth(authorization)
    return {
        "user_id": user["user_id"],
        "email": get_setting("user_email", ""),
        "plan": get_setting("plan_tier", "free"),
        "currency": get_setting("display_currency", "THB"),
        "created_at": get_setting("account_created_at", ""),
    }


@app.get("/v1/subscriptions")
def list_subscriptions(active_only: bool = Query(False),
                        authorization: Optional[str] = Header(None)) -> list[dict]:
    _require_auth(authorization)
    conn = get_conn()
    sql = "SELECT * FROM subscriptions"
    if active_only:
        sql += " WHERE active = 1"
    sql += " ORDER BY cost DESC"
    return [dict(r) for r in conn.execute(sql).fetchall()]


@app.get("/v1/token_usage")
def list_token_usage(since: Optional[str] = None, limit: int = 1000,
                      authorization: Optional[str] = Header(None)) -> list[dict]:
    _require_auth(authorization)
    conn = get_conn()
    sql = "SELECT * FROM token_usage"
    params: list = []
    if since:
        sql += " WHERE timestamp >= ?"
        params.append(since)
    sql += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)
    return [dict(r) for r in conn.execute(sql, params).fetchall()]


@app.get("/v1/stats/monthly")
def monthly_stats(authorization: Optional[str] = Header(None)) -> dict:
    _require_auth(authorization)
    conn = get_conn()
    df = pd.read_sql_query(
        "SELECT strftime('%Y-%m', timestamp) AS month, "
        "COUNT(*) AS msgs, "
        "COALESCE(SUM(cost_usd), 0) AS cost_usd, "
        "COALESCE(SUM(input_tokens), 0) AS input_tokens, "
        "COALESCE(SUM(output_tokens), 0) AS output_tokens "
        "FROM token_usage GROUP BY month ORDER BY month DESC LIMIT 24",
        conn,
    )
    return {"months": df.to_dict(orient="records")}


@app.get("/v1/leaderboard/{category}")
def get_leaderboard(category: str,
                     window: str = Query("monthly"),
                     scope: str = Query("friends"),
                     authorization: Optional[str] = Header(None)) -> list[dict]:
    _require_auth(authorization)
    if category not in ("best_roi", "longest_streak", "token_wizard",
                         "power_day", "project_depth"):
        raise HTTPException(status_code=400, detail="invalid_category")
    try:
        from cloud.leaderboard import fetch_rankings
        entries = fetch_rankings(category, window=window, scope=scope)  # type: ignore
        return [
            {"rank": e.rank, "display_name": e.display_name,
             "value": e.metric_value, "unit": e.metric_unit}
            for e in entries
        ]
    except Exception:
        return []


@app.post("/v1/export")
def trigger_export(format: str = Query("csv"),
                    authorization: Optional[str] = Header(None)) -> Response:
    _require_auth(authorization)
    if format == "csv":
        data = export.export_all_zip()
        return Response(content=data, media_type="application/zip",
                        headers={"Content-Disposition": "attachment; filename=pulse-export.zip"})
    elif format == "pdf":
        month = datetime.now().strftime("%Y-%m")
        data = export.export_monthly_pdf(month)
        return Response(content=data, media_type="application/pdf",
                        headers={"Content-Disposition": f"attachment; filename=pulse-{month}.pdf"})
    else:
        raise HTTPException(status_code=400, detail="invalid_format")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "pulse-api", "version": "1.0.0",
            "ts": datetime.now(timezone.utc).isoformat()}


# Mount the WebSocket bridge for browser-extension real-time ingestion
try:
    from api.ws_bridge import router as ws_router
    app.include_router(ws_router)
except ImportError:
    pass
