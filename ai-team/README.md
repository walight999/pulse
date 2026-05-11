# 🤖 Pulse — AI Team

Eight AI agents organized in two tracks. Each agent has a clear scope, owns specific deliverables, and can be invoked via Claude Code skill.

---

## Track A — Business agents (4)

These keep the business side of Pulse running.

### A1. CEO — Strategic decision-maker

**Owns**: Roadmap, pricing, acquisition strategy, vision.

**Invokes**: When making decisions that affect direction (defer Phase B, change pricing tier, target acquirer).

**Outputs**: Decision logs, strategic memos, board-style updates.

**Files**: `business/00-executive-summary.md`, `business/04-offers.md`, `docs/MICROSOFT.md`

### A2. PM — Product manager

**Owns**: PRD, sprint planning, feature prioritization, triage.

**Invokes**: When defining a new feature, breaking work into issues, deciding what ships next.

**Outputs**: PRDs, user stories, acceptance criteria, sprint plans.

**Files**: `product/pulse/01-prd.md`, GitHub issues

### A3. Marketing — Growth + brand voice

**Owns**: Twitter, Reddit, Show HN, email, Discord, Pulse Pro waitlist.

**Invokes**: When writing public-facing copy or planning a campaign.

**Outputs**: Tweets, posts, email templates, launch playbooks.

**Files**: `marketing/twitter-warmup-tweets.md`, `marketing/twitter-launch-thread.md`, `marketing/beta-tester-outreach.md`, `marketing/hn-faq-bank.md`, `marketing/reddit-crosspost-templates.md`, `marketing/discord-server-template.md`, `marketing/welcome-email.html`, `marketing/email-signature.html`, `marketing/invoice-template.html`

### A4. Designer — Brand + UX consistency

**Owns**: Brand assets, design system, UX critiques, visual identity.

**Invokes**: When adding new visual elements, redesigning a page, generating brand assets.

**Outputs**: Brand assets (via `pulse-brand-core/`), CSS specs, design critiques.

**Files**: `business/02-brand.md`, `product/pulse/03-uxui.md`, `pulse-brand-core/`

---

## Track B — Development agents (4)

These build and maintain the technical product.

### B1. Lead Engineer — Architecture + code review

**Owns**: Module layout, tech decisions, code review standards.

**Invokes**: When making architectural changes, choosing libraries, reviewing PRs.

**Outputs**: Architecture decisions, tech spec, refactor plans.

**Files**: `product/pulse/02-tech-spec.md`, `ROADMAP.md`

### B2. Frontend Engineer — UI implementation

**Owns**: `dashboard.py`, `theme.py`, all Streamlit + Plotly + CSS work, landing page (Next.js).

**Invokes**: When building/fixing UI, theming components, polishing visual feedback.

**Outputs**: Streamlit page renders, Tailwind landing pages, browser-ext popup UI.

**Files**: `dashboard.py`, `theme.py`, `landing/app/page.tsx`, `landing/app/layout.tsx`, `static/manifest.json`, `static/sw.js`, `static/offline.html`, `browser-ext/popup.html`

### B3. Backend Engineer — Data, integrations, cloud

**Owns**: `db.py`, `sync_tokens.py`, `cloud/`, `api/`, `integrations/`, `providers/`.

**Invokes**: When wiring new data sources, building integrations, extending the schema.

**Outputs**: Database migrations, parser implementations, integration code, REST endpoints.

**Files**: `db.py`, `sync_tokens.py`, `cloud/*.py`, `api/server.py`, `integrations/*.py`, `providers/*.py`, `sdk/python/pulse_client.py`

### B4. DevOps / Release Engineer — Deploy + ops

**Owns**: Build, package, deploy, monitor. Browser extension submission, Vercel landing, Stripe products.

**Invokes**: When releasing a version, deploying landing page, submitting to Chrome Web Store.

**Outputs**: Release notes, deploy scripts, monitoring dashboards, store submissions.

**Files**: `CHANGELOG.md`, `requirements.txt`, `requirements-cloud.txt`, `landing/vercel.json`, `browser-ext/STORE_LISTING.md`, `docs/LAUNCH_CHECKLIST.md`

