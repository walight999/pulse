<div align="center">

<img src="static/brand/logomark.png" width="80" alt="pulse" />

# pulse

### The cost console Claude Code never gave you.

Local-first dashboard that proves your $200 Claude Max plan returns $4,000 in API value — with accurate cache TTL pricing, plan ROI scoring, and zero telemetry.

[![MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Downloads](https://img.shields.io/github/downloads/walight999/pulse/total)](https://github.com/walight999/pulse/releases)
[![Stars](https://img.shields.io/github/stars/walight999/pulse?style=social)](https://github.com/walight999/pulse/stargazers)
[![Twitter Follow](https://img.shields.io/twitter/follow/mintforai?style=social)](https://twitter.com/mintforai)

[Download for Windows](https://github.com/walight999/pulse/releases/latest) · [Website](https://mintforai.com) · [Discord](https://discord.gg/pulse) · [Changelog](https://mintforai.com/changelog)

</div>

---

<!-- Demo GIF appears here once recorded — see operations/demo-script.md -->
<!-- ![pulse dashboard demo](docs/assets/demo.gif) -->

## What pulse does

**You pay $200/month for Claude Max.** You have no idea if it's worth it. pulse answers that question — and shows you exactly how much value you're getting back.

In one local dashboard, pulse shows:

- 💎 **Plan ROI score** — 5-tier rating from "Idle" to "Legendary value 10×+"
- ⚡ **Accurate cache pricing** — split 5min vs 1hr Anthropic cache rates (most tools are off by 11%+)
- 📊 **Per-model + per-project breakdown** — see where your tokens actually go
- 🔥 **Streak gamification** — daily AI use tracking with glow effect at 30+ days
- 💸 **Cost-per-hour-of-use** — link Claude to your actual coding sessions
- 🌍 **Multi-currency** — 30+ currencies with live ECB rates
- 🔒 **100% local** — SQLite + Streamlit, zero cloud, zero signup, zero telemetry

## Why pulse exists

Anthropic Console shows org-level usage. ClaudeMetrics requires manual upload. Time trackers ignore AI costs. Bank apps don't know the difference between Claude Code and Cursor.

**pulse is the only tool built for the developer who wants to know: "Is my $200/month plan worth it?"**

The answer, for most Claude Code power users, is yes — and pulse proves it with hard numbers, not vibes.

## Install

### Windows (recommended)

Download the latest `.exe` from [Releases](https://github.com/walight999/pulse/releases/latest).

Double-click, follow the installer. pulse appears in your system tray. Click to open the dashboard.

First-run wizard takes 30 seconds: pick currency, set monthly budget, choose alerts. Done.

See [INSTALL.md](INSTALL.md) for detailed install steps. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) if anything goes wrong.

### macOS

Coming Q3 2026 — native Apple Silicon + Intel build. The `platform_compat.py` shim is ready; needs codesigning + Apple Developer account testing.

[Join the macOS waitlist →](https://mintforai.com/#waitlist)

### From source (developers)

```bash
git clone https://github.com/walight999/pulse
cd pulse
pip install -r requirements.txt
python app.py
```

Requires Python 3.12+. SQLite + Streamlit handled automatically.

## How it works

1. **First launch** — pulse detects `~/.claude/projects/*.jsonl` and reads your Claude Code history (read-only, never modified)
2. **Background tracking** — system tray app monitors foreground apps with idle awareness (no keystroke logging)
3. **Live FX rates** — `frankfurter.dev` ECB rates cached for 24h
4. **Cache TTL pricing** — pulse implements the exact Anthropic pricing matrix (Opus/Sonnet/Haiku × 5m/1h cache × input/output)
5. **Dashboard** — Streamlit UI, theme switcher, smooth charts

All data stays on your machine. There is no account. There is no cloud. There is no telemetry by default.

(Pro tier with optional encrypted cross-device sync launches Q3 2026 — see [ROADMAP.md](ROADMAP.md))

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

### AI usage (Claude Code in v1.0)

- Auto-imports Claude Code logs from `~/.claude/projects/*.jsonl`
- Today / This month / All time tabs with hourly + daily granularity
- Per-model + per-project cost breakdown
- Plan ROI hero card with celebratory tiers
- Daily + monthly budgets with spike alerts
- 7-day × 24h heatmap (when do you actually use AI?)
- Forecast for end-of-month projected spend
- Cache hit rate display (most tools skip this)

### Activity

- Foreground app tracking, idle-aware (pauses after 5min of no input)
- Auto-categorization (Productivity, Browser, Distraction, Development)
- Top apps list with gradient bars (productive vs distraction)
- Cross-references with subscriptions for ROI calculation
- Toggle-able anytime (privacy-first)

### System

- Windows system tray app — runs in background, dashboard one click away
- 4 background daemons: token sync (6h), alerts (30min), backup (24h), maintenance (weekly)
- SQLite backup with rotation (last 7 kept)
- Single-instance lock via socket bind (no duplicate processes)
- Light + dark themes with smooth transitions
- 30-second first-run wizard

## Roadmap (high-level)

- **v1.0 (now)** — Local Windows + Claude Code parser + all features above
- **v1.1 (Q3 2026)** — macOS port + 4 more providers (Cursor, OpenAI, Copilot, Gemini)
- **v1.2 (Q3 2026)** — Browser extension for web capture + PWA mobile install
- **v2.0 (Q4 2026)** — Pulse Cloud opt-in: encrypted cross-device sync, friend leaderboard, mobile push, AI assistant
- **v3.0 (Q1 2027)** — Pulse for Teams: per-user attribution, Slack/Teams/Discord, admin controls
- **v4.0+ (Y2)** — Pulse OS: OpenAI-compatible routing + caching gateway (Phase 6, see [Roadmap on Notion](https://www.notion.so/35e9defb95298136ac5ffad90764cd49))

See [ROADMAP.md](ROADMAP.md) for detailed phases + [CHANGELOG.md](CHANGELOG.md) for shipped releases.

## Open-core model

Pulse follows the [Logseq](https://logseq.com) / [Plausible](https://plausible.io) / [Cal.com](https://cal.com) playbook:

| | What | Price |
|---|---|---|
| **Open-source local app** | Everything in this repo. SQLite + Streamlit, no signup, no cloud, no telemetry. | Free forever (MIT) |
| **Pulse Pro (Cloud)** | Cross-device sync, mobile PWA, friend leaderboard | $9/mo (launching Q3 2026) |
| **Pulse Team** | Per-user attribution, Slack/Teams integration, audit retention | $19/seat/mo (launching Q4 2026) |
| **Pulse Enterprise** | SSO (SAML/OIDC), SOC 2, on-prem, custom retention | Custom |

The **free local app** is fully featured for one device on its own. The cloud tier is purely additive — if you never want sync, you never need to pay.

**Special offers:**

- 🎓 **50% off Pro** for verified students (.edu) and OSS maintainers with 100+ stars
- 💎 **Lifetime Pro $199** one-time for first 500 customers (early-adopter unlock)

We open-source the desktop client because we believe a privacy-tracking app must be auditable. If you can read the code, you know it can't phone home.

## Privacy

pulse is **local-first by design**. Your subscription data, AI logs, and activity stay on your machine. There is no cloud connection, no telemetry, no signup, no account.

When Pulse Cloud launches (v2.0), syncing will be **opt-in per metric**. End-to-end encryption is the default. Aggregate stats (leaderboard rankings) require explicit consent.

See [PRIVACY.md](PRIVACY.md) for full details and [SECURITY.md](SECURITY.md) for the threat model.

## Architecture

```
pulse desktop (Windows tray)
├── app.py             — system tray + background daemons + Streamlit launcher
├── dashboard.py       — Streamlit UI (Overview, Subscriptions, AI usage, Activity, Settings)
├── tracker.py         — foreground app + idle tracking via Win32 APIs
├── sync_tokens.py     — Claude Code log parser with exact cache TTL pricing
├── db.py              — SQLite schema + idempotent migrations + audit log
├── theme.py           — light/dark CSS variable system
├── fx.py              — frankfurter.dev FX rates with 24h cache
├── account.py         — tier feature flag system (free/pro/team/enterprise + 26 flags)
├── notifications.py   — Windows toast via PowerShell + Windows.UI.Notifications
├── backup.py          — SQLite backup API with rotation
├── alerts.py          — renewal + cost spike + dead-sub alerts
├── categories.py      — app categorization rules
├── cloud/             — Phase 2 cloud sync (Supabase + AES-256-GCM + Argon2id)
├── api/               — FastAPI REST server + WebSocket bridge
├── integrations/      — Slack / Teams / Discord webhook clients (stdlib only)
├── providers/         — multi-provider parsers (OpenAI / Cursor / Gemini / Copilot)
├── sdk/python/        — programmatic access library
├── browser-ext/       — Chrome/Edge Manifest V3 extension
└── landing/           — Next.js 14 marketing site (deploys to mintforai.com)
```

## Tech stack

- **Frontend**: Streamlit 1.57 + custom CSS (theme variables, gradient animations, Material icons)
- **Backend**: Python 3.12 + SQLite + pandas
- **Charts**: Plotly (themed, no rescaling)
- **Tray**: pystray + pythonw.exe
- **Native APIs**: ctypes for Win32 (foreground window, idle detection)
- **FX**: frankfurter.dev (ECB rates, no API key needed)
- **Pricing**: Anthropic public pricing matrix (Opus/Sonnet/Haiku × 5m/1h cache)
- **Cloud (Phase 2)**: Supabase + FastAPI + AES-256-GCM + Argon2id
- **Landing**: Next.js 14 App Router + Tailwind + Vercel

## Contributing

PRs welcome. Priority areas:

1. **macOS port** — `tracker.py` for foreground app + idle detection via AppKit/IOKit
2. **Additional provider parsers** — Cursor, OpenAI, Copilot, Gemini (see `providers/` scaffold)
3. **Subscription detection heuristics** — non-English receipt emails
4. **Theme variants** — community-contributed light/dark/seasonal themes
5. **Translations** — Japanese, German, Korean, Spanish prioritized

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup + style guide.

## Community

- [GitHub Discussions](https://github.com/walight999/pulse/discussions) — questions + ideas
- [Discord](https://discord.gg/pulse) — chat + support (coming soon)
- [Twitter / X](https://twitter.com/mintforai) — updates
- [hi@mintforai.com](mailto:hi@mintforai.com) — anything else

## License

MIT — see [LICENSE](LICENSE). All current code is permissively licensed. The future hosted cloud service (`cloud/`, `api/`, mobile apps) will remain open under the same license; revenue comes from running the infrastructure, not from license fees.

## Acknowledgements

Inspired by Mint (R.I.P., 2009–2024), the original personal-finance dashboard that taught a generation to see their money. pulse aims to do the same for AI spend.

Built in Bangkok 🇹🇭 by [@walight999](https://github.com/walight999).
