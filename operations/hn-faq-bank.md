# Show HN — FAQ response bank

Pre-written responses for the most likely questions on Show HN.
First reply within 30 minutes of every comment is the most important
signal for HN ranking. Have these ready.

---

## "Is it really local-first?"

```
Yes. The entire app is a Python Streamlit + SQLite stack that runs from your
machine. The DB lives at `~/.local/share/pulse/tracker.db` (Win/Mac/Linux).

No network calls except:
1. `frankfurter.dev` for live FX rates (cached 24h, can be disabled)
2. Optional Gmail MCP for receipt scanning (opt-in, OAuth in your browser)

No telemetry, no analytics, no account creation.

Future Pulse Cloud is strictly opt-in and uses E2E encryption (AES-256-GCM
+ Argon2id key derivation). Server never sees your data.

Code is MIT licensed and auditable: github.com/walight999/pulse
```

---

## "How is this different from ClaudeMetrics?"

```
ClaudeMetrics (the .com) is for individual Claude conversation analysis via
exports. ClaudeMetrics (the idea — proxy gateway for team usage) targets
enterprise teams on Bedrock/Vertex.

Pulse targets the PROSUMER who pays for 4-6 AI tools personally and wants
unified visibility:

- All AI subscriptions (auto-detected from Gmail)
- Claude usage (auto-parsed from local logs)
- Cross-provider (OpenAI/Cursor/Gemini coming via browser extension)
- App activity (foreground tracking for ROI per hour-of-use)
- Multi-currency native (30+ via ECB rates)

Other tools give fragments. Pulse gives the whole picture.

Also: pulse is free + open source + MIT.
```

---

## "How is this different from Anthropic Console?"

