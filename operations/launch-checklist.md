# pulse — launch master checklist

The end-to-end runbook for going from "v1.2 in repo" to "live with traction."

## T-minus 7 days

### Domain + landing
- [ ] Register `pulse.app` ($30/yr on Namecheap or $14/yr on Cloudflare)
- [ ] Set up Vercel project from `landing/` folder
- [ ] Point `pulse.app` DNS to Vercel (A + CNAME records)
- [ ] Verify SSL provisioned
- [ ] Confirm OG card renders correctly via opengraph.xyz test

### Social accounts
- [ ] Reserve `@pulse_app_ai` on Twitter/X
- [ ] Reserve `@pulse.app` on Bluesky
- [ ] Reserve `pulse-app` on GitHub org (if not already taken)
- [ ] Set up `hi@pulse.app` email forward via your domain provider
- [ ] Apply email signature from `marketing/email-signature.html`

### Repo polish
- [ ] Add 3-5 screenshots to README (hero, dashboard, ROI card, dark mode, mobile)
- [ ] Generate 30-second demo GIF (OBS Studio → ffmpeg compress)
- [ ] Pin issue: "v1.1 roadmap — multi-provider parsers"
- [ ] Add CODE_OF_CONDUCT.md (Contributor Covenant standard)
- [ ] Add GitHub topics: `personal-finance`, `ai`, `claude`, `dashboard`, `local-first`, `streamlit`

### Backend prep (optional for launch, required for Pro)
- [ ] Create Supabase project (free tier OK initially)
- [ ] Run schema migrations (cloud tables, RLS policies)
- [ ] Create the 5 RPC functions referenced in `cloud/*.py`
- [ ] Generate `SUPABASE_URL` + `SUPABASE_ANON_KEY`, store in 1Password
- [ ] Stripe dashboard — create 4 products (Free is just a flag): Pro $9, Pro Annual $89, Team $19/seat, Enterprise $199/seat
- [ ] Store Stripe IDs in `cloud/billing.py` PRICE_* constants

## T-minus 3 days

### Pre-launch validation
- [ ] Cold install on a fresh Windows VM — works?
- [ ] Onboarding flow takes < 60 seconds?
- [ ] First-time Claude log import is automatic?
- [ ] Dark mode and light mode both look polished?
- [ ] Browser extension loads via Load Unpacked without errors?

### Content ready
- [ ] Show HN post drafted (pick angle from `docs/SHOW_HN.md`)
- [ ] Twitter thread drafted (`marketing/twitter-launch-thread.md`)
- [ ] LinkedIn post drafted (one paragraph for professional network)
- [ ] r/ClaudeCode crosspost drafted
- [ ] r/sysadmin crosspost drafted

### Outreach list
- [ ] 10 friends/colleagues for warm DM 4 hours before HN post
- [ ] 5 influencers / journalists for "exclusive preview" DM 24 hours before
- [ ] Email list of 20+ early-adopter relationships ready to receive launch email

## Launch day (T-0)

### Morning (08:00 ICT)
- [ ] Post to Twitter (full 10-tweet thread)
- [ ] Send LinkedIn post
- [ ] Email launch list (subject: "pulse just shipped")

### Mid-morning (11:00 ICT = 00:00 EST)
- [ ] Post Show HN
- [ ] DM the 10 warm friends with "I just posted — would love a comment if you can"
- [ ] Crosspost to r/ClaudeCode (link to HN, not direct)
- [ ] Crosspost to r/sysadmin

### Day-of monitoring (every 30 min, 6 hours)
- [ ] Reply to every HN comment within 30 minutes
- [ ] Quote-RT every Twitter mention
- [ ] Pin best-feedback tweet to thread
- [ ] Update Notion HQ with launch metrics

### Evening
- [ ] Write follow-up thread: "first day numbers"
- [ ] Reach out to anyone who starred the repo with a thanks note
- [ ] Send "thanks for trying it" email to anyone in waitlist

## T+1 to T+7

### Week 1 cadence
- [ ] Daily Twitter update with one specific feature highlight
- [ ] One blog post: "What I learned shipping pulse to HN"
- [ ] One YouTube short / demo video (60-90s)
- [ ] DM 10 more influencers (those who didn't reply pre-launch)

### Maintenance
- [ ] Triage every GitHub issue within 24 hours
- [ ] Daily check of waitlist email count
- [ ] Daily check of HN comment ranking (decay analysis)

### Conversion measurement
- [ ] HN clicks → GitHub stars → repo clones → installs → waitlist
- [ ] Target after week 1: 500 stars · 200 waitlist · 50 repo forks

## T+14: Day 14 review

- [ ] Total install estimate from `account.py` `client_id` uniques (if telemetry on)
- [ ] Waitlist total
- [ ] Press mentions
- [ ] Decide: Build Phase B (cloud) immediately, OR ship more v1.x polish?
  - 200+ waitlist signups → Phase B
  - <100 waitlist → iterate on v1.x first

## T+45: Day 45 master decision

Per Maa-launch methodology:

| Metric | "Hot" threshold | Decision |
|--------|-----------------|----------|
| Stars | 1000+ | Hot — ship Cloud |
| Stars | 200-1000 | Warm — focus on growth |
| Stars | <200 | Cool — iterate or pivot |

Hot → start outreach to Microsoft, Anthropic, Intuit for partnership/M&A conversations.

## T+90: Phase B+C activation

If still on track, execute the following from `docs/MICROSOFT.md`:

- [ ] Schedule first Microsoft demo call
- [ ] Apply for Vercel for Startups (free Pro plan)
- [ ] Apply for Stripe Atlas if not already incorporated
- [ ] Begin SOC2 Type I audit (Drata or Vanta)
- [ ] First paying Team-tier customer

## Risks + mitigations

| Risk | Mitigation |
|------|-----------|
| HN post tanks | Have 2 backup angles ready; iterate on subreddits |
| Anthropic ships native consumer dashboard | Pivot to multi-provider faster |
| ClaudeMetrics raises and out-spends us | Lean on local-first + privacy + UX |
| Privacy concern from press | Have audit-log + open-source + MIT license front and center |
| macOS users frustrated by Windows-only | Push macOS port to top priority post-launch |

## Success criteria

**Minimum**: 100 GitHub stars, 50 waitlist signups, 1 press mention
**Target**: 1000 stars, 500 waitlist, 3 press mentions
**Stretch**: 5000 stars, 2000 waitlist, M&A inbound
