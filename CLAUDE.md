# pulse (life-tracker) — Root CLAUDE.md

> Local-first desktop dashboard for AI spend, subscriptions, and productivity.
> **Pipeline version:** v2 (added 2026-05-11 — lean-launch-audit baseline)
> **Stage:** S2 — Soft Launch (v1.0 preview)
> **Wedge:** AI-Native — only tool that correlates subscription cost + AI token spend + actual usage time

---

## Repository Type

This is **not** `/idea-to-mvp` output. It's a working Streamlit application (Python + SQLite) with associated landing page (Next.js) and browser extension. Most of the structure precedes the skill-pipeline.

Pipeline v2 added retroactively:
- `lean-launch-audit.md` — 9-step lean audit applied to existing stack
- No `deploy-readiness.md` (no `.claude/agents/`, solo-builder mode)
- No Foundation files (01-personas etc.) — README + ROADMAP serve as Business OS substitute

If Pulse adds a Pro tier with paying users → consider running `/idea-to-mvp` retroactively to add Foundation + agents for marketing/support.

---

## Folder Map

```
life-tracker/                       # repo root (named "pulse" in README)
├── README.md                       # product overview
├── ROADMAP.md                      # v1.0 → v1.1 → v1.2 → v2.0 plan
├── CHANGELOG.md                    # version history
├── CONTRIBUTING.md
├── LICENSE                         # MIT
├── PRIVACY.md                      # privacy policy (local-first)
├── TERMS.md
├── SECURITY.md
├── lean-launch-audit.md            # ← Pipeline v2 (2026-05-11)
├── CLAUDE.md                       # ← this file (Pipeline v2)
├── docs/                           # LAUNCH_CHECKLIST, MICROSOFT, SHOW_HN
├── api/                            # internal API for daemons
├── assistant/                      # in-app AI assistant
├── backups/                        # auto-rotated SQLite backups
├── browser-ext/                    # Chrome/Firefox/Edge extension
├── cloud/                          # OPTIONAL cloud sync (must be opt-in)
├── data/                           # SQLite + assets
├── integrations/                   # 3rd-party API integrations
├── landing/                        # Next.js landing page
├── logs/
├── marketing/                      # launch templates (HN, Twitter, Reddit, etc.)
├── app.py                          # entrypoint
├── dashboard.py                    # main Streamlit UI
├── db.py                           # SQLite layer
└── *.py                            # feature modules
```

---

## Read Order for New Sessions

1. **`STATE.md`** ← read first (single-page state — stage, capacity, next gate, top 3 TODOs, Notion sync)
2. `README.md` — product overview
3. `ROADMAP.md` — current vs upcoming
4. `lean-launch-audit.md` — Step 0 capacity warning + Step 3 anti-pattern flags (telemetry audit + cloud opt-in verification)
5. `docs/LAUNCH_CHECKLIST.md` — pre-Show-HN tasks
6. `docs/SHOW_HN.md` — drafted Show HN post

---

## Active Constraints (per audit)

- **Capacity:** 4 active projects (≥3 ceiling). Pulse runs in **passive mode** — no daily content cadence, GitHub-led growth
- **Stack:** Streamlit + SQLite (local) + Next.js landing + browser-ext. No cloud infra at v1.0 = $0 marginal cost ✓
- **Promotion gate to S3:** >100 GitHub stars + >10 external install reports + 1+ inbound feature request

---

## Audit Action Items (from lean-launch-audit.md)

Top 3 before Show HN post:
1. Audit code for unauthorized telemetry (`grep -r "requests.post\|httpx.post\|analytics"`)
2. Verify cloud features are opt-in only (run UI with cloud disabled)
3. Add Code of Conduct + GitHub issue templates → better first impression for HN traffic

---

## Don't List

- ❌ Forced cloud signup at any tier (breaks "100% local" claim)
- ❌ Implicit telemetry without opt-in
- ❌ Auto-update without user consent
- ❌ Pro tier marketing before v1.1 ships multi-provider
- ❌ Native iOS app (PWA / web preferred per pipeline)

---

## Skill Pipeline Status

- **`/lean-launch-stack`** — ✅ ran 2026-05-11 → `lean-launch-audit.md` + this file
  - 3 action items: ✅ telemetry audited (no unauthorized POST) · ✅ cloud opt-in verified (leaderboard, telemetry, sync all opt-in) · ✅ CoC + 3 issue templates + PR template added
  - Re-run if adding Pro tier (Stripe compliance) or when cloud sync ships
- **`/deploy-agent-routines`** — ✅ Path 1 ready 2026-05-11 → `.claude/agents/` (8 agents) + `deploy-readiness.md`
  - Solo founder can invoke `/ceo`, `/pm`, `/marketing`, `/designer`, `/dev`, `/ops` with pulse-specific context loaded
  - Path 2 (Make.com cron + LINE brief) deferred until >100 stars
  - Path 3 (full autonomy + Notion DBs) deferred until >1,000 stars
- **`/idea-to-mvp`** — only if Pulse pivots to multi-person team or full company structure (currently solo OSS — overkill)

---

## Notion HQ (verified 2026-05-11)

Pulse **does** have a Notion HQ — discovered during Pipeline v2 sync. HQ tracks build progress v1.0 → v1.5 + Show HN launch playbook.

- **HQ root:** https://www.notion.so/35d9defb952981848312e64e6823571b
- **Pipeline v2 sub-page:** https://www.notion.so/35d9defb952981b8aa92de940faca7c5

Earlier note in STATE.md said "no Notion HQ" — that was incorrect. Pulse HQ exists and v2 update has been pushed there. Solo-OSS model still applies (no agent roster, no `deploy-readiness.md`).
