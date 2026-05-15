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


import os

# Dev mode bypasses JWT signature verification — only honored when
# PULSE_API_DEV_MODE=1 is set in the environment. Production deployments
# verify Supabase JWTs via JWKS or the shared SUPABASE_JWT_SECRET.
PULSE_API_DEV_MODE = os.environ.get("PULSE_API_DEV_MODE", "") == "1"
SUPABASE_JWT_SECRET = os.environ.get("SUPABASE_JWT_SECRET", "")


def _verify_supabase_jwt(token: str) -> dict:
    """Verify a Supabase-issued JWT. Requires SUPABASE_JWT_SECRET env var.

    Falls back to the dev bypass if SUPABASE_JWT_SECRET is not set AND
    PULSE_API_DEV_MODE=1 — letting a developer hack on the API without
    standing up a Supabase project first.
    """
    if not SUPABASE_JWT_SECRET:
        if PULSE_API_DEV_MODE:
            # Accept any non-empty token, derive user_id from a sha1 of it.
            import hashlib
            uid = hashlib.sha1(token.encode("utf-8")).hexdigest()[:16]
            return {"user_id": f"dev-{uid}", "token": token, "dev_mode": True}
        raise HTTPException(
            status_code=500,
            detail="SUPABASE_JWT_SECRET not configured (or set PULSE_API_DEV_MODE=1 for dev)",
        )

    # Real verification via PyJWT if available, otherwise hand-rolled HMAC.
    try:
        import jwt  # PyJWT
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=["HS256"],
            audience=os.environ.get("SUPABASE_JWT_AUDIENCE", "authenticated"),
        )
        return {"user_id": payload.get("sub", ""), "token": token, "claims": payload}
    except ImportError:
        # Fallback: manual HMAC verify (good enough for HS256, the Supabase default)
        return _verify_hs256_manual(token, SUPABASE_JWT_SECRET)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"invalid_token: {e}")


def _verify_hs256_manual(token: str, secret: str) -> dict:
    import base64, hmac, hashlib, json as _json
    try:
        header_b64, payload_b64, sig_b64 = token.split(".")
    except ValueError:
        raise HTTPException(status_code=401, detail="malformed_token")

    def _b64decode(s: str) -> bytes:
        s = s + "=" * (-len(s) % 4)
        return base64.urlsafe_b64decode(s)

    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    expected_sig = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    if not hmac.compare_digest(_b64decode(sig_b64), expected_sig):
        raise HTTPException(status_code=401, detail="invalid_signature")

    payload = _json.loads(_b64decode(payload_b64))
    exp = payload.get("exp", 0)
    if exp and exp < datetime.now(timezone.utc).timestamp():
        raise HTTPException(status_code=401, detail="token_expired")
    return {"user_id": payload.get("sub", ""), "token": token, "claims": payload}


def _require_auth(authorization: Optional[str]) -> dict:
    """Verify Supabase JWT (or accept any bearer in dev mode)."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing_bearer_token")
    return _verify_supabase_jwt(authorization[7:])


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


@app.get("/healthz")
def healthz() -> dict:
    """Kubernetes-style health check — same as /health but with /z suffix
    so platforms like Fly.io / Render / Railway recognize it automatically."""
    return {
        "status": "ok",
        "service": "pulse-api",
        "version": "1.0.0",
        "dev_mode": PULSE_API_DEV_MODE,
        "supabase_configured": bool(SUPABASE_JWT_SECRET),
        "ts": datetime.now(timezone.utc).isoformat(),
    }


# Mount the WebSocket bridge for browser-extension real-time ingestion
try:
    from api.ws_bridge import router as ws_router
    app.include_router(ws_router)
except ImportError:
    pass


def main() -> None:
    """CLI entry point: `python -m api.server` or `python api/server.py`."""
    import argparse
    try:
        import uvicorn
    except ImportError:
        raise SystemExit("uvicorn not installed — run: pip install -r requirements-cloud.txt")

    parser = argparse.ArgumentParser(description="Pulse REST API server")
    parser.add_argument("--host", default="127.0.0.1", help="Bind address (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Port (default: 8000)")
    parser.add_argument("--dev", action="store_true",
                        help="Dev mode — bypass JWT signature verification (sets PULSE_API_DEV_MODE=1)")
    parser.add_argument("--reload", action="store_true", help="Auto-reload on file changes")
    args = parser.parse_args()

    if args.dev:
        os.environ["PULSE_API_DEV_MODE"] = "1"
        global PULSE_API_DEV_MODE
        PULSE_API_DEV_MODE = True
        print("⚠ DEV MODE — JWT signatures NOT verified. Do NOT expose this to the public internet.")

    if not SUPABASE_JWT_SECRET and not PULSE_API_DEV_MODE:
        print(
            "⚠ SUPABASE_JWT_SECRET not set — every request will return 500.\n"
            "  Either: (a) set SUPABASE_JWT_SECRET=... in env, or\n"
            "          (b) pass --dev to bypass JWT verification for local development."
        )

    uvicorn.run(
        "api.server:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info",
    )


if __name__ == "__main__":
    main()
