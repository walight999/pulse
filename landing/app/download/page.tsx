import type { Metadata } from "next";
import Link from "next/link";

const VERSION = "1.0.0";
const RELEASES_URL = "https://github.com/walight999/pulse/releases";
const LATEST_URL = "https://github.com/walight999/pulse/releases/latest";

export const metadata: Metadata = {
  title: "Download pulse",
  description:
    "Download pulse — the local-first AI subscription + Claude usage + activity dashboard. Windows packaged installer, macOS + Linux from source today, packaged builds coming Q3/Q4 2026.",
  alternates: { canonical: "/download" },
  openGraph: {
    title: "Download pulse",
    description: "Local-first AI finance dashboard. Windows installer + portable zip + run from source.",
    url: "https://mintforai.com/download",
    type: "article",
  },
};

type OsStatus = "available" | "source-only" | "coming-q3" | "coming-q4";

function osBadge(s: OsStatus) {
  if (s === "available")   return { label: "Available now", cls: "bg-mint-900/40 text-mint-400 border-mint-800/60" };
  if (s === "source-only") return { label: "From source today", cls: "bg-amber-900/40 text-amber-400 border-amber-800/60" };
  if (s === "coming-q3")   return { label: "Packaged Q3 2026", cls: "bg-amber-900/30 text-amber-300 border-amber-800/40" };
  return                          { label: "Packaged Q4 2026", cls: "bg-zinc-900 text-zinc-400 border-zinc-800" };
}

function Badge({ status }: { status: OsStatus }) {
  const { label, cls } = osBadge(status);
  return (
    <span className={`inline-block text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded border ${cls}`}>
      {label}
    </span>
  );
}

