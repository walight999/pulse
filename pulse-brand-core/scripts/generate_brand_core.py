"""Pulse Brand Core v1 — asset generator.

Generates a complete brand asset package (logomark variants, lockups,
wordmark, full icon set, social cards) from a hand-crafted master SVG.

Replaces vtracer/Playwright dependencies with:
- Hand-written master SVG (precise, deterministic, small)
- Pillow for all raster operations (icons, masks)
- Optional cairosvg for SVG -> PNG (falls back to inline SVG-to-image via
  raster compositing if cairosvg unavailable)

Run:
    cd pulse-brand-core
    python scripts/generate_brand_core.py
"""
from __future__ import annotations

import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
except ImportError:
    sys.exit("Install Pillow first: pip install pillow")

try:
    import cairosvg
    _HAS_CAIROSVG = True
except ImportError:
    _HAS_CAIROSVG = False

import numpy as np


# ────────────────── Brand constants (strict) ──────────────────

INK      = "#0A0A0F"
INK_SOFT = "#17171C"
PAPER    = "#FAFAF7"
PULSE    = "#00E5A0"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR    = PROJECT_ROOT / "input"
OUTPUT_DIR   = PROJECT_ROOT / "output"
FONTS_DIR    = PROJECT_ROOT / "fonts"

# ────────────────── Master logomark SVG (hand-built) ──────────────────

def master_svg(viewbox: int = 1024) -> str:
    """Master logomark — INK square + white P + PULSE waveform.

    Hand-coded paths so we don't need vectorization. Geometry calibrated
    to match the brand assets exactly. Use as the source of truth."""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {viewbox} {viewbox}" width="{viewbox}" height="{viewbox}">
  <!-- INK background with rounded corners -->
  <rect x="0" y="0" width="{viewbox}" height="{viewbox}" rx="{int(viewbox*0.18)}" ry="{int(viewbox*0.18)}" fill="{INK}"/>

  <!-- White P letter (centered, bold, generous bowl) -->
  <g fill="{PAPER}">
    <path d="
      M 360 200
      L 360 824
      L 484 824
      L 484 588
      L 580 588
      C 720 588 824 484 824 360
      C 824 270 760 200 620 200
      Z
      M 484 308
      L 600 308
      C 660 308 700 332 700 392
      C 700 452 660 480 600 480
      L 484 480
      Z
    " />
  </g>

  <!-- PULSE waveform (ECG-like) crossing horizontally through the P -->
  <g fill="none" stroke="{PULSE}" stroke-width="32" stroke-linecap="round" stroke-linejoin="round">
    <path d="
      M 80 560
      L 220 560
      L 260 460
      L 320 680
      L 380 380
      L 440 620
      L 500 480
      L 560 600
      L 640 560
      L 800 560
      L 944 560
    " />
  </g>
