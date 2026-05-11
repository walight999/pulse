# 🚀 Pulse MVP — Product Requirements Document (PRD)

**Status**: v1.0 shipped · v1.1 in progress
**Owner**: White (@walight999)
**Last updated**: 2026-05-11

---

## 1. Vision

Pulse is the local-first personal-finance dashboard for the AI era. It replaces three things people currently do badly: tracking AI subscriptions in spreadsheets, guessing Claude ROI from memory, and not knowing what apps they actually use.

## 2. Problem statement

The average AI prosumer pays $250-$400/mo across 4-6 subscriptions, with no unified view of cost, usage, or value. Existing tools solve fragments (Anthropic Console = Claude only, bank apps = no AI categorization, spreadsheets = manual).

## 3. Users

Three personas (full detail in `business/01-personas.md`):

- **P1**: AI Power User (engineer/designer, 4-6 AI subs, $250-$400/mo)
- **P2**: Curious Prosumer (marketer/founder, 2-4 AI subs, $80-$150/mo)
- **P3**: Dev Team Lead (engineering manager, $1K-$10K team AI spend, needs per-user attribution)

## 4. Goals (v1.0)

| Metric | Target | Measurement |
|--------|--------|-------------|
| GitHub stars in 48h post-launch | 100+ | repo Insights |
| Pro waitlist signups in 14 days | 50+ | `data/waitlist.json` |
| Beta tester testimonials | 10+ | `marketing/beta-tester-outreach.md` tracking |
| Press mentions in 7 days | 1+ | manual tracking |
| Cold-install success rate | 95%+ | manual VM testing |

## 5. Non-goals (v1.0)

Explicitly NOT in scope:

- macOS / Linux native builds (Q3-Q4, shim ready in `platform_compat.py`)
- Mobile native app (PWA in v2.0)
- Cloud sync (Q3, opt-in)
- AI assistant ("Ask Pulse") (Phase 3)
- Bank integration (v1.5)
- Receipt OCR (v1.3)
- Multi-provider live (v1.1, scaffolded only in v1.0)

## 6. User stories (v1.0)

### Onboarding

- **US-01** As a new user, I want a 30-second onboarding so I can start using Pulse without reading docs.
- **US-02** As a new user, I want to set my display currency upfront so all values show consistently.
- **US-03** As a new user, I want to set my monthly AI plan budget so the ROI hero card has meaningful context.

### Subscriptions

- **US-04** As a user, I want to add a subscription manually with name + cost + cycle.
- **US-05** As a user, I want Pulse to auto-detect subscriptions from my Gmail receipts (via Gmail MCP).
- **US-06** As a user, I want to see active vs cancelled subs with smart status badges.
- **US-07** As a user, I want renewal alerts 3 days before a bill hits.
- **US-08** As a user, I want a one-click cancel link for each sub.
- **US-09** As a user, I want to see lifetime savings from cancelled subs.

### AI usage

- **US-10** As a Claude user, I want Pulse to auto-parse my `~/.claude/projects/*.jsonl` files.
- **US-11** As a user, I want per-model + per-project cost breakdown.
- **US-12** As a user, I want a Plan ROI hero with 5-tier rating ("Legendary" through "Plan idle").
- **US-13** As a user, I want a 7×24h heatmap showing when I use AI most.
- **US-14** As a user, I want today's spend with cost-spike alerts (3× average).

### Activity

- **US-15** As a user, I want Pulse to track foreground apps without my input.
- **US-16** As a user, I want auto-categorization (Productivity / Development / Browser / Distraction).
- **US-17** As a user, I want cost-per-hour-of-use ROI for app-linked subs.
- **US-18** As a user, I want a top-apps list with productive vs distraction visual.

### System

- **US-19** As a user, I want Pulse to run in the Windows tray, opening to dashboard with one click.
- **US-20** As a user, I want light + dark themes with smooth transitions.
- **US-21** As a user, I want daily automatic SQLite backups (7 kept).
- **US-22** As a user, I want a CSV export of all my data.

## 7. Acceptance criteria (v1.0 — all shipped)

- [x] US-01 to US-22 all implemented in `dashboard.py`
- [x] First-run wizard takes <60 seconds
- [x] Auto-detect parses common receipt emails (Anthropic, OpenAI, GitHub, Cursor, Lovable)
- [x] Claude log parsing dedupes by `request_id`, splits 5min/1hr cache
- [x] ROI hero 5-tier rating renders with stars + savings number
- [x] Heatmap themed to mint intensity in both light + dark mode
- [x] Activity tracker pauses after 5 min idle (`LASTINPUTINFO` API)
- [x] Windows tray app runs as background process
- [x] Dark mode covers every Streamlit component
- [x] Daily backup rotation in `backups/` (last 7 kept)
- [x] CSV export available via `Settings → Data`

## 8. Future scope (v1.1+)

### v1.1 (M+1, ~30 days post-launch)

- Multi-provider parsers live: OpenAI API key, Cursor IDE state, Gemini AI Studio, GitHub Copilot
- Browser extension submitted to Chrome Web Store + Edge Add-ons
- macOS port verified on a real Mac
- Receipt OCR (Tesseract local + Gemini Flash fallback)

### v2.0 Cloud (M+3-6)

- Supabase auth (magic link)
- Bidirectional E2E encrypted sync (AES-256-GCM + Argon2id)
- Mobile PWA (iOS/Android home screen install)
- Friend leaderboard (5 categories, opt-in)
- "Ask Pulse" AI assistant (natural-language queries)
- Slack/Teams/Discord webhook integrations live

### v3.0 Team + Enterprise (M+6-12)

- Multi-user team workspaces with role-based access
- Per-developer attribution
- Pulse SDK + REST API published
- SSO/SAML for enterprise
- SOC 2 Type I audit underway

## 9. Open questions

- Should the free tier include browser extension or gate to Pro?
  - **Current answer**: Free includes browser extension. Cross-device sync is the Pro gate.
- Should we offer self-hosted Pulse Cloud?
  - **Current answer**: Yes, with optional paid setup support. Increases enterprise trust.
- How aggressive should we be on multi-provider in v1.1?
  - **Current answer**: Live for OpenAI + Cursor by M+1. Gemini + Copilot by M+2. Don't block on completeness.
- Should we add a "wallet" view showing all subs as a payment timeline?
  - **TBD** — would test in v1.2 if user research validates.

## 10. Success measures

Quantitative:
- GitHub stars (vanity but indicates reach)
- Repo install counts (best-effort via telemetry opt-in)
- Pro waitlist signups (best leading indicator of revenue)
- Press mentions
- Show HN ranking + comment count

Qualitative:
- Beta tester sentiment in DMs
- Discord engagement
- Quote-worthy testimonials for marketing
- Inbound from press / acquirers
