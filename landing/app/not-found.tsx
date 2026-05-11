import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Page not found",
  description: "That page doesn't exist on pulse — let's get you back on track.",
  robots: { index: false, follow: false },
};

export default function NotFound() {
  return (
    <main className="min-h-screen bg-black text-white flex items-center justify-center px-6">
      <div className="text-center max-w-md">
        <div className="inline-flex items-center justify-center mb-7">
          <span className="logo-mark w-14 h-14 rounded-2xl text-2xl">P</span>
        </div>
        <div className="text-mint-400 text-sm font-bold tracking-wider uppercase mb-3">404</div>
        <h1 className="text-3xl md:text-5xl font-bold tracking-tight">Pulse not detected.</h1>
        <p className="mt-5 text-zinc-400 leading-relaxed">
          That page isn't in the dashboard. It may have been moved, renamed, or never existed.
          The signal flatlines but the patient is fine.
        </p>
        <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-3">
          <Link
            href="/"
            className="bg-mint-500 hover:bg-mint-600 text-white font-semibold px-6 py-3 rounded-xl transition shadow-lg shadow-mint-500/20"
          >
            Back to home
          </Link>
          <Link
            href="/changelog"
            className="text-zinc-300 hover:text-white font-medium px-4 py-3 transition"
          >
            See what's new →
          </Link>
        </div>
        <div className="mt-10 ecg-line max-w-xs mx-auto opacity-50" />
        <div className="mt-12 text-xs text-zinc-600 flex items-center justify-center gap-5">
          <Link href="/privacy" className="hover:text-zinc-400">Privacy</Link>
          <Link href="/terms" className="hover:text-zinc-400">Terms</Link>
          <Link href="/security" className="hover:text-zinc-400">Security</Link>
          <a href="https://github.com/walight999/pulse" target="_blank" rel="noopener" className="hover:text-zinc-400">GitHub</a>
        </div>
      </div>
    </main>
  );
}
