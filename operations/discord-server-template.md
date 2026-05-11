# Pulse Discord server — setup template

Goal: lightweight community for beta testers + early adopters. Not a support
forum (use GitHub Issues for that). Discord is for vibes + casual feedback.

---

## Server identity

- **Server name**: pulse
- **Icon**: `static/brand/icon-512.png` (Discord auto-rounds it)
- **Banner**: `static/brand/lockup-horizontal-dark.png` (Discord crops to 16:9)
- **Server tagline**: Mint for the AI era
- **Description**: "Local-first personal finance dashboard for AI subscriptions, Claude tokens, and focused work. github.com/walight999/pulse"

---

## Channels (8 minimum, no more)

### Category: WELCOME

**#welcome** (everyone-readable, no posting)

```
Welcome to pulse 💚

We're building the personal finance dashboard for the AI era.
Mint for ChatGPT + Claude + Cursor + everything-else-you-pay-for.

Local-first by default. Cloud sync (opt-in, E2E encrypted) launches Q3.
Free forever for local use. Pro is $9/mo for cross-device.

🔗 Get started: github.com/walight999/pulse
🔗 Landing: pulse.app
🔗 Roadmap: github.com/walight999/pulse/blob/main/ROADMAP.md

To get started:
1. Read this channel + #rules
2. Self-introduce in #introductions
3. Pick a role in #role-select (Beta tester / Pro waitlist / Curious)
4. Hang out in #general

If you find a bug, file it on GitHub: github.com/walight999/pulse/issues
Discord is for vibes — not support tickets.
```

**#rules** (everyone-readable, no posting)

```
1. Be kind. Critique ideas, not people.
2. No spam, no AI-generated content without disclosure.
3. No promotion of competing tools unless directly relevant.
4. English + Thai both welcome.
5. Bugs → GitHub Issues. Vibes → here.
6. Be patient with the team (it's just one of us right now).

Founders are gone for 6 hours when ICT timezone is sleeping.
Bot will respond to common questions in the meantime.
```

**#announcements** (founder-only post, everyone read)

Pin: "v1.0 launched — read everything in #release-notes"

### Category: TALK

**#general** — open chat, all topics related to AI cost / personal finance / pulse
**#introductions** — single-message self-intros
**#feedback** — open-ended feedback, not bug reports
**#showcase** — share your dashboard screenshots, ROI numbers, etc.

### Category: PRODUCT

**#release-notes** (founder-only post)

For every version release, post:
```
🟢 pulse v1.0 — initial public release (May 26, 2026)

What's new:
- AI subscription tracker
- Claude usage analytics
- Activity tracking (Windows-only for now)
- Plan ROI hero with 5-tier rating
- Multi-currency (30+ via ECB)

What's coming:
- v1.1: OpenAI / Cursor / Gemini / Copilot parsers (30 days)
- v1.2: macOS + Linux ports (60 days)
- v2.0: Pulse Cloud + mobile PWA (Q3 2026)

Install: github.com/walight999/pulse
Bug reports: github.com/walight999/pulse/issues
```

**#feature-requests** — community-driven roadmap voting

Format:
```
**[FEATURE] Cancel button for renewals from dashboard**

I want to be able to right-click a subscription in pulse and have it open
the cancel URL in my browser. Even better: notify me 7 days before with a
1-click cancel link.

👍 if you want this
```

### Category: BETA

**#beta-testers** (role-restricted, beta-tester role only)

Private channel for the 10-15 beta testers. Direct line to founder.

---

## Roles (4 minimum)

| Role | Color | Use |
|------|-------|-----|
| **Founder** | #00E5A0 (pulse green) | the one person managing it |
| **Beta Tester** | #00C58A (pulse dim) | first 15 early users, year of Pro |
| **Pro Waitlist** | #FAFAF7 (paper) | signed up for Pulse Pro waitlist |
| **Curious** | default gray | everyone else |

Self-select Beta Tester / Pro Waitlist / Curious in **#role-select** via
reaction (use the Carl-bot or similar reaction-role bot).

---

## Bots

Minimum bot setup (all free tier):

1. **Carl-bot** — reaction roles, anti-spam, basic moderation
2. **MEE6** or **Dyno** — welcome message + auto-roles
3. **Custom Pulse Bot** (future) — pulls live waitlist count, Pulse Pro
   conversion rate, etc. into #general

Pin the founder's GitHub Issues feed as a webhook in #release-notes.

---

## Onboarding flow

When a new member joins:

1. Bot DM: welcome + link to #welcome + ask them to introduce
2. After they introduce: auto-grant "Curious" role
3. After 7 days active: invite to self-select Beta Tester (if they used pulse)
4. After 30 days active: invite to become Discord Moderator (if engaged)

---

## Founder presence

- Post in #general at least once / day
- Reply to every DM within 24 hours
- Run a weekly "office hours" voice call (Saturday 10am ICT)
- Tag people in #release-notes when their feedback shipped

Burnout protection:
- No notifications between 22:00 and 09:00 ICT
- One full day off per week (Sunday)
- Set status to "Sleeping" when off

---

## Growth strategy

- Don't promote outside (Discord is a magnet, not a beacon)
- Cross-link from GitHub README ("Join the community →")
- Cross-link from pulse.app footer
- After Show HN: invite top commenters who installed
- After v1.1 release: invite providers parser PR contributors

Target: 50 active members at 30-day mark, 200 at 90-day mark.

If we hit 500 active by 90-day mark, consider:
- Hiring community manager part-time
- Weekly newsletter from Discord activity
- Dedicated #api-help and #integrations channels

---

## Anti-patterns to avoid

- ❌ Don't create more than 10 channels at launch (overwhelming)
- ❌ Don't gate everything behind roles (kills new-member engagement)
- ❌ Don't make Discord the only support channel (GitHub Issues is canonical)
- ❌ Don't post Twitter / Notion / Slack links in #welcome (one source of truth)
- ❌ Don't run polls every day (kills attention)

---

## Discord launch checklist

- [ ] Server created with brand assets (icon, banner, color)
- [ ] All 8 channels created with welcome / rules / pin messages
- [ ] 4 roles defined with colors
- [ ] Carl-bot / Dyno added + welcome flow configured
- [ ] GitHub Issues webhook posting to #release-notes
- [ ] Founder profile set up with pulse logo + bio
- [ ] Invite link generated with infinite use + no expiry
- [ ] Link added to GitHub README + pulse.app footer
- [ ] First 5 messages in #general (founder posts to seed activity)

After launch:
- [ ] Reply to every join in 2 hours
- [ ] Pin the most useful community post weekly
- [ ] Voice "office hours" Saturdays 10am ICT
