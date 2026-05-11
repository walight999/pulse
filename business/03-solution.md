# 💡 Pulse — Solution

## The problem (restated)

AI subscriptions are exploding. The average prosumer pays for 4-6 AI tools simultaneously ($250-$400/mo), but has no unified view of:

1. **What they pay for** (auto-detected from receipts vs manual entry)
2. **What they use** (Claude tokens, ChatGPT prompts, Cursor calls)
3. **What it's worth** (ROI vs API equivalent, hours of actual use per $)
4. **What to cancel** (subscriptions they signed up for and forgot)

Existing tools solve fragments:
- **Anthropic Console**: org-level, Claude only
- **ClaudeMetrics**: team proxy, Claude only, requires DevOps
- **Bank apps**: see subs but don't categorize "AI"
- **Spreadsheets**: manual labor

## The solution

Pulse is the personal finance dashboard for the AI era. It runs locally, parses your AI usage automatically, and shows you ROI in language that makes the value real.

### Three pillars

**1. Subscription tracker**
Auto-detect subscriptions from Gmail receipts. Manual entry for the rest.
Smart status detection: active monthly / probably yearly / likely cancelled.
Renewal alerts. Cancellation savings tracking.

**2. AI usage analytics**
Parses `~/.claude/projects/*.jsonl` directly for accurate per-model + per-cache-TTL pricing.
Today / This month / All time views with hourly heatmap.
Plan ROI hero with 5-tier gamified rating.
Cross-provider parsing (OpenAI/Cursor/Gemini/Copilot) in v1.1.

**3. Activity tracking**
Foreground app tracking via Win32 APIs (macOS/Linux ports ready).
Idle-aware (pauses after 5 min of no input).
Auto-categorization (Productivity / Development / Browser / Distraction).
Cross-references with subscriptions for ROI per hour-of-use.

## What makes Pulse different (11 moats)

1. **Multi-modal personal tracker** — only tool combining subs + usage + activity
2. **Plan ROI hero** — 5-tier gamified rating with stars + savings number
3. **Cancellation savings tracker** — "Saved $4,300 cancelling 7 subs"
4. **Cost-per-hour-of-use** — links subscription → app → real ROI
5. **Streak gamification** — 30-day glow effect, mint pulse animation
6. **Multi-currency native** — 30+ currencies via ECB live rates
7. **Cache TTL pricing** — split 5min vs 1hr (most tools off by 11%)
8. **Local-first zero-setup** — no cloud, no proxy, no signup
9. **Branded UX** — Pulse mint identity, dark mode, ECG animation
10. **Browser extension** — captures web-based AI sessions (no competitor has)
11. **Cross-platform ready** — Win shipping, macOS + Linux shims ready

## What's NOT in v1

Honesty about scope. v1 does NOT include:

- ❌ macOS native bundle (Q3 — `platform_compat.py` is ready, needs testing)
- ❌ Linux native bundle (Q4 — same)
- ❌ Mobile native app (PWA in v2.0, native in v3.0)
- ❌ Cloud sync (Q3, opt-in)
- ❌ AI assistant ("Ask Pulse") (Phase 3)
- ❌ Bank integration (Plaid US + KBank/SCB TH in v1.5)
- ❌ Receipt OCR (v1.3)
- ❌ Friend leaderboard (Phase 3, scaffolded only)
- ❌ Multi-provider parsing live (scaffolded in `providers/`, needs API keys to test)

This list is intentional. v1 is for the Claude-heavy Windows prosumer. We expand horizontally only after we prove value for the primary persona.

## Success criteria (per phase)

**v1.0 launch** (May 26 or 28):
- 100+ GitHub stars in 48 hours
- 50+ Pulse Pro waitlist signups
- 10+ beta tester testimonials
- 1+ press mention

**v1.1 (M+1)**:
- 1,000+ stars
- Multi-provider live for OpenAI / Cursor / Gemini
- 200+ Pro waitlist

**v2.0 Cloud (M+3-6)**:
- 5,000+ stars
- 100+ paying Pro users
- 5+ Team customers
- Mobile PWA live

**M12**:
- 25,000+ stars
- 600 paying Pro = $5,400 MRR
- 50 Team customers (3+ seats avg) = $2,850 MRR
- 5 Enterprise = $4,000+ MRR
- **Total ~$13,000-44,000 MRR** depending on tier mix
- Inbound from Microsoft / Anthropic / Intuit

## Why now

1. **AI subscriptions exploding** — ChatGPT, Claude, Cursor, Copilot, Gemini, Perplexity, Lovable, v0, Replit, Mistral, Glean, Reflect, Cluely...
2. **Anthropic Console insufficient** — org-only, Claude-only
3. **Mint vacancy** — personal finance category open since 2024
4. **Privacy regulation pushes local-first** — EU AI Act, US state laws
5. **Browser AI growth** — ChatGPT.com, claude.ai, gemini.google.com need capture tool

## Strategic decisions (locked)

- **Defer Phase B+C cloud activation 60+ days post-launch** — prevent scope creep
- **Show HN target shift**: May 18 → May 26 or 28 — give warmup phase runway
- **Beta tester recruitment is non-negotiable** — minimum 10 installs before launch
- **Landing page is critical path** — cannot launch without `pulse.app` live
- **Free truly free** — local users never need to pay, ever
- **Pro hooked on cross-device** — sync + mobile are the freemium upsell
- **Team hooked on shared visibility** — per-user attribution + Slack
