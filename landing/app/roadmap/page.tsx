import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Roadmap — pulse",
  description:
    "What's shipped, what's next, what's later, and what's under consideration for pulse. Community votes via GitHub Discussions shape the order.",
  alternates: { canonical: "/roadmap" },
  openGraph: {
    title: "Roadmap — pulse",
    description: "Public roadmap for pulse — local-first AI subscription + Claude usage + activity dashboard.",
    url: "https://mintforai.com/roadmap",
    type: "article",
  },
};

type Col = {
  title: string;
  subtitle: string;
  badge: string;
  badgeCls: string;
  items: string[];
};

const cols: Col[] = [
  {
    title: "Now",
    subtitle: "Shipped in v1.0",
    badge: "Available",
    badgeCls: "bg-mint-900/40 text-mint-400 border-mint-800/60",
    items: [
      "Subscription tracker (30+ currencies via ECB)",
      "Claude Code log parser (~/.claude/projects/*.jsonl)",
      "Plan ROI vs equivalent API value",
      "Cache TTL pricing (5m + 1h split)",
      "Local activity tracker (foreground time)",
      "Cost-per-active-hour per subscription",
      "Cancellation savings counter",
      "CSV export",
      "Multi-currency display",
      "Windows packaged installer",
      "macOS + Linux run-from-source",
      "Local SQLite + auto backups (7 days)",
    ],
  },
  {
    title: "Next",
    subtitle: "Pro tier · Q3 2026",
    badge: "Q3 2026",
    badgeCls: "bg-amber-900/40 text-amber-400 border-amber-800/60",
    items: [
      "E2E encrypted cloud sync (AES-256-GCM + Argon2id)",
      "Mobile PWA (iOS + Android)",
      "Multi-provider live tracking (OpenAI / Cursor / Gemini / Copilot)",
      "Ask pulse AI assistant (Claude-powered)",
      "Friend leaderboard (opt-in, three visibility levels)",
      "Stripe billing + subscription management",
      "macOS packaged build (universal2)",
      "Self-host cloud server (MIT, bring-your-own Supabase)",
    ],
  },
  {
    title: "Later",
    subtitle: "Team tier · Q3/Q4 2026",
    badge: "Q4 2026",
    badgeCls: "bg-amber-900/30 text-amber-300 border-amber-800/40",
    items: [
      "Team workspaces + per-user attribution",
      "Slack / Teams / Discord renewal alerts",
      "Admin controls + audit log retention",
      "Browser extension web capture (Chrome/Firefox/Edge)",
      "Linux AppImage / Flatpak",
      "Bug bounty program",
      "Public anonymized AI-spend benchmarks",
      "SOC 2 Type I audit",
    ],
  },
  {
    title: "Under consideration",
    subtitle: "No ETA · open to community feedback",
    badge: "Roadmap",
    badgeCls: "bg-zinc-900 text-zinc-400 border-zinc-800",
    items: [
      "SSO (SAML 2.0 + OIDC) — Enterprise",
      "SOC 2 Type II — Enterprise",
      "On-prem / VPC deployment — Enterprise",
      "Bank integration (Plaid) — auto-detect recurring charges",
      "Gmail OAuth — receipt-based subscription discovery",
      "Receipt OCR (drop image → extract subscription)",
      "Local DB encryption at rest (passphrase)",
      "Native iOS / Android apps (vs PWA)",
      "Affiliate links for cheaper alternative plans",
      "Renewal negotiation playbook templates",
    ],
  },
];

