import type { Metadata } from "next";
import { LegalPage } from "../../../components/LegalPage";

export const metadata: Metadata = {
  title: "Cursor cost tracker — pulse",
  description:
    "Track your Cursor Pro subscription cost, foreground time, and cost-per-active-hour today. Cursor token-level tracking ships with pulse Pro Q3 2026 via the local Cursor state-DB parser.",
  keywords: [
    "cursor cost tracker",
    "cursor pro tracker",
    "cursor ai usage",
    "cursor vs copilot cost",
    "ai ide cost dashboard",
  ],
  alternates: { canonical: "/compare/cursor-cost-tracker" },
  openGraph: {
    title: "Cursor cost tracker — pulse",
    description: "Track Cursor Pro cost + active hours + cost-per-hour today; token-level tracking Q3 2026.",
    url: "https://mintforai.com/compare/cursor-cost-tracker",
    type: "article",
  },
};

export default function CursorCostTrackerPage() {
  return (
    <LegalPage
      title="Cursor cost tracker"
      subtitle="Pulse tracks your Cursor Pro subscription cost, foreground time in the Cursor app, and cost per active hour — today, in v1.0. Cursor token-level tracking (the local Cursor state-DB parser) ships with Pulse Pro in Q3 2026."
      lastUpdated="2026-05-15"
    >
      <div className="not-prose mb-8 rounded-xl border border-amber-800/40 bg-amber-950/20 p-4 text-sm text-amber-200/90">
        <strong className="text-amber-300">Status:</strong> Cursor subscription tracking + activity tracking
        are <em>available now</em> in pulse v1.0. Token-level usage parsing (per-request cost, per-model
        breakdown) ships with Pro in Q3 2026 — the parser code exists at{" "}
        <a href="https://github.com/walight999/pulse/blob/main/providers/cursor_parser.py" target="_blank" rel="noopener noreferrer">
          providers/cursor_parser.py
        </a>{" "}
        but isn't wired into the dashboard yet.
      </div>

      <h2>What works today (v1.0, free local app)</h2>
      <ul>
        <li>
          <strong>Subscription cost tracking.</strong> Add Cursor Pro at $20/mo (or whatever you pay).
          Multi-currency. Renewal alerts. Auto-detect from email receipts (if you import them).
        </li>
        <li>
          <strong>Foreground time tracking.</strong> Link the Cursor subscription to <code>Cursor.exe</code>{" "}
          (or <code>cursor</code> on macOS/Linux). Pulse measures how many hours you spent in Cursor with
          the window in focus, idle-aware (5-min threshold).
        </li>
        <li>
          <strong>Cost per active hour.</strong> $20/mo ÷ 24 hours of focused Cursor time = $0.83/hour.
          See it for every subscription side-by-side.
        </li>
        <li>
          <strong>Cancellation savings.</strong> If you cancel Cursor and switch to Claude Code, pulse counts
          the cumulative $/month saved from cancellation date forward.
        </li>
      </ul>

      <h2>What ships in Q3 2026 (Pro)</h2>
      <ul>
        <li>
          <strong>Per-request cost breakdown</strong> from Cursor's local state DB. Cursor stores recent
          requests + response IDs locally; the parser reads them and joins against published OpenAI / Anthropic
          rates.
        </li>
        <li><strong>Per-model breakdown</strong> — how much of your Cursor usage hits gpt-4o vs Sonnet vs Claude</li>
        <li><strong>Dashboard usage (when paste-cookie supplied)</strong> — pulls daily usage from cursor.com's dashboard API</li>
        <li><strong>Cross-tool ROI</strong> — Claude Code + Cursor + Copilot combined ROI score</li>
      </ul>

      <h2>Cursor vs Claude Code vs Copilot — cost per hour rough math</h2>
      <p>
        Same fake data as the <a href="/demo">interactive demo</a> (developer persona):
      </p>
      <div className="not-prose overflow-x-auto rounded-xl border border-zinc-900 bg-black/40 my-4">
        <table className="w-full text-sm">
          <thead className="bg-zinc-950 border-b border-zinc-900 text-zinc-400">
            <tr>
              <th className="text-left font-semibold px-4 py-3">Tool</th>
              <th className="text-right font-semibold px-4 py-3">Monthly cost</th>
              <th className="text-right font-semibold px-4 py-3">Active hours / mo</th>
              <th className="text-right font-semibold px-4 py-3">Cost / active hour</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-900 text-zinc-300">
            <tr><td className="px-4 py-2 font-medium text-zinc-100">Claude Max (via Claude Code)</td><td className="text-right tabular-nums">$200</td><td className="text-right tabular-nums">92 hr</td><td className="text-right tabular-nums text-mint-400 font-semibold">$2.17</td></tr>
            <tr><td className="px-4 py-2 font-medium text-zinc-100">Cursor Pro</td><td className="text-right tabular-nums">$20</td><td className="text-right tabular-nums">60 hr</td><td className="text-right tabular-nums text-mint-400 font-semibold">$0.33</td></tr>
            <tr><td className="px-4 py-2 font-medium text-zinc-100">GitHub Copilot</td><td className="text-right tabular-nums">$10</td><td className="text-right tabular-nums">48 hr</td><td className="text-right tabular-nums text-mint-400 font-semibold">$0.21</td></tr>
          </tbody>
        </table>
      </div>
      <p className="text-xs text-zinc-500">
        Numbers are illustrative. Real usage varies wildly. Pulse computes these from your actual foreground
        time on your machine.
      </p>

      <h2>Privacy guarantees (because Cursor IDE has access to your code)</h2>
      <p>
        Pulse never reads your <em>code</em>. It reads:
      </p>
      <ul>
        <li>Subscription metadata you enter manually</li>
        <li>The Cursor process name (<code>Cursor.exe</code> or similar) when the window is in focus</li>
        <li>Window titles only if you opted in (off by default; the brief case for turning this off is open project paths in titles)</li>
        <li><em>Future:</em> Cursor's local request-ID state-DB rows (request count + token estimates, never prompt content)</li>
      </ul>
      <p>
        Pulse is MIT-licensed — see <a href="https://github.com/walight999/pulse/blob/main/tracker.py" target="_blank" rel="noopener noreferrer">tracker.py</a>{" "}
        and <a href="https://github.com/walight999/pulse/blob/main/providers/cursor_parser.py" target="_blank" rel="noopener noreferrer">providers/cursor_parser.py</a>{" "}
        to audit exactly what's read.
      </p>

      <h2>Install + start tracking today</h2>
      <ol>
        <li>Download <a href="/download">pulse for Windows</a> (mac/Linux from source)</li>
        <li>Onboarding asks if you want to enable activity tracking — turn it on if you want cost-per-hour numbers for Cursor</li>
        <li>Subscriptions tab → Add subscription → "Cursor Pro" → $20/mo</li>
        <li>Subscriptions tab → Edit Cursor row → linked app: <code>Cursor.exe</code></li>
        <li>Cost-per-hour shows up after your first hour in Cursor</li>
      </ol>

      <p>
        <a href="/download" className="text-mint-400 hover:text-mint-300">⬇ Download pulse</a> ·{" "}
        <a href="/demo" className="text-mint-400 hover:text-mint-300">▶ Interactive demo</a> ·{" "}
        <a href="/methodology#6-cost-per-active-hour" className="text-mint-400 hover:text-mint-300">📐 Cost-per-hour math</a> ·{" "}
        <a href="/alternatives" className="text-mint-400 hover:text-mint-300">⚖ Compared to alternatives</a>
      </p>
    </LegalPage>
  );
}
