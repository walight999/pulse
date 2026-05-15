import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Offline — pulse",
  description: "You're offline. The pulse desktop app keeps working — it doesn't need this site to be up.",
  alternates: { canonical: "/offline" },
  robots: { index: false, follow: false },
};

export default function OfflinePage() {
  return (
    <main className="min-h-screen bg-black text-white">
      <header className="sticky top-0 z-40 bg-black/80 backdrop-blur border-b border-zinc-900">
        <nav className="max-w-4xl mx-auto px-6 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <span className="logo-mark w-8 h-8 rounded-lg text-sm" aria-hidden>P</span>
            <span className="text-lg font-bold tracking-tight lowercase">pulse</span>
          </Link>
        </nav>
      </header>

      <section className="max-w-4xl mx-auto px-6 py-20 md:py-28 text-center">
        <div className="inline-flex items-center gap-2 mb-5 px-3 py-1.5 rounded-full border border-amber-700 bg-amber-900/30 text-xs font-medium text-amber-300 uppercase tracking-wider">
          <span className="w-1.5 h-1.5 rounded-full bg-amber-300" aria-hidden></span>
          You're offline
        </div>
        <h1 className="text-3xl md:text-5xl font-bold tracking-tight leading-tight">
          Pulse desktop app doesn't need this site.
        </h1>
        <p className="mt-5 text-zinc-400 text-lg leading-relaxed max-w-2xl mx-auto">
          You're seeing this because your browser couldn't reach mintforai.com. That's fine —
          the pulse desktop app runs entirely on your machine and keeps working without an internet
          connection (except the once-a-day FX rate fetch).
        </p>

        <div className="mt-10 grid grid-cols-1 md:grid-cols-3 gap-4 max-w-2xl mx-auto text-left">
          <div className="rounded-xl border border-zinc-900 bg-zinc-950/40 p-5">
            <div className="text-xs uppercase tracking-wider text-zinc-500 font-bold mb-2">Cached pages</div>
            <ul className="space-y-1.5 text-sm text-zinc-300">
              <li><Link href="/demo" className="hover:text-mint-400">Interactive demo</Link></li>
              <li><Link href="/docs" className="hover:text-mint-400">Documentation</Link></li>
              <li><Link href="/methodology" className="hover:text-mint-400">ROI methodology</Link></li>
              <li><Link href="/roadmap" className="hover:text-mint-400">Roadmap</Link></li>
              <li><Link href="/alternatives" className="hover:text-mint-400">Alternatives</Link></li>
            </ul>
          </div>
          <div className="rounded-xl border border-zinc-900 bg-zinc-950/40 p-5">
            <div className="text-xs uppercase tracking-wider text-zinc-500 font-bold mb-2">If pulse is running</div>
            <p className="text-sm text-zinc-300">
              Right-click the tray icon → <em>Open dashboard</em>. Your data is on this machine, not
              ours.
            </p>
          </div>
          <div className="rounded-xl border border-zinc-900 bg-zinc-950/40 p-5">
            <div className="text-xs uppercase tracking-wider text-zinc-500 font-bold mb-2">Try again</div>
            <a href="/" className="text-sm text-mint-400 hover:text-mint-300">
              Reload home →
            </a>
            <p className="text-xs text-zinc-500 mt-2">Or press the browser reload button.</p>
          </div>
        </div>
      </section>

      <footer className="border-t border-zinc-900 py-10">
        <div className="max-w-4xl mx-auto px-6 text-center text-xs text-zinc-600">
          © 2026 pulse · MIT-licensed local app · the offline-friendly AI finance dashboard
        </div>
      </footer>
    </main>
  );
}
