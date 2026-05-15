# STATE — pulse (life-tracker)

> Single-page project state. Standardized format across all v2-upgraded projects.
> **Last updated:** 2026-05-15
> **Pipeline version:** v2

---

## Project Identity

| Field | Value |
|---|---|
| **Slug** | pulse |
| **Tagline** | Mint for the AI era — local-first dashboard for AI spend + subscriptions + productivity |
| **Wedge** | AI-Native (only tool correlating subscription cost + AI token spend + actual usage time) |
| **Source** | Founder-built OSS (not from idea-to-mvp flow) |
| **Working dir** | `C:\Users\usEr\life-tracker\` (folder) / "pulse" (product name) |
| **Repo** | github.com/walight999/pulse (`.git` present locally) |

---

## Stage & Capacity

| Field | Value |
|---|---|
| **Current stage** | **S2 — Soft Launch** (v1.0 preview) |
| **Target stage** | S3 — Validated (>100 GitHub stars + >10 external installs + 1 inbound feature request) |
| **Capacity slot** | **PASSIVE** (4/4 active but pulse = local-first $0 marginal — no daily cadence) |
| **Founder involvement** | Loose (monitor + bug fix, GitHub-led) |

---

## Next Promotion Gate

**S2 → S3** (Validated):
- [ ] Show HN post published (draft exists in `docs/SHOW_HN.md`)
- [ ] >100 GitHub stars within 14 days
- [ ] >10 install reports from non-friends
- [ ] >1 inbound feature request from external user
- [x] PRIVACY + TERMS + SECURITY published ✓

---

## Top 3 TODOs (post-website-audit)

1. **Set Vercel env vars + deploy** — for the new pluggable `/api/waitlist`: `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` (create table per `landing/WAITLIST_SETUP.md` SQL), `RESEND_API_KEY` + `WAITLIST_FROM_EMAIL`. Endpoint works without these (logs to Vercel), so this is plug-when-ready.
2. **Reserve Twitter handle** (`@mintforai` / `@mintforai_ai` / `@pulse_dashboard`) + start `twitter-warmup-tweets.md` cadence
3. **Beta tester recruitment** — 5+ DMs/day for 6 days per `beta-tester-outreach.md`

**Done (older TODOs):** ✅ Telemetry audited (no unauthorized POST) · ✅ Cloud opt-in verified · ✅ CoC + 3 issue templates + PR template added · ✅ `mintforai.com` domain registered · ✅ Landing audit Phases 1-4 (honesty / activation / credibility / plumbing) — see commits d174044, a2fef41, 75ec298, 26774d7

---

## Pipeline v2 Files

| File | Status | Purpose |
|---|---|---|
| `CLAUDE.md` | ✓ (new) | Entry point + pipeline version |
| `STATE.md` | ✓ (this) | Single-page state |
| `lean-launch-audit.md` | ✓ | DESKTOP + STATIC + EXT audit |
| `deploy-readiness.md` | ✗ N/A | Solo OSS, no `.claude/agents/` — autonomous stack would over-engineer |
| `README.md` | ✓ | Product overview (substitutes for Foundation files) |
| `ROADMAP.md` | ✓ | v1.0 → v1.1 → v1.2 plan |
| `PRIVACY.md`, `TERMS.md`, `SECURITY.md` | ✓ | Compliance baseline ✓ |
| `docs/LAUNCH_CHECKLIST.md` | ✓ | Pre-Show-HN tasks |
| `docs/SHOW_HN.md` | ✓ (draft) | Show HN post draft |

---

## Notion Sync

| Item | Status | Notes |
|---|---|---|
| Company HQ | ✓ found | https://www.notion.so/35d9defb952981848312e64e6823571b |
| **Pipeline v2 sub-page** | ✓ pushed 2026-05-11 | https://www.notion.so/35d9defb952981b8aa92de940faca7c5 |

**Sync completed:**
- ✓ "🛡️ Pipeline v2 — Audit + Readiness" sub-page created under HQ (HQ tracks v1.0 → v1.5 build progress + Show HN target May 26/28)
- Contains: capacity status, DESKTOP/EXT/STATIC audit, telemetry/cloud-opt-in flags, S2→S3 gate criteria
- No deploy-readiness (no agent roster); pulse PASSIVE in capacity rules

---

## Recent Activity

| Date | Update |
|---|---|
| 2026-05-15 | Landing audit Phases 1-5 shipped (16 routes static, pytest 51/51). Phase 1 (d174044) honesty: status badges, lifetime defused, governing law. Phase 2 (a2fef41) activation: `/download`, `/methodology`, segmented waitlist. Phase 3 (75ec298) credibility: personas, integrations matrix, self-host comparison, `/roadmap`. Phase 4 (26774d7) plumbing: pluggable `/api/waitlist` (Supabase + Resend opt-in), onboarding consent, `tracker.py` honors privacy toggles. Phase 5 (6420bfc) polish: trust strip, `/docs` hub (9 sections × 4 cards), CSS overflow safety, a11y (skip-link / focus-visible / reduced-motion), Vercel Analytics, UTM capture in waitlist, Finance/Ops persona card, activity allowlist + danger-zone wipe, onboarding shows data location + demo-data seed. v1.6 changelog entry documents all 5 phases. |
| 2026-05-11 | `mintforai.com` registered on Cloudflare; all 38 repo refs swapped from `pulse.app`; landing build verified clean (Next 14.2.35, 91kB First Load JS, zero warnings); pytest 44/44; open-core model documented in README |
| 2026-05-11 | Pipeline v2 upgrade: added lean-launch-audit + CLAUDE.md + STATE.md |
| 2026-05-11 | No deploy-readiness (correctly skipped — no agent roster) |
| Earlier | Active codebase development (Streamlit + landing + browser-ext) |

---

## Don't List

- ❌ Forced cloud signup at any tier (breaks "100% local" claim)
- ❌ Implicit telemetry without opt-in
- ❌ Auto-update without user consent
- ❌ Pro tier marketing before v1.1 ships multi-provider
- ❌ Native iOS app (PWA / web preferred per pipeline)

---

## Sync to Notion Command

N/A — pulse does not sync to Notion. To check status:
```
cd "C:\Users\usEr\life-tracker"
type STATE.md
```
