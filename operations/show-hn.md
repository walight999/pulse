# Show HN draft — Pulse

Different angles to test. Pick one, post, measure, iterate.

---

## Angle 1: Personal AI finance (broad)

**Title**: Show HN: Pulse — Personal finance dashboard for the AI era (local-first, MIT)

**Body**:

I built Pulse because I lost track of my AI spending. ChatGPT Plus, Claude Max, Cursor Pro,
Copilot — all hitting my card monthly, and I had no idea if any of them were worth it.

Pulse is a local-first Windows tray app + Streamlit dashboard that tracks:

- All AI subscriptions (auto-detected from your inbox via Gmail MCP)
- Claude Code token usage parsed directly from `~/.claude/projects/*.jsonl` (accurate
  per-model + per-cache-TTL pricing — most tools are off by 10%+)
- Foreground app activity with idle detection (Win32 APIs)
- Combines all three into a single dashboard that tells me, e.g., "Your $200/mo Claude Max
  plan is returning $4,000 in API-equivalent value this month — Legendary tier ★★★★★"

Everything runs locally. No account, no cloud, no telemetry. Optional Pulse Cloud
(coming Q3) will add E2E-encrypted sync, mobile companion, and friend leaderboards.

Open source (MIT) at https://github.com/walight999/pulse. Would love feedback.

---

## Angle 2: Developer cost visibility (technical)

**Title**: Show HN: I parse my Claude Code logs to track per-project AI spend

**Body**:

Anthropic Console shows org-level Claude spend. ClaudeMetrics.com asks you to upload exports.
LiteLLM requires DevOps to deploy a proxy. None of them work for the prosumer case:
"I'm one dev, I want to see what my last week of Claude Code cost me and which projects ate
the budget."

So I built Pulse. It reads `~/.claude/projects/*.jsonl` directly, dedupes by request_id
(multi-block messages share IDs — caught me by surprise), splits cache_creation tokens
into 5min vs 1hr TTLs (huge accuracy win), and presents the data with:

- Today / This month / All time tabs
- Per-project breakdown (which `cwd` is burning your tokens?)
- Hourly heatmap (when do you actually use AI?)
- Plan ROI: API equivalent ÷ plan cost, with a 5-tier gamified rating

It's part of a larger personal-finance app for the AI era (subscriptions, activity tracking,
multi-currency, alerts) but the AI usage view alone might be useful for r/ClaudeCode folks.

Open source (MIT) at https://github.com/walight999/pulse.

---

## Angle 3: Mint nostalgia (consumer/emotional)

**Title**: Show HN: Mint died, so I built Pulse — personal finance for AI subscriptions

**Body**:

Mint shut down in 2024. The category it pioneered — automatic personal-finance dashboards
— has been vacant since.

Meanwhile we all started paying $9, $20, $30, $200/month for AI tools. ChatGPT, Claude,
Cursor, Copilot, Lovable, v0, Perplexity Pro. By 2027 the average prosumer will subscribe
to 10+ AI tools. Bank apps don't categorize them. AI providers don't tell you what you're
spending across the ecosystem.

Pulse is what Mint would have been if it shipped in 2026: local-first by default, AI-aware,
beautiful UI, with three killer features no one else has:

1. **Plan ROI Hero** — Your $200/mo Claude Max returning $4,000 in API value? Pulse shows
   you "Legendary value ★★★★★" with the exact savings number.
2. **Cost-per-hour-of-use** — Linked Photoshop to your $30/mo Adobe sub? Pulse shows "$15/hr
   based on your last 30 days" so you can decide if it's worth it.
3. **Cancellation savings tracker** — "You've saved $4,300 by cancelling 7 subs since you
   started using Pulse."

Local-only forever for personal use. Cloud sync + leaderboard (opt-in) coming Q3.

MIT licensed, Python + Streamlit, runs as Windows tray app.

https://github.com/walight999/pulse

---

## Recommended angle

**Angle 1** for broadest reach. **Angle 2** for technical credibility on r/programming /
r/ClaudeCode crossposts. **Angle 3** for press pickup (Mint nostalgia hooks journalists).

## Pre-launch checklist

- [ ] Screenshots in README (light + dark theme)
- [ ] 30-second demo GIF showing tab navigation
- [ ] Pin a "Roadmap to v1.1" issue with multi-provider work
- [ ] LICENSE file (✓ done — MIT)
- [ ] CONTRIBUTING.md (TODO)
- [ ] Set up `gh repo watch` for first-comment notifications
- [ ] Have Pulse Pro waitlist ready in Settings (✓ done)
- [ ] Have leaderboard waitlist ready (✓ done)
- [ ] Twitter/X account prepared with handle reservation
- [ ] Discord server setup for community Q&A

## Post-launch follow-ups

- Reply to every comment within 4 hours
- Cross-post to r/ClaudeCode, r/sysadmin, r/MicrosoftAI, r/sideproject
- Tweet thread with key features + demo video
- Email outreach to top 5 productivity YouTubers

## Expected outcome

- 200-500 stars in 48h if angle hits
- 50-200 waitlist signups for Pro + leaderboard
- 1-3 enterprise inquiry emails
- 1-2 acquisition or partnership probes
