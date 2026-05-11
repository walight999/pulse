# Lean Launch Audit — pulse (life-tracker)

> Retroactive audit via `/lean-launch-stack` skill (pipeline v2 upgrade).
> Generated 2026-05-11 as part of bringing pulse up to current skill output spec.
> Wedge: **AI-Native** — local-first dashboard correlating AI subscription cost + AI token spend + actual usage time.

---

## Step 0 — Capacity Check

**Active projects:** 4 (LineZap, CHUM, Maa, pulse) — ceiling = 3 → ⚠️ **WARN**

**Decision:** pulse is the **least operationally heavy** of the 4 (local-first, no cloud infra, no daily content cadence). Continue passive maintenance: ship v1.0 → preview release on GitHub → community detection.

**Trade-off:** pulse runs without active sprint commitment. No marketing budget, no recurring infra cost, no daily checklist. Allow it to grow organically (HN / Show HN / GitHub-led).

---

## Step 1-2 — Classification

| Field | Value |
|---|---|
| **Product Type** | DESKTOP (Python/Streamlit + Windows system tray) + STATIC landing page (Next.js on Vercel/CF Pages) + EXT (browser-ext folder) |
| **Current Stage** | **S2 — Soft Launch** — v1.0 preview, README live, ROADMAP public, Show HN copy drafted |
| **Target Stage** | **S3 — Validated** after Show HN post → 100+ GitHub stars + 10+ active install reports |
| **Pattern Match** | Closest: Pattern 6 (Internal Tool) + DESKTOP from STACKS_BY_TYPE — applied below |

---

## Step 3 — Anti-Pattern Check

| Anti-pattern | Status | Notes |
|---|---|---|
| Hostinger / shared hosting | ✅ N/A — local-first app, no hosting needed |
| Dedicated domain pre-validation | ⚠️ Check — does `pulse.<tld>` exist? README references "github.com/walight999/pulse" not a domain |
| Apple Developer fee | ✅ Clear — Windows-only at v1.0, macOS deferred to v1.2 |
| Code signing pre-S3 | ✅ Acceptable to skip at S0-S2 (open source, GitHub-distributed) |
| Premium TLD pre-validation | ✅ No TLD owned (assumption) |
| VPS / dedicated server | ✅ N/A — local-first |
| AI API costs (Anthropic) on user's behalf | ✅ Pulse READS user's local JSONL logs — doesn't make API calls itself ✓ |
| Cloud-dependent features at S2 | ⚠️ Review: `integrations/` + `cloud/` folders exist — confirm cloud is optional |

**Special anti-patterns for local-first apps:**
- ❌ Forced cloud signup blocks "100% local" claim — Pulse correctly markets as zero-cloud
- ❌ Telemetry without opt-in — **TODO verify** no implicit telemetry in v1.0
- ❌ Auto-update without user consent — **TODO verify** update mechanism

---

## Step 4 — Domain Strategy

| Tier | Current | Recommendation |
|---|---|---|
| Tier 0 | GitHub Pages `walight999.github.io/pulse` (option) | Use for landing if Tier 1 unavailable |
| **Tier 1** | `pulse.<umbrella-brand>.<tld>` | **Recommended for v1.0 launch** — use existing brand |
| Tier 2 | `mintforai.com` ✅ registered (2026-05-11) | Live by v1.0 launch — wire to Vercel + Cloudflare DNS |

**For Show HN** — use **GitHub URL directly** (HN community prefers repo over marketing site). Landing page = secondary destination.

---

## Step 5 — Recommended Stack (audit of current)

| Component | Current | Lean assessment |
|---|---|---|
| Core app | Streamlit + SQLite + Python | ✅ Aligned — fast iteration, $0 infra |
| System tray | Windows native (pystray-like) | ✅ Aligned |
| Landing page | Next.js + Tailwind + Vercel (`/landing`) | ✅ Aligned |
| Background daemons | 4 daemons in-process | ✅ Aligned (no separate workers needed) |
| Backups | SQLite local rotation | ✅ Aligned (local-first promise) |
| FX rates | live ECB | ✅ Aligned (no paid API) |
| Browser extension | `browser-ext/` (Chrome/Firefox/Edge) | ✅ Aligned (Chrome $5 one-time, others free) |
| Cloud sync (`cloud/`) | Optional feature | ✅ Acceptable IF opt-in only |

**Stack changes recommended:**
- For landing page distribution: switch from Vercel → **Cloudflare Pages** (unlimited bandwidth + allows commercial use — Pulse roadmap mentions premium tier later)
- Browser extension distribution: list on Edge first (free) → Chrome ($5 one-time) → Firefox (free) at v1.0 launch

---

## Step 6 — Cost Breakdown

Pulse = **near-zero ongoing cost** thanks to local-first model.