---

## How agents collaborate

Most decisions flow:

```
CEO (A1) ──▶ PM (A2) ──▶ Lead Engineer (B1)
                              │
                              ├─▶ Frontend (B2)
                              ├─▶ Backend (B3)
                              └─▶ DevOps (B4)

Marketing (A3) ◀──▶ Designer (A4) ─────────▶ Frontend (B2)
```

Concrete examples:

**Adding multi-provider support (OpenAI parser)**:
1. PM (A2) writes user story + acceptance in PRD
2. Lead Engineer (B1) approves architecture
3. Backend (B3) implements `providers/openai_parser.py`
4. Frontend (B2) wires UI in `dashboard.py`
5. Designer (A4) approves visual consistency
6. DevOps (B4) tags release + updates CHANGELOG

**Launching Show HN**:
1. CEO (A1) approves launch decision + timing
2. Marketing (A3) writes thread + crossposts + FAQ
3. Designer (A4) provides screenshots + GIF
4. Frontend (B2) ensures landing page is live
5. DevOps (B4) submits browser extension to stores
6. PM (A2) tracks metrics post-launch

---

## Daily rhythm (when active)

| Time | Agent | Action |
|------|-------|--------|
| 07:30 ICT | CEO | Review White's Brief (Notion) — what shipped, what's blocked |
| 09:00 ICT | PM | Triage any new GitHub issues |
| 10:00 ICT | Backend | Continue current feature (multi-provider, cloud, etc.) |
| 11:00 ICT | Frontend | Continue current feature |
| 14:00 ICT | Marketing | Post warm-up tweet (during launch warmup phase) |
| 16:00 ICT | Designer | Review any UI work shipped today |
| 18:00 ICT | DevOps | Tag any release, deploy landing changes |
| 22:00 ICT | All | Update Notion page + push to repo |

---

## Skills mapping

Each agent maps to a Claude Code skill (in `~/.claude/skills/`):

| Agent | Claude Code skill |
|-------|-------------------|
| A1 CEO | `/ceo` |
| A2 PM | `/pm` |
| A3 Marketing | `/marketing` |
| A4 Designer | `/designer` |
| B1 Lead Engineer | `/dev` |
| B2 Frontend | `/dev` (with frontend context) |
| B3 Backend | `/dev` (with backend context) |
| B4 DevOps | `/ops` |

Activate via: `/ceo`, `/pm`, etc. in Claude Code.

---

## Agent invocation patterns

### "I need to add a feature"

1. Start with `/pm` — writes user stories + acceptance criteria
2. Then `/dev` — implements
3. Then `/designer` — reviews visual
4. Then `/ops` — releases

### "I want to launch something"

1. `/ceo` — confirms strategic fit
2. `/marketing` — writes copy + plans channels
3. `/designer` — provides assets
4. `/ops` — coordinates timing

### "I found a bug"

1. `/dev` with `/diagnose` skill — reproduce + minimize + fix
2. `/ops` — release patch

### "Big strategic decision"

1. `/grill-me` — stress-test the plan
2. `/ceo` — make the call
3. Update `business/00-executive-summary.md`

---

## When to add a 9th agent

Add a new agent when:

- A discrete responsibility shows up repeatedly (e.g., "Sales" for enterprise outreach when first Team customers exist)
- An existing agent is overloaded (e.g., split Frontend → "Frontend Web" + "Frontend Mobile" when PWA + native ship)
- A specialized skill becomes routine (e.g., "Researcher" for ongoing competitive intelligence)

Do NOT add agents prematurely. 8 is already a lot for a 1-person company.

---

## Future agents (when justified)

- **A5. Sales** — when first 5 Team customers signed
- **A6. Customer Success** — when Pro user base hits 100
- **A7. Finance** — when MRR hits $5,000 (needs proper bookkeeping)
- **A8. Legal** — when first enterprise contract negotiation begins
- **B5. Data Engineer** — when leaderboard ranking computations exceed Supabase free tier
- **B6. Security Engineer** — when SOC 2 Type I audit begins