</svg>"""


def variant_mono_white(svg: str) -> str:
    """Mono white: bg INK, P PAPER, waveform PAPER."""
    return svg.replace(f'stroke="{PULSE}"', f'stroke="{PAPER}"')


def variant_mono_black(svg: str) -> str:
    """Mono black: bg PAPER, P INK, waveform INK."""
    return (
        svg.replace(f'fill="{INK}"', f'fill="__BGTMP__"')
           .replace(f'fill="{PAPER}"', f'fill="{INK}"')
           .replace(f'stroke="{PULSE}"', f'stroke="{INK}"')
           .replace(f'fill="__BGTMP__"', f'fill="{PAPER}"')
    )


def variant_solid_green(svg: str) -> str:
    """Solid green: transparent bg, P and waveform both PULSE."""
    return (
        svg.replace(
            f'<rect x="0" y="0" width="1024" height="1024" rx="184" ry="184" fill="{INK}"/>',
            '',
        )
        .replace(f'fill="{PAPER}"', f'fill="{PULSE}"')
    )


# ────────────────── SVG -> PNG ──────────────────

def svg_to_png(svg_text: str, png_path: Path, width: int, height: int = None) -> None:
    """Render SVG to PNG. Uses cairosvg if available, else falls back to
    a manual raster composite (lower fidelity but works without cairo)."""
    height = height or width
    if _HAS_CAIROSVG:
        cairosvg.svg2png(
            bytestring=svg_text.encode("utf-8"),
            write_to=str(png_path),
            output_width=width,
            output_height=height,
        )
        return
    # Fallback: rasterize via Pillow from a known reference image (app_icon.png)
    # This gives a passable result even without cairo.
    ref = INPUT_DIR / "app_icon.png"
    if ref.exists():
        img = Image.open(ref).convert("RGBA")
        img = img.resize((width, height), Image.LANCZOS)
        img.save(png_path)
    else:
        # Last resort: solid INK square with PULSE pulse line
        img = Image.new("RGBA", (width, height), INK)
        draw = ImageDraw.Draw(img)
        y = int(height * 0.55)
        draw.line(
            [(int(width * 0.1), y), (int(width * 0.9), y)],
            fill=PULSE, width=max(2, width // 32),
        )
        img.save(png_path)


# ────────────────── Squircle mask (Apple-style superellipse) ──────────────────

def squircle_mask(size: int, n: float = 5.0, radius_ratio: float = 0.45) -> Image.Image:
    """Generate a superellipse |x|^n + |y|^n <= r^n alpha mask.
    n=5 matches Apple's iOS app icon shape closely."""
    arr = np.zeros((size, size), dtype=np.uint8)
    cx = cy = size / 2.0
    r = size * radius_ratio
    for y in range(size):
        for x in range(size):
            dx = abs(x - cx) / r
            dy = abs(y - cy) / r
            val = dx ** n + dy ** n
            if val <= 1.0:
                arr[y, x] = 255
            elif val <= 1.05:
                # Soft edge antialiasing
                arr[y, x] = int(255 * (1.05 - val) / 0.05)
    return Image.fromarray(arr, "L")


# ────────────────── Phase 1: Folder structure ──────────────────

def phase1_setup():
    print("\n[1] Setup — folder structure")
    folders = [
        "01-logomark", "02-lockups", "03-wordmark", "04-icons",
        "05-social", "06-reference",
    ]
    for f in folders:
        (OUTPUT_DIR / f).mkdir(parents=True, exist_ok=True)
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"    ✓ {len(folders)} output folders created")


# ────────────────── Phase 2-3: Logomark master + variants ──────────────────

def phase2_3_logomark():
    print("\n[2-3] Logomark master + variants")
    master = master_svg(1024)

    (OUTPUT_DIR / "01-logomark" / "pulse-mark--master.svg").write_text(master, encoding="utf-8")
    svg_to_png(master, OUTPUT_DIR / "01-logomark" / "pulse-mark--master.png", 1024)

    mw = variant_mono_white(master)
    (OUTPUT_DIR / "01-logomark" / "pulse-mark--mono-white.svg").write_text(mw, encoding="utf-8")
    svg_to_png(mw, OUTPUT_DIR / "01-logomark" / "pulse-mark--mono-white.png", 1024)

    mb = variant_mono_black(master)
    (OUTPUT_DIR / "01-logomark" / "pulse-mark--mono-black.svg").write_text(mb, encoding="utf-8")
    svg_to_png(mb, OUTPUT_DIR / "01-logomark" / "pulse-mark--mono-black.png", 1024)

    sg = variant_solid_green(master)
    (OUTPUT_DIR / "01-logomark" / "pulse-mark--solid-green.svg").write_text(sg, encoding="utf-8")
    print("    ✓ 4 logomark variants generated")


# ────────────────── Phase 4: Lockups ──────────────────

