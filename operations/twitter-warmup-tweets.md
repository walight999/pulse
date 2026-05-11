# Twitter / X warm-up — 10 ready-to-post tweets

Post order: top to bottom, 1-3 per day starting **May 12**.
Final tweet (the Show HN announcement) reserved for launch day Tue May 26 or Thu May 28.

All tweets ≤ 280 chars. Threading not used for warm-up — single tweets get better
distribution. Save threads for launch day only.

---

## Day 1 — May 12 (Mon)

### Tweet 1.1 — Build-in-public intro
```
Building pulse — the personal finance dashboard for the AI era.

ChatGPT Plus. Claude Max. Cursor. Copilot. Gemini.
You pay for 4-6 of them. You have no idea which are worth it.

I'm building the tool I wished existed.

Local-first, MIT, Windows-tray.
github.com/walight999/pulse
```

Attach: `static/brand/lockup-horizontal-dark.png`

### Tweet 1.2 — Problem statement
```
The average AI prosumer spent $327/mo on subscriptions in 2025.

That's ~$4,000/year of subscriptions that auto-renew silently.

Most people have no idea what their ROI is.
Bank app doesn't categorize "AI."
Anthropic Console only shows Claude.

Pulse fixes this.
```

---

## Day 2 — May 13 (Tue)

### Tweet 2.1 — Feature highlight: ROI hero
```
The killer feature in pulse:

It tells you "your $200/mo Claude Max plan returned $4,127 in API equivalent value — Legendary tier ★★★★★"

Real number. Real savings.

Then you go to bed feeling great instead of anxious.
```

Attach: ROI hero card screenshot (dark mode)

### Tweet 2.2 — Privacy positioning
```
Pulse is 100% local-first.

No account. No cloud. No telemetry by default.
Your data lives in ~/.local/share/pulse/.

When Cloud launches (Q3), sync will be opt-in + E2E encrypted.
We literally cannot see your data.

This is non-negotiable.
```

---

## Day 3 — May 14 (Wed)

### Tweet 3.1 — Comparison
```
Tools that exist but don't solve this:

• Anthropic Console — org-level, Claude only
• ClaudeMetrics — team proxy, Claude only
• Bank app — sees subs but no AI category
• Spreadsheet — what I had before

Pulse is the only tool that links subs + tokens + activity in one local view.
```

### Tweet 3.2 — Behind the scenes
```
The thing I'm most proud of building:

Accurate cache TTL pricing for Claude.

Most tools use one flat cache rate. But Anthropic charges differently for 5-min vs 1-hour cache.

Pulse splits these correctly.
We're off by 10%+ less than every other tool.
```

---

## Day 4 — May 15 (Thu)

### Tweet 4.1 — Cancellation savings
```
The hardest part of personal finance:

Cancelling subscriptions you don't use.

Pulse tracks cancellations as wins. "You've saved $4,300 by cancelling 7 subs since starting Pulse."

Visible proof that the hard habit was worth it.
```

Attach: lifetime savings card

### Tweet 4.2 — Browser extension
```
Building a browser extension to capture chat.openai.com, claude.ai, gemini, perplexity sessions.

Metadata only — model + timestamp + length. Never message text.

Combined with desktop logs you get a full cross-provider AI usage view.

MV3, Chrome + Edge. Open source.
```

Attach: browser extension popup screenshot

---

## Day 5 — May 16 (Fri)

### Tweet 5.1 — Streak gamification
```
Streak chips light up at 30+ days.

The "47-day streak" glow on your overview page is the kind of small habit-feedback that personal-finance apps used to do well (Mint, RIP).

We need this for AI too.
```

Attach: streak chip animated GIF if possible

### Tweet 5.2 — Mint nostalgia
```
Mint shut down in 2024.

The category it pioneered (automatic personal-finance dashboards) has been vacant since.

Meanwhile we all started paying for AI tools. ChatGPT, Claude, Cursor.

Pulse = Mint for the AI era.

That's the brief.
```

---

## Day 6 — May 17 (Sat)

### Tweet 6.1 — Tease
```
Show HN coming next week.

Looking for 10 early users to install + use for 1 week before launch.
DM me if you pay for ≥3 AI tools and want unified visibility.

Will personally onboard each one.

Beta = free pulse Pro for 1 year.
```

---

## Day 7 — May 19 (Mon)

### Tweet 7.1 — Demo / screenshot
```
A quick walkthrough of pulse:

1. Install (zero setup)
2. Auto-detect AI subs from Gmail
3. Parse Claude logs from ~/.claude
4. Show you ROI: "$200 Claude → $4,127 API value"

That's it. Beautiful, local, fast.
```

Attach: 30-sec demo GIF

---

## Day 8 — May 21 (Wed)

### Tweet 8.1 — Open source / GitHub
```
Pulse repo passed 100 stars overnight 🌱

The MIT license + local-first design clearly resonates.

Building in public means I get feedback before launch.
Show HN goes live Thursday.

github.com/walight999/pulse
```

(Adjust this tweet's metric to whatever's actually true on May 21)

---

## Day 9 — May 23 (Fri)

### Tweet 9.1 — Last-mile
```
Show HN launches next Thursday.

If you've been following along — would love a star on the repo before then.
Helps with HN ranking the first hour.

github.com/walight999/pulse

Pulse is for anyone who pays for ≥3 AI tools and wants to know if any of them are worth it.
```

---

## Day 10 (LAUNCH DAY) — Tue May 26 or Thu May 28

### Tweet 10.1 — Pinned launch tweet
**FULL 10-TWEET THREAD** per `twitter-launch-thread.md`. Post immediately
after Show HN goes live (~3-5 minutes after submission). Pin this thread.

---

## Engagement rules

- Reply to every reply within 4 hours
- Quote-RT every shoutout with a thank-you
- DO NOT use #AI, #ChatGPT, #buildinpublic hashtag (kills reach)
- DO use plain text — Twitter's algorithm hates hashtags & links combined
- For tweets with images, the image should add information (screenshot of feature, not just brand asset)

## Image asset checklist (need before Day 1)

- [x] Lockup horizontal dark — `static/brand/lockup-horizontal-dark.png`
- [x] App icon — `static/brand/app-icon.png`
- [x] OG card — `static/brand/og-social-card.png`
- [ ] Dashboard hero screenshot (Overview page, dark mode, 2x retina) — **needs capture**
- [ ] ROI hero card close-up — **needs capture**
- [ ] Lifetime savings card close-up — **needs capture**
- [ ] Browser extension popup — **needs capture**
- [ ] Streak chip glow GIF — **needs capture** (use OBS or LICEcap)
- [ ] 30-second walkthrough demo GIF — **needs capture**

To capture screenshots: Streamlit on localhost:8501, F11 for fullscreen,
Win + Shift + S for region capture. Save 2x resolution PNG.
