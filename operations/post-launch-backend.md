# Post-launch backend wiring — triggers + runbooks

> The UX surface for Pro / Team / Enterprise is **complete** (pricing page, tier feature flags, Settings → Plans & billing, lock banners, Stripe portal placeholder). This doc lists the backend infrastructure that should be wired **only when a real trigger fires**, so we don't burn 40-60 hours on infrastructure that no one will use.

**Author:** White
**Last updated:** 2026-05-11
**Companion to:** `operations/launch-checklist.md`, `cloud/README.md`

---

## Why "deferred until trigger"

CLAUDE.md `Don't List` says: *"Pro tier marketing before v1.1 ships multi-provider"*. Building Stripe webhooks before a single paying user is the same anti-pattern. We have **0 paying customers today**. Every hour spent on SSO before the first Enterprise lead is an hour stolen from beta-tester recruitment.

The UX layer is enough to:
- ✅ Capture waitlist signups
- ✅ Display real pricing to HN traffic
- ✅ Show "Upgrade" CTAs in-app
- ✅ Send Team/Enterprise inquiries to sales@ / enterprise@ inboxes
- ✅ Display feature comparison matrix
- ✅ Set up the upgrade flow so v2.0 wiring is a small change

What we **don't** have yet:
- ❌ Live Stripe checkout (placeholder Payment Links work for now)
- ❌ Webhook → tier-sync (Supabase RPC ready, no Stripe webhooks)
- ❌ Real SSO (Enterprise card is mailto: only)
- ❌ Team invite flow (UI mockup only)

---

## Trigger → wiring map

### Trigger 1 — First Pro waitlist signup conversion intent

**Signal:** Someone on the waitlist replies "I'd pay today" OR we hit 20+ Pro waitlist signups.

**Wire (3-4 hours):**
1. Create Stripe products + prices: `pulse-pro-monthly` ($9), `pulse-pro-yearly` ($89)
2. Create [Stripe Payment Links](https://stripe.com/payment-links) — no code, copy URL into landing page Pro card `href`
3. Set Stripe Customer Portal preferences (cancel, update payment, download invoices)
4. Update `landing/app/page.tsx` Pro card `href` → Payment Link URL
5. Update `dashboard.py` Settings → Billing card `stripe_portal_url` setting

**Acceptance:** Tester clicks "Join waitlist" → "Subscribe now" → Stripe checkout → returns to landing with success param. Manual tier flip via `account.set_tier("pro")` until webhook is wired.

### Trigger 2 — First Pro subscriber wants cross-device

**Signal:** Pro subscriber asks "How do I get this on my laptop / phone?"

**Wire (6-8 hours):**
1. Spin up Supabase project (free tier OK initially)
2. Apply `cloud/supabase_schema.sql` (already exists — 8 tables, 6 RPC functions, RLS policies)
3. Set `SUPABASE_URL` + `SUPABASE_ANON_KEY` in dashboard env
4. Wire `cloud/sync.py:push_deltas()` to call `pulse_push_deltas` RPC
5. Set up Stripe webhook → Supabase edge function:
   - `customer.subscription.created` → `set_user_tier(user_id, 'pro')`
   - `customer.subscription.deleted` → `set_user_tier(user_id, 'free')`
6. Wire `cloud/auth.py:sign_in()` → Supabase magic link

**Acceptance:** Sign in on Win → install on Mac → first sync pulls 90 days history within 30 sec.

### Trigger 3 — First Team inquiry

**Signal:** First reply to `sales@mintforai.com` for Team plan.

**Wire (10-12 hours):**
1. Reply manually with Calendly + invoice
2. Create team via Supabase RPC `create_team(name, owner_id)` (already in schema)
3. Issue invite codes manually via SQL until UI is built
4. Build Team Settings UI in dashboard:
   - Team dashboard sub-page (`render_team_dashboard()`)
   - Invite member form
   - Member list with attribution metrics
5. Wire `integrations/slack.py:send_digest()` for the first paying team

**Acceptance:** 3-seat team paying = $57/mo confirmed in Stripe. Shared dashboard shows per-user attribution + Slack digest fires Mon 9am.

### Trigger 4 — First Enterprise lead

**Signal:** First reply to `enterprise@mintforai.com` with org domain (.gov, .edu, Fortune 500).

**Wire (16-24 hours over 2-4 weeks):**
1. Reply manually with intro deck (build deck on demand — don't pre-build)
2. NDA + procurement process (1-2 weeks)
3. SSO setup — Okta/Azure AD/Google Workspace via Supabase Pro + custom SAML adapter
4. SOC 2 audit prep (Drata + 60-day window)
5. Custom contract — annual term, data residency, SLA
6. Self-hosted Helm chart for on-prem (defer to second Enterprise customer)

**Acceptance:** First annual contract signed. Set `account.set_tier("enterprise")` for their domain via Supabase RPC.

---

## Cost projections (don't wire infra before this curve hits)

| Milestone | Monthly burn | When to wire |
|---|---|---|
| 0 paying customers | $0 (Vercel + Cloudflare free) | UX only — already done |
| 1-10 Pro ($9-90 MRR) | $25 (Supabase free + Stripe 2.9%) | Wire trigger 1+2 |
| 50 Pro ($450 MRR) | $50 (Supabase Pro + monitoring) | Already worth time |
| First Team ($57+ MRR) | +$0 marginal | Wire trigger 3 |
| First Enterprise ($1000+ MRR) | +$200 (SSO + audit infrastructure) | Wire trigger 4 |

---

## What's already built (don't re-do)

- `cloud/auth.py` — Supabase magic-link flow (needs `SUPABASE_URL` env)
- `cloud/crypto.py` — AES-256-GCM + Argon2id E2E encryption (works standalone)
- `cloud/sync.py` — Bidirectional sync protocol
- `cloud/leaderboard.py` — Friend leaderboard ranking
- `cloud/teams.py` — Team management
- `cloud/supabase_schema.sql` — Full schema with RPC functions + RLS
- `api/server.py` — REST API scaffold
- `api/ws_bridge.py` — WebSocket bridge for real-time browser-ext ingestion
- `sdk/python/pulse_client.py` — Programmatic access library
- `integrations/{slack,teams,discord}.py` — Webhook clients (stdlib only, no requests dep)
- `account.py:get_tier()` + `feature_enabled()` — Tier flag system with 4 tiers + 26 flags

The work to ship Pro/Team is mostly **wiring** the above, not **building** it.

---

## Anti-patterns to avoid

1. **Don't pre-build SSO** — every Enterprise has different IdP configs; build per-customer
2. **Don't pre-build self-serve Team signup** — first 5 Teams hand-onboard for learning
3. **Don't pre-build mobile native app** — PWA is enough for v2.0; native is v3.0
4. **Don't write Stripe webhook handler from scratch** — use Supabase Stripe extension
5. **Don't market Pro before v1.1 ships multi-provider parsers live** (CLAUDE.md rule)

---

## When this doc becomes obsolete

Delete this doc when:
- 10+ paying Pro customers
- 1+ paying Team customer
- 1+ Enterprise contract signed

At that point all triggers have fired and the wiring is done. The infrastructure becomes part of the codebase, not a deferred backlog.
