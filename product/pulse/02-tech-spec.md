# 🛠️ Pulse MVP — Technical Specification

**Status**: v1.5 production
**Owner**: White (@walight999)
**Last updated**: 2026-05-11

---

## 1. Architecture overview

Pulse is a local-first Python application with optional cloud sync. Four layers:

1. **Tray + background daemons** (`app.py`) — system integration
2. **Dashboard UI** (`dashboard.py`) — Streamlit-based web view
3. **Domain modules** — `db.py`, `theme.py`, `quips.py`, `fx.py`, `notifications.py`, etc.
4. **Optional cloud** (`cloud/`, `api/`, `sdk/`) — Phase 2+

```
                   ┌─────────────────────────────────────────┐
                   │  Pulse desktop (Windows tray)            │
                   │                                          │
   ┌───────────┐   │  ┌──────────┐    ┌──────────────────┐  │
   │ Streamlit │◀──┤  │ app.py   │    │ background_*_loop│  │
   │ dashboard │   │  │ tray +   │    │  · sync (6h)     │  │
   │ (browser) │   │  │ daemons  │    │  · alerts (30m)  │  │
   └─────┬─────┘   │  └────┬─────┘    │  · backup (24h)  │  │
         │         │       │           │  · maintenance   │  │
         ▼         │       ▼           └──────────────────┘  │
   ┌─────────────┐ │  ┌─────────────┐                       │
   │ dashboard.py│◀┼──┤ db.py       │◀── ┌─────────────┐    │
   │ (UI render) │ │  │ SQLite      │    │ sync_tokens │    │
   └─────┬───────┘ │  │ tracker.db  │    │ parse jsonl │    │
         │         │  └─────────────┘    └─────────────┘    │
         ▼         │       │                                 │
   ┌─────────────┐ │       ▼                                 │
   │ theme.py    │ │  ┌─────────────┐                       │
   │ CSS vars    │ │  │ tracker.py  │                       │
   └─────────────┘ │  │ Win32 APIs  │                       │
                   │  │  · GetFG    │                       │
                   │  │  · idle     │                       │
                   │  └─────────────┘                       │
                   └─────────────────────────────────────────┘
                              │
                              │ (optional Phase 2)
                              ▼
                   ┌─────────────────────────────────────────┐
                   │  Pulse Cloud (Supabase + Stripe)         │
                   │  · cloud/auth.py    magic-link           │
                   │  · cloud/sync.py    E2E encrypted        │
                   │  · cloud/teams.py   shared dashboards    │
                   │  · api/server.py    REST API             │
                   └─────────────────────────────────────────┘
```

## 2. Tech stack

### Core (v1.0)

| Layer | Tech | Version | Why |
|-------|------|---------|-----|
| UI framework | Streamlit | 1.57 | Rapid dashboard iteration, Python-native |
| Database | SQLite | (built-in) | Local, zero-setup, supports rich queries |
| Charts | Plotly | 5.18 | Themeable, supports custom palettes |
| Process management | pystray | 0.19 | Cross-platform tray (Win primary) |
| HTTP requests | stdlib urllib | (built-in) | No requests dep for core |
| FX rates | frankfurter.dev | (free) | ECB rates, no API key |
| Pricing | Anthropic public | (hardcoded) | Sync_tokens.py PRICING dict |

### Optional cloud stack (v2.0+)

| Layer | Tech | Why |
|-------|------|-----|
| Auth | Supabase Auth | Magic link, JWT, free tier |
| Database | Supabase Postgres | Row-Level Security, free tier |
| Encryption | cryptography (PyCA) + argon2-cffi | Audited AES-GCM + Argon2id |
| API | FastAPI + uvicorn | Modern Python, OpenAPI auto |
| Billing | Stripe | Standard PCI-compliant |
| Reports | reportlab | PDF generation |
| Banks | Plaid (US) | Industry-standard aggregator |

### Frontend

| Touchpoint | Tech | Notes |
|------------|------|-------|
| Streamlit dashboard | Streamlit + custom CSS | Theme via CSS variables |
| Landing page | Next.js 14 (App Router) | Tailwind, Vercel deploy |
| Browser extension | Manifest V3 JS | Chrome + Edge first, Firefox skipped |
| Mobile | PWA (manifest.json + service worker) | iOS/Android home-screen install |

## 3. Database schema

