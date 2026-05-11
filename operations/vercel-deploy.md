# Vercel deploy + Cloudflare DNS — hand-off

**Domain registered:** `mintforai.com` (Cloudflare, 2026-05-11)
**Goal:** `https://mintforai.com` resolves to the Next.js landing in `landing/`.
**Time:** ~20 minutes total.
**Cost:** $0 (Vercel Hobby tier).

---

## Step 1 — Vercel deploy (10 min)

1. Open https://vercel.com/new
2. **Continue with GitHub** (use the `walight999` account)
3. **Import** repo `walight999/pulse`
4. Configure project:
   - **Project Name**: `pulse` (or `mintforai`)
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: click "Edit" → set to `landing`
   - **Build Command**: leave default (`next build`)
   - **Output Directory**: leave default (`.next`)
   - **Install Command**: leave default (`npm install`)
   - **Environment Variables**: none needed for v1
5. Click **Deploy**
6. Wait ~60-90 seconds → green checkmark + preview URL like `pulse-xxxxxxxx.vercel.app`
7. Click the preview URL → confirm landing page renders correctly

> If the build fails: the build was already verified locally on 2026-05-11 (`npm run build` produced 91kB First Load JS, no errors, no warnings). Most likely cause of failure is missing the "Root Directory: landing" step above.

---

## Step 2 — Add custom domain in Vercel (5 min)

1. In the Vercel project → **Settings** → **Domains**
2. Type `mintforai.com` → **Add**
3. Vercel will show 2 records you need to add at Cloudflare:
   - **A record** for apex (`@`) → `76.76.21.21`
   - **CNAME record** for `www` → `cname.vercel-dns.com`
   *(Vercel may show slightly different IPs — use whatever Vercel shows, not the values above.)*
4. Don't close this Vercel tab yet — leave it open for the verify step.

---

## Step 3 — Cloudflare DNS records (5 min)

1. Open https://dash.cloudflare.com → select `mintforai.com`
2. Left sidebar → **DNS** → **Records**
3. Click **Add record**:
   - Type: `A`
   - Name: `@` (or `mintforai.com`)
   - IPv4 address: `76.76.21.21` (or whatever Vercel showed in Step 2)
   - Proxy status: **DNS only** (gray cloud, NOT orange — Vercel handles SSL)
   - TTL: Auto
   - Save
4. Click **Add record** again:
   - Type: `CNAME`
   - Name: `www`
   - Target: `cname.vercel-dns.com`
   - Proxy status: **DNS only** (gray cloud)
   - TTL: Auto
   - Save
5. Go back to the Vercel tab → click **Refresh** next to the domain → should turn green within 1-5 min

---

## Step 4 — Verify (1 min)

Run from terminal:

```bash
# DNS resolves
nslookup mintforai.com 1.1.1.1

# HTTPS works
curl -sS -o /dev/null -w "HTTP %{http_code}\n" https://mintforai.com
```

Expected: A record returns Vercel IP + HTTP 200.

Open https://mintforai.com in browser → landing page should render with the open graph card.

---

## Step 5 — www redirect (optional, 2 min)

By default Vercel will also serve the site at `www.mintforai.com`. Most prefer one canonical host.

In Vercel → Domains → `www.mintforai.com` → click the **three dots** → **Set as Redirect** → target `mintforai.com`.

This makes `www` 308-redirect to apex.

---

## Step 6 — Confirm OG card (3 min)

Drop these into the social card debuggers to confirm OG image + metadata:

- **Twitter Card Validator**: https://cards-dev.twitter.com/validator
- **Facebook OG Debugger**: https://developers.facebook.com/tools/debug/
- **LinkedIn Inspector**: https://www.linkedin.com/post-inspector/

Each should show:
- Title: "pulse — Mint for the AI era"
- Description: "Prove your $200 Claude plan returns $4,000 in API value."
- Image: 1200×630 mint-themed card

If image doesn't load, that's the `metadataBase` issue — already fixed locally in commit after this doc lands.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Vercel shows "Invalid Configuration" on domain | DNS not propagated yet | Wait 5-15 min, click Refresh |
| `nslookup` returns Cloudflare IPs (104.x.x.x) | Cloudflare proxy is ON (orange cloud) | Switch to DNS-only (gray cloud) |
| Browser shows "Vercel 404" | Wrong Root Directory in Vercel | Settings → General → Root Directory: `landing` → Redeploy |
| OG image fails on Twitter | Image path resolves to localhost | Already fixed via `metadataBase: new URL("https://mintforai.com")` |
| ERR_SSL_PROTOCOL_ERROR | Hit HTTPS before SSL certificate issued | Wait 2-3 min, Vercel auto-issues Let's Encrypt cert |

---

## After deploy is live

Update these once `mintforai.com` is confirmed live:

1. **GitHub repo description** → add "Landing: https://mintforai.com"
2. **GitHub topics** → ensure `personal-finance`, `ai`, `claude`, `local-first` are set
3. **Notion HQ** → mark Top 3 Move #2 as ✅
4. **STATE.md** → bump status from "deploy pending" to "live"
5. **Show HN prep** → landing URL ready for HN post body

---

## What's NOT in this deploy

- ❌ No backend API (`api/` is for v2)
- ❌ No database (waitlist signups go to `/api/waitlist` which only logs to console for now — wire to Supabase/Resend later)
- ❌ No analytics (intentional — no Plausible/Vercel Analytics until launch +14 days)
- ❌ No A/B testing (defer until 1K+ visitors/week)
