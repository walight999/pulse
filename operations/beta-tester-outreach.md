# Beta tester outreach

Target: 10-15 active testers before Show HN launch (Tue May 26 or Thu May 28).

Each beta tester gets:
- 1 free year of Pulse Pro when it launches
- Direct line to the founder for feedback
- Early access to leaderboard waitlist invite codes
- Listed (with permission) in launch thread as design partner

In return we ask for:
- Install + use for 1 week
- 1-2 sentences of honest feedback (good or bad)
- Optional: 1 screenshot + testimonial quote for launch materials

---

## Channel 1: Twitter cold DM (preferred)

Find people who tweet about Claude Code, AI subscription pricing, or AI tool stacks.
Search queries:

- `"claude max" OR "claude pro" cost`
- `cursor "$20/month" OR "cursor pro"`
- `"ai subscriptions" OR "ai tool stack"`
- `chatgpt plus claude both`

### DM template (warm)

```
Hey [first name] — saw your tweet about [specific thing they said about AI pricing/Claude/etc].

I've been building Pulse — a local-first personal-finance dashboard for AI subscriptions + Claude/GPT/Cursor usage. Auto-detects what you pay for, parses your local Claude logs, computes ROI vs API.

Looking for 10 early testers before Show HN next week. Would love your eyes on it.

In exchange: 1 free year of Pulse Pro when it launches, plus a shoutout (optional) as a design partner.

Interested? Install takes ~2 minutes, MIT licensed, all local. Repo: github.com/walight999/pulse
```

### DM template (cold)

```
Hey [first name] — I saw [thing they posted].

I'm building Pulse — Mint for the AI era. Local-first dashboard that auto-detects your AI subscriptions and parses your Claude usage logs to compute real ROI.

Looking for 10 beta testers. Free Pulse Pro for 1 year + design-partner credit if interested.

Repo: github.com/walight999/pulse — would love your take.
```

---

## Channel 2: Reddit DM / comment reply

In r/ClaudeCode, r/ChatGPT, r/LocalLLaMA — find people complaining about AI cost visibility.

**Comment reply** (preferred — don't spam DMs):

```
This is exactly the pain I'm building Pulse for — a local-first dashboard that auto-parses your Claude logs and shows ROI vs API. MIT licensed, runs as Windows tray. Looking for ~10 beta testers before Show HN next week. Free Pulse Pro for 1 year if you're in. Repo in bio.
```

(Bio link → github.com/walight999/pulse)

---

## Channel 3: Friend / network warm intro

For people you actually know in tech who fit the profile:

```
Hey — building something that'd save you money.

You're paying for [Claude / ChatGPT / Cursor / etc.] right? Pulse auto-detects what you pay across AI tools, parses your local Claude logs, and tells you "your $200/mo plan returns $X in API value."

It's the Mint for AI era. Local-first, MIT licensed.

Looking for 10 beta users this week. You'd be #2 on the list. Free Pulse Pro for 1 year for early users + I'll personally onboard you.

Want to try? It's a 2-minute install. https://github.com/walight999/pulse
```

---

## Tracking sheet (Notion or Airtable)

| Name | Channel | DM sent | Reply | Installed | Feedback | Testimonial OK |
|------|---------|---------|-------|-----------|----------|----------------|
| ... | DM/Reddit/Email | Date | Y/N | Date | text | Y/N |

Target conversion:
- Send 30 DMs → 12 replies → 8 installs → 5 feedback → 3 testimonials

If conversion is lower, increase DM volume. If higher, you're crushing it.

---

## Onboarding script for beta testers

When someone agrees:

1. Send the install link + 2-line quickstart:
   ```
   git clone https://github.com/walight999/pulse
   cd pulse && pip install -r requirements.txt && python app.py
   ```
2. Tell them to expect a 30-second onboarding wizard
3. Tell them what to look at first (Overview page, ROI hero card)
4. Send a follow-up DM 3 days later: "Tried it yet? What stood out?"
5. After feedback, ask: "Mind if I quote you for the launch thread?"

---

## Testimonial collection prompt

Once they've used it for a few days:

```
Hey [name] — would you mind sharing 1-2 sentences of honest feedback I can quote (with your name + Twitter handle) for the Show HN launch?

What surprised you about Pulse? Why would you (or wouldn't you) recommend it to someone paying for Claude / ChatGPT?

Even if it's critical that's fine — I'd rather have real than rave.
```

Target: 3 testimonials before launch, ideally one each from:
- Solo developer
- Designer / non-engineer prosumer
- Team lead at a small company

---

## Beta tester perks (clearly communicated upfront)

- ✅ 1 free year of Pulse Pro when it launches (Q3 2026, normally $9/mo = $108 saved)
- ✅ Listed as design partner in launch thread (opt-in)
- ✅ Direct DM line to founder for support
- ✅ First friend leaderboard invite codes (when leaderboard launches Phase 3)
- ✅ Vote on roadmap priority for v1.x

What we do NOT promise:
- ❌ Bug-free experience (it's pre-launch)
- ❌ macOS or Linux support today (Windows-only at launch)
- ❌ Cloud sync (Q3 2026)
- ❌ Equity or revenue share

---

## Critical-path risk

If we can't recruit 10 beta testers by **Friday May 23** (3 days before launch):

- Delay launch to **Tuesday June 2** to give another week of warm-up
- Or launch with less social proof (acceptable but suboptimal)

Decision criteria:
- 5+ installs + 2+ testimonials = LAUNCH
- 2-4 installs + 0-1 testimonials = DELAY 1 WEEK
- 0-1 installs = pivot warm-up strategy (Reddit-first, not Twitter)