### Tables

```sql
-- subscriptions
CREATE TABLE subscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cost REAL NOT NULL,
    currency TEXT DEFAULT 'USD',
    billing_cycle TEXT NOT NULL,
    next_billing_date TEXT,
    last_charge_date TEXT,
    last_charge_amount REAL,
    linked_process TEXT,
    notes TEXT,
    cancel_url TEXT,
    tag TEXT,
    is_trial INTEGER DEFAULT 0,
    trial_ends_at TEXT,
    email_sender TEXT,
    user_confirmed_at TEXT,
    cancelled_at TEXT,
    cancelled_monthly_usd REAL,
    provider TEXT,
    active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT
);

-- token_usage
CREATE TABLE token_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    provider TEXT NOT NULL,
    model TEXT,
    input_tokens INTEGER DEFAULT 0,
    output_tokens INTEGER DEFAULT 0,
    cache_creation_tokens INTEGER DEFAULT 0,
    cache_creation_5m_tokens INTEGER DEFAULT 0,
    cache_creation_1h_tokens INTEGER DEFAULT 0,
    cache_read_tokens INTEGER DEFAULT 0,
    cost_usd REAL DEFAULT 0,
    project_tag TEXT,
    session_id TEXT,
    request_id TEXT UNIQUE,  -- dedupe key
    source TEXT DEFAULT 'manual',
    updated_at TEXT
);

-- app_activity
CREATE TABLE app_activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    process_name TEXT NOT NULL,
    window_title TEXT,
    duration_seconds INTEGER,
    updated_at TEXT
);

-- system_snapshots, app_categories, app_settings, alert_log, backup_log,
-- audit_log, cloud_state, friend_invites, api_keys, integrations_webhooks
-- (full schema in db.py)
```

### Migrations

All migrations are idempotent ALTER TABLE statements in `db.py:MIGRATIONS`. On every startup:

1. `executescript(SCHEMA)` — creates missing tables
2. For each migration: try execute, silently skip if column exists

This makes schema evolution safe for existing users without explicit migration tracking.

## 4. Module responsibilities

### Single-purpose modules

| Module | Responsibility |
|--------|---------------|
| `app.py` | System tray + 4 background daemons + Streamlit launcher |
| `dashboard.py` | All UI rendering (5 pages) |
| `db.py` | SQLite schema + migrations + setting helpers + audit log |
| `theme.py` | Light/dark CSS variable system |
| `tracker.py` | Foreground app + idle detection (Win32 APIs) |
| `sync_tokens.py` | Claude Code log parser + accurate pricing |
| `fx.py` | frankfurter.dev FX rates with 24h cache |
| `notifications.py` | Windows toast via PowerShell + Windows.UI.Notifications |
| `backup.py` | SQLite backup API with rotation |
| `alerts.py` | Renewal + cost spike + dead-sub alert logic |
| `categories.py` | App categorization rules |
| `quips.py` | Playful one-liners (seeded for daily stability) |
| `export.py` | CSV + ZIP + PDF generation |
| `discover_subscriptions.py` | Gmail receipt parsing via Gmail MCP |
| `ics_export.py` | Calendar (.ics) export for renewals |
| `platform_compat.py` | Win + macOS + Linux shims (foreground, idle, toast) |

### Cloud modules (v2.0+, scaffolded today)

| Module | Responsibility |
|--------|---------------|
| `cloud/auth.py` | Supabase Auth magic-link flow |
| `cloud/crypto.py` | AES-256-GCM + Argon2id E2E encryption |
| `cloud/sync.py` | Encrypted bidirectional sync protocol |
| `cloud/leaderboard.py` | 5-category ranking computation |
| `cloud/teams.py` | Team workspaces + RBAC |
| `cloud/sso.py` | SAML/OIDC for enterprise |
| `cloud/billing.py` | Stripe Checkout integration |

### Integration modules (v1.0 webhook senders; bank stub in v1.5)

| Module | Responsibility |
|--------|---------------|
| `integrations/slack.py` | Block Kit webhook sender |
| `integrations/teams.py` | Adaptive Card webhook sender |
| `integrations/discord.py` | Embed webhook sender |
| `integrations/plaid_stub.py` | Plaid bank integration (v1.5) |

### Provider parsers (v1.1)

