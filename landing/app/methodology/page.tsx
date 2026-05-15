import type { Metadata } from "next";
import { LegalPage } from "../../components/LegalPage";

export const metadata: Metadata = {
  title: "ROI methodology — pulse",
  description:
    "How pulse calculates Plan ROI, equivalent API value, cost per active hour, and cancellation savings — with formulas, data sources, and limitations.",
  alternates: { canonical: "/methodology" },
  openGraph: {
    title: "ROI methodology — pulse",
    description: "Plan ROI = Equivalent API Value / Subscription Cost. Here's exactly how each number is computed.",
    url: "https://mintforai.com/methodology",
    type: "article",
  },
};

export default function MethodologyPage() {
  return (
    <LegalPage
      title="ROI methodology"
      subtitle="Pulse makes claims like 'your $200 Claude plan returned $4,000 in API value.' Those numbers are computed locally from your real token usage — not estimated, not aggregated. Here is exactly how, with sources, formulas, and limitations."
      lastUpdated="2026-05-15"
    >
      <div className="not-prose mb-8 rounded-xl border border-mint-800/40 bg-mint-950/20 p-4 text-sm text-mint-200/90">
        <strong className="text-mint-300">TL;DR.</strong> Plan ROI = Equivalent API Value ÷ Subscription Cost.
        Equivalent API Value is the sum of <em>input</em>, <em>output</em>, <em>cache write (5min and 1hr TTL)</em>,
        and <em>cache read</em> token costs at published provider rates. Currencies are converted via
        ECB rates from <code>frankfurter.dev</code>, cached 24h. Everything is computed on your machine
        from the local <code>~/.claude/projects/*.jsonl</code> log files — no upload, no estimation.
      </div>

      <h2>1. Plan ROI</h2>
      <p>The headline number on the dashboard.</p>
      <pre className="not-prose rounded-xl border border-zinc-900 bg-black p-4 overflow-x-auto text-sm text-zinc-200 my-4">
{`Plan ROI = Equivalent API Value (this billing period)
           ─────────────────────────────────────────
                  Subscription Cost (this billing period)`}
      </pre>
      <p>
        A Plan ROI of <strong>10.5×</strong> means: if you had paid per-token at Anthropic's published API
        rates for everything you used this month, the bill would have been 10.5× what your flat-rate
        Claude Max subscription cost you. Higher is better. Anything &gt; 1× means the plan is paying for
        itself.
      </p>

      <h2>2. Equivalent API Value</h2>
      <p>
        For each Claude Code request logged in <code>~/.claude/projects/*.jsonl</code>, pulse extracts five
        token counts and multiplies each by the model's published rate:
      </p>
      <pre className="not-prose rounded-xl border border-zinc-900 bg-black p-4 overflow-x-auto text-sm text-zinc-200 my-4">
{`Equivalent API Value =
    input_tokens             × input_price        / 1,000,000
  + output_tokens            × output_price       / 1,000,000
  + cache_creation_5m_tokens × cw_5m_price        / 1,000,000
  + cache_creation_1h_tokens × cw_1h_price        / 1,000,000
  + cache_read_tokens        × cache_read_price   / 1,000,000`}
      </pre>
      <p>Token counts come straight from the request payload Anthropic writes to disk. No estimation.</p>

      <h2>3. Token pricing source</h2>
      <p>
        Prices are sourced from <a href="https://docs.anthropic.com/en/docs/about-claude/models/all-models" target="_blank" rel="noopener noreferrer">Anthropic's official pricing page</a>{" "}
        and bundled with the app in{" "}
        <a href="https://github.com/walight999/pulse/blob/main/sync_tokens.py" target="_blank" rel="noopener noreferrer">
          sync_tokens.py
        </a>{" "}
        as a static table — exact, not estimated.
      </p>
      <p>USD per <strong>1,000,000 tokens</strong>, current as of 2026-05:</p>
      <div className="not-prose overflow-x-auto rounded-xl border border-zinc-900 bg-black/40 my-4">
        <table className="w-full text-sm">
          <thead className="bg-zinc-950 border-b border-zinc-900 text-zinc-400">
            <tr>
              <th className="text-left font-semibold px-4 py-3">Model</th>
              <th className="text-right font-semibold px-4 py-3">Input</th>
              <th className="text-right font-semibold px-4 py-3">Output</th>
              <th className="text-right font-semibold px-4 py-3">Cache write (5m)</th>
              <th className="text-right font-semibold px-4 py-3">Cache write (1h)</th>
              <th className="text-right font-semibold px-4 py-3">Cache read</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-900 text-zinc-300">
            <tr><td className="px-4 py-2">Claude Opus 4 / 4.6 / 4.7</td><td className="text-right tabular-nums">$15.00</td><td className="text-right tabular-nums">$75.00</td><td className="text-right tabular-nums">$18.75</td><td className="text-right tabular-nums">$30.00</td><td className="text-right tabular-nums">$1.50</td></tr>
            <tr><td className="px-4 py-2">Claude Sonnet 4 / 4.5 / 4.6</td><td className="text-right tabular-nums">$3.00</td><td className="text-right tabular-nums">$15.00</td><td className="text-right tabular-nums">$3.75</td><td className="text-right tabular-nums">$6.00</td><td className="text-right tabular-nums">$0.30</td></tr>
            <tr><td className="px-4 py-2">Claude Haiku 4 / 4.5</td><td className="text-right tabular-nums">$0.80</td><td className="text-right tabular-nums">$4.00</td><td className="text-right tabular-nums">$1.00</td><td className="text-right tabular-nums">$1.60</td><td className="text-right tabular-nums">$0.08</td></tr>
          </tbody>
        </table>
      </div>
      <p>
        Pricing updates ship in pulse releases. If Anthropic changes prices and pulse hasn't shipped
        an update, the dashboard surfaces a banner suggesting you check for an update. You can also
        edit the <code>PRICING</code> table in <code>sync_tokens.py</code> directly — it's a plain Python dict.
      </p>
      <p>
        <strong>Other providers (OpenAI, Cursor, Gemini, Copilot):</strong> tracked once their parsers ship
        in v1.1 (Q3 2026). Today pulse only computes equivalent API value for Claude Code usage. Other
        subscriptions are tracked as cost line-items without per-token ROI.
      </p>

      <h2>4. Cache TTL — why 5m and 1h are split</h2>
      <p>
        Anthropic's prompt caching offers two TTLs. The 5-minute cache is cheaper to write
        (1.25× input price) but expires quickly. The 1-hour cache is more expensive to write (2.0× input
        price) but persists. Both reads are billed at 0.10× input price.
      </p>
      <p>
        Most cost trackers lump <code>cache_creation_tokens</code> together and use one rate — which is
        off by up to 60% on cache-heavy workloads. Pulse reads the TTL-split fields{" "}
        (<code>cache_creation_5m_tokens</code> + <code>cache_creation_1h_tokens</code>) directly from the log
        and prices them separately. If only the bulk field is present (older log format), pulse falls
        back to the cheaper 5-minute rate to avoid over-counting savings.
      </p>

      <h2>5. Subscription cost — exact, estimated, or per-tier?</h2>
      <p>
        Cost values entered by you in the Subscriptions tab are <strong>exact</strong>. Renewal dates,
        currency, and amount are taken straight from your input. If you select a plan from the
        built-in catalog (e.g. "Claude Max — $200/mo"), the price comes from a static table updated
        in pulse releases.
      </p>
      <p>
        FX conversion: if your subscription is in THB and your display currency is USD, pulse uses
        the latest cached ECB rate from <code>frankfurter.dev</code> at the time of display. The rate is
        re-fetched daily (24h cache). Historical conversions on already-recorded charges use the rate
        on file at the time of recording, not today's rate.
      </p>

      <h2>6. Cost per active hour</h2>
      <pre className="not-prose rounded-xl border border-zinc-900 bg-black p-4 overflow-x-auto text-sm text-zinc-200 my-4">
{`Cost per active hour =
    Subscription Cost (this billing period)
    ─────────────────────────────────────────
    Foreground hours where this subscription's
    linked app was the active window`}
      </pre>
      <p>
        "Foreground hours" comes from pulse's local activity tracker — measured in 1-second polling
        intervals when the app is in the active window and the user is not idle. Idle is detected via
        OS-level idle-time APIs (Win32 <code>GetLastInputInfo</code>, macOS <code>IOHIDIdleTime</code>,
        Linux <code>XScreenSaverQueryInfo</code>) with a 5-minute threshold.
      </p>
      <p>
        Hours where the subscription's linked app was running in the <em>background</em> are not
        counted — pulse only counts time you were actively in the window. This is intentionally
        conservative: cost-per-hour is meant to reflect real engagement, not passive presence.
      </p>
      <p>
        Activity tracking is <strong>opt-in</strong> and can be paused, app-allowlisted, or fully
        disabled at any time. See <a href="/privacy">Privacy</a>.
      </p>

      <h2>7. Cancellation savings</h2>
      <pre className="not-prose rounded-xl border border-zinc-900 bg-black p-4 overflow-x-auto text-sm text-zinc-200 my-4">
{`Cancellation savings =
    Sum across all subscriptions you've marked Cancelled, of:
        monthly_cost × months_since_cancellation_date`}
      </pre>
      <p>
        Pulse counts savings from the cancellation date forward, not retroactively. Annual subscriptions
        are normalized to a monthly rate (annual_cost ÷ 12). This is a <strong>cumulative counter</strong>{" "}
        — once you cancel something, the savings climb every month until you re-activate it.
      </p>

      <h2>8. What's exact vs estimated</h2>
      <div className="not-prose overflow-x-auto rounded-xl border border-zinc-900 bg-black/40 my-4">
        <table className="w-full text-sm">
          <thead className="bg-zinc-950 border-b border-zinc-900 text-zinc-400">
            <tr>
              <th className="text-left font-semibold px-4 py-3">Value</th>
              <th className="text-left font-semibold px-4 py-3">Source</th>
              <th className="text-center font-semibold px-4 py-3">Exact?</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-900 text-zinc-300">
            <tr><td className="px-4 py-2">Token counts (Claude Code)</td><td className="px-4 py-2"><code>~/.claude/projects/*.jsonl</code> request payloads</td><td className="text-center text-mint-400 font-semibold">Exact</td></tr>
            <tr><td className="px-4 py-2">Per-token pricing</td><td className="px-4 py-2">Anthropic published rates (static table)</td><td className="text-center text-mint-400 font-semibold">Exact</td></tr>
            <tr><td className="px-4 py-2">Subscription cost (user-entered)</td><td className="px-4 py-2">Your input</td><td className="text-center text-mint-400 font-semibold">Exact</td></tr>
            <tr><td className="px-4 py-2">Subscription cost (catalog)</td><td className="px-4 py-2">Built-in plan table</td><td className="text-center text-amber-400 font-semibold">Snapshot</td></tr>
            <tr><td className="px-4 py-2">FX conversions</td><td className="px-4 py-2">ECB rates via frankfurter.dev, 24h cache</td><td className="text-center text-amber-400 font-semibold">Snapshot</td></tr>
            <tr><td className="px-4 py-2">Foreground hours</td><td className="px-4 py-2">1s polling + idle detection</td><td className="text-center text-amber-400 font-semibold">±1%</td></tr>
            <tr><td className="px-4 py-2">Cache TTL split (older logs)</td><td className="px-4 py-2">Falls back to 5m rate if 1h field missing</td><td className="text-center text-amber-400 font-semibold">Conservative</td></tr>
            <tr><td className="px-4 py-2">Cancellation savings</td><td className="px-4 py-2">monthly_cost × months_since_cancel</td><td className="text-center text-amber-400 font-semibold">Projection</td></tr>
          </tbody>
        </table>
      </div>

      <h2>9. Limitations and honest caveats</h2>
      <ul>
        <li>
          <strong>Plan ROI assumes counterfactual API usage.</strong> If you used Claude Max heavily this
          month, the equivalent API bill would be high. But you might have used the API more
          <em>conservatively</em> if you were paying per-token. ROI tells you what the same token volume
          would cost à la carte — not what you would have <em>chosen</em> to spend.
        </li>
        <li>
          <strong>ROI only covers Claude Code today.</strong> Other AI tools (ChatGPT, Cursor, Gemini,
          Copilot) appear on the dashboard as subscription line-items but don't yet contribute to
          equivalent API value. Multi-provider live tracking ships with Pro in Q3 2026.
        </li>
        <li>
          <strong>Cache TTL fallback can under-count savings.</strong> If your Claude logs predate
          TTL-split fields, pulse uses the cheaper 5-minute rate for all cache writes. Your real
          cache value is likely higher than what pulse reports.
        </li>
        <li>
          <strong>FX rates are end-of-day ECB, not real-time.</strong> Don't use pulse for currency
          arbitrage. Historical charges use the rate cached on the day they were recorded.
        </li>
        <li>
          <strong>Cost-per-hour ignores background usage.</strong> If a tool runs in the background and
          you find that valuable (e.g. a CLI daemon), pulse's foreground-only counter under-states
          its real utility.
        </li>
        <li>
          <strong>Cancellation savings is a projection.</strong> It assumes you would have kept paying.
          If you would have switched to a free tier instead, real savings are lower.
        </li>
      </ul>

      <h2>10. Verify it yourself</h2>
      <p>
        All ROI math is in plain Python in{" "}
        <a href="https://github.com/walight999/pulse/blob/main/sync_tokens.py" target="_blank" rel="noopener noreferrer">sync_tokens.py</a>{" "}
        (the <code>calc_cost()</code> function and the <code>PRICING</code> table). The dashboard renders
        in <a href="https://github.com/walight999/pulse/blob/main/dashboard.py" target="_blank" rel="noopener noreferrer">dashboard.py</a>.
        Pulse is MIT-licensed; fork it, audit it, or rip the formulas out for your own tool.
      </p>
      <p>
        If you find a methodology bug, please open an issue at{" "}
        <a href="https://github.com/walight999/pulse/issues" target="_blank" rel="noopener noreferrer">github.com/walight999/pulse/issues</a>.
        ROI accuracy is the single most important thing this product gets right — corrections are
        welcome.
      </p>
    </LegalPage>
  );
}
