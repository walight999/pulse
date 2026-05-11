# 📅 Pulse — Operations + Roadmap

The operational runbook for launching + scaling Pulse. Everything in this folder is meant to be acted on.

---

## Quick navigation

| File | Purpose |
|------|---------|
| `launch-checklist.md` | T-7d → T+90 master runbook |
| `microsoft-outreach.md` | Acquisition one-pager (5 reasons to acquire) |
| `show-hn.md` | 3 launch angle drafts |
| `demo-script.md` | 30-sec GIF + 90-sec video storyboards |
| `twitter-warmup-tweets.md` | 10 ready-to-post tweets, day-by-day calendar |
| `twitter-launch-thread.md` | Launch-day 10-tweet thread |
| `beta-tester-outreach.md` | 4 DM templates + tracking |
| `hn-faq-bank.md` | 14 pre-written HN responses + tone guide |
| `reddit-crosspost-templates.md` | 5 subreddit-specific posts |
| `discord-server-template.md` | 8-channel setup + 4 roles |
| `browser-extension-store-listing.md` | Chrome/Edge store submission |
| `vercel-deploy.md` | **Click-by-click Vercel + Cloudflare DNS for `mintforai.com`** |
| `post-launch-backend.md` | Stripe/Supabase/SSO wiring runbook — triggered per first paying user / team / enterprise |
| `welcome-email.html` | Waitlist confirmation email |
| `email-signature.html` | Founder email signature |
| `invoice-template.html` | Stripe-renderable customer invoice |

---

## 14-day critical path to Show HN launch

### Phase 1 — Deploy brand (Days 1–2) ✅ DONE

- v1.5 Brand Core shipped
- 42 brand assets generated + deployed
- Touchpoints wired (Streamlit, landing, manifest)
- Repo pushed to GitHub

### Phase 2 — Landing page (Days 3–6)

**Critical bottleneck**. Cannot launch without `mintforai.com` live.

- [x] Register `mintforai.com` on Cloudflare — DONE 2026-05-11
- [x] `landing/` builds clean on Next 14.2.35 (verified 2026-05-11, 91kB First Load JS, zero warnings)
- [ ] Vercel deploy + custom domain — see `operations/vercel-deploy.md` for step-by-step
- [ ] Wire waitlist endpoint to Supabase (or Formspree initially) — 1 hr
- [ ] Lighthouse ≥ 95 audit — 30 min
- [ ] Mobile responsiveness check — 30 min

### Phase 3 — Distribution warmup (Days 7–10)

- [ ] Reserve `@pulse_app_ai` Twitter handle — 2 min
- [ ] Upload brand assets to Twitter profile — 10 min
- [ ] Start posting per `twitter-warmup-tweets.md` (1–3/day) — ongoing
- [ ] DM 30 beta tester targets per `beta-tester-outreach.md` — ongoing
- [ ] Hit 10 beta installs + 3 testimonials — by Day 10
- [ ] Capture 30-sec demo GIF + 90-sec video per `demo-script.md` — Day 7–8
- [ ] Setup Discord server per `discord-server-template.md` — Day 9
- [ ] Final cold-install test on fresh Windows VM — Day 10

### Phase 4 — Launch day (Day 11–14 = Tue May 26 or Thu May 28)

```
T-1h     Final dashboard + landing check
T-15m    Notify beta testers "going now"
T-0      08:00 EST = 19:00 ICT — submit Show HN
T+5m     Twitter thread (10 tweets) with HN link
T+10m    Discord announcement
T+15m    Reddit crossposts per `reddit-crosspost-templates.md`
T+30m    First HN comment responses (positive vibes signal)
T+1h-6h  Reply every 15 min
T+4h     First metrics review
T+24h    Day 1 metrics + thank-you DMs to commenters
```

---

## 30 / 60 / 90-day post-launch plan

### M1 (Day 0 → Day 30)

**Goal**: Stabilize + ship v1.1 multi-provider

- Daily Twitter highlight tweet
- Reply to every GitHub issue within 24 hours
- Weekly office-hours voice call (Discord)
- Ship OpenAI parser → Cursor → Gemini → Copilot
- Submit browser extension to Chrome Web Store + Edge Add-ons

**Success criteria**: 500 GitHub stars · 200 Pro waitlist · 1 press mention

### M2 (Day 30 → Day 60)

**Goal**: Validate Pro demand + start Cloud

- Activate Supabase project + run schema migrations
- Wire `cloud/auth.py` end-to-end with magic-link flow
- Test `cloud/sync.py` round-trip with 3 beta testers
- Add Settings → Cloud → Sign in UI to dashboard
- Begin macOS port testing on a real Mac

**Success criteria**: 1,000 stars · 500 waitlist · 10 paying Pro subscribers (early bird $5/mo)

### M3 (Day 60 → Day 90)

**Goal**: Ship Cloud + Mobile PWA

- Pulse Cloud Public Beta (Pro tier opens)
- Mobile PWA live with push notifications
- Friend leaderboard launch (5 categories, opt-in)
- First Team-tier customer onboarding (manual)
- Microsoft outreach — initial Principal PM contact

**Success criteria**: 2,500 stars · 1,000 waitlist · 50 paying Pro · 3 Team customers

### M4–M6 — Acquisition signals

Per `microsoft-outreach.md`:

- Apply for Vercel for Startups (free Pro)
- Begin SOC 2 Type I prep (Drata or Vanta)
- TechCrunch pitch
- 30+ enterprise design partners signed
- M&A inbound from Microsoft / Anthropic / Intuit

---

## Decision framework (T+14 + T+45 + T+90)

### Day 14 review

| Metric | Threshold | Decision |
|--------|-----------|----------|
| Pro waitlist signups | 200+ | Hot — start Phase B Cloud immediately |
| Pro waitlist signups | 50-200 | Warm — iterate on v1.x first |
| Pro waitlist signups | <50 | Cool — refine warmup strategy, delay Cloud |

### Day 45 master decision (per Maa-launch methodology)

| Stars | Status | Action |
|-------|--------|--------|
| 1,000+ | Hot | Ship Cloud + start Microsoft outreach |
| 200-1,000 | Warm | Focus on growth + v1.x polish |
| <200 | Cool | Iterate angle or pivot |

### Day 90 — Phase C activation

If Hot at Day 45:

- Schedule first Microsoft demo call
- Apply for Vercel for Startups
- Begin SOC 2 Type I audit
- Find first paying Team customer

---

## Risk register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| HN post tanks | Medium | High | Have 2 backup angles ready (`show-hn.md`) |
| Anthropic ships native consumer dashboard | Low | High | Pivot to multi-provider faster (v1.1) |
| ClaudeMetrics raises + out-spends | Medium | Medium | Lean on local-first + privacy + UX moat |
| macOS users frustrated by Win-only | High | Medium | Push macOS port to top priority post-launch |
| Streamlit performance issues at scale | Low | Medium | Have backup React port plan (`product/pulse/02-tech-spec.md`) |
| First Pro customers churn | Medium | Medium | 30-day free trial; weekly check-in DMs |

---

## Success criteria

**Minimum** (must-hit): 100 stars · 50 waitlist · 1 press mention
**Target** (likely): 1,000 stars · 500 waitlist · 3 press mentions
**Stretch** (aggressive): 5,000 stars · 2,000 waitlist · M&A inbound
