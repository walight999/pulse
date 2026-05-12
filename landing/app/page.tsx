"use client";
import Image from "next/image";
import Link from "next/link";
import { useState } from "react";

export default function Home() {
  return (
    <main className="min-h-screen bg-black text-white">
      <Header />
      <Hero />
      <Screenshots />
      <Compare />
      <Features />
      <Pricing />
      <Waitlist />
      <Footer />
    </main>
  );
}

function Header() {
  const [open, setOpen] = useState(false);
  return (
    <header className="sticky top-0 z-40 bg-black/80 backdrop-blur border-b border-zinc-900">
      <nav className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between" aria-label="Main">
        <a href="#" className="flex items-center gap-2" aria-label="pulse — home">
          <span className="logo-mark w-8 h-8 rounded-lg text-sm" aria-hidden>P</span>
          <span className="text-lg font-bold tracking-tight lowercase">pulse</span>
        </a>
        <div className="hidden md:flex items-center gap-7 text-sm text-zinc-400">
          <a href="#features" className="hover:text-white">Features</a>
          <a href="#pricing" className="hover:text-white">Pricing</a>
          <Link href="/changelog" className="hover:text-white">Changelog</Link>
          <a href="https://github.com/walight999/pulse" target="_blank" rel="noopener" className="hover:text-white">GitHub</a>
          <a href="#waitlist" className="bg-mint-500 hover:bg-mint-600 text-white font-semibold px-4 py-2 rounded-lg transition">Get early access</a>
        </div>
        <button
          type="button"
          className="md:hidden p-2 rounded-lg hover:bg-zinc-900 transition"
          aria-label={open ? "Close menu" : "Open menu"}
          aria-expanded={open}
          aria-controls="mobile-menu"
          onClick={() => setOpen((v) => !v)}
        >
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
            {open ? (
              <>
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </>
            ) : (
              <>
                <line x1="3" y1="6" x2="21" y2="6" />
                <line x1="3" y1="12" x2="21" y2="12" />
                <line x1="3" y1="18" x2="21" y2="18" />
              </>
            )}
          </svg>
        </button>
      </nav>
      {open && (
        <div id="mobile-menu" className="md:hidden border-t border-zinc-900 bg-black/95 backdrop-blur">
          <div className="max-w-6xl mx-auto px-6 py-4 flex flex-col gap-3 text-sm text-zinc-300">
            <a href="#features" onClick={() => setOpen(false)} className="py-2 hover:text-white">Features</a>
            <a href="#pricing" onClick={() => setOpen(false)} className="py-2 hover:text-white">Pricing</a>
            <Link href="/changelog" onClick={() => setOpen(false)} className="py-2 hover:text-white">Changelog</Link>
            <a href="https://github.com/walight999/pulse" target="_blank" rel="noopener" className="py-2 hover:text-white">GitHub</a>
            <a href="#waitlist" onClick={() => setOpen(false)} className="mt-2 bg-mint-500 hover:bg-mint-600 text-white text-center font-semibold px-4 py-3 rounded-lg transition">Get early access</a>
          </div>
        </div>
      )}
    </header>
  );
}

