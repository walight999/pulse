# Pulse E2E tests (Playwright)

End-to-end tests covering the landing page (Next.js) and dashboard (Streamlit).

## Install

```bash
cd tests/e2e
npm install
npx playwright install chromium
```

## Run

```bash
# Both — assumes both servers running
npm test

# Landing only (requires Next.js dev server)
cd ../../landing && npm run dev &
cd ../tests/e2e && npm run test:landing

# Dashboard only (requires Streamlit running)
cd ../../ && python app.py &
cd tests/e2e && npm run test:dashboard

# Interactive UI mode for debugging
npm run test:ui
```

## Environment overrides

```bash
PULSE_LANDING_URL=https://mintforai.com npm run test:landing
PULSE_DASHBOARD_URL=http://192.168.1.5:8501 npm run test:dashboard
```

## What's tested

### Landing (`specs/landing.spec.ts`)

- Title + brand wordmark
- Nav (Features / Pricing / GitHub / waitlist CTA)
- Compare table (vs ClaudeMetrics + Anthropic Console)
- Pricing tiers visible
- Waitlist form validates email
- Favicon + OG meta tags
- Footer links
- ECG line animation (brand signature)
- Page loads under 3s

### Dashboard (`specs/dashboard.spec.ts`)

- Page title
- Sidebar shows brand + 5 nav items
- Brand mark is inline SVG (not CSS pseudo) — regression test
- Overview greeting + ECG line
- Theme toggle present
- Settings has exactly 3 tabs (Advanced removed)
- No "Made with Streamlit" / Deploy button visible
- AI usage ROI hero shows at top of page

## CI integration

GitHub Actions can run these on `landing/` changes:

```yaml
# Add to .github/workflows/ci.yml
landing-e2e:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: 20
        cache: npm
        cache-dependency-path: tests/e2e/package-lock.json
    - run: cd tests/e2e && npm ci
    - run: cd tests/e2e && npx playwright install --with-deps chromium
    - run: cd landing && npm ci && npm run build && npm run start &
    - run: sleep 5
    - run: cd tests/e2e && npm test
```

## Notes

- Tests are intentionally permissive on edge cases (e.g., AI usage tests
  pass even if no token data) to avoid flakiness on fresh installs
- Dashboard tests target our custom CSS classes (`.pulse-brand-row`,
  `.pulse-ecg-line`) — these are stable across versions
- Landing tests are stricter because Next.js + Tailwind output is more
  deterministic than Streamlit DOM
