"""Theme system — light / dark / auto.

Streamlit's base theme is configured at build-time in .streamlit/config.toml.
This module overrides it at runtime by injecting CSS that targets every
element. Reads `theme` setting from app_settings (light/dark/auto).
"""
from __future__ import annotations

from db import get_setting


# ────────────────── Color tokens ──────────────────
LIGHT = {
    "bg_primary":   "#ffffff",
    "bg_secondary": "#f6f7f9",
    "bg_card":      "#ffffff",
    "bg_input":     "#ffffff",
    "bg_hover":     "#f1f3f5",

    "text_primary":   "#0a0b0f",
    "text_secondary": "#5a6172",
    "text_muted":     "#9ca3af",
    "text_invert":    "#ffffff",

    "border":         "#e5e7eb",
    "border_strong":  "#d1d5db",
    "border_subtle":  "#f3f4f6",

    # Pulse brand — mint/emerald accent (matches logomark pulse line)
    "accent":         "#10b981",
    "accent_hover":   "#059669",
    "accent_bg":      "#ecfdf5",
    "accent_border":  "#a7f3d0",

    "success":        "#10b981",
    "success_bg":     "#ecfdf5",
    "success_border": "#a7f3d0",

    "warning":        "#d97706",
    "warning_bg":     "#fef3c7",
    "warning_border": "#fcd34d",

    "danger":         "#dc2626",
    "danger_bg":      "#fee2e2",
    "danger_border":  "#fca5a5",

    "amber":          "#9a6700",
    "blue":           "#0969da",
    "gray":           "#5a6172",

    "shadow_sm":  "0 1px 2px rgba(10, 11, 15, 0.04)",
    "shadow_md":  "0 1px 3px rgba(10, 11, 15, 0.08)",
}

DARK = {
    # Pulse brand dark — pure black canvas with mint accent (matches logomark).
    "bg_primary":   "#000000",   # true black to match logo
    "bg_secondary": "#0a0b0f",   # sidebar / subtle raised
    "bg_card":      "#111317",   # card surface
    "bg_input":     "#0a0b0f",   # inputs (recessed)
    "bg_hover":     "#1a1d23",   # interactive hover

    "text_primary":   "#ffffff",   # pure white (matches logo P)
    "text_secondary": "#a3a4ae",
    "text_muted":     "#6a6b76",
    "text_invert":    "#000000",

    "border":         "#22252c",   # subtle on black
    "border_strong":  "#393c44",
    "border_subtle":  "#15171c",

    # Pulse brand mint — vivid emerald that pops on pure black
    "accent":         "#34d399",   # emerald-400 (the logo pulse line color)
    "accent_hover":   "#6ee7b7",   # emerald-300 brighter for hover
    "accent_bg":      "#022c22",   # deep emerald tint
    "accent_border":  "#065f46",   # emerald-800

    "success":        "#34d399",
    "success_bg":     "#022c22",
    "success_border": "#065f46",

    "warning":        "#fbbf24",
    "warning_bg":     "#2a1c05",
    "warning_border": "#a16207",

    "danger":         "#f87171",
    "danger_bg":      "#2a1010",
    "danger_border":  "#b91c1c",

    "amber":          "#fbbf24",
    "blue":           "#60a5fa",
    "gray":           "#a3a4ae",

    "shadow_sm":  "0 1px 2px rgba(0, 0, 0, 0.6)",
    "shadow_md":  "0 4px 14px rgba(0, 0, 0, 0.7)",
}


def current_theme() -> str:
    """Returns 'light' or 'dark' (resolves 'auto' via prefers-color-scheme)."""
    pref = get_setting("theme", "light")
    if pref in ("light", "dark"):
        return pref
    # 'auto' is handled in CSS via @media query
    return "auto"


def get_palette() -> dict:
    """For server-side rendering decisions (e.g., chart colors).
    Returns LIGHT for 'auto' since we can't detect prefers-color-scheme server-side."""
    t = current_theme()
    if t == "dark":
        return DARK
    return LIGHT


def css_block() -> str:
    """Render <style> block with all theme tokens + dark-mode overrides."""
    pref = get_setting("theme", "light")

    light_vars = "\n".join(f"  --{k.replace('_', '-')}: {v};" for k, v in LIGHT.items())
    dark_vars  = "\n".join(f"  --{k.replace('_', '-')}: {v};" for k, v in DARK.items())

    if pref == "dark":
        # Force dark always
        root_block = f":root {{\n{dark_vars}\n  color-scheme: dark;\n}}"
    elif pref == "light":
        root_block = f":root {{\n{light_vars}\n  color-scheme: light;\n}}"
    else:  # auto
        root_block = (
            f":root {{\n{light_vars}\n  color-scheme: light dark;\n}}\n"
            f"@media (prefers-color-scheme: dark) {{\n  :root {{\n{dark_vars}\n  }}\n}}"
        )

    return f"<style>\n{root_block}\n</style>"