function Screenshots() {
  return (
    <section className="bg-zinc-950 border-y border-zinc-900 py-20">
      <div className="max-w-6xl mx-auto px-6">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <div className="inline-flex items-center gap-2 mb-4 px-3 py-1.5 rounded-full border border-mint-800 bg-mint-900/30 text-xs font-medium text-mint-400 uppercase tracking-wider">
            <span className="w-1.5 h-1.5 rounded-full bg-mint-400"></span>
            Built in public
          </div>
          <h2 className="text-2xl md:text-4xl font-bold mb-3">See pulse in action</h2>
          <p className="text-zinc-400 leading-relaxed">
            Subscription tracker, AI usage analytics with Plan ROI hero, and activity tracking — all in one local Streamlit dashboard.
          </p>
        </div>
        <div className="relative rounded-2xl overflow-hidden border border-zinc-900 bg-black shadow-2xl shadow-mint-900/20">
          <Image
            src="/brand/browser-mockup-clean.png"
            alt="pulse desktop dashboard — Plan ROI hero, subscription tracker, AI usage charts"
            width={1600}
            height={1000}
            priority
            sizes="(max-width: 768px) 100vw, (max-width: 1280px) 80vw, 1100px"
            className="w-full h-auto"
          />
        </div>
        <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4 text-center text-sm">
          <div className="rounded-xl border border-zinc-900 bg-black/40 px-5 py-4">
            <div className="text-mint-400 text-2xl font-extrabold tabular-nums">100%</div>
            <div className="text-zinc-400 mt-1">Local-first. No telemetry by default.</div>
          </div>
          <div className="rounded-xl border border-zinc-900 bg-black/40 px-5 py-4">
            <div className="text-mint-400 text-2xl font-extrabold tabular-nums">MIT</div>
            <div className="text-zinc-400 mt-1">Open source. Audit the code yourself.</div>
          </div>
          <div className="rounded-xl border border-zinc-900 bg-black/40 px-5 py-4">
            <div className="text-mint-400 text-2xl font-extrabold tabular-nums">$0</div>
            <div className="text-zinc-400 mt-1">Free forever for local use.</div>
          </div>
        </div>
      </div>
    </section>
  );
}

function Hero() {
  return (
    <section className="relative max-w-6xl mx-auto px-6 py-24 md:py-36 text-center overflow-hidden">
      <div className="inline-flex items-center gap-2 mb-7 px-3 py-1.5 rounded-full border border-mint-800 bg-mint-900/30 text-xs font-medium text-mint-400 uppercase tracking-wider">
        <span className="w-1.5 h-1.5 rounded-full bg-mint-400 animate-pulse"></span>
        Mint for the AI era
      </div>
      <h1 className="text-4xl md:text-7xl font-bold tracking-tight leading-[1.05] max-w-4xl mx-auto">
        Prove your <span className="text-mint-400">$200</span> Claude plan returns <span className="text-mint-400">$4,000</span> in API value.
      </h1>
      <p className="mt-7 text-lg md:text-xl text-zinc-400 max-w-2xl mx-auto leading-relaxed">
        Local-first personal-finance dashboard for the AI era. Track every recurring AI subscription, every Claude token, every hour of focused work — in one beautiful view.
      </p>
      <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
        <a href="#waitlist" className="bg-mint-500 hover:bg-mint-600 text-white font-semibold px-8 py-4 rounded-xl transition shadow-lg shadow-mint-500/20 text-base">
          Join waitlist
        </a>
        <a href="https://github.com/walight999/pulse" target="_blank" rel="noopener" className="text-zinc-300 hover:text-white font-medium px-6 py-4 transition">
          View on GitHub →
        </a>
      </div>
      <div className="mt-14 ecg-line max-w-4xl mx-auto" />
    </section>
  );
}

