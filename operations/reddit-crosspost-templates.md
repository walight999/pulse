# Reddit crosspost templates

Post these in order, **after** Show HN goes live. Each subreddit has different
norms — using identical text everywhere gets you banned.

Wait 30 minutes after HN post before crossposting (HN ranking is sensitive
to immediate cross-referrals).

---

## r/ClaudeAI

**Title**: I built a local dashboard that shows your real Claude ROI vs API equivalent

**Flair**: Project Showcase

**Body**:
```
Hey r/ClaudeAI 👋

I got tired of not knowing if my Claude Max plan was actually worth $200/mo,
so I built Pulse — a local-first dashboard that parses your `~/.claude/projects/`
JSONL logs and computes the real API-equivalent value.

Mine shows my current Max plan returning $4,127 in API-equivalent value this
month — "Legendary value ★★★★★" tier.

What it does (Claude-specific):
- Auto-imports all your Claude Code logs (request-deduped, cache TTL split)
- Per-model breakdown (Opus / Sonnet / Haiku)
- Per-project breakdown (which `cwd` is burning tokens)
- 7-day × 24h heatmap (when do you actually use AI?)
- Plan ROI tier with star rating
- Cost spike alerts (when today exceeds 3× your average)

Plus subscription tracking (any provider), activity correlation, multi-currency
(30+ via live ECB rates), and a Windows tray app.

Everything runs locally. No account, no cloud, no telemetry. MIT licensed.

Repo: https://github.com/walight999/pulse

Show HN: [link]

Would love feedback from heavy Claude users. Especially curious if anyone
else has the cache_5m vs cache_1h pricing right — I had to reverse-engineer
that from the `ephemeral_*_input_tokens` fields and most tools I've seen
are off by 10%+ because they use a flat cache rate.
```

---

## r/LocalLLaMA

**Title**: Show: Local-first dashboard for AI subscription + usage tracking (no cloud, no telemetry)

**Flair**: Tutorial | Guide

**Body**:
```
Built this for myself, sharing in case useful to the local-first crowd here.

Pulse runs entirely on your machine — Python + SQLite + Streamlit. No
account creation, no cloud calls (except optional frankfurter.dev for live
FX rates), no telemetry.

What it tracks:
- AI subscriptions (auto-detect from Gmail receipts or manual entry)
- Claude usage (parses your local `~/.claude/projects/*.jsonl`)
- Foreground app activity with idle detection (Win32 APIs)
- Plan ROI: "$200 Claude → $4,127 API value"

Cross-platform shim ready for macOS + Linux (`platform_compat.py`) — just
needs testing. Win32-first only because that's what I run.

Future cloud sync (Pulse Cloud, optional, Q3 2026) will use AES-256-GCM
with Argon2id key derivation — server can't see your data. Or you can
self-host the cloud with Docker Compose.

Repo: https://github.com/walight999/pulse (MIT)

Would love a Linux user to test platform_compat.py against xdotool/xprintidle.
```

---

## r/sysadmin

**Title**: Show: Local dashboard for tracking your team's AI tool spend (no SaaS, no proxy)

**Flair**: Tools & Software

**Body**:
```
If anyone here is responsible for tracking the team's Claude Code / ChatGPT
spend without setting up a LiteLLM proxy + Grafana stack — this might help.

Pulse runs as a Windows tray app. Each dev installs it locally. It parses
their own Claude logs (or future: OpenAI/Cursor logs) and shows:

- Daily/monthly spend with budget alerts
- Per-project cost (which client is burning Claude budget)
- API equivalent vs flat plan cost (when does the plan stop paying off?)
- CSV/PDF export for finance

Team tier (Q3) will add shared dashboards with per-user attribution + Slack
webhooks for daily digest. For now it's single-user local but the schema
is sync-ready.

Privacy: nothing leaves the dev's machine unless they opt into Pulse Cloud
(coming Q3, E2E encrypted, self-hostable). No proxy in your network path.

MIT licensed: https://github.com/walight999/pulse

PR-ready Slack/Teams integration already in the repo if your shop wants to
fork.
```

---

## r/SaaS

**Title**: Show: Mint for the AI era — personal finance dashboard for AI subscriptions

**Flair**: Show & Tell

**Body**:
```
Mint shut down in 2024. The category — automatic personal-finance dashboards
— has been vacant since.

Meanwhile we all started paying for ChatGPT Plus + Claude Max + Cursor Pro +
Copilot + Gemini Advanced + maybe Lovable / v0 / Perplexity. Average prosumer:
$300+/mo across 4-6 AI tools.

Bank apps don't categorize "AI." Anthropic Console only shows Claude. There's
no Mint for this.

So I built Pulse — local-first, auto-detects subscriptions from Gmail
receipts, parses Claude usage from local logs, computes ROI ("your $200
plan returns $4,127 in API value"), tracks cancellation savings ("you've
saved $4,300 by cancelling 7 subs").

Pricing model:
- Free forever for local use (MIT licensed)
- Pro ($9/mo) — cloud sync + mobile + leaderboard + cross-provider — Q3
- Team ($19/seat) — shared dashboards, Slack — Q3
- Enterprise ($199/seat) — SSO, SOC 2 — Q4

Repo: https://github.com/walight999/pulse
HN: [link]
Landing: pulse.app (when live)

Curious what r/SaaS folks think about the freemium positioning. Free truly
free + Pro hooked on cross-device + Team hooked on shared visibility.
```

---

## r/sideproject

**Title**: Show: Pulse — personal AI finance dashboard (8 months solo, MIT, launched today)

**Flair**: Showoff

**Body**:
```
8-month solo build, launching publicly today.

Pulse = Mint for AI subscriptions. Local-first dashboard:
- All AI subs in one view (auto-detected)
- Claude / GPT / Cursor / Gemini usage (Claude shipping, others Q2)
- ROI tier: "Your $200 Claude returns $4,127 in API value — Legendary"
- Cancellation savings tracker (the part that pays for itself)
- Streak gamification (47-day glow at 30+ days)
- 100% local, no signup

MIT licensed, Python + Streamlit + SQLite. Windows tray app, macOS/Linux
ports scaffolded (need testing).

Code: https://github.com/walight999/pulse
HN: [link]

Open to PRs especially for macOS/Linux port and additional provider parsers.

Open to feedback especially on the freemium model — Free is genuinely free,
Pro is $9/mo for cloud + mobile + leaderboard, Team is $19/seat. Pricing
fair? Too cheap? Too expensive?
```

---

## Posting rules

- ⏰ Show HN first → wait 30 minutes → then crossposts
- ✋ Don't crosspost to more than 5 subreddits the same day (looks spammy)
- 🔗 Always link back to HN, not the landing page (HN ranking benefits)
- 💬 Reply to comments on Reddit within 2 hours
- 🚫 Don't ask for upvotes (against rules everywhere)
- ✅ Do answer follow-up questions in detail

## Subreddit-specific etiquette

| Subreddit | What works | What gets banned |
|-----------|-----------|------------------|
| r/ClaudeAI | Technical detail, code links | Marketing-speak |
| r/LocalLLaMA | Privacy emphasis, MIT license | Cloud-first products |
| r/sysadmin | Operations angle, finance reporting | Consumer pitches |
| r/SaaS | Business model discussion | Pure product showcase |
| r/sideproject | Solo-founder vibe, behind-scenes | Big-team brand pitches |

## What to do if a post gets removed

Don't argue with mods publicly. DM them:

```
Hey — saw my pulse post was removed. Happy to adjust to meet community
norms. What changes would help it fit better? Thanks for the work you do.
```

90% of bans are reversible if you're polite + specific.
