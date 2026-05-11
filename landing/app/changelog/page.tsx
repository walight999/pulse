import type { Metadata } from "next";
import { LegalPage } from "../../components/LegalPage";

export const metadata: Metadata = {
  title: "Changelog — pulse",
  description: "Release notes and what's new in pulse — local-first personal-finance dashboard for the AI era.",
  alternates: { canonical: "/changelog" },
  openGraph: {
    title: "Changelog — pulse",
    description: "What's new in pulse — release notes by version.",
    url: "https://mintforai.com/changelog",
    type: "article",
  },
};

export default function ChangelogPage() {
  return (
    <LegalPage
      title="Changelog"
      subtitle="What's new in pulse. Versions follow semver; minor releases ship roughly every 4 weeks."
      lastUpdated="2026-05-12"
    >
      <p>
        Building in public — every release ships with a public PR + release notes on{" "}
        <a href="https://github.com/walight999/pulse/releases" target="_blank" rel="noopener noreferrer">
          GitHub
        </a>.
      </p>

      <h2 id="v1-5">v1.5 — Open-core + domain (2026-05-12)</h2>
      <h3>Added</h3>
      <ul>
        <li>
          <strong>Tier feature flag system</strong> — <code>account.get_tier()</code> with 4 tiers
          (free/pro/team/enterprise) and 26 feature flags. Lock UI helper{" "}
          <code>tier_lock_banner()</code> for one-line gating.
        </li>
        <li>
          <strong>Pricing landing page</strong> — 4-tier cards + 21-row feature comparison matrix +
          8-question FAQ
        </li>
        <li>
          <strong>Settings → Plans & billing</strong> — current tier card, Stripe Customer Portal
          link, billing metadata
        </li>
        <li>
          <strong>Settings → Integrations</strong> — Slack / Teams / Discord webhook form (Team
          tier) + SSO row (Enterprise tier)
        </li>
        <li>
          <strong>PWA manifest</strong> — installable from browser with icons, shortcuts, brand
          colors
        </li>
        <li>
          <strong>Custom domain</strong> — <a href="https://mintforai.com">mintforai.com</a> live
          on Vercel
        </li>
        <li>
          <strong>Open-core docs</strong> — README now explicitly explains Logseq/Plausible/Cal.com
          pattern
        </li>
        <li>
          <strong>Vercel + Cloudflare DNS playbook</strong> — click-by-click for self-hosters
        </li>
      </ul>
      <h3>Changed</h3>
      <ul>
        <li>Next.js bumped 14.2.5 → 14.2.35 (security patch)</li>
        <li><code>metadataBase</code> set so OG images resolve correctly across all paths</li>
        <li><code>themeColor</code> moved to viewport export (Next 14.2+ API)</li>
      </ul>

      <h2 id="v1-1">v1.1 — Phase B foundation (2026-05-11)</h2>
      <h3>Added — cloud + multi-provider scaffolding</h3>
      <ul>
        <li>
          <strong>Cloud sync</strong> (<code>cloud/</code>) — production-ready code for Supabase
          Auth + E2E encrypted sync
        </li>
        <li><strong>REST API</strong> (<code>api/server.py</code>) — FastAPI server with auth, exports, leaderboard endpoints</li>
        <li><strong>Python SDK</strong> (<code>sdk/python/pulse_client.py</code>) — programmatic access to your own pulse data</li>
        <li><strong>Browser extension</strong> (<code>browser-ext/</code>) — Manifest V3 capture for ChatGPT, Claude.ai, Gemini, Perplexity</li>
        <li><strong>Cross-platform shim</strong> — foreground app + idle detection + notifications for Windows / macOS / Linux</li>
        <li><strong>CSV + PDF export</strong> — full data export, monthly PDF reports via reportlab</li>
        <li><strong>Slack / Teams / Discord integrations</strong> — themed daily digests, spend alerts, renewal reminders</li>
      </ul>
      <h3>Added — providers</h3>
      <ul>
        <li><code>providers/openai_parser.py</code> — ChatGPT Plus + API + Team with current GPT-5/o3 pricing</li>
        <li><code>providers/cursor_parser.py</code> — Cursor IDE local state DB parser</li>
        <li><code>providers/gemini_parser.py</code> — Google AI Studio + Gemini app with current pricing</li>
        <li><code>providers/copilot_parser.py</code> — GitHub Copilot flat + GraphQL audit</li>
      </ul>
      <h3>Added — security + compliance</h3>
      <ul>
        <li><code>SECURITY.md</code> — full threat model + encryption details + bug bounty plan</li>
        <li>Audit log table (<code>audit_log</code>) — all sensitive events tracked locally</li>
      </ul>
      <h3>Changed — UX polish</h3>
      <ul>
        <li>Sub-action row no longer overlaps card (4px gap instead of -2px overlap)</li>
        <li>Streak chip glow radius reduced (no overlap with H1)</li>
        <li>Filter chips center-aligned with no leftover spacing from hidden radio circle</li>
        <li>Page header gets 8-12px breathing room before content</li>
        <li>Streamlit columns get explicit 1rem gap (was tight default)</li>
        <li>Top apps legend moved from bottom to header row</li>
        <li>ROI hero card moved to top of AI usage + Overview pages</li>
        <li>All Streamlit branding hidden (deploy button, viewer badges, footer)</li>
      </ul>
      <h3>Changed — performance</h3>
      <ul>
        <li>Theme toggle no longer clears cache (2-3x faster switching)</li>
        <li>Smooth theme transitions on cards, tables, sidebar (180ms)</li>
        <li>Sidebar collapse → smooth slide animation (was snap)</li>
      </ul>

      <h2 id="v1-0">v1.0 — initial public preview (2026-05)</h2>
      <h3>New</h3>
      <ul>
        <li><strong>Theme toggle</strong> — sun/moon icon in sidebar, light + dark modes</li>
        <li><strong>Subscription tracker</strong> — manual entry + Gmail-discovered receipts</li>
        <li><strong>AI usage analytics</strong> — Claude Code logs auto-imported, equivalent API cost vs flat plan</li>
        <li><strong>Activity tracking</strong> — foreground apps, idle-aware, auto-categorized</li>
        <li><strong>Smart auto-detect</strong> — "monthly but not charged 60+ days = probably yearly or cancelled"</li>
        <li><strong>Renewal alerts</strong> — Windows toast 3 days before bill</li>
        <li><strong>Cost spike alerts</strong> — when today exceeds 3× your average</li>
        <li><strong>Multi-currency</strong> — 30+ currencies, live ECB rates</li>
        <li><strong>Plan ROI</strong> — see what your subscription saves vs API rates</li>
        <li><strong>Streak tracker</strong> — consecutive days using AI (glow at 30+ days)</li>
        <li><strong>Cancellation savings</strong> — track lifetime $ saved when canceling unused subs</li>
        <li><strong>Smart suggestions</strong> — apps you use a lot but don't track as subscriptions</li>
        <li><strong>Undo delete</strong> — 30-second window after deleting a subscription</li>
        <li><strong>Backup + restore</strong> — auto daily, last 7 kept</li>
        <li><strong>Leaderboard preview</strong> — coming-soon teaser with 5 categories</li>
      </ul>

      <h2>Coming next</h2>
      <ul>
        <li>Cloud sync + mobile PWA (Pro)</li>
        <li>"Ask pulse" AI assistant — natural-language queries</li>
        <li>Cross-provider live: OpenAI, Cursor, Gemini, Copilot (Pro)</li>
        <li>Bank account auto-import (Plaid US, KBank/SCB TH)</li>
        <li>Receipt OCR</li>
        <li>Email weekly digest + push notifications (Pro)</li>
        <li>Friend leaderboard (5 categories, opt-in, aggregate metrics only)</li>
      </ul>
      <p>
        <a href="/#waitlist">Join the Pro waitlist</a> for early access.
      </p>
    </LegalPage>
  );
}
