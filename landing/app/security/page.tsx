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

type BadgeKind = "shipped" | "designed-pro" | "planned-team" | "enterprise-roadmap" | "not-certified";

function StatusBadge({ kind }: { kind: BadgeKind }) {
  const map: Record<BadgeKind, { label: string; cls: string }> = {
    "shipped":            { label: "Implemented · local mode",   cls: "bg-mint-900/40 text-mint-400 border-mint-800/60" },
    "designed-pro":       { label: "Designed for Pro · not yet shipped", cls: "bg-amber-900/40 text-amber-400 border-amber-800/60" },
    "planned-team":       { label: "Planned for Team",           cls: "bg-amber-900/30 text-amber-300 border-amber-800/40" },
    "enterprise-roadmap": { label: "Enterprise roadmap",         cls: "bg-zinc-900 text-zinc-400 border-zinc-800" },
    "not-certified":      { label: "Not certified yet",          cls: "bg-zinc-900 text-zinc-500 border-zinc-800" },
  };
  const { label, cls } = map[kind];
  return (
    <span className={`not-prose inline-block text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 ml-2 rounded border align-middle ${cls}`}>
      {label}
    </span>
  );
}

export default function SecurityPage() {
  return (
    <LegalPage
      title="Security"
      subtitle="Pulse handles sensitive personal-finance data: subscription costs, AI API spending, app activity. This page lays out our threat model, what's implemented today, what's designed but not yet shipped, and what's on the roadmap."
      lastUpdated="2026-05-15"
    >
      <div className="not-prose mb-8 rounded-xl border border-amber-800/40 bg-amber-950/20 p-4 text-sm text-amber-200/90">
        <strong className="text-amber-300">Status legend.</strong> Each section below is tagged with one of:{" "}
        <span className="inline-block px-1.5 py-0.5 rounded bg-mint-900/40 text-mint-400 border border-mint-800/60 text-[10px] font-bold uppercase tracking-wider">Implemented · local mode</span>{" "}
        <span className="inline-block px-1.5 py-0.5 rounded bg-amber-900/40 text-amber-400 border border-amber-800/60 text-[10px] font-bold uppercase tracking-wider">Designed for Pro</span>{" "}
        <span className="inline-block px-1.5 py-0.5 rounded bg-amber-900/30 text-amber-300 border border-amber-800/40 text-[10px] font-bold uppercase tracking-wider">Planned for Team</span>{" "}
        <span className="inline-block px-1.5 py-0.5 rounded bg-zinc-900 text-zinc-400 border border-zinc-800 text-[10px] font-bold uppercase tracking-wider">Enterprise roadmap</span>{" "}
        <span className="inline-block px-1.5 py-0.5 rounded bg-zinc-900 text-zinc-500 border border-zinc-800 text-[10px] font-bold uppercase tracking-wider">Not certified yet</span>.
        Pulse v1.0 today is a local Streamlit app. The cloud server, mobile PWA, SSO, SOC 2, on-prem, and SLA features described below are <em>designed and partially scaffolded in code</em>, but no cloud service is in production and no certification has been issued.
      </div>

      <h2>Threat model</h2>
      <p>Our threat model assumes:</p>
      <ol>
        <li><strong>The user's machine is trusted.</strong> We are not a malware sandbox.</li>
        <li>
          <strong>The user's master password is the root of trust.</strong> Lost password = lost
          cloud data (intentional — we cannot decrypt without it). <em>Applies once Pro cloud sync ships.</em>
        </li>
        <li>
          <strong>The cloud service may be compromised.</strong> All synced data is designed to be encrypted with
          user-derived keys before leaving the device. <em>Cloud sync is not yet live.</em>
        </li>
        <li>
          <strong>Network attackers are active.</strong> Any future cloud traffic will require TLS 1.3+.
        </li>
      </ol>

      <h2>Encryption</h2>
      <ul>
        <li>
          <strong>At rest, local:</strong> SQLite database is stored unencrypted in{" "}
          <code>data/tracker.db</code>. Users on shared machines should encrypt their disk
          (BitLocker, FileVault). <StatusBadge kind="shipped" />
        </li>
        <li>
          <strong>At rest, cloud:</strong> Per-row AES-256-GCM with 12-byte random nonce per row.
          Server stores only ciphertext + HMAC-SHA256 searchable indexes. <StatusBadge kind="designed-pro" />
        </li>
        <li>
          <strong>Key derivation:</strong> Argon2id(password, salt=account_id, m=64MB, t=3, p=1).
          The master key never leaves the device. <StatusBadge kind="designed-pro" />
        </li>
        <li>
          <strong>In transit:</strong> Local app's only outbound call is to frankfurter.dev over HTTPS.
          Future cloud sync will use TLS 1.3 to Supabase + Stripe. <StatusBadge kind="designed-pro" />
        </li>
      </ul>
      <p>
        See{" "}
        <a href="https://github.com/walight999/pulse/blob/main/cloud/crypto.py" target="_blank" rel="noopener noreferrer">
          cloud/crypto.py
        </a>{" "}
        for the implementation scaffold. The cloud server itself is not yet deployed.
      </p>

      <h2>Authentication</h2>
      <ul>
        <li>
          <strong>Local app:</strong> No account required, no sign-in, no telemetry by default. <StatusBadge kind="shipped" />
        </li>
        <li>
          <strong>Cloud accounts (Pro):</strong> Magic-link sign-in via Supabase Auth planned. No passwords
          stored. <StatusBadge kind="designed-pro" />
        </li>
        <li>
          <strong>JWT refresh:</strong> tokens auto-rotate every 60 minutes; refresh tokens last 30
          days. <StatusBadge kind="designed-pro" />
        </li>
        <li>
          <strong>API keys:</strong> scoped to user's own data only. Generated in Settings →
          Developer. Revocable. Logged in audit table. <StatusBadge kind="designed-pro" />
        </li>
        <li>
          <strong>SSO:</strong> SAML 2.0 + OIDC via Supabase Pro / Auth0. Configurable per organization with
          domain allowlists. <StatusBadge kind="enterprise-roadmap" />
        </li>
      </ul>

      <h2>Privacy</h2>
      <ul>
        <li>Local-only mode requires zero account, zero telemetry. <StatusBadge kind="shipped" /></li>
        <li>
          Cloud mode: opt-in only. Each synced data category (subscriptions, AI usage, activity)
          toggleable separately. <StatusBadge kind="designed-pro" />
        </li>
        <li>
          Leaderboard: opt-in only with three visibility levels (off / friends / public). Aggregate
          metrics only — raw token data never leaves the device. <StatusBadge kind="designed-pro" />
        </li>
        <li>No analytics, no fingerprinting, no third-party trackers in the local app today. <StatusBadge kind="shipped" /></li>
      </ul>
      <p>
        See <a href="/privacy">Privacy</a> for the full privacy policy.
      </p>

      <h2>Audit logging</h2>
      <p>
        Pulse maintains a local audit log (<code>audit_log</code> table) of: <StatusBadge kind="shipped" />
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
        Cloud-side audit mirror with 90d (Pro) / 1yr (Team) / 7yr (Enterprise) retention is{" "}
        <StatusBadge kind="planned-team" /> — not yet running in production.
      </p>

      <h2>Reporting vulnerabilities</h2>
      <p>If you discover a security issue, <strong>please do not file a public issue</strong>. <StatusBadge kind="shipped" /></p>
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
        Once pulse Pro launches with paying customers, we will offer a bug bounty program. <StatusBadge kind="planned-team" />
        Estimated tiers (subject to change):
      </p>
      <ul>
        <li>Critical (RCE, auth bypass, mass data leak): $500–2000</li>
        <li>High (auth flaw, IDOR): $200–500</li>
        <li>Medium (XSS, CSRF, broken access): $50–200</li>
      </ul>

      <h2>Compliance roadmap</h2>
      <p>
        Pulse holds no security certifications today. The local v1.0 app is MIT-licensed open source
        and does not require certification to run. The targets below are planned milestones, not
        commitments.
      </p>
      <ul>
        <li><strong>v1.0 (current):</strong> MIT-licensed local app, no compliance certifications needed. <StatusBadge kind="shipped" /></li>
        <li><strong>v2.0 (Cloud / Pro):</strong> GDPR-compliant data handling, EU data residency option. <StatusBadge kind="designed-pro" /></li>
        <li><strong>v2.5 (Team):</strong> SOC 2 Type I audit (Drata + reputable auditor). <StatusBadge kind="planned-team" /> <StatusBadge kind="not-certified" /></li>
        <li><strong>v3.0 (Enterprise):</strong> SOC 2 Type II, ISO 27001, HIPAA-ready architecture. <StatusBadge kind="enterprise-roadmap" /> <StatusBadge kind="not-certified" /></li>
      </ul>

      <h2>Service-level claims</h2>
      <p>
        There is no production cloud service today and therefore no SLA is offered. The "99.9% SLA"
        figure referenced on the pricing page is a planned commitment for Enterprise contracts
        once the cloud service is live and stable. <StatusBadge kind="enterprise-roadmap" />
      </p>

      <h2>Dependencies</h2>
      <p>We minimize third-party dependencies. Key ones for security:</p>
      <ul>
        <li><code>cryptography</code> (PyCA) — for AES-GCM, audited</li>
        <li><code>argon2-cffi</code> — for password hashing, audited</li>
        <li><code>supabase</code> — backend (planned); Supabase is SOC 2 Type II</li>
        <li><code>stripe</code> — billing (planned); PCI-DSS compliant</li>
        <li><code>fastapi</code> — API server (scaffolded); widely-used, secure-by-default</li>
      </ul>
      <p>We do not vendor or fork security-sensitive libraries.</p>
    </LegalPage>
  );
}