export default function RoadmapPage() {
  return (
    <main className="min-h-screen bg-black text-white">
      <header className="sticky top-0 z-40 bg-black/80 backdrop-blur border-b border-zinc-900">
        <nav className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between" aria-label="Main">
          <Link href="/" className="flex items-center gap-2" aria-label="pulse — home">
            <span className="logo-mark w-8 h-8 rounded-lg text-sm" aria-hidden>P</span>
            <span className="text-lg font-bold tracking-tight lowercase">pulse</span>
          </Link>
          <Link href="/" className="text-sm text-zinc-400 hover:text-white transition">
            ← Back to home
          </Link>
        </nav>
      </header>

      <section className="max-w-6xl mx-auto px-6 py-14 md:py-20">
        <div className="inline-flex items-center gap-2 mb-5 px-3 py-1.5 rounded-full border border-mint-800 bg-mint-900/30 text-xs font-medium text-mint-400 uppercase tracking-wider">
          <span className="w-1.5 h-1.5 rounded-full bg-mint-400" aria-hidden></span>
          Public roadmap · community-shaped
        </div>
        <h1 className="text-3xl md:text-5xl font-bold tracking-tight leading-tight">Roadmap</h1>
        <p className="mt-4 text-zinc-400 text-lg leading-relaxed max-w-2xl">
          Honest split of what's shipped, what's next, what's later, and what's still under
          consideration. Order is shaped by community votes on GitHub Discussions and Issues —
          plans below are not promises, especially anything past Q3 2026.
        </p>

        <div className="mt-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          {cols.map((c, i) => (
            <div key={i} className="rounded-2xl border border-zinc-900 bg-zinc-950/40 p-6 flex flex-col">
              <div className="mb-3">
                <span className={`inline-block text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded border ${c.badgeCls}`}>{c.badge}</span>
              </div>
              <h2 className="text-xl font-bold text-zinc-100 mb-1">{c.title}</h2>
              <p className="text-xs text-zinc-500 mb-5">{c.subtitle}</p>
              <ul className="space-y-2 text-sm text-zinc-300 flex-1">
                {c.items.map((item, j) => (
                  <li key={j} className="flex items-start gap-2">
                    <span className="text-zinc-600 mt-0.5 flex-shrink-0" aria-hidden>·</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-14 rounded-2xl border border-zinc-900 bg-zinc-950/40 p-6 md:p-8">
          <h2 className="text-lg md:text-xl font-bold mb-2">Vote on what ships next</h2>
          <p className="text-zinc-400 text-sm mb-5 max-w-2xl">
            Pulse is solo-built open-source. The order of "Later" and "Under consideration" items is
            heavily shaped by community demand. Open a Discussion with your use case, or thumbs-up
            an existing Issue — both count.
          </p>
          <div className="flex flex-wrap gap-3">
            <a
              href="https://github.com/walight999/pulse/discussions"
              target="_blank"
              rel="noopener noreferrer"
              className="bg-mint-500 hover:bg-mint-600 text-white font-semibold px-5 py-2.5 rounded-lg transition text-sm"
            >
              Open a Discussion →
            </a>
            <a
              href="https://github.com/walight999/pulse/issues"
              target="_blank"
              rel="noopener noreferrer"
              className="border border-zinc-800 hover:border-zinc-700 text-zinc-200 font-medium px-5 py-2.5 rounded-lg transition text-sm"
            >
              Browse Issues →
            </a>
            <a
              href="/#waitlist"
              className="border border-zinc-800 hover:border-zinc-700 text-zinc-200 font-medium px-5 py-2.5 rounded-lg transition text-sm"
            >
              Join waitlist →
            </a>
          </div>
        </div>
      </section>

      <footer className="border-t border-zinc-900 py-10">
        <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-3 text-xs text-zinc-600">
          <div>© 2026 pulse · operated by White, Bangkok, Thailand · MIT licensed local app</div>
          <div className="flex items-center gap-5">
            <Link href="/download" className="hover:text-white">Download</Link>
            <Link href="/methodology" className="hover:text-white">Methodology</Link>
            <Link href="/changelog" className="hover:text-white">Changelog</Link>
            <Link href="/security" className="hover:text-white">Security</Link>
          </div>
        </div>
      </footer>
    </main>
  );
}