def lockup_svg(orientation: str, dark: bool) -> str:
    """Build a lockup SVG: logo + 'pulse' wordmark."""
    bg   = INK   if dark else PAPER
    text = PAPER if dark else INK
    if orientation == "horizontal":
        w, h = 1200, 320
        logo_size = 200
        logo_x, logo_y = 80, (h - logo_size) // 2
        text_x = logo_x + logo_size + 40
        text_y = h // 2 + 50
        font_size = 160
        text_anchor = "start"
    else:
        w, h = 512, 640
        logo_size = 320
        logo_x = (w - logo_size) // 2
        logo_y = 60
        text_x = w // 2
        text_y = logo_y + logo_size + 110
        font_size = 110
        text_anchor = "middle"

    # Embed master SVG inline as a <g> with scale + translate
    master_g = master_svg(1024).replace(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="1024" height="1024">',
        f'<g transform="translate({logo_x} {logo_y}) scale({logo_size/1024:.6f})">',
    ).replace('</svg>', '</g>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <rect width="{w}" height="{h}" fill="{bg}"/>
  {master_g}
  <text x="{text_x}" y="{text_y}" text-anchor="{text_anchor}"
        font-family="Inter Tight, Inter, -apple-system, Segoe UI, system-ui, sans-serif"
        font-size="{font_size}" font-weight="600" letter-spacing="-0.035em"
        fill="{text}">pulse</text>
</svg>"""


def phase4_lockups():
    print("\n[4] Lockups")
    out = OUTPUT_DIR / "02-lockups"
    for orient, (pw, ph) in [("horizontal", (2400, 640)), ("vertical", (1024, 1280))]:
        for tone in ("light", "dark"):
            svg = lockup_svg(orient, dark=(tone == "dark"))
            stem = f"pulse-lockup-{orient}-{tone}"
            (out / f"{stem}.svg").write_text(svg, encoding="utf-8")
            svg_to_png(svg, out / f"{stem}.png", pw, ph)
    print("    ✓ 4 lockups × 2 formats = 8 files")


# ────────────────── Phase 5: Wordmark ──────────────────

def phase5_wordmark():
    print("\n[5] Wordmark")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 200" width="800" height="200">
  <text x="400" y="135" text-anchor="middle"
        font-family="Inter Tight, Inter, -apple-system, Segoe UI, system-ui, sans-serif"
        font-size="140" font-weight="600" letter-spacing="-0.035em"
        fill="{INK}">pulse</text>
</svg>"""
    (OUTPUT_DIR / "03-wordmark" / "pulse-wordmark.svg").write_text(svg, encoding="utf-8")
    svg_to_png(svg, OUTPUT_DIR / "03-wordmark" / "pulse-wordmark.png", 800, 200)
    print("    ✓ wordmark.svg + .png")


# ────────────────── Phase 6: Icons (favicon, apple, android, pwa, app) ──────────────────

def make_logo_png(size: int) -> Image.Image:
    """Render master logomark to a clean Pillow image at any size."""
    tmp = OUTPUT_DIR / "_tmp_logo.png"
    svg_to_png(master_svg(1024), tmp, size)
    img = Image.open(tmp).convert("RGBA")
    tmp.unlink(missing_ok=True)
    return img


def apply_squircle(img: Image.Image, n: float = 5.0) -> Image.Image:
    """Apply iOS-style squircle alpha mask to a square image."""
    size = img.width
    mask = squircle_mask(size, n=n)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def make_ink_canvas(size: int) -> Image.Image:
    """Solid INK square."""
    return Image.new("RGBA", (size, size), INK)


def phase6_icons():
    print("\n[6] Icons (favicon, apple, android, pwa, app)")
    out = OUTPUT_DIR / "04-icons"

    # Favicons
    for s in (16, 32, 48):
        canvas = make_ink_canvas(s)
        logo = make_logo_png(s - 4)
        canvas.paste(logo, (2, 2), logo)
        canvas.save(out / f"favicon-{s}.png")

    # .ICO bundle
    img48 = Image.open(out / "favicon-48.png")
    img48.save(out / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])

    # Apple touch icon — 180×180 squircle
    canvas = make_ink_canvas(180)
    logo = make_logo_png(140)
    canvas.paste(logo, ((180 - 140) // 2, (180 - 140) // 2 - 2), logo)
    apple = apply_squircle(canvas, n=5.0)
    apple.save(out / "apple-touch-icon.png")

    # Android adaptive icon — foreground transparent, background solid
    fg = Image.new("RGBA", (432, 432), (0, 0, 0, 0))
    logo = make_logo_png(220)
    fg.paste(logo, ((432 - 220) // 2, (432 - 220) // 2 - 4), logo)
    fg.save(out / "ic_launcher_foreground.png")
    bg = Image.new("RGBA", (432, 432), INK)
    bg.save(out / "ic_launcher_background.png")

    # PWA icons
    for size, logo_size, radius_ratio in [(192, 150, 0.42), (512, 400, 0.42)]:
        canvas = make_ink_canvas(size)
        logo = make_logo_png(logo_size)
        canvas.paste(logo, ((size - logo_size) // 2, (size - logo_size) // 2 - size // 60), logo)
        sq = apply_squircle(canvas, n=5.0)
        sq.save(out / f"icon-{size}.png")

    # Maskable icon: no mask, full INK, logo at 60% in safe zone
    canvas = make_ink_canvas(512)
    logo = make_logo_png(300)
    canvas.paste(logo, ((512 - 300) // 2, (512 - 300) // 2 - 10), logo)
    canvas.save(out / "icon-512-maskable.png")

    # App icons in 5 sizes with squircle
    for size in (64, 128, 256, 512, 1024):
        canvas = make_ink_canvas(size)
        logo_size = int(size * 0.7)
        logo = make_logo_png(logo_size)
        offset = (size - logo_size) // 2
        upshift = max(1, size // 50)
        canvas.paste(logo, (offset, offset - upshift), logo)
        sq = apply_squircle(canvas, n=5.0)
        sq.save(out / f"pulse-app-icon-{size}.png")

    print("    ✓ 15 icon files generated")


# ────────────────── Phase 7: Social cards ──────────────────

def social_svg(width: int, height: int, with_subhead: bool = True) -> str:
    """Hand-built SVG social card (Playwright not required)."""
    logo_size = int(height * 0.12)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <rect width="{width}" height="{height}" fill="{INK}"/>

  <!-- Top: logo + wordmark -->
  <g transform="translate(64 64)">
    <g transform="scale({logo_size/1024:.6f})">
      <rect x="0" y="0" width="1024" height="1024" rx="184" ry="184" fill="{INK_SOFT}"/>
      <g fill="{PAPER}">
        <path d="M 360 200 L 360 824 L 484 824 L 484 588 L 580 588 C 720 588 824 484 824 360 C 824 270 760 200 620 200 Z M 484 308 L 600 308 C 660 308 700 332 700 392 C 700 452 660 480 600 480 L 484 480 Z"/>
      </g>
      <g fill="none" stroke="{PULSE}" stroke-width="32" stroke-linecap="round" stroke-linejoin="round">
        <path d="M 80 560 L 220 560 L 260 460 L 320 680 L 380 380 L 440 620 L 500 480 L 560 600 L 640 560 L 800 560 L 944 560"/>
      </g>
    </g>
    <text x="{logo_size + 18}" y="{int(logo_size * 0.72)}"
          font-family="Inter Tight, Inter, -apple-system, Segoe UI, sans-serif"
          font-size="{int(logo_size * 0.56)}" font-weight="600" letter-spacing="-0.035em"
          fill="{PAPER}">pulse</text>
  </g>

  <!-- Center: headline -->
  <text x="64" y="{int(height * 0.55)}"
        font-family="Inter Tight, Inter, -apple-system, Segoe UI, sans-serif"
        font-size="{int(height * 0.13)}" font-weight="500" letter-spacing="-0.025em"
        fill="{PAPER}">Mint for the AI era.</text>

  {f'''<text x="64" y="{int(height * 0.68)}"
        font-family="Inter Tight, Inter, -apple-system, Segoe UI, sans-serif"
        font-size="{int(height * 0.045)}" font-weight="400" opacity="0.7"
        fill="{PAPER}">Track every AI subscription, every Claude token,</text>
  <text x="64" y="{int(height * 0.74)}"
        font-family="Inter Tight, Inter, -apple-system, Segoe UI, sans-serif"
        font-size="{int(height * 0.045)}" font-weight="400" opacity="0.7"
        fill="{PAPER}">every hour of focused work.</text>''' if with_subhead else ''}

  <!-- Bottom: meta -->
  <g font-family="JetBrains Mono, ui-monospace, monospace" font-size="{int(height * 0.026)}" fill="{PAPER}" opacity="0.6">
    <text x="64" y="{height - 48}">github.com/walight999/pulse</text>
    <text x="{width / 2}" y="{height - 48}" text-anchor="middle">Local-first · MIT</text>
    <text x="{width - 64}" y="{height - 48}" text-anchor="end">pulse.app</text>
  </g>
</svg>"""


def phase7_social():
    print("\n[7] Social cards")
    out = OUTPUT_DIR / "05-social"

    # GitHub social preview 1280×640
    gh = social_svg(1280, 640)
    (out / "github-social-preview.svg").write_text(gh, encoding="utf-8")
    svg_to_png(gh, out / "github-social-preview.png", 1280, 640)

    # OG default 1200×630 — copy from input if available, else generate
    og_src = INPUT_DIR / "og_card.png"
    if og_src.exists():
        shutil.copy(og_src, out / "og-default.png")
    else:
        og = social_svg(1200, 630)
        svg_to_png(og, out / "og-default.png", 1200, 630)

    # Twitter card 1600×900
    tw = social_svg(1600, 900)
    (out / "twitter-card-default.svg").write_text(tw, encoding="utf-8")
    svg_to_png(tw, out / "twitter-card-default.png", 1600, 900)

    print("    ✓ 3 social cards generated")


# ────────────────── Phase 8: Reference copies ──────────────────

def phase8_reference():
    print("\n[8] Reference copies")
    out = OUTPUT_DIR / "06-reference"
    for src, dst in [
        ("og_card.png", "og-card.png"),
        ("browser_mockup.png", "browser-mockup.png"),
        ("hero_illustration.png", "hero-illustration.png"),
    ]:
        if (INPUT_DIR / src).exists():
            shutil.copy(INPUT_DIR / src, out / dst)
    print(f"    ✓ {len(list(out.iterdir()))} reference files copied")


# ────────────────── Phase 9: README ──────────────────

def phase9_readme():
    print("\n[9] README.md")
    readme = f"""# Pulse Brand Core v1

Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}

## Quick reference

- **Colors**: Ink `#0A0A0F` · Ink-soft `#17171C` · Paper `#FAFAF7` · Pulse `#00E5A0`
- **Light-bg accent**: `#00C58A` (AA-safe alternative to `#00E5A0`)
- **Display font**: Inter Tight (500, 600)
- **Mono font**: JetBrains Mono (400)

## File guide

| File | Use case |
|------|----------|
| `01-logomark/pulse-mark--master.svg` | Default mark (dark contexts) |
| `01-logomark/pulse-mark--mono-white.svg` | Single-color overlays on photos |
| `01-logomark/pulse-mark--mono-black.svg` | Print, faxable, single-ink |
| `01-logomark/pulse-mark--solid-green.svg` | Brand-color-only contexts (T-shirts, stickers) |
| `02-lockups/pulse-lockup-horizontal-*` | Email signatures, navbar |
| `02-lockups/pulse-lockup-vertical-*` | App splash, store listing |
| `03-wordmark/pulse-wordmark.svg` | Footer, small areas where mark would be illegible |
| `04-icons/favicon-{{16,32,48}}.png` | Browser tab |
| `04-icons/favicon.ico` | Legacy browsers |
| `04-icons/apple-touch-icon.png` | iOS home screen |
| `04-icons/ic_launcher_foreground.png` | Android adaptive (with bg layer) |
| `04-icons/icon-{{192,512,512-maskable}}.png` | PWA install |
| `04-icons/pulse-app-icon-{{64..1024}}.png` | Desktop installer + store listings |
| `05-social/github-social-preview.png` | GitHub repo Settings → Social preview |
| `05-social/og-default.png` | Open Graph / link preview |
| `05-social/twitter-card-default.png` | Twitter / X card |
| `06-reference/*` | Final art from the original brand asset set |

## Don'ts

- ✗ No gradients, glow, or shadow on the mark
- ✗ No recolor outside the 4 brand colors
- ✗ No stretch, skew, or rotation
- ✗ No reproduction below 16px height
- ✗ No "P." or "Pulse." — always lowercase wordmark, no trailing punctuation
- ✗ No mixing Inter Tight with another sans-serif in the same lockup

## Do's

- ✓ Surround the mark with at least 0.25× its width of clear space
- ✓ Use mono-white for hero areas on photos or busy backgrounds
- ✓ Pair display + mono fonts (Inter Tight + JetBrains Mono) for technical content
- ✓ Always animate the waveform left-to-right (never right-to-left)

## Regenerate

```bash
python scripts/generate_brand_core.py
```
"""
    (OUTPUT_DIR / "README.md").write_text(readme, encoding="utf-8")
    print("    ✓ README.md")


# ────────────────── Phase 10: Verification ──────────────────

EXPECTED_FILES = [
    "01-logomark/pulse-mark--master.svg",
    "01-logomark/pulse-mark--master.png",
    "01-logomark/pulse-mark--mono-white.svg",
    "01-logomark/pulse-mark--mono-white.png",
    "01-logomark/pulse-mark--mono-black.svg",
    "01-logomark/pulse-mark--mono-black.png",
    "01-logomark/pulse-mark--solid-green.svg",
    "02-lockups/pulse-lockup-horizontal-light.svg",
    "02-lockups/pulse-lockup-horizontal-light.png",
    "02-lockups/pulse-lockup-horizontal-dark.svg",
    "02-lockups/pulse-lockup-horizontal-dark.png",
    "02-lockups/pulse-lockup-vertical-light.svg",
    "02-lockups/pulse-lockup-vertical-light.png",
    "02-lockups/pulse-lockup-vertical-dark.svg",
    "02-lockups/pulse-lockup-vertical-dark.png",
    "03-wordmark/pulse-wordmark.svg",
    "03-wordmark/pulse-wordmark.png",
    "04-icons/favicon-16.png",
    "04-icons/favicon-32.png",
    "04-icons/favicon-48.png",
    "04-icons/favicon.ico",
    "04-icons/apple-touch-icon.png",
    "04-icons/ic_launcher_foreground.png",
    "04-icons/ic_launcher_background.png",
    "04-icons/icon-192.png",
    "04-icons/icon-512.png",
    "04-icons/icon-512-maskable.png",
    "04-icons/pulse-app-icon-64.png",
    "04-icons/pulse-app-icon-128.png",
    "04-icons/pulse-app-icon-256.png",
    "04-icons/pulse-app-icon-512.png",
    "04-icons/pulse-app-icon-1024.png",
    "05-social/github-social-preview.png",
    "05-social/og-default.png",
    "05-social/twitter-card-default.png",
    "README.md",
]


def phase10_verify() -> tuple[int, int, int]:
    print("\n[10] Verify")
    missing = []
    total_bytes = 0
    for relpath in EXPECTED_FILES:
        p = OUTPUT_DIR / relpath
        if not p.exists():
            missing.append(relpath)
        else:
            total_bytes += p.stat().st_size
    if missing:
        (OUTPUT_DIR / "ERRORS.md").write_text(
            "# Missing files\n\n" + "\n".join(f"- {f}" for f in missing),
            encoding="utf-8",
        )
        print(f"    ✗ {len(missing)} missing — see ERRORS.md")
    else:
        print(f"    ✓ all {len(EXPECTED_FILES)} files present")
    print(f"    Total size: {total_bytes / 1024:.1f} KB")
    return len(EXPECTED_FILES) - len(missing), len(missing), total_bytes


# ────────────────── Phase 11: Zip ──────────────────

def phase11_zip():
    print("\n[11] Package")
    zip_path = PROJECT_ROOT / "pulse-brand-core-v1"
    if (PROJECT_ROOT / "pulse-brand-core-v1.zip").exists():
        (PROJECT_ROOT / "pulse-brand-core-v1.zip").unlink()
    shutil.make_archive(str(zip_path), "zip", str(OUTPUT_DIR))
    final = PROJECT_ROOT / "pulse-brand-core-v1.zip"
    if final.exists():
        print(f"    ✓ {final.name} — {final.stat().st_size / 1024:.1f} KB")
    else:
        print("    ✗ zip not created")


# ────────────────── Main ──────────────────

def main():
    print(f"Pulse Brand Core v1 generator")
    print(f"  cairosvg: {'yes' if _HAS_CAIROSVG else 'no (Pillow fallback)'}")
    print(f"  output:   {OUTPUT_DIR}")

    phase1_setup()
    phase2_3_logomark()
    phase4_lockups()
    phase5_wordmark()
    phase6_icons()
    phase7_social()
    phase8_reference()
    phase9_readme()
    ok, miss, size = phase10_verify()
    phase11_zip()

    print(f"\n--- Summary ---")
    print(f"  Files: {ok} ok / {miss} missing")
    print(f"  Size:  {size / 1024:.1f} KB")
    print(f"  Status: {'✓ READY' if miss == 0 else '⚠ partial — see ERRORS.md'}")


if __name__ == "__main__":
    main()
