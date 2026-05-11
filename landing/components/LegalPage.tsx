import Link from "next/link";
import type { ReactNode } from "react";

export function LegalPage({
  title,
  subtitle,
  lastUpdated,
  children,
}: {
  title: string;
  subtitle?: string;
  lastUpdated?: string;
  children: ReactNode;
}) {
  return (
    <main className="min-h-screen bg-black text-white">
      <header className="sticky top-0 z-40 bg-black/80 backdrop-blur border-b border-zinc-900">
        <nav className="max-w-4xl mx-auto px-6 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <span className="logo-mark w-8 h-8 rounded-lg text-sm">P</span>
            <span className="text-lg font-bold tracking-tight lowercase">pulse</span>
          </Link>
          <Link href="/" className="text-sm text-zinc-400 hover:text-white transition">
            ← Back to home
          </Link>
        </nav>
      </header>

      <article className="max-w-3xl mx-auto px-6 py-14 md:py-20">
        <h1 className="text-3xl md:text-5xl font-bold tracking-tight">{title}</h1>
        {subtitle && (
          <p className="mt-3 text-zinc-400 text-lg leading-relaxed">{subtitle}</p>
        )}
        {lastUpdated && (
          <p className="mt-5 text-xs uppercase tracking-wider text-zinc-600">
            Last updated · {lastUpdated}
          </p>
        )}
        <hr className="mt-8 border-zinc-900" />

        <div className="legal-prose mt-10 text-zinc-300 leading-relaxed">
          {children}
        </div>

        <hr className="mt-14 border-zinc-900" />
        <div className="mt-6 flex flex-wrap items-center justify-between gap-3 text-sm">
          <Link href="/" className="text-zinc-400 hover:text-white">
            ← pulse home
          </Link>
          <div className="flex items-center gap-5 text-zinc-500">
            <Link href="/privacy" className="hover:text-white">Privacy</Link>
            <Link href="/terms" className="hover:text-white">Terms</Link>
            <Link href="/security" className="hover:text-white">Security</Link>
            <Link href="/changelog" className="hover:text-white">Changelog</Link>
          </div>
        </div>
      </article>
    </main>
  );
}
