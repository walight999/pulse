# Pulse — Privacy

*Last updated: 2026-05-10*

Pulse is local-first by design. **Your data never leaves your computer**
unless you explicitly opt in to a cloud feature (none ship today).

## What Pulse stores locally

All data lives in:
- `data/tracker.db` — SQLite database
- `data/fx_cache.json` — exchange rate snapshot
- `data/waitlist.json` — your local waitlist signup (if any)
- `data/referrals.json` — your referral code
- `data/telemetry.jsonl` — usage events (only if opted in)
- `logs/*.log` — diagnostic logs
- `backups/*.db.gz` — last 7 daily snapshots

The database contains:

| Data | What |
|------|------|
| Subscriptions | Names, costs, billing cycle, renewal dates, your notes |
| App activity | Process names + foreground time + window titles |
| Token usage | Per-API-call counts (input/output tokens), model name, project tag |
| Settings | Currency, budgets, alert toggles, idle threshold |

**Window titles can be sensitive** (e.g., document names, browser tab titles).
If you don't want them tracked, delete `data/tracker.db` and disable the tracker.

## What Pulse does NOT store

- No passwords, payment cards, or bank details
- No prompt content or AI conversation text (only token counts)
- No browser history or website URLs
- No screenshots or webcam captures
- No keystrokes or clipboard content

## What Pulse sends over the network

By default, **two** outbound calls happen:

1. **Exchange rates** — once per 24h, GET to `https://api.frankfurter.dev/v1/latest`. No personal data sent. Used for currency conversion.
2. **(Optional) Anthropic Admin API** — only if you set the `ANTHROPIC_ADMIN_KEY` env var. Pulls org-level token usage from your Anthropic account.

That's it. No analytics, no telemetry, no error reporting unless you opt in.

## Telemetry (opt-in)

If you check "Help improve Pulse with anonymous usage data" in Settings,
Pulse logs feature usage events to `data/telemetry.jsonl`. **These events
stay on your computer until cloud sync ships (Phase 1)**. When that ships,
opted-in events will be batched and sent over HTTPS to the analytics endpoint.

What's in an event:
- Event name (e.g., `subscription_added`, `token_sync_clicked`)
- Anonymous account UUID
- Timestamp
- Numeric counts (e.g., `subs_count: 5`)

What's NOT:
- No subscription names
- No email addresses
- No token usage cost / amounts
- No app or window titles

You can opt out at any time and delete `data/telemetry.jsonl`.

## Cloud features (Pro tier — not yet shipped)

Pro will add cloud sync. When it ships:
- Data will be **end-to-end encrypted** with a key only you hold
- We will not be able to read your subscriptions, AI cost, or activity
- You can disable sync per device
- Local data remains usable if you cancel Pro

A separate, version-stamped privacy policy will accompany the Pro release.

## Data deletion

Local: delete the `data/` folder. That removes everything.

To reinstall fresh: re-run `init_db()` or just start the app again — a new
empty database will be created.

## Contact

Questions about privacy: open an issue on the repository, or email
(coming with the Pro launch).
