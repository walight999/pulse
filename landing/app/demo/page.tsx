"use client";

import Link from "next/link";
import { useMemo, useState } from "react";

// --------------------------------------------------------------
// /demo — interactive product preview with persona-toggleable
// fake data. All numbers are computed live from the inputs below,
// so the math itself is real (same formulas as /methodology).
// Only the seed data is synthetic.
// --------------------------------------------------------------

type Persona = "solo" | "developer" | "founder";

type Sub = {
  name: string;
  vendor: string;
  monthlyUsd: number;
  cancelled?: boolean;
  monthsSinceCancel?: number;
  linkedAppHours?: number;
};

type TokenUsage = {
  model: "Opus" | "Sonnet" | "Haiku";
  inputTokens: number;
  outputTokens: number;
  cacheWrite5mTokens: number;
  cacheWrite1hTokens: number;
  cacheReadTokens: number;
};

// Prices from sync_tokens.py (USD per million tokens)
const PRICING: Record<TokenUsage["model"], { input: number; output: number; cw5m: number; cw1h: number; cr: number }> = {
  Opus:   { input: 15.0, output: 75.0, cw5m: 18.75, cw1h: 30.0, cr: 1.50 },
  Sonnet: { input: 3.0,  output: 15.0, cw5m: 3.75,  cw1h: 6.0,  cr: 0.30 },
  Haiku:  { input: 0.80, output: 4.0,  cw5m: 1.00,  cw1h: 1.6,  cr: 0.08 },
};

function apiValue(u: TokenUsage): number {
  const p = PRICING[u.model];
  return (
    (u.inputTokens         * p.input  +
     u.outputTokens        * p.output +
     u.cacheWrite5mTokens  * p.cw5m   +
     u.cacheWrite1hTokens  * p.cw1h   +
     u.cacheReadTokens     * p.cr) / 1_000_000
  );
}

