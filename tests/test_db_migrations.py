"""Test DB migrations — schema applies cleanly on fresh + existing DB.

Uses pytest's tmp_path fixture (Windows-friendly: pytest delays cleanup
past the test, so SQLite handles released by `db` module global state
won't conflict).
"""
import sqlite3
from unittest.mock import patch


def test_fresh_db_creates_all_tables(tmp_path):
    """Init on empty DB → all expected tables exist."""
    import db
    test_db = tmp_path / "test.db"
    with patch.object(db, "DB_PATH", test_db):
        db.init_db()
        conn = sqlite3.connect(test_db)
        try:
            tables = {r[0] for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()}
        finally:
            conn.close()
    expected = {
        "subscriptions", "app_activity", "system_snapshots", "token_usage",
        "sync_state", "app_settings", "app_categories", "alert_log",
        "backup_log", "audit_log", "cloud_state", "friend_invites",
        "api_keys", "integrations_webhooks",
    }
    missing = expected - tables
    assert not missing, f"Missing tables: {missing}"


def test_migrations_idempotent(tmp_path):
    """Running init_db twice → no errors."""
    import db
    test_db = tmp_path / "test.db"
    with patch.object(db, "DB_PATH", test_db):
        db.init_db()
        db.init_db()


def test_audit_log_helper(tmp_path):
    """db.log_audit() inserts a row with required fields."""
    import db
    test_db = tmp_path / "test.db"
    with patch.object(db, "DB_PATH", test_db):
        db.init_db()
        db.log_audit(action="test_event", actor="pytest",
                     details={"key": "value"})
        conn = sqlite3.connect(test_db)
        try:
            row = conn.execute(
                "SELECT actor, action, details "
                "FROM audit_log ORDER BY id DESC LIMIT 1"
            ).fetchone()
        finally:
            conn.close()
    assert row is not None
    assert row[0] == "pytest"
    assert row[1] == "test_event"
    assert "key" in row[2]
