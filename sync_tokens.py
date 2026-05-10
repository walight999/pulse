"""Token usage sync — Claude Code local logs + (optional) Anthropic Admin API.

Sources:
  1. Claude Code transcripts in ~/.claude/projects/**/*.jsonl   (no key required)
  2. Anthropic Admin API                                        (requires ANTHROPIC_ADMIN_KEY)
  3. OpenAI Usage API                                           (requires OPENAI_ADMIN_KEY) — stub

Idempotent: deduplicates on request_id, so re-running is safe.
"""
from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from db import get_conn, init_db

CLAUDE_PROJECTS_DIR = Path.home() / ".claude" / "projects"

# Pricing in USD per million tokens. Cache pricing has separate 5min vs 1hr rates:
#   - 5min ephemeral cache write: 1.25 x input price
#   - 1hr  ephemeral cache write: 2.00 x input price
#   - cache read:                 0.10 x input price
PRICING: dict[str, dict[str, float]] = {
    "claude-opus-4-7":     {"input": 15.0,  "output": 75.0,  "cw_5m": 18.75, "cw_1h": 30.0,  "cache_read": 1.50},
    "claude-opus-4-6":     {"input": 15.0,  "output": 75.0,  "cw_5m": 18.75, "cw_1h": 30.0,  "cache_read": 1.50},
    "claude-opus-4":       {"input": 15.0,  "output": 75.0,  "cw_5m": 18.75, "cw_1h": 30.0,  "cache_read": 1.50},
    "claude-sonnet-4-6":   {"input": 3.0,   "output": 15.0,  "cw_5m":  3.75, "cw_1h":  6.0,  "cache_read": 0.30},
    "claude-sonnet-4-5":   {"input": 3.0,   "output": 15.0,  "cw_5m":  3.75, "cw_1h":  6.0,  "cache_read": 0.30},
    "claude-sonnet-4":     {"input": 3.0,   "output": 15.0,  "cw_5m":  3.75, "cw_1h":  6.0,  "cache_read": 0.30},
    "claude-haiku-4-5":    {"input": 0.80,  "output": 4.0,   "cw_5m":  1.00, "cw_1h":  1.6,  "cache_read": 0.08},
    "claude-haiku-4":      {"input": 0.80,  "output": 4.0,   "cw_5m":  1.00, "cw_1h":  1.6,  "cache_read": 0.08},
}
DEFAULT_PRICING = {"input": 3.0, "output": 15.0, "cw_5m": 3.75, "cw_1h": 6.0, "cache_read": 0.30}


def price_for(model: str) -> dict[str, float]:
    """Return pricing dict for a model, falling back to Sonnet-equivalent if unknown."""
    if not model:
        return DEFAULT_PRICING
    # Strip vendor suffixes / version brackets like "[1m]"
    base = model.split("[")[0].strip()
    if base in PRICING:
        return PRICING[base]
    # Try matching by family
    for k in PRICING:
        if base.startswith(k):
            return PRICING[k]
    return DEFAULT_PRICING


def calc_cost(usage: dict, model: str) -> float:
    """Cost in USD. Uses TTL-split cache write tokens if available; falls back to
    treating the bulk cache_creation_tokens as 5min-cache (cheaper assumption)."""
    p = price_for(model)
    in_t  = usage.get("input_tokens", 0) or 0
    out_t = usage.get("output_tokens", 0) or 0
    cr_t  = usage.get("cache_read_tokens", 0) or 0
    cw_5m = usage.get("cache_creation_5m_tokens", 0) or 0
    cw_1h = usage.get("cache_creation_1h_tokens", 0) or 0
    cw_total = usage.get("cache_creation_tokens", 0) or 0

    # If breakdown not provided, assume all 5m (legacy / older logs)
    if cw_5m == 0 and cw_1h == 0 and cw_total > 0:
        cw_5m = cw_total

    return (
        in_t  * p["input"]      / 1_000_000 +
        out_t * p["output"]     / 1_000_000 +
        cr_t  * p["cache_read"] / 1_000_000 +
        cw_5m * p["cw_5m"]      / 1_000_000 +
        cw_1h * p["cw_1h"]      / 1_000_000
    )


def project_tag_from_cwd(cwd: str | None, fallback_dir_name: str | None = None) -> str | None:
    if cwd:
        return Path(cwd).name
    if fallback_dir_name:
        # Claude Code dir name format: C--Users-usEr-Projects-foo
        parts = fallback_dir_name.split("-")
        return parts[-1] if parts else fallback_dir_name
    return None


