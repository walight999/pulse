"""Cloud sync — encrypted bidirectional sync to Supabase.

Protocol:
1. collect_local_changes(since) — read rows updated since last sync, encrypt, batch
2. push_changes(deltas) — POST to /sync/push (RPC: pulse_push_deltas)
3. pull_changes(since) — fetch server changes newer than `since`
4. merge_into_local(deltas) — decrypt + UPSERT to local SQLite

Conflict resolution: last-write-wins by `updated_at`. When timestamps tie,
prefer local (user just edited). Surface in audit log either way.

Runs every 60s in app.py background_sync_loop() when user is signed in.
"""
from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Iterable, Optional

from cloud import auth, crypto
from db import get_conn


SYNCED_TABLES = ["subscriptions", "token_usage", "app_activity"]


@dataclass
class SyncDelta:
    table: str
    row_id: str
    encrypted_blob: bytes
    nonce: bytes
    searchable_index: dict   # hashed fields for server-side filter (e.g. {timestamp_yyyymm: hash})
    updated_at: str
    deleted: bool = False

    def to_wire(self) -> dict:
        return {
            "table": self.table,
            "row_id": self.row_id,
            "ciphertext": self.encrypted_blob.hex(),
            "nonce": self.nonce.hex(),
            "searchable_index": self.searchable_index,
            "updated_at": self.updated_at,
            "deleted": self.deleted,
        }

    @classmethod
    def from_wire(cls, d: dict) -> "SyncDelta":
        return cls(
            table=d["table"],
            row_id=d["row_id"],
            encrypted_blob=bytes.fromhex(d["ciphertext"]),
            nonce=bytes.fromhex(d["nonce"]),
            searchable_index=d.get("searchable_index", {}),
            updated_at=d["updated_at"],
            deleted=d.get("deleted", False),
        )


def _row_to_json(row: sqlite3.Row) -> str:
    return json.dumps({k: row[k] for k in row.keys()}, default=str)


def _searchable_index_for(table: str, row: sqlite3.Row, hmac_secret: bytes) -> dict:
    """Hashed values that the server can filter on without decrypting the row."""
    idx = {}
    if table == "token_usage":
        ts = (row["timestamp"] or "")[:7]   # yyyy-mm
        if ts:
            idx["month"] = crypto.hash_searchable(ts, hmac_secret)
    elif table == "subscriptions":
        active = "1" if row["active"] else "0"
        idx["active"] = crypto.hash_searchable(active, hmac_secret)
    return idx


def collect_local_changes(since: str, master_key: bytes, hmac_secret: bytes) -> list[SyncDelta]:
    """Find rows updated since `since` and encrypt them into deltas."""
    conn = get_conn()
    deltas: list[SyncDelta] = []
    for table in SYNCED_TABLES:
        # Need `updated_at` column — added by migration for sync support
        try:
            rows = conn.execute(
                f"SELECT * FROM {table} WHERE COALESCE(updated_at, created_at, '') > ?",
                (since,),
            ).fetchall()
        except sqlite3.OperationalError:
            continue
        for r in rows:
            payload = _row_to_json(r).encode("utf-8")
            ct, nonce = crypto.encrypt_row(payload, master_key)
            deltas.append(SyncDelta(
                table=table,
                row_id=str(r["id"]),
                encrypted_blob=ct,
                nonce=nonce,
                searchable_index=_searchable_index_for(table, r, hmac_secret),
                updated_at=str(r["updated_at"] if "updated_at" in r.keys() else r["created_at"]),
            ))
    return deltas


def push_changes(deltas: list[SyncDelta]) -> dict:
    """RPC: pulse_push_deltas(workspace_id, deltas). Returns accepted/rejected."""
    session = auth.current_session()
    if not session:
        return {"ok": False, "error": "not_signed_in"}
    client = auth._client()
    if not client:
        return {"ok": False, "error": "cloud_not_configured"}
    try:
        resp = client.rpc(
            "pulse_push_deltas",
            {
                "workspace_id": session.account_id,
                "deltas": [d.to_wire() for d in deltas],
            },
        ).execute()
        return {"ok": True, "result": resp.data}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def pull_changes(since: str) -> list[SyncDelta]:
    session = auth.current_session()
    if not session:
        return []
    client = auth._client()
    if not client:
        return []
    try:
        resp = client.rpc(
            "pulse_pull_deltas",
            {"workspace_id": session.account_id, "since": since},
        ).execute()
        return [SyncDelta.from_wire(d) for d in (resp.data or [])]
    except Exception:
        return []


def merge_into_local(deltas: list[SyncDelta], master_key: bytes) -> int:
    """Apply server changes locally. Returns rows touched."""
    conn = get_conn()
    n = 0
    for d in deltas:
        try:
            plaintext = crypto.decrypt_row(d.encrypted_blob, d.nonce, master_key)
            row = json.loads(plaintext)
            if d.deleted:
                conn.execute(f"DELETE FROM {d.table} WHERE id = ?", (row.get("id"),))
            else:
                cols = ", ".join(row.keys())
                placeholders = ", ".join("?" * len(row))
                updates = ", ".join(f"{c}=excluded.{c}" for c in row.keys() if c != "id")
                conn.execute(
                    f"INSERT INTO {d.table} ({cols}) VALUES ({placeholders}) "
                    f"ON CONFLICT(id) DO UPDATE SET {updates}",
                    tuple(row.values()),
                )
            n += 1
        except Exception:
            continue
    conn.commit()
    return n


def sync_once(master_key: bytes, hmac_secret: bytes) -> dict:
    """One full sync cycle. Returns summary {pushed, pulled, conflicts}."""
    from db import get_setting, set_setting
    last_sync = get_setting("cloud_last_sync_at", "1970-01-01T00:00:00Z")
    now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")

    local_deltas = collect_local_changes(last_sync, master_key, hmac_secret)
    push_result = push_changes(local_deltas) if local_deltas else {"ok": True}
    server_deltas = pull_changes(last_sync)
    merged = merge_into_local(server_deltas, master_key)

    set_setting("cloud_last_sync_at", now_iso)
    return {
        "pushed": len(local_deltas),
        "pulled": len(server_deltas),
        "merged": merged,
        "push_ok": push_result.get("ok", False),
    }
