"""SQLite schema and helpers for life-tracker."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "tracker.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS app_activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    process_name TEXT NOT NULL,
    window_title TEXT,
    duration_seconds INTEGER
);
CREATE INDEX IF NOT EXISTS idx_activity_started ON app_activity(started_at);
CREATE INDEX IF NOT EXISTS idx_activity_process ON app_activity(process_name);

CREATE TABLE IF NOT EXISTS system_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    process_name TEXT NOT NULL,
    cpu_pct REAL,
    memory_mb REAL
);
CREATE INDEX IF NOT EXISTS idx_snap_ts ON system_snapshots(timestamp);
CREATE INDEX IF NOT EXISTS idx_snap_proc ON system_snapshots(process_name);

CREATE TABLE IF NOT EXISTS subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cost REAL NOT NULL,
    currency TEXT DEFAULT 'USD',
    billing_cycle TEXT NOT NULL,
    next_billing_date TEXT,
    linked_process TEXT,
    notes TEXT,
    active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS token_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    provider TEXT NOT NULL,
    model TEXT,
    input_tokens INTEGER DEFAULT 0,
    output_tokens INTEGER DEFAULT 0,
    cache_creation_tokens INTEGER DEFAULT 0,
    cache_read_tokens INTEGER DEFAULT 0,
    cost_usd REAL DEFAULT 0,
    project_tag TEXT,
    session_id TEXT,
    request_id TEXT UNIQUE,
    source TEXT DEFAULT 'manual'
);
CREATE INDEX IF NOT EXISTS idx_token_ts ON token_usage(timestamp);
CREATE INDEX IF NOT EXISTS idx_token_project ON token_usage(project_tag);

CREATE TABLE IF NOT EXISTS sync_state (
    source TEXT PRIMARY KEY,
    last_synced_at TEXT NOT NULL,
    rows_added INTEGER DEFAULT 0,
    note TEXT
);

CREATE TABLE IF NOT EXISTS app_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS app_categories (
    process_name TEXT PRIMARY KEY,
    category TEXT NOT NULL,
    is_distraction INTEGER DEFAULT 0,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS alert_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kind TEXT NOT NULL,           -- 'renewal', 'spike', 'dead_sub', etc.
    target_id TEXT,               -- subscription id, etc.
    body TEXT NOT NULL,
    sent_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(kind, target_id, sent_at)
);

CREATE TABLE IF NOT EXISTS backup_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path TEXT NOT NULL,
    size_bytes INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


# Lightweight migrations for existing databases (idempotent — silently skip if column exists)
MIGRATIONS = [
    "ALTER TABLE token_usage ADD COLUMN cache_creation_tokens INTEGER DEFAULT 0",
    "ALTER TABLE token_usage ADD COLUMN cache_read_tokens INTEGER DEFAULT 0",
    "ALTER TABLE token_usage ADD COLUMN session_id TEXT",
    "ALTER TABLE token_usage ADD COLUMN request_id TEXT",
    "ALTER TABLE token_usage ADD COLUMN source TEXT DEFAULT 'manual'",
    "CREATE UNIQUE INDEX IF NOT EXISTS idx_token_request ON token_usage(request_id) WHERE request_id IS NOT NULL",
    # Subscription enrichment fields
    "ALTER TABLE subscriptions ADD COLUMN last_charge_date TEXT",
    "ALTER TABLE subscriptions ADD COLUMN last_charge_amount REAL",
    "ALTER TABLE subscriptions ADD COLUMN email_sender TEXT",
    "ALTER TABLE subscriptions ADD COLUMN user_confirmed_at TEXT",  # when user clicked "still active"
    # Token cache TTL split
    "ALTER TABLE token_usage ADD COLUMN cache_creation_5m_tokens INTEGER DEFAULT 0",
    "ALTER TABLE token_usage ADD COLUMN cache_creation_1h_tokens INTEGER DEFAULT 0",
    # New subscription power features (added during productization)
    "ALTER TABLE subscriptions ADD COLUMN cancel_url TEXT",
    "ALTER TABLE subscriptions ADD COLUMN tag TEXT",        # business / personal / family etc.
    "ALTER TABLE subscriptions ADD COLUMN is_trial INTEGER DEFAULT 0",
    "ALTER TABLE subscriptions ADD COLUMN trial_ends_at TEXT",
    # Savings tracking — captured at time of cancellation
    "ALTER TABLE subscriptions ADD COLUMN cancelled_at TEXT",
    "ALTER TABLE subscriptions ADD COLUMN cancelled_monthly_usd REAL",  # at-cancel monthly equiv
]


def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.executescript(SCHEMA)
    for stmt in MIGRATIONS:
        try:
            conn.execute(stmt)
        except sqlite3.OperationalError:
            pass  # column already exists
    conn.commit()
    return conn


def get_setting(key: str, default: str = "") -> str:
    conn = get_conn()
    row = conn.execute("SELECT value FROM app_settings WHERE key = ?", (key,)).fetchone()
    return row["value"] if row else default


def set_setting(key: str, value: str) -> None:
    conn = get_conn()
    conn.execute(
        "INSERT INTO app_settings (key, value) VALUES (?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value, "
        "updated_at = CURRENT_TIMESTAMP",
        (key, value),
    )
    conn.commit()


if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
