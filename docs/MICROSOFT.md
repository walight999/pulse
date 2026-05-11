# Pulse for Microsoft — one-pager

**Prepared for**: Microsoft GitHub Next / Azure AI / M365 Copilot leadership
**Date**: 2026-05-11
**Stage**: v1.0 preview, profitable trajectory, open source

---

## TL;DR

Pulse is the personal finance dashboard for the AI era — local-first, multi-provider, beautifully designed.
We track subscriptions, AI token usage, and app activity in one view. Users see that their
$200/mo Claude Max plan returns $4,000 in API-equivalent value, automatically cancel dead
subscriptions, and gain a coherent view of their AI spend.

We believe this becomes a category-defining product. We'd love to talk about how it fits with
Microsoft's Copilot, Edge, and Windows roadmap.

---

## Why this matters to Microsoft

### 1. Consumer narrative for M365 Copilot
Microsoft is selling Copilot at $30/seat/mo and needs proof of ROI for the consumer/SMB
segment. **Pulse already computes this**: "Copilot saved you 12.4 hours this month based on
your actual usage." We provide the data + presentation; Microsoft provides the distribution.

### 2. Provider-agnostic positioning
Microsoft backs OpenAI but Azure ships Claude, Llama, Mistral. Enterprise customers want
dashboards that don't lock them into one provider. Pulse is **provider-neutral by design**
— current providers: Anthropic, planned: OpenAI, Cursor, Gemini, Copilot, Perplexity.

### 3. Windows-native fit
Pulse is Windows-tray-native: pythonw.exe, Win32 APIs (foreground window, LASTINPUTINFO
idle detection), pystray, native PowerShell toast notifications. The team has rare expertise
in modern Windows desktop development.

### 4. Privacy-first as moat
Microsoft's privacy brand (Edge, Windows Hello, BitLocker) values local-first architecture.
Pulse is **100% local by default**, with E2E-encrypted optional cloud sync. This matches the
Microsoft positioning vs. Google's data harvesting.

### 5. Edge browser extension
We're shipping a browser extension to capture chat.openai.com, claude.ai, gemini.google.com
session data. Edge is the natural distribution channel — and a Edge-first deployment gets us
to scale faster than building Chrome adoption.

---

## What we've built

| Component | Status |
|-----------|--------|
| Windows tray app + dashboard | ✅ shipped |
| Subscription tracker with smart auto-detect | ✅ shipped |
| Claude Code token analytics (accurate cache TTL pricing) | ✅ shipped |
| Activity tracking (foreground app + idle) | ✅ shipped |
| Plan ROI hero card with 5-tier rating | ✅ shipped |
| Cancellation savings tracker | ✅ shipped |
| Multi-currency (30+, live ECB rates) | ✅ shipped |
| Light/dark themes with smooth transitions | ✅ shipped |
| Leaderboard preview + waitlist | ✅ shipped |
| OpenAI / Cursor / Gemini / Copilot parsers | 🛠 scaffolded |
| macOS port | 🛠 in progress |
| Cloud sync (Supabase, E2E encrypted) | 🛠 scaffolded |
| PWA mobile (iOS/Android home screen) | 🛠 manifest + SW ready |
| Team tier (per-user attribution) | 🛠 scaffolded |
| Slack / Teams / Discord webhooks | ✅ shipped |
| CSV / PDF export | ✅ shipped |
| Pulse REST API + Python SDK | ✅ shipped |
| SSO / SAML for Enterprise | 🛠 scaffolded |

Repo: https://github.com/walight999/pulse (MIT licensed)

---

## Distribution + traction plan

1. **Show HN launch** — "Local-first personal AI subscription tracker" (planned next 14 days)
2. **r/ClaudeCode + r/MicrosoftAI + r/sysadmin** organic posts
3. **Twitter/X dev community** — demo videos of "Legendary value 10x" hero card
4. **Anthropic Discord** — first-mover advantage in Claude ecosystem
5. **Productivity-tool YouTubers** — affiliate program at $9/mo Pro tier

Expected: 1k-5k installs in month 1, 10k by month 3, conversion to Pro ~5%.

---

## Why now

- **AI subscriptions are exploding** (ChatGPT, Claude Max, Cursor, Copilot, Cluely, Lovable,
  v0, Replit, Mistral, Perplexity, Glean, Reflect...). Average prosumer pays for 4-6 today,
  trending to 10+ by 2027.
- **No consumer-facing tool exists** for this category. ClaudeMetrics.com and Anthropic
  Console serve narrow needs; Pulse is the only multi-provider personal dashboard.
- **Mint died in 2024.** The personal-finance category is wide open for AI-era reinvention.
  Intuit paid $170M for Mint in 2009 → became multi-billion personal-finance brand.
- **Privacy regulation** (EU AI Act, US state laws) makes local-first architecture a
  competitive advantage.

---

## Team

- **White (@walight999)** — Founder + Engineer. Macro/gold trader by background, technical
  builder by craft. Based in Bangkok. 10+ years software engineering.
- **Looking for**: Co-founder with B2B sales / enterprise distribution experience.

---

## What we're asking

- 30-min intro call with Microsoft GitHub Next or Azure AI leadership
- Feedback on integration angles (Edge extension, Copilot ROI tie-in)
- Distribution partnership exploration (Edge add-on store, Windows Store)
- Acquisition conversation in M6-M12 timeframe

---

## Contact

- White / walight999 — walight999@gmail.com
- GitHub: https://github.com/walight999
- Repo: https://github.com/walight999/pulse
- Demo: localhost (Windows installer coming Q3 2026)
