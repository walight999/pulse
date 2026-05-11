# pulse — Chrome Web Store & Edge Add-ons listing

Copy-paste ready for submission. Target listing date: ~7 days after Show HN launch
(when waitlist + initial users are warm).

## Store category

- **Chrome Web Store**: Productivity
- **Edge Add-ons**: Productivity
- **Firefox Add-ons**: (skip — MV3 fork required)

## Short description (132 char max)

> Track your ChatGPT, Claude, Gemini & Perplexity usage privately. Captures metadata only — no message text ever leaves your machine.

## Detailed description

```
Pulse — Mint for the AI era.

The browser companion to the pulse desktop dashboard (https://mintforai.com).
Captures your AI tool web sessions and feeds them into your local pulse
dashboard for unified analytics across ChatGPT, Claude.ai, Gemini, and
Perplexity.

WHAT IT DOES
• Watches your AI tool tabs for completed conversations
• Sends model name + timestamp + approximate length to your local pulse app
• Buffers events when pulse is offline; syncs every 5 minutes
• Zero account, zero cloud calls (until you opt into pulse Pro)

WHAT IT CAPTURES
✓ Provider name (openai, anthropic-web, google-gemini, perplexity)
✓ Model name (when exposed by the response)
✓ Timestamp
✓ Approximate character count of response

WHAT IT NEVER CAPTURES
✗ Your messages
✗ Conversation content
✗ Personal information
✗ Anything not strictly necessary for usage analytics

WHY YOU MIGHT WANT THIS
• See your real cross-provider AI spend in one dashboard
• Discover that your $200/mo Claude Max plan returns $4,000 in API value
• Cancel subscriptions you no longer use
• Track your AI usage streak (gamified)

REQUIRES
• pulse desktop app running locally (free, MIT-licensed)
• Download: https://github.com/walight999/pulse

OPEN SOURCE
Pulse is MIT-licensed. The extension is reviewable on GitHub:
https://github.com/walight999/pulse/tree/main/browser-ext

PRIVACY
We capture only what's needed for cost tracking and never read message text.
See https://github.com/walight999/pulse/blob/main/PRIVACY.md for full details.
```

## Promotional images (required)

Submit:

- **Small tile**: 440x280 px — `static/brand/og-social-card.png` (crop to 440x280)
- **Large tile**: 920x680 px — TBD (use Figma export of dashboard preview)
- **Marquee**: 1400x560 px — TBD

## Screenshots (1-5 required, 1280x800 or 640x400)

Capture these in order:

1. **Hero shot** — extension popup over chatgpt.com tab, showing "12 buffered events" + "Sync now"
2. **Setup flow** — chrome://extensions Load Unpacked, with pulse loaded
3. **Privacy** — DevTools showing the actual capture payload (model + timestamp only, no message text)
4. **Dashboard tie-in** — desktop pulse showing the combined provider breakdown
5. **Roadmap teaser** — "Coming soon: native integration with pulse Cloud"

## Tagline

> Your AI usage. Everywhere you use it. Privately.

## Listing keywords

`AI usage tracker, ChatGPT analytics, Claude analytics, Gemini analytics,
Perplexity tracker, AI cost dashboard, AI subscription tracker, token counter,
LLM observability, AI productivity, AI spend monitor, Claude Code cost,
GPT cost tracking`

## Single-purpose disclosure (required for Chrome)

> This extension has one purpose: to capture metadata from AI tool tabs
> (provider, model, timestamp, response length) and forward it to the user's
> local pulse desktop app for cost analytics. It does not modify any web
> content, inject ads, or read message text.

## Host permissions justification

For each `https://...` permission in manifest.json, explain why:

- `chat.openai.com / chatgpt.com` — capture model name + response metadata
- `claude.ai` — capture model name + response metadata
- `gemini.google.com / aistudio.google.com` — capture generation events
- `www.perplexity.ai` — capture query / answer events
- `cursor.com` — future use for Cursor browser-based features
- `http://localhost:8000/*` — send captured events to the local pulse desktop app

## Submission checklist

- [ ] $5 Chrome Web Store one-time developer fee
- [ ] Verified developer identity
- [ ] Privacy policy URL (https://github.com/walight999/pulse/blob/main/PRIVACY.md)
- [ ] Support URL (https://github.com/walight999/pulse/issues)
- [ ] Icons in `browser-ext/icons/` (16x16, 48x48, 128x128) — generate from app-icon.png
- [ ] Manifest validated (Chrome's extensions:// page accepts Load Unpacked without errors)
- [ ] Tested in Chrome stable + Edge stable
- [ ] Demo video (60-90 seconds, optional but recommended)

## Edge-specific notes

Edge Add-ons accepts the same MV3 zip as Chrome. Submit second; review usually
faster (3-5 days vs Chrome 7-14 days). Edge has a "Made for Surface" badge
program — apply once we have macOS port.

## Post-listing growth

- Add "Available on Chrome Web Store" badge to mintforai.com
- Add to product hunt launch
- Cross-link with desktop GitHub README
- Discord announcement: "pulse browser extension is live"
