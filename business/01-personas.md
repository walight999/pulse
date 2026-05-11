# 🎯 Pulse — Personas

Three target personas, ranked by adoption priority. Each persona drives different feature requests, pricing perception, and growth channels.

---

## P1 — "The AI Power User" (primary)

**Profile**: Software engineer or designer, 28–42, pays for 4–6 AI tools monthly.

**Current stack**:
- ChatGPT Plus $20/mo
- Claude Max $200/mo (or Pro $20/mo)
- Cursor Pro $20/mo
- GitHub Copilot $10/mo (work-paid or personal)
- 1–2 niche tools (Perplexity Pro, Lovable, v0, Replit Core)

**Total AI spend**: $250–$400/mo

**Pain points**:
- "I have no idea if Claude Max is worth $200 vs paying per-API."
- "Every month a charge hits and I forget what it's even for."
- "I keep meaning to cancel [thing I haven't used in 2 months] but never get around to it."
- "I want to see all my AI spending in one place without a spreadsheet."

**What they want from Pulse**:
1. Auto-detection of every AI subscription
2. Real Claude ROI vs API equivalent
3. One-click cancel links
4. Streak / progress feedback to feel good about usage habits

**Why they buy Pro ($9/mo)**:
- Cross-device (laptop + phone)
- Mobile companion to check spend on the go
- Browser extension to capture web-based AI sessions

**Channel to reach them**:
- Show HN (highest leverage)
- r/ClaudeAI, r/ChatGPT, r/LocalLLaMA
- Twitter (especially AI dev community)
- Discord — Anthropic Discord, Cursor Discord, indie hacker servers

**Conversion proof point**: "Pulse showed me my $200 Claude plan returned $4,127. I almost cancelled it last month."

---

## P2 — "The Curious Prosumer" (secondary)

**Profile**: Marketer, founder, content creator, or product manager, 30–48. Uses AI tools daily but doesn't think of themselves as "technical."

**Current stack**:
- ChatGPT Plus $20/mo
- Claude Pro $20/mo
- Maybe Perplexity Pro $20/mo
- Notion AI add-on $10/mo
- Lovable / v0 / Cluely / etc (whichever is hot this month)

**Total AI spend**: $80–$150/mo

**Pain points**:
- "I keep signing up for AI tools and never actually use most of them."
- "My bank statement has 5 things I don't recognize this month."
- "How do I know which tools are actually saving me time?"

**What they want from Pulse**:
1. Subscription tracker with smart auto-detect
2. Cancellation reminders
3. Simple "this is your AI bill this month" view
4. Not too technical — just clean numbers

**Why they buy Pro ($9/mo)**:
- Mobile companion (they're not at a desk all day)
- Friend leaderboard (slight gamification)
- Receipt OCR (snap a photo of a receipt)

**Channel to reach them**:
- Product Hunt launch (less technical than HN)
- IndieHackers
- Twitter (productivity community)
- Newsletter mentions (Daring Fireball, Stratechery)

**Conversion proof point**: "Pulse caught 3 subscriptions I forgot I had. Saved me $80/month."

---

## P3 — "The Dev Team Lead" (tertiary, Pro Team tier)

**Profile**: Engineering manager or CTO at a 5–50 person company. Sees the team's collective Claude/Copilot bill but doesn't know per-developer breakdown.

**Current stack**:
- Claude Code on Anthropic API (or Bedrock/Vertex)
- GitHub Copilot Business
- ChatGPT Team
- Various dev-side tools (Cursor seats, Sourcegraph Cody)

**Total team AI spend**: $1,000–$10,000/mo

**Pain points**:
- "I see $3,000 from Anthropic on our card. No idea which devs are using how much."
- "Anthropic Console only works if everyone uses direct API."
- "We're on Bedrock so we don't get usage metrics back from Anthropic."
- "I need to attribute AI cost to projects for client billing."

**What they want from Pulse**:
1. Per-developer attribution (Pulse Team tier)
2. Slack digest of weekly team spend
3. Cost-by-project for client billing exports
4. CSV/PDF for finance

**Why they buy Team ($19/seat/mo)**:
- Replaces $50/dev burden of building internal dashboards
- Slack/Teams integration saves them building it
- One-tool consistency across team

**Channel to reach them**:
- r/sysadmin posts
- ClaudeMetrics direct comparison content
- Direct outreach via LinkedIn
- Anthropic Discord (engineering team conversations)

**Conversion proof point**: "We caught one dev burning $400/wk on Opus when Sonnet would've worked. ROI on Pulse Team paid for itself in week one."

---

## Anti-personas (do NOT target)

- **Enterprise procurement** (Phase C only — too slow buying cycle for v1)
- **Casual consumers** with 1–2 AI subs (TAM too small, not pain-aware)
- **Pure hobbyists** who don't pay for AI (not addressable)
- **Bedrock/Vertex enterprise-only orgs** (ClaudeMetrics serves them better)

---

## Persona-driven feature priority

| Feature | P1 weight | P2 weight | P3 weight | Priority |
|---------|----------|----------|----------|----------|
| Plan ROI hero | 10 | 7 | 5 | P0 |
| Subscription auto-detect | 9 | 10 | 6 | P0 |
| Claude log parsing | 10 | 4 | 9 | P0 |
| Cancellation tracker | 7 | 10 | 4 | P0 |
| Multi-provider (OpenAI/Cursor) | 9 | 7 | 8 | P1 |
| Mobile companion | 6 | 9 | 3 | P1 |
| Friend leaderboard | 6 | 8 | 2 | P2 |
| Per-dev attribution | 2 | 1 | 10 | P2 (Team tier) |
| Slack digest | 3 | 4 | 9 | P2 (Team tier) |
| SSO/SAML | 0 | 0 | 6 | P3 (Enterprise) |

Phase 1 (M1–M3) focus: top 4 P0 features for P1 + P2.
Phase 2 (M3–M6) focus: P1 features for cross-device.
Phase 3 (M6+): P2 features for Team tier monetization.

---

*Source of truth for "who pulse is for." Update only after substantive user research.*
