# Pulse — Roadmap & architecture

This document describes what Pulse will become and how to build it.

Phase 0 (current local-only release) is complete. Phases 1–4 require
external infrastructure (a cloud backend, Stripe account, mobile app
build pipeline, OAuth credentials) that the local app cannot provision
on its own. This file is the spec — any developer with those external
accounts can pick it up and build.

---

## Phase 1 — Auth + cloud sync + payment

**Goal:** Pro tier launches. Users can pay $9/mo, sign in, and have
their Pulse data synced to a server (encrypted), accessible from a web
dashboard at pulse.app.

### 1.1 Backend stack

Recommended:
- **Supabase** (Postgres + Auth + Storage + Edge Functions)
  - Free tier handles ~50K MAU
  - Built-in Row-Level Security (RLS) for multi-tenant isolation
  - JWT-based auth lines up with Pulse desktop client
- Alternative: Cloudflare Workers + D1 + Auth0 + KV
- Self-host alternative: Postgres on Hetzner / Fly.io + custom auth

### 1.2 Cloud database schema (Postgres)

```sql
-- accounts (one row per signed-up user)
CREATE TABLE accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    pulse_account_id UUID UNIQUE NOT NULL,  -- migrated from local UUID
    plan TEXT NOT NULL DEFAULT 'free',       -- 'free' | 'pro' | 'team'
    stripe_customer_id TEXT UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    pro_until TIMESTAMPTZ,
    referral_code TEXT UNIQUE NOT NULL,
    referred_by UUID REFERENCES accounts(id)
);

-- workspaces (1 per account for Pro; multi-user for Team)
CREATE TABLE workspaces (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    owner_id UUID REFERENCES accounts(id) NOT NULL,
    plan TEXT NOT NULL DEFAULT 'pro',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE workspace_members (
    workspace_id UUID REFERENCES workspaces(id),
    account_id UUID REFERENCES accounts(id),
    role TEXT NOT NULL,  -- 'admin' | 'member' | 'viewer'
    PRIMARY KEY (workspace_id, account_id)
);

-- subscriptions, encrypted client-side
CREATE TABLE subscriptions_enc (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id UUID REFERENCES workspaces(id) NOT NULL,
    encrypted_blob BYTEA NOT NULL,            -- AES-GCM ciphertext of full row
    encrypted_meta JSONB,                     -- searchable hashes for filtering
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

CREATE INDEX idx_subs_workspace ON subscriptions_enc(workspace_id);
CREATE INDEX idx_subs_updated ON subscriptions_enc(workspace_id, updated_at);

-- token_usage and app_activity follow the same encrypted-blob pattern
-- (same workspace_id + encrypted_blob + meta hashes for filtering)

-- audit log (Team feature)
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    workspace_id UUID REFERENCES workspaces(id),
    actor_id UUID REFERENCES accounts(id),
    action TEXT NOT NULL,
    target_id TEXT,
    metadata JSONB,
    at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS policies
ALTER TABLE subscriptions_enc ENABLE ROW LEVEL SECURITY;
CREATE POLICY "members can read their workspace subs"
  ON subscriptions_enc FOR SELECT
  USING (workspace_id IN (
    SELECT workspace_id FROM workspace_members WHERE account_id = auth.uid()
  ));
-- (similar policies for INSERT/UPDATE/DELETE and other tables)
```

### 1.3 End-to-end encryption

**Key derivation (client-side):**
- User chooses a master password at first cloud sign-in
- Derive a 256-bit key with Argon2id (m=64MB, t=3, p=1) using the user's UUID as salt
- Store the *encrypted* master key (encrypted with a password-derived KEK) on the server, so it can be retrieved on a new device

**Per-row encryption:**
- Each subscription row is serialized to JSON
- Encrypted with AES-256-GCM using the master key
- A 12-byte nonce is generated per row, stored alongside the ciphertext
- Searchable fields (e.g., name) are hashed with HMAC-SHA-256 + secret prefix → `encrypted_meta` (so server can filter without decrypting)

The server **must never** see the master key or its password. If the user
loses both, their data is unrecoverable. Make this very loud in the UI.

### 1.4 Sync protocol