def iter_claude_records(jsonl_path: Path) -> Iterable[dict]:
    try:
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue
    except (OSError, UnicodeDecodeError):
        return


def extract_usage_row(rec: dict, fallback_project: str | None = None) -> dict | None:
    """Pull a single token_usage row dict out of a Claude Code transcript record.

    DEDUPLICATION NOTE: One API call can log MANY assistant entries in the JSONL
    (one per content block — text/tool_use/etc.) all sharing the same requestId.
    Each entry carries the AGGREGATED usage for the whole message, not the per-block
    usage. The DB has UNIQUE(request_id) so we keep only the first; the rest collide
    on insert and get silently skipped. Counting them all would over-count by ~2x.
    """
    if rec.get("type") != "assistant":
        return None
    msg = rec.get("message")
    if not isinstance(msg, dict):
        return None
    usage = msg.get("usage")
    if not isinstance(usage, dict):
        return None

    model = msg.get("model") or "unknown"
    in_t  = int(usage.get("input_tokens", 0) or 0)
    out_t = int(usage.get("output_tokens", 0) or 0)
    cw_t  = int(usage.get("cache_creation_input_tokens", 0) or 0)
    cr_t  = int(usage.get("cache_read_input_tokens", 0) or 0)

    # TTL split (87% of writes are 1hr in our usage; pricing differs significantly)
    cc = usage.get("cache_creation") or {}
    cw_5m = int(cc.get("ephemeral_5m_input_tokens", 0) or 0)
    cw_1h = int(cc.get("ephemeral_1h_input_tokens", 0) or 0)

    if in_t + out_t + cw_t + cr_t == 0:
        return None

    cost = calc_cost(
        {"input_tokens": in_t, "output_tokens": out_t,
         "cache_creation_tokens": cw_t, "cache_read_tokens": cr_t,
         "cache_creation_5m_tokens": cw_5m, "cache_creation_1h_tokens": cw_1h},
        model,
    )

    project = project_tag_from_cwd(rec.get("cwd"), fallback_project)
    request_id = rec.get("requestId") or rec.get("uuid")  # uuid as fallback
    if not request_id:
        return None

    return {
        "timestamp": rec.get("timestamp") or datetime.now(timezone.utc).isoformat(),
        "provider": "anthropic",
        "model": model,
        "input_tokens": in_t,
        "output_tokens": out_t,
        "cache_creation_tokens": cw_t,
        "cache_creation_5m_tokens": cw_5m,
        "cache_creation_1h_tokens": cw_1h,
        "cache_read_tokens": cr_t,
        "cost_usd": round(cost, 6),
        "project_tag": project,
        "session_id": rec.get("sessionId"),
        "request_id": request_id,
        "source": "claude_code_log",
    }


def insert_rows(conn: sqlite3.Connection, rows: list[dict]) -> int:
    if not rows:
        return 0
    inserted = 0
    cur = conn.cursor()
    for r in rows:
        try:
            cur.execute(
                """
                INSERT INTO token_usage
                  (timestamp, provider, model, input_tokens, output_tokens,
                   cache_creation_tokens, cache_creation_5m_tokens, cache_creation_1h_tokens,
                   cache_read_tokens, cost_usd,
                   project_tag, session_id, request_id, source)
                VALUES (:timestamp, :provider, :model, :input_tokens, :output_tokens,
                        :cache_creation_tokens, :cache_creation_5m_tokens, :cache_creation_1h_tokens,
                        :cache_read_tokens, :cost_usd,
                        :project_tag, :session_id, :request_id, :source)
                """,
                r,
            )
            inserted += 1
        except sqlite3.IntegrityError:
            pass  # duplicate request_id — skip
    conn.commit()
    return inserted


def sync_claude_code_logs(verbose: bool = False) -> dict:
    """Scan ~/.claude/projects/**/*.jsonl and import all assistant token usage."""
    if not CLAUDE_PROJECTS_DIR.exists():
        return {"source": "claude_code_log", "files_scanned": 0, "rows_added": 0,
                "note": f"directory not found: {CLAUDE_PROJECTS_DIR}"}

    conn = init_db()
    files_scanned = 0
    rows_added = 0

    for jsonl in CLAUDE_PROJECTS_DIR.rglob("*.jsonl"):
        files_scanned += 1
        proj_dir_name = None
        try:
            proj_dir_name = jsonl.relative_to(CLAUDE_PROJECTS_DIR).parts[0]
        except (ValueError, IndexError):
            pass

        batch: list[dict] = []
        for rec in iter_claude_records(jsonl):
            row = extract_usage_row(rec, fallback_project=proj_dir_name)
            if row:
                batch.append(row)
        n = insert_rows(conn, batch)
        rows_added += n
        if verbose and n:
            print(f"  + {n:4d} rows from {jsonl.name}")

    record_sync("claude_code_log", rows_added,
                note=f"scanned {files_scanned} jsonl files")
    return {"source": "claude_code_log", "files_scanned": files_scanned,
            "rows_added": rows_added}


