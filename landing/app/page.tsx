"use client";
import Image from "next/image";
import { useState } from "react";

export default function Home() {
  return (
    <main className="min-h-screen bg-black text-white">
      <Header />
      <Hero />
      <Compare />
      <Features />
      <Pricing />
      <Waitlist />
      <Footer />
    </main>
  );
}

function Header() {
  return (
    <header className="sticky top-0 z-40 bg-black/80 backdrop-blur border-b border-zinc-900">
      <nav className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <a href="#" className="flex items-center gap-2">
          <span className="logo-mark w-8 h-8 rounded-lg text-sm">P</span>
          <span className="text-lg font-bold tracking-tight lowercase">pulse</span>
        </a>
        <div className="hidden md:flex items-center gap-7 text-sm text-zinc-400">
          <a href="#features" className="hover:text-white">Features</a>
          <a href="#pricing" className="hover:text-white">Pricing</a>
          <a href="https://github.com/walight999/pulse" target="_blank" rel="noopener" className="hover:text-white">GitHub</a>
          <a href="#waitlist" className="bg-mint-500 hover:bg-mint-600 text-white font-semibold px-4 py-2 rounded-lg transition">Get early access</a>
        </div>
      </nav>
    </header>
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
  const rows: Array<[string, boolean, boolean, boolean]> = [
    ["Subscription + AI usage + activity in one view", true, false, false],
    ["Local-first, zero setup", true, false, false],
    ["Multi-currency native (30+)", true, false, false],
    ["Plan ROI vs API equivalent", true, false, false],
    ["Cancellation savings tracker", true, false, false],
    ["Per-developer attribution", true, true, false],
    ["Friend leaderboard (opt-in)", true, false, false],
    ["Browser extension web capture", true, false, false],
    ["Per-cache TTL pricing (5m + 1h)", true, false, true],
    ["Works on Bedrock / Vertex", true, true, false],
  ];
  return (
    <section className="bg-zinc-950 border-y border-zinc-900 py-20">
      <div className="max-w-5xl mx-auto px-6">
        <h2 className="text-2xl md:text-4xl font-bold text-center mb-3">Why pulse wins</h2>
        <p className="text-zinc-400 text-center mb-12">Other tools give you fragments. pulse gives you the picture.</p>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-zinc-800">
                <th className="text-left py-4 px-3 font-semibold text-zinc-300">Feature</th>
                <th className="text-center py-4 px-3 font-semibold text-mint-400">pulse</th>
                <th className="text-center py-4 px-3 font-semibold text-zinc-500">ClaudeMetrics</th>
                <th className="text-center py-4 px-3 font-semibold text-zinc-500">Anthropic Console</th>
              </tr>
            </thead>
            <tbody>
              {rows.map(([label, p, c, a], i) => (
                <tr key={i} className="border-b border-zinc-900/60">
                  <td className="py-4 px-3 text-zinc-300">{label}</td>
                  <td className="text-center py-4 px-3">{p ? <span className="text-mint-400">●</span> : <span className="text-zinc-700">—</span>}</td>
                  <td className="text-center py-4 px-3">{c ? <span className="text-zinc-400">●</span> : <span className="text-zinc-700">—</span>}</td>
                  <td className="text-center py-4 px-3">{a ? <span className="text-zinc-400">●</span> : <span className="text-zinc-700">—</span>}</td>
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

        <div className="mt-20 text-center text-zinc-500 text-sm">
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
    <footer className="border-t border-zinc-900 py-12">
      <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="flex items-center gap-2">
          <span className="logo-mark w-7 h-7 rounded-lg text-xs">P</span>
          <span className="font-bold tracking-tight lowercase">pulse</span>
          <span className="text-zinc-700 mx-3">·</span>
          <span className="text-zinc-500 text-sm">Mint for the AI era</span>
        </div>
        <div className="flex items-center gap-6 text-sm text-zinc-500">
          <a href="https://github.com/walight999/pulse" target="_blank" rel="noopener" className="hover:text-white">GitHub</a>
          <a href="https://github.com/walight999/pulse/blob/main/PRIVACY.md" target="_blank" rel="noopener" className="hover:text-white">Privacy</a>
          <a href="https://github.com/walight999/pulse/blob/main/TERMS.md" target="_blank" rel="noopener" className="hover:text-white">Terms</a>
          <span>© 2026 White</span>
        </div>
      </div>
    </footer>
  );
}
