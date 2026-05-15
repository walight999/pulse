import type { Metadata } from "next";
import { LegalPage } from "../../components/LegalPage";

export const metadata: Metadata = {
  title: "Pulse vs alternatives — Mint, YNAB, ClaudeMetrics, Vantage",
  description:
    "Honest comparison of pulse against ClaudeMetrics, Anthropic Console, OpenAI Usage, Vantage, Mint (shut down 2024), YNAB, Lunch Money, and Actual Budget. Open-source local-first Mint alternative for the AI era.",
  keywords: [
    "open source mint alternative",
    "ai subscription tracker",
    "ClaudeMetrics alternative",
    "Vantage alternative",
    "local first finance dashboard",
    "YNAB AI",
    "open source budget tracker",
  ],
  alternates: { canonical: "/alternatives" },
  openGraph: {
    title: "Pulse vs alternatives — honest comparison",
    description: "How pulse compares to ClaudeMetrics, Vantage, Mint, YNAB, and other personal/SaaS finance tools — for AI power users.",
    url: "https://mintforai.com/alternatives",
    type: "article",
  },
};

export default function AlternativesPage() {
  return (
    <LegalPage
      title="Pulse vs alternatives"
      subtitle="Honest, scored comparison against every tool people ask about. No 'we're better at everything' — pulse trades a few things off, and this page says what."
      lastUpdated="2026-05-15"
    >
      <p>
        Mint shut down in March 2024. People who relied on it have been hunting for a replacement
        that handles AI subscriptions correctly — because the cost of Claude Max, ChatGPT Plus,
        Cursor, Copilot, and a dozen smaller AI tools is now the biggest discretionary line in many
        software-team budgets. This page maps where pulse fits relative to the alternatives.
      </p>

      <h2>Category 1 — AI-cost trackers (closest competitors)</h2>

      <h3>ClaudeMetrics</h3>
      <p>
        Anthropic-specific cost analyzer. You upload a Claude export and it computes token costs. Web
        app, paid tier for teams.
      </p>
      <ul>
        <li><strong>Where ClaudeMetrics wins:</strong> hosted web app, no install, share via URL.</li>
        <li>
          <strong>Where pulse wins:</strong> reads <code>~/.claude/projects/*.jsonl</code> directly with no
          upload step; combines AI usage with subscription tracking and activity tracking in one dashboard;
          MIT open-source; cache TTL 5m + 1h pricing split correctly.
        </li>
        <li><strong>When to pick ClaudeMetrics:</strong> you don't want to install anything and a web app is fine.</li>
        <li><strong>When to pick pulse:</strong> you want the full picture (subs + tokens + active hours), local-first by default, and ROI in real time.</li>
      </ul>

      <h3>Anthropic Console (usage page)</h3>
      <p>
        The built-in usage dashboard at <code>console.anthropic.com</code>. Shows API spend by day and model.
      </p>
      <ul>
        <li><strong>Where the Console wins:</strong> authoritative source for API spend, official.</li>
        <li>
          <strong>Where pulse wins:</strong> covers <em>Claude Max flat-plan</em> usage (which the Console doesn't
          show); computes equivalent API value (Plan ROI); tracks non-Claude tools too.
        </li>
        <li><strong>When to pick Console:</strong> you only use the Anthropic API, never the Claude Max plan.</li>
        <li><strong>When to pick pulse:</strong> Claude Max is in your stack, you want to know if the flat plan is paying off vs per-token.</li>
      </ul>

      <h3>OpenAI Usage dashboard</h3>
      <p>
        Same role as Anthropic Console but for OpenAI API.
      </p>
      <ul>
        <li><strong>OpenAI Usage wins:</strong> official, real-time, no API-key sharing needed.</li>
        <li>
          <strong>Pulse wins:</strong> ChatGPT Plus subscription cost is invisible to the OpenAI dashboard;
          pulse captures it. Plus tracks the rest of your AI stack in one place.
        </li>
        <li><strong>OpenAI multi-provider live tracking is planned for pulse Q3 2026</strong> — until then, pulse handles ChatGPT Plus as a subscription line-item.</li>
      </ul>

      <h2>Category 2 — Cloud cost dashboards (adjacent)</h2>

      <h3>Vantage</h3>
      <p>
        SaaS cost-management platform for AWS / GCP / Azure / Datadog / SaaS subscriptions. Used by FinOps teams.
      </p>
      <ul>
        <li><strong>Vantage wins:</strong> deep cloud-bill analysis, RI/SP recommendations, multi-account governance, FinOps-team features.</li>
        <li>
          <strong>Pulse wins:</strong> AI subscription + per-token ROI is a category Vantage doesn't cover;
          local-first (no SOC 2 negotiation, no contract); free MIT-licensed.
        </li>
        <li>
          <strong>Best combo:</strong> Vantage for cloud infra, pulse for AI subscriptions + per-user usage. They don't overlap.
        </li>
      </ul>

      <h3>Pry / Cledara / Spendflo</h3>
      <p>
        SaaS subscription management for finance teams. Handles renewals, vendor relations, approvals.
      </p>
      <ul>
        <li><strong>They win:</strong> approval workflows, vendor negotiation, finance-team handoff, multi-employee SaaS visibility.</li>
        <li><strong>Pulse wins:</strong> connects subscription cost to actual usage (foreground time, token consumption). Most SaaS-management tools are blind to whether you're actually <em>using</em> what you pay for.</li>
      </ul>

      <h2>Category 3 — Personal finance (the Mint replacement question)</h2>

      <h3>Mint — shut down March 2024</h3>
      <p>
        Intuit shut Mint down and migrated users to Credit Karma. People who used Mint to track recurring
        subscriptions are looking for replacements. Pulse is one option <em>specifically</em> for users whose
        budget is dominated by AI tools and SaaS.
      </p>

      <h3>YNAB (You Need A Budget)</h3>
      <p>
        Zero-based budgeting app, $14.99/mo or $109/yr. Cloud sync, mobile apps, strong community.
      </p>
      <ul>
        <li><strong>YNAB wins:</strong> full-spectrum personal finance, debt payoff, joint accounts, mobile-first, accountability community.</li>
        <li><strong>Pulse wins:</strong> AI-aware categorization out of the box; tracks usage hours, not just spend; local-first means zero recurring cost.</li>
        <li><strong>Best combo:</strong> YNAB for life budgeting, pulse for the AI/SaaS slice.</li>
      </ul>

      <h3>Lunch Money</h3>
      <p>
        Modern personal-finance app, $10/mo. Strong on transactions + crypto + multi-currency.
      </p>
      <ul>
        <li><strong>Lunch Money wins:</strong> bank-account auto-sync (Plaid), crypto holdings, rich UI for transactions.</li>
        <li><strong>Pulse wins:</strong> no bank credentials required, no monthly fee, AI-specific ROI metrics.</li>
      </ul>

      <h3>Actual Budget</h3>
      <p>
        Open-source local-first envelope budgeting, MIT-ish license, self-host friendly. Closest <em>spiritual</em>
        cousin to pulse.
      </p>
      <ul>
        <li><strong>Actual wins:</strong> envelope budgeting workflow, mature import/export, multi-currency, well-documented self-host.</li>
        <li><strong>Pulse wins:</strong> AI-cost focus (Plan ROI, cache TTL, token-level math); activity tracking; built-in Claude Code log parser.</li>
        <li><strong>Best combo:</strong> Actual for general budgeting, pulse for AI-specific deep-dive. Both local-first, both MIT, same philosophy.</li>
      </ul>

      <h3>Tiller, Copilot, Monarch, Quicken Simplifi</h3>
      <p>
        Spreadsheet-first (Tiller), opinionated personal finance (Monarch, Copilot), legacy (Quicken). None
        treats AI tooling as a primary category — pulse is complementary, not competitive.
      </p>

      <h2>Quick-pick guide</h2>
      <div className="not-prose overflow-x-auto rounded-xl border border-zinc-900 bg-black/40 my-4">
        <table className="w-full text-sm">
          <thead className="bg-zinc-950 border-b border-zinc-900 text-zinc-400">
            <tr>
              <th className="text-left font-semibold px-4 py-3">If your priority is…</th>
              <th className="text-left font-semibold px-4 py-3">Pick</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-900 text-zinc-300">
            <tr><td className="px-4 py-2.5">Claude Max ROI vs API rates</td><td className="px-4 py-2.5 font-semibold text-mint-400">pulse</td></tr>
            <tr><td className="px-4 py-2.5">Track multi-AI-tool spend in one place</td><td className="px-4 py-2.5 font-semibold text-mint-400">pulse</td></tr>
            <tr><td className="px-4 py-2.5">Hosted, no install, web-only</td><td className="px-4 py-2.5">ClaudeMetrics (Claude-only) or wait for pulse Pro Q3</td></tr>
            <tr><td className="px-4 py-2.5">Authoritative API-only spend</td><td className="px-4 py-2.5">Anthropic Console / OpenAI Usage</td></tr>
            <tr><td className="px-4 py-2.5">Full FinOps for cloud infra</td><td className="px-4 py-2.5">Vantage</td></tr>
            <tr><td className="px-4 py-2.5">Multi-employee SaaS approvals</td><td className="px-4 py-2.5">Pry / Cledara / Spendflo</td></tr>
            <tr><td className="px-4 py-2.5">Full personal finance + debt + budgeting</td><td className="px-4 py-2.5">YNAB or Lunch Money</td></tr>
            <tr><td className="px-4 py-2.5">Open-source local-first budgeting</td><td className="px-4 py-2.5">Actual Budget</td></tr>
            <tr><td className="px-4 py-2.5">AI subscription ROI + activity ROI</td><td className="px-4 py-2.5 font-semibold text-mint-400">pulse</td></tr>
          </tbody>
        </table>
      </div>

      <h2>Where pulse is genuinely worse</h2>
      <p>
        Three honest weaknesses to set expectations:
      </p>
      <ol>
        <li>
          <strong>Single-user today.</strong> Multi-seat Team workspaces are planned Q3 2026 but not yet shipped. If you need shared dashboards across an org today, Vantage or a custom Looker dashboard is the better call.
        </li>
        <li>
          <strong>Claude-first.</strong> Equivalent-API-value math works fully for Claude Code today; OpenAI / Cursor / Gemini / Copilot are tracked as subscription line-items until v1.1 ships their parsers in Q3 2026.
        </li>
        <li>
          <strong>No bank auto-sync.</strong> Subscriptions are entered manually (or detected from Claude logs and email patterns). Plaid integration is on the roadmap, not shipped.
        </li>
      </ol>

      <h2>Try pulse</h2>
      <p>
        Install in 5 minutes — free, MIT-licensed, no account, runs locally.
      </p>
      <p>
        <a href="/download" className="text-mint-400 hover:text-mint-300">⬇ Download for Windows</a> ·{" "}
        <a href="/demo" className="text-mint-400 hover:text-mint-300">▶ Interactive demo</a> ·{" "}
        <a href="/methodology" className="text-mint-400 hover:text-mint-300">📐 ROI methodology</a> ·{" "}
        <a href="https://github.com/walight999/pulse" target="_blank" rel="noopener noreferrer" className="text-mint-400 hover:text-mint-300">⭐ GitHub</a>
      </p>
    </LegalPage>
  );
}