| Component | Year 1 | At 1K users | At 10K users |
|---|---|---|---|
| GitHub Releases (binary distribution) | $0 | $0 | $0 (unlimited bandwidth) |
| Domain (if Tier 1 subdomain) | $0 | $0 | $0 |
| Landing page (Vercel Hobby → CF Pages) | $0 | $0 | $0 |
| Chrome Web Store one-time | $5 | — | — |
| Edge Add-ons | $0 | — | — |
| Firefox AMO | $0 | — | — |
| Apple Developer (v1.2 macOS) | $0 | $99 (one-time prep) | $99/yr |
| Code signing (v1.2 Windows EV cert) | $0 | $250-400/yr (optional, removes SmartScreen warning) | $250-400/yr |
| Cloud sync infra (if shipped opt-in) | $0 | $5-15/mo Supabase | $25-100/mo |
| **Total recurring** | **$5 (one-time)** | **$0-15/mo** | **$25-200/mo** |

Pulse can sustain ~10K users at **<$200/mo** because the app runs entirely on user machines.

**Revenue model (suggested for v1.2+):**
- Free tier: all local features (current v1.0 spec)
- Pro tier: cloud sync + multi-device + leaderboard (referenced in roadmap)
- Pricing target: $4-7/mo (lower than competitors since you have $0 marginal cost)

**Hard caps:** N/A in v1.0 (no cloud calls). For v1.2 cloud:
- [ ] Supabase usage alert
- [ ] Cloud function execution cap

---

## Step 7 — Promotion Gates

**S2 → S3** (Validated):
- [ ] Show HN post published
- [ ] >100 GitHub stars within 14 days
- [ ] >10 install reports from non-friends (Reddit, HN, Twitter)
- [ ] >1 inbound feature request from external user
- [ ] PRIVACY + TERMS + SECURITY published (✓ already present)

**S3 → S4** (Production-ready):
- [ ] v1.1 multi-provider (OpenAI, Cursor, Gemini etc.) shipped
- [ ] >1,000 users (estimated via download metrics)
- [ ] Decide on Pro tier pricing + launch
- [ ] Sustained <100 GitHub issues / month (manageable)

---

## Step 8 — Compliance & Trust Signal Check

### Privacy (local-first = strong baseline)
- [x] Privacy Policy — present (`PRIVACY.md`) ✓
- [x] Terms of Service — present (`TERMS.md`) ✓
- [x] Security policy — present (`SECURITY.md`) ✓
- [ ] Verify zero telemetry in code — **TODO audit** any `requests.post` / analytics calls
- [ ] Opt-in flag for cloud features clearly labeled (when v1.2 ships)

### Trust Signals
- [x] Founder identity (walight999 on GitHub) — visible
- [x] HTTPS / GitHub repo cloning — secure ✓
- [x] License (MIT) — present ✓
- [x] CHANGELOG.md — present ✓
- [x] CONTRIBUTING.md — present ✓
- [ ] About page / founder face on landing — TODO
- [ ] FAQ / support channel — TODO (mention in landing + README)

### Tax (if Pro tier launches at S3)
- [ ] Payment gateway (Stripe / Lemon Squeezy — LS handles VAT globally, simpler for solo dev)
- [ ] Invoice automation
- [ ] DBD พาณิชย์ submission

### Open-source specifics
- [x] LICENSE present ✓
- [ ] Code of Conduct — TODO (helps community growth)
- [ ] Issue templates — check `.github/` (typically auto-generated)
- [ ] PR template — same

### Trading/Finance disclaimer
Pulse tracks subscription costs — not investment advice. README is clear about this. ✓

---

## Next Actions (in order)

1. **Today** — Audit code for any unauthorized telemetry (`grep -r "requests.post\|httpx.post\|analytics" *.py`)
2. **Today** — Verify cloud features are opt-in only (run UI with cloud disabled, ensure full feature parity for local)
3. **This week** — Add Code of Conduct + issue templates → improves first-impression for HN traffic
4. **This week** — Publish Show HN post (already drafted in `docs/SHOW_HN.md`)
5. **Day +14** — Review GitHub star + install metrics → S3 promotion gate check
6. **v1.1 plan** — Add multi-provider per ROADMAP (no new infra cost)

---

## Pipeline v2 Cross-References

- DESKTOP pattern from `~/.claude/skills/lean-launch-stack/references/stacks-by-type.md`
- Local-first app = lowest cost profile in lean framework → leverage this in pricing
- **No `deploy-readiness.md` for pulse** — no `.claude/agents/` folder, no Notion HQ. Pulse is solo-builder mode, autonomous stack would over-engineer
- If pulse adds a Pro tier with paying users → consider running `/idea-to-mvp` retroactively to add Foundation files + agent team for marketing/support
