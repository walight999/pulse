# Pulse Brand Core v1 — build spec (executable)

This folder is a self-contained brand asset generator. Run:

```bash
cd pulse-brand-core
pip install pillow numpy            # required
pip install cairosvg                # optional but recommended
python scripts/generate_brand_core.py
```

## Outputs (35+ files)

- `output/01-logomark/` — master + mono-white + mono-black + solid-green (SVG + PNG)
- `output/02-lockups/` — horizontal × vertical × light/dark (SVG + PNG)
- `output/03-wordmark/` — lowercase wordmark (SVG + PNG)
- `output/04-icons/` — favicon set, Apple touch, Android adaptive, PWA, app icons 64–1024
- `output/05-social/` — GitHub preview, OG default, Twitter card
- `output/06-reference/` — final-form copies of the 5 source brand images
- `output/README.md` — brand do's / don'ts / file guide
- `pulse-brand-core-v1.zip` — distributable package

## Constants (do not deviate)

```python
INK      = "#0A0A0F"
INK_SOFT = "#17171C"
PAPER    = "#FAFAF7"
PULSE    = "#00E5A0"
```

## Differences vs the original spec

| Original spec | This implementation | Why |
|---------------|--------------------|------|
| `vtracer` for vectorization | Hand-coded master SVG | Deterministic, < 2KB, < 1s, no external CLI |
| Playwright HTML→PNG for social | Hand-built SVG → PNG | No chromium download, no font loading wait |
| `fonttools` glyph outlining | `<text>` with system font fallback | Inter Tight not bundled (caveat) |
| `cairosvg` required | Optional (Pillow fallback) | Works without cairo install |

## Optional upgrades

For pixel-perfect typography in lockups / social cards, install Inter Tight + JetBrains Mono into `fonts/`:

```bash
# Linux/macOS
curl -L "https://fonts.gstatic.com/s/intertight/v8/NaNZepOXO_NexZs0b5QrzlOHb8wA.woff2" -o fonts/InterTight-Medium.woff2
curl -L "https://fonts.gstatic.com/s/intertight/v8/NaNZepOXO_NexZs0b5QrzlOHb8wA.woff2" -o fonts/InterTight-SemiBold.woff2

# Or via google-fonts-downloader
pip install google-fonts-downloader
google-fonts-downloader "Inter Tight:500,600" --output fonts/
google-fonts-downloader "JetBrains Mono:400" --output fonts/
```

Then re-run `python scripts/generate_brand_core.py`.
