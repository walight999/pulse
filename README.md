# Pulse

**Mint for AI.** A local-first desktop dashboard for your AI spend, subscriptions, and productivity.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20soon-lightgrey)
![Privacy](https://img.shields.io/badge/privacy-100%25%20local-success)
![Status](https://img.shields.io/badge/status-v1.0%20preview-orange)

Pulse is the only personal-finance app built for the AI era. Track every recurring AI subscription, every Claude token, every hour of focused work — all in one local-first dashboard. Discover that your $200/mo Claude Max plan returns $4,000 in API-equivalent value. Cancel the dead subscriptions automatically detected from your inbox. See your stack health at a glance.

> Built for individuals who pay real money for AI tools and want to know if it's worth it.

---

## Why Pulse

Other tools give you fragments:

| Tool | What it shows | What's missing |
|------|--------------|----------------|
| **Anthropic Console** | Per-org Claude usage | No personal view, no other providers, no subscriptions |
| **ClaudeMetrics.com** | Conversation analytics | Manual export upload, Claude-only, no subscriptions |
| **Bank apps** | All subscriptions | No AI-specific breakdown, no usage correlation |
| **Time trackers** | Hours per app | No financial context, no AI link |

**Pulse is the only tool that connects all three** — subscription cost, AI token spend, and actual app usage time — into one personal-finance dashboard.

## What's unique

- 🏆 **Plan ROI hero** — 5-tier rating from "Legendary value" (10x+ return) to "Plan idle" with stars, savings number, and visual coverage bar
- 💎 **Cancellation savings tracker** — "You've saved ฿18,500 by cancelling 3 subs since you started using Pulse"
- 🔥 **Streak gamification** — daily AI use streak with glow effect at 30+ days
- 📊 **Cost-per-hour-of-use** — link a subscription to its app; Pulse computes ROI from your real usage
- 🌍 **Multi-currency native** — 30+ currencies with live ECB rates; pay in THB, see in USD reference
- ⚡ **Accurate cache TTL pricing** — split 5min vs 1hr cache rates (most tools are off by 11%)
- 🔒 **Local-first** — SQLite + Streamlit + Windows tray; zero cloud, zero signup, zero proxy

## Features

### Subscriptions
- Auto-detect status: active monthly / late payment / probably yearly / likely cancelled
- Smart classification: "monthly but not charged 60+ days = probably yearly or cancelled"
- Renewal alerts (Windows toast 3 days before)
- Calendar export (.ics) — see all renewals in Google/Apple Calendar
- Cancellation URL field — one-click cancel
- Trial period tracking with end-date warnings
- Multi-currency with live FX rates
- Tag system (business / personal / family) for tax-time review

### AI usage
- Imports Claude Code logs from `~/.claude/projects/*.jsonl` automatically
- Today / This month / All time tabs with hourly + daily granularity
- Per-model + per-project cost breakdown
- Plan ROI hero card with celebratory tiers
- Daily + monthly budgets with spike alerts
- 7-day x 24h heatmap (when do you actually use AI?)
- Forecast for end-of-month projected spend
- Leaderboard preview (Phase 3)

### Activity
- Foreground app tracking, idle-aware (pauses after 5 min of no input)
- Auto-categorization (Productivity, Browser, Distraction, Development, etc.)
- Top apps list with gradient bars (productive vs distraction)
- Cross-references with subscriptions for ROI

### System
- Windows system tray app — runs in background, dashboard one click away
- 4 background daemons: token sync (6h), alerts (30min), backup (24h), maintenance (weekly)
- SQLite backup with rotation (last 7 kept)
- Single-instance lock via socket bind (no duplicate processes)
- Light + dark themes with smooth transitions

## Install

```powershell
git clone https://github.com/walight999/pulse
cd pulse
pip install -r requirements.txt
python app.py
```

Pulse appears in your Windows system tray. Click to open the dashboard.

**First run**: 30-second onboarding to pick currency, set monthly AI plan budget, and choose which alerts to enable.

## Roadmap

### v1.0 — Local-first preview (now)
- All features above on Windows

### v1.1 — Multi-provider (next 30 days)
- OpenAI / ChatGPT Plus usage detection
- Cursor Pro tracking
- Gemini Advanced
- GitHub Copilot
- Perplexity / Replit / v0 / Lovable
- Universal "AI subscription" category in dashboard

### v1.2 — Cross-platform (60 days)
- macOS port (system tray, idle detection, foreground app)
- Linux support (best-effort)
- Progressive Web App (install on iOS/Android home screen)

### v2.0 — Pulse Cloud (Q3 2026)
- Optional account for cross-device sync
- Mobile companion app (PWA, then native)
- Friend invite system + AI usage leaderboard (5 categories: Best ROI, Longest streak, Token wizard, Power day, Project depth)
- Slack / Teams / Discord weekly digest
- Bank integration (Plaid US, KBank / SCB Thailand)
- Receipt OCR (photo of subscription receipt → auto-add)

### v3.0 — Pulse for Teams (Q4 2026)
- Multi-user dashboard with per-developer attribution
- Role-based access (admin / member / viewer)
- SSO/SAML for enterprise
- SOC2 Type I compliance
- Pulse SDK — embed cost widgets in Notion / Linear / Slack
- Pulse API — programmatic access to your own data

See [`ROADMAP.md`](ROADMAP.md) for the full architecture spec.

## Pricing

- **Pulse Free** — local-only, all current features, forever
- **Pulse Pro** ($9/mo) — cloud sync, mobile, leaderboard, cross-provider, AI assistant ("Ask Pulse")
- **Pulse Team** ($19/seat/mo, min 3 seats) — shared dashboard, per-user attribution, Slack integration, admin controls
- **Pulse Enterprise** ($199/seat/mo) — SSO, SOC2, custom roles, dedicated support, SLA

Pro and above launch with Phase 2. Join the waitlist in Settings → Pulse Pro.

## Privacy

Pulse is **local-first by design**. Your subscription data, AI logs, and activity tracking stay on your machine. There is no cloud, no telemetry, no signup, no account.

When Pulse Cloud launches (v2.0), syncing will be **opt-in**. End-to-end encryption is the default. Aggregate stats (rankings, streaks) require explicit consent per metric.

See [`PRIVACY.md`](PRIVACY.md) for details.

## Architecture

```
Pulse desktop (Windows tray)
├── app.py — system tray + background daemons + Streamlit launcher
├── dashboard.py — Streamlit UI (Overview, Subscriptions, Activity, AI usage, Settings)
├── tracker.py — foreground app + idle tracking via Win32 APIs
├── sync_tokens.py — Claude Code log parser with exact cache TTL pricing
├── db.py — SQLite schema + idempotent migrations
├── theme.py — light/dark CSS variable system
├── fx.py — frankfurter.dev FX rates with 24h cache
├── notifications.py — Windows toast via PowerShell + Windows.UI.Notifications
├── backup.py — SQLite backup API with rotation
├── alerts.py — renewal + cost spike + dead-sub alerts
├── categories.py — app categorization rules
├── providers/ — multi-provider adapters (Phase 2)
├── cloud/ — auth, sync, billing scaffolding (Phase 2)
├── assistant/ — "Ask Pulse" tool definitions (Phase 3)
└── integrations/ — Plaid, Slack, Teams (Phase 2-3)
```

## Tech stack

- **Frontend**: Streamlit 1.57 + custom CSS (theme variables, gradient animations, Material icons)
- **Backend**: Python 3.12 + SQLite + pandas
- **Charts**: Plotly (themed, no rescaling)
- **Tray**: pystray + pythonw.exe
- **Native**: ctypes for Win32 APIs (foreground window, idle detection)
- **FX**: frankfurter.dev (ECB rates, no API key needed)
- **Pricing**: Anthropic public pricing matrix (Opus/Sonnet/Haiku × 5m/1h cache)

## License

MIT — see [`LICENSE`](LICENSE).

## Contributing

Pulse is a personal project but PRs are welcome. Focus areas:

- macOS / Linux port (especially `tracker.py` for foreground + idle)
- Additional provider parsers in `providers/`
- Subscription detection heuristics for non-English receipt emails
- Theme variants

See [`CONTRIBUTING.md`](CONTRIBUTING.md) (coming soon).

## Acknowledgements

Inspired by Mint (R.I.P., 2009-2024), the original personal-finance dashboard that taught a generation to see their money. Pulse aims to do the same for AI spend.

Built in Bangkok.
