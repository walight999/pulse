# 🎨 Pulse MVP — UX/UI specification

**Status**: v1.5 shipped
**Design system**: see `business/02-brand.md`

---

## 1. Information architecture

Single-window app with 5 primary pages:

```
┌─────────────────────────────────────────────────────┐
│ Sidebar (250px fixed)        │ Main view             │
│                              │                       │
│ [P] pulse  ☾                │ ─── page header ───   │
│ Mint for the AI era          │                       │
│                              │ ─── ECG line ───      │
│ • Overview      ← active     │                       │
│ • Subscriptions              │ ─── content ───       │
│ • Activity                   │                       │
│ • AI usage                   │                       │
│                              │                       │
│ ─── SUMMARY ───              │                       │
│ Real monthly:    ฿4,289      │                       │
│ Likely wasted:   ฿250        │                       │
│ Stack health:    ━━━━ 86%    │                       │
│                              │                       │
│ ─── Settings ───             │                       │
└─────────────────────────────────────────────────────┘
```

## 2. Five pages

### Page 1: Overview (default)

**Purpose**: At-a-glance status. The page users see daily.

**Sections (top to bottom)**:
1. Greeting + streak chip + animated ECG line
2. Plan ROI hero card (5-tier rating, big number)
3. KPI strip (4 cards: Monthly, AI this month, App hours, Likely wasted)
4. Two-column: Upcoming renewals + Insights
5. Lifetime savings (shimmer pill if cancellations exist)

**Key interactions**:
- ROI hero card click → AI usage page
- Renewal item click → Subscriptions page (filtered by name)
- Streak chip glow at 30+ days

### Page 2: Subscriptions

**Purpose**: Manage every recurring AI service.

**Sections**:
1. Page header with "+ Add subscription" action button
2. KPI strip (Monthly, Yearly, Need attention, Likely wasted)
3. Search + filter chips (Active / Attention / Off? / History / All)
4. Subscription cards with status stripes + actions
5. CSV import dialog (collapsible)
6. Tips footer

**Card layout**:
```
┌─────────────────────────────────────────────────┐
│|│ Netflix                          $15.99/mo    │
│|│ Active monthly · last 12d ago     paid $... USD│
│|│ ━━━━━━━━━━━━━━░░░░░░ 65% through cycle        │
│|│ Notes: business expense                       │
│  └─ [Edit] [Delete] [Cancel] [Confirm]         │
└─────────────────────────────────────────────────┘
```

Status stripes (left edge, gradient):
- Green → accent: healthy active
- Amber → green: needs attention
- Red → amber: likely wasted
- Blue: cost-not-set
- Gray: history

### Page 3: Activity

**Purpose**: Where your time goes.

**Sections**:
1. Page header + range slider
2. KPI strip (Apps tracked, Total hours, Most used)
3. Two-column: By category table + Top apps list
4. Top apps inline legend (Productive / Distraction swatches in header row)

**Top apps list layout**:
```
Top apps              ⬤ Productive  ⬤ Distraction
┌────────────────────────────────────────────────┐
│ 1  VS Code              ━━━━━━━━━━     12.3h  │
│    Development                          15 sess│
│ 2  Chrome               ━━━━━━           8.1h  │
│    Browser                              42 sess│
│ 3  Slack                ━━━              4.3h  │
│    Distraction                          28 sess│
└────────────────────────────────────────────────┘
```

### Page 4: AI usage

**Purpose**: Real ROI on AI spending.

**Sections**:
1. Page header with "Sync now" action
2. Plan ROI hero (moved to top per user preference)
3. Time-period tabs (Today / This month / All time)
4. KPI strip (Cost, Messages, Avg per active bucket)
5. Forecast banner (month tab only)
6. Tokens KPI row (Input, Output, Cache create, Cache read)
7. Time-series chart (themed bars, color by % budget)
8. 7×24h heatmap (mint intensity gradient)
9. By model + By project tables (matched height, scrollable)
10. Leaderboard preview card

### Page 5: Settings

**Purpose**: Configuration without overwhelming.

**Tabs**:
- Preferences (theme, currency, plan cost, alerts)
- Pulse Pro (waitlist signup, referrals, account info)
- Data & backup (manual backup, restore, export CSV/PDF, sync log)
- Advanced (pricing mode, app categories, diagnostics)

## 3. Design tokens

See `business/02-brand.md` for the full token spec.

Key for UX consistency:

| Token | Value | Use |
|-------|-------|-----|
| Border radius | 8px | Cards, buttons |
| Border radius (large) | 14px | Hero cards |
| Border radius (pill) | 999px | Chips, badges |
| Spacing unit | 4px | Multiples for padding/margin |
| Standard padding | 14-16px | Cards, sections |
| Form padding | 20-22px | Form containers |
| Animation duration | 0.15-0.28s | Transitions |
| Animation easing | cubic-bezier(0.4,0,0.2,1) | Smooth slide |

## 4. Component library

