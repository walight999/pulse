# 🎯 Pulse MVP — Build Prompt (Mega-Prompt)

For pasting into Claude Code or another LLM coding agent when rebuilding from scratch
or extending the v1.0 codebase. This consolidates PRD + tech spec + UX spec into a
single executable brief.

---

## Role

You are the lead engineer building **Pulse** — a local-first personal-finance dashboard
for the AI era. Your job is to ship working code that matches the spec exactly.

## Context

- Repo: https://github.com/walight999/pulse
- Status: v1.5 in production (10 commits, ~180 files, ~14k lines)
- Tech: Python 3.12, Streamlit 1.57, SQLite, Plotly, Win32 ctypes
- Owner: White (@walight999)
- Working dir: `C:\Users\usEr\life-tracker\`

## Brand identity (do not deviate)

- Wordmark: **"pulse"** lowercase, letter-spacing -0.03em
- Tagline: **"Mint for the AI era"**
- Colors: INK `#0A0A0F` · INK_SOFT `#17171C` · PAPER `#FAFAF7` · PULSE `#00E5A0` (dark) · `#00C58A` (light AA-safe) · SLATE `#6B6B6B`
- Display font: Inter Tight 500/600
- Mono font: JetBrains Mono 400

## Architecture

Read `product/pulse/02-tech-spec.md` for the full layered architecture. In short:

1. `app.py` — Windows tray + 4 background daemons + Streamlit launcher
2. `dashboard.py` — All UI rendering (5 pages: Overview / Subscriptions / Activity / AI usage / Settings)
3. Domain modules: `db.py`, `theme.py`, `tracker.py`, `sync_tokens.py`, `fx.py`, etc.
4. Optional cloud: `cloud/`, `api/`, `sdk/` (Phase 2+, scaffolded)

## Acceptance criteria (per `product/pulse/01-prd.md`)

All US-01 through US-22 must work in the running app. Specifically:

### Subscriptions
- Auto-detect via `discover_subscriptions.py` (Gmail MCP)
- Smart status (active/wasted/likely-cancelled/cost-not-set/history)
- Renewal alerts via `alerts.py` background daemon
- Lifetime savings tracker on cancelled subs
- Multi-currency native (30+ via `fx.py`)
- One-click cancel URL link

### AI usage
- Parse `~/.claude/projects/*.jsonl` in `sync_tokens.py`
- Dedupe by `request_id`
- Accurate split: `cache_creation_5m_tokens` × 1.25 + `cache_creation_1h_tokens` × 2 × input rate
- Plan ROI hero with 5-tier rating (Legendary/Excellent/Great/Plan paying off/Underused/Plan idle)
- 7×24h heatmap with mint intensity scale
- Time-series chart with bars colored by % of daily budget

### Activity
- Foreground app via Win32 `GetForegroundWindow` (or `osascript` on macOS via `platform_compat.py`)
- Idle via `LASTINPUTINFO` (or `ioreg` on macOS, `xprintidle` on Linux)
- Auto-categorize via `categories.py`
- Top apps list with gradient bars (productive vs distraction)

### System
- Tray app in `app.py` with single-instance lock (socket bind port 8500)
- Light + dark themes in `theme.py` (CSS variables, no cache clear on toggle)
- Daily backup rotation in `backup.py` (last 7 kept)
- Audit log in `db.log_audit()`

## UX requirements (per `product/pulse/03-uxui.md`)

- 5 pages with sidebar nav (Overview/Subscriptions/Activity/AI usage/Settings)
- Sidebar fixed 250px width with smooth fold animation
- Logomark: black square + white P + animated mint pulse line (via CSS pseudo elements)
- ECG line decoration below greeting on Overview
- Plan ROI hero moved to TOP of AI usage + Overview pages
- All Streamlit components themed for both light + dark modes
- All tables use `pulse_table()` helper (not `st.dataframe`) for theme consistency
- Empty states use `pulse_empty()` helper with SVG icons
- All animations respect `prefers-reduced-motion`

## Code quality rules

- **No emoji walls** — max 1 emoji per code section
- **Tabular numerics** — all financial figures use `font-variant-numeric: tabular-nums`
- **Idempotent migrations** — every schema change in `db.py:MIGRATIONS` must silently no-op if column exists
- **No vague benefits** — UI copy always shows specific numbers ($4,300 saved, 10.5× return)
- **Local-first** — zero network calls except optional FX + opt-in Gmail MCP
- **Privacy** — no telemetry, no analytics, no fingerprinting
- **MIT licensed** — every file inherits MIT, never include non-permissive code