Background daemon in `app.py` runs every 60s when Pro:
1. POST `/sync/changes` with `{since: <last_synced_at>, changes: [...]}`
2. Server returns: `{server_changes: [...], conflicts: [...]}`
3. Client merges (last-write-wins per row by `updated_at`)
4. Update local `last_synced_at`

Conflict resolution: `updated_at` is authoritative. Show user a "conflict
detected" notification with an option to view both versions.

### 1.5 Stripe integration

**Products:**
- `pulse_pro_monthly` — $9.00/mo recurring
- `pulse_pro_annual` — $89.00/yr recurring (15% off)
- `pulse_pro_lifetime` — $199.00 one-time (limited launch tier)
- `pulse_team_seat` — $19.00/mo per seat

**Webhook events to handle:**
- `customer.subscription.created` → set `account.plan = 'pro'`, `pro_until = +1mo`
- `customer.subscription.updated` → extend `pro_until` on renewal
- `customer.subscription.deleted` → at end of period, downgrade to `free`
- `invoice.payment_failed` → grace period 7 days, then downgrade
- `customer.deleted` → mark account inactive, keep data 30 days

**In-app upgrade flow:**
1. User clicks "Upgrade" in Settings
2. Redirect to Stripe Checkout (hosted) with `client_reference_id = pulse_account_id`
3. Stripe Checkout completes → webhook fires → server records `pro_until`
4. App polls `/account/me` every 5s after redirect; updates UI when plan flips

### 1.6 New stub modules in code

These already-empty interfaces should be implemented in Phase 1:

- `cloud/auth.py` — sign-up, sign-in, JWT refresh
- `cloud/sync.py` — push/pull changes
- `cloud/crypto.py` — Argon2id + AES-GCM
- `cloud/billing.py` — Stripe customer + subscription helpers

### 1.7 Acceptance criteria

- [ ] User can sign up with email + master password
- [ ] User can subscribe to Pro via Stripe Checkout
- [ ] Local data encrypts and uploads to server within 60s of changes
- [ ] User can sign in on a 2nd machine, install Pulse, see same data after first sync
- [ ] Cancelling subscription downgrades to free at end of billing period
- [ ] All cloud data is unreadable to server admin (verified via test account)

**Estimated effort:** 8-12 weeks for one experienced full-stack dev.

---

## Phase 2 — Mobile companion + Gmail OAuth

**Goal:** iOS/Android app that shows your Pulse dashboard, sends push
notifications, and lets you add subscriptions on the go. Real Gmail
OAuth replaces the Claude-Code-chat dependency for subscription
discovery.

### 2.1 Mobile architecture

Recommended:
- **React Native (Expo)** — single codebase, fast iteration
  - Alternative: Flutter (better perf, separate codebase from Pulse desktop)

**Initial scope (read-mostly):**
- View dashboard (Overview, Subscriptions, Activity, AI usage)
- Receive push notifications (renewals, spikes)
- Add/edit subscriptions
- Snooze alerts

**Out of scope (v1 mobile):**
- Tracker (mobile foreground tracking is OS-restricted)
- AI usage import (no Claude Code on phone)

### 2.2 API contract (REST, JSON)

Base URL: `https://api.pulse.app/v1/`

```
POST   /auth/login          {email, password} → {jwt, refresh_token}
POST   /auth/refresh        {refresh_token}   → {jwt}

GET    /workspaces                            → [{id, name, role}]
GET    /workspaces/:id/subscriptions          → [encrypted blobs]
POST   /workspaces/:id/subscriptions          → {encrypted_blob}
PATCH  /workspaces/:id/subscriptions/:sub_id  → {encrypted_blob}
DELETE /workspaces/:id/subscriptions/:sub_id

POST   /sync/push           {changes: [...]}
GET    /sync/pull?since=ts                    → {changes: [...]}

POST   /alerts/devices      {push_token, platform} (FCM/APNs registration)
GET    /alerts              → [recent alerts]
```

### 2.3 Push notifications

- **iOS:** APNs (Apple Push Notification service) via Firebase Cloud Messaging
- **Android:** FCM directly
- Server sends push when:
  - Subscription is N days from renewal (per user setting)
  - AI cost spikes
  - Subscription appears unused

