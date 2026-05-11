# What's new in Pulse

## v1.1 — Phase B foundation (2026-05-11)

### Added — cloud + multi-provider scaffolding

- **Cloud sync** (`cloud/`) — production-ready code for Supabase Auth + E2E encrypted sync
  - `cloud/auth.py` — magic-link sign-in, session caching, JWT refresh
  - `cloud/crypto.py` — AES-256-GCM + Argon2id key derivation (passes self-test)
  - `cloud/sync.py` — encrypted delta sync with conflict resolution
  - `cloud/leaderboard.py` — friend ranking computation across 5 categories
  - `cloud/teams.py` — multi-user team workspaces with role-based access
  - `cloud/sso.py` — SAML/OIDC scaffolding for enterprise tier
  - `cloud/billing.py` — Stripe Checkout for Pro/Team/Enterprise tiers
- **REST API** (`api/server.py`) — FastAPI server with auth, exports, leaderboard endpoints
- **Python SDK** (`sdk/python/pulse_client.py`) — programmatic access to your own Pulse data
- **Browser extension** (`browser-ext/`) — Manifest V3 capture for ChatGPT, Claude.ai, Gemini, Perplexity
- **Cross-platform shim** (`platform_compat.py`) — foreground app + idle detection + notifications for Windows / macOS / Linux
- **CSV + PDF export** (`export.py`) — full data export, monthly PDF reports via reportlab
- **Slack / Teams / Discord integrations** — themed daily digests, spend alerts, renewal reminders
- **PWA assets** (`static/`) — manifest.json, service worker, offline page

### Added — providers

- `providers/openai_parser.py` — ChatGPT Plus + API + Team with current GPT-5/o3 pricing
- `providers/cursor_parser.py` — Cursor IDE local state DB parser
- `providers/gemini_parser.py` — Google AI Studio + Gemini app with current pricing
- `providers/copilot_parser.py` — GitHub Copilot flat + GraphQL audit

### Added — security + compliance

- `SECURITY.md` — full threat model + encryption details + bug bounty plan
- Audit log table (`audit_log`) — all sensitive events tracked locally
- `db.log_audit()` helper for instrumented logging

### Added — docs + outreach

- `LICENSE` — MIT
- `CONTRIBUTING.md` — onboarding for new contributors
- `docs/MICROSOFT.md` — one-pager for partnership / acquisition outreach
- `docs/SHOW_HN.md` — 3 launch angles with copy + checklists
- `sdk/README.md` — SDK quickstart

### Added — database

- `audit_log` table for security events
- `cloud_state` for sync bookkeeping
- `friend_invites` for leaderboard friend graph
- `api_keys` for SDK / 3rd party access
- `integrations_webhooks` for Slack/Teams/Discord URLs
- `updated_at` columns on subscriptions / token_usage / app_activity for delta sync
- `provider` column on subscriptions for multi-provider tagging

### Changed — UX polish

- Sub-action row no longer overlaps card (4px gap instead of -2px overlap)
- Streak chip glow radius reduced (no overlap with H1)
- Filter chips center-aligned with no leftover spacing from hidden radio circle
- Page header gets 8-12px breathing room before content
- Streamlit columns get explicit 1rem gap (was tight default)
- Vertical block gap 0.4rem → 0.6rem
- Tab panel padding-top 0 → 0.6rem
- Top apps legend moved from bottom to header row (no more "tab" at footer)
- Renewal + Insight boxes height-locked at 72px (matched, balanced)
- AI usage budget bar refactored with `_render_bar()` helper + breathing room
- ROI hero card moved to top of AI usage + Overview pages
- Hide all Streamlit branding (deploy button, viewer badges, footer)

### Changed — performance

- Theme toggle no longer clears cache (2-3x faster switching)
- Fade-in animation 220ms on every page render
- Smooth theme transitions on cards, tables, sidebar (180ms)
- Sidebar collapse → smooth slide animation (was snap)

## v1.0 — initial public preview (2026-05)

### New

- **Theme toggle** — sun/moon icon in sidebar, light + dark modes
- **Subscription tracker** — manual entry + Gmail-discovered receipts
- **AI usage analytics** — Claude Code logs auto-imported, equivalent API cost vs flat plan
- **Activity tracking** — foreground apps, idle-aware, auto-categorized
- **Smart auto-detect** — "monthly but not charged 60+ days = probably yearly or cancelled"
- **Renewal alerts** — Windows toast 3 days before bill
- **Cost spike alerts** — when today exceeds 3× your average
- **Multi-currency** — 30+ currencies, live ECB rates
- **Plan ROI** — see what your subscription saves vs API rates
- **Streak tracker** — consecutive days using AI (glow at 30+ days)
- **Cancellation savings** — track lifetime $ saved when canceling unused subs
- **Smart suggestions** — apps you use a lot but don't track as subscriptions
- **Undo delete** — 30-second window after deleting a subscription
- **Backup + restore** — auto daily, last 7 kept
- **Leaderboard preview** — coming-soon teaser in AI usage page with 5 categories

### Coming next (Pulse Pro)

- Cloud sync + mobile companion app (PWA, then native)
- "Ask Pulse" AI assistant — natural-language queries
- Cross-provider tracking (OpenAI, Cursor, Gemini, Copilot)
- Bank account auto-import (Plaid US, KBank/SCB TH)
- Receipt OCR
- Email weekly digest
- Push notifications
- Friend leaderboard (5 categories, opt-in, aggregate metrics only)

[Join the waitlist](#) in Settings → Pulse Pro for early access.
