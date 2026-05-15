import type { Metadata } from "next";
import Link from "next/link";

const REPO = "https://github.com/walight999/pulse";

export const metadata: Metadata = {
  title: "Docs — pulse",
  description:
    "Quickstart, install guides, Claude log import, activity privacy, backup, self-host, security, ROI methodology, and troubleshooting for pulse.",
  alternates: { canonical: "/docs" },
  openGraph: {
    title: "Docs — pulse",
    description: "Everything you need to set up and run pulse — local-first AI subscription dashboard.",
    url: "https://mintforai.com/docs",
    type: "article",
  },
};

type DocCard = {
  title: string;
  body: string;
  href: string;
  external?: boolean;
};

type Section = {
  heading: string;
  cards: DocCard[];
};

const sections: Section[] = [
  {
    heading: "Quickstart",
    cards: [
      {
        title: "Install on Windows (5 min)",
        body: "Download installer, click through wizard, dashboard opens in your browser. SmartScreen workaround included.",
        href: "/download",
      },
      {
        title: "Install on macOS",
        body: "Run from source today (Python 3.12). Packaged universal2 .app planned Q3 2026 once Apple Developer ID is set up.",
        href: `${REPO}/blob/main/INSTALL.md#macos--coming-q3-2026`,
        external: true,
      },
      {
        title: "Install on Linux",
        body: "Run from source today on any X11 or Wayland desktop. AppImage planned Q4 2026 once community testers are confirmed.",
        href: `${REPO}/blob/main/INSTALL.md#linux--coming-q4-2026`,
        external: true,
      },
      {
        title: "Install from source",
        body: "git clone + pip install + python app.py. Works on Windows, macOS, and Linux today.",
        href: `${REPO}/blob/main/INSTALL.md#from-source-any-platform--for-developers`,
        external: true,
      },
    ],
  },
  {
    heading: "Importing your data",
    cards: [
      {
        title: "Claude Code log import",
        body: "Pulse auto-detects ~/.claude/projects/*.jsonl on first launch. Set CLAUDE_LOG_DIR if your config is elsewhere. Manual import in Settings → AI usage.",
        href: `${REPO}/blob/main/README.md#claude-code-token-import`,
        external: true,
      },
      {
        title: "Anthropic Admin API setup",
        body: "Paste your Admin API key in Settings → Provider API keys for team-level attribution beyond a single machine. Stored locally.",
        href: "/methodology#3-token-pricing-source",
      },
      {
        title: "Add AI subscriptions manually",
        body: "Subscriptions tab → Add subscription. Pick a plan from the catalog (Claude Max / ChatGPT Plus / Cursor / …) or enter a custom price.",
        href: `${REPO}/blob/main/README.md#what-pulse-does`,
        external: true,
      },
      {
        title: "Set display currency",
        body: "Settings → Preferences → Currency. 30+ currencies via daily ECB rates from frankfurter.dev (cached 24h).",
        href: "/methodology#5-subscription-cost--exact-estimated-or-per-tier",
      },
    ],
  },
  {
    heading: "Privacy & security",
    cards: [
      {
        title: "Activity tracking privacy",
        body: "Opt-in only — off by default. Settings → Preferences → Privacy & activity tracking. Master toggle, store-titles toggle, blocklist, pause buttons.",
        href: "/security#privacy",
      },
      {
        title: "Window title redaction",
        body: "If you turn activity tracking on, leave 'Also store window titles' OFF. Pulse will still log which app you used but never the title (which may contain document names, tab content, customer info).",
        href: "/security#privacy",
      },
      {
        title: "Pause tracking",
        body: "Settings → Preferences → Privacy → Pause buttons (1 hour / until tomorrow / 1 week). The tracker picks up changes within 60 seconds without a restart.",
        href: "/security#privacy",
      },
      {
        title: "Delete activity history",
        body: "Settings → Preferences → Privacy → Delete activity history. Tick the confirm checkbox first — deletes every row from app_activity, irreversible.",
        href: "/security#audit-logging",
      },
    ],
  },
  {
    heading: "Backup, export, and data location",
    cards: [
      {
        title: "Where your data lives",
        body: "All data is in a single SQLite file under your user profile. See the data-location table on the Download page for the exact path per OS.",
        href: "/download#where-your-data-lives",
      },
      {
        title: "Auto backups",
        body: "Pulse rotates SQLite backups daily and keeps the last 7. Located in pulse/backups/ inside your user profile.",
        href: `${REPO}/blob/main/README.md#privacy--security`,
        external: true,
      },
      {
        title: "Export to CSV",
        body: "Settings → Data & backup → Export. Generates a CSV of subscriptions, AI usage, and activity. Open in Excel / Sheets / your finance tool.",
        href: `${REPO}/blob/main/README.md#exports`,
        external: true,
      },
      {
        title: "Restore from backup",
        body: "Settings → Data & backup → Restore. Pick a .db file from pulse/backups/ — the current DB is moved aside automatically.",
        href: `${REPO}/blob/main/TROUBLESHOOTING.md`,
        external: true,
      },
    ],
  },
  {
    heading: "Self-hosting the cloud server",
    cards: [
      {
        title: "Why self-host?",
        body: "Free, MIT-licensed, no rate limit. Bring your own Supabase project. Pulse Pro hosting is a convenience tier, not a feature gate.",
        href: "/#pricing",
      },
      {
        title: "Cloud module overview",
        body: "cloud/auth.py, cloud/sync.py, cloud/crypto.py, api/server.py. Argon2id + AES-256-GCM, FastAPI server. Scaffolded today, deploys with v1.1 (Q3 2026).",
        href: `${REPO}/tree/main/cloud`,
        external: true,
      },
      {
        title: "Set up Supabase",
        body: "Create a free project, run the schema in ROADMAP.md § 1.2, set SUPABASE_URL + SUPABASE_ANON_KEY env vars on your client.",
        href: `${REPO}/blob/main/ROADMAP.md#phase-1--auth--cloud-sync--payment`,
        external: true,
      },
    ],
  },
  {
    heading: "How pulse calculates things",
    cards: [
      {
        title: "ROI methodology",
        body: "Plan ROI = Equivalent API Value ÷ Subscription Cost. Token counts come from your local Claude logs; prices come from Anthropic's published rates.",
        href: "/methodology",
      },
      {
        title: "Cache TTL pricing (5m + 1h)",
        body: "Most tools lump cache writes together — pulse splits 5-minute and 1-hour TTLs at their respective rates. Off by up to 60% otherwise.",
        href: "/methodology#4-cache-ttl--why-5m-and-1h-are-split",
      },
      {
        title: "Cost-per-active-hour",
        body: "Subscription cost ÷ foreground hours where the linked app was the active window (idle excluded). Activity tracking must be opted in.",
        href: "/methodology#6-cost-per-active-hour",
      },
      {
        title: "Cancellation savings",
        body: "monthly_cost × months_since_cancellation_date, summed across every cancelled subscription. Cumulative counter from cancellation date forward.",
        href: "/methodology#7-cancellation-savings",
      },
    ],
  },
  {
    heading: "Security model",
    cards: [
      {
        title: "Threat model",
        body: "What pulse assumes is trusted (your machine) and what it doesn't (the cloud — once it exists). Master password is the root of trust for cloud sync.",
        href: "/security#threat-model",
      },
      {
        title: "Encryption today vs planned",
        body: "Local SQLite is unencrypted by default — use BitLocker / FileVault. Per-row AES-256-GCM is designed for Pro cloud sync but not yet shipped.",
        href: "/security#encryption",
      },
      {
        title: "Compliance roadmap",
        body: "No certifications today (MIT local app needs none). SOC 2 Type I planned for Team tier. SOC 2 Type II + ISO 27001 + HIPAA-ready architecture on the Enterprise roadmap.",
        href: "/security#compliance-roadmap",
      },
      {
        title: "Reporting a vulnerability",
        body: "Email security@mintforai.com — do not file a public issue. Acknowledgement within 24 hours, critical fixes within 7 days.",
        href: "/security#reporting-vulnerabilities",
      },
    ],
  },
  {
    heading: "Troubleshooting",
    cards: [
      {
        title: "Top 10 common issues",
        body: "SmartScreen / Defender, dashboard didn't open, Claude logs not detected, port conflicts, FX rate fetch failure, uninstall clean.",
        href: `${REPO}/blob/main/TROUBLESHOOTING.md`,
        external: true,
      },
      {
        title: "How to uninstall + delete all local data",
        body: "Windows: Settings → Apps → pulse → Uninstall → choose 'No' to keep data. From-source: delete the cloned repo and pulse user-profile folder.",
        href: "/download#troubleshooting",
      },
      {
        title: "Claude Code logs aren't being detected",
        body: "Pulse looks at ~/.claude/projects/*.jsonl. If you've moved your Claude config, set CLAUDE_LOG_DIR. Manual import button in Settings → AI usage.",
        href: "/download#troubleshooting",
      },
      {
        title: "Where to ask for help",
        body: "GitHub Discussions for questions, Issues for bug reports, hi@mintforai.com for anything else. There's no Discord yet (planned with Pro).",
        href: `${REPO}/discussions`,
        external: true,
      },
    ],
  },
  {
    heading: "FAQ by audience",
    cards: [
      {
        title: "Developer FAQ",
        body: "How exact are the numbers? Where does the pricing table live? Can I rip ROI logic into my own tool? Why Python + Streamlit? Read the pricing source in sync_tokens.py.",
        href: "/methodology#10-verify-it-yourself",
      },
      {
        title: "Non-technical FAQ",
        body: "Why MIT-licensed? Does pulse phone home? Will I lose data if I uninstall? Is the Pro plan a lock-in? What happens if you stop developing pulse?",
        href: "/#pricing",
      },
      {
        title: "Founder FAQ",
        body: "How does pulse compare to Mint / YNAB / Vantage / Datadog? Is it ready for a 10-person team? What's the cloud cost model if we hit 1,000 employees?",
        href: "/roadmap",
      },
      {
        title: "Privacy-conscious FAQ",
        body: "What's stored on disk? What's the only outbound network call? Can I run fully air-gapped? Why is activity tracking opt-in?",
        href: "/security",
      },
    ],
  },
];