function Compare() {
  type Status = "available" | "pro-q3" | "roadmap";
  const rows: Array<{ label: string; status: Status; pulse: boolean; cm: boolean; ac: boolean }> = [
    { label: "Subscription + AI usage + activity in one view", status: "available", pulse: true,  cm: false, ac: false },
    { label: "Local-first, zero setup",                         status: "available", pulse: true,  cm: false, ac: false },
    { label: "Multi-currency native (30+)",                     status: "available", pulse: true,  cm: false, ac: false },
    { label: "Plan ROI vs API equivalent",                      status: "available", pulse: true,  cm: false, ac: false },
    { label: "Cancellation savings tracker",                    status: "available", pulse: true,  cm: false, ac: false },
    { label: "Per-cache TTL pricing (5m + 1h)",                 status: "available", pulse: true,  cm: false, ac: true  },
    { label: "Per-developer attribution",                       status: "pro-q3",    pulse: true,  cm: true,  ac: false },
    { label: "Friend leaderboard (opt-in)",                     status: "pro-q3",    pulse: true,  cm: false, ac: false },
    { label: "Browser extension web capture",                   status: "pro-q3",    pulse: true,  cm: false, ac: false },
    { label: "Works on Bedrock / Vertex",                       status: "roadmap",   pulse: true,  cm: true,  ac: false },
  ];

  const tag = (status: Status) => {
    if (status === "available") return <span className="inline-block text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded bg-mint-900/40 text-mint-400 border border-mint-800/50">Available</span>;
    if (status === "pro-q3")    return <span className="inline-block text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded bg-amber-900/40 text-amber-400 border border-amber-800/50">Pro · Q3</span>;
    return                              <span className="inline-block text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded bg-zinc-900 text-zinc-500 border border-zinc-800">Roadmap</span>;
  };

  return (
    <section className="bg-zinc-950 border-y border-zinc-900 py-20">
      <div className="max-w-5xl mx-auto px-6">
        <h2 className="text-2xl md:text-4xl font-bold text-center mb-3">Why pulse wins</h2>
        <p className="text-zinc-400 text-center mb-3">Other tools give you fragments. pulse gives you the picture.</p>
        <p className="text-zinc-600 text-center text-xs mb-12">Status legend: <span className="text-mint-400 font-semibold">Available</span> = shipped in v1.0 today · <span className="text-amber-400 font-semibold">Pro · Q3</span> = launches Q3 2026 · <span className="text-zinc-400 font-semibold">Roadmap</span> = planned, no ETA</p>
        <div className="overflow-x-auto rounded-xl border border-zinc-900 bg-black/30">
          <table className="w-full text-sm">
            <thead className="bg-zinc-950 border-b border-zinc-800">
              <tr>
                <th className="text-left py-4 px-3 font-semibold text-zinc-300">Feature</th>
                <th className="text-center py-4 px-3 font-semibold text-zinc-500 w-28">Status</th>
                <th className="text-center py-4 px-3 font-semibold text-mint-400">pulse</th>
                <th className="text-center py-4 px-3 font-semibold text-zinc-500">ClaudeMetrics</th>
                <th className="text-center py-4 px-3 font-semibold text-zinc-500">Anthropic Console</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-900/60">
              {rows.map((r, i) => (
                <tr key={i} className="hover:bg-zinc-950/40">
                  <td className="py-3.5 px-3 text-zinc-300">{r.label}</td>
                  <td className="text-center py-3.5 px-3">{tag(r.status)}</td>
                  <td className="text-center py-3.5 px-3">{r.pulse ? <span className="text-mint-400">●</span> : <span className="text-zinc-700">—</span>}</td>
                  <td className="text-center py-3.5 px-3">{r.cm    ? <span className="text-zinc-400">●</span> : <span className="text-zinc-700">—</span>}</td>
                  <td className="text-center py-3.5 px-3">{r.ac    ? <span className="text-zinc-400">●</span> : <span className="text-zinc-700">—</span>}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}

function Features() {
  const items = [
    {
      title: "Plan ROI hero",
      body: '"Legendary value 10×" with a five-tier gamified rating, savings number, and visual coverage bar. The moment you see your real ROI, you understand the value.',
      highlight: "10.5×",
    },
    {
      title: "Cancellation savings tracker",
      body: "Every cancelled subscription is counted. Lifetime savings since you started using pulse. The hardest financial habit, made visible.",
      highlight: "$4,300",
    },
    {
      title: "Cost-per-hour-of-use",
      body: "Link a subscription to its app. pulse shows what each hour of actual use costs — so you decide if it's worth it. No more guessing.",
      highlight: "$15/hr",
    },
    {
      title: "Streak gamification",
      body: "Consecutive days using AI. The streak chip glows once you hit 30+. Habit-building wrapped in beautiful visual feedback.",
      highlight: "47 days",
    },
    {
      title: "Multi-currency native",
      body: "30+ currencies with live ECB rates. Pay in THB, see USD reference. No more spreadsheet conversions or manual lookups.",
      highlight: "฿ → $",
    },
    {
      title: "Cache TTL pricing",
      body: "Split 5min vs 1hr Anthropic cache rates. Most tools are off by 10%+. pulse gets it right — to the cent.",
      highlight: "100%",
    },
  ];
  return (
    <section id="features" className="max-w-6xl mx-auto px-6 py-24">
      <h2 className="text-2xl md:text-4xl font-bold text-center mb-3">Six reasons people switch</h2>
      <p className="text-zinc-400 text-center mb-14 max-w-2xl mx-auto">
        Features that exist in zero other AI cost trackers.
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {items.map((it, i) => (
          <div key={i} className="bg-zinc-950 border border-zinc-900 rounded-2xl p-7 hover:border-mint-800 transition">
            <div className="text-3xl font-extrabold tracking-tight text-mint-400 mb-2 tabular-nums">
              {it.highlight}
            </div>
            <div className="text-lg font-semibold mb-2">{it.title}</div>
            <p className="text-sm text-zinc-400 leading-relaxed">{it.body}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

function Pricing() {
  const tiers: Array<{
    name: string;
    price: string;
    sub: string;
    tagline: string;
    perks: string[];
    cta: string;
    href: string;
    featured: boolean;
  }> = [
    {
      name: "Free",
      price: "$0",
      sub: "forever",
      tagline: "Local use, all features",
      perks: [
        "All v1.0 features",
        "Subscription tracker + AI usage + activity",
        "Local SQLite, no account, no telemetry",
        "Windows + macOS (Q3) + Linux (Q4)",
        "Browser extension capture",
        "Source available (MIT)",
      ],
      cta: "Download",
      href: "https://github.com/walight999/pulse/releases",
      featured: false,
    },
    {
      name: "Pro",
      price: "$9",
      sub: "/mo",
      tagline: "Cross-device sync + mobile",
      perks: [
        "Everything in Free",
        "E2E encrypted cloud sync",
        "Mobile PWA (iOS + Android)",
        "Friend leaderboard (opt-in)",
        "Multi-provider live (OpenAI, Cursor, Gemini, Copilot)",
        "Ask pulse AI assistant",
        "Cancel any time",
      ],
      cta: "Join waitlist",
      href: "#waitlist",
      featured: true,
    },
    {
      name: "Team",
      price: "$19",
      sub: "/seat/mo",
      tagline: "5-50 dev teams",
      perks: [
        "Everything in Pro",
        "Shared team dashboard",
        "Per-user attribution",
        "Slack + Teams + Discord webhooks",
        "Admin controls + audit log (1yr)",
        "Priority email support",
        "Min 3 seats",
      ],
      cta: "Contact sales",
      href: "mailto:sales@mintforai.com?subject=pulse%20Team%20inquiry",
      featured: false,
    },
    {
      name: "Enterprise",
      price: "Custom",
      sub: "",
      tagline: "50+ seats · regulated industries",
      perks: [
        "Everything in Team",
        "SSO (SAML 2.0 + OIDC)",
        "SOC 2 Type II",
        "Custom roles + audit retention (7yr)",
        "Dedicated CSM + 99.9% SLA",
        "On-prem / VPC deploy option",
        "EU/US data residency",
      ],
      cta: "Talk to us",
      href: "mailto:enterprise@mintforai.com?subject=pulse%20Enterprise%20inquiry",
      featured: false,
    },
  ];

  const matrix: Array<{ row: string; cells: [boolean | string, boolean | string, boolean | string, boolean | string] }> = [
    { row: "Local desktop app", cells: ["✓", "✓", "✓", "✓"] },
    { row: "Subscription tracker", cells: ["✓", "✓", "✓", "✓"] },
    { row: "AI usage + Plan ROI", cells: ["✓", "✓", "✓", "✓"] },
    { row: "Activity + categories", cells: ["✓", "✓", "✓", "✓"] },
    { row: "Browser extension", cells: ["✓", "✓", "✓", "✓"] },
    { row: "Multi-currency (30+)", cells: ["✓", "✓", "✓", "✓"] },
    { row: "Cloud sync (E2E encrypted)", cells: [false, "✓", "✓", "✓"] },
    { row: "Mobile PWA", cells: [false, "✓", "✓", "✓"] },
    { row: "Multi-provider live", cells: [false, "✓", "✓", "✓"] },
    { row: "Friend leaderboard", cells: [false, "✓", "✓", "✓"] },
    { row: "Ask pulse AI", cells: [false, "✓", "✓", "✓"] },
    { row: "Devices per account", cells: ["1", "3", "Unlimited", "Unlimited"] },
    { row: "Team dashboard + roles", cells: [false, false, "✓", "✓"] },
    { row: "Slack/Teams/Discord", cells: [false, false, "✓", "✓"] },
    { row: "Per-user attribution", cells: [false, false, "✓", "✓"] },
    { row: "Audit log retention", cells: ["30d local", "90d", "1yr", "7yr"] },
    { row: "Admin controls", cells: [false, false, "Standard", "Custom roles"] },
    { row: "SSO (SAML / OIDC)", cells: [false, false, false, "✓"] },
    { row: "SOC 2 Type II", cells: [false, false, false, "✓"] },
    { row: "Custom data residency", cells: [false, false, false, "✓"] },
    { row: "Dedicated CSM + SLA", cells: [false, false, "Email", "99.9% SLA"] },
  ];

  const faqs: Array<[string, string]> = [
    [
      "Is Free really free forever?",
      "Yes. The local desktop app is MIT-licensed open source. We commit to never paywalling features that already exist in v1.0. Revenue comes from cloud sync, team dashboards, and enterprise services — not from selling binaries.",
    ],
    [
      "Why do you charge for Pro if everything is open-source?",
      "You're paying for the cloud infrastructure (encrypted sync server, mobile PWA hosting, friend leaderboard ranking, AI assistant API). You can self-host the cloud server from the same repo for free.",
    ],
    [
      "Can I cancel any time?",
      "Yes. Pro is month-to-month. Team has a 14-day money-back guarantee. Enterprise contracts are annual with 30-day exit clauses. If you cancel, your local data stays — you only lose cloud sync.",
    ],
    [
      "Do you offer student / open-source maintainer discounts?",
      "Yes — 50% off Pro for verified students (.edu) and open-source maintainers with 100+ stars. Email hi@mintforai.com.",
    ],
    [
      "Is there a Team annual discount?",
      "Yes. Team = $19/seat/mo or $190/seat/yr (2 months free). Min 3 seats either way.",
    ],
    [
      "How does data residency work for Enterprise?",
      "We offer EU (Frankfurt) + US (Virginia) + on-prem deployment via Helm chart. The data never crosses regions unless you opt in.",
    ],
    [
      "What's your refund policy?",
      "Pro: cancel anytime, no questions. Team: 14-day money-back. Enterprise: pro-rated refund for unused term if you cancel within first 60 days.",
    ],
    [
      "When does Pro launch?",
      "Q3 2026. Waitlist signups get 1 month free + early access to friend leaderboard invite codes.",
    ],
    [
      "Is there a lifetime deal?",
      "Yes — Lifetime Pro $199 (one-time) for the first 500 customers. After that, the deal closes permanently and Pro reverts to monthly/annual only. Lifetime includes every future Pro feature: cloud sync, mobile PWA, multi-provider live, friend leaderboard, Ask pulse AI, and anything we ship under Pro through pulse v9.x.",
    ],
    [
      "What's the difference between pulse and ClaudeMetrics?",
      "ClaudeMetrics requires manual export upload and is Claude-only. pulse runs locally, parses ~/.claude/projects/*.jsonl directly with no upload step, and combines AI usage with subscription tracking + activity tracking in one dashboard. Both are valid tools — pulse is for the developer who wants the full picture in real time.",
    ],
    [
      "Does pulse work without internet?",
      "Yes. The local app needs internet only twice: (1) on first run to fetch FX rates from frankfurter.dev, cached for 24h, and (2) optionally to check for updates. Subscription tracking + AI usage parsing + activity tracking all work fully offline.",
    ],
    [
      "Will pulse phone home? Track me? Sell my data?",
      "No, no, and no. Local mode has zero outbound calls except the FX rate fetch. Telemetry is opt-in and defaults to OFF. Cloud features (Pro+) are opt-in per metric, and synced data is end-to-end encrypted (AES-256-GCM + Argon2id) — the server cannot read your data even if compromised. We're MIT-licensed; audit the source.",
    ],
    [
      "What platforms does pulse support?",
      "Today: Windows 10 + 11 (system tray app via pystray + Win32 APIs). Q3 2026: native macOS (Apple Silicon + Intel universal2 build). Q4 2026: Linux (AppImage). The cross-platform shim (platform_compat.py) is already in the repo — macOS and Linux work from source today, just unsigned.",
    ],
    [
      "Can I self-host the cloud server?",
      "Yes. The cloud server (cloud/auth.py, cloud/sync.py, api/server.py) is MIT-licensed and ships in the same repo. Bring your own Supabase project, set SUPABASE_URL + SUPABASE_ANON_KEY, deploy. No paywall, no rate limit. We charge for hosting + maintenance, not for the right to use the software.",
    ],
    [
      "What AI providers does pulse track?",
      "v1.0 (today): Claude Code via local ~/.claude/projects/*.jsonl parser. v1.1 (Q3 2026): OpenAI (ChatGPT + API), Cursor (local state DB), Google Gemini (Studio + app), GitHub Copilot (flat + audit log). Browser extension (v1.2) captures web sessions for ChatGPT, Claude.ai, Gemini, Perplexity.",
    ],
  ];

  return (
    <section id="pricing" className="bg-zinc-950 border-y border-zinc-900 py-24">
      <div className="max-w-6xl mx-auto px-6">
        <h2 className="text-2xl md:text-4xl font-bold text-center mb-3">Pricing</h2>
        <p className="text-zinc-400 text-center mb-14">Free forever for local use. Pay only when you go cloud.</p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          {tiers.map((t, i) => (
            <div
              key={i}
              className={`rounded-2xl p-7 transition flex flex-col ${
                t.featured
                  ? "bg-mint-900/20 border-2 border-mint-500 shadow-lg shadow-mint-500/10 scale-[1.02]"
                  : "bg-black border border-zinc-900"
              }`}
            >
              {t.featured && (
                <div className="text-xs font-bold tracking-wider text-mint-400 uppercase mb-3">Most popular</div>
              )}
              <div className="text-lg font-bold mb-1">{t.name}</div>
              <div className="text-zinc-500 text-sm mb-5">{t.tagline}</div>
              <div className="flex items-baseline mb-5">
                <span className="text-4xl font-bold">{t.price}</span>
                <span className="text-zinc-500 ml-1 text-sm">{t.sub}</span>
              </div>
              <ul className="space-y-2 mb-7 text-sm text-zinc-300 flex-1">
                {t.perks.map((p, j) => (
                  <li key={j} className="flex items-start gap-2">
                    <span className="text-mint-400 mt-0.5 flex-shrink-0">●</span> <span>{p}</span>
                  </li>
                ))}
              </ul>
              <a
                href={t.href}
                target={t.href.startsWith("http") ? "_blank" : undefined}
                rel={t.href.startsWith("http") ? "noopener" : undefined}
                className={`block text-center font-semibold py-3 rounded-lg transition ${
                  t.featured
                    ? "bg-mint-500 hover:bg-mint-600 text-white"
                    : "border border-zinc-800 hover:border-zinc-700 text-zinc-200"
                }`}
              >
                {t.cta}
              </a>
            </div>
          ))}
        </div>

        <div className="mt-12 rounded-2xl border-2 border-amber-500/40 bg-gradient-to-br from-amber-950/30 via-black to-mint-950/20 p-6 md:p-8">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-5">
            <div className="flex-1">
              <div className="inline-flex items-center gap-2 mb-2 px-2.5 py-1 rounded-full bg-amber-500/20 border border-amber-500/40 text-amber-400 text-[10px] font-bold uppercase tracking-wider">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse" aria-hidden></span>
                Early-adopter unlock · first 500 only
              </div>
              <h3 className="text-2xl md:text-3xl font-bold tracking-tight">
                Lifetime Pro for <span className="text-amber-400 tabular-nums">$199</span>
              </h3>
              <p className="mt-2 text-zinc-400 text-sm max-w-xl leading-relaxed">
                One-time payment. Pulse Pro forever — cloud sync, mobile PWA, multi-provider live, friend leaderboard, Ask pulse AI, and every future Pro feature through v9.x. After 500 buyers, this deal closes permanently.
              </p>
            </div>
            <a
              href="#waitlist"
              className="flex-shrink-0 bg-amber-500 hover:bg-amber-400 text-black font-bold px-7 py-3.5 rounded-xl transition shadow-lg shadow-amber-500/30 text-sm whitespace-nowrap"
            >
              Reserve a lifetime seat →
            </a>
          </div>
        </div>

        <div className="mt-10 flex flex-col md:flex-row items-center justify-center gap-x-8 gap-y-3 text-center text-sm text-zinc-500">
          <div>🎓 <span className="text-zinc-300">50% off Pro</span> for verified students (.edu) and OSS maintainers with 100+ stars</div>
        </div>

        <div className="mt-12 text-center text-zinc-500 text-sm">
          All plans include: MIT-licensed local app · 30+ currencies · privacy-by-default · open audit trail · cancel any time
        </div>

        <div className="mt-20">
          <h3 className="text-xl md:text-2xl font-bold text-center mb-3">Compare every feature</h3>
          <p className="text-zinc-500 text-center text-sm mb-10">Honest comparison, no hidden gotchas.</p>
          <div className="overflow-x-auto rounded-xl border border-zinc-900 bg-black/40">
            <table className="w-full text-sm">
              <thead className="bg-zinc-950 border-b border-zinc-900">
                <tr>
                  <th className="text-left font-semibold text-zinc-300 px-4 py-3">Feature</th>
                  <th className="font-semibold text-zinc-400 px-4 py-3">Free</th>
                  <th className="font-semibold text-mint-400 px-4 py-3">Pro</th>
                  <th className="font-semibold text-zinc-300 px-4 py-3">Team</th>
                  <th className="font-semibold text-zinc-300 px-4 py-3">Enterprise</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-900">
                {matrix.map((m, i) => (
                  <tr key={i} className="hover:bg-zinc-950/40">
                    <td className="text-left text-zinc-300 px-4 py-2.5">{m.row}</td>
                    {m.cells.map((c, j) => (
                      <td key={j} className="text-center px-4 py-2.5">
                        {c === false ? (
                          <span className="text-zinc-700">—</span>
                        ) : c === "✓" ? (
                          <span className="text-mint-400 font-bold">✓</span>
                        ) : (
                          <span className="text-zinc-400 text-xs">{c}</span>
                        )}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="mt-20 max-w-3xl mx-auto">
          <h3 className="text-xl md:text-2xl font-bold text-center mb-10">Frequently asked questions</h3>
          <div className="space-y-3">
            {faqs.map(([q, a], i) => (
              <details key={i} className="group rounded-xl border border-zinc-900 bg-black/40 open:bg-zinc-950/60 transition">
                <summary className="cursor-pointer px-5 py-4 text-zinc-200 font-medium flex items-center justify-between hover:text-white transition">
                  <span>{q}</span>
                  <span className="text-zinc-600 group-open:text-mint-400 transition text-lg">+</span>
                </summary>
                <div className="px-5 pb-4 pt-1 text-zinc-400 text-sm leading-relaxed">{a}</div>
              </details>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function Waitlist() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "ok" | "err">("idle");

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setStatus("loading");
    try {
      const r = await fetch("/api/waitlist", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      setStatus(r.ok ? "ok" : "err");
    } catch {
      setStatus("err");
    }
  }

  return (
    <section id="waitlist" className="max-w-3xl mx-auto px-6 py-24 text-center">
      <h2 className="text-2xl md:text-4xl font-bold mb-3">Get early access</h2>
      <p className="text-zinc-400 mb-10 max-w-xl mx-auto">
        Pulse Pro launches Q3 2026. Sign up now and get 1 month free + first dibs on friend
        leaderboard invite codes.
      </p>
      {status === "ok" ? (
        <div className="bg-mint-900/30 border border-mint-700 rounded-xl p-6 text-mint-400">
          You're on the list. We'll email when pulse Pro launches.
        </div>
      ) : (
        <form onSubmit={submit} className="flex flex-col sm:flex-row gap-3 max-w-md mx-auto">
          <input
            type="email"
            required
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="flex-1 bg-zinc-950 border border-zinc-800 rounded-lg px-4 py-3 text-white placeholder-zinc-500 focus:border-mint-500 focus:outline-none transition"
          />
          <button
            type="submit"
            disabled={status === "loading"}
            className="bg-mint-500 hover:bg-mint-600 text-white font-semibold px-6 py-3 rounded-lg transition disabled:opacity-50"
          >
            {status === "loading" ? "Joining..." : "Join waitlist"}
          </button>
        </form>
      )}
      <div className="text-xs text-zinc-600 mt-4">
        No spam. One email when Pro launches. Unsubscribe anytime.
      </div>
    </section>
  );
}

function Footer() {
  return (
    <footer className="border-t border-zinc-900 pt-16 pb-10">
      <div className="max-w-6xl mx-auto px-6">
        <div className="grid grid-cols-2 md:grid-cols-5 gap-10 mb-12">
          <div className="col-span-2">
            <div className="flex items-center gap-2 mb-3">
              <span className="logo-mark w-8 h-8 rounded-lg text-sm" aria-hidden>P</span>
              <span className="text-lg font-bold tracking-tight lowercase">pulse</span>
            </div>
            <p className="text-zinc-500 text-sm leading-relaxed max-w-xs">
              Mint for the AI era. Local-first personal-finance dashboard for AI subscriptions, Claude tokens, and focused work.
            </p>
            <div className="mt-5 flex items-center gap-4">
              <a href="https://github.com/walight999/pulse" target="_blank" rel="noopener" aria-label="GitHub" className="text-zinc-600 hover:text-white transition">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden>
                  <path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0 1 12 6.844a9.59 9.59 0 0 1 2.504.337c1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.847-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.02 10.02 0 0 0 22 12.017C22 6.484 17.522 2 12 2z" />
                </svg>
              </a>
              <a href="https://twitter.com/mintforai" target="_blank" rel="noopener" aria-label="Twitter" className="text-zinc-600 hover:text-white transition">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden>
                  <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
                </svg>
              </a>
            </div>
          </div>
          <div>
            <div className="text-xs uppercase tracking-wider text-zinc-500 font-bold mb-4">Product</div>
            <ul className="space-y-3 text-sm">
              <li><a href="#features" className="text-zinc-400 hover:text-white">Features</a></li>
              <li><a href="#pricing" className="text-zinc-400 hover:text-white">Pricing</a></li>
              <li><a href="https://github.com/walight999/pulse/releases" target="_blank" rel="noopener" className="text-zinc-400 hover:text-white">Download</a></li>
              <li><Link href="/changelog" className="text-zinc-400 hover:text-white">Changelog</Link></li>
              <li><a href="#waitlist" className="text-zinc-400 hover:text-white">Pro waitlist</a></li>
            </ul>
          </div>
          <div>
            <div className="text-xs uppercase tracking-wider text-zinc-500 font-bold mb-4">Community</div>
            <ul className="space-y-3 text-sm">
              <li><a href="https://github.com/walight999/pulse" target="_blank" rel="noopener" className="text-zinc-400 hover:text-white">GitHub</a></li>
              <li><a href="https://github.com/walight999/pulse/discussions" target="_blank" rel="noopener" className="text-zinc-400 hover:text-white">Discussions</a></li>
              <li><a href="https://github.com/walight999/pulse/issues" target="_blank" rel="noopener" className="text-zinc-400 hover:text-white">Issues</a></li>
              <li><a href="https://twitter.com/mintforai" target="_blank" rel="noopener" className="text-zinc-400 hover:text-white">Twitter</a></li>
            </ul>
          </div>
          <div>
            <div className="text-xs uppercase tracking-wider text-zinc-500 font-bold mb-4">Legal</div>
            <ul className="space-y-3 text-sm">
              <li><Link href="/privacy" className="text-zinc-400 hover:text-white">Privacy</Link></li>
              <li><Link href="/terms" className="text-zinc-400 hover:text-white">Terms</Link></li>
              <li><Link href="/security" className="text-zinc-400 hover:text-white">Security</Link></li>
              <li><a href="mailto:security@mintforai.com" className="text-zinc-400 hover:text-white">Report vuln</a></li>
              <li><a href="mailto:hi@mintforai.com" className="text-zinc-400 hover:text-white">Contact</a></li>
            </ul>
          </div>
        </div>
        <div className="border-t border-zinc-900 pt-8 flex flex-col md:flex-row items-center justify-between gap-3 text-xs text-zinc-600">
          <div>© 2026 White · Built in Bangkok · MIT licensed</div>
          <div className="flex items-center gap-2">
            <span className="w-1.5 h-1.5 rounded-full bg-mint-400 animate-pulse" aria-hidden></span>
            <span>v1.5 · all systems operational</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
