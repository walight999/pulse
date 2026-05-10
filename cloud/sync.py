"""Cloud sync — push/pull encrypted changes — Phase 1 stub.

Sync model: last-write-wins by `updated_at`, per row, per workspace.
Conflict resolution surfaces both versions to the user when timestamps tie.

When implemented, runs every 60s in app.py background_sync_loop().
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SyncDelta:
    table: str           # 'subscriptions' | 'token_usage' | 'app_activity'
    row_id: str          # local UUID
    encrypted_blob: bytes
    encrypted_meta: dict # hashed-fields-for-server-side-filter
    updated_at: str
    deleted: bool = False


def push_changes(jwt: str, workspace_id: str, deltas: list[SyncDelta]) -> dict:
    """POST changes to server. Returns {accepted: N, rejected: [...]}."""
    raise NotImplementedError("Phase 1 — POST /sync/push")


def pull_changes(jwt: str, workspace_id: str, since: str) -> list[SyncDelta]:
    """GET changes newer than `since`."""
    raise NotImplementedError("Phase 1 — GET /sync/pull")


def merge_into_local(deltas: list[SyncDelta]) -> int:
    """Decrypt + apply server changes to local SQLite. Returns rows affected."""
    raise NotImplementedError("Phase 1 — call cloud.crypto.decrypt then UPDATE")


def collect_local_changes(since: str) -> list[SyncDelta]:
    """Read local rows updated since `since`, encrypt them into deltas."""
    raise NotImplementedError("Phase 1 — query local DB + cloud.crypto.encrypt")