## How to extend (build path)

1. **Read these files in order before coding**:
   - `README.md` (project overview)
   - `product/pulse/01-prd.md` (what + why)
   - `product/pulse/02-tech-spec.md` (how)
   - `product/pulse/03-uxui.md` (design)
   - `business/02-brand.md` (visual identity)
   - `business/04-offers.md` (pricing)
   - `ROADMAP.md` (phase plan)

2. **Run locally**:
   ```bash
   pip install -r requirements.txt
   python app.py
   # Or headless dev:
   streamlit run dashboard.py --server.port 8501
   ```

3. **Make changes**:
   - Edit files in place (don't reorganize)
   - Run syntax check: `python -c "import ast; ast.parse(open('dashboard.py').read())"`
   - Restart Streamlit (config has `runOnSave=false`)
   - Hard-refresh browser (Ctrl+Shift+R) to clear CSS cache

4. **Test**:
   - Manual: click through every page in both light + dark mode
   - Verify all 22 user stories work
   - Cold-install on fresh VM before any release

5. **Commit + push**:
   - Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
   - Push to `walight999/pulse` main branch

## Common pitfalls (don't fall into these)

1. **Don't add cloud features without env vars guard** — `cloud/` modules must gracefully degrade when SUPABASE_URL/KEY missing.
2. **Don't use `st.dataframe` for theme-critical tables** — Glide grid ignores CSS vars. Use `pulse_table()` helper.
3. **Don't clear `st.cache_data` on theme toggle** — only CSS changes, data is the same. Causes jarring full-page reload.
4. **Don't break the brand row CSS** — `.pulse-logo-mark::before` (the "P") and `::after` (the pulse line) are CSS-generated. Don't add a literal "P" inside the div.
5. **Don't use Capital "Pulse" in body copy** — always lowercase "pulse" per brand spec.
6. **Don't add comments that just repeat what the code does** — comment only when WHY is non-obvious.
7. **Don't make sidebar resizable** — locked at 250px per brand spec, drag handle CSS-hidden.

## What "done" looks like

A working v1.x release means:

- [ ] All 22 user stories pass manual testing
- [ ] Light + dark mode both visually consistent
- [ ] No Streamlit branding visible (footer, deploy button, viewer badge)
- [ ] All CSV exports work
- [ ] Notifications fire correctly (Windows toast on Win)
- [ ] Tray app runs in background without DOS box visible
- [ ] Single-instance lock works
- [ ] Backups rotate correctly
- [ ] Audit log captures sensitive events
- [ ] Theme toggle smooth (no flicker)
- [ ] No syntax errors
- [ ] Brand identity preserved everywhere

## Done criteria for new features

Every new feature must include:

1. Code (in correct module per `product/pulse/02-tech-spec.md`)
2. Schema migration (if DB changes)
3. UI integration (per `product/pulse/03-uxui.md`)
4. Settings exposure (if user-configurable)
5. CHANGELOG entry
6. Audit log call (if security-relevant)
7. Manual test pass on Windows
8. Commit with descriptive message

## Reference materials

- `pulse-brand-core/output/README.md` — brand do's/don'ts + asset locations
- `docs/MICROSOFT.md` — acquisition pitch + talking points
- `docs/SHOW_HN.md` — launch copy + 3 angles
- `docs/LAUNCH_CHECKLIST.md` — T-7d → T+90 runbook
- `marketing/twitter-warmup-tweets.md` — 10 warm-up tweets ready to post
- `marketing/beta-tester-outreach.md` — 4 DM templates
- `marketing/hn-faq-bank.md` — 14 pre-written HN responses

## Execution mode

If asked to **build a new feature**: read PRD → write code → write test plan → ship.

If asked to **fix a bug**: reproduce → minimize → instrument → fix → regression test.

If asked to **refactor**: only if it removes complexity without changing behavior.

If asked to **add a provider parser** (OpenAI/Cursor/etc.): scaffold in `providers/`, follow existing `sync_tokens.py` pattern, add to migrations, expose in dashboard.

**Always** commit incrementally. **Always** preserve brand identity. **Always** check syntax before declaring done.