export default function DocsPage() {
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
          User docs
        </div>
        <h1 className="text-3xl md:text-5xl font-bold tracking-tight leading-tight">Documentation</h1>
        <p className="mt-4 text-zinc-400 text-lg leading-relaxed max-w-2xl">
          Everything you need to install pulse, import your data, control your privacy, and trust the
          numbers. Links to external docs (INSTALL, TROUBLESHOOTING, ROADMAP, source code) open on
          GitHub.
        </p>

        <div className="mt-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <a href="/download" className="rounded-xl border border-mint-800/60 bg-mint-950/20 p-4 hover:border-mint-700 transition">
            <div className="text-sm font-bold text-mint-400">Quickstart →</div>
            <div className="text-xs text-zinc-400 mt-1">Install + first-run in 5 minutes</div>
          </a>
          <a href="/methodology" className="rounded-xl border border-zinc-900 bg-zinc-950/40 p-4 hover:border-zinc-700 transition">
            <div className="text-sm font-bold text-zinc-100">ROI methodology →</div>
            <div className="text-xs text-zinc-400 mt-1">Every formula, source, and limitation</div>
          </a>
          <a href="/security" className="rounded-xl border border-zinc-900 bg-zinc-950/40 p-4 hover:border-zinc-700 transition">
            <div className="text-sm font-bold text-zinc-100">Security →</div>
            <div className="text-xs text-zinc-400 mt-1">Threat model + implemented vs planned</div>
          </a>
          <a href={REPO} target="_blank" rel="noopener noreferrer" className="rounded-xl border border-zinc-900 bg-zinc-950/40 p-4 hover:border-zinc-700 transition">
            <div className="text-sm font-bold text-zinc-100">GitHub →</div>
            <div className="text-xs text-zinc-400 mt-1">Source code, releases, issues</div>
          </a>
        </div>

        {sections.map((s, i) => (
          <section key={i} className="mt-14">
            <h2 className="text-xl md:text-2xl font-bold tracking-tight mb-5">{s.heading}</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {s.cards.map((c, j) => {
                const inner = (
                  <div className="h-full rounded-xl border border-zinc-900 bg-zinc-950/40 p-5 hover:border-mint-800 transition">
                    <div className="font-semibold text-zinc-100 mb-1.5 flex items-start gap-2">
                      <span className="flex-1 min-w-0">{c.title}</span>
                      {c.external && <span className="text-xs text-zinc-500 flex-shrink-0" aria-hidden>↗</span>}
                    </div>
                    <p className="text-sm text-zinc-400 leading-relaxed">{c.body}</p>
                  </div>
                );
                if (c.external) {
                  return (
                    <a key={j} href={c.href} target="_blank" rel="noopener noreferrer" className="block">
                      {inner}
                    </a>
                  );
                }
                return (
                  <Link key={j} href={c.href} className="block">
                    {inner}
                  </Link>
                );
              })}
            </div>
          </section>
        ))}

        <div className="mt-14 rounded-2xl border border-zinc-900 bg-zinc-950/40 p-6 md:p-8">
          <h2 className="text-lg md:text-xl font-bold mb-2">Can't find what you need?</h2>
          <p className="text-zinc-400 text-sm mb-5 max-w-2xl">
            Pulse is solo-built. If a doc is missing or wrong, the fastest fix is to open a
            Discussion — most "missing docs" turn into a real doc within a few days. Bug reports go
            in Issues.
          </p>
          <div className="flex flex-wrap gap-3">
            <a
              href={`${REPO}/discussions`}
              target="_blank"
              rel="noopener noreferrer"
              className="bg-mint-500 hover:bg-mint-600 text-white font-semibold px-5 py-2.5 rounded-lg transition text-sm"
            >
              Open a Discussion →
            </a>
            <a
              href={`${REPO}/issues`}
              target="_blank"
              rel="noopener noreferrer"
              className="border border-zinc-800 hover:border-zinc-700 text-zinc-200 font-medium px-5 py-2.5 rounded-lg transition text-sm"
            >
              Report a bug →
            </a>
            <a
              href="mailto:hi@mintforai.com"
              className="border border-zinc-800 hover:border-zinc-700 text-zinc-200 font-medium px-5 py-2.5 rounded-lg transition text-sm"
            >
              Email hi@mintforai.com
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
            <Link href="/roadmap" className="hover:text-white">Roadmap</Link>
            <Link href="/changelog" className="hover:text-white">Changelog</Link>
            <Link href="/security" className="hover:text-white">Security</Link>
          </div>
        </div>
      </footer>
    </main>
  );
}