### KPI card (`kpi_card()` in dashboard.py)

```
┌─────────────────────────┐
│ LABEL                   │  ← 0.7rem uppercase
│ ฿4,289                  │  ← 1.2rem bold tabular
│ ($121.32)               │  ← 0.72rem secondary
└─────────────────────────┘
```

Variants by tint:
- default · warning · danger · success · accent

### Pulse table (`pulse_table()` in dashboard.py)

Replaces Streamlit's dataframe where full theming is required (Glide grid doesn't follow CSS vars). Used in:
- Activity → By category
- AI usage → By model
- AI usage → By project

### Empty state (`pulse_empty()` in dashboard.py)

```
┌─────────────────────────────────┐
│         ┌────┐                  │
│         │ 📅 │  ← SVG icon      │
│         └────┘                  │
│                                 │
│       Quiet ahead               │
│  No renewals in 2 weeks         │
└─────────────────────────────────┘
```

5 icons: calendar / no-activity / search / no-data / inbox.

### Sub-card

Subscription cards with gradient left-stripe based on status. See "Page 2: Subscriptions" above.

### Pulse Pro tier card

Pricing card with "Most popular" badge on Pro tier. 4-column grid on landing page.

## 5. Theme system

Light + dark mode via CSS variables. Toggle via Material icon (sun/moon) in sidebar header.

**Implementation**: `theme.py` outputs `<style>` block with CSS custom properties (`--bg-primary`, `--accent`, etc.). Theme switch sets a single setting + reruns. No cache clear (180ms transition instead of full re-render).

**Tokens for dark mode**:
- Background: `#0A0A0F` (INK)
- Text: `#FAFAF7` (PAPER)
- Accent: `#00E5A0` (PULSE)
- Cards: `#17171C` (INK_SOFT)

**Tokens for light mode**:
- Background: `#FAFAF7` (PAPER)
- Text: `#0A0A0F` (INK)
- Accent: `#00C58A` (PULSE_dim, AA-safe)
- Cards: `#FFFFFF` (white)

## 6. Animations

| Animation | Duration | Easing | Purpose |
|-----------|---------|--------|---------|
| `pulse-app-fade-in` | 0.22s | ease-out | Page render |
| `pulse-page-enter` | 0.28s | cubic-bezier(0.4,0,0.2,1) | Nav switch |
| Theme transition | 0.18s | ease | Color shift on toggle |
| Sidebar fold | 0.28s | cubic-bezier(0.4,0,0.2,1) | Collapse handle slide |
| `pulse-streak-glow` | 2.4s | ease-in-out infinite | Streak chip ≥30 days |
| `pulse-ecg-flow` | 6s | linear infinite | ECG line decoration |
| `pulse-savings-shimmer` | 9s | linear infinite | Lifetime savings card |
| `pulse-logo-shift` | 14s | ease-in-out infinite | Logomark gradient shift |
| `pulse-loading-bar` | 1.4s | cubic-bezier(0.4,0,0.2,1) infinite | Top progress bar |
| `pulse-spin` | 0.8s | linear infinite | Spinner |

All animations respect `prefers-reduced-motion: reduce`.

## 7. Accessibility

- **Color contrast**: AA minimum (4.5:1 for text, 3:1 for large text). `PULSE_dim` (#00C58A) is the AA-safe accent on light backgrounds.
- **Focus rings**: 2px solid `var(--accent)` with 2px offset on all interactive elements.
- **Keyboard**: All nav + actions accessible via Tab.
- **Reduced motion**: All animations disabled via media query.
- **Screen readers**: alt text on icons, aria-label on icon-only buttons.

## 8. Responsive design

| Breakpoint | Behavior |
|------------|----------|
| ≥1140px | Full desktop layout (4-col KPI strip, 2-col Renewals+Insights) |
| 700-1140px | Stack KPI cards 2×2, keep 2-col panels |
| <700px | Sidebar overlays (z-index 100, fixed position), all columns stack 1-up |

PWA mobile uses standalone display mode + theme-color meta + apple-touch-icon. Service worker provides offline cache (Phase 2).

## 9. Mobile-specific (PWA, Phase 2)

- Bottom nav instead of sidebar
- Swipe to switch tabs
- Pull-to-refresh on Overview
- Push notifications for renewals + spend spikes
- Add to home screen via manifest.json
- Offline-first: cached shell + last-synced data

## 10. Brand voice in copy

Examples from current app:

✓ "You're crushing it — 10.5× return on the plan."
✓ "You saved ฿18,500 by cancelling 3 subs since starting Pulse."
✓ "Quiet ahead — no renewals in 2 weeks."

✗ Avoid: "Welcome to your dashboard!" (generic, no specificity)
✗ Avoid: "Awesome insights powered by AI" (buzzy)
✗ Avoid: "Click here to optimize your subscriptions" (passive)

Every piece of UI copy should pass the test: **Can a user predict what number/result they'll see when they click this?**
