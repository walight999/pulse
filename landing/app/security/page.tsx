import type { Metadata } from "next";
import { LegalPage } from "../../components/LegalPage";

export const metadata: Metadata = {
  title: "Security — pulse",
  description:
    "Pulse takes security seriously. Threat model, encryption practices, vulnerability reporting, and compliance roadmap.",
  alternates: { canonical: "/security" },
  openGraph: {
    title: "Security — pulse",
    description: "Threat model · E2E encryption · vulnerability disclosure · SOC 2 roadmap.",
    url: "https://mintforai.com/security",
    type: "article",
  },
};

export default function SecurityPage() {
  return (
    <LegalPage
      title="Security"
      subtitle="Pulse handles sensitive personal-finance data: subscription costs, AI API spending, app activity. This page lays out our threat model, security practices, and how to report vulnerabilities."
      lastUpdated="2026-05-12"
    >
      <h2>Threat model</h2>
      <p>Our threat model assumes:</p>
      <ol>
        <li><strong>The user's machine is trusted.</strong> We are not a malware sandbox.</li>
        <li>
          <strong>The user's master password is the root of trust.</strong> Lost password = lost
          cloud data (intentional — we cannot decrypt without it).
        </li>
        <li>
          <strong>The cloud service may be compromised.</strong> All synced data is encrypted with
          user-derived keys before leaving the device.
        </li>
        <li>
          <strong>Network attackers are active.</strong> All cloud traffic is TLS 1.3+.
        </li>
      </ol>

      <h2>Encryption</h2>
      <ul>
        <li>
          <strong>At rest, local:</strong> SQLite database is stored unencrypted in{" "}
          <code>data/tracker.db</code>. Users on shared machines should encrypt their disk
          (BitLocker, FileVault).
        </li>
        <li>
          <strong>At rest, cloud:</strong> Per-row AES-256-GCM with 12-byte random nonce per row.
          Server stores only ciphertext + HMAC-SHA256 searchable indexes.
        </li>
        <li>
          <strong>Key derivation:</strong> Argon2id(password, salt=account_id, m=64MB, t=3, p=1).
          The master key never leaves the device.
        </li>
        <li>
          <strong>In transit:</strong> TLS 1.3 to Supabase + Stripe + frankfurter.dev. Webhook
          endpoints (Slack/Teams/Discord) use TLS to vendor URLs.
        </li>
      </ul>
      <p>
        See{" "}
        <a href="https://github.com/walight999/pulse/blob/main/cloud/crypto.py" target="_blank" rel="noopener noreferrer">
          cloud/crypto.py
        </a>{" "}
        for the implementation.
      </p>

      <h2>Authentication</h2>
      <ul>
        <li>
          <strong>Cloud accounts:</strong> Magic-link sign-in via Supabase Auth. No passwords
          stored.
        </li>
        <li>
          <strong>JWT refresh:</strong> tokens auto-rotate every 60 minutes; refresh tokens last 30
          days.
        </li>
        <li>
          <strong>API keys:</strong> scoped to user's own data only. Generated in Settings →
          Developer. Revocable. Logged in audit table.
        </li>
        <li>
          <strong>SSO (Enterprise):</strong> SAML 2.0 + OIDC via Supabase Pro / Auth0. Configurable
          per organization with domain allowlists.
        </li>
      </ul>

      <h2>Privacy</h2>
      <ul>
        <li>Local-only mode requires zero account, zero telemetry.</li>
        <li>
          Cloud mode: opt-in only. Each synced data category (subscriptions, AI usage, activity)
          toggleable separately.
        </li>
        <li>
          Leaderboard: opt-in only with three visibility levels (off / friends / public). Aggregate
          metrics only — raw token data never leaves the device.
        </li>
        <li>No analytics, no fingerprinting, no third-party trackers.</li>
      </ul>
      <p>
        See <a href="/privacy">Privacy</a> for the full privacy policy.
      </p>

      <h2>Audit logging</h2>
      <p>
        Pulse maintains a local audit log (<code>audit_log</code> table) of:
      </p>
      <ul>
        <li>Sign in / sign out events</li>
        <li>API key creation / revocation</li>
        <li>Team membership changes</li>
        <li>Settings changes (currency, plan, alerts)</li>
        <li>Export operations</li>
        <li>Sync events (counts only, never content)</li>
      </ul>
      <p>
        Cloud accounts get a mirror in Supabase audit table, retained for 90 days (Pro) / 1 year
        (Team) / 7 years (Enterprise).
      </p>

      <h2>Reporting vulnerabilities</h2>
      <p>If you discover a security issue, <strong>please do not file a public issue</strong>.</p>
      <p>
        Email: <a href="mailto:security@mintforai.com">security@mintforai.com</a> or DM{" "}
        <a href="https://github.com/walight999" target="_blank" rel="noopener noreferrer">@walight999</a> on GitHub.
      </p>
      <p>We aim to:</p>
      <ul>
        <li>Acknowledge within 24 hours</li>
        <li>Fix critical issues within 7 days</li>
        <li>Coordinate disclosure with the reporter</li>
        <li>Credit reporters publicly (if they wish)</li>
      </ul>

      <h2>Bug bounty</h2>
      <p>
        Once pulse Pro launches with paying customers, we will offer a bug bounty program.
        Estimated tiers:
      </p>
      <ul>
        <li>Critical (RCE, auth bypass, mass data leak): $500–2000</li>
        <li>High (auth flaw, IDOR): $200–500</li>
        <li>Medium (XSS, CSRF, broken access): $50–200</li>
      </ul>

      <h2>Compliance roadmap</h2>
      <ul>
        <li><strong>v1.0 (current):</strong> MIT-licensed local app, no compliance certifications needed</li>
        <li><strong>v2.0 (Cloud):</strong> GDPR-compliant data handling, EU data residency option</li>
        <li><strong>v2.5 (Team):</strong> SOC 2 Type I audit (Drata + reputable auditor)</li>
        <li><strong>v3.0 (Enterprise):</strong> SOC 2 Type II, ISO 27001, HIPAA-ready architecture</li>
      </ul>

      <h2>Dependencies</h2>
      <p>We minimize third-party dependencies. Key ones for security:</p>
      <ul>
        <li><code>cryptography</code> (PyCA) — for AES-GCM, audited</li>
        <li><code>argon2-cffi</code> — for password hashing, audited</li>
        <li><code>supabase</code> — backend; Supabase is SOC 2 Type II</li>
        <li><code>stripe</code> — billing; PCI-DSS compliant</li>
        <li><code>fastapi</code> — API server; widely-used, secure-by-default</li>
      </ul>
      <p>We do not vendor or fork security-sensitive libraries.</p>
    </LegalPage>
  );
}
