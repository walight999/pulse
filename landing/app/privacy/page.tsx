import type { Metadata } from "next";
import { LegalPage } from "../../components/LegalPage";

export const metadata: Metadata = {
  title: "Privacy — pulse",
  description:
    "Pulse is local-first by design. Your data never leaves your computer unless you explicitly opt in to a cloud feature.",
  alternates: { canonical: "/privacy" },
  openGraph: {
    title: "Privacy — pulse",
    description: "Local-first by design. Your data never leaves your computer.",
    url: "https://mintforai.com/privacy",
    type: "article",
  },
};

export default function PrivacyPage() {
  return (
    <LegalPage
      title="Privacy"
      subtitle="Pulse is local-first by design. Your data never leaves your computer unless you explicitly opt in to a cloud feature (none ship today)."
      lastUpdated="2026-05-12"
    >
      <h2>What pulse stores locally</h2>
      <p>All data lives in:</p>
      <ul>
        <li><code>data/tracker.db</code> — SQLite database</li>
        <li><code>data/fx_cache.json</code> — exchange rate snapshot</li>
        <li><code>data/waitlist.json</code> — your local waitlist signup (if any)</li>
        <li><code>data/referrals.json</code> — your referral code</li>
        <li><code>data/telemetry.jsonl</code> — usage events (only if opted in)</li>
        <li><code>logs/*.log</code> — diagnostic logs</li>
        <li><code>backups/*.db.gz</code> — last 7 daily snapshots</li>
      </ul>
      <p>The database contains:</p>
      <table>
        <thead>
          <tr><th>Data</th><th>What</th></tr>
        </thead>
        <tbody>
          <tr><td>Subscriptions</td><td>Names, costs, billing cycle, renewal dates, your notes</td></tr>
          <tr><td>App activity</td><td>Process names + foreground time + window titles</td></tr>
          <tr><td>Token usage</td><td>Per-API-call counts (input/output tokens), model name, project tag</td></tr>
          <tr><td>Settings</td><td>Currency, budgets, alert toggles, idle threshold</td></tr>
        </tbody>
      </table>
      <p>
        <strong>Window titles can be sensitive</strong> (e.g., document names, browser tab titles).
        If you don't want them tracked, delete <code>data/tracker.db</code> and disable the tracker.
      </p>

      <h2>What pulse does NOT store</h2>
      <ul>
        <li>No passwords, payment cards, or bank details</li>
        <li>No prompt content or AI conversation text (only token counts)</li>
        <li>No browser history or website URLs</li>
        <li>No screenshots or webcam captures</li>
        <li>No keystrokes or clipboard content</li>
      </ul>

      <h2>What pulse sends over the network</h2>
      <p>By default, <strong>two</strong> outbound calls happen:</p>
      <ol>
        <li>
          <strong>Exchange rates</strong> — once per 24h, GET to{" "}
          <code>https://api.frankfurter.dev/v1/latest</code>. No personal data sent. Used for
          currency conversion.
        </li>
        <li>
          <strong>(Optional) Anthropic Admin API</strong> — only if you set the{" "}
          <code>ANTHROPIC_ADMIN_KEY</code> env var. Pulls org-level token usage from your Anthropic
          account.
        </li>
      </ol>
      <p>That's it. No analytics, no telemetry, no error reporting unless you opt in.</p>

      <h2>Telemetry (opt-in)</h2>
      <p>
        If you check "Help improve pulse with anonymous usage data" in Settings, pulse logs feature
        usage events to <code>data/telemetry.jsonl</code>.{" "}
        <strong>These events stay on your computer until cloud sync ships (Phase 1)</strong>. When
        that ships, opted-in events will be batched and sent over HTTPS to the analytics endpoint.
      </p>
      <p>What's in an event:</p>
      <ul>
        <li>Event name (e.g., <code>subscription_added</code>, <code>token_sync_clicked</code>)</li>
        <li>Anonymous account UUID</li>
        <li>Timestamp</li>
        <li>Numeric counts (e.g., <code>subs_count: 5</code>)</li>
      </ul>
      <p>What's NOT:</p>
      <ul>
        <li>No subscription names</li>
        <li>No email addresses</li>
        <li>No token usage cost / amounts</li>
        <li>No app or window titles</li>
      </ul>
      <p>You can opt out at any time and delete <code>data/telemetry.jsonl</code>.</p>

      <h2>Cloud features (Pro tier — not yet shipped)</h2>
      <p>Pro will add cloud sync. When it ships:</p>
      <ul>
        <li>Data will be <strong>end-to-end encrypted</strong> with a key only you hold</li>
        <li>We will not be able to read your subscriptions, AI cost, or activity</li>
        <li>You can disable sync per device</li>
        <li>Local data remains usable if you cancel Pro</li>
      </ul>
      <p>A separate, version-stamped privacy policy will accompany the Pro release.</p>

      <h2>Data deletion</h2>
      <p>Local: delete the <code>data/</code> folder. That removes everything.</p>
      <p>
        To reinstall fresh: re-run <code>init_db()</code> or just start the app again — a new empty
        database will be created.
      </p>

      <h2>Contact</h2>
      <p>
        Questions about privacy:{" "}
        <a href="https://github.com/walight999/pulse/issues" target="_blank" rel="noopener noreferrer">
          open an issue on the repository
        </a>, or email{" "}
        <a href="mailto:hi@mintforai.com">hi@mintforai.com</a>.
      </p>
    </LegalPage>
  );
}
