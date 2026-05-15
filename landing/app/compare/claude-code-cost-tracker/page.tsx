import type { Metadata } from "next";
import { LegalPage } from "../../../components/LegalPage";

export const metadata: Metadata = {
  title: "Claude Code cost tracker — pulse",
  description:
    "Pulse is the local-first Claude Code cost tracker. Parses ~/.claude/projects/*.jsonl directly, computes Plan ROI vs API rates, splits cache TTL 5min and 1hr pricing correctly, runs 100% offline. MIT open-source.",
  keywords: [
    "claude code cost tracker",
    "claude code usage tracker",
    "claude code token cost",
    "claude max ROI",
    "anthropic api cost dashboard",
    "claude cache pricing",
  ],
  alternates: { canonical: "/compare/claude-code-cost-tracker" },
  openGraph: {
    title: "Claude Code cost tracker — pulse",
    description: "Local Claude Code cost tracker that gets cache TTL pricing right. Plan ROI in real time.",
    url: "https://mintforai.com/compare/claude-code-cost-tracker",
    type: "article",
  },
};

export default function ClaudeCodeCostTrackerPage() {
  return (
    <LegalPage
      title="Claude Code cost tracker"
      subtitle="Pulse is the local-first cost tracker built specifically for Claude Code. It reads your ~/.claude/projects/*.jsonl logs directly, computes cost per request at Anthropic's published rates, and tells you whether your Claude Max plan is paying off."
      lastUpdated="2026-05-15"
    >
      <p>
        Most "Claude cost tools" are export-uploaders or API-key dashboards. Pulse is different in
        three ways that matter when you're tracking heavy Claude Code usage:
      </p>
      <ol>
        <li>
          <strong>Local parser, no upload.</strong> Token counts are extracted from the same log files Claude Code
          writes to disk. Nothing leaves your machine. You don't paste an Admin API key, you don't share a
          workspace, you don't grant access to an OAuth scope.
        </li>
        <li>
          <strong>Cache TTL pricing split correctly.</strong> Anthropic bills 5-minute cache writes at 1.25×
          input rate and 1-hour cache writes at 2.0× input rate. Most cost trackers lump them together and
          get the bill wrong by 10–60% on cache-heavy workloads. Pulse reads{" "}
          <code>cache_creation_5m_tokens</code> and <code>cache_creation_1h_tokens</code> separately and prices
          each at its actual rate.
        </li>
        <li>
          <strong>Plan ROI scoring.</strong> Anthropic's Console shows API spend. Claude Max users have <em>flat-plan</em>{" "}
          usage that the Console doesn't surface at all. Pulse converts your token volume to an equivalent
          API bill — so you can answer "is my $200/mo Claude Max plan actually saving me money?" with a
          real number, not a vibe.
        </li>
      </ol>

      <h2>What you get on day one</h2>
      <ul>
        <li><strong>Plan ROI</strong> — e.g. 10.5× means $2,100 of API value for $200 of subscription</li>
        <li><strong>Per-model breakdown</strong> — Opus / Sonnet / Haiku, input / output / cache write 5m / cache write 1h / cache read</li>
        <li><strong>Per-project costs</strong> — costs grouped by the project directory Claude Code wrote logs from</li>
        <li><strong>Cost spike alerts</strong> — Windows toast when today exceeds 3× your 30-day average</li>
        <li><strong>Multi-currency display</strong> — 30+ currencies via daily ECB rates from frankfurter.dev</li>
        <li><strong>CSV export</strong> — same format as the <a href="/demo">interactive demo's sample CSV</a></li>
      </ul>

      <h2>How pulse compares to other Claude tools</h2>
      <div className="not-prose overflow-x-auto rounded-xl border border-zinc-900 bg-black/40 my-4">
        <table className="w-full text-sm">
          <thead className="bg-zinc-950 border-b border-zinc-900 text-zinc-400">
            <tr>
              <th className="text-left font-semibold px-4 py-3">Feature</th>
              <th className="text-center font-semibold px-4 py-3 text-mint-400">pulse</th>
              <th className="text-center font-semibold px-4 py-3">ClaudeMetrics</th>
              <th className="text-center font-semibold px-4 py-3">Anthropic Console</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-900 text-zinc-300">
            <tr><td className="px-4 py-2">Reads ~/.claude/projects/*.jsonl locally</td><td className="text-center text-mint-400 font-bold">✓</td><td className="text-center text-zinc-600">requires export</td><td className="text-center text-zinc-600">—</td></tr>
            <tr><td className="px-4 py-2">Cache TTL 5m + 1h split pricing</td><td className="text-center text-mint-400 font-bold">✓</td><td className="text-center text-zinc-600">approximate</td><td className="text-center text-mint-400 font-bold">✓</td></tr>
            <tr><td className="px-4 py-2">Plan ROI vs API equivalent</td><td className="text-center text-mint-400 font-bold">✓</td><td className="text-center text-zinc-600">—</td><td className="text-center text-zinc-600">—</td></tr>
            <tr><td className="px-4 py-2">Covers Claude Max flat-plan usage</td><td className="text-center text-mint-400 font-bold">✓</td><td className="text-center text-mint-400 font-bold">✓</td><td className="text-center text-zinc-600">— (API only)</td></tr>
            <tr><td className="px-4 py-2">Combines with non-Claude subscriptions</td><td className="text-center text-mint-400 font-bold">✓</td><td className="text-center text-zinc-600">—</td><td className="text-center text-zinc-600">—</td></tr>
            <tr><td className="px-4 py-2">Activity tracking (cost per active hour)</td><td className="text-center text-mint-400 font-bold">✓</td><td className="text-center text-zinc-600">—</td><td className="text-center text-zinc-600">—</td></tr>
            <tr><td className="px-4 py-2">Runs offline</td><td className="text-center text-mint-400 font-bold">✓</td><td className="text-center text-zinc-600">—</td><td className="text-center text-zinc-600">—</td></tr>
            <tr><td className="px-4 py-2">MIT open-source (audit the math)</td><td className="text-center text-mint-400 font-bold">✓</td><td className="text-center text-zinc-600">—</td><td className="text-center text-zinc-600">—</td></tr>
            <tr><td className="px-4 py-2">Cost</td><td className="text-center text-mint-400 font-bold">Free</td><td className="text-center text-zinc-400 text-xs">Free + paid</td><td className="text-center text-zinc-400 text-xs">API price</td></tr>
          </tbody>
        </table>
      </div>

      <h2>The cache-TTL math (why most trackers are wrong)</h2>
      <p>
        Anthropic published two cache TTLs (5-minute and 1-hour) at different write prices. Cache writes
        with the 5-minute TTL cost 1.25× the input price; 1-hour TTL costs 2.0× input. Cache reads are
        0.10× input price regardless of TTL.
      </p>
      <p>
        Older Claude logs only had a single <code>cache_creation_tokens</code> field. Newer logs split it into{" "}
        <code>cache_creation_5m_tokens</code> and <code>cache_creation_1h_tokens</code>. Pulse uses the split fields
        when present and falls back to the cheaper 5-minute rate when only the bulk field exists — so your
        ROI is never overstated.
      </p>
      <p>
        Full pricing table for Opus / Sonnet / Haiku is on{" "}
        <a href="/methodology#3-token-pricing-source">/methodology § 3</a>.
      </p>

      <h2>Install + first ROI in 5 minutes</h2>
      <ol>
        <li>Download <a href="/download">pulse for Windows</a> (~80 MB installer) — or run from source on macOS/Linux</li>
        <li>Open the dashboard from the system tray icon</li>
        <li>Complete the 30-second onboarding (currency, optional plan price, activity tracking opt-in)</li>
        <li>Pulse auto-imports your Claude Code logs from <code>~/.claude/projects/*.jsonl</code></li>
        <li>Plan ROI appears on the Overview tab — refreshed every 6 hours</li>
      </ol>

      <h2>Try the interactive demo</h2>
      <p>
        See the dashboard with fake-but-realistic data before installing —{" "}
        <a href="/demo">▶ Open interactive demo</a>. All numbers compute live from the same formulas the
        real app uses.
      </p>

      <p>
        <a href="/download" className="text-mint-400 hover:text-mint-300">⬇ Download pulse</a> ·{" "}
        <a href="/methodology" className="text-mint-400 hover:text-mint-300">📐 How ROI is computed</a> ·{" "}
        <a href="/alternatives" className="text-mint-400 hover:text-mint-300">⚖ Compared to alternatives</a> ·{" "}
        <a href="https://github.com/walight999/pulse" target="_blank" rel="noopener noreferrer" className="text-mint-400 hover:text-mint-300">⭐ GitHub</a>
      </p>
    </LegalPage>
  );
}
