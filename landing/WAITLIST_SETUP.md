# Waitlist provider setup

`/api/waitlist` works out of the box (logs to Vercel console + returns a referral code), but you can plug in two optional providers via env vars in Vercel.

Both are **opt-in**. If the env vars aren't set, that provider is silently skipped — the endpoint still returns success and the entry still shows up in Vercel logs.

---

## Option A — Supabase (durable storage)

Create a free Supabase project at [supabase.com](https://supabase.com) and run this SQL in the SQL editor:

```sql
create table if not exists waitlist (
  email          text primary key,
  persona        text,
  os             text,
  tools          text[],
  monthly_spend  text,
  plan_interest  text,
  biggest_pain   text,
  referrer       text,
  utm_source     text,
  utm_medium     text,
  utm_campaign   text,
  utm_term       text,
  utm_content    text,
  referred_by    text,
  referral_code  text not null,
  ts             timestamptz not null default now()
);

-- Optional: a view of recent signups grouped by persona, for prioritization.
create or replace view waitlist_persona_breakdown as
select persona, count(*) as signups
from waitlist
group by persona
order by signups desc;
```

Then in Vercel → Project Settings → Environment Variables, add:

| Variable | Value | Notes |
|---|---|---|
| `SUPABASE_URL` | `https://xxxxx.supabase.co` | from Supabase project settings → API |
| `SUPABASE_SERVICE_ROLE_KEY` | `eyJhbGc…` | **service_role** key, not anon. Server-only. |
| `SUPABASE_WAITLIST_TABLE` | `waitlist` | optional, defaults to `waitlist` |

Duplicate emails are silently ignored (`Prefer: resolution=ignore-duplicates`).

> Why service role and not anon: the route runs on the server, never in the browser, and the table has no public read access. The service role bypasses RLS so inserts work without seeding a policy. If you want RLS-gated inserts instead, use the anon key + add a `for insert with check (true)` policy.

---

## Option B — Resend (confirmation email)

Create a Resend account at [resend.com](https://resend.com), verify a sending domain (e.g. `mintforai.com`), and create an API key.

In Vercel env vars:

| Variable | Value | Notes |
|---|---|---|
| `RESEND_API_KEY` | `re_…` | Resend API key |
| `WAITLIST_FROM_EMAIL` | `pulse <hi@mintforai.com>` | must be on a verified Resend domain |

The confirmation email is plain text (no tracking pixels, no HTML, no links to a tracking domain). Template lives in `app/api/waitlist/route.ts` under `sendConfirmationEmail()`.

> Why Resend over Postmark / SendGrid: smallest API surface, no SDK required, free tier covers 3k emails/mo which is well above any realistic waitlist volume pre-Pro launch. Swap providers by editing the URL + auth header in the same function.

---

## Verifying

After deploying with the env vars set:

1. Submit a test email via the waitlist form on production
2. Check Vercel → Deployments → Functions → `/api/waitlist` logs
3. Look for `[pulse waitlist] {...}` — `supabase` and `resend` fields should say `ok`. If they say an error string, that provider failed but the response still succeeded.
4. Verify the row exists in Supabase
5. Verify the confirmation email arrives (check spam if you just set up the sending domain)

---

## What this does NOT do

- No analytics on email opens / clicks (intentional — privacy-preserving)
- No marketing-list segmentation by tag (do that with SQL on the table)
- No drip campaign (one transactional confirmation, then silence until Pro launch)
- No double opt-in (single opt-in only — Thai PDPA + EU GDPR both permit single opt-in for product-launch notifications when the user explicitly typed their email; revisit if you start broader marketing)
- No referral-credit attribution (the `referral_code` is generated and stored, but no logic yet rewards the referrer when a friend signs up — wire that when Pro launches)