### 2.4 Gmail OAuth flow

Replaces the Claude-Code-chat-based discovery with a real OAuth client:

1. **Create Google Cloud project** at console.cloud.google.com
2. Enable Gmail API
3. Create OAuth 2.0 client ID (web app type)
   - Redirect URI: `https://api.pulse.app/oauth/google/callback`
4. In-app:
   - User clicks "Connect Gmail" in Settings
   - Browser opens to Google's consent screen
   - On approval, Google redirects to Pulse callback with auth code
   - Backend exchanges code for refresh token (stored encrypted)
   - Backend periodically (daily) calls Gmail API to look for receipts
   - Returns discovered subs to client over sync

**Required Gmail API scopes:**
- `gmail.readonly` (read messages — strict scope, requires app verification)
- Or `gmail.metadata` (subjects + senders only — looser, but needs full body for amount parsing)

**App verification:** Required for production (Google reviews privacy
policy + scope justification). Allow 4-6 weeks.

**Estimated effort:** 8-10 weeks (mobile + backend + OAuth verification).

---

## Phase 3 — AI assistant + cross-provider tracking

**Goal:** "Ask Pulse" natural-language assistant. Track AI spend across
OpenAI, Anthropic, Gemini, Cursor, Copilot in one place.

### 3.1 AI assistant ("Ask Pulse")

