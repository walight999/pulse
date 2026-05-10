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
    "bg_secondary": "#f8fafc",
    "bg_card":      "#ffffff",
    "bg_input":     "#ffffff",
    "bg_hover":     "#f1f5f9",

    "text_primary":   "#0f172a",
    "text_secondary": "#64748b",
    "text_muted":     "#94a3b8",
    "text_invert":    "#ffffff",

    "border":         "#e2e8f0",
    "border_strong":  "#cbd5e1",
    "border_subtle":  "#f1f5f9",

    "accent":         "#6366f1",
    "accent_hover":   "#4f46e5",
    "accent_bg":      "#eef2ff",
    "accent_border":  "#c7d2fe",

    "success":        "#16a34a",
    "success_bg":     "#dcfce7",
    "success_border": "#86efac",

    "warning":        "#d97706",
    "warning_bg":     "#fef3c7",
    "warning_border": "#fcd34d",

    "danger":         "#dc2626",
    "danger_bg":      "#fee2e2",
    "danger_border":  "#fca5a5",

    "amber":          "#9a6700",
    "blue":           "#0969da",
    "gray":           "#64748b",

    "shadow_sm":  "0 1px 2px rgba(15, 23, 42, 0.04)",
    "shadow_md":  "0 1px 3px rgba(15, 23, 42, 0.08)",
}

DARK = {
    # Modern dark — near-black with subtle cool tint, layered elevation.
    # Inspired by Linear / Vercel / Notion dark themes.
    "bg_primary":   "#0a0b0f",   # near-black canvas
    "bg_secondary": "#111217",   # sidebar / subtle raised
    "bg_card":      "#16181d",   # card surface
    "bg_input":     "#0e1014",   # inputs (recessed look)
    "bg_hover":     "#1f2128",   # interactive hover

    "text_primary":   "#e8e8ec",   # off-white, easier on eyes
    "text_secondary": "#a3a4ae",
    "text_muted":     "#6a6b76",
    "text_invert":    "#0a0b0f",

    "border":         "#26272e",   # ~10% white
    "border_strong":  "#393a44",   # ~16% white
    "border_subtle":  "#1a1c22",

    "accent":         "#a5b4fc",   # indigo-300 — pops on dark
    "accent_hover":   "#c7d2fe",
    "accent_bg":      "#1a1c3d",   # deep indigo tint
    "accent_border":  "#4338ca",

    "success":        "#4ade80",
    "success_bg":     "#0a2418",
    "success_border": "#15803d",

    "warning":        "#fbbf24",
    "warning_bg":     "#2a1c05",
    "warning_border": "#a16207",

    "danger":         "#f87171",
    "danger_bg":      "#2a1010",
    "danger_border":  "#b91c1c",

    "amber":          "#fbbf24",
    "blue":           "#60a5fa",
    "gray":           "#a3a4ae",

    "shadow_sm":  "0 1px 2px rgba(0, 0, 0, 0.5)",
    "shadow_md":  "0 4px 12px rgba(0, 0, 0, 0.6)",
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
