# How I built pulse in 11 days — Mint for the AI era

**Launch day blog post draft.** Target: dev.to / Medium / personal blog.
Post immediately after Show HN goes live + Twitter thread.

---

## TL;DR

I lost track of my AI subscriptions. So I built **pulse** — a local-first
personal-finance dashboard for the AI era. 11 days from idea to public preview.
Open source (MIT) at https://github.com/walight999/pulse.

You can prove your $200 Claude plan returns $4,000 in API-equivalent value.
Track every recurring AI service. Cancel the dead ones. See the ROI you don't
usually see.

It's the only tool that combines:
- Subscription tracking (auto-detected from Gmail receipts)
- AI token usage (parsed from local Claude logs)
- Activity tracking (foreground apps, idle-aware)

In one local-first dashboard.

---

## The problem nobody is solving

You probably pay for 4-6 AI tools right now. ChatGPT Plus. Claude Max.
Cursor Pro. GitHub Copilot. Gemini Advanced. Maybe v0 or Lovable or
Perplexity Pro. Maybe Cluely or Replit Core or Mistral Le Chat.

The average AI prosumer spends **$327/month** across these subscriptions.

You have no idea which ones are worth it.

- Your bank app doesn't categorize "AI" — just shows charges from
  "Anthropic, Inc." and "Cursor AI Inc." with no context.
- Anthropic Console exists but only shows Claude usage at the org level.
- ClaudeMetrics.com requires you to manually upload conversation exports.
- LiteLLM needs your DevOps team to set up a proxy.

**There's no Mint for AI.**

Mint shut down in 2024. The category — automatic personal-finance dashboards —
has been vacant ever since. Meanwhile we all started paying real money for
AI, and nobody built a dashboard for it.

So I did.

---

## What pulse does

### 1. Plan ROI hero

The killer feature. pulse tells you in plain language:

> Your $200/mo Claude Max plan returned **$4,127** in API-equivalent value
> this month — **Legendary tier ★★★★★**

That's a real number from my own dashboard. If I'd paid per-API at Anthropic's
rates, the same tokens would have cost $4,127. The plan is a 20× return.

5-tier rating from "Legendary value" (10×+) down to "Plan idle" (<0.5×) —
so you know exactly when a plan is paying off vs when to downgrade.

### 2. Cancellation savings tracker

The hardest part of personal finance is cancelling subscriptions you don't
use. pulse makes this visible:

> You've cancelled **7 subscriptions** since starting pulse — saving
> **$4,300/year**.

The visible proof that the hard habit was worth it. Compounds over time.

### 3. Cost-per-hour-of-use

Link a subscription to its app (e.g., Photoshop → adobe.exe). pulse computes
ROI per hour of actual use:

> Photoshop · $30/mo · 2 hours used last 30 days → **$15/hour**

Now you decide. Worth $15/hr? Cancel? Switch to a cheaper alternative?

### 4. Streak gamification

The chip glows at 30+ days of consecutive AI use. Small dopamine hit for
the habit. Not gimmicky — just visible.

### 5. Multi-currency native

30+ currencies via live ECB rates (frankfurter.dev — no API key needed).
Pay in THB, see in USD reference. No spreadsheets.

### 6. Accurate cache TTL pricing

This one's technical but it matters. Anthropic charges differently for 5-min
vs 1-hour cache tokens (1.25× vs 2× input rate). **Most tools use one flat
rate and are off by 10%+** on heavy users. pulse splits them correctly.

---

## The local-first stance

pulse runs entirely on your machine.

- Python + SQLite + Streamlit + Windows tray
- Zero account, zero cloud, zero telemetry by default
- The only network calls are: ECB FX rates (cached 24h, can be disabled)
  + optional Gmail MCP for receipt scanning (you opt in)

When pulse Cloud launches in Q3 (cross-device sync + mobile + friend
leaderboard), it'll be opt-in and end-to-end encrypted with AES-256-GCM
+ Argon2id key derivation. Server can't see your data even if they want to.

Or self-host with Docker Compose. Your call.

---

## The 11 days

Day 1 — concept. I'd been losing track of my AI subs for months.
Started sketching.