const PERSONAS: Record<Persona, { label: string; sub: string; subs: Sub[]; tokens: TokenUsage[] }> = {
  solo: {
    label: "Solo AI user",
    sub: "Claude Max + ChatGPT Plus + Cursor",
    subs: [
      { name: "Claude Max",    vendor: "Anthropic", monthlyUsd: 200, linkedAppHours: 38 },
      { name: "ChatGPT Plus",  vendor: "OpenAI",    monthlyUsd: 20,  linkedAppHours: 8 },
      { name: "Cursor Pro",    vendor: "Cursor",    monthlyUsd: 20,  linkedAppHours: 24 },
      { name: "Suno (cancelled)", vendor: "Suno", monthlyUsd: 10, cancelled: true, monthsSinceCancel: 4 },
    ],
    tokens: [
      { model: "Opus",   inputTokens:  6_200_000, outputTokens:  1_900_000, cacheWrite5mTokens: 2_400_000, cacheWrite1hTokens:   180_000, cacheReadTokens: 12_000_000 },
      { model: "Sonnet", inputTokens: 14_000_000, outputTokens:  4_100_000, cacheWrite5mTokens: 5_100_000, cacheWrite1hTokens:   320_000, cacheReadTokens: 28_000_000 },
    ],
  },
  developer: {
    label: "Developer",
    sub: "Heavy Claude Code user, multiple AI tools",
    subs: [
      { name: "Claude Max",        vendor: "Anthropic",  monthlyUsd: 200, linkedAppHours: 92 },
      { name: "GitHub Copilot",    vendor: "GitHub",     monthlyUsd: 10,  linkedAppHours: 48 },
      { name: "Cursor Pro",        vendor: "Cursor",     monthlyUsd: 20,  linkedAppHours: 60 },
      { name: "ChatGPT Plus",      vendor: "OpenAI",     monthlyUsd: 20,  linkedAppHours: 4 },
      { name: "Perplexity (cancelled)", vendor: "Perplexity", monthlyUsd: 20, cancelled: true, monthsSinceCancel: 6 },
      { name: "Replit Core (cancelled)", vendor: "Replit", monthlyUsd: 25, cancelled: true, monthsSinceCancel: 9 },
    ],
    tokens: [
      { model: "Opus",   inputTokens: 22_000_000, outputTokens:  6_400_000, cacheWrite5mTokens:  9_100_000, cacheWrite1hTokens:   620_000, cacheReadTokens:  48_000_000 },
      { model: "Sonnet", inputTokens: 48_000_000, outputTokens: 14_200_000, cacheWrite5mTokens: 18_000_000, cacheWrite1hTokens: 1_100_000, cacheReadTokens: 102_000_000 },
      { model: "Haiku",  inputTokens:  8_400_000, outputTokens:  1_800_000, cacheWrite5mTokens:  2_900_000, cacheWrite1hTokens:    80_000, cacheReadTokens:  16_000_000 },
    ],
  },
  founder: {
    label: "Founder / operator",
    sub: "AI SaaS spend for the whole stack",
    subs: [
      { name: "Claude Max",      vendor: "Anthropic",   monthlyUsd: 200, linkedAppHours: 54 },
      { name: "ChatGPT Plus",    vendor: "OpenAI",      monthlyUsd: 20,  linkedAppHours: 22 },
      { name: "Cursor Pro",      vendor: "Cursor",      monthlyUsd: 20,  linkedAppHours: 12 },
      { name: "GitHub Copilot",  vendor: "GitHub",      monthlyUsd: 10,  linkedAppHours: 16 },
      { name: "Linear",          vendor: "Linear",      monthlyUsd: 8,   linkedAppHours: 14 },
      { name: "Notion AI",       vendor: "Notion",      monthlyUsd: 10,  linkedAppHours: 6 },
      { name: "Granola",         vendor: "Granola",     monthlyUsd: 14,  linkedAppHours: 3 },
      { name: "Suno (cancelled)", vendor: "Suno", monthlyUsd: 10, cancelled: true, monthsSinceCancel: 3 },
      { name: "Midjourney (cancelled)", vendor: "Midjourney", monthlyUsd: 30, cancelled: true, monthsSinceCancel: 7 },
    ],
    tokens: [
      { model: "Opus",   inputTokens: 12_400_000, outputTokens:  3_600_000, cacheWrite5mTokens:  4_800_000, cacheWrite1hTokens:   400_000, cacheReadTokens: 22_000_000 },
      { model: "Sonnet", inputTokens: 26_000_000, outputTokens:  7_900_000, cacheWrite5mTokens: 10_200_000, cacheWrite1hTokens:   780_000, cacheReadTokens: 56_000_000 },
    ],
  },
};

function fmtUsd(n: number, places = 0): string {
  return n.toLocaleString("en-US", { style: "currency", currency: "USD", maximumFractionDigits: places, minimumFractionDigits: places });
}

function fmtNum(n: number): string {
  return Math.round(n).toLocaleString("en-US");
}