export default function DownloadPage() {
  return (
    <main className="min-h-screen bg-black text-white">
      <header className="sticky top-0 z-40 bg-black/80 backdrop-blur border-b border-zinc-900">
        <nav className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between" aria-label="Main">
          <Link href="/" className="flex items-center gap-2" aria-label="pulse — home">
            <span className="logo-mark w-8 h-8 rounded-lg text-sm" aria-hidden>P</span>
            <span className="text-lg font-bold tracking-tight lowercase">pulse</span>
          </Link>
          <Link href="/" className="text-sm text-zinc-400 hover:text-white transition">
            ← Back to home
          </Link>
        </nav>
      </header>

      <section className="max-w-5xl mx-auto px-6 py-14 md:py-20">
        <div className="inline-flex items-center gap-2 mb-5 px-3 py-1.5 rounded-full border border-mint-800 bg-mint-900/30 text-xs font-medium text-mint-400 uppercase tracking-wider">
          <span className="w-1.5 h-1.5 rounded-full bg-mint-400" aria-hidden></span>
          pulse v{VERSION} · local-first
        </div>
        <h1 className="text-3xl md:text-5xl font-bold tracking-tight leading-tight">
          Download pulse
        </h1>
        <p className="mt-4 text-zinc-400 text-lg leading-relaxed max-w-2xl">
          The local desktop app. Runs entirely on your machine. No account, no telemetry by default,
          no cloud calls except a once-daily FX rate fetch. MIT-licensed — audit the code yourself.
        </p>

        <div className="mt-10 grid grid-cols-1 md:grid-cols-3 gap-5">
          <OSCard
            os="Windows"
            icon="W"
            status="available"
            primary={{ label: "Download installer (.exe)", href: LATEST_URL }}
            secondary={{ label: "Portable .zip", href: LATEST_URL }}
            details={[
              "Windows 10 + 11 (x64)",
              "~80 MB installer",
              "System-tray app + browser dashboard",
              "Optional auto-start on login",
            ]}
          />
          <OSCard
            os="macOS"
            icon=""
            status="source-only"
            primary={{ label: "Run from source", href: "https://github.com/walight999/pulse#install-from-source" }}
            secondary={{ label: "Notify me when packaged", href: "/#waitlist" }}
            details={[
              "macOS 12+ (Apple Silicon + Intel)",
              "Works from source today (Python 3.12)",
              "Universal2 .app bundle planned Q3 2026",
              "Awaiting Apple Developer ID + notarization",
            ]}
          />
          <OSCard
            os="Linux"
            icon="L"
            status="source-only"
            primary={{ label: "Run from source", href: "https://github.com/walight999/pulse#install-from-source" }}
            secondary={{ label: "Notify me when packaged", href: "/#waitlist" }}
            details={[
              "Any X11 / Wayland desktop",
              "Works from source today (Python 3.12)",
              "AppImage planned Q4 2026",
              "Foreground detection via xdotool / wmctrl",
            ]}
          />
        </div>

        <div className="mt-6 rounded-xl border border-zinc-900 bg-zinc-950/50 p-5 text-sm text-zinc-400">
          <strong className="text-zinc-200">Verifying your download.</strong> Every GitHub release ships
          with SHA-256 checksums in the release notes. Verify with{" "}
          <code className="text-zinc-300">CertUtil -hashfile pulse-setup-{VERSION}.exe SHA256</code>{" "}
          (Windows) or <code className="text-zinc-300">shasum -a 256 &lt;file&gt;</code> (mac/Linux),
          then compare against the value on the{" "}
          <a href={LATEST_URL} target="_blank" rel="noopener noreferrer" className="text-mint-400 hover:text-mint-300">
            release page
          </a>
          .
        </div>
      </section>

      <section className="border-t border-zinc-900 bg-zinc-950/40 py-16">
        <div className="max-w-5xl mx-auto px-6">
          <h2 className="text-2xl md:text-3xl font-bold tracking-tight">Install in 4 steps (Windows)</h2>
          <ol className="mt-8 space-y-5">
            <Step n={1} title="Download the installer">
              Grab <code className="text-zinc-200">pulse-setup-{VERSION}.exe</code> from the{" "}
              <a href={LATEST_URL} target="_blank" rel="noopener noreferrer" className="text-mint-400 hover:text-mint-300">latest release</a>.
              First-time downloads may see a "Windows protected your PC" SmartScreen warning — this
              fades as more people install. Click <em>More info → Run anyway</em>.
            </Step>
            <Step n={2} title="Run the installer">
              Pick an install directory (default <code className="text-zinc-200">C:\Program Files\pulse\</code>),
              choose whether to add a desktop shortcut, and whether to auto-start on login. No admin
              install required — pulse only writes to <code className="text-zinc-200">HKCU</code>.
            </Step>
            <Step n={3} title="Click the tray icon">
              Pulse appears in your system tray (bottom-right of the taskbar). Click it to open the
              dashboard in your default browser at <code className="text-zinc-200">http://localhost:&lt;port&gt;</code>.
            </Step>
            <Step n={4} title="Run the 30-second first-run wizard">
              Pick currency, set a monthly AI budget (optional), choose alert preferences. All
              skippable. Pulse auto-detects Claude Code logs at{" "}
              <code className="text-zinc-200">~/.claude/projects/*.jsonl</code> on first launch.
            </Step>
          </ol>
        </div>
      </section>

      <section className="py-16">
        <div className="max-w-5xl mx-auto px-6">
          <h2 className="text-2xl md:text-3xl font-bold tracking-tight">Where your data lives</h2>
          <p className="mt-3 text-zinc-400 max-w-2xl">
            Everything pulse collects stays on your machine. Nothing is uploaded unless you turn on
            cloud sync (Pro, not yet shipped).
          </p>
          <div className="mt-8 overflow-x-auto rounded-xl border border-zinc-900 bg-black/40">
            <table className="w-full text-sm">
              <thead className="bg-zinc-950 border-b border-zinc-900 text-zinc-400">
                <tr>
                  <th className="text-left font-semibold px-4 py-3">Location</th>
                  <th className="text-left font-semibold px-4 py-3">What's stored</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-900 text-zinc-300">
                <tr>
                  <td className="px-4 py-2.5"><code>%USERPROFILE%\pulse\data\tracker.db</code></td>
                  <td className="px-4 py-2.5">SQLite database — subscriptions, AI usage, activity</td>
                </tr>
                <tr>
                  <td className="px-4 py-2.5"><code>%USERPROFILE%\pulse\backups\</code></td>
                  <td className="px-4 py-2.5">Auto-rotated DB backups (last 7 days)</td>
                </tr>
                <tr>
                  <td className="px-4 py-2.5"><code>%USERPROFILE%\pulse\logs\</code></td>
                  <td className="px-4 py-2.5">Diagnostic logs (rotated, last 30 days)</td>
                </tr>
                <tr>
                  <td className="px-4 py-2.5"><code>~/.claude/projects/*.jsonl</code></td>
                  <td className="px-4 py-2.5">Pulse reads Claude Code token logs from here — never modifies</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p className="mt-5 text-xs text-zinc-500 max-w-2xl">
            macOS / Linux equivalents: <code className="text-zinc-300">~/Library/Application Support/pulse/</code>{" "}
            and <code className="text-zinc-300">~/.local/share/pulse/</code>.
          </p>
        </div>
      </section>

      <section className="border-t border-zinc-900 bg-zinc-950/40 py-16">
        <div className="max-w-5xl mx-auto px-6">
          <h2 className="text-2xl md:text-3xl font-bold tracking-tight">Run from source (any OS)</h2>
          <p className="mt-3 text-zinc-400 max-w-2xl">
            macOS and Linux work today this way — no packaged build needed. Windows users can too,
            if they want to read or modify the code.
          </p>
          <pre className="mt-6 rounded-xl border border-zinc-900 bg-black p-5 overflow-x-auto text-sm text-zinc-200">
{`git clone https://github.com/walight999/pulse
cd pulse
pip install -r requirements.txt
python app.py`}
          </pre>
          <p className="mt-4 text-sm text-zinc-500">
            Requires Python 3.12+ and git. Full developer guide in{" "}
            <a href="https://github.com/walight999/pulse/blob/main/INSTALL.md" target="_blank" rel="noopener noreferrer" className="text-mint-400 hover:text-mint-300">INSTALL.md</a>.
          </p>
        </div>
      </section>

      <section className="py-16">
        <div className="max-w-5xl mx-auto px-6">
          <h2 className="text-2xl md:text-3xl font-bold tracking-tight">Troubleshooting</h2>
          <div className="mt-8 space-y-3">
            <Faq q="Windows Defender or SmartScreen blocks the installer">
              The signing certificate is new, so SmartScreen will warn until enough people install. Click{" "}
              <em>More info → Run anyway</em>. If Defender quarantines the file, restore it from
              quarantine + add an exclusion for <code className="text-zinc-300">C:\Program Files\pulse\</code>.
              See full steps in{" "}
              <a href="https://github.com/walight999/pulse/blob/main/TROUBLESHOOTING.md" target="_blank" rel="noopener noreferrer" className="text-mint-400 hover:text-mint-300">TROUBLESHOOTING.md</a>.
            </Faq>
            <Faq q="The dashboard didn't open in my browser">
              Pulse auto-picks an unused localhost port. Right-click the tray icon → <em>Open
              dashboard</em> to force-open. If still blocked, copy the URL from{" "}
              <code className="text-zinc-300">%USERPROFILE%\pulse\logs\app.log</code>.
            </Faq>
            <Faq q="Claude Code logs aren't being detected">
              Pulse looks at <code className="text-zinc-300">~/.claude/projects/*.jsonl</code>. If you've
              moved your Claude config, set <code className="text-zinc-300">CLAUDE_LOG_DIR</code> to the
              right path before launch. The Settings → AI Usage tab also has a manual import button.
            </Faq>
            <Faq q="How do I uninstall and delete all local data?">
              Settings → Apps → <em>pulse</em> → Uninstall. The uninstaller asks whether to keep your
              data. Choose <em>No</em> to wipe <code className="text-zinc-300">%USERPROFILE%\pulse\</code>{" "}
              completely. From-source installs: delete the cloned repo and the user-profile pulse folder.
            </Faq>
            <Faq q="Does pulse phone home? Track me? Sell my data?">
              No, no, and no. The local app makes one outbound call: the daily FX rate fetch from{" "}
              <code className="text-zinc-300">frankfurter.dev</code>, cached for 24h. Telemetry is opt-in
              and off by default. Cloud sync is Pro-only and not yet shipped. See{" "}
              <Link href="/privacy" className="text-mint-400 hover:text-mint-300">Privacy</Link> +{" "}
              <Link href="/security" className="text-mint-400 hover:text-mint-300">Security</Link>.
            </Faq>
          </div>
          <div className="mt-10 text-sm text-zinc-400">
            More help:{" "}
            <a href="https://github.com/walight999/pulse/discussions" target="_blank" rel="noopener noreferrer" className="text-mint-400 hover:text-mint-300">Discussions</a>{" "}·{" "}
            <a href="https://github.com/walight999/pulse/issues" target="_blank" rel="noopener noreferrer" className="text-mint-400 hover:text-mint-300">Issues</a>{" "}·{" "}
            <a href="mailto:hi@mintforai.com" className="text-mint-400 hover:text-mint-300">hi@mintforai.com</a>
          </div>
        </div>
      </section>

      <footer className="border-t border-zinc-900 py-10">
        <div className="max-w-5xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-3 text-xs text-zinc-600">
          <div>© 2026 pulse · operated by White, Bangkok, Thailand · MIT licensed local app</div>
          <div className="flex items-center gap-5">
            <a href={RELEASES_URL} target="_blank" rel="noopener noreferrer" className="hover:text-white">All releases</a>
            <Link href="/methodology" className="hover:text-white">Methodology</Link>
            <Link href="/roadmap" className="hover:text-white">Roadmap</Link>
            <Link href="/security" className="hover:text-white">Security</Link>
            <Link href="/privacy" className="hover:text-white">Privacy</Link>
          </div>
        </div>
      </footer>
    </main>
  );
}

function OSCard({
  os,
  icon,
  status,
  primary,
  secondary,
  details,
}: {
  os: string;
  icon: string;
  status: OsStatus;
  primary: { label: string; href: string };
  secondary?: { label: string; href: string };
  details: string[];
}) {
  const featured = status === "available";
  return (
    <div className={`rounded-2xl p-6 flex flex-col ${featured ? "bg-mint-900/10 border-2 border-mint-700/40" : "bg-zinc-950/50 border border-zinc-900"}`}>
      <div className="flex items-center justify-between mb-3">
        <div className="text-2xl font-extrabold tracking-tight">{os}</div>
        <Badge status={status} />
      </div>
      <ul className="space-y-1.5 mb-6 text-sm text-zinc-400 flex-1">
        {details.map((d, i) => (
          <li key={i} className="flex items-start gap-2">
            <span className="text-zinc-600 mt-0.5 flex-shrink-0" aria-hidden>·</span>
            <span>{d}</span>
          </li>
        ))}
      </ul>
      <a
        href={primary.href}
        target={primary.href.startsWith("http") ? "_blank" : undefined}
        rel={primary.href.startsWith("http") ? "noopener noreferrer" : undefined}
        className={`block text-center font-semibold py-2.5 rounded-lg transition text-sm ${
          featured
            ? "bg-mint-500 hover:bg-mint-600 text-white"
            : "border border-zinc-800 hover:border-zinc-700 text-zinc-200"
        }`}
      >
        {primary.label}
      </a>
      {secondary && (
        <a
          href={secondary.href}
          target={secondary.href.startsWith("http") ? "_blank" : undefined}
          rel={secondary.href.startsWith("http") ? "noopener noreferrer" : undefined}
          className="block text-center text-xs text-zinc-500 hover:text-zinc-300 mt-2.5 transition"
        >
          {secondary.label}
        </a>
      )}
    </div>
  );
}

function Step({ n, title, children }: { n: number; title: string; children: React.ReactNode }) {
  return (
    <li className="flex gap-4 items-start">
      <div className="flex-shrink-0 w-8 h-8 rounded-full bg-mint-900/40 border border-mint-700/50 text-mint-400 font-bold text-sm flex items-center justify-center">
        {n}
      </div>
      <div className="flex-1">
        <div className="font-semibold text-zinc-100 mb-1">{title}</div>
        <p className="text-sm text-zinc-400 leading-relaxed">{children}</p>
      </div>
    </li>
  );
}

function Faq({ q, children }: { q: string; children: React.ReactNode }) {
  return (
    <details className="group rounded-xl border border-zinc-900 bg-black/40 open:bg-zinc-950/60 transition">
      <summary className="cursor-pointer px-5 py-4 text-zinc-200 font-medium flex items-center justify-between hover:text-white transition">
        <span>{q}</span>
        <span className="text-zinc-600 group-open:text-mint-400 transition text-lg">+</span>
      </summary>
      <div className="px-5 pb-4 pt-1 text-zinc-400 text-sm leading-relaxed">{children}</div>
    </details>
  );
}
