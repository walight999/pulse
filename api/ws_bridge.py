"""WebSocket bridge — real-time browser-extension → desktop ingestion.

Replaces the 5-min HTTP buffer flush with a persistent local WebSocket.
Browser extension connects to `ws://localhost:8000/v1/ws/ingest`, pushes
events as they happen, desktop dashboard sees them within milliseconds.

If desktop is offline (port not listening), the extension falls back to
its existing 5-min HTTP buffer (background.js handles both paths).

Run alongside the REST API:
    uvicorn api.server:app --host 127.0.0.1 --port 8000

The WS endpoint is mounted on the same FastAPI app.

Security: localhost-only by design (no auth required — local trust boundary).
"""
from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime, timezone
from typing import Any

try:
    from fastapi import APIRouter, WebSocket, WebSocketDisconnect
except ImportError:
    raise SystemExit("FastAPI not installed — pip install fastapi uvicorn")


logger = logging.getLogger("pulse.ws_bridge")
router = APIRouter()


class ConnectionManager:
    """Tracks active WebSocket connections. Multiple browser extensions
    (Chrome + Edge + Firefox) can connect simultaneously."""

    def __init__(self):
        self.active: list[WebSocket] = []
        self.lock = asyncio.Lock()
        self.events_received_total = 0

    async def connect(self, ws: WebSocket):
        await ws.accept()
        async with self.lock:
            self.active.append(ws)
        logger.info("ws connect (total=%d)", len(self.active))

    async def disconnect(self, ws: WebSocket):
        async with self.lock:
            if ws in self.active:
                self.active.remove(ws)
        logger.info("ws disconnect (total=%d)", len(self.active))

    async def broadcast(self, message: dict):
        """Echo message to all connected clients (for cross-browser dashboards)."""
        async with self.lock:
            for ws in list(self.active):
                try:
                    await ws.send_json(message)
                except Exception:
                    self.active.remove(ws)


manager = ConnectionManager()


def _ingest_event(event: dict) -> dict:
    """Insert a single browser-ext event into token_usage.
    Returns {ok, request_id} or {ok: False, error}."""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from db import get_conn

    provider = event.get("provider", "unknown")
    model = event.get("model", f"{provider}-web")
    ts = event.get("timestamp") or datetime.now(timezone.utc).isoformat(timespec="seconds")
    approx_chars = int(event.get("approx_chars", 0) or 0)
    approx_tokens = max(approx_chars // 4, 1) if approx_chars else 1

    # Synthetic request_id ensures dedup if browser retries
    captured = event.get("captured_at", ts)
    request_id = f"browser-ext:{provider}:{captured}:{model}"

    conn = get_conn()
    try:
        conn.execute(
            "INSERT INTO token_usage "
            "(timestamp, provider, model, "
            " input_tokens, output_tokens, "
            " cache_creation_tokens, cache_creation_5m_tokens, cache_creation_1h_tokens, "
            " cache_read_tokens, cost_usd, project_tag, session_id, request_id, source) "
            "VALUES (?, ?, ?, 0, ?, 0, 0, 0, 0, 0, ?, NULL, ?, 'browser-ext')",
            (ts, provider, model, approx_tokens, f"web-{provider}", request_id),
        )
        conn.commit()
        return {"ok": True, "request_id": request_id}
    except Exception as e:
        # UNIQUE violation = already ingested, silently ok
        if "UNIQUE" in str(e):
            return {"ok": True, "request_id": request_id, "dedup": True}
        return {"ok": False, "error": str(e)}


@router.websocket("/v1/ws/ingest")
async def ws_ingest(ws: WebSocket):
    """Real-time ingestion endpoint for browser extensions.

    Protocol:
        Client sends: {"events": [{provider, model, timestamp, approx_chars, ...}, ...]}
        Server replies: {"received": N, "ingested": M, "errors": [...]}

    Also accepts single-event messages: {provider, model, timestamp, ...}
    """
    await manager.connect(ws)
    try:
        while True:
            raw = await ws.receive_text()
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                await ws.send_json({"ok": False, "error": "invalid_json"})
                continue

            events = msg.get("events")
            if events is None and "provider" in msg:
                # Single-event message — wrap in list
                events = [msg]
            if not isinstance(events, list):
                await ws.send_json({"ok": False, "error": "expected 'events' array"})
                continue

            ingested = 0
            errors: list[str] = []
            for ev in events:
                result = _ingest_event(ev)
                if result.get("ok"):
                    ingested += 1
                    manager.events_received_total += 1
                else:
                    errors.append(result.get("error", "unknown"))

            await ws.send_json({
                "received": len(events),
                "ingested": ingested,
                "errors": errors[:5],   # cap error list
                "total_session": manager.events_received_total,
            })
    except WebSocketDisconnect:
        await manager.disconnect(ws)
    except Exception as e:
        logger.error("ws_ingest error: %s", e)
        await manager.disconnect(ws)


@router.get("/v1/ws/stats")
async def ws_stats():
    """Inspect current WS connections + total events ingested this session."""
    return {
        "active_connections": len(manager.active),
        "events_this_session": manager.events_received_total,
    }