export default function DemoPage() {
  const [persona, setPersona] = useState<Persona>("solo");
  const data = PERSONAS[persona];

  const computed = useMemo(() => {
    const activeSubs = data.subs.filter((s) => !s.cancelled);
    const monthlyAiSpend = activeSubs.reduce((a, s) => a + s.monthlyUsd, 0);
    const claudeMax = activeSubs.find((s) => s.name === "Claude Max");
    const equivalentApiValue = data.tokens.reduce((a, u) => a + apiValue(u), 0);
    const planRoi = claudeMax ? equivalentApiValue / claudeMax.monthlyUsd : 0;

    const totalForegroundHours = activeSubs.reduce((a, s) => a + (s.linkedAppHours || 0), 0);
    const subsWithHours = activeSubs.filter((s) => (s.linkedAppHours || 0) > 0);
    const subCostPerHour = subsWithHours.map((s) => ({
      name: s.name,
      hours: s.linkedAppHours || 0,
      perHour: (s.linkedAppHours || 0) > 0 ? s.monthlyUsd / (s.linkedAppHours || 1) : 0,
    }));

    const cancellationSavings = data.subs
      .filter((s) => s.cancelled)
      .reduce((a, s) => a + s.monthlyUsd * (s.monthsSinceCancel || 0), 0);

    return { activeSubs, monthlyAiSpend, equivalentApiValue, planRoi, totalForegroundHours, subCostPerHour, cancellationSavings };
  }, [data]);

  const roiTier = computed.planRoi >= 10 ? "Legendary value 10×+" : computed.planRoi >= 5 ? "Great value" : computed.planRoi >= 2 ? "Solid value" : computed.planRoi >= 1 ? "Breaks even" : "Idle";

  return (
    <main className="min-h-screen bg-black text-white">
      <header className="sticky top-0 z-40 bg-black/80 backdrop-blur border-b border-zinc-900">
        <nav className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between" aria-label="Main">
          <Link href="/" className="flex items-center gap-2" aria-label="pulse — home">
            <span className="logo-mark w-8 h-8 rounded-lg text-sm" aria-hidden>P</span>
            <span className="text-lg font-bold tracking-tight lowercase">pulse</span>
          </Link>
          <Link href="/" className="text-sm text-zinc-400 hover:text-white transition">← Back to home</Link>
        </nav>
      </header>

      <section className="max-w-6xl mx-auto px-6 py-12 md:py-16">
        <div className="inline-flex items-center gap-2 mb-4 px-3 py-1.5 rounded-full border border-amber-700 bg-amber-900/30 text-xs font-medium text-amber-300 uppercase tracking-wider">
          <span className="w-1.5 h-1.5 rounded-full bg-amber-300" aria-hidden></span>
          Demo data only · your real data stays local
        </div>
        <h1 className="text-3xl md:text-5xl font-bold tracking-tight leading-tight">See pulse in 30 seconds</h1>
        <p className="mt-4 text-zinc-400 text-lg leading-relaxed max-w-2xl">
          Pick a persona — pulse computes Plan ROI, monthly spend, cost per hour, and cancellation savings live
          using the same formulas as the real app. The math is real; only the input data below is synthetic.
        </p>

        <div className="mt-8 inline-flex p-1 rounded-xl bg-zinc-950 border border-zinc-900" role="tablist" aria-label="Persona">
          {(["solo", "developer", "founder"] as Persona[]).map((p) => (
            <button
              key={p}
              role="tab"
              aria-selected={persona === p}
              onClick={() => setPersona(p)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                persona === p ? "bg-mint-500 text-white" : "text-zinc-400 hover:text-white"
              }`}
            >
              {PERSONAS[p].label}
            </button>
          ))}
        </div>

        <p className="mt-3 text-xs text-zinc-500">
          Currently showing: <span className="text-zinc-300 font-medium">{data.label}</span> · {data.sub}
        </p>

        {/* ────── headline metric tiles ────── */}
        <div className="mt-10 grid grid-cols-2 lg:grid-cols-4 gap-4">
          <Metric
            label="Plan ROI"
            value={`${computed.planRoi.toFixed(1)}×`}
            sub={roiTier}
            tone="mint"
          />
          <Metric
            label="Equivalent API value (mo)"
            value={fmtUsd(computed.equivalentApiValue)}
            sub={`for ${fmtUsd(200)} Claude Max`}
            tone="mint"
          />
          <Metric
            label="Monthly AI spend"
            value={fmtUsd(computed.monthlyAiSpend)}
            sub={`${computed.activeSubs.length} active subs`}
            tone="neutral"
          />
          <Metric
            label="Cancellation savings (cumulative)"
            value={fmtUsd(computed.cancellationSavings)}
            sub={`${data.subs.filter((s) => s.cancelled).length} subs cancelled`}
            tone="neutral"
          />
        </div>

        {/* ────── subscriptions table ────── */}
        <div className="mt-12">
          <h2 className="text-xl md:text-2xl font-bold tracking-tight mb-4">Subscriptions</h2>
          <div className="overflow-x-auto rounded-xl border border-zinc-900 bg-black/40">
            <table className="w-full text-sm">
              <thead className="bg-zinc-950 border-b border-zinc-900 text-zinc-400">
                <tr>
                  <th className="text-left font-semibold px-4 py-3">Subscription</th>
                  <th className="text-left font-semibold px-4 py-3">Vendor</th>
                  <th className="text-right font-semibold px-4 py-3">Monthly</th>
                  <th className="text-right font-semibold px-4 py-3">Foreground hrs</th>
                  <th className="text-right font-semibold px-4 py-3">Cost / active hr</th>
                  <th className="text-center font-semibold px-4 py-3 w-24">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-900 text-zinc-300">
                {data.subs.map((s, i) => (
                  <tr key={i} className={s.cancelled ? "opacity-60" : ""}>
                    <td className="px-4 py-2.5 font-medium text-zinc-100">{s.name}</td>
                    <td className="px-4 py-2.5 text-xs text-zinc-500">{s.vendor}</td>
                    <td className="px-4 py-2.5 text-right tabular-nums">{fmtUsd(s.monthlyUsd)}</td>
                    <td className="px-4 py-2.5 text-right tabular-nums">{s.cancelled ? "—" : `${s.linkedAppHours || 0} hr`}</td>
                    <td className="px-4 py-2.5 text-right tabular-nums">
                      {s.cancelled || !s.linkedAppHours ? "—" : fmtUsd(s.monthlyUsd / s.linkedAppHours, 2)}
                    </td>
                    <td className="px-4 py-2.5 text-center">
                      {s.cancelled ? (
                        <span className="inline-block text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-zinc-900 text-zinc-500 border border-zinc-800">Cancelled</span>
                      ) : (
                        <span className="inline-block text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-mint-900/40 text-mint-400 border border-mint-800/50">Active</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* ────── token usage breakdown ────── */}
        <div className="mt-12">
          <h2 className="text-xl md:text-2xl font-bold tracking-tight mb-4">Claude token usage (this month)</h2>
          <p className="text-sm text-zinc-500 mb-4">
            Token counts parsed from <code className="text-zinc-300">~/.claude/projects/*.jsonl</code>. Prices are
            Anthropic's published rates from <a href="/methodology" className="text-mint-400 hover:text-mint-300">sync_tokens.py</a>.
          </p>
          <div className="overflow-x-auto rounded-xl border border-zinc-900 bg-black/40">
            <table className="w-full text-sm">
              <thead className="bg-zinc-950 border-b border-zinc-900 text-zinc-400">
                <tr>
                  <th className="text-left font-semibold px-4 py-3">Model</th>
                  <th className="text-right font-semibold px-4 py-3">Input</th>
                  <th className="text-right font-semibold px-4 py-3">Output</th>
                  <th className="text-right font-semibold px-4 py-3">Cache write (5m)</th>
                  <th className="text-right font-semibold px-4 py-3">Cache write (1h)</th>
                  <th className="text-right font-semibold px-4 py-3">Cache read</th>
                  <th className="text-right font-semibold px-4 py-3">API equivalent</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-900 text-zinc-300">
                {data.tokens.map((u, i) => (
                  <tr key={i}>
                    <td className="px-4 py-2.5 font-medium text-zinc-100">Claude {u.model}</td>
                    <td className="px-4 py-2.5 text-right tabular-nums text-xs">{fmtNum(u.inputTokens)}</td>
                    <td className="px-4 py-2.5 text-right tabular-nums text-xs">{fmtNum(u.outputTokens)}</td>
                    <td className="px-4 py-2.5 text-right tabular-nums text-xs">{fmtNum(u.cacheWrite5mTokens)}</td>
                    <td className="px-4 py-2.5 text-right tabular-nums text-xs">{fmtNum(u.cacheWrite1hTokens)}</td>
                    <td className="px-4 py-2.5 text-right tabular-nums text-xs">{fmtNum(u.cacheReadTokens)}</td>
                    <td className="px-4 py-2.5 text-right tabular-nums font-semibold text-mint-400">{fmtUsd(apiValue(u))}</td>
                  </tr>
                ))}
                <tr className="bg-zinc-950/40 font-semibold">
                  <td className="px-4 py-2.5 text-zinc-100" colSpan={6}>Total equivalent API value</td>
                  <td className="px-4 py-2.5 text-right tabular-nums text-mint-400">{fmtUsd(computed.equivalentApiValue)}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* ────── ROI explainer + sample CSV ────── */}
        <div className="mt-12 grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="rounded-2xl border border-mint-800/60 bg-mint-950/20 p-6">
            <h3 className="text-lg font-bold mb-2 text-mint-300">How Plan ROI is computed</h3>
            <pre className="text-xs text-zinc-300 mb-3 overflow-x-auto">
{`Plan ROI = Equivalent API Value ÷ Subscription Cost
         = ${fmtUsd(computed.equivalentApiValue)} ÷ ${fmtUsd(200)}
         = ${computed.planRoi.toFixed(1)}×`}
            </pre>
            <p className="text-xs text-zinc-400">
              Full formula breakdown including cache TTL pricing on{" "}
              <Link href="/methodology" className="text-mint-400 hover:text-mint-300">/methodology</Link>.
            </p>
          </div>
          <div className="rounded-2xl border border-zinc-900 bg-zinc-950/40 p-6">
            <h3 className="text-lg font-bold mb-2 text-zinc-100">Try the real export format</h3>
            <p className="text-sm text-zinc-400 mb-4">
              This is what pulse generates when you click <em>Settings → Data → Export CSV</em> — same columns, same
              structure, populated with the demo data above.
            </p>
            <a
              href="/samples/pulse-sample-export.csv"
              download
              className="inline-flex items-center gap-2 bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 text-zinc-100 font-medium px-4 py-2.5 rounded-lg transition text-sm"
            >
              ⬇ Download sample CSV (3 KB)
            </a>
          </div>
        </div>

        {/* ────── CTA strip ────── */}
        <div className="mt-14 rounded-2xl border border-mint-800/60 bg-gradient-to-br from-mint-950/30 via-black to-zinc-950/30 p-6 md:p-8">
          <h2 className="text-xl md:text-2xl font-bold mb-2">Ready to see your real numbers?</h2>
          <p className="text-zinc-400 text-sm mb-5 max-w-2xl">
            Pulse is free, MIT-licensed, and runs locally. Install in 5 minutes — it auto-detects your Claude Code
            logs and shows you a real Plan ROI within the first session.
          </p>
          <div className="flex flex-wrap gap-3">
            <Link
              href="/download"
              className="bg-mint-500 hover:bg-mint-600 text-white font-semibold px-6 py-3 rounded-lg transition text-sm"
            >
              Download pulse →
            </Link>
            <Link
              href="/methodology"
              className="border border-zinc-800 hover:border-zinc-700 text-zinc-200 font-medium px-6 py-3 rounded-lg transition text-sm"
            >
              How the math works →
            </Link>
            <Link
              href="/#waitlist"
              className="border border-zinc-800 hover:border-zinc-700 text-zinc-200 font-medium px-6 py-3 rounded-lg transition text-sm"
            >
              Join Pro waitlist →
            </Link>
          </div>
        </div>
      </section>

      <footer className="border-t border-zinc-900 py-10">
        <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-3 text-xs text-zinc-600">
          <div>© 2026 pulse · operated by White, Bangkok, Thailand · demo numbers are synthetic</div>
          <div className="flex items-center gap-5">
            <Link href="/download" className="hover:text-white">Download</Link>
            <Link href="/methodology" className="hover:text-white">Methodology</Link>
            <Link href="/docs" className="hover:text-white">Docs</Link>
            <Link href="/security" className="hover:text-white">Security</Link>
          </div>
        </div>
      </footer>
    </main>
  );
}

function Metric({ label, value, sub, tone }: { label: string; value: string; sub: string; tone: "mint" | "neutral" }) {
  return (
    <div className={`rounded-2xl p-5 border ${tone === "mint" ? "border-mint-800/60 bg-mint-950/20" : "border-zinc-900 bg-zinc-950/40"}`}>
      <div className="text-[10px] uppercase tracking-wider font-bold text-zinc-500 mb-2">{label}</div>
      <div className={`text-3xl md:text-4xl font-extrabold tabular-nums ${tone === "mint" ? "text-mint-400" : "text-zinc-100"}`}>
        {value}
      </div>
      <div className="text-xs text-zinc-500 mt-1.5">{sub}</div>
    </div>
  );
}