Day 2-3 — v0.1: Streamlit dashboard reading Claude Code logs from
`~/.claude/projects/*.jsonl`. Dedup by `request_id` (multi-block messages
share one — caught me by surprise on day 2). Plotly chart of daily spend.

Day 4-5 — subscription tracker. Gmail MCP integration for auto-detect.
Smart status logic: "monthly but not charged 60+ days = probably yearly
or cancelled."

Day 6 — activity tracker. Win32 APIs (`GetForegroundWindow`, `LASTINPUTINFO`).
Auto-categorization.

Day 7 — multi-currency. Plan ROI hero with the 5-tier rating.

Day 8 — dark mode + brand identity. Settled on "pulse" (lowercase) + mint
green accent (#00E5A0) + pure-black dark mode + ECG heartbeat line as the
brand signature.

Day 9 — landing page (Next.js + Tailwind) + browser extension (Manifest V3
for Chrome/Edge) + REST API + Python SDK + 8 AI agent definitions.

Day 10 — brand asset generator (`pulse-brand-core/`) that produces 42
deterministic assets from a hand-coded master SVG. No vtracer needed.

Day 11 — launch materials: Twitter thread, beta tester DM templates,
HN FAQ bank, Reddit crossposts, Discord setup, demo video storyboards.

The pace was possible because I shipped one user-visible thing per day,
deferred scope creep aggressively, and used Claude Code as a 24/7 pair
programmer.

---

## What's next

**v1.1 (next 30 days)**: real multi-provider parsers for OpenAI / Cursor /
Gemini / Copilot. Browser extension submitted to Chrome Web Store + Edge
Add-ons. macOS port.

**v2.0 (Q3)**: pulse Cloud — opt-in E2E encrypted sync. Mobile PWA. Friend
leaderboard (5 categories, opt-in, aggregate stats only — never raw token
data shared).

**v3.0 (Q4)**: pulse Team ($19/seat) for 5-50 dev teams. pulse Enterprise
($199/seat) with SSO + SOC 2. Pulse SDK for embedding cost widgets in
Notion / Linear / Slack.

---

## Pricing (when Pro launches)

| Tier | Price | Hook |
|------|-------|------|
| **Free** | $0 forever | All v1 features, local only |
| **Pro** | $9/mo | Cloud sync + mobile + leaderboard |
| **Team** | $19/seat/mo (3+) | Per-user attribution + Slack |
| **Enterprise** | $199/seat/mo | SSO + SOC 2 |

Free is genuinely free forever for local users. You only pay if you go cloud
or team. **Open source MIT under both modes** — including the cloud server.
Self-host if you don't trust us.

---

## How to try it

```bash
git clone https://github.com/walight999/pulse
cd pulse
pip install -r requirements.txt
python app.py
```

Pulse appears in your Windows system tray. Click → dashboard opens at
http://localhost:8501. 30-second onboarding (pick currency, set monthly
AI plan budget, choose alerts). Done.

If you use Claude Code, pulse picks up your logs automatically and shows
your real ROI on the first launch.

---

## Show me your stack

I'd love to see what other people are paying for AI. Drop your stack +
monthly spend in the comments. Mine right now:

- Claude Max: $200/mo (used hard — 10× ROI per pulse)
- ChatGPT Plus: $20/mo (mostly for image gen now)
- Cursor Pro: $20/mo (paying for itself in time saved)
- GitHub Copilot: $10/mo (cheap insurance)
- Gemini Advanced: $20/mo (rarely use — about to cancel after pulse showed me)
- Total: $270/mo. After cancelling Gemini → $250/mo.

---

## Links

- 🔗 Code: https://github.com/walight999/pulse
- 🔗 Landing: https://pulse.app (live soon)
- 🔗 Show HN: [link when live]
- 🔗 Twitter: @pulse_app_ai

---

## A note on the AI era

I genuinely believe AI is the biggest shift since smartphones, and that
the personal-finance category has to be rebuilt around AI subscriptions
the same way Mint was built around credit cards.

If pulse becomes that thing — great. If something better comes along,
I'll use it. Either way: prosumers should be able to see their AI spend
in one local dashboard. That's the bar.

Open to feedback, contributors, and acquisition conversations. Reply here
or DM me.

— White
