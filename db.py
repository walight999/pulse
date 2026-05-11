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
    # Phase B — sync support: every table needs updated_at for delta sync
    "ALTER TABLE subscriptions ADD COLUMN updated_at TEXT",
    "ALTER TABLE token_usage ADD COLUMN updated_at TEXT",
    "ALTER TABLE app_activity ADD COLUMN updated_at TEXT",
    "ALTER TABLE subscriptions ADD COLUMN provider TEXT",   # 'openai' | 'anthropic' | 'cursor' | etc.
    # Phase B — audit log (security + compliance)
    """CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        actor TEXT,                    -- 'local-user' | <account_id> | 'system'
        action TEXT NOT NULL,          -- 'signin' | 'signout' | 'api_key_create' | 'export' | etc.
        target TEXT,                   -- entity touched (sub id, project, etc.)
        details TEXT,                  -- JSON blob with relevant context
        ip TEXT,
        user_agent TEXT
    )""",
    "CREATE INDEX IF NOT EXISTS idx_audit_ts ON audit_log(timestamp DESC)",
    "CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_log(action)",
    # Phase B — cloud sync state per workspace
    """CREATE TABLE IF NOT EXISTS cloud_state (
        workspace_id TEXT PRIMARY KEY,
        last_sync_at TEXT,
        sync_status TEXT,              -- 'synced' | 'pending' | 'error'
        last_error TEXT,
        rows_pushed INTEGER DEFAULT 0,
        rows_pulled INTEGER DEFAULT 0
    )""",
    # Phase B — friend invites (for leaderboard)
    """CREATE TABLE IF NOT EXISTS friend_invites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,
        issued_by TEXT NOT NULL,
        issued_at TEXT DEFAULT CURRENT_TIMESTAMP,
        redeemed_by TEXT,
        redeemed_at TEXT
    )""",
    "CREATE INDEX IF NOT EXISTS idx_friend_code ON friend_invites(code)",
    # Phase B — API keys for Pulse SDK + 3rd party
    """CREATE TABLE IF NOT EXISTS api_keys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key_prefix TEXT NOT NULL,      -- first 8 chars for display, e.g. 'pk_live_...'
        key_hash TEXT UNIQUE NOT NULL, -- SHA-256 of full key (never store plaintext)
        label TEXT,                    -- user-supplied
        scopes TEXT DEFAULT 'read',    -- comma-separated: 'read,write,leaderboard'
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        last_used_at TEXT,
        revoked_at TEXT
    )""",
    "CREATE INDEX IF NOT EXISTS idx_apikey_hash ON api_keys(key_hash)",
    # Phase B — webhook integrations
    """CREATE TABLE IF NOT EXISTS integrations_webhooks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kind TEXT NOT NULL,            -- 'slack' | 'teams' | 'discord' | 'generic'
        url TEXT NOT NULL,
        events TEXT,                   -- comma-separated event types
        enabled INTEGER DEFAULT 1,
        last_sent_at TEXT,
        last_status INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""",
]


def log_audit(action: str, actor: str = "local-user",
              target: str | None = None, details: dict | None = None,
              ip: str | None = None, user_agent: str | None = None) -> None:
    """Append an entry to the audit log. Use for security-relevant events."""
    import json as _json
    conn = get_conn()
    conn.execute(
        "INSERT INTO audit_log (actor, action, target, details, ip, user_agent) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (actor, action, target,
         _json.dumps(details) if details else None,
         ip, user_agent),
    )
    conn.commit()


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