| Module | Responsibility |
|--------|---------------|
| `providers/openai_parser.py` | ChatGPT API + Plus subscription detection |
| `providers/cursor_parser.py` | Cursor IDE local state DB parsing |
| `providers/gemini_parser.py` | Google AI Studio + Gemini app |
| `providers/copilot_parser.py` | GitHub Copilot via GraphQL audit |

## 5. Key algorithms

### Plan ROI computation

```python
roi = api_equivalent_cost_usd / plan_cost_usd
# 5-tier classification:
# ≥10x → "Legendary value" (Top 1%)
# ≥5x  → "Excellent value" (Power user)
# ≥2x  → "Great value" (Smart spender)
# ≥1x  → "Plan paying off" (Break-even)
# ≥0.5x → "Underused"
# <0.5x → "Plan idle" (Consider downgrading)
```

### Claude cache TTL pricing

Per Anthropic docs, cache_creation tokens have two flavors:

- `ephemeral_5m_input_tokens` charged at **1.25× input rate** (5-min TTL)
- `ephemeral_1h_input_tokens` charged at **2× input rate** (1-hour TTL)

Most tools use one flat rate (1.25×) which under-prices long-lived caches by ~11% on heavy users. Pulse splits these correctly in `sync_tokens.py:PRICING`.

### Request deduplication

Multi-block Claude messages share a `request_id`. `sync_tokens.py` enforces UNIQUE constraint on `request_id`, avoiding ~5-15% double-counting that naive parsers produce.

### Smart status (subscription)

```
if no cost set → "blue" (cost-not-set, needs user input)
elif active=0 → "gray" (historical)
elif last_charge_date older than 60 days AND cycle=monthly →
    if cycle yearly fits → "blue" (reclassify suggestion)
    else → "red" (likely cancelled)
elif last_charge_date within 7 days of expected → "green" (active)
elif renewal in past + < 14 days late → "amber" (verify)
else → "green"
```

### Cost-per-hour-of-use

```python
hours_30d = sum(app_activity.duration_seconds where process_name = linked_process, last 30 days) / 3600
cost_per_hour = monthly_equivalent_usd / hours_30d
```

Surfaced under each linked subscription card.

## 6. Performance targets

| Operation | Target | Actual (measured) |
|-----------|--------|-------------------|
| Dashboard initial load | <2s | ~1.4s |
| Page navigation | <100ms (cached) | ~80ms |
| Theme toggle | <250ms | ~180ms (CSS-only, no cache clear) |
| Claude log sync (full) | <30s for 10k entries | ~12s on dev machine |
| CSV export | <2s for 50k rows | <1s |
| PDF export | <5s (single month) | ~3s (with reportlab) |
| Idle detection accuracy | ±2s | <1s in testing |

## 7. Privacy + security

See `SECURITY.md` for full threat model.

Key invariants:

- **Local-first**: zero network calls except optional FX + opt-in Gmail MCP
- **E2E encryption**: master key derived via Argon2id from password + account_id salt, never sent to server
- **Audit log**: every security event tracked in `audit_log` table
- **No telemetry**: zero analytics, zero pings
- **Open source**: MIT licensed, full source auditable

## 8. Deployment

### v1.0 desktop

Users `git clone` + `pip install -r requirements.txt` + `python app.py`. Future: bundled installer via PyInstaller.

### Landing page (Vercel)

```bash
cd landing && vercel --prod
# Custom domain: mintforai.com
```

### REST API (Phase 2)

Cloudflare Workers or Fly.io. JWT auth via Supabase. CORS configured for mintforai.com + Pro mobile.

### Browser extension

Chrome Web Store: $5 fee + ~7-14 day review.
Edge Add-ons: free + ~3-5 day review.
Firefox skipped (would need MV2 fork).

## 9. Testing strategy

- **Unit**: not yet (priority TODO for v1.1)
- **Manual**: full UI walkthrough each release
- **Cold install**: fresh Windows VM before each launch
- **Cross-platform**: macOS + Linux blocked on Mac access

## 10. Known limitations / debt

- No formal test suite (pytest skeleton TODO)
- Streamlit reruns full script on every interaction (not ideal but acceptable at our scale)
- Win32 APIs only — macOS / Linux ports verified but untested on real hardware
- Gmail MCP requires user to have Claude Desktop with Gmail MCP enabled
- ChatGPT Plus has no API for usage; relies on browser extension for capture
