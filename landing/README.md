# pulse landing — Next.js 14 (App Router)

Marketing site at `mintforai.com` (when deployed).

## Quickstart

```bash
cd landing
cp ../static/brand/*.png public/brand/    # copy logo + hero + OG card
npm install
npm run dev
# open http://localhost:3000
```

## Deploy to Vercel

```bash
npm i -g vercel
vercel               # first-time setup
vercel --prod        # production deploy
```

Once domain `mintforai.com` is registered:

1. In Vercel → Settings → Domains → Add `mintforai.com`
2. In your registrar → DNS → Add Vercel A/CNAME records
3. SSL auto-provisions via Let's Encrypt

## Stack

- Next.js 14 App Router
- React 18
- Tailwind CSS 3.4 (Pulse mint palette in `tailwind.config.ts`)
- TypeScript
- One API route (`/api/waitlist`) — replace `console.log` with Supabase insert when ready

## Pages

- `/` — hero + features + pricing + waitlist (single-page marketing)
- `/api/waitlist` — POST handler for email signups

## Brand assets

Place the 5 PNGs from `static/brand/` into `landing/public/brand/`:

- `app-icon.png`
- `logomark.png`
- `hero-illustration.png`
- `og-social-card.png`
- `browser-extension-mockup.png`

## Roadmap

- [ ] Real waitlist backend (Supabase row insert or ConvertKit API)
- [ ] Blog at `/blog` (MDX-based)
- [ ] Docs at `/docs` (MDX or Mintlify)
- [ ] Pricing page detail (`/pricing` — currently in-page anchor)
- [ ] Compare page (`/vs/claudemetrics`, `/vs/anthropic-console`)
- [ ] Status page (`status.mintforai.com`)
- [ ] Sign-in flow (when Cloud launches)