**Architecture:**
- Embed Anthropic Claude Sonnet (or user's own API key for power users)
- Tool-use pattern: Claude has tools to query the user's local DB

**Tools exposed to the assistant:**

```python
# In assistant/tools.py
TOOLS = [
    {
        "name": "query_subscriptions",
        "description": "Get subscriptions matching filters",
        "input_schema": {
            "type": "object",
            "properties": {
                "active_only": {"type": "boolean"},
                "tag": {"type": "string"},
                "billing_cycle": {"type": "string"},
            },
        },
    },
    {
        "name": "query_token_usage",
        "description": "Get AI token usage for a date range, optionally by project/model",
        "input_schema": {
            "type": "object",
            "properties": {
                "start_date": {"type": "string", "format": "date"},
                "end_date": {"type": "string", "format": "date"},
                "group_by": {"type": "string", "enum": ["project", "model", "day"]},
            },
        },
    },
    {
        "name": "compute_savings",
        "description": "What would I save if I cancel X / switch X to Sonnet?",
        "input_schema": {...},
    },
]
```

**Sample prompts the assistant should handle:**
- "Show me subscriptions I haven't used in 60 days"
- "Compare my AI cost this month vs last"
- "Which project costs the most in tokens?"
- "If I switched all Opus calls in finisit-site to Sonnet, how much would I save?"
- "Predict my December AI bill"
- "Cancel Suno and tell me how much I save per year"

### 3.2 Cross-provider tracking

**Adapter pattern** in `providers/`:

```python
# providers/base.py
class TokenUsageProvider(ABC):
    @abstractmethod
    def sync(self) -> list[TokenUsageRow]: ...

# providers/anthropic_logs.py — already exists (sync_tokens.py)
# providers/openai_admin.py — Phase 3
# providers/openai_chatgpt.py — Phase 3 (scrapes ChatGPT export)
# providers/gemini.py — Phase 3
# providers/cursor.py — Phase 3 (Cursor exposes usage in their dashboard)
# providers/copilot.py — Phase 3
```

**OpenAI Admin API:**
- User pastes their admin key in Settings → Advanced → Integrations
- Daily sync pulls usage, normalizes to Pulse schema, dedup by request_id
- Same encrypted-blob storage pattern

**ChatGPT export:**
- ChatGPT Plus users can export their data (`/settings/data-controls`)
- Pulse parses the JSON to extract message counts (no costs since it's a flat plan, but ROI calculation works)

**Cursor:**
- Cursor's API exposes per-user usage at https://cursor.com/api/dashboard/usage
- Requires session cookie (user pastes from devtools)

**Estimated effort:** 6-10 weeks.

---

## Phase 4 — Bank integration + Team tier

**Goal:** Detect subscriptions from bank/credit card transactions
automatically. Multi-user workspaces for families and small teams.

### 4.1 Bank integration

**Providers:**
- **Plaid** — US, Canada, UK, EU. ~$0.30 per linked account/month.
- **TrueLayer** — UK, EU
- **For Thai banks:** No public API (KBank/SCB/etc. don't expose). Workaround: CSV import wizard with auto-pattern-detection.

**Plaid flow:**
1. User clicks "Connect bank" in Settings
2. Plaid Link opens (popup, hosted)
3. User selects bank, logs in
4. Plaid returns `public_token` → backend exchanges for `access_token`
5. Daily: backend fetches transactions, applies recurring-charge detection algorithm
6. Likely subs are surfaced in app for user approval

**Recurring detection algorithm (backend):**
- Group transactions by `merchant_name` (Plaid normalizes this)
- For each merchant: compute time deltas between charges
- Flag as recurring if deltas are clustered around 28-31 days (monthly), 89-93 days (quarterly), 360-372 days (yearly), with ≥3 charges
- Surface as "Pulse detected: recurring charge from Netflix, $13.99/mo, 6 charges over 6 months" → user accepts → adds to subscription list

### 4.2 Team workspaces

DB schema (already in Phase 1.2): `workspaces` + `workspace_members` exists.

**UI changes:**
- Workspace switcher in sidebar
- Per-subscription "owner" attribution
- "Approve to add" workflow for non-admin members
- Activity feed (audit log)

**Pricing:**
- $19/seat/month
- 3-seat minimum

**Estimated effort:** 8-12 weeks (Plaid contract + integration + multi-tenant UI).

---

## Phase 5 (future) — moat-builders

Not yet planned but worth considering:

- **Subscription marketplace insights** — anonymous benchmarking ("users like you typically pay $X for Cursor")
- **Browser extension** — auto-fill subscription details when on `/billing` pages
- **Receipt OCR** — drop image, extract subscription
- **Negotiation playbook** — built-in templates for renewal calls
- **API access** for Pro/Team users
- **Affiliate links** — Pulse recommends switching to a cheaper plan, gets referral commission
- **Subscription marketplace** — share + import subscription discovery rules

---

## Operational checklist (when launching Phase 1)

Before opening Pro signups:

- [ ] Marketing site (pulse.app) live with pricing page
- [ ] Privacy policy + Terms of service published
- [ ] Stripe live keys + webhook verified
- [ ] Cloud DB migrated + tested with 100+ test accounts
- [ ] E2E encryption audited by external party
- [ ] Customer support pipeline (intercom or email)
- [ ] Status page (statuspage.io) for outage transparency
- [ ] Backup + recovery for cloud DB tested
- [ ] Rate-limiting on API
- [ ] DDoS protection (Cloudflare)
- [ ] GDPR/CCPA data deletion endpoint
- [ ] First-month metrics dashboard for the team

---

## Tech stack summary

| Component | Recommended | Alternative |
|-----------|-------------|-------------|
| Cloud DB + auth | Supabase | Postgres + Auth0 |
| Backend hosting | Supabase Edge Functions | Cloudflare Workers, Fly.io |
| Payment | Stripe | Paddle (better for VAT/MoR) |
| Push notifications | FCM (Firebase) | OneSignal |
| Bank integration | Plaid | TrueLayer (UK/EU only) |
| Mobile framework | React Native (Expo) | Flutter |
| AI assistant | Anthropic Claude Sonnet | OpenAI GPT-4o |
| Email transactional | Postmark | Resend, SendGrid |
| Customer support | Plain.com | Crisp, Intercom |
| Monitoring | Sentry + Better Stack | Datadog (overkill for early) |
| Marketing site | Astro + Vercel | Next.js + Vercel |
| Status page | statuspage.io | Better Stack Status |

---

## Pricing strategy reference

| Tier | Monthly | Annual | Lifetime |
|------|---------|--------|----------|
| Free | — | — | — |
| Pro | $9 | $89 (15% off) | $199 (launch only, capped) |
| Team | $19/user | $190/user (15% off) | n/a |

Free trial: 14-day Pro, no credit card required.

---

## Get in touch

This roadmap is open to revision. If you're picking up Pulse to take it
to Phase 1+, open a discussion — happy to align on architecture choices
before code is written.
