# Deploy Readiness — pulse

> Generated 2026-05-11 as part of `/deploy-agent-routines` Pipeline v2 retroactive activation.

---

## Agent roster (8 agents — Maa/CHUM pattern)

All agents defined in `.claude/agents/` as separate `.md` files with Claude Code front-matter (name, description, tools).

| ID | Agent | File | Skill |
|----|-------|------|-------|
| A1 | CEO | `.claude/agents/pulse-ceo.md` | `/ceo` |
| A2 | PM | `.claude/agents/pulse-pm.md` | `/pm` |
| A3 | Marketing | `.claude/agents/pulse-marketing.md` | `/marketing` |
| A4 | Designer | `.claude/agents/pulse-designer.md` | `/designer` |
| B1 | Lead Engineer | `.claude/agents/pulse-lead-engineer.md` | `/dev` |
| B2 | Frontend | `.claude/agents/pulse-frontend.md` | `/dev` |
| B3 | Backend | `.claude/agents/pulse-backend.md` | `/dev` |
| B4 | DevOps | `.claude/agents/pulse-devops.md` | `/ops` |

## Prerequisites for full deploy-agent-routines

- [x] `.claude/agents/` with 8 `.md` files (DONE today)
- [x] Notion HQ + 5 sub-pages structure (DONE)
- [ ] Personal HQ in Notion (separate workspace — required for multi-company stack)
- [ ] Make.com (Integromat) MCP connector (required for cron scenarios)
- [ ] LINE / Slack channel for daily White's Brief (required for delivery)
- [ ] Company HQ Roadmap database in Notion (currently HQ page only, not DB)
- [ ] Action Items DB in Notion (currently roadmap text only)
- [ ] Personal Chief of Staff agent profile (separate from Pulse agents)

## What's ready vs not

### ✅ Ready

- Agent definitions (8 agents with clear scope + tools + invocation patterns)
- Notion Company HQ + 5 sub-pages structure
- Brand voice constraints documented
- Audit log table in DB for security events

### ⏳ Not ready (requires user setup)

- Personal HQ (Notion workspace for founder personal life vs companies)
- Make.com scenarios (daily aggregation, briefing splitter, weekly synthesizer)
- LINE/Slack delivery channel
- Notion databases (Roadmap, Action Items) — currently pages only
- Personal Chief of Staff agent

## Current mode

**Solo OSS / passive mode** per `CLAUDE.md`:

> No agent roster, no `deploy-readiness.md`. Solo-OSS model still applies.

Today's update **changes this** — agent roster now exists. Solo founder can invoke any of the 8 agents via Claude Code skill (e.g., `/dev` activates B1/B2/B3 context, `/marketing` activates A3, etc.).

Full autonomous mode (cron + brief delivery) requires the 6 unchecked prerequisites above.

## Activation paths

### Path 1 — Manual agent invocation (works today)

```
User: /ceo should we ship feature X?
Claude: (reads pulse-ceo.md context) → strategic decision

User: /dev implement parser for OpenAI
Claude: (reads pulse-backend.md context) → implementation
```

### Path 2 — Semi-autonomous (requires Make.com setup)

- Daily cron at 07:30 ICT aggregates GitHub issues + Notion Action Items
- Personal CoS agent generates White's Brief
- Sends to LINE/Slack
- White reviews + delegates back via DM to specific agents

### Path 3 — Full autonomous (requires Phase 2 cloud + Notion DBs)

- Action Items DB tracks each task
- Each agent runs scheduled jobs (Marketing posts at 14:00 ICT, DevOps checks deploys at 18:00 ICT, etc.)
- Critical-bypass escalation: P0 alerts bypass daily brief and go direct to founder
- Weekly synthesis aggregates all agent outputs into Sunday review

## Recommendation

For pulse v1.0 launch (May 26/28), **Path 1 is sufficient**. Solo founder + 8 agents on-demand.

After launch:
- If 100+ stars → Path 2 setup (Make.com + LINE) to scale operations without hiring
- If 1,000+ stars → Path 3 setup (cloud + Notion DBs + full autonomy)

## Next deploy actions (when activating Path 2)

1. Create Personal HQ in Notion (separate workspace)
2. Set up Make.com account + Notion + LINE MCP connectors
3. Create Personal Chief of Staff agent (`personal-cos.md` in `.claude/agents/`)
4. Create cron scenario: daily aggregation 07:00 ICT → brief at 07:30 ICT
5. Test brief delivery to LINE
6. Iterate weekly

## Sign-off

- Agent definitions reviewed: 2026-05-11
- Pulse CEO approval needed for: Path 2 activation (when stars > 100)
