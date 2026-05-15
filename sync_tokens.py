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


def sync_openai(verbose: bool = False) -> dict:
    """Pull OpenAI API usage via /v1/usage. Requires `openai_api_key` setting (sk-...)."""
    try:
        from db import get_setting
        api_key = (get_setting("openai_api_key", "") or "").strip()
    except Exception:
        api_key = ""

    if not api_key or not api_key.startswith("sk-"):
        return {"source": "openai_api", "rows_added": 0,
                "note": "openai_api_key not set in Settings → Provider API keys"}

    try:
        from providers.openai_parser import sync_from_api as _openai_sync
    except Exception as e:
        return {"source": "openai_api", "rows_added": 0, "note": f"import error: {e}"}

    try:
        rows = _openai_sync(api_key)
    except Exception as e:
        return {"source": "openai_api", "rows_added": 0, "note": f"fetch error: {e}"}

    conn = init_db()
    n = insert_rows(conn, rows)
    record_sync("openai_api", n, note=f"fetched {len(rows)} day-model buckets")
    if verbose:
        print(f"  + {n} OpenAI usage rows (from {len(rows)} fetched)")
    return {"source": "openai_api", "rows_added": n, "fetched": len(rows)}


def sync_cursor(verbose: bool = False) -> dict:
    """Read Cursor IDE's local state DB and import chat-session usage rows."""
    try:
        from providers.cursor_parser import sync as _cursor_sync, is_cursor_installed
    except Exception as e:
        return {"source": "cursor_local", "rows_added": 0, "note": f"import error: {e}"}

    if not is_cursor_installed():
        return {"source": "cursor_local", "rows_added": 0,
                "note": "Cursor not installed (no state.vscdb found)"}

    try:
        rows = _cursor_sync()
    except Exception as e:
        return {"source": "cursor_local", "rows_added": 0, "note": f"parse error: {e}"}

    conn = init_db()
    n = insert_rows(conn, rows)
    record_sync("cursor_local", n, note=f"fetched {len(rows)} messages")
    if verbose:
        print(f"  + {n} Cursor rows (from {len(rows)} fetched)")
    return {"source": "cursor_local", "rows_added": n, "fetched": len(rows)}


def sync_copilot(verbose: bool = False) -> dict:
    """Pull GitHub Copilot org-level usage. Requires `copilot_github_token` + `copilot_org` settings."""
    try:
        from db import get_setting
        token = (get_setting("copilot_github_token", "") or "").strip()
        org   = (get_setting("copilot_org", "") or "").strip()
    except Exception:
        return {"source": "copilot_api", "rows_added": 0, "note": "settings read failed"}

    if not token or not org:
        return {"source": "copilot_api", "rows_added": 0,
                "note": "copilot_github_token + copilot_org not set (Settings → Provider API keys)"}

    try:
        from providers.copilot_parser import sync_from_github_api as _copilot_sync
    except Exception as e:
        return {"source": "copilot_api", "rows_added": 0, "note": f"import error: {e}"}

    try:
        rows = _copilot_sync(token, org=org)
    except Exception as e:
        return {"source": "copilot_api", "rows_added": 0, "note": f"fetch error: {e}"}

    conn = init_db()
    n = insert_rows(conn, rows)
    record_sync("copilot_api", n, note=f"fetched {len(rows)} day-buckets")
    if verbose:
        print(f"  + {n} Copilot rows (from {len(rows)} fetched)")
    return {"source": "copilot_api", "rows_added": n, "fetched": len(rows)}


def sync_chatgpt_export(zip_or_dir_path: str | Path, verbose: bool = False) -> dict:
    """Parse a ChatGPT 'Export Data' archive and insert message-count rows into token_usage.

    Path to the ZIP (or the unzipped folder) is passed in by the dashboard's file-uploader.
    Token counts are approximated from message character length (1 token ≈ 4 chars) since
    ChatGPT exports don't include token counts. Use the OpenAI API sync for exact figures.
    """
    try:
        from providers.openai_parser import parse_export_archive
    except Exception as e:
        return {"source": "chatgpt_export", "rows_added": 0, "note": f"import error: {e}"}

    target = Path(zip_or_dir_path) if not isinstance(zip_or_dir_path, Path) else zip_or_dir_path
    if not target.exists():
        return {"source": "chatgpt_export", "rows_added": 0,
                "note": f"path not found: {target}"}

    rows: list[dict] = []
    try:
        for row in parse_export_archive(target):
            rows.append(row)
    except Exception as e:
        return {"source": "chatgpt_export", "rows_added": 0, "note": f"parse error: {e}"}

    if not rows:
        return {"source": "chatgpt_export", "rows_added": 0,
                "note": "no assistant messages found in export"}

    conn = init_db()
    n = insert_rows(conn, rows)
    record_sync("chatgpt_export", n,
                note=f"parsed {len(rows)} messages from {target.name}")
    if verbose:
        print(f"  + {n} ChatGPT export rows (from {len(rows)} parsed)")
    return {"source": "chatgpt_export", "rows_added": n, "fetched": len(rows)}


def sync_gemini(verbose: bool = False) -> dict:
    """Validate Gemini API key. Google AI Studio doesn't expose retrospective usage —
    pulse tracks Gemini going forward via the browser extension (if installed)."""
    try:
        from db import get_setting
        api_key = (get_setting("gemini_api_key", "") or "").strip()
    except Exception:
        api_key = ""

    if not api_key:
        return {"source": "gemini_api", "rows_added": 0,
                "note": "gemini_api_key not set"}

    try:
        from providers.gemini_parser import validate_api_key as _gemini_validate
        ok = _gemini_validate(api_key)
    except Exception as e:
        return {"source": "gemini_api", "rows_added": 0, "note": f"validate error: {e}"}

    note = "key validated; Google AI Studio has no retrospective usage API — install the browser extension to capture Gemini sessions going forward" if ok else "key invalid"
    record_sync("gemini_api", 0, note=note)
    return {"source": "gemini_api", "rows_added": 0, "note": note}


def sync_all(verbose: bool = False) -> list[dict]:
    return [
        sync_claude_code_logs(verbose=verbose),
        sync_anthropic_admin(verbose=verbose),
        sync_openai(verbose=verbose),
        sync_cursor(verbose=verbose),
        sync_copilot(verbose=verbose),
        sync_gemini(verbose=verbose),
    ]


if __name__ == "__main__":
    print("Running sync_all...")
    for r in sync_all(verbose=True):
        print(r)
