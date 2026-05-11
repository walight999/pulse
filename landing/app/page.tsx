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
  const tiers = [
    {
      name: "Free",
      price: "$0",
      sub: "forever",
      tagline: "Local use, all features",
      perks: ["All v1.0 features", "Local SQLite", "No account", "Windows tray (macOS soon)"],
      cta: "Download",
      featured: false,
    },
    {
      name: "Pro",
      price: "$9",
      sub: "/mo",
      tagline: "Cross-device sync + mobile",
      perks: ["E2E encrypted cloud sync", "Mobile PWA", "Friend leaderboard", "Multi-provider (OpenAI, Cursor, Gemini, Copilot)", "Ask pulse AI assistant"],
      cta: "Join waitlist",
      featured: true,
    },
    {
      name: "Team",
      price: "$19",
      sub: "/seat/mo",
      tagline: "5-50 dev teams",
      perks: ["Shared dashboard", "Per-user attribution", "Slack/Teams/Discord webhooks", "Admin controls", "Min 3 seats"],
      cta: "Contact sales",
      featured: false,
    },
    {
      name: "Enterprise",
      price: "$199",
      sub: "/seat/mo",
      tagline: "50+ orgs",
      perks: ["SSO/SAML", "SOC 2", "Custom roles", "Dedicated support", "SLA"],
      cta: "Talk to us",
      featured: false,
    },
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
              className={`rounded-2xl p-7 transition ${
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
              <ul className="space-y-2 mb-7 text-sm text-zinc-300">
                {t.perks.map((p, j) => (
                  <li key={j} className="flex items-start gap-2">
                    <span className="text-mint-400 mt-0.5">●</span> <span>{p}</span>
                  </li>
                ))}
              </ul>
              <a
                href="#waitlist"
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