```
Anthropic Console is the official org-level dashboard for direct-API users.
Free for orgs. Doesn't work for:

- Individual Claude Pro / Max plan users (no Console access)
- People on Bedrock / Vertex / Foundry (Anthropic doesn't see those calls)
- People using Claude alongside ChatGPT / Cursor / Gemini

Pulse parses your local `~/.claude/projects/*.jsonl` directly, so it works
for every Claude user regardless of provider. Plus it adds subs + activity +
multi-currency that Console doesn't have.

Think of it as: Console for the org, Pulse for the person.
```

---

## "Why Python / Streamlit instead of [React / Tauri / Electron]?"

```
Three reasons:

1. Speed of iteration. Streamlit lets me ship a polished dashboard in 200
   lines of Python vs 2000 lines of React.

2. The user is already running Python. Pulse parses Claude Code logs which
   are Python-native. Same runtime = no IPC.

3. Cross-platform comes free. Streamlit + pystray + Win32 ctypes works on
   Windows day-one. macOS/Linux is one file of platform shims away
   (platform_compat.py already in the repo).

Tauri was tempting but the bundle size + Rust learning curve didn't pay
off for v1. Maybe v2 if there's demand.
```

---

## "How do you make money?"

```
Pulse Free is free forever for local use. No telemetry, no upsells, no
"premium features" gated.

Pulse Pro ($9/mo) launches with Cloud sync (E2E encrypted) — for cross-
device, mobile companion, leaderboard, cross-provider tracking. Optional.

Pulse Team ($19/seat) is for 5-50 dev teams who want shared dashboards
and per-user attribution. Slack/Teams integration.

Pulse Enterprise ($199/seat) adds SSO, SOC 2, custom roles.

Free is genuinely free. The freemium hooks are cloud sync + multi-device
+ team features. If you only use one machine, you never need to pay.

Roadmap: github.com/walight999/pulse/blob/main/ROADMAP.md
```

---

## "Does it support [OpenAI / Cursor / Gemini]?"

```
Today: Claude usage parsing (from local logs) + manual subscription tracking
for any provider (you type in the cost + cycle).

Coming in v1.1 (next 30 days):
- OpenAI API key usage via /v1/usage endpoint
- Cursor IDE local state DB parsing
- Gemini AI Studio API
- GitHub Copilot via GraphQL audit log
- Browser extension capturing chat.openai.com, claude.ai, gemini, perplexity
  web sessions (metadata only — model, timestamp, length)

Code is scaffolded in `providers/` and `browser-ext/`. PRs welcome.
```

---

## "Privacy concerns about parsing logs?"

```
Valid question. Pulse only reads (never writes to) `~/.claude/projects/`.

Specifically, it parses `.jsonl` files that Claude Code itself writes. These
files are already on your disk — Pulse is just reading what's already there
and showing it back to you in a nicer view.

Per-conversation message text is NOT stored in pulse's own database. We
only persist the metadata: model name, token counts, cache splits, project
tag (the `cwd`), timestamp.

If you want, you can `grep` the pulse DB schema to verify:
github.com/walight999/pulse/blob/main/db.py

Or check what we ingest: github.com/walight999/pulse/blob/main/sync_tokens.py
```

---

## "Will you add bank integration?"

```
On the roadmap. Plaid for US bank accounts in v1.5 (Q3-Q4 2026).

For Thailand: working on KBank / SCB / Krungsri scrapers since Plaid
doesn't cover Asian banks. Will probably ship Thailand-first since
that's where I'm based.

This is opt-in. Free tier never needs banking. It's a Pro feature for
catching AI subs that don't go through Gmail (e.g., paid via Stripe direct
or Apple/Google in-app).
```

---

## "Why 'Mint for AI era' positioning?"

```
Mint (RIP 2024) was the canonical personal finance dashboard. It taught a
generation to see their money. The category went vacant when Intuit shut it
down.

Meanwhile we all started paying real money for AI tools — $9/mo to $200/mo
each, often 4-6 simultaneously. By 2027 that's likely 10+ for the average
prosumer.

Bank apps don't categorize "AI" — they just show a Stripe charge from
"Anthropic, Inc." or "Cursor AI Inc." with no context.

Pulse exists to be the bookkeeper for that spending — automatically, with
ROI context, with cancellation prompts when you stop using something.

Mint did this for groceries and gym memberships. Pulse does it for AI.
```

---

## "Roadmap?"

```
Full roadmap: github.com/walight999/pulse/blob/main/ROADMAP.md

Quick version:

v1.0 (now) — Windows tray + dashboard + Claude parser + subs + activity
v1.1 (30d) — Multi-provider parsers (OpenAI/Cursor/Gemini/Copilot)
v1.2 (60d) — macOS + Linux native ports
v2.0 (Q3) — Cloud sync (Supabase) + PWA mobile + leaderboard
v3.0 (Q4) — Pulse Team + Enterprise + Pulse SDK

Free tier features land first, then Pro features. Everything is MIT.
```

---

## "Can I self-host the cloud?"

```
Yes, that's the plan. When Pulse Cloud launches we'll ship a Docker Compose
that runs the same Supabase schema + API server + sync protocol locally.

Self-hosted Pulse Cloud will be free. Hosted Pulse Cloud is $9/mo because
you pay us to run Postgres, push notifications, etc.

Trade-off: self-hosted means you maintain your own backups, TLS, etc.
Hosted = we handle that.
```

---

## "Is the AI usage thing actually accurate?"

```
Yes — to the cent.

Most tools have 10-15% errors because:

1. They use one flat cache_creation rate. Anthropic charges differently for
   5-minute vs 1-hour cache tokens. Pulse splits these correctly.

2. They count multi-block messages multiple times (same request_id). Pulse
   dedupes on `request_id` UNIQUE constraint.

3. They use stale pricing. Pulse's pricing matrix is in `sync_tokens.py:PRICING`
   and gets updated when Anthropic announces new prices.

I cross-checked against ccusage (CLI tool) and we match within 0.1%.
The difference is real — multi-block dedupe alone is ~5% on heavy users.
```

---

## "Anthropic might just build this natively"

```
Possible. But:

1. Anthropic Console is org-tier only. They've shown no interest in
   consumer-facing analytics.

2. Pulse is cross-provider (Claude + OpenAI + Cursor + Gemini). Anthropic
   has no incentive to build that.

3. Pulse is local-first + privacy-focused. Anthropic's analytics naturally
   live in their cloud.

4. Pulse is the wallet, not the gateway. We're a complement, not a competitor.

Even if Anthropic ships native consumer analytics for Claude specifically,
Pulse's multi-provider + multi-modal (subs + activity + usage) view stays
defensible.
```

---

## Critical / hostile responses

### "This is just a glorified spreadsheet"

```
Fair critique. The differentiation is:

1. Auto-detection from Gmail receipts (saves data entry)
2. Auto-parsing of Claude logs (saves more data entry)
3. ROI computation with current Anthropic pricing (saves math)
4. Renewal alerts (saves money)
5. Cross-machine sync (Pulse Cloud, opt-in)

If you're happy with a spreadsheet, you don't need pulse. But once your AI
sub count hits 5+ and you're paying for tools you don't use, the auto-
detection alone pays for itself.
```

### "Why would I trust a sole-founder side project with my data?"

```
You don't have to. Pulse is local-first — your data never leaves your machine.
The code is MIT licensed and auditable.

When Pulse Cloud ships (Q3 2026), you'll have three choices:
1. Free local only (most users)
2. Hosted Pulse Cloud (E2E encrypted, opt-in)
3. Self-hosted Pulse Cloud (run your own Supabase)

You don't pay anything until you actively choose to sync to a cloud.
And we genuinely can't see your data even if you do.
```

### "This is just self-promotion"

```
Fair. Show HN is meant for self-promotion of MIT-licensed projects, but I
hear you.

What would have made this post less promotional and more useful for you?
Genuinely asking — first time launching anything publicly.
```

(This response works because it's vulnerable + invites real conversation)

---

## Response timing strategy

- First 30 min: reply to every comment within 5 min
- 30 min - 4 hours: reply within 30 min
- 4-24 hours: reply within 2 hours
- 24-48 hours: daily check, reply to substantive comments
- 48+ hours: weekly summary tweet, response to issues becomes async

## What NOT to do

- ❌ Don't argue with hostile commenters past 2 exchanges
- ❌ Don't reply with corporate-speak ("we appreciate your feedback")
- ❌ Don't link to landing page in every reply (HN hates this)
- ❌ Don't deflect to roadmap when current pain is valid
- ❌ Don't promise features publicly that aren't on the roadmap

## What WORKS on HN

- ✅ Specific technical detail (HN values precision)
- ✅ Acknowledging trade-offs explicitly
- ✅ Vulnerable / honest tone (vulnerability is a flex)
- ✅ Linking to specific source files when discussing implementation
- ✅ Saying "I don't know yet" when you don't
- ✅ Asking what would make it better (genuine curiosity)