def sync_anthropic_admin(verbose: bool = False) -> dict:
    """Pull org-level usage from Anthropic Admin API. Requires ANTHROPIC_ADMIN_KEY env var."""
    key = os.environ.get("ANTHROPIC_ADMIN_KEY")
    if not key:
        return {"source": "anthropic_admin", "rows_added": 0,
                "note": "ANTHROPIC_ADMIN_KEY not set — skipped"}

    try:
        import urllib.request
        import urllib.error
    except ImportError:
        return {"source": "anthropic_admin", "rows_added": 0, "note": "urllib unavailable"}

    # Anthropic Admin Usage API — last 7 days, daily granularity
    end = datetime.now(timezone.utc).date()
    from datetime import timedelta
    start = end - timedelta(days=7)
    url = (
        "https://api.anthropic.com/v1/organizations/usage_report/messages"
        f"?starting_at={start.isoformat()}T00:00:00Z"
        f"&ending_at={end.isoformat()}T23:59:59Z"
        "&bucket_width=1d"
    )
    req = urllib.request.Request(
        url,
        headers={
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"source": "anthropic_admin", "rows_added": 0,
                "note": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"source": "anthropic_admin", "rows_added": 0, "note": f"error: {e}"}

    conn = init_db()
    rows = []
    for bucket in data.get("data", []):
        ts = bucket.get("starting_at") or bucket.get("ending_at") or datetime.now(timezone.utc).isoformat()
        for result in bucket.get("results", []):
            model = result.get("model", "unknown")
            in_t = int(result.get("uncached_input_tokens", 0) or 0)
            out_t = int(result.get("output_tokens", 0) or 0)
            cw_t = int(result.get("cache_creation_input_tokens", 0) or 0)
            cr_t = int(result.get("cache_read_input_tokens", 0) or 0)
            if in_t + out_t + cw_t + cr_t == 0:
                continue
            cost = calc_cost(
                {"input_tokens": in_t, "output_tokens": out_t,
                 "cache_creation_tokens": cw_t, "cache_read_tokens": cr_t},
                model,
            )
            request_id = f"admin:{ts}:{model}"
            rows.append({
                "timestamp": ts,
                "provider": "anthropic",
                "model": model,
                "input_tokens": in_t,
                "output_tokens": out_t,
                "cache_creation_tokens": cw_t,
                "cache_creation_5m_tokens": 0,
                "cache_creation_1h_tokens": 0,
                "cache_read_tokens": cr_t,
                "cost_usd": round(cost, 6),
                "project_tag": "admin-api",
                "session_id": None,
                "request_id": request_id,
                "source": "anthropic_admin",
            })

    n = insert_rows(conn, rows)
    record_sync("anthropic_admin", n, note=f"fetched {len(rows)} buckets")
    return {"source": "anthropic_admin", "rows_added": n,
            "buckets": len(rows)}


def record_sync(source: str, rows_added: int, note: str = "") -> None:
    conn = init_db()
    conn.execute(
        """
        INSERT INTO sync_state (source, last_synced_at, rows_added, note)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(source) DO UPDATE SET
          last_synced_at = excluded.last_synced_at,
          rows_added     = excluded.rows_added,
          note           = excluded.note
        """,
        (source, datetime.now(timezone.utc).isoformat(timespec="seconds"), rows_added, note),
    )
    conn.commit()


def get_sync_status() -> list[dict]:
    conn = init_db()
    cur = conn.execute(
        "SELECT source, last_synced_at, rows_added, note FROM sync_state ORDER BY source"
    )
    return [
        {"source": r[0], "last_synced_at": r[1], "rows_added": r[2], "note": r[3]}
        for r in cur.fetchall()
    ]


def sync_all(verbose: bool = False) -> list[dict]:
    return [
        sync_claude_code_logs(verbose=verbose),
        sync_anthropic_admin(verbose=verbose),
    ]


if __name__ == "__main__":
    print("Running sync_all...")
    for r in sync_all(verbose=True):
        print(r)
