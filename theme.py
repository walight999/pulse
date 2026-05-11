"""Theme system — light / dark / auto.

Streamlit's base theme is configured at build-time in .streamlit/config.toml.
This module overrides it at runtime by injecting CSS that targets every
element. Reads `theme` setting from app_settings (light/dark/auto).
"""
from __future__ import annotations

from db import get_setting


# ────────────────── Color tokens ──────────────────
LIGHT = {
    # Pulse Brand Core v1 — exact tokens (PAPER bg, INK text, PULSE accent)
    "bg_primary":   "#FAFAF7",     # PAPER
    "bg_secondary": "#F4F4F0",
    "bg_card":      "#FFFFFF",
    "bg_input":     "#FFFFFF",
    "bg_hover":     "#EFEFEC",

    "text_primary":   "#0A0A0F",   # INK
    "text_secondary": "#6B6B6B",   # SLATE
    "text_muted":     "#9C9C9C",
    "text_invert":    "#FAFAF7",

    "border":         "#E4E4DF",
    "border_strong":  "#CFCFCA",
    "border_subtle":  "#EFEFEC",

    # Pulse green — accent (use sparingly per brand guidelines)
    "accent":         "#00C58A",   # slightly muted PULSE for light bg AA contrast
    "accent_hover":   "#00A076",
    "accent_bg":      "#E6FFF5",
    "accent_border":  "#9FF0CC",

    "success":        "#00C58A",
    "success_bg":     "#E6FFF5",
    "success_border": "#9FF0CC",

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
    # Pulse Brand Core v1 — INK canvas with vivid PULSE accent
    "bg_primary":   "#0A0A0F",     # INK (Brand Core master)
    "bg_secondary": "#11111A",
    "bg_card":      "#17171C",     # INK_SOFT
    "bg_input":     "#0A0A0F",
    "bg_hover":     "#1F1F26",

    "text_primary":   "#FAFAF7",   # PAPER
    "text_secondary": "#A3A3A0",
    "text_muted":     "#6B6B6B",   # SLATE
    "text_invert":    "#0A0A0F",

    "border":         "#22222A",
    "border_strong":  "#3A3A42",
    "border_subtle":  "#15151C",

    # Pulse green — vivid PULSE accent (the logomark pulse line)
    "accent":         "#00E5A0",   # PULSE (Brand Core master)
    "accent_hover":   "#33EBB8",
    "accent_bg":      "#022820",
    "accent_border":  "#065F46",

    "success":        "#00E5A0",
    "success_bg":     "#022820",
    "success_border": "#065F46",

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
