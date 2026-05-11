# Security Policy

Pulse takes security seriously. This document covers our threat model, security
practices, and how to report vulnerabilities.

## Threat model

Pulse handles sensitive personal-finance data: subscription costs, AI API
spending, app activity. Our threat model assumes:

1. **The user's machine is trusted.** We are not a malware sandbox.
2. **The user's master password is the root of trust.** Lost password = lost
   cloud data (intentional — we cannot decrypt without it).
3. **The cloud service may be compromised.** All synced data is encrypted with
   user-derived keys before leaving the device.
4. **Network attackers are active.** All cloud traffic is TLS 1.3+.

## Encryption

- **At rest, local**: SQLite database is stored unencrypted in `data/tracker.db`.
  Users on shared machines should encrypt their disk (BitLocker, FileVault).
- **At rest, cloud**: Per-row AES-256-GCM with 12-byte random nonce per row.
  Server stores only ciphertext + HMAC-SHA256 searchable indexes.
- **Key derivation**: Argon2id(password, salt=account_id, m=64MB, t=3, p=1).
  The master key never leaves the device.
- **In transit**: TLS 1.3 to Supabase + Stripe + frankfurter.dev. Webhook
  endpoints (Slack/Teams/Discord) use TLS to vendor URLs.

See `cloud/crypto.py` for the implementation.

## Authentication

- **Cloud accounts**: Magic-link sign-in via Supabase Auth. No passwords stored.
- **JWT refresh**: tokens auto-rotate every 60 minutes; refresh tokens last 30 days.
- **API keys**: scoped to user's own data only. Generated in Settings → Developer.
  Revocable. Logged in audit table.
- **SSO (Enterprise)**: SAML 2.0 + OIDC via Supabase Pro / Auth0. Configurable
  per organization with domain allowlists.

## Privacy

- Local-only mode requires zero account, zero telemetry.
- Cloud mode: opt-in only. Each synced data category (subscriptions, AI usage,
  activity) toggleable separately.
- Leaderboard: opt-in only with three visibility levels (off / friends / public).
  Aggregate metrics only — raw token data never leaves the device.
- No analytics, no fingerprinting, no third-party trackers.

See `PRIVACY.md` for the full privacy policy.

## Audit logging

Pulse maintains a local audit log (`audit_log` table) of:

- Sign in / sign out events
- API key creation / revocation
- Team membership changes
- Settings changes (currency, plan, alerts)
- Export operations
- Sync events (counts only, never content)

Cloud accounts get a mirror in Supabase audit table, retained for 90 days
(Pro) / 1 year (Team) / 7 years (Enterprise).

## Reporting vulnerabilities

If you discover a security issue, **please do not file a public issue**.

Email: security@mintforai.com (when domain registered) or DM @walight999 on GitHub.

We aim to:

- Acknowledge within 24 hours
- Fix critical issues within 7 days
- Coordinate disclosure with the reporter
- Credit reporters publicly (if they wish)

## Bug bounty

Once Pulse Pro launches with paying customers, we will offer a bug bounty
program. Estimated tiers:

- Critical (RCE, auth bypass, mass data leak): $500–2000
- High (auth flaw, IDOR): $200–500
- Medium (XSS, CSRF, broken access): $50–200

## Compliance roadmap

- **v1.0** (current): MIT-licensed local app, no compliance certifications needed
- **v2.0** (Cloud): GDPR-compliant data handling, EU data residency option
- **v2.5** (Team): SOC 2 Type I audit (Drata + reputable auditor)
- **v3.0** (Enterprise): SOC 2 Type II, ISO 27001, HIPAA-ready architecture

## Dependencies

We minimize third-party dependencies. Key ones for security:

- `cryptography` (PyCA) — for AES-GCM, audited
- `argon2-cffi` — for password hashing, audited
- `supabase` — backend; Supabase is SOC 2 Type II
- `stripe` — billing; PCI-DSS compliant
- `fastapi` — API server; widely-used, secure-by-default

We do not vendor or fork security-sensitive libraries.

## Last updated

2026-05-11 (v1.0 preview)
