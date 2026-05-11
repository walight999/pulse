# 🎨 Pulse — Brand

## Identity

**Name**: pulse (always lowercase wordmark)
**Tagline**: Mint for the AI era.
**One-line**: Local-first personal-finance dashboard for the AI era.
**Voice**: Confident, local-first, numbers-focused.

## Brand tokens (Brand Core v1)

| Token | Hex | Use |
|-------|-----|-----|
| `INK` | `#0A0A0F` | Primary dark surface |
| `INK_SOFT` | `#17171C` | Card surface (dark) |
| `PAPER` | `#FAFAF7` | Light surface, dark-mode text |
| `PULSE` | `#00E5A0` | Vivid mint accent (dark bg) |
| `PULSE_dim` | `#00C58A` | AA-safe variant (light bg) |
| `SLATE` | `#6B6B6B` | Muted text |

## Typography

- **Display**: Inter Tight (weight 500 + 600), letter-spacing -0.035em
- **Mono**: JetBrains Mono (weight 400)
- **Tabular numerics**: `font-variant-numeric: tabular-nums` for all financial figures

## Logomark

- Black rounded square (radius 18%)
- White "P" centered, bold, letter-spacing -0.04em
- Mint pulse line (`PULSE`) crossing horizontally through P at ~55% height
- Glow shadow on pulse line: `0 0 8px rgba(52,211,153,0.7)`

Variants (in `pulse-brand-core/output/01-logomark/`):
- `pulse-mark--master.svg` — default (dark contexts)
- `pulse-mark--mono-white.svg` — single-color overlays on photos
- `pulse-mark--mono-black.svg` — print, single-ink
- `pulse-mark--solid-green.svg` — T-shirts, stickers
- `pulse-mark--transparent-white.svg` — overlay on any surface
- `pulse-mark--transparent-ink.svg` — ink-color overlay

## Voice and tone

### Three forces (cannot drop one without slipping)

1. **Confident** — we know the data, we show the data
2. **Local-first** — privacy + ownership baked in
3. **Numbers-focused** — specific savings figures, not vague benefits

### Do's

- ✓ Lowercase "pulse" wordmark in every reference
- ✓ Specific dollar/baht savings ("$4,300", "฿18,500")
- ✓ Acknowledge trade-offs honestly ("Windows-only today, macOS coming")
- ✓ Tabular numerics for all financial values
- ✓ "Mint for the AI era" tagline in marketing
- ✓ Animated ECG pulse line as decorative element (left-to-right only)
- ✓ Capital sentence case for headers, lowercase for navigation

### Don'ts

- ✗ Capital "P" in body copy ("Pulse" → "pulse")
- ✗ Vague benefits ("save money" — use specific number)
- ✗ AI buzzwords ("AI-powered", "intelligence", "revolutionary")
- ✗ Comparison shaming ("unlike ClaudeMetrics" — compare honestly, don't trash)
- ✗ Emoji walls (max 1 emoji per section, prefer text symbols ★ ✓ →)
- ✗ Right-to-left ECG animation (always left-to-right, like a heart monitor)
- ✗ Reproduction of mark below 16px height (illegible)
- ✗ Stretch, skew, rotation of mark
- ✗ Recolor outside the 4 brand colors
- ✗ Mixing Inter Tight with another sans-serif in the same lockup

## Visual language

### ECG pulse line

The signature visual element. A horizontal line with a heartbeat waveform in mint (`PULSE`).
Used:
- Below H1 greeting on Overview page (`dashboard.py`)
- Between hero sections on landing page
- In email templates as a section divider
- As subtle decoration in OG cards

Animation: `pulse-ecg-flow` keyframe, 6-second loop, left-to-right.
Disable for users with `prefers-reduced-motion: reduce`.

### Stars (★)

5-star rating in Plan ROI hero card. Filled stars in mint, empty in `border-strong`.
Used only in ROI hero — not generic decoration.

### Clear space

Logomark: at least 0.25× its width of clear space on all sides.
Wordmark: at least its cap height of clear space below.

## Tagline variants

Default: **"Mint for the AI era."**

Variants by context:
- Twitter bio: "Mint for the AI era · Local-first · MIT"
- Email signature: "Mint for the AI era — pulse.app"
- GitHub repo description: "Mint for the AI era. Local-first personal-finance dashboard for AI subscriptions, Claude tokens, and focused work."
- HN title: depends on angle (see `operations/marketing/hn-faq-bank.md`)

## Headline writing rules

Hero headlines should always:
1. Lead with a specific dollar amount
2. Show a ratio (`X×`, `Y%`, `+Z`)
3. Use "you" or "your" (second person, direct)

Examples:
- ✓ "Prove your $200 Claude plan returns $4,000 in API value."
- ✓ "You saved $4,300 by cancelling 7 subs."
- ✓ "10.5× return on plan cost this month."
- ✗ "The smartest AI cost tracker" (vague, no number)
- ✗ "Track your AI spending" (passive, no benefit)
- ✗ "Our advanced analytics" (no specificity)

## Brand asset inventory

Located in `static/brand/` and `pulse-brand-core/output/`:

| Asset | Location | Use |
|-------|----------|-----|
| `logomark.svg` (master) | static/brand/ | Default mark |
| `logomark-mono-white.svg` | static/brand/ | Photo overlays |
| `logomark-mono-black.svg` | static/brand/ | Print |
| `logomark-solid-green.svg` | static/brand/ | Brand-color contexts |
| `logomark-transparent-white.png` | static/brand/ | Overlay use |
| `wordmark.svg` | static/brand/ | Standalone wordmark |
| `app-icon.png` (256px) | static/brand/ | Streamlit favicon |
| `apple-touch-icon.png` (180px) | static/brand/ | iOS home screen |
| `icon-192.png` / `icon-512.png` | static/brand/ | PWA install |
| `icon-512-maskable.png` | static/brand/ | Android adaptive |
| `favicon-32.png` + `favicon.ico` | static/brand/ | Browser tab |
| `github-social-preview.png` | static/brand/ | GitHub repo Settings |
| `og-social-card.png` (1200×630) | static/brand/ | Open Graph |
| `lockup-horizontal-dark.png` | static/brand/ | README hero, navbar |
| `browser-mockup-clean.svg/.png` | static/brand/ | Product mockup |
| `hero-illustration.png` | static/brand/ | Marketing pages |

Full library: `pulse-brand-core/output/` (42 assets)
Distributable: `pulse-brand-core/pulse-brand-core-v1.zip`

## Regenerate brand assets

```bash
cd pulse-brand-core
python scripts/generate_brand_core.py
```

Phases 1-11 produce the full 42-asset library deterministically.
