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
      lastUpdated="2026-05-15"
    >
      <p>
        Building in public — every release ships with a public PR + release notes on{" "}
        <a href="https://github.com/walight999/pulse/releases" target="_blank" rel="noopener noreferrer">
          GitHub
        </a>.
      </p>

      <h2 id="v1-8">v1.8 — Cloud server runnable + PWA + ChatGPT export + macOS CI (2026-05-15)</h2>
      <p>
        Closing the remaining infra gaps. The cloud server is now bootable in one command, the
        landing is a real PWA with offline support, ChatGPT Plus exports import into the dashboard
        with a drag-and-drop ZIP, and a GitHub Actions workflow produces an unsigned macOS build on
        every push to <code>main</code>.
      </p>
      <h3>Added — runnable cloud server</h3>
      <ul>
        <li>
          <code>python -m api.server --dev --port 8000</code> boots the FastAPI server in dev mode
          (JWT signature verification bypassed; user_id derived from token sha1). Without <code>--dev</code>,
          the server requires <code>SUPABASE_JWT_SECRET</code> and verifies every request.
        </li>
        <li>
          Real HS256 JWT verification path — uses PyJWT if installed, falls back to a hand-rolled HMAC
          verifier so a basic Supabase Pro setup works with zero extra dependencies.
        </li>
        <li>
          New <code>/healthz</code> endpoint reports dev_mode + supabase_configured flags — picked up
          automatically by Fly.io / Render / Railway health checks.
        </li>
        <li>
          <strong>New <code>CLOUD_DEPLOY.md</code></strong> — step-by-step Supabase + Fly.io deploy (with fly.toml, Dockerfile.api, fly secrets set commands), alternative platform comparison table, env-var reference, cost-at-scale table.
        </li>
        <li>
          9 new pytest cases (<code>tests/test_api_server.py</code>) covering health, unauthenticated rejection, dev-mode bypass, and every <code>/v1/*</code> endpoint shape. Total tests: 51 → 60.
        </li>
      </ul>
      <h3>Added — PWA with offline support</h3>
      <ul>
        <li>
          <code>landing/public/sw.js</code> — service worker with 4 strategies: network-first for
          <code>/</code>, stale-while-revalidate for content subpages, cache-first for hashed Next
          static + brand assets, no caching for <code>/api/*</code>. Precaches the 11 main routes on
          install. Old caches evicted on activate.
        </li>
        <li>
          <strong>New <code>/offline</code> route</strong> — fallback page when the network is down
          and the user navigates to a non-cached page. Reminds the user the pulse desktop app keeps
          working without the network. Lists which pages are cached.
        </li>
        <li>
          Service worker registered from <code>layout.tsx</code> on HTTPS only (skipped in dev). Manifest
          already existed; bumping <code>CACHE_VERSION</code> in <code>sw.js</code> evicts stale assets after
          deploys.
        </li>
      </ul>
      <h3>Added — ChatGPT Plus export import</h3>
      <ul>
        <li>
          <code>sync_chatgpt_export(zip_path)</code> in <code>sync_tokens.py</code> wires the existing
          <code>parse_export_archive()</code> from <code>providers/openai_parser.py</code> into the standard
          insert pipeline. Inserts approximate token counts (1 token ≈ 4 chars) since ChatGPT exports
          don't ship token counts.
        </li>
        <li>
          Settings → Integrations → "ChatGPT Plus / Pro export importer" file-uploader. Drop the ZIP,
          pulse parses it server-side in a temp file, deletes the temp on success/failure, shows the
          count of imported messages.
        </li>
        <li>
          Integration matrix on <code>/</code>: ChatGPT Plus export moves from <em>Coming Q3 2026</em>
          to <em>Available now</em>.
        </li>
      </ul>
      <h3>Added — macOS GitHub Actions</h3>
      <ul>
        <li>
          <code>.github/workflows/build-macos.yml</code> — runs on every push to <code>main</code> that
          touches Python or build scripts. Produces an unsigned <code>.app</code> + <code>.zip</code> as
          a workflow artifact (14-day retention). Includes a GITHUB_STEP_SUMMARY explaining how to bypass
          Gatekeeper for unsigned builds.
        </li>
        <li>
          <code>release.yml</code> macOS job ungated. Was previously hidden behind an
          <code>APPLE_BUILD_ENABLED</code> secret; now runs on every release tag and attaches the
          macOS zip to the GitHub Release alongside the Windows installer. Signs only if
          <code>APPLE_DEVELOPER_ID</code> secret is set; ships unsigned otherwise.
        </li>
      </ul>

      <h2 id="v1-7">v1.7 — Multi-provider wiring + Ask pulse (2026-05-15)</h2>
      <p>
        Stop letting v1.1 scaffolding sit on disk. OpenAI + Cursor parsers were written months ago but
        never wired into the sync loop; Copilot + Gemini + the assistant tools were stubs returning
        <code>NotImplementedError</code>. This release ships them as real code so the integration matrix on
        this site stops describing aspirations and starts describing what runs.
      </p>
      <h3>Added — multi-provider sync</h3>
      <ul>
        <li>
          <strong>OpenAI <code>/v1/usage</code> sync</strong> — pulse pulls last-30-day GPT-5 / GPT-4o / o-series usage
          from your account when you paste an API key. Real pricing math from the public rate table; cache
          reads accounted for separately.
        </li>
        <li>
          <strong>Cursor IDE local parser</strong> — read-only scan of Cursor's <code>state.vscdb</code> on Windows /
          macOS / Linux. Approximate token counts from message char length; provider tagged as <code>cursor</code>.
        </li>
        <li>
          <strong>GitHub Copilot org-level sync</strong> — for org admins. Daily suggestions-made /
          suggestions-accepted / chat-turn counts via <code>/orgs/&lt;org&gt;/copilot/usage</code>, used to compute
          cost-per-accepted-suggestion against the flat seat price.
        </li>
        <li>
          <strong>Gemini API key validation</strong> — single test call confirms the key works. Google AI Studio
          has no retrospective usage endpoint, so the parser inserts no historical rows and tells you to
          install the browser extension for going-forward capture (honest, not aspirational).
        </li>
        <li>
          All four wired into <code>sync_all()</code> so they run automatically in the 6-hour background loop
          alongside the existing Claude Code log scan.
        </li>
      </ul>
      <h3>Added — Ask pulse assistant</h3>
      <ul>
        <li>
          <strong>New <em>Ask pulse</em> sidebar nav item.</strong> Natural-language Q&A against your local data,
          powered by Anthropic Messages API + tool-use. User pastes their own Anthropic key in Settings;
          pulse calls Anthropic directly, never proxies through a pulse server.
        </li>
        <li>
          5 tool functions implemented in <code>assistant/tools.py</code>: <code>query_subscriptions</code>,
          <code>query_token_usage</code>, <code>compute_savings</code>, <code>predict_monthly_total</code>,
          <code>activity_summary</code>. All run read-only SQL against local SQLite — no writes, no uploads.
        </li>
        <li>
          Multi-turn chat history persisted in session_state with a "Clear conversation" reset. Quick-action
          buttons for the 3 most common questions (top subscriptions, AI spend last 30d, EOM forecast).
          Tool-call log surfaced in an expander so you can see exactly what Claude queried.
        </li>
        <li>
          Up to 4 tool-use round-trips per question to keep cost bounded. System prompt instructs Claude
          to cite specific numbers from tool output rather than guessing.
        </li>
      </ul>
      <h3>Added — Settings → Provider API keys</h3>
      <ul>
        <li>Anthropic API key field repurposed to power Ask pulse (in addition to Admin sync).</li>
        <li>GitHub Copilot org PAT + org slug fields added for Copilot sync.</li>
        <li>Mistral field tagged as planned (parser still pending Q3).</li>
      </ul>
      <h3>Changed — website</h3>
      <ul>
        <li>
          Integration matrix on <code>/</code>: 7 rows now <strong>Available now</strong> (Claude Code, Anthropic
          Admin API, OpenAI API, Cursor, Copilot org, browser extension, Ask pulse), 1 Coming Q3 (ChatGPT
          Plus export), 2 Planned (Gemini retrospective — Google API limitation, Mistral).
        </li>
        <li>
          <code>/roadmap</code> "Now" column expanded from 12 to 17 items. "Next" column slimmed to ship-able
          Q3 work only (cloud sync, mobile PWA, ChatGPT Plus export, Mistral, leaderboard, Stripe).
        </li>
      </ul>

      <h2 id="v1-6">v1.6 — Website audit + privacy plumbing (2026-05-15)</h2>
      <p>
        Five-phase audit of the website and end-to-end privacy plumbing. Site shipped from "explains
        the vision well" to "honest about what's live today." Activity-tracking consent is now true
        end-to-end, not just a marketing claim.
      </p>
      <h3>Phase 1 — Honesty</h3>
      <ul>
        <li>
          Lifetime Pro defused to an interest-list with no commercial promise — removed "first 500",
          "$199", and "every future Pro feature through v9.x". Final terms will be published before
          any sale.
        </li>
        <li>Pricing tiers got <code>Available now</code> / <code>Coming Q3 2026</code> / <code>Roadmap</code> badges. CTAs softened on unreleased tiers.</li>
        <li>New "What you can use today" 3-column section above Screenshots.</li>
        <li>Pricing comparison matrix gained a Status column tagging every row.</li>
        <li>
          <code>/security</code> page: top status-legend callout + per-claim badges (Implemented · local
          mode / Designed for Pro / Planned for Team / Enterprise roadmap / Not certified yet). New
          "Service-level claims" section says no SLA today.
        </li>
        <li>Operator name and governing law (Thai law, Bangkok) added to footer and <code>/terms</code>.</li>
      </ul>
      <h3>Phase 2 — Activation</h3>
      <ul>
        <li>
          <strong>New <code>/download</code> page</strong> — OS card matrix, 4-step install walkthrough, data-location table,
          run-from-source snippet, troubleshooting accordion, SHA-256 verification guidance.
        </li>
        <li>
          <strong>New <code>/methodology</code> page</strong> — Plan ROI formula, equivalent API value breakdown, full
          Anthropic pricing table from <code>sync_tokens.py</code>, cache TTL explainer, cost-per-active-hour formula,
          cancellation savings formula, exact-vs-estimate table, honest limitations section.
        </li>
        <li>
          Waitlist form gained optional segmentation: persona, OS, AI tools, monthly spend, plan
          interest, biggest pain. Success state replaced with a 3-step next-steps card + personal
          referral link.
        </li>
      </ul>
      <h3>Phase 3 — Credibility</h3>
      <ul>
        <li>
          New Personas section: 5 cards — Solo AI users / Developers / Founders + Operators / Teams (Q3) /
          Finance + Ops — each with persona-specific jobs-to-be-done and tailored CTAs.
        </li>
        <li>
          New Integrations matrix: per-provider table (Claude Code, Anthropic Admin API, OpenAI, ChatGPT
          Plus, Cursor, Gemini, Copilot, Browser extension) with Status / Data source / Accuracy / Notes.
        </li>
        <li>
          Self-host vs hosted comparison added at the top of Pricing — 5 rows distinguishing Local Free /
          Self-host Cloud / Pro Hosted / Team Hosted / Enterprise.
        </li>
        <li>
          <strong>New <code>/roadmap</code> page</strong> — public Now / Next / Later / Under consideration board with
          vote-via-Discussions CTA.
        </li>
      </ul>
      <h3>Phase 4 — Plumbing</h3>
      <ul>
        <li>
          <code>/api/waitlist</code> made pluggable. If <code>SUPABASE_URL</code> + <code>SUPABASE_SERVICE_ROLE_KEY</code> are set,
          inserts to a <code>waitlist</code> table. If <code>RESEND_API_KEY</code> is set, sends a plain-text confirmation email
          with the user's referral link. Both opt-in; falls back to Vercel logs if not configured.
          UTM + referral params (<code>utm_source</code>, <code>utm_medium</code>, <code>utm_campaign</code>, <code>r</code>) now captured.
        </li>
        <li>
          New <code>landing/WAITLIST_SETUP.md</code> with the Supabase SQL schema + Resend domain verification +
          Vercel env-var table.
        </li>
        <li>
          <strong>First-run onboarding wizard expanded</strong>: from 4 sections to 7. Auto-detects Claude
          Code logs at <code>~/.claude/projects/*.jsonl</code>, asks for explicit activity-tracking + window-title
          consent (both default OFF), shows where your data lives, optional demo-data seed (4 example
          subscriptions you can poke around with).
        </li>
        <li>
          New Settings → Preferences → "Privacy & activity tracking" section: master tracking toggle,
          store-titles toggle, allowlist + blocklist (semicolon-separated), pause buttons (1h / until
          tomorrow / 1 week), export activity CSV, delete activity history. Plus a "Danger zone" expander
          for full local-data wipe with type-DELETE confirmation.
        </li>
        <li>
          <strong>Tracker honors privacy settings end-to-end</strong>. <code>tracker.py</code> refreshes settings every
          60 seconds. If tracking is off or paused, no rows are inserted at all. If window-title storage
          is off, the title column is always empty. Allowlist takes precedence over blocklist when both
          are set.
        </li>
      </ul>
      <h3>Phase 5 — Polish + production readiness</h3>
      <ul>
        <li>Trust strip below Hero: 100% local · MIT open-source · no telemetry · 1 outbound call · no account.</li>
        <li>
          <strong>New <code>/docs</code> hub</strong> — 9 sections × 4 cards each. Quickstart, importing data, privacy & security,
          backup + export + data location, self-hosting, how pulse calculates things, security model,
          troubleshooting, FAQ by audience (developer / non-technical / founder / privacy-conscious).
        </li>
        <li>
          CSS safety rules applied verbatim from the website brief — <code>box-sizing: border-box</code>,
          <code>overflow-x: clip</code> on html/body, <code>overflow-wrap: break-word</code> on text elements,
          <code>word-break: anywhere</code> on code paths. No horizontal scroll at 320–1440px.
        </li>
        <li>
          Accessibility: skip-to-content link at the top of <code>/</code>, <code>:focus-visible</code> mint outline on
          every interactive element, <code>prefers-reduced-motion</code> media query that disables the ECG animation
          for users who set the OS preference.
        </li>
        <li>
          Vercel Analytics added (<code>@vercel/analytics</code>). Privacy-safe by default — no cookies, no PII.
          Disabled at build time via <code>NEXT_PUBLIC_ANALYTICS_DISABLED=1</code> if you don't want it.
        </li>
      </ul>
      <h3>Phase 6 — Interactive demo + SEO landing variants</h3>
      <ul>
        <li>
          <strong>New <code>/demo</code></strong> — interactive client page with persona toggle (Solo / Developer / Founder),
          synthetic-but-realistic subscriptions and token usage, all metrics computed live from the same
          formulas as the real app. Plan ROI / equivalent API value / cost per active hour / cancellation
          savings update instantly when you switch persona. "Demo data only — your real data stays local"
          banner at the top. Downloadable sample CSV.
        </li>
        <li>
          <strong>New <code>/alternatives</code></strong> — honest 800-word comparison hub against ClaudeMetrics,
          Anthropic Console, OpenAI Usage, Vantage, Pry/Cledara, Mint (shut down 2024), YNAB, Lunch Money,
          Actual Budget. Includes "where pulse is genuinely worse" section (no shared dashboards today,
          Claude-first parser coverage, no bank auto-sync). Quick-pick guide table at the bottom.
        </li>
        <li>
          <strong>New <code>/compare/claude-code-cost-tracker</code></strong> — focused SEO landing for the highest-intent
          search term. Explains the cache TTL 5m/1h pricing math, why most cost trackers are off by 10-60%,
          and the local-parser-no-upload advantage.
        </li>
        <li>
          <strong>New <code>/compare/cursor-cost-tracker</code></strong> — Cursor-specific landing. Tells the truth about
          what's available now (subscription cost + foreground time + cost-per-hour) vs Q3 2026 (per-request
          token breakdown from Cursor's local state DB).
        </li>
        <li>
          Sample CSV file at <code>/samples/pulse-sample-export.csv</code> — same column structure as the real export,
          populated with the demo persona's data.
        </li>
        <li>Hero CTA simplified to <em>Download pulse</em> + <em>Try interactive demo</em> (the demo replaces "View on GitHub" as the secondary action — GitHub stays in the header).</li>
        <li>Footer Product column + nav (desktop and mobile) updated for all 4 new routes. Sitemap priorities set.</li>
      </ul>
      <h3>Build verification</h3>
      <p>
        pytest 51/51 pass. Next 14.2.35 build clean (<strong>20 routes static</strong> at the end of Phase 6).
        <code>/</code> at 115 kB First Load JS. <code>/demo</code> at 100 kB (client-side React for the persona toggle).
        Every other subpage under 97 kB.
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
