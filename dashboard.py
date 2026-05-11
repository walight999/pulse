"""Life Tracker — text-first dashboard (VS Code extension feel)."""
import io
import json
from datetime import datetime, timedelta, date
from html import escape
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import fx
import categories
import quips
import account
import waitlist
import referrals
import telemetry
import theme
from db import get_conn, init_db, get_setting, set_setting
from sync_tokens import sync_all, get_sync_status

init_db()

_BRAND_ICON = Path(__file__).parent / "static" / "brand" / "app-icon.png"
st.set_page_config(
    page_title="pulse — Mint for the AI era",
    page_icon=str(_BRAND_ICON) if _BRAND_ICON.exists() else "💚",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "pulse — Mint for the AI era. https://pulse.app"},
)

# ============================================================
# Brand & colors
# ============================================================
APP_NAME = "pulse"          # lowercase wordmark per brand identity
APP_TAGLINE = "Mint for the AI era"

# Master Brand Core SVG — inline so logo matches favicon + landing + email
# everywhere. Geometry from pulse-brand-core/scripts/generate_brand_core.py.
_PULSE_LOGO_SVG = (
    '<svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" '
    'style="width:100%;height:100%;display:block;">'
    '<rect x="0" y="0" width="1024" height="1024" rx="184" ry="184" fill="#0A0A0F"/>'
    '<g fill="#FAFAF7">'
    '<path d="M 360 200 L 360 824 L 484 824 L 484 588 L 580 588 '
    'C 720 588 824 484 824 360 C 824 270 760 200 620 200 Z '
    'M 484 308 L 600 308 C 660 308 700 332 700 392 '
    'C 700 452 660 480 600 480 L 484 480 Z"/>'
    '</g>'
    '<g fill="none" stroke="#00E5A0" stroke-width="32" '
    'stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M 80 560 L 220 560 L 260 460 L 320 680 L 380 380 '
    'L 440 620 L 500 480 L 560 600 L 640 560 L 800 560 L 944 560"/>'
    '</g>'
    '</svg>'
)

COLOR_HEX = {
    "green":  "#16a34a",
    "amber":  "#d97706",
    "blue":   "#6366f1",
    "red":    "#dc2626",
    "gray":   "#64748b",
}
# Theme-aware status colors — for text/borders on cards (readable in dark mode)
COLOR_VAR = {
    "green":  "var(--success)",
    "amber":  "var(--warning)",
    "blue":   "var(--accent)",
    "red":    "var(--danger)",
    "gray":   "var(--text-muted)",
}
ACCENT = "var(--accent)"        # theme-aware accent
ACCENT_BG = "var(--accent-bg)"  # theme-aware tint
ACCENT_BORDER = "var(--accent-border)"

# ============================================================
# CSS — GitHub / VS Code light, dense and consistent
# ============================================================
# Inject theme tokens FIRST so var(--...) works in subsequent CSS
st.markdown(theme.css_block(), unsafe_allow_html=True)

st.markdown(
    """
    <style>
        /* Hide Streamlit chrome — keep sidebar toggle visible */
        #MainMenu,
        footer,
        [data-testid="stStatusWidget"],
        [data-testid="stDecoration"],
        [data-testid="stToolbar"],
        [data-testid="stMainMenu"],
        [data-testid="stDeployButton"],
        a[href*="streamlit.io"],
        a[href*="share.streamlit"],
        .viewerBadge_container__1QSob,
        ._terminalButton_rix23_138,
        [class*="viewerBadge"],
        [class*="streamlit"] [href*="streamlit"] {
            display: none !important;
            visibility: hidden !important;
        }
        [data-testid="stHeader"] {
            background: transparent !important;
            height: 0 !important;
            min-height: 0 !important;
        }
        /* "Made with Streamlit" footer / running indicator */
        .stApp > footer,
        .stApp [class*="MadeWithStreamlit"] {
            display: none !important;
        }

        /* Fade-in animation for content — smooths reruns / theme switches */
        @keyframes pulse-app-fade-in {
            from { opacity: 0.4; }
            to   { opacity: 1; }
        }
        [data-testid="stMain"] [data-testid="stMainBlockContainer"] {
            animation: pulse-app-fade-in 0.22s ease-out;
        }
        /* Theme transitions — soft color shift instead of jarring repaint */
        [data-testid="stApp"],
        [data-testid="stSidebar"],
        .sub-card,
        .pulse-table,
        .top-apps-list,
        .kpi-card {
            transition: background 0.18s ease, color 0.18s ease, border-color 0.18s ease;
        }
        @media (prefers-reduced-motion: reduce) {
            [data-testid="stMainBlockContainer"] { animation: none !important; }
        }
        /* Sidebar collapse/expand toggle — unified slide-handle.
           Streamlit places these in different DOM containers (collapse button
           lives inside stSidebarHeader; expand button is at the app root).
           Use position:fixed + top:50vh anchored to viewport so they appear
           at the same vertical mid-point regardless of parent.
           Note: avoid translateY — if any ancestor has `transform`, fixed
           positioning becomes relative to it. margin-top is safer. */

        /* Neutralize sidebar header positioning so it doesn't trap our fixed button */
        [data-testid="stSidebarHeader"] {
            position: static !important;
            overflow: visible !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        button[data-testid="stSidebarCollapseButton"],
        button[data-testid="stExpandSidebarButton"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="stExpandSidebarButton"] {
            visibility: visible !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            position: fixed !important;
            top: 50vh !important;
            margin-top: -28px !important;  /* half of height for vertical center */
            transform: none !important;
            width: 24px !important;
            min-width: 24px !important;
            max-width: 24px !important;
            height: 56px !important;
            min-height: 56px !important;
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            border-left: none !important;
            border-radius: 0 10px 10px 0 !important;
            box-shadow: 3px 0 10px rgba(0, 0, 0, 0.15) !important;
            z-index: 99999 !important;
            cursor: pointer !important;
            color: var(--text-secondary) !important;
            padding: 0 !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
            margin-bottom: 0 !important;
            font-size: 0.9rem !important;
        }
        button[data-testid="stSidebarCollapseButton"]:hover,
        button[data-testid="stExpandSidebarButton"]:hover,
        [data-testid="stSidebarCollapseButton"]:hover,
        [data-testid="stExpandSidebarButton"]:hover {
            background: var(--bg-hover) !important;
            color: var(--accent) !important;
            border-color: var(--accent-border) !important;
        }
        /* OPEN: handle attaches flush at right edge of sidebar (250px wide) */
        button[data-testid="stSidebarCollapseButton"],
        [data-testid="stSidebarCollapseButton"] {
            left: 250px !important;
        }
        /* CLOSED: handle at left edge of viewport */
        button[data-testid="stExpandSidebarButton"],
        [data-testid="stExpandSidebarButton"] {
            left: 0 !important;
        }
        /* Inner icon centering */
        [data-testid="stSidebarCollapseButton"] > *,
        [data-testid="stExpandSidebarButton"] > * {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 100% !important;
            height: 100% !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        /* Icon SVG fills the button */
        [data-testid="stSidebarCollapseButton"] svg,
        [data-testid="stExpandSidebarButton"] svg {
            width: 14px !important;
            height: 14px !important;
        }

        /* override Streamlit base background + text color (heavy hand for dark mode) */
        html, body,
        [data-testid="stApp"],
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"],
        .main, .stApp,
        section[data-testid="stMain"] {
            background: var(--bg-primary) !important;
            color: var(--text-primary) !important;
        }

        /* Main container — comfortable, modern.
           Generous padding gives content room to breathe rather than feeling
           cramped against viewport edges. */
        .block-container {
            padding-top: 1.8rem;
            padding-bottom: 3rem;
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 1140px;
            font-size: 14px;
            color: var(--text-primary);
        }
        /* Vertical rhythm — Streamlit blocks get consistent breathing room */
        [data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] {
            gap: 0.6rem;
        }
        /* Horizontal column spacing — prevents adjacent KPI cards/widgets
           from touching each other. Default Streamlit gap is too tight. */
        [data-testid="stMainBlockContainer"] [data-testid="stHorizontalBlock"] {
            gap: 1rem;
        }
        /* Markdown block bottom margin — keeps consecutive paragraphs apart */
        [data-testid="stMarkdownContainer"] > * + * {
            margin-top: 0.4rem;
        }
        /* Sidebar columns get tighter spacing (less width to spare) */
        [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
            gap: 0.5rem;
        }
        /* Tab panel — give content space below the tab strip */
        [data-testid="stTabs"] [data-baseweb="tab-panel"] {
            padding-top: 0.6rem;
        }
        /* Last child of vertical block — no extra bottom margin */
        [data-testid="stVerticalBlock"] > div:last-child {
            margin-bottom: 0;
        }

        /* Typography — looser line-heights, better hierarchy */
        h1, h2, h3, h4, h5, h6 {color: var(--text-primary);}
        h1 {
            font-size: 1.7rem !important;
            font-weight: 700;
            padding: 0;
            margin: 0 0 0.2rem 0;
            line-height: 1.25;
            letter-spacing: -0.015em;
        }
        h2 {
            font-size: 1.1rem !important;
            font-weight: 600;
            margin-top: 1.4rem;
            margin-bottom: 0.5rem;
            line-height: 1.35;
        }
        h3, h4, h5 {
            font-size: 0.96rem !important;
            font-weight: 600;
            margin-top: 1rem;
            margin-bottom: 0.4rem;
            line-height: 1.4;
        }
        h5 { font-size: 0.92rem !important; letter-spacing: -0.005em; }
        p, label, span, div {color: inherit;}
        p { line-height: 1.55; }

        [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * {
            font-size: 0.85rem;
            color: var(--text-secondary);
        }

        /* Sidebar — clean, themed, fixed width + smooth fold animation */
        [data-testid="stSidebar"] {
            background: var(--bg-secondary) !important;
            border-right: 1px solid var(--border) !important;
            width: 250px !important;
            min-width: 250px !important;
            max-width: 250px !important;
            flex: 0 0 250px !important;
            transition: transform 0.28s cubic-bezier(0.4, 0, 0.2, 1),
                        margin 0.28s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        /* Smooth fold transition for the collapse handle position */
        button[data-testid="stSidebarCollapseButton"],
        button[data-testid="stExpandSidebarButton"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="stExpandSidebarButton"] {
            transition: left 0.28s cubic-bezier(0.4, 0, 0.2, 1),
                        background 0.15s ease, color 0.15s ease,
                        border-color 0.15s ease !important;
        }
        /* Main content shifts smoothly when sidebar opens/closes */
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"] {
            transition: margin 0.28s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        [data-testid="stSidebar"] > div:first-child {
            width: 250px !important;
            min-width: 250px !important;
            max-width: 250px !important;
        }
        /* Disable the user-drag resize handle on sidebar edge */
        [data-testid="stSidebarResizeHandle"],
        [data-testid="stSidebar"] [class*="resizeHandle"],
        [data-testid="stSidebar"] [class*="ResizeHandle"] {
            display: none !important;
            pointer-events: none !important;
            cursor: default !important;
            width: 0 !important;
        }
        [data-testid="stSidebar"] * {color: var(--text-primary);}
        [data-testid="stSidebar"] .block-container {padding-top: 1.5rem;}
        [data-testid="stSidebar"] [data-testid="stRadio"] label {
            font-size: 0.9rem;
            padding: 7px 12px;
            border-radius: 6px;
            transition: background 0.15s ease;
        }
        [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
            background: var(--bg-hover);
        }

        /* Brand row — exact Pulse logomark (inline SVG) + lowercase wordmark.
           SVG matches Brand Core master geometry exactly (P + ECG waveform). */
        .pulse-brand-row {
            display: flex;
            align-items: center;
            gap: 10px;
            height: 38px;
        }
        .pulse-logo-mark {
            width: 36px;
            height: 36px;
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            filter: drop-shadow(0 1px 4px rgba(0, 229, 160, 0.25));
        }
        .pulse-logo-mark svg {
            width: 100%;
            height: 100%;
            display: block;
        }
        .pulse-brand-name {
            font-size: 1.32rem;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.03em;
            line-height: 1;
            text-transform: lowercase;
            font-family: -apple-system, "Segoe UI", system-ui, sans-serif;
        }

        /* Theme toggle — icon button, fills its column slot cleanly */
        [data-testid="stSidebar"] [data-testid="stHorizontalBlock"]:first-of-type
            .stButton > button {
            font-size: 1.05rem !important;
            padding: 0 !important;
            height: 38px !important;
            min-height: 38px !important;
            border-radius: 9px !important;
            text-align: center !important;
            justify-content: center !important;
            display: flex !important;
            align-items: center !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border) !important;
            background: var(--bg-card) !important;
            font-weight: 400 !important;
        }
        [data-testid="stSidebar"] [data-testid="stHorizontalBlock"]:first-of-type
            .stButton > button:hover {
            background: var(--bg-hover) !important;
            color: var(--accent) !important;
            border-color: var(--accent-border) !important;
        }
        /* Material icon inside the theme toggle — force theme color, proper size */
        [data-testid="stSidebar"] [data-testid="stHorizontalBlock"]:first-of-type
            .stButton > button [data-testid="stIconMaterial"],
        [data-testid="stSidebar"] [data-testid="stHorizontalBlock"]:first-of-type
            .stButton > button span[class*="Icon"] {
            color: var(--text-primary) !important;
            font-size: 1.15rem !important;
            line-height: 1 !important;
        }
        [data-testid="stSidebar"] [data-testid="stHorizontalBlock"]:first-of-type
            .stButton > button:hover [data-testid="stIconMaterial"],
        [data-testid="stSidebar"] [data-testid="stHorizontalBlock"]:first-of-type
            .stButton > button:hover span[class*="Icon"] {
            color: var(--accent) !important;
        }

        /* Sidebar nav buttons — clean nav-item look + comfortable spacing */
        [data-testid="stSidebar"] .stButton > button {
            text-align: left;
            justify-content: flex-start;
            background: transparent;
            border: 1px solid transparent;
            color: var(--text-secondary);
            font-weight: 500;
            font-size: 0.88rem;
            padding: 0 14px;
            min-height: 40px;
            height: 40px;
            box-shadow: none;
            letter-spacing: -0.005em;
            margin-bottom: 4px;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            background: var(--bg-hover);
            border-color: transparent;
            color: var(--text-primary);
        }
        [data-testid="stSidebar"] .stButton > button[kind="primary"] {
            background: var(--accent-bg);
            color: var(--accent);
            border: 1px solid var(--accent-border);
            box-shadow: none;
            font-weight: 600;
        }
        [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
            background: var(--accent-bg);
            filter: brightness(1.05);
        }

        /* metric tiles — softer, more elevated, more breathing room */
        [data-testid="stMetric"] {
            background: var(--bg-card);
            padding: 14px 18px;
            border: 1px solid var(--border);
            border-radius: 10px;
            box-shadow: var(--shadow-sm);
        }
        [data-testid="stMetricValue"] {
            font-size: 1.4rem !important;
            font-weight: 700;
            color: var(--text-primary) !important;
            font-variant-numeric: tabular-nums;
            line-height: 1.2;
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.7rem !important;
            color: var(--text-secondary) !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600;
            margin-bottom: 4px;
        }

        /* sidebar metrics — borderless, tight */
        [data-testid="stSidebar"] [data-testid="stMetric"] {
            background: transparent;
            border: none;
            box-shadow: none;
            padding: 4px 0;
        }
        [data-testid="stSidebar"] [data-testid="stMetricValue"] {
            font-size: 1.05rem !important;
        }
        [data-testid="stSidebar"] [data-testid="stMetricLabel"] {
            font-size: 0.68rem !important;
        }

        /* buttons — modern, themed */
        .stButton > button, .stDownloadButton > button {
            font-size: 0.82rem;
            padding: 4px 12px;
            min-height: 32px;
            height: 32px;
            border-radius: 7px;
            border: 1px solid var(--border);
            background: var(--bg-card);
            color: var(--text-primary);
            font-weight: 500;
            white-space: nowrap;
            transition: all 0.15s ease;
        }
        .stButton > button:hover, .stDownloadButton > button:hover {
            background: var(--bg-hover);
            border-color: var(--border-strong);
        }
        .stButton > button[kind="primary"] {
            background: var(--accent);
            color: var(--text-invert);
            border-color: var(--accent);
            box-shadow: var(--shadow-sm);
        }
        .stButton > button[kind="primary"]:hover {
            background: var(--accent-hover);
            border-color: var(--accent-hover);
        }

        /* Radio chips (horizontal) — pill-style, theme-aware. Streamlit's
           default chip ignores our CSS vars, so we override every state. */
        [data-testid="stRadio"] [role="radiogroup"] {
            gap: 6px;
            flex-wrap: wrap;
            align-items: center;
        }
        /* Horizontal radio specifically (filter chips on subscriptions page)
           — pack to the right edge of its column */
        [data-testid="stRadio"][aria-orientation="horizontal"] [role="radiogroup"] {
            justify-content: flex-end !important;
        }
        [data-testid="stRadio"][aria-orientation="horizontal"] label,
        [data-testid="stRadio"] [role="radiogroup"] label {
            font-size: 0.82rem !important;
            padding: 6px 14px !important;
            white-space: nowrap;
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            color: var(--text-secondary) !important;
            border-radius: 999px !important;
            font-weight: 500 !important;
            transition: all 0.15s ease;
            cursor: pointer;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            line-height: 1.2 !important;
            min-height: 30px !important;
            gap: 0 !important;
            margin: 0 !important;
        }
        [data-testid="stRadio"][aria-orientation="horizontal"] label:hover,
        [data-testid="stRadio"] [role="radiogroup"] label:hover {
            background: var(--bg-hover) !important;
            border-color: var(--border-strong) !important;
            color: var(--text-primary) !important;
        }
        /* Selected (checked) — accent tint pill */
        [data-testid="stRadio"][aria-orientation="horizontal"] label:has(input:checked),
        [data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) {
            background: var(--accent-bg) !important;
            border-color: var(--accent-border) !important;
            color: var(--accent) !important;
            font-weight: 600 !important;
        }
        /* Hide the actual radio circle for the chip look */
        [data-testid="stRadio"][aria-orientation="horizontal"] label > div:first-child,
        [data-testid="stRadio"] [role="radiogroup"] label > div:first-child {
            display: none !important;
            width: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        /* Text wrapper inside label — center, no extra spacing */
        [data-testid="stRadio"][aria-orientation="horizontal"] label > div:not(:first-child),
        [data-testid="stRadio"] [role="radiogroup"] label > div:not(:first-child),
        [data-testid="stRadio"] [role="radiogroup"] label p {
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1.2 !important;
            text-align: center !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-style: normal !important;
        }

        /* Sub-card status stripes — vertical gradient via pseudo element */
        .sub-card {
            position: relative;
            padding-left: 16px !important;
        }
        .sub-card::before {
            content: "";
            position: absolute;
            left: 0; top: 0; bottom: 0;
            width: 3px;
            border-radius: 8px 0 0 8px;
        }
        .sub-green::before {
            background: linear-gradient(180deg, var(--success) 0%, var(--accent) 100%);
        }
        .sub-amber::before {
            background: linear-gradient(180deg, var(--warning) 0%, var(--success) 100%);
        }
        .sub-red::before {
            background: linear-gradient(180deg, var(--danger) 0%, var(--warning) 100%);
        }
        .sub-blue::before { background: var(--accent); }
        .sub-gray::before { background: var(--text-muted); }

        /* KPI tinted variants — subtle gradient hint */
        .kpi-warning {
            background: linear-gradient(135deg, var(--bg-card) 0%, var(--warning-bg) 130%) !important;
        }
        .kpi-danger {
            background: linear-gradient(135deg, var(--bg-card) 0%, var(--danger-bg) 130%) !important;
        }
        .kpi-success {
            background: linear-gradient(135deg, var(--bg-card) 0%, var(--success-bg) 130%) !important;
        }
        .kpi-accent {
            background: linear-gradient(135deg, var(--bg-card) 0%, var(--accent-bg) 130%) !important;
        }

        /* Sidebar mini health bar — gradient red→amber→green, fill = % healthy */
        .pulse-health-track {
            height: 5px;
            border-radius: 3px;
            background: var(--bg-hover);
            overflow: hidden;
            margin-top: 8px;
            position: relative;
        }
        .pulse-health-fill {
            height: 100%;
            background: linear-gradient(90deg,
                var(--danger) 0%,
                var(--warning) 50%,
                var(--success) 100%);
            background-size: 100% 100%;
            transition: width 0.4s ease;
            border-radius: 3px;
        }
        .pulse-health-label {
            font-size: 0.65rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 6px;
            display: flex;
            justify-content: space-between;
        }

        /* Shimmer pill — for "lifetime savings" celebratory accent */
        @keyframes pulse-shimmer {
            0%   { background-position: 200% center; }
            100% { background-position: -200% center; }
        }
        .pulse-savings-shimmer {
            background: linear-gradient(110deg,
                var(--success-bg) 0%,
                var(--accent-bg) 35%,
                var(--success-bg) 70%,
                var(--success-bg) 100%) !important;
            background-size: 200% 100% !important;
            animation: pulse-shimmer 9s linear infinite;
        }

        /* Animated logo gradient — slow tasteful shift */
        @keyframes pulse-logo-shift {
            0%   { background-position: 0% 50%; }
            50%  { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .pulse-logo-mark {
            background-size: 300% 300% !important;
            animation: pulse-logo-shift 14s ease-in-out infinite;
        }
        @media (prefers-reduced-motion: reduce) {
            .pulse-logo-mark, .pulse-savings-shimmer { animation: none !important; }
        }

        /* compact text inputs and selectboxes — fits text without bloat */
        .block-container [data-testid="stTextInput"] input {
            font-size: 0.85rem;
            padding: 6px 10px;
        }
        /* Input placeholder — visible in dark mode (Streamlit defaults to a near-black) */
        .block-container [data-testid="stTextInput"] input::placeholder,
        .block-container [data-testid="stTextArea"] textarea::placeholder,
        .block-container [data-testid="stNumberInput"] input::placeholder {
            color: var(--text-muted) !important;
            opacity: 1 !important;
        }
        /* Input wrapper bg — Streamlit wraps in baseweb input container */
        .block-container [data-baseweb="input"],
        .block-container [data-baseweb="base-input"],
        .block-container [data-testid="stTextInput"] > div > div {
            background: var(--bg-input) !important;
            border-color: var(--border) !important;
            color: var(--text-primary) !important;
        }
        .block-container [data-baseweb="input"]:focus-within,
        .block-container [data-testid="stTextInput"] > div > div:focus-within {
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 1px var(--accent) !important;
        }
        .block-container [data-testid="stSelectbox"] > div > div {
            min-height: 34px;
            font-size: 0.85rem;
        }
        .block-container [data-testid="stSelectbox"] > div > div > div {
            padding: 2px 8px;
        }

        /* dataframe */
        [data-testid="stDataFrame"] {
            border: 1px solid var(--border);
            border-radius: 8px;
            font-size: 0.85rem;
            overflow: hidden;
        }

        /* expander — subtle */
        [data-testid="stExpander"] {
            border: 1px solid var(--border);
            border-radius: 8px;
            background: var(--bg-secondary);
        }
        [data-testid="stExpander"] summary {
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--text-primary);
        }

        /* form — generous padding for breathing room */
        [data-testid="stForm"] {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px 22px;
            box-shadow: var(--shadow-sm);
        }
        [data-testid="stForm"] [data-testid="stVerticalBlock"] {
            gap: 0.75rem;
        }

        /* alerts */
        [data-testid="stAlert"] {
            font-size: 0.9rem;
            padding: 12px 16px;
            border-radius: 8px;
            margin: 0.5rem 0;
        }

        /* Branded spinner — matches accent color, smooth */
        @keyframes pulse-spin {
            from { transform: rotate(0deg); }
            to   { transform: rotate(360deg); }
        }
        [data-testid="stSpinner"] {
            color: var(--accent) !important;
        }
        [data-testid="stSpinner"] > div {
            border-top-color: var(--accent) !important;
            border-right-color: var(--accent-border) !important;
            border-bottom-color: transparent !important;
            border-left-color: transparent !important;
            animation: pulse-spin 0.8s linear infinite !important;
        }
        [data-testid="stSpinner"] > div + div {
            color: var(--text-secondary) !important;
            font-size: 0.85rem !important;
        }

        /* Top progress bar — Linear-style indicator during script reruns */
        @keyframes pulse-loading-bar {
            0%   { transform: translateX(-100%); width: 30%; }
            50%  { transform: translateX(50%);   width: 60%; }
            100% { transform: translateX(200%);  width: 30%; }
        }
        [data-testid="stStatusWidget"][class*="running"]::before,
        [data-testid="stApp"]:has([data-testid="stSpinner"])::before {
            content: '';
            position: fixed;
            top: 0; left: 0;
            height: 2px;
            background: linear-gradient(90deg, var(--accent), var(--accent-hover));
            z-index: 99998;
            animation: pulse-loading-bar 1.4s cubic-bezier(0.4, 0, 0.2, 1) infinite;
            pointer-events: none;
        }

        /* Streak chip — glow animation when streak hits 30+ days.
           Glow radius kept small so it doesn't overlap with the H1 title next to it. */
        @keyframes pulse-streak-glow {
            0%, 100% { box-shadow: 0 0 0 0 var(--accent-bg), 0 0 4px 0 var(--accent); }
            50%      { box-shadow: 0 0 0 2px transparent, 0 0 10px 1px var(--accent); }
        }
        .pulse-streak-chip {
            position: relative;
            top: -1px;
        }
        .pulse-streak-elite {
            animation: pulse-streak-glow 2.4s ease-in-out infinite !important;
        }

        /* ECG / heartbeat line — Pulse signature visual.
           Use as decorative element between sections or behind hero numbers. */
        @keyframes pulse-ecg-flow {
            0%   { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }
        .pulse-ecg-line {
            height: 2px;
            background: linear-gradient(90deg,
                transparent 0%,
                var(--accent) 18%,
                var(--accent-hover) 24%,
                var(--accent) 30%,
                transparent 50%,
                var(--accent) 68%,
                var(--accent-hover) 74%,
                var(--accent) 80%,
                transparent 100%);
            background-size: 200% 100%;
            animation: pulse-ecg-flow 6s linear infinite;
            border-radius: 1px;
            opacity: 0.7;
        }
        @media (prefers-reduced-motion: reduce) {
            .pulse-ecg-line { animation: none !important; }
        }

        /* Skeleton shimmer — reusable loading placeholder */
        @keyframes pulse-skeleton-shimmer {
            0%   { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }
        .pulse-skeleton {
            background: linear-gradient(90deg,
                var(--bg-secondary) 0%,
                var(--bg-hover) 50%,
                var(--bg-secondary) 100%);
            background-size: 200% 100%;
            animation: pulse-skeleton-shimmer 1.4s ease-in-out infinite;
            border-radius: 6px;
            display: block;
        }
        .pulse-skeleton-text { height: 14px; margin: 4px 0; }
        .pulse-skeleton-card { height: 80px; margin-bottom: 8px; }
        .pulse-skeleton-bar  { height: 8px; }

        /* Empty state — illustrated, themed, friendly */
        .pulse-empty {
            text-align: center;
            padding: 36px 24px;
            border: 1px dashed var(--border);
            border-radius: 12px;
            background: var(--bg-secondary);
            color: var(--text-muted);
        }
        .pulse-empty-icon {
            width: 56px; height: 56px;
            margin: 0 auto 12px;
            color: var(--text-muted);
            opacity: 0.5;
        }
        .pulse-empty-title {
            font-size: 1rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 6px;
        }
        .pulse-empty-msg {
            font-size: 0.88rem;
            color: var(--text-secondary);
            max-width: 380px;
            margin: 0 auto;
            line-height: 1.5;
        }

        /* Page transition — subtle Y-translate fade for nav switches */
        @keyframes pulse-page-enter {
            from { opacity: 0.3; transform: translateY(6px); }
            to   { opacity: 1;   transform: translateY(0); }
        }
        [data-testid="stMain"] [data-testid="stMainBlockContainer"] > div:first-child {
            animation: pulse-page-enter 0.28s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* Slider — branded thumb with accent gradient */
        [data-testid="stSlider"] [role="slider"] {
            background: linear-gradient(135deg, var(--accent), var(--accent-hover)) !important;
            border: 2px solid var(--bg-card) !important;
            box-shadow: 0 1px 4px var(--accent-bg),
                        0 0 0 1px var(--accent-border) !important;
            width: 18px !important;
            height: 18px !important;
            transition: transform 0.12s ease, box-shadow 0.12s ease;
        }
        [data-testid="stSlider"] [role="slider"]:hover {
            transform: scale(1.15);
            box-shadow: 0 2px 6px var(--accent-bg),
                        0 0 0 2px var(--accent) !important;
        }
        /* Slider track — themed, subtle */
        [data-testid="stSlider"] [data-baseweb="slider"] > div {
            background: var(--border) !important;
        }
        [data-testid="stSlider"] [data-baseweb="slider"] > div > div {
            background: linear-gradient(90deg, var(--accent), var(--accent-hover)) !important;
        }

        /* Toast notifications — themed Streamlit st.toast() output */
        [data-testid="stToast"] {
            background: var(--bg-card) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border) !important;
            border-radius: 10px !important;
            box-shadow: var(--shadow-md) !important;
        }
        [data-testid="stToast"] svg { color: var(--accent) !important; }

        @media (prefers-reduced-motion: reduce) {
            .pulse-streak-elite,
            .pulse-skeleton,
            [data-testid="stMain"] [data-testid="stMainBlockContainer"] > div:first-child {
                animation: none !important;
            }
        }

        /* horizontal rule — theme-aware separator with generous breathing room */
        hr,
        [data-testid="stMarkdownContainer"] hr,
        [data-testid="stHorizontalRule"],
        [data-testid="stDivider"] {
            border: none !important;
            border-top: 1px solid var(--border-strong) !important;
            background: transparent !important;
            margin: 1.6rem 0 !important;
            height: 1px !important;
            color: var(--border-strong) !important;
        }
        /* st.divider() renders an inner element — color that too */
        [data-testid="stDivider"] > * {
            background: var(--border-strong) !important;
            border-color: var(--border-strong) !important;
        }

        /* input labels */
        [data-testid="stSelectbox"] label, [data-testid="stTextInput"] label,
        [data-testid="stNumberInput"] label, [data-testid="stDateInput"] label,
        [data-testid="stTextArea"] label, [data-testid="stCheckbox"] label {
            font-size: 0.82rem;
            color: var(--text-secondary);
            font-weight: 500;
        }

        /* input fields themed */
        .block-container [data-testid="stTextInput"] input,
        .block-container [data-testid="stNumberInput"] input,
        .block-container [data-testid="stDateInput"] input,
        .block-container [data-testid="stTextArea"] textarea {
            background: var(--bg-input);
            color: var(--text-primary);
            border-color: var(--border);
        }
        .block-container [data-testid="stSelectbox"] > div > div {
            background: var(--bg-input);
            color: var(--text-primary);
        }

        /* Streamlit alerts — themed by type. Streamlit's base theme (config.toml)
           is locked to "light" so its native alert renders with light bg even in
           our custom dark mode. Override every type explicitly. */
        [data-testid="stAlert"],
        [data-testid="stAlertContainer"] {
            border-radius: 8px !important;
        }
        [data-testid="stAlert"] [data-baseweb="notification"],
        [data-testid="stAlertContainer"] {
            color: var(--text-primary) !important;
            border: 1px solid var(--border);
        }
        /* st.success — green tint */
        [data-testid="stAlertContentSuccess"],
        .stAlert[data-baseweb="notification"][kind="positive"] [data-baseweb="notification"],
        [data-testid="stAlert"]:has([data-testid="stAlertContentSuccess"]),
        [data-testid="stAlert"]:has(svg[fill*="positive"]) {
            background: var(--success-bg) !important;
            border-color: var(--success-border) !important;
            color: var(--text-primary) !important;
        }
        /* st.error — red tint */
        [data-testid="stAlertContentError"],
        [data-testid="stAlert"]:has([data-testid="stAlertContentError"]) {
            background: var(--danger-bg) !important;
            border-color: var(--danger-border) !important;
            color: var(--text-primary) !important;
        }
        /* st.warning — amber tint */
        [data-testid="stAlertContentWarning"],
        [data-testid="stAlert"]:has([data-testid="stAlertContentWarning"]) {
            background: var(--warning-bg) !important;
            border-color: var(--warning-border) !important;
            color: var(--text-primary) !important;
        }
        /* st.info — accent tint */
        [data-testid="stAlertContentInfo"],
        [data-testid="stAlert"]:has([data-testid="stAlertContentInfo"]) {
            background: var(--accent-bg) !important;
            border-color: var(--accent-border) !important;
            color: var(--text-primary) !important;
        }
        /* All text inside alerts inherits theme color (overrides Streamlit dark text) */
        [data-testid="stAlert"] *,
        [data-testid="stAlertContainer"] * {
            color: var(--text-primary) !important;
        }
        /* Alert SVG icons — colored to match alert type */
        [data-testid="stAlertContentSuccess"] svg { color: var(--success) !important; }
        [data-testid="stAlertContentError"]   svg { color: var(--danger)  !important; }
        [data-testid="stAlertContentWarning"] svg { color: var(--warning) !important; }
        [data-testid="stAlertContentInfo"]    svg { color: var(--accent)  !important; }

        /* Streamlit slider — themed track + thumb */
        [data-testid="stSlider"] {
            color: var(--text-primary);
        }
        [data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
            background: var(--accent) !important;
            border-color: var(--accent) !important;
        }
        [data-testid="stSlider"] [data-baseweb="slider"] div[style*="background"] {
            background: var(--accent) !important;
        }
        [data-testid="stSlider"] [data-testid="stTickBar"] {
            color: var(--text-secondary) !important;
        }
        [data-testid="stSlider"] [data-testid="stThumbValue"] {
            color: var(--text-primary) !important;
            background: var(--bg-card) !important;
        }

        /* Streamlit native st.metric (used in Activity page) — themed */
        [data-testid="stMetric"] [data-testid="stMetricDelta"] {
            color: var(--text-secondary) !important;
        }
        [data-testid="stMetric"] [data-testid="stMetricDelta"] svg {
            color: var(--text-secondary) !important;
        }

        /* Tab panel content — text-primary */
        [data-testid="stTabs"] [data-baseweb="tab-panel"] {
            color: var(--text-primary);
        }

        /* Markdown/text containers */
        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        .stMarkdown {
            color: var(--text-primary);
        }
        [data-testid="stMarkdownContainer"] strong {
            color: var(--text-primary);
        }
        [data-testid="stMarkdownContainer"] a {
            color: var(--accent);
        }

        /* Streamlit popover/dialog — for menus that overlay content */
        [data-testid="stPopoverBody"] {
            background: var(--bg-card) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border) !important;
        }

        /* Custom HTML tables (.pulse-table) — replaces st.dataframe where full
           theming is required. Streamlit's dataframe uses Glide Data Grid which
           ignores our CSS variables. */
        .pulse-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            overflow: hidden;
            font-size: 0.84rem;
            font-variant-numeric: tabular-nums;
        }
        .pulse-table thead th {
            background: var(--bg-secondary);
            color: var(--text-secondary);
            font-weight: 600;
            text-align: left;
            padding: 11px 14px;
            border-bottom: 1px solid var(--border);
            text-transform: uppercase;
            font-size: 0.68rem;
            letter-spacing: 0.05em;
            white-space: nowrap;
        }
        .pulse-table thead th.num { text-align: right; }
        .pulse-table tbody td {
            color: var(--text-primary);
            padding: 10px 14px;
            border-bottom: 1px solid var(--border-subtle);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 200px;
        }
        .pulse-table tbody td.num {
            text-align: right;
            color: var(--text-secondary);
        }
        .pulse-table tbody td.strong { color: var(--text-primary); font-weight: 600; }
        .pulse-table tbody tr:last-child td { border-bottom: none; }
        .pulse-table tbody tr:hover { background: var(--bg-hover); }
        .pulse-table-wrap {
            max-height: 420px;
            overflow-y: auto;
            border-radius: 8px;
        }

        /* Top apps list — single redesigned view replacing chart+table */
        .top-apps-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 16px;
        }
        .top-app-row {
            display: grid;
            grid-template-columns: 26px 1fr 110px 75px;
            align-items: center;
            gap: 12px;
            padding: 8px 6px;
            border-radius: 6px;
            transition: background 0.15s ease;
        }
        .top-app-row:hover { background: var(--bg-hover); }
        .top-app-rank {
            font-size: 0.72rem;
            font-weight: 700;
            color: var(--text-muted);
            text-align: center;
            font-variant-numeric: tabular-nums;
        }
        .top-app-info { min-width: 0; }
        .top-app-name {
            font-size: 0.86rem;
            font-weight: 500;
            color: var(--text-primary);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .top-app-cat {
            font-size: 0.7rem;
            color: var(--text-muted);
            margin-top: 1px;
        }
        .top-app-bar {
            position: relative;
            height: 6px;
            background: var(--bg-hover);
            border-radius: 3px;
            overflow: hidden;
        }
        .top-app-bar-fill {
            position: absolute; left: 0; top: 0; bottom: 0;
            border-radius: 3px;
            transition: width 0.3s ease;
        }
        .top-app-bar-fill.productive {
            background: linear-gradient(90deg, var(--success) 0%, var(--accent) 100%);
        }
        .top-app-bar-fill.distraction {
            background: linear-gradient(90deg, var(--warning) 0%, var(--danger) 100%);
        }
        .top-app-hours {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-primary);
            text-align: right;
            font-variant-numeric: tabular-nums;
        }
        .top-app-hours-sub {
            font-size: 0.68rem;
            color: var(--text-muted);
            text-align: right;
        }

        /* Selectbox dropdown popup (portal'd outside main) — match theme */
        [data-baseweb="popover"] [data-baseweb="menu"],
        [data-baseweb="popover"] ul[role="listbox"] {
            background: var(--bg-card) !important;
            border: 1px solid var(--border) !important;
            color: var(--text-primary) !important;
        }
        [data-baseweb="popover"] li[role="option"] {
            color: var(--text-primary) !important;
        }
        [data-baseweb="popover"] li[role="option"]:hover,
        [data-baseweb="popover"] li[aria-selected="true"] {
            background: var(--bg-hover) !important;
            color: var(--accent) !important;
        }

        /* Date picker calendar — themed */
        [data-baseweb="calendar"] {
            background: var(--bg-card) !important;
            color: var(--text-primary) !important;
        }
        [data-baseweb="calendar"] [aria-selected="true"] {
            background: var(--accent) !important;
            color: var(--text-invert) !important;
        }

        /* Tooltip — readable on both themes */
        [data-baseweb="tooltip"] {
            background: var(--bg-card) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border);
            font-size: 0.8rem !important;
        }

        /* Number input increment/decrement buttons */
        [data-testid="stNumberInput"] button {
            background: var(--bg-input) !important;
            color: var(--text-secondary) !important;
            border-color: var(--border) !important;
        }
        [data-testid="stNumberInput"] button:hover {
            background: var(--bg-hover) !important;
            color: var(--accent) !important;
        }

        /* Code blocks — readable contrast in dark mode */
        code, pre {
            background: var(--bg-secondary) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--border);
        }

        /* Toolbar (top-right Streamlit menu) — match theme */
        [data-testid="stToolbar"] {
            background: transparent !important;
        }

        /* Caption (small grey text) */
        [data-testid="stMarkdownContainer"] code {
            font-size: 0.85em;
            padding: 1px 5px;
            border-radius: 3px;
        }

        /* subscription cards — subtle hover */
        .sub-card:hover {
            box-shadow: var(--shadow-md);
            transform: translateY(-1px);
        }

        /* Sub-action row — sits under the card with a small gap, NOT overlapping.
           Previous design tried to overlap (margin-top:-2px) which caused the
           dashed border to clip the card's bottom border. */
        .sub-actions-row + [data-testid="stHorizontalBlock"] {
            margin-top: 4px !important;
            margin-bottom: 18px !important;
            padding: 8px 10px !important;
            background: var(--bg-secondary);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            gap: 0.4rem !important;
        }
        /* Action buttons: smaller, ghost-like, text center, tightly packed */
        .sub-actions-row + [data-testid="stHorizontalBlock"] .stButton > button {
            font-size: 0.78rem !important;
            padding: 0 12px !important;
            height: 30px !important;
            min-height: 30px !important;
            border-radius: 6px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
        }

        /* popover — make it match brand */
        [data-testid="stPopover"] button {
            font-weight: 500;
        }

        /* tabs — Pulse style with breathing room */
        [data-testid="stTabs"] [data-baseweb="tab-list"] {
            gap: 8px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 12px;
        }
        [data-testid="stTabs"] [data-baseweb="tab"] {
            color: var(--text-secondary) !important;
            background: transparent !important;
            padding: 10px 18px !important;
            font-size: 0.92rem !important;
            font-weight: 500 !important;
            letter-spacing: -0.005em !important;
            border-bottom: 2px solid transparent !important;
            margin-bottom: -1px !important;
        }
        [data-testid="stTabs"] [data-baseweb="tab"]:hover {
            color: var(--text-primary) !important;
            background: var(--bg-hover) !important;
            border-radius: 6px 6px 0 0;
        }
        [data-testid="stTabs"] [aria-selected="true"] {
            color: var(--accent) !important;
            border-bottom: 2px solid var(--accent) !important;
            font-weight: 600 !important;
        }

        /* dataframe (Glide grid) — theme via gdg-* CSS variables.
           Glide reads these tokens to paint the canvas. Avoid touching the
           wrapper background — the canvas is drawn inside it and an opaque
           bg can occlude content. */
        [data-testid="stDataFrame"] {
            border: 1px solid var(--border);
            border-radius: 8px;
            overflow: hidden;
            --gdg-bg-cell: var(--bg-card);
            --gdg-bg-cell-medium: var(--bg-secondary);
            --gdg-bg-header: var(--bg-secondary);
            --gdg-bg-header-has-focus: var(--bg-hover);
            --gdg-bg-header-hovered: var(--bg-hover);
            --gdg-bg-bubble: var(--accent-bg);
            --gdg-bg-bubble-selected: var(--accent);
            --gdg-bg-search-result: var(--warning-bg);
            --gdg-text-dark: var(--text-primary);
            --gdg-text-medium: var(--text-secondary);
            --gdg-text-light: var(--text-muted);
            --gdg-text-bubble: var(--text-primary);
            --gdg-text-header: var(--text-secondary);
            --gdg-text-header-selected: var(--text-primary);
            --gdg-text-group-header: var(--text-secondary);
            --gdg-border-color: var(--border);
            --gdg-horizontal-border-color: var(--border-subtle);
            --gdg-accent-color: var(--accent);
            --gdg-accent-fg: var(--text-invert);
            --gdg-accent-light: var(--accent-bg);
            --gdg-link-color: var(--accent);
            --gdg-cell-horizontal-padding: 10px;
            --gdg-cell-vertical-padding: 6px;
        }

        /* Focus rings — keyboard accessibility */
        button:focus-visible, [role="button"]:focus-visible,
        input:focus-visible, select:focus-visible, textarea:focus-visible,
        [data-testid="stRadio"] label:focus-within {
            outline: 2px solid var(--accent) !important;
            outline-offset: 2px !important;
            border-radius: 6px;
        }

        /* Mobile responsive — under 700px, sidebar overlay style */
        @media (max-width: 700px) {
            [data-testid="stSidebar"] {
                position: fixed !important;
                z-index: 100;
                height: 100vh;
            }
            .block-container {
                padding-left: 12px;
                padding-right: 12px;
            }
            /* Stack KPI cards on mobile */
            [data-testid="column"] {
                min-width: 100% !important;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Helpers
# ============================================================
# ----- Currency: dynamic via fx.py + user setting -----

@st.cache_data(ttl=3600, show_spinner=False)
def cached_fx_rates() -> dict:
    """Cached FX rates for the dashboard (refreshes hourly)."""
    return fx.get_rates(base="USD")


def current_currency() -> str:
    """User's display currency. Read from settings (set during onboarding).
    Defaults to THB; user can override on the Settings page."""
    return get_setting("display_currency", "THB").upper()


# ----- Setting helpers (typed) -----
def setting_int(key: str, default: int) -> int:
    raw = get_setting(key, "")
    try:
        return int(raw) if raw else default
    except ValueError:
        return default


def setting_float(key: str, default: float) -> float:
    raw = get_setting(key, "")
    try:
        return float(raw) if raw else default
    except ValueError:
        return default


def setting_bool(key: str, default: bool) -> bool:
    raw = get_setting(key, "")
    if not raw:
        return default
    return raw.lower() in ("1", "true", "yes", "on")


# ----- Plan price (Anthropic Max default; user-editable in Settings) -----
def plan_monthly_usd() -> float:
    return setting_float("plan_monthly_usd", 200.0)


def usd_to_local(usd: float, currency: str | None = None) -> float:
    cur = (currency or current_currency()).upper()
    rates = cached_fx_rates()["rates"]
    return usd * rates.get(cur, 1.0)


def local_symbol(currency: str | None = None) -> str:
    return fx.symbol(currency or current_currency())


def to_usd(amount: float, currency: str) -> float:
    """Convert native amount to USD."""
    code = (currency or "USD").upper()
    if code == "USD":
        return amount
    rates = cached_fx_rates()["rates"]
    rate = rates.get(code, 1.0)
    return amount / rate if rate else amount


def fmt_local(usd: float, decimals: int = 0) -> str:
    """USD amount -> user-currency string. Symbol prefixed."""
    cur = current_currency()
    val = usd_to_local(usd, cur)
    return f"{fx.symbol(cur)}{val:,.{decimals}f}"


def fmt_local_compact(usd: float) -> str:
    """Compact form with K/M suffix for large amounts. e.g. 1,234,567 -> ฿1.2M."""
    cur = current_currency()
    val = usd_to_local(usd, cur)
    sym = fx.symbol(cur)
    abs_val = abs(val)
    if abs_val >= 1_000_000:
        return f"{sym}{val / 1_000_000:.1f}M"
    if abs_val >= 10_000:
        return f"{sym}{val / 1_000:.1f}K"
    return f"{sym}{val:,.0f}"


def fmt_local_2(usd: float) -> str:
    return fmt_local(usd, 2)


def fmt_usd_ref(usd: float, decimals: int = 2) -> str:
    """Small reference text showing USD amount."""
    return f"${usd:,.{decimals}f} USD"


def fmt_native(amount: float, native_currency: str) -> str:
    """Format an amount in its native currency."""
    code = (native_currency or "USD").upper()
    sym = fx.symbol(code)
    if code == "USD":
        return f"{sym}{amount:,.2f}"
    return f"{sym}{amount:,.2f}"


# ────────── Empty state illustrations ──────────
# Inline SVG icons — monochrome, theme-color via currentColor.
_SVG_ATTRS = (
    'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
    'stroke-linecap="round" stroke-linejoin="round" '
    'style="width:100%;height:100%;"'
)
ICON_CALENDAR_EMPTY = (
    f'<svg {_SVG_ATTRS}>'
    '<rect x="3" y="4" width="18" height="18" rx="2"/>'
    '<line x1="16" y1="2" x2="16" y2="6"/>'
    '<line x1="8" y1="2" x2="8" y2="6"/>'
    '<line x1="3" y1="10" x2="21" y2="10"/>'
    '<circle cx="12" cy="15" r="1.5" fill="currentColor"/>'
    '</svg>'
)
ICON_NO_ACTIVITY = (
    f'<svg {_SVG_ATTRS}>'
    '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>'
    '</svg>'
)
ICON_SEARCH_EMPTY = (
    f'<svg {_SVG_ATTRS}>'
    '<circle cx="11" cy="11" r="8"/>'
    '<line x1="21" y1="21" x2="16.65" y2="16.65"/>'
    '</svg>'
)
ICON_NO_DATA = (
    f'<svg {_SVG_ATTRS}>'
    '<circle cx="12" cy="12" r="10"/>'
    '<polyline points="8 12 11 15 16 9"/>'
    '</svg>'
)
ICON_INBOX = (
    f'<svg {_SVG_ATTRS}>'
    '<polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/>'
    '<path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>'
    '</svg>'
)


def pulse_empty(title: str, message: str, icon: str = ICON_NO_DATA) -> None:
    """Render a friendly illustrated empty state."""
    st.markdown(
        f'<div class="pulse-empty">'
        f'<div class="pulse-empty-icon">{icon}</div>'
        f'<div class="pulse-empty-title">{escape(title)}</div>'
        f'<div class="pulse-empty-msg">{message}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def pulse_table(df: pd.DataFrame, num_cols: list[str] | None = None,
                strong_cols: list[str] | None = None,
                col_labels: dict[str, str] | None = None,
                max_height: int | None = None) -> None:
    """Render a DataFrame as a fully-themed HTML table.
    `num_cols` get right-aligned tabular numerics.
    `strong_cols` get text-primary weight 600.
    `col_labels` rename headers (e.g. {'process_name': 'Process'}).
    `max_height` (px) wraps in a scroll container."""
    num_cols = set(num_cols or [])
    strong_cols = set(strong_cols or [])
    col_labels = col_labels or {}

    head = "".join(
        f'<th class="{"num" if c in num_cols else ""}">'
        f'{escape(str(col_labels.get(c, c)))}</th>'
        for c in df.columns
    )
    body_rows = []
    for _, r in df.iterrows():
        cells = []
        for c in df.columns:
            v = r[c]
            cls = []
            if c in num_cols: cls.append("num")
            if c in strong_cols: cls.append("strong")
            cls_attr = f' class="{" ".join(cls)}"' if cls else ""
            cells.append(f'<td{cls_attr}>{escape(str(v)) if v is not None else ""}</td>')
        body_rows.append(f'<tr>{"".join(cells)}</tr>')

    table_html = (
        f'<table class="pulse-table"><thead><tr>{head}</tr></thead>'
        f'<tbody>{"".join(body_rows)}</tbody></table>'
    )
    if max_height:
        table_html = (
            f'<div class="pulse-table-wrap" style="max-height:{max_height}px;">'
            f'{table_html}</div>'
        )
    st.markdown(table_html, unsafe_allow_html=True)


def kpi_card(label: str, primary: str, secondary: str | None = None,
             color: str = "default", help_text: str | None = None) -> None:
    """Render a KPI tile with optional small secondary text.
    `color` tints both the primary value AND the card background subtly."""
    color_css = {
        "default": "var(--text-primary)",
        "warning": "var(--warning)",
        "danger":  "var(--danger)",
        "success": "var(--success)",
        "accent":  "var(--accent)",
    }.get(color, "var(--text-primary)")
    tint_class = {
        "warning": " kpi-warning",
        "danger":  " kpi-danger",
        "success": " kpi-success",
        "accent":  " kpi-accent",
    }.get(color, "")
    title_attr = f' title="{help_text}"' if help_text else ""
    secondary_html = (
        f'<div style="font-size:0.72rem; color:var(--text-secondary); '
        f'font-variant-numeric:tabular-nums;">{secondary}</div>'
        if secondary else '<div style="height:0.85rem;"></div>'
    )
    st.markdown(
        f'<div class="kpi-card{tint_class}"{title_attr} '
        f'style="background:var(--bg-card); padding:12px 16px; '
        f'border:1px solid var(--border); border-radius:10px; box-shadow:var(--shadow-sm);">'
        f'<div style="font-size:0.7rem; color:var(--text-secondary); text-transform:uppercase; '
        f'letter-spacing:0.04em; margin-bottom:4px; font-weight:600;">{label}</div>'
        f'<div style="font-size:1.2rem; font-weight:700; color:{color_css}; '
        f'font-variant-numeric:tabular-nums; line-height:1.25; margin-bottom:2px;">{primary}</div>'
        f'{secondary_html}'
        f'</div>',
        unsafe_allow_html=True,
    )


def monthly_equiv(cost: float, cycle: str) -> float:
    """Monthly equivalent cost in the SAME currency the row is in."""
    cycle = (cycle or "").lower()
    if cycle == "yearly":     return cost / 12
    if cycle == "weekly":     return cost * 4.33
    if cycle == "daily":      return cost * 30
    if cycle == "one-time":   return 0.0  # not recurring
    return cost  # monthly default


def monthly_equiv_usd(row: dict) -> float:
    """Monthly equivalent in USD (for portfolio totals)."""
    return to_usd(monthly_equiv(row["cost"], row["billing_cycle"]),
                  row.get("currency", "USD"))


def days_since(d_iso: str | None) -> int | None:
    if not d_iso:
        return None
    try:
        return (date.today() - datetime.fromisoformat(d_iso).date()).days
    except Exception:
        return None


def smart_status(row: dict) -> tuple[str, str, str]:
    """Returns (color_key, label, message)."""
    if not row.get("active"):
        return "gray", "Cancelled", f"marked inactive · last charge {row.get('last_charge_date') or 'unknown'}"

    cycle = (row.get("billing_cycle") or "").lower()

    # One-time purchase — paid once, no renewals
    if cycle == "one-time":
        if (row.get("cost") or 0) == 0:
            return "amber", "Cost not set", "one-time purchase — add the amount"
        return "blue", "One-time purchase", f"paid {row.get('last_charge_date') or 'unknown'} — not recurring"

    # Active but cost not set → user needs to fill it in before we can value it
    if (row.get("cost") or 0) == 0:
        return "amber", "Cost not set", "click Edit to add the actual amount — currently counted as $0"

    d = days_since(row.get("last_charge_date"))

    if d is None:
        return "amber", "Unknown", "no charge history yet — re-scan Gmail"

    if cycle == "yearly":
        if d <= 380:
            return "green", "Active yearly", f"last charge {d} days ago — on schedule"
        return "red", "Likely cancelled", f"last charge {d} days ago — over 1 year"

    if cycle == "monthly":
        if d <= 35:    return "green", "Active monthly",       f"last charge {d} days ago"
        if d <= 60:    return "amber", "Late payment?",         f"last charge {d} days ago"
        if d <= 200:   return "blue",  "Reclassify as yearly",  f"no monthly charge for {d} days — likely yearly or cancelled"
        return "red", "Likely cancelled", f"no charge for {d} days — almost certainly inactive"

    if d <= 14:
        return "green", "Active", f"last charge {d} days ago"
    return "amber", "Verify", f"last charge {d} days ago"


def load_subscriptions(active_only: bool = False) -> pd.DataFrame:
    conn = get_conn()
    q = "SELECT * FROM subscriptions"
    if active_only:
        q += " WHERE active = 1"
    # Active first; within active, cost-not-set rows surface at top (need user attention),
    # then by cost DESC. Inactive rows last.
    q += " ORDER BY active DESC, CASE WHEN cost = 0 THEN 0 ELSE 1 END, cost DESC"
    return pd.read_sql_query(q, conn)


def load_app_usage(days: int) -> pd.DataFrame:
    conn = get_conn()
    since = (datetime.now() - timedelta(days=days)).isoformat(timespec="seconds")
    return pd.read_sql_query(
        "SELECT process_name, SUM(COALESCE(duration_seconds, 0))/3600.0 AS hours, "
        "COUNT(*) AS sessions, MAX(started_at) AS last_used "
        "FROM app_activity WHERE started_at > ? "
        "GROUP BY process_name ORDER BY hours DESC",
        conn, params=(since,),
    )


def page_header(title: str, caption: str, action_label: str | None = None, action_key: str | None = None) -> bool:
    """Render page title with optional action button on the right.
    Adds breathing room below the header so content doesn't crowd the title."""
    if action_label:
        col_t, col_a = st.columns([5, 1])
        with col_t:
            st.markdown(f"# {title}")
            st.caption(caption)
        with col_a:
            st.markdown('<div style="height: 12px;"></div>', unsafe_allow_html=True)
            clicked = st.button(action_label, key=action_key, use_container_width=True)
        st.markdown('<div style="height: 8px;"></div>', unsafe_allow_html=True)
        return clicked
    else:
        st.markdown(f"# {title}")
        st.caption(caption)
        st.markdown('<div style="height: 8px;"></div>', unsafe_allow_html=True)
        return False


# ============================================================
# First-run onboarding
# ============================================================
def run_onboarding() -> bool:
    """Returns True if onboarding is shown (and the rest of the page should skip)."""
    if get_setting("onboarded", "") == "1":
        return False

    st.markdown(
        '<div style="display:flex; align-items:center; gap:14px; margin-bottom:8px;">'
        '<div style="width:48px; height:48px; flex-shrink:0; '
        'filter:drop-shadow(0 1px 6px rgba(0,229,160,0.3));">'
        + _PULSE_LOGO_SVG +
        '</div>'
        f'<h1 style="margin:0;">Welcome to {APP_NAME}</h1>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.caption("30 seconds to set up. Everything is editable later in Settings.")

    with st.form("onboarding"):
        st.markdown("##### Where do you live?")
        currencies = ["THB", "USD", "EUR", "GBP", "JPY", "SGD", "MYR",
                      "CNY", "KRW", "AUD", "CAD", "HKD", "INR", "PHP", "IDR"]
        c = st.selectbox(
            "Display currency", currencies,
            help="All money will be shown in this currency. (FX auto-fetched daily.)"
        )

        st.markdown("##### Your AI subscription (optional)")
        plan = st.number_input(
            "Plan price per month (USD)", min_value=0.0, value=200.0, step=10.0,
            help="What you pay for Claude Max / ChatGPT Pro / similar. Used to compute ROI vs API equivalent.",
        )

        st.markdown("##### Budget alerts (optional — set 0 to disable)")
        c1, c2 = st.columns(2)
        with c1:
            daily = st.number_input("Daily token budget (USD)", min_value=0.0, value=50.0, step=10.0)
        with c2:
            monthly = st.number_input("Monthly token budget (USD)", min_value=0.0, value=500.0, step=50.0)

        spike = st.slider(
            "Spike alert: notify when daily cost exceeds X× your 30-day average",
            min_value=2.0, max_value=10.0, value=3.0, step=0.5,
        )

        st.markdown("##### Notifications")
        nc1, nc2, nc3 = st.columns(3)
        with nc1:
            n_renew = st.checkbox("Renewal alerts", value=True)
        with nc2:
            n_spike = st.checkbox("Cost spike alerts", value=True)
        with nc3:
            n_dead = st.checkbox("Unused-sub alerts", value=True)

        if st.form_submit_button("Get started", use_container_width=True, type="primary"):
            set_setting("display_currency", c)
            set_setting("plan_monthly_usd", str(plan))
            set_setting("token_daily_budget_usd", str(daily))
            set_setting("token_monthly_budget_usd", str(monthly))
            set_setting("alerts_token_spike_multiplier", str(spike))
            set_setting("alerts_renewals_enabled", "1" if n_renew else "0")
            set_setting("alerts_token_spike_enabled", "1" if n_spike else "0")
            set_setting("alerts_dead_subs_enabled", "1" if n_dead else "0")
            set_setting("onboarded", "1")
            st.rerun()
        return True
    return True


if run_onboarding():
    st.stop()


# ============================================================
# Sidebar
# ============================================================
with st.sidebar:
    # Brand row — logo + name on left, theme toggle on right (single flex row).
    # Material icons render as themeable SVG (always inherit color cleanly,
    # never get hijacked by the OS emoji font).
    current_theme = get_setting("theme", "light")
    if current_theme == "dark":
        toggle_label = ":material/light_mode:"   # click → switch to light
        next_theme = "light"
    else:
        toggle_label = ":material/dark_mode:"    # click → switch to dark
        next_theme = "dark"

    brand_col, toggle_col = st.columns([1, 0.32])
    with brand_col:
        st.markdown(
            f'<div class="pulse-brand-row">'
            f'<div class="pulse-logo-mark">{_PULSE_LOGO_SVG}</div>'
            f'<div class="pulse-brand-name">{APP_NAME}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with toggle_col:
        if st.button(
            toggle_label,
            key="theme_toggle_btn",
            use_container_width=True,
        ):
            # Don't clear cache — only theme tokens change. Clearing forces all
            # data queries to re-run, making toggle feel slow and jarring.
            set_setting("theme", next_theme)
            st.rerun()

    # Tagline (smaller, below)
    st.markdown(
        f'<div style="font-size:0.76rem; color:var(--text-muted); '
        f'margin: 2px 0 14px 0;">{APP_TAGLINE}</div>',
        unsafe_allow_html=True,
    )

    # Button-based nav (avoids radio state syncing with session_state)
    if "page" not in st.session_state:
        st.session_state["page"] = "Overview"

    nav_items = ["Overview", "Subscriptions", "Activity", "AI usage"]
    for label in nav_items:
        is_active = st.session_state["page"] == label
        if st.button(
            label,
            key=f"nav_{label}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            st.session_state["page"] = label
            st.rerun()

    page = st.session_state["page"]

    st.markdown("---")

    # Quick summary (all in USD-equivalent for cross-currency aggregation)
    all_subs_side = load_subscriptions(active_only=False)
    active_side = all_subs_side[all_subs_side["active"] == 1]
    if not active_side.empty:
        wasted_side = 0.0
        ok_monthly = 0.0
        attention = 0
        for _, row in active_side.iterrows():
            d = row.to_dict()
            color, _, _ = smart_status(d)
            me_usd = monthly_equiv_usd(d)
            if color == "red":
                wasted_side += me_usd
            else:
                ok_monthly += me_usd
            if color in ("amber", "blue"):
                attention += 1

        st.markdown(
            '<div style="font-size:0.68rem; color:var(--text-secondary); text-transform:uppercase; '
            'letter-spacing:0.05em; margin-bottom:2px;">SUMMARY</div>',
            unsafe_allow_html=True,
        )
        kpi_card("Real monthly", fmt_local(ok_monthly, 0), fmt_usd_ref(ok_monthly))
        if wasted_side > 0:
            kpi_card("Likely wasted",
                     f"{fmt_local(wasted_side, 0)}/mo",
                     fmt_usd_ref(wasted_side),
                     color="danger")
        if attention:
            kpi_card("Need attention", f"{attention}", color="warning")

        # Mini health bar — proportion of stack that's healthy (gradient red→green)
        total_side = ok_monthly + wasted_side
        if total_side > 0:
            health_pct = (ok_monthly / total_side) * 100
            health_label = (
                "Healthy" if health_pct >= 90
                else "Mostly OK" if health_pct >= 70
                else "Needs review" if health_pct >= 40
                else "Bleeding"
            )
            st.markdown(
                f'<div class="pulse-health-track" '
                f'title="Healthy {health_pct:.0f}% / Wasted {100-health_pct:.0f}%">'
                f'<div class="pulse-health-fill" style="width:{health_pct:.1f}%;"></div>'
                f'</div>'
                f'<div class="pulse-health-label">'
                f'<span>STACK HEALTH</span><span>{health_label}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # Gear at sidebar bottom — Settings as a tucked-away page, not main nav
    st.markdown(
        '<div style="flex:1;"></div>',  # spacer to push gear down (visual only)
        unsafe_allow_html=True,
    )
    st.markdown("")
    is_settings = st.session_state["page"] == "Settings"
    if st.button("Settings", key="gear_btn", use_container_width=True,
                  type="primary" if is_settings else "secondary"):
        st.session_state["page"] = "Settings" if not is_settings else "Overview"
        st.rerun()


# ============================================================
# PAGE: SUBSCRIPTIONS
# ============================================================
def render_subscription_row(d: dict) -> None:
    color = d["_color"]
    border = COLOR_VAR[color]
    sub_class = f"sub-card sub-{color}"
    cycle = d["billing_cycle"]
    cost = float(d["cost"])
    currency = d.get("currency", "USD")
    me = monthly_equiv(cost, cycle)            # in native currency
    me_usd = monthly_equiv_usd(d)              # in USD
    last = d.get("last_charge_date") or "—"
    nxt  = d.get("next_billing_date") or "—"
    sender = d.get("email_sender") or ""

    user_cur = current_currency()

    # Native cost in USD, then to local — for the BIG primary number
    native_usd = to_usd(cost, currency)            # the actual cost paid each cycle, USD
    native_local = usd_to_local(native_usd)        # same, in user's display currency

    # Primary cost label (top-right): actual cycle amount in local currency
    if cycle == "one-time":
        cost_local_str = fmt_local(native_usd, 2)
    else:
        cost_local_str = f"{fmt_local(native_usd, 2)}/{cycle}"

    # Native cost reference (shown small below the primary)
    if currency == user_cur:
        # Native already in display currency; show USD reference instead
        native_ref = fmt_usd_ref(native_usd)
    else:
        # User paid in a different currency; show what was actually paid
        sym = fx.symbol(currency)
        native_ref = f"paid {sym}{cost:,.2f} {currency}/{cycle}"

    # Cost-per-hour-of-use ROI (if linked_process is tracked)
    roi_str = ""
    linked_proc = d.get("linked_process")
    if linked_proc:
        conn = get_conn()
        row = conn.execute(
            "SELECT SUM(COALESCE(duration_seconds, 0)) AS sec "
            "FROM app_activity WHERE process_name = ? AND started_at > date('now', '-30 days')",
            (linked_proc,),
        ).fetchone()
        hours_30d = (row["sec"] or 0) / 3600 if row else 0
        if hours_30d > 0.1:
            cost_per_hour_usd = me_usd / hours_30d
            roi_str = f"{fmt_local(cost_per_hour_usd, 2)}/hr-of-use"
        elif hours_30d == 0:
            roi_str = "unused last 30d"

    # Secondary line — keep it short. Show only what isn't already on the card.
    # (last/next dates are already in the progress bar; cost is on the right)
    secondary_parts = []

    # Monthly equivalent only if cycle != monthly (avoid duplication)
    cycle_l = (cycle or "").lower()
    if cycle_l == "yearly":
        secondary_parts.append(f"≈ {fmt_local(me_usd, 0)}/mo")
    elif cycle_l in ("weekly", "daily"):
        secondary_parts.append(f"≈ {fmt_local(me_usd, 0)}/mo")

    if roi_str:
        secondary_parts.append(roi_str)

    if sender:
        # Truncate long senders
        s = sender if len(sender) < 36 else sender[:33] + "…"
        secondary_parts.append(escape(s))

    secondary = " · ".join(secondary_parts)

    # Cancel URL (separate small link below)
    cancel_url = d.get("cancel_url")
    cancel_link_html = ""
    if cancel_url:
        cancel_link_html = (
            f'<div style="font-size:0.78rem; margin-top:2px;">'
            f'<a href="{escape(cancel_url)}" target="_blank" '
            f'style="color:var(--accent); text-decoration:none;">→ Cancel / manage</a>'
            f'</div>'
        )

    # Renewal progress bar — visualize "X days through this cycle"
    progress_html = ""
    if d.get("active") and d.get("last_charge_date") and d.get("next_billing_date"):
        try:
            last_d = datetime.fromisoformat(d["last_charge_date"]).date()
            next_d = datetime.fromisoformat(d["next_billing_date"]).date()
            today_d = date.today()
            total_days = max((next_d - last_d).days, 1)
            elapsed = max((today_d - last_d).days, 0)
            pct = min(elapsed / total_days * 100, 100)
            days_left = (next_d - today_d).days
            label_left = (
                f"{days_left} days until renewal" if days_left > 0
                else ("today" if days_left == 0 else f"{-days_left} days overdue")
            )
            # Smooth gradient track: green → amber → red across full width.
            # A right-side cover hides the unfilled portion, so the visible
            # right edge naturally tracks the urgency color.
            progress_html = (
                f'<div style="margin-top:8px;">'
                f'<div style="display:flex; justify-content:space-between; '
                f'font-size:0.7rem; color:var(--text-secondary); margin-bottom:3px;">'
                f'<span>{label_left}</span>'
                f'<span>{pct:.0f}% through cycle</span>'
                f'</div>'
                f'<div style="position:relative; height:4px; border-radius:3px; '
                f'overflow:hidden; '
                f'background:linear-gradient(90deg, '
                f'var(--success) 0%, var(--warning) 65%, var(--danger) 100%);">'
                f'<div style="position:absolute; right:0; top:0; bottom:0; '
                f'width:{100-pct:.1f}%; background:var(--bg-hover);"></div>'
                f'</div></div>'
            )
        except Exception:
            pass

    name_html = escape(d["name"])
    label_html = escape(d["_label"])
    msg_html = escape(d["_msg"])
    notes_html = ""
    if d.get("notes"):
        notes_html = (
            f'<div style="font-size:0.78rem; color:var(--text-secondary); margin-top:6px; '
            f'padding:6px 10px; background:var(--bg-secondary); border-left:2px solid var(--border-strong); '
            f'border-radius:4px;">{escape(d["notes"])}</div>'
        )

    # Trial badge
    trial_badge_html = ""
    if d.get("is_trial"):
        trial_end_str = d.get("trial_ends_at") or ""
        trial_badge_html = (
            f'<span style="display:inline-block; padding:2px 8px; '
            f'background:var(--warning-bg); color:var(--warning); font-size:0.7rem; '
            f'font-weight:600; border-radius:999px; margin-left:6px;">'
            f'TRIAL{" · ends " + trial_end_str[:10] if trial_end_str else ""}</span>'
        )

    # Right-side cost block: primary local currency + secondary (USD ref or native paid)
    cost_block_html = (
        f'<div style="font-size:0.95rem; font-weight:600; '
        f'font-variant-numeric:tabular-nums; color:var(--text-primary); '
        f'white-space:nowrap; text-align:right;">{escape(cost_local_str)}</div>'
        f'<div style="font-size:0.72rem; color:var(--text-secondary); '
        f'font-variant-numeric:tabular-nums; text-align:right;">{escape(native_ref)}</div>'
    )

    st.markdown(
        f"""
<div class="{sub_class}" style="
            padding: 14px 16px;
            margin-top: 10px;
            background: var(--bg-card);
            border: 1px solid var(--border-subtle);
            border-radius: 10px;
            transition: all 0.15s ease;">
  <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:14px;">
    <div style="min-width:0; flex:1;">
      <div style="font-size:0.95rem; font-weight:600; color:var(--text-primary);">
        {name_html}{trial_badge_html}
      </div>
      <div style="font-size:0.82rem; margin-top:2px;">
        <span style="font-weight:600; color:{border};">{label_html}</span>
        <span style="color:var(--text-secondary);"> · {msg_html}</span>
      </div>
    </div>
    <div style="white-space:nowrap;">{cost_block_html}</div>
  </div>
  {(
    f'<div style="font-size:0.78rem; color:var(--text-secondary); margin-top:4px; '
    f'overflow:hidden; text-overflow:ellipsis; white-space:nowrap;" '
    f'title="{secondary}">{secondary}</div>'
  ) if secondary else ""}
  {cancel_link_html}
  {notes_html}
  {progress_html}
</div>
        """,
        unsafe_allow_html=True,
    )


def build_actions(d: dict) -> list[tuple[str, str, str]]:
    """Return list of (label, key, action) for this row's status."""
    actions = []
    color = d["_color"]
    if d["active"]:
        if color == "blue":
            actions.append(("Make yearly", f"yearly_{d['id']}", "yearly"))
        if color in ("blue", "red", "amber"):
            actions.append(("Cancel", f"cancel_{d['id']}", "cancel"))
        if color in ("amber", "blue"):
            actions.append(("Confirm", f"confirm_{d['id']}", "confirm"))
    else:
        actions.append(("Activate", f"reactivate_{d['id']}", "reactivate"))
    actions.append(("Edit", f"edit_{d['id']}", "edit"))
    # Two-click delete: change label to red "Confirm?" after first click
    if st.session_state.get(f"_pending_del_{d['id']}"):
        actions.append(("Confirm delete?", f"delete_{d['id']}", "delete"))
    else:
        actions.append(("Delete", f"delete_{d['id']}", "delete"))
    return actions


def handle_action(sid: int, action: str, current_cost: float | None = None) -> str | None:
    conn = get_conn()
    if action == "yearly":
        # Just change the cycle; keep cost as-is.
        # Reasoning: when smart_status flags "Reclassify as yearly", it's because
        # we saw a single annual charge that was mis-tagged as monthly. The
        # logged cost IS the yearly amount, not 1/12 of it.
        conn.execute(
            "UPDATE subscriptions SET billing_cycle='yearly' WHERE id=?", (sid,))
        conn.commit()
        return "Reclassified as yearly (cost unchanged — edit if wrong)"
    if action == "cancel":
        # Capture monthly USD equivalent at time of cancellation for lifetime savings
        row = conn.execute(
            "SELECT cost, currency, billing_cycle FROM subscriptions WHERE id=?", (sid,)
        ).fetchone()
        cancelled_monthly_usd = 0.0
        if row:
            d = {"cost": row["cost"], "currency": row["currency"],
                 "billing_cycle": row["billing_cycle"]}
            cancelled_monthly_usd = monthly_equiv_usd(d)
        conn.execute(
            "UPDATE subscriptions SET active=0, cancelled_at=?, cancelled_monthly_usd=? "
            "WHERE id=?",
            (datetime.now().isoformat(timespec="seconds"), cancelled_monthly_usd, sid),
        )
        conn.commit()
        return None
    if action == "confirm":
        conn.execute(
            "UPDATE subscriptions SET user_confirmed_at=? WHERE id=?",
            (datetime.now().isoformat(timespec="seconds"), sid))
        conn.commit()
        return None
    if action == "reactivate":
        # Clear stale dates — both last_charge_date and next_billing_date can be in
        # the past, which would make smart_status immediately re-flag the row.
        conn.execute(
            "UPDATE subscriptions SET active=1, last_charge_date=NULL, "
            "next_billing_date=NULL WHERE id=?", (sid,))
        conn.commit()
        return None
    if action == "edit":
        st.session_state["edit_id"] = sid
        return None
    if action == "delete":
        # Two-click confirmation pattern
        pending_key = f"_pending_del_{sid}"
        if st.session_state.get(pending_key):
            # Capture row for undo before deleting
            row = conn.execute(
                "SELECT * FROM subscriptions WHERE id=?", (sid,)
            ).fetchone()
            if row:
                st.session_state["_undo_delete"] = {
                    "row": dict(row),
                    "deleted_at": datetime.now().timestamp(),
                }
            conn.execute("DELETE FROM subscriptions WHERE id=?", (sid,))
            conn.commit()
            st.session_state.pop(pending_key, None)
            return f"Deleted '{row['name'] if row else ''}'. You can undo above."
        st.session_state[pending_key] = True
        return None  # rerun shows the "Confirm delete?" button
    return None


def render_subscription_form(all_subs: pd.DataFrame) -> None:
    """Edit/Add form. Pinned to the top of the page so users see it immediately
    after clicking Edit or Add."""
    edit_id = st.session_state.get("edit_id")
    show_add = st.session_state.get("show_add_form", False)
    if not (edit_id or show_add):
        return

    edit_row = None
    if edit_id:
        edit_row = next((r for r in all_subs.to_dict("records") if r["id"] == edit_id), None)
        if edit_row is None:
            # Stale state — clear it
            st.session_state.pop("edit_id", None)
            return

    title = f"Editing — {edit_row['name']}" if edit_row else "Add new subscription"
    st.markdown(
        f'<div style="background:var(--warning-bg); border:1px solid var(--warning-border); padding:6px 12px; '
        f'border-radius:6px; font-size:0.85rem; margin-bottom:8px;">'
        f'<strong>{title}</strong></div>',
        unsafe_allow_html=True,
    )

    with st.form("sub_form", clear_on_submit=False):
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            name = st.text_input(
                "Name", value=edit_row["name"] if edit_row else "",
                help="The service name as it appears on receipts (e.g. 'Anthropic Claude Max').",
            )
        with c2:
            cost = st.number_input(
                "Cost", min_value=0.0, step=1.0,
                value=float(edit_row["cost"]) if edit_row else 20.0,
                help="The amount you actually pay per cycle (NOT monthly equivalent).",
            )
        with c3:
            currencies = ["USD", "THB", "EUR", "GBP"]
            currency = st.selectbox(
                "Currency", currencies,
                index=currencies.index(edit_row["currency"]) if edit_row and edit_row["currency"] in currencies else 0,
                help="The currency you were charged in. Pulse converts to your display currency.",
            )
        c4, c5 = st.columns(2)
        with c4:
            cycles = ["monthly", "yearly", "weekly", "daily", "one-time"]
            cycle = st.selectbox(
                "Billing cycle", cycles,
                index=cycles.index(edit_row["billing_cycle"]) if edit_row and edit_row["billing_cycle"] in cycles else 0,
                help="How often you're charged. Use 'one-time' for permanent purchases like lifetime licenses.",
            )
        with c5:
            nb_default = date.today() + timedelta(days=30)
            if edit_row and edit_row.get("next_billing_date"):
                try:
                    nb_default = datetime.fromisoformat(edit_row["next_billing_date"]).date()
                except Exception:
                    pass
            nb = st.date_input(
                "Next billing", value=nb_default,
                help="Pulse will alert you a few days before this date.",
            )
        c6, c7 = st.columns(2)
        with c6:
            sender = st.text_input(
                "Email sender (auto-detect)",
                value=edit_row.get("email_sender", "") if edit_row else "",
                placeholder="billing@example.com",
                help="Email address that sends receipts. Used by Gmail discovery (advanced).",
            )
        with c7:
            linked = st.text_input(
                "Linked process",
                value=edit_row.get("linked_process", "") if edit_row else "",
                placeholder="Cursor.exe",
                help="The .exe name of the app this subscription unlocks. "
                     "Pulse uses it to compute cost-per-hour-of-use and detect unused subs.",
            )
        c8, c9 = st.columns(2)
        with c8:
            cancel_url = st.text_input(
                "Cancellation URL (optional)",
                value=edit_row.get("cancel_url", "") if edit_row else "",
                placeholder="https://service.com/account/cancel",
                help="One-click access from the subscription card",
            )
        with c9:
            # Tag input with autocomplete-style hint
            existing_tags = sorted({
                r.get("tag") for r in all_subs.to_dict("records")
                if r.get("tag")
            })
            tag_help = ("Existing tags: " + ", ".join(existing_tags[:6])) if existing_tags else "e.g. business, personal, family"
            tag = st.text_input(
                "Tag",
                value=edit_row.get("tag", "") if edit_row else "",
                help=tag_help,
                placeholder="business / personal / family",
            )

        # Trial detection
        trial_default = bool(edit_row.get("is_trial")) if edit_row else False
        trial_end_default = None
        if edit_row and edit_row.get("trial_ends_at"):
            try:
                trial_end_default = datetime.fromisoformat(edit_row["trial_ends_at"]).date()
            except Exception:
                pass

        is_trial = st.checkbox(
            "This is a free trial (alert me before it auto-renews)",
            value=trial_default,
        )
        trial_end = None
        if is_trial:
            trial_end = st.date_input(
                "Trial ends",
                value=trial_end_default or (date.today() + timedelta(days=14)),
                help="You'll get a notification 3 days before this date",
            )

        notes = st.text_area(
            "Notes",
            value=edit_row.get("notes", "") if edit_row else "",
            height=70,
        )

        csub1, csub2, _ = st.columns([1, 1, 4])
        with csub1:
            save = st.form_submit_button("Save", use_container_width=True, type="primary")
        with csub2:
            cancel_btn = st.form_submit_button("Cancel", use_container_width=True)

        if save:
            if not name:
                st.error("Name required")
            else:
                conn = get_conn()
                trial_iso = trial_end.isoformat() if (is_trial and trial_end) else None
                if edit_row:
                    conn.execute(
                        "UPDATE subscriptions SET name=?, cost=?, currency=?, billing_cycle=?, "
                        "next_billing_date=?, email_sender=?, linked_process=?, "
                        "cancel_url=?, tag=?, notes=?, is_trial=?, trial_ends_at=? WHERE id=?",
                        (name, cost, currency, cycle, nb.isoformat(),
                         sender or None, linked or None, cancel_url or None,
                         tag or None, notes or None,
                         1 if is_trial else 0, trial_iso, edit_id),
                    )
                else:
                    conn.execute(
                        "INSERT INTO subscriptions (name, cost, currency, billing_cycle, "
                        "next_billing_date, email_sender, linked_process, "
                        "cancel_url, tag, notes, is_trial, trial_ends_at) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (name, cost, currency, cycle, nb.isoformat(),
                         sender or None, linked or None, cancel_url or None,
                         tag or None, notes or None,
                         1 if is_trial else 0, trial_iso),
                    )
                conn.commit()
                st.session_state.pop("edit_id", None)
                st.session_state["show_add_form"] = False
                st.rerun()
        if cancel_btn:
            st.session_state.pop("edit_id", None)
            st.session_state["show_add_form"] = False
            st.rerun()

    st.markdown("---")


def render_subscriptions():
    add_clicked = page_header(
        "Subscriptions",
        "Everything you're paying for — and what you might not need.",
        action_label="+ Add",
        action_key="add_new_btn",
    )
    if add_clicked:
        st.session_state["show_add_form"] = True

    all_subs = load_subscriptions(active_only=False)

    # Undo-delete banner (shown for ~30s after a delete)
    undo = st.session_state.get("_undo_delete")
    if undo:
        age = datetime.now().timestamp() - undo.get("deleted_at", 0)
        if age < 30:
            ub1, ub2, ub3 = st.columns([5, 1, 1])
            with ub1:
                st.markdown(
                    f'<div style="background:var(--warning-bg); '
                    f'border:1px solid var(--warning-border); border-radius:8px; '
                    f'padding:8px 14px; font-size:0.88rem; color:var(--text-primary);">'
                    f'Deleted <strong>{escape(undo["row"].get("name", ""))}</strong>. '
                    f'<span style="color:var(--text-secondary);">'
                    f'({30 - int(age)}s to undo)</span></div>',
                    unsafe_allow_html=True,
                )
            with ub2:
                if st.button("Undo", key="undo_del_btn", type="primary",
                              use_container_width=True):
                    r = undo["row"]
                    conn = get_conn()
                    conn.execute(
                        "INSERT INTO subscriptions "
                        "(id, name, cost, currency, billing_cycle, next_billing_date, "
                        " linked_process, notes, active, created_at, last_charge_date, "
                        " last_charge_amount, email_sender, user_confirmed_at, "
                        " cancel_url, tag, is_trial, trial_ends_at) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (r.get("id"), r.get("name"), r.get("cost"), r.get("currency"),
                         r.get("billing_cycle"), r.get("next_billing_date"),
                         r.get("linked_process"), r.get("notes"), r.get("active"),
                         r.get("created_at"), r.get("last_charge_date"),
                         r.get("last_charge_amount"), r.get("email_sender"),
                         r.get("user_confirmed_at"), r.get("cancel_url"),
                         r.get("tag"), r.get("is_trial"), r.get("trial_ends_at")),
                    )
                    conn.commit()
                    st.session_state.pop("_undo_delete", None)
                    st.rerun()
            with ub3:
                if st.button("Dismiss", key="undo_dis_btn",
                              use_container_width=True):
                    st.session_state.pop("_undo_delete", None)
                    st.rerun()
        else:
            st.session_state.pop("_undo_delete", None)

    # Form pinned at top so it's always visible immediately after Edit/Add click
    render_subscription_form(all_subs)

    active = all_subs[all_subs["active"] == 1]

    needs_attention = 0
    likely_wasted = 0.0
    real_monthly = 0.0
    for _, row in active.iterrows():
        d = row.to_dict()
        color, _, _ = smart_status(d)
        me_usd = monthly_equiv_usd(d)
        if color in ("amber", "blue"):
            needs_attention += 1
        if color == "red":
            likely_wasted += me_usd
        else:
            real_monthly += me_usd

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi_card("Monthly", fmt_local_compact(real_monthly), fmt_usd_ref(real_monthly),
                 help_text=f"FX: 1 USD = {usd_to_local(1.0):.4f} {current_currency()}")
    with k2:
        kpi_card("Yearly", fmt_local_compact(real_monthly * 12), fmt_usd_ref(real_monthly * 12))
    with k3:
        kpi_card("Need attention", f"{needs_attention}",
                 color="warning" if needs_attention else "default")
    with k4:
        kpi_card("Likely wasted",
                 f"{fmt_local_compact(likely_wasted)}/mo" if likely_wasted else "—",
                 fmt_usd_ref(likely_wasted) if likely_wasted else None,
                 color="danger" if likely_wasted else "default")

    st.markdown("---")

    # Search + tag + sort + filter row
    all_tags = sorted({d.get("tag") or "" for d in all_subs.to_dict("records")})
    all_tags = [t for t in all_tags if t]  # remove empties

    # Row 1 — primary: search + filter chips (most common actions)
    r1c1, r1c1b, r1c2 = st.columns([3, 0.5, 5])
    with r1c1:
        # Persist search across reruns via key so it survives page interactions
        search_q = st.text_input(
            "Search", placeholder="Search subscriptions…",
            label_visibility="collapsed",
            key="sub_search_input",
        ).strip().lower()
    with r1c1b:
        # Clear button — empty if no search, X if active
        if search_q:
            if st.button("×", key="sub_search_clear", help="Clear search"):
                st.session_state["sub_search_input"] = ""
                st.rerun()
    with r1c2:
        flt_short = st.radio(
            "Filter",
            ["Active", "Attention", "Off?", "History", "All"],
            horizontal=True,
            label_visibility="collapsed",
        )
        flt = {
            "Active": "All active",
            "Attention": "Needs attention",
            "Off?": "Likely cancelled",
            "History": "Cancelled (history)",
            "All": "All",
        }[flt_short]

    # Default sort: by cost descending (no UI clutter for these — power users
    # can re-sort by clicking the dataframe header in About → Diagnostics if needed)
    sort_choice = "Cost ↓"
    tag_choice = "All tags"

    # (Tools moved to Settings → Data — keeps the subscriptions page focused on daily use)

    rows_to_show = []
    for _, row in all_subs.iterrows():
        d = row.to_dict()
        color, label, msg = smart_status(d)
        d["_color"], d["_label"], d["_msg"] = color, label, msg
        if flt == "All active" and not d["active"]:                              continue
        if flt == "Needs attention"     and color not in ("amber", "blue"):      continue
        if flt == "Likely cancelled"    and not (d["active"] and color == "red"): continue
        if flt == "Cancelled (history)" and d["active"]:                         continue
        # Search across name, notes, tag, sender
        if search_q:
            haystack = " ".join(filter(None, [
                str(d.get("name") or ""),
                str(d.get("notes") or ""),
                str(d.get("tag") or ""),
                str(d.get("email_sender") or ""),
            ])).lower()
            if search_q not in haystack:
                continue
        if tag_choice and tag_choice != "All tags":
            if (d.get("tag") or "") != tag_choice:
                continue
        rows_to_show.append(d)

    # Apply sort to visible rows (after filter)
    def _sort_key(d, key):
        v = d.get(key)
        # Sort missing values last; dates/strings handled
        if v is None or v == "":
            return (1, "")
        return (0, v)

    if sort_choice == "Cost ↓":
        rows_to_show.sort(key=lambda d: monthly_equiv_usd(d), reverse=True)
    elif sort_choice == "Cost ↑":
        rows_to_show.sort(key=lambda d: monthly_equiv_usd(d))
    elif sort_choice == "Name":
        rows_to_show.sort(key=lambda d: (d.get("name") or "").lower())
    elif sort_choice == "Next renewal":
        rows_to_show.sort(key=lambda d: _sort_key(d, "next_billing_date"))
    elif sort_choice == "Recent charge":
        rows_to_show.sort(key=lambda d: _sort_key(d, "last_charge_date"), reverse=True)

    # Many-subs quip banner (above the list)
    many_subs_quip = quips.for_sub_count(len(active))
    if many_subs_quip:
        st.markdown(
            f'<div style="margin-bottom:6px; font-size:0.85rem; color:var(--text-secondary); '
            f'font-style:italic; padding-left:4px;">{escape(many_subs_quip)}</div>',
            unsafe_allow_html=True,
        )

    # Smart suggestion: apps used heavily but no linked subscription
    conn = get_conn()
    linked_set = set()
    for _, s in active.iterrows():
        lp = s.get("linked_process")
        if isinstance(lp, str) and lp.strip():
            linked_set.add(lp.strip().lower())
    suspect_apps = pd.read_sql_query(
        "SELECT process_name, SUM(COALESCE(duration_seconds, 0))/3600.0 AS hours "
        "FROM app_activity WHERE started_at > date('now', '-30 days') "
        "GROUP BY process_name HAVING hours > 10 "
        "ORDER BY hours DESC LIMIT 30",
        conn,
    )
    # Filter out: system apps, browsers, terminals, and already-linked
    EXCLUDE_KEYWORDS = {
        "explorer", "dwm", "svchost", "taskmgr", "settings", "searchhost",
        "textinputhost", "startmenu", "shellexp", "widgets", "lockapp",
        "crossdevice", "phoneex", "runtimebroker", "sihost", "ctfmon",
        "chrome", "msedge", "edge.exe", "firefox", "brave", "opera",
        "windowsterminal", "powershell", "cmd.exe", "wsl", "bash",
        "applicationframehost",
    }
    suggestions = []
    for _, r in suspect_apps.iterrows():
        proc = r["process_name"]
        proc_l = proc.lower()
        if any(kw in proc_l for kw in EXCLUDE_KEYWORDS):
            continue
        if proc_l in linked_set:
            continue
        suggestions.append((proc, float(r["hours"])))
        if len(suggestions) >= 3:
            break

    if suggestions and not st.session_state.get("dismiss_suggestions"):
        items_html = ""
        for proc, hrs in suggestions:
            items_html += (
                f'<li style="margin-bottom:4px;">'
                f'<strong>{escape(proc)}</strong> '
                f'<span style="color:var(--text-secondary);">— used {hrs:.1f}h '
                f'in 30 days but no subscription linked</span>'
                f'</li>'
            )
        ds1, ds2 = st.columns([6, 1])
        with ds1:
            st.markdown(
                f'<div style="background:var(--accent-bg); '
                f'border:1px solid var(--accent-border); border-radius:8px; '
                f'padding:10px 14px; margin-bottom:10px; font-size:0.88rem;">'
                f'<div style="font-weight:600; color:var(--accent); '
                f'margin-bottom:4px;">Tracking suggestions</div>'
                f'<div style="color:var(--text-secondary); margin-bottom:6px;">'
                f'You use these apps a lot. Add them as subscriptions to track '
                f'cost-per-hour-of-use.</div>'
                f'<ul style="margin:0; padding-left:20px; color:var(--text-primary);">'
                f'{items_html}</ul></div>',
                unsafe_allow_html=True,
            )
        with ds2:
            if st.button("Dismiss", key="dismiss_suggest_btn"):
                st.session_state["dismiss_suggestions"] = True
                st.rerun()

    if not rows_to_show:
        if all_subs.empty:
            # First-run empty state — friendly nudge with quip
            empty_quip = quips.for_empty()
            st.markdown(
                f'<div style="padding:36px; text-align:center; '
                f'background:{ACCENT_BG}; border:1px dashed {ACCENT_BORDER}; '
                f'border-radius:12px; margin-top:16px;">'
                f'<div style="font-size:1.05rem; font-weight:600; color:var(--text-primary); '
                f'margin-bottom:6px;">{escape(empty_quip)}</div>'
                f'<div style="font-size:0.9rem; color:var(--text-secondary); max-width:380px; '
                f'margin:0 auto 14px;">Add your first subscription and Pulse will track '
                f'when it renews, what you really pay, and whether you actually use it.</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            pulse_empty(
                "No matches",
                "Try clearing the search or switching to <strong>All</strong>.",
                ICON_SEARCH_EMPTY,
            )
    else:
        for d in rows_to_show:
            render_subscription_row(d)

            actions = build_actions(d)
            n = len(actions)
            # Buttons right-aligned: spacer on left, buttons on right.
            # Wrapper class lets CSS visually attach this row to the card above.
            st.markdown(
                '<div class="sub-actions-row"></div>',
                unsafe_allow_html=True,
            )
            ratios = [max(1, 12 - 2 * n)] + [2] * n
            cols = st.columns(ratios)
            for i, (label, key, action) in enumerate(actions):
                with cols[i + 1]:
                    if st.button(label, key=key, use_container_width=True):
                        msg = handle_action(d["id"], action, current_cost=d["cost"])
                        if msg:
                            st.success(msg)
                        st.rerun()

    # CSV import dialog
    if st.session_state.get("show_csv_import"):
        with st.expander("Import subscriptions from CSV", expanded=True):
            st.caption(
                "CSV columns required: `name, cost, currency, billing_cycle`. "
                "Optional: `next_billing_date, last_charge_date, email_sender, "
                "linked_process, cancel_url, tag, notes`."
            )
            uploaded = st.file_uploader("Upload CSV", type=["csv"], key="csv_uploader")
            if uploaded is not None:
                try:
                    df = pd.read_csv(uploaded)
                    st.dataframe(df.head(20), hide_index=True, use_container_width=True)
                    if st.button(f"Import {len(df)} rows", type="primary"):
                        conn = get_conn()
                        n = 0
                        for _, row in df.iterrows():
                            try:
                                conn.execute(
                                    "INSERT INTO subscriptions "
                                    "(name, cost, currency, billing_cycle, next_billing_date, "
                                    " last_charge_date, email_sender, linked_process, cancel_url, "
                                    " tag, notes, active) "
                                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)",
                                    (
                                        row.get("name"),
                                        float(row.get("cost", 0) or 0),
                                        row.get("currency", "USD"),
                                        row.get("billing_cycle", "monthly"),
                                        row.get("next_billing_date") or None,
                                        row.get("last_charge_date") or None,
                                        row.get("email_sender") or None,
                                        row.get("linked_process") or None,
                                        row.get("cancel_url") or None,
                                        row.get("tag") or None,
                                        row.get("notes") or None,
                                    ),
                                )
                                n += 1
                            except Exception as e:
                                st.warning(f"Row '{row.get('name')}' failed: {e}")
                        conn.commit()
                        st.session_state["show_csv_import"] = False
                        st.toast(f"Imported {n} subscriptions", icon=":material/check_circle:")
                        st.rerun()
                except Exception as e:
                    st.error(f"Failed to read CSV: {e}")
            if st.button("Close"):
                st.session_state["show_csv_import"] = False
                st.rerun()

    with st.expander("Tips"):
        st.markdown(
            "- **Use the Cancellation URL** field — keeps cancel links one click away.\n"
            "- **Tag** subscriptions as `business` / `personal` / `family` for easier review at tax time.\n"
            "- **Export .ics** to see all renewals in your calendar — never miss one.\n"
            "- **Cost-per-hour-of-use** appears under each row when you set a `Linked process`."
        )


# ============================================================
# PAGE: APP USAGE
# ============================================================
def render_apps():
    page_header("Activity", "Where your time actually goes — auto-categorized")

    # Detect actual data span
    conn = get_conn()
    span_row = pd.read_sql_query(
        "SELECT MIN(started_at) AS first, MAX(started_at) AS last, COUNT(*) AS n FROM app_activity",
        conn,
    ).iloc[0]
    n_rows = int(span_row["n"]) if span_row["n"] is not None else 0

    if n_rows == 0:
        pulse_empty(
            "No activity yet",
            "Pulse is waiting for you to use your computer. Activity tracking "
            "captures foreground apps every 5 seconds and pauses when you're idle.",
            ICON_NO_ACTIVITY,
        )
        return

    first_seen = datetime.fromisoformat(span_row["first"])
    span_days = max(1, (datetime.now() - first_seen).days)
    span_hours = (datetime.now() - first_seen).total_seconds() / 3600

    if span_hours < 24:
        st.caption(
            f"Tracker started {span_hours:.1f} hours ago — only today's data is available. "
            f"Range slider will show meaningful results after a few days of tracking."
        )
        days_apps = 1
    else:
        max_range = min(30, span_days + 1)
        days_apps = st.slider(
            f"Range (days) — {span_days} day(s) of history available",
            1, max_range, min(7, max_range),
            key="apps_range",
        )

    usage_t = load_app_usage(days=days_apps)
    if usage_t.empty:
        st.info("No app activity in this range.")
        return

    total_h = usage_t["hours"].sum()
    top_app = usage_t.iloc[0]["process_name"] if len(usage_t) else "—"

    k1, k2, k3 = st.columns(3)
    k1.metric("Apps tracked", f"{len(usage_t)}")
    k2.metric("Total hours",  f"{total_h:.1f}h")
    k3.metric("Most used",    top_app[:24])

    st.markdown("---")

    # Add categories
    full = usage_t.copy()
    full["category"] = full["process_name"].apply(lambda p: categories.classify(p)[0])
    full["distraction"] = full["process_name"].apply(lambda p: categories.classify(p)[1])

    # Category summary
    by_cat = full.groupby("category", as_index=False).agg(
        hours=("hours", "sum"),
        apps=("process_name", "count"),
    ).sort_values("hours", ascending=False)
    by_cat["hours"] = by_cat["hours"].round(2)

    distraction_h = full[full["distraction"]]["hours"].sum()
    productive_h = full[~full["distraction"]]["hours"].sum()

    # Both columns share the same content height for visual balance.
    # 5 top-app rows × ~46px + container padding/gap ≈ 280px
    PANEL_H = 300

    cc1, cc2 = st.columns([1, 2])
    with cc1:
        st.markdown("**By category**")
        cat_display = by_cat.copy()
        cat_display["hours"] = cat_display["hours"].apply(lambda v: f"{v:.1f}h")
        cat_display["apps"] = cat_display["apps"].apply(lambda v: f"{int(v)}")
        pulse_table(
            cat_display[["category", "hours", "apps"]],
            num_cols=["hours", "apps"],
            strong_cols=["category"],
            col_labels={"category": "Category", "hours": "Hours", "apps": "Apps"},
            max_height=PANEL_H,
        )
        if distraction_h > 0:
            ratio = distraction_h / max(distraction_h + productive_h, 0.001) * 100
            st.caption(f"Distraction time: {distraction_h:.1f}h ({ratio:.0f}% of tracked)")
    with cc2:
        top = full.head(5).copy()
        top["hours"] = top["hours"].round(2)

        # Header row: title (left) + inline legend (right) — keeps the bottom
        # of the panel clean for the actual data.
        st.markdown(
            '<div style="display:flex; justify-content:space-between; align-items:center; '
            'margin-bottom:8px; gap:12px;">'
            '<div style="font-weight:600; font-size:0.95rem; color:var(--text-primary);">'
            'Top apps</div>'
            '<div style="display:flex; gap:14px; font-size:0.7rem; '
            'color:var(--text-muted); align-items:center;">'
            '<span style="display:inline-flex; align-items:center;">'
            '<span style="display:inline-block; width:10px; height:6px; '
            'border-radius:2px; background:linear-gradient(90deg, var(--success), var(--accent)); '
            'margin-right:5px;"></span>Productive</span>'
            '<span style="display:inline-flex; align-items:center;">'
            '<span style="display:inline-block; width:10px; height:6px; '
            'border-radius:2px; background:linear-gradient(90deg, var(--warning), var(--danger)); '
            'margin-right:5px;"></span>Distraction</span>'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        # Single redesigned list: rank · name+category · gradient bar · hours.
        # Replaces the chart+table pair with a cleaner, more scannable layout.
        max_h = float(top["hours"].max()) if not top.empty else 1.0
        rows_html = []
        for i, r in enumerate(top.itertuples(index=False), start=1):
            hrs = float(r.hours)
            pct = (hrs / max_h * 100) if max_h > 0 else 0
            cls_distraction = "distraction" if bool(getattr(r, "distraction", False)) else "productive"
            sess = getattr(r, "sessions", 0)
            sess_str = f"{int(sess)} session{'s' if int(sess) != 1 else ''}"
            rows_html.append(
                f'<div class="top-app-row">'
                f'<div class="top-app-rank">{i}</div>'
                f'<div class="top-app-info">'
                f'<div class="top-app-name">{escape(str(r.process_name))}</div>'
                f'<div class="top-app-cat">{escape(str(r.category))}</div>'
                f'</div>'
                f'<div class="top-app-bar">'
                f'<div class="top-app-bar-fill {cls_distraction}" '
                f'style="width:{pct:.1f}%;"></div>'
                f'</div>'
                f'<div>'
                f'<div class="top-app-hours">{hrs:.1f}h</div>'
                f'<div class="top-app-hours-sub">{sess_str}</div>'
                f'</div>'
                f'</div>'
            )
        st.markdown(
            f'<div class="top-apps-list" '
            f'style="height:{PANEL_H}px; overflow-y:auto;">{"".join(rows_html)}</div>',
            unsafe_allow_html=True,
        )


# ============================================================
# PAGE: TOKEN SPEND — Today / This month / All time, ccusage-style
# ============================================================

# Sonnet uniform rates (USD per million tokens) — used for "extension parity" mode.
SONNET_RATES = {
    "input": 3.0, "output": 15.0,
    "cw_5m": 3.75, "cw_1h": 6.0,
    "cache_read": 0.30,
}


def _period_window(period: str) -> tuple[str, str, str]:
    """Return (since_iso, granularity, time_format) for a period key."""
    now = datetime.now()
    if period == "today":
        since = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return since.isoformat(timespec="seconds"), "hour", "%H:00"
    if period == "month":
        since = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return since.isoformat(timespec="seconds"), "day", "%Y-%m-%d"
    # all time
    return "1970-01-01T00:00:00", "day", "%Y-%m-%d"


def _cost_expr(mode: str) -> str:
    """SQL expression that aggregates cost. Switches between per-model rate
    (uses cost_usd computed at sync time) and uniform Sonnet rate."""
    if mode == "per_model":
        return "COALESCE(SUM(cost_usd), 0)"
    r = SONNET_RATES
    return (
        "("
        f"SUM(input_tokens) * {r['input']:.4f} + "
        f"SUM(output_tokens) * {r['output']:.4f} + "
        f"SUM(cache_creation_5m_tokens) * {r['cw_5m']:.4f} + "
        f"SUM(cache_creation_1h_tokens) * {r['cw_1h']:.4f} + "
        # Fallback for rows without TTL breakdown (treat unspilt as 5min)
        f"(SUM(cache_creation_tokens) - SUM(cache_creation_5m_tokens) - SUM(cache_creation_1h_tokens)) * {r['cw_5m']:.4f} + "
        f"SUM(cache_read_tokens) * {r['cache_read']:.4f}"
        ") / 1000000.0"
    )


@st.cache_data(ttl=60, show_spinner=False)
def load_token_period(period: str, pricing_mode: str) -> dict:
    """Pricing_mode: 'per_model' (accurate) or 'sonnet' (uniform Sonnet rate)."""
    conn = get_conn()
    since, granularity, _ = _period_window(period)
    cost_sql = _cost_expr(pricing_mode)

    # Bucket timestamps in the user's LOCAL timezone (SQLite 'localtime' modifier).
    # Claude Code writes UTC timestamps; converting to local makes hourly buckets
    # show actual time-of-day usage in the user's clock, not UTC.
    if granularity == "hour":
        ts_expr = "strftime('%Y-%m-%dT%H:00:00', timestamp, 'localtime')"
    else:
        ts_expr = "DATE(timestamp, 'localtime')"

    series = pd.read_sql_query(
        f"""
        SELECT {ts_expr} AS bucket,
               {cost_sql} AS cost,
               SUM(input_tokens) AS input_tok,
               SUM(output_tokens) AS output_tok,
               SUM(cache_creation_tokens) AS cache_w_tok,
               SUM(cache_read_tokens) AS cache_r_tok,
               COUNT(*) AS messages
        FROM token_usage WHERE timestamp >= ?
        GROUP BY bucket ORDER BY bucket
        """,
        conn, params=(since,),
    )

    by_model = pd.read_sql_query(
        f"""
        SELECT model,
               COUNT(*) AS messages,
               SUM(input_tokens) AS input_tok,
               SUM(output_tokens) AS output_tok,
               SUM(cache_creation_tokens) AS cache_w_tok,
               SUM(cache_read_tokens) AS cache_r_tok,
               {cost_sql} AS cost
        FROM token_usage WHERE timestamp >= ?
        GROUP BY model ORDER BY cost DESC
        """,
        conn, params=(since,),
    )

    by_project = pd.read_sql_query(
        f"""
        SELECT project_tag,
               COUNT(*) AS messages,
               SUM(input_tokens + output_tokens + cache_creation_tokens + cache_read_tokens) AS total_tok,
               {cost_sql} AS cost
        FROM token_usage WHERE timestamp >= ?
        GROUP BY project_tag ORDER BY cost DESC LIMIT 20
        """,
        conn, params=(since,),
    )

    grand = pd.read_sql_query(
        f"""
        SELECT COUNT(*) AS messages,
               {cost_sql} AS cost,
               COALESCE(SUM(input_tokens), 0) AS input_tok,
               COALESCE(SUM(output_tokens), 0) AS output_tok,
               COALESCE(SUM(cache_creation_tokens), 0) AS cache_w_tok,
               COALESCE(SUM(cache_read_tokens), 0) AS cache_r_tok,
               MIN(timestamp) AS first_ts,
               MAX(timestamp) AS last_ts
        FROM token_usage WHERE timestamp >= ?
        """,
        conn, params=(since,),
    ).iloc[0]

    return {
        "series": series, "by_model": by_model, "by_project": by_project,
        "grand": grand, "granularity": granularity,
    }


def fmt_tokens(n) -> str:
    n = int(n or 0)
    if n >= 1_000_000:
        return f"{n / 1_000_000:.2f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return f"{n}"


def render_plan_roi(grand, period: str) -> None:
    """Show 'value vs Max plan' callout — celebrate when ROI is high.
    Big, prideful display with rating stars, savings number, and progress bar."""
    cost = float(grand["cost"]) if grand["cost"] is not None else 0.0
    first_ts = grand.get("first_ts")
    last_ts = grand.get("last_ts")
    if not first_ts or not last_ts or cost <= 0:
        return
    try:
        first = datetime.fromisoformat(first_ts[:19])
        last  = datetime.fromisoformat(last_ts[:19])
    except Exception:
        return
    span_days = max((last - first).days, 1)
    plan_per_month = plan_monthly_usd()
    plan_cost_usd = (span_days / 30.0) * plan_per_month
    if plan_cost_usd <= 0:
        return
    roi = cost / plan_cost_usd
    savings_usd = max(cost - plan_cost_usd, 0)
    deficit_usd = max(plan_cost_usd - cost, 0)

    # Rating tier — gives the user a tangible "achievement level"
    if roi >= 10:
        title, badge_text = "Legendary value", "Top 1% efficiency"
        emotion = "You're an absolute power user — getting elite mileage out of this plan."
        stars_filled = 5
        tone_bg, tone_border, tone_color = "var(--success-bg)", "var(--success-border)", "var(--success)"
    elif roi >= 5:
        title, badge_text = "Excellent value", "Power user"
        emotion = "Outstanding ROI. The plan is working hard for you."
        stars_filled = 5
        tone_bg, tone_border, tone_color = "var(--success-bg)", "var(--success-border)", "var(--success)"
    elif roi >= 2:
        title, badge_text = "Great value", "Smart spender"
        emotion = "Plan more than pays for itself. Keep it going."
        stars_filled = 4
        tone_bg, tone_border, tone_color = "var(--success-bg)", "var(--success-border)", "var(--success)"
    elif roi >= 1:
        title, badge_text = "Plan paying off", "Break-even"
        emotion = "Covering its cost. Use AI more to unlock bigger savings."
        stars_filled = 3
        tone_bg, tone_border, tone_color = "var(--accent-bg)", "var(--accent-border)", "var(--accent)"
    elif roi >= 0.5:
        title, badge_text = "Underused", "Below break-even"
        emotion = "You'd save by paying per-API right now — or use the plan more."
        stars_filled = 2
        tone_bg, tone_border, tone_color = "var(--warning-bg)", "var(--warning-border)", "var(--warning)"
    else:
        title, badge_text = "Plan idle", "Consider downgrading"
        emotion = "AI usage is far below the plan cost. Use more or switch."
        stars_filled = 1
        tone_bg, tone_border, tone_color = "var(--warning-bg)", "var(--warning-border)", "var(--warning)"

    stars_html = (
        '<span style="color:' + tone_color + '; letter-spacing:3px; font-size:0.95rem;">'
        + ("★" * stars_filled)
        + '<span style="color:var(--border-strong);">'
        + ("★" * (5 - stars_filled))
        + '</span></span>'
    )

    # Visual progress: % of API cost the plan paid for (capped at 100%).
    # If ROI > 1, the plan covered <100% of API cost (good — you got more than paid).
    coverage_pct = min((plan_cost_usd / cost) * 100, 100) if cost > 0 else 0

    if savings_usd > 0:
        savings_block = (
            f'<div style="margin-top:14px; padding:12px 14px; background:var(--bg-card); '
            f'border:1px solid var(--border); border-radius:10px;">'
            f'<div style="font-size:0.7rem; color:var(--text-secondary); '
            f'text-transform:uppercase; letter-spacing:0.06em; font-weight:600;">YOU SAVED</div>'
            f'<div style="font-size:1.8rem; font-weight:800; color:{tone_color}; '
            f'line-height:1.1; margin-top:2px; font-variant-numeric:tabular-nums;">'
            f'{fmt_local_compact(savings_usd)}</div>'
            f'<div style="font-size:0.78rem; color:var(--text-muted); margin-top:2px;">'
            f'{fmt_usd_ref(savings_usd, 0)} · over {span_days} days · vs paying per-API'
            f'</div></div>'
        )
    elif deficit_usd > 0:
        savings_block = (
            f'<div style="margin-top:14px; padding:12px 14px; background:var(--bg-card); '
            f'border:1px solid var(--border); border-radius:10px;">'
            f'<div style="font-size:0.7rem; color:var(--text-secondary); '
            f'text-transform:uppercase; letter-spacing:0.06em; font-weight:600;">'
            f'POTENTIAL OVERPAY</div>'
            f'<div style="font-size:1.5rem; font-weight:700; color:{tone_color}; '
            f'line-height:1.1; margin-top:2px;">'
            f'-{fmt_local_compact(deficit_usd)}</div>'
            f'<div style="font-size:0.78rem; color:var(--text-muted); margin-top:2px;">'
            f'over {span_days} days at current usage</div></div>'
        )
    else:
        savings_block = ""

    st.markdown(
        f'<div style="background:{tone_bg}; border:1px solid {tone_border}; '
        f'border-radius:14px; padding:18px 20px; margin-top:12px;">'
        # Header row: title + stars
        f'<div style="display:flex; justify-content:space-between; align-items:center; '
        f'margin-bottom:10px;">'
        f'<div>'
        f'<div style="font-size:0.7rem; color:{tone_color}; '
        f'text-transform:uppercase; letter-spacing:0.06em; font-weight:700;">{title}</div>'
        f'<div style="font-size:0.78rem; color:var(--text-muted); margin-top:1px;">'
        f'{badge_text}</div>'
        f'</div>'
        f'<div>{stars_html}</div>'
        f'</div>'
        # Big ROI number
        f'<div style="font-size:3rem; font-weight:800; color:{tone_color}; '
        f'line-height:1; font-variant-numeric:tabular-nums; letter-spacing:-0.02em;">'
        f'{roi:.1f}<span style="font-size:1.6rem; margin-left:4px;">×</span></div>'
        f'<div style="font-size:0.78rem; color:var(--text-secondary); '
        f'margin-top:2px; font-weight:500;">return on plan cost</div>'
        # Emotional one-liner
        f'<div style="font-size:0.92rem; color:var(--text-primary); '
        f'margin-top:10px; line-height:1.4;">{emotion}</div>'
        # Coverage bar — visualizes how much of the API cost the plan paid for
        f'<div style="margin-top:14px;">'
        f'<div style="display:flex; justify-content:space-between; '
        f'font-size:0.72rem; color:var(--text-secondary); margin-bottom:4px;">'
        f'<span>Plan paid: <strong style="color:var(--text-primary);">'
        f'{fmt_local_compact(plan_cost_usd)}</strong></span>'
        f'<span>API would cost: <strong style="color:var(--text-primary);">'
        f'{fmt_local_compact(cost)}</strong></span>'
        f'</div>'
        f'<div style="height:8px; background:var(--bg-hover); border-radius:4px; '
        f'overflow:hidden; position:relative;">'
        f'<div style="position:absolute; left:0; top:0; bottom:0; '
        f'width:{coverage_pct:.1f}%; '
        f'background:linear-gradient(90deg, {tone_color}, var(--accent));"></div>'
        f'</div></div>'
        f'{savings_block}'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_budget_status(period: str, today_cost_usd: float, month_cost_usd: float) -> None:
    """Show budget bar + warning banner if over."""
    daily_budget = setting_float("token_daily_budget_usd", 0)
    monthly_budget = setting_float("token_monthly_budget_usd", 0)

    def _render_bar(label: str, used: float, budget: float, pct: float, color: str) -> None:
        """Themed budget bar with breathing room above and below."""
        st.markdown(
            f'<div style="margin: 8px 0 18px;">'
            f'<div style="display:flex; justify-content:space-between; '
            f'font-size:0.8rem; color:var(--text-secondary); margin-bottom:6px;">'
            f'<span>{label}: <strong style="color:var(--text-primary);">'
            f'{fmt_local(used, 0)}</strong> '
            f'<span style="color:var(--text-muted);">/ {fmt_local(budget, 0)}</span></span>'
            f'<span style="color:{color}; font-weight:700;">{pct:.0f}%</span>'
            f'</div>'
            f'<div style="background:var(--bg-hover); border-radius:4px; height:8px; '
            f'overflow:hidden; position:relative;">'
            f'<div style="background:linear-gradient(90deg, {color}, var(--accent-hover)); '
            f'height:100%; width:{min(pct, 100):.0f}%; '
            f'transition: width 0.4s ease;"></div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    if period == "today" and daily_budget > 0:
        pct = today_cost_usd / daily_budget * 100
        color = "var(--success)" if pct < 70 else ("var(--warning)" if pct < 100 else "var(--danger)")
        _render_bar("Daily budget", today_cost_usd, daily_budget, pct, color)
    if period == "month" and monthly_budget > 0:
        pct = month_cost_usd / monthly_budget * 100
        color = "var(--success)" if pct < 70 else ("var(--warning)" if pct < 100 else "var(--danger)")
        _render_bar("Monthly budget", month_cost_usd, monthly_budget, pct, color)


def render_forecast(period: str, cost_usd: float) -> None:
    """For 'month' period, show projected end-of-month cost."""
    if period != "month" or cost_usd <= 0:
        return
    now = datetime.now()
    days_elapsed = now.day
    days_in_month = (now.replace(day=28) + timedelta(days=4)).replace(day=1).day - 1 + 1
    # Simpler: get last day of current month
    if now.month == 12:
        last_day = 31
    else:
        last_day = (now.replace(month=now.month + 1, day=1) - timedelta(days=1)).day
    if days_elapsed < 1:
        return
    daily_avg = cost_usd / days_elapsed
    forecast = daily_avg * last_day
    st.markdown(
        f'<div style="background:var(--warning-bg); border:1px solid var(--warning-border); '
        f'border-radius:8px; padding:10px 14px; margin-top:8px; font-size:0.85rem; '
        f'color:var(--text-primary);">'
        f'<strong>Forecast</strong> · '
        f'at this pace ({fmt_local(daily_avg, 0)}/day average), '
        f'end-of-month total: <strong>{fmt_local(forecast, 0)}</strong> '
        f'<span style="color:var(--text-secondary);">({fmt_usd_ref(forecast, 0)})</span>'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_token_view(period: str, pricing_mode: str) -> None:
    data = load_token_period(period, pricing_mode)
    grand = data["grand"]
    series = data["series"]

    cost     = float(grand["cost"]) if grand["cost"] is not None else 0.0
    msgs     = int(grand["messages"])
    in_tok   = int(grand["input_tok"])
    out_tok  = int(grand["output_tok"])
    cw_tok   = int(grand["cache_w_tok"])
    cr_tok   = int(grand["cache_r_tok"])

    if msgs == 0:
        if period == "today":
            tip = "Use Claude Code today and refresh, or click <strong>Sync now</strong> to import recent activity."
        else:
            tip = "Click <strong>Sync now</strong> at the top to import your Claude Code logs."
        pulse_empty("No AI usage in this range", tip, ICON_NO_DATA)
        return

    # Plan ROI — moved to top so the celebration is the first thing user sees
    # (most meaningful for "all time" / "month"; harmless on "today" if data exists)
    if period in ("all", "month"):
        render_plan_roi(grand, period)

    # Budget bar (today / month)
    render_budget_status(period, cost, cost)

    # Top KPIs (cost / messages / avg per active bucket)
    n_buckets = max(len(series), 1)
    avg_cost = cost / n_buckets
    avg_label = {"hour": "Avg / active hour", "day": "Avg / active day"}[data["granularity"]]

    k1, k2, k3 = st.columns(3)
    with k1:
        kpi_card("Cost", fmt_local_compact(cost), fmt_usd_ref(cost))
    with k2:
        kpi_card("Messages", f"{msgs:,}")
    with k3:
        kpi_card(avg_label, fmt_local_compact(avg_cost), fmt_usd_ref(avg_cost))

    # Forecast (month tab only)
    render_forecast(period, cost)

    # Token breakdown row
    st.markdown(
        '<div style="font-size:0.7rem; color:var(--text-secondary); text-transform:uppercase; '
        'letter-spacing:0.04em; margin-top:8px; margin-bottom:4px;">TOKENS</div>',
        unsafe_allow_html=True,
    )
    t1, t2, t3, t4 = st.columns(4)
    with t1: kpi_card("Input",        fmt_tokens(in_tok))
    with t2: kpi_card("Output",       fmt_tokens(out_tok))
    with t3: kpi_card("Cache create", fmt_tokens(cw_tok))
    with t4: kpi_card("Cache read",   fmt_tokens(cr_tok))

    st.markdown("---")

    # Time-series chart — stacked bar by bucket
    if not series.empty:
        chart_title = {
            "hour": "Hourly cost (today)",
            "day":  "Daily cost",
        }[data["granularity"]]
        # If today, pad to all 24 hours
        if data["granularity"] == "hour":
            today_str = datetime.now().strftime("%Y-%m-%d")
            full_hours = pd.DataFrame({
                "bucket": [f"{today_str}T{h:02d}:00:00" for h in range(24)],
            })
            series = full_hours.merge(series, on="bucket", how="left").fillna(0)
            x_labels = [b[11:13] + ":00" for b in series["bucket"]]
        else:
            x_labels = series["bucket"].tolist()

        # Convert cost (USD) -> local currency for chart
        sym_now = local_symbol()
        local_cost = [usd_to_local(c) for c in series["cost"]]
        pal = theme.get_palette()

        # Color each bar by % of daily budget — green (under) → amber (>=70%) → red (>=100%)
        daily_budget_usd = setting_float("token_daily_budget_usd", 0)
        if data["granularity"] == "hour":
            # For hourly, compare each hour to (daily budget / 24)
            ref_budget = daily_budget_usd / 24 if daily_budget_usd > 0 else 0
        else:
            ref_budget = daily_budget_usd

        bar_colors = []
        for c_usd in series["cost"]:
            if ref_budget > 0:
                ratio = c_usd / ref_budget
                if ratio >= 1.0:
                    bar_colors.append(pal["danger"])
                elif ratio >= 0.70:
                    bar_colors.append(pal["warning"])
                elif c_usd > 0:
                    bar_colors.append(pal["success"])
                else:
                    bar_colors.append(pal["border"])
            else:
                bar_colors.append(pal["accent"])

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=x_labels, y=local_cost,
            customdata=series["cost"],
            marker_color=bar_colors,
            hovertemplate="%{x}<br>" + sym_now + "%{y:,.0f}"
                          + " (<i>$%{customdata:.2f} USD</i>)<extra></extra>",
            name="cost",
        ))
        fig.update_layout(
            title=dict(text=chart_title, font=dict(size=12, color=pal["text_primary"])),
            height=220, margin=dict(l=10, r=10, t=34, b=10),
            plot_bgcolor=pal["bg_card"], paper_bgcolor=pal["bg_card"],
            xaxis=dict(showgrid=False, color=pal["text_secondary"], fixedrange=True),
            yaxis=dict(gridcolor=pal["border"], title=None, color=pal["text_secondary"],
                       tickprefix=sym_now, fixedrange=True),
            font=dict(color=pal["text_primary"], size=11),
            showlegend=False,
            bargap=0.12,
            dragmode=False,
        )
        st.plotly_chart(
            fig, use_container_width=True,
            config={"displayModeBar": False, "responsive": False, "scrollZoom": False},
        )

    # 7-day × 24h heatmap (only for "all" or "month" — most useful when there's data)
    if period in ("month", "all"):
        conn = get_conn()
        since_iso, _, _ = _period_window(period)
        hm_df = pd.read_sql_query(
            "SELECT strftime('%w', timestamp, 'localtime') AS dow, "
            "       strftime('%H', timestamp, 'localtime') AS hour, "
            "       SUM(cost_usd) AS cost "
            "FROM token_usage WHERE timestamp >= ? "
            "GROUP BY dow, hour",
            conn, params=(since_iso,),
        )
        if not hm_df.empty:
            # Pivot into 7×24 matrix
            hm_df["dow"] = hm_df["dow"].astype(int)
            hm_df["hour"] = hm_df["hour"].astype(int)
            grid = [[0.0] * 24 for _ in range(7)]
            for _, r in hm_df.iterrows():
                grid[int(r["dow"])][int(r["hour"])] = float(r["cost"] or 0)
            day_labels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
            hour_labels = [f"{h:02d}" for h in range(24)]
            local_grid = [[c * usd_to_local(1.0) for c in row] for row in grid]

            pal = theme.get_palette()
            # Heatmap gradient — multi-stop intensity scale, theme-aware.
            # Low usage = bg-secondary (blends in), high = vivid accent gradient.
            # Pulse brand — mint/emerald heatmap intensity scale
            if get_setting("theme", "light") == "dark":
                heatmap_scale = [
                    [0.00, pal["bg_secondary"]],    # empty cells blend with black
                    [0.15, "#022c22"],               # whisper emerald
                    [0.40, "#065f46"],               # mid emerald
                    [0.70, "#10b981"],               # vivid emerald
                    [1.00, "#34d399"],               # peak — bright mint
                ]
            else:
                heatmap_scale = [
                    [0.00, "#f6f7f9"],
                    [0.15, "#d1fae5"],               # whisper mint
                    [0.40, "#6ee7b7"],               # mid mint
                    [0.70, "#10b981"],               # vivid emerald
                    [1.00, "#065f46"],               # peak — deep
                ]

            fig_hm = go.Figure(data=go.Heatmap(
                z=local_grid, x=hour_labels, y=day_labels,
                colorscale=heatmap_scale,
                hovertemplate=f"%{{y}} %{{x}}:00<br>{local_symbol()}%{{z:,.0f}}<extra></extra>",
                showscale=False,
            ))
            fig_hm.update_layout(
                title=dict(text="When you use AI most (heatmap)",
                           font=dict(size=12, color=pal["text_primary"])),
                height=200, margin=dict(l=10, r=10, t=34, b=10),
                plot_bgcolor=pal["bg_card"], paper_bgcolor=pal["bg_card"],
                xaxis=dict(side="bottom",
                           tickfont=dict(size=10, color=pal["text_secondary"]),
                           fixedrange=True),
                yaxis=dict(autorange="reversed",
                           tickfont=dict(size=10, color=pal["text_secondary"]),
                           fixedrange=True),
                font=dict(color=pal["text_primary"], size=11),
                dragmode=False,
            )
            st.plotly_chart(
                fig_hm, use_container_width=True,
                config={"displayModeBar": False, "responsive": False, "scrollZoom": False},
            )

    # By model + by project tables side by side (matched heights).
    # ~5 rows visible + header; rest scrollable.
    TABLE_H = 240
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**By model**")
        bm = data["by_model"].copy()
        if not bm.empty:
            cost_col = f"cost ({local_symbol()})"
            for c in ("input_tok", "output_tok", "cache_w_tok", "cache_r_tok"):
                bm[c] = bm[c].apply(fmt_tokens)
            bm["cost"] = bm["cost"].apply(lambda v: fmt_local(v, 0))
            bm["messages"] = bm["messages"].apply(lambda v: f"{int(v):,}")
            bm.columns = ["model", "msgs", "input", "output", "cache_w", "cache_r", cost_col]
            pulse_table(
                bm,
                num_cols=["msgs", "input", "output", "cache_w", "cache_r", cost_col],
                strong_cols=["model", cost_col],
                col_labels={"model": "Model", "msgs": "Msgs", "input": "Input",
                            "output": "Output", "cache_w": "Cache W", "cache_r": "Cache R"},
                max_height=TABLE_H,
            )
        else:
            st.caption("(no data)")

    with col2:
        st.markdown("**By project (top 20)**")
        bp = data["by_project"].copy()
        if not bp.empty:
            cost_col = f"cost ({local_symbol()})"
            bp["total_tok"] = bp["total_tok"].apply(fmt_tokens)
            bp["cost"] = bp["cost"].apply(lambda v: fmt_local(v, 0))
            bp["messages"] = bp["messages"].apply(lambda v: f"{int(v):,}")
            bp.columns = ["project", "msgs", "tokens", cost_col]
            pulse_table(
                bp,
                num_cols=["msgs", "tokens", cost_col],
                strong_cols=["project", cost_col],
                col_labels={"project": "Project", "msgs": "Msgs", "tokens": "Tokens"},
                max_height=TABLE_H,
            )
        else:
            st.caption("(no data)")

    # ROI display moved to top of this view (just below page header).


def render_tokens():
    sync_clicked = page_header(
        "AI usage",
        "Claude Code & API equivalent cost — Today, this month, all time",
        action_label="Sync now",
        action_key="sync_now_btn",
    )
    if sync_clicked:
        with st.spinner("Scanning Claude Code logs..."):
            results = sync_all()
        for r in results:
            if r["rows_added"]:
                st.success(f"{r['source']}: +{r['rows_added']} rows")
            else:
                st.info(f"{r['source']}: {r.get('note', '0 new rows')}")

    # Sync status caption
    status = get_sync_status()
    if status:
        line = " · ".join(
            f"{s['source']} {s['last_synced_at'][:16].replace('T', ' ')}"
            for s in status
        )
        st.markdown(
            f'<div style="font-size:0.75rem; color:var(--text-secondary); margin-top:-4px; margin-bottom:8px;">'
            f'Last sync · {line}</div>',
            unsafe_allow_html=True,
        )

    # Pricing mode read from settings (changeable in Settings → Advanced)
    pricing_mode = get_setting("token_pricing_mode", "per_model")

    # Three time-period tabs
    tab_today, tab_month, tab_all = st.tabs(["Today", "This month", "All time"])
    with tab_today:
        render_token_view("today", pricing_mode)
    with tab_month:
        render_token_view("month", pricing_mode)
    with tab_all:
        render_token_view("all", pricing_mode)

    # Leaderboard teaser — Phase 3 feature, captures interest now via waitlist
    render_leaderboard_preview()


def render_leaderboard_preview() -> None:
    """Coming-soon preview for AI-usage leaderboard. Captures waitlist signups
    so Phase 3 launch can email back early adopters first."""
    st.markdown("---")

    # Header strip
    st.markdown(
        f'<div style="display:flex; justify-content:space-between; align-items:center; '
        f'margin-bottom:14px;">'
        f'<div>'
        f'<div style="font-size:0.7rem; color:var(--accent); text-transform:uppercase; '
        f'letter-spacing:0.08em; font-weight:700;">COMING SOON · LEADERBOARD</div>'
        f'<div style="font-size:1.25rem; font-weight:700; color:var(--text-primary); '
        f'margin-top:4px; letter-spacing:-0.015em;">Compare with friends. Privately.</div>'
        f'<div style="font-size:0.88rem; color:var(--text-secondary); margin-top:2px; '
        f'max-width:560px;">See where you rank on AI usage efficiency. '
        f'Opt-in, aggregate metrics only — no raw token data ever shared.</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # 5 category preview cards
    categories = [
        ("Best ROI",        "Plan value vs cost — efficiency king",            "var(--success)"),
        ("Longest streak",  "Consecutive days using AI — consistency",         "var(--accent)"),
        ("Token wizard",    "Output / input ratio — efficient prompting",      "var(--warning)"),
        ("Power day",       "Highest single-day useful spend — peak focus",    "var(--accent)"),
        ("Project depth",   "Distinct projects worked on — versatility",       "var(--success)"),
    ]
    cols = st.columns(5)
    for col, (name, sub, color) in zip(cols, categories):
        with col:
            st.markdown(
                f'<div style="padding:14px 12px; background:var(--bg-card); '
                f'border:1px solid var(--border); border-radius:10px; '
                f'min-height:130px; display:flex; flex-direction:column;">'
                f'<div style="font-size:0.72rem; color:{color}; font-weight:700; '
                f'text-transform:uppercase; letter-spacing:0.05em;">{name}</div>'
                f'<div style="font-size:0.78rem; color:var(--text-secondary); '
                f'margin-top:6px; line-height:1.4; flex:1;">{sub}</div>'
                f'<div style="font-size:1.4rem; font-weight:800; color:var(--text-muted); '
                f'margin-top:6px; letter-spacing:-0.02em; opacity:0.4;'
                f'font-variant-numeric:tabular-nums;">—</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # Waitlist signup form
    n_signups = waitlist.count()
    st.markdown(
        f'<div style="margin-top:18px; padding:16px 18px; background:var(--accent-bg); '
        f'border:1px solid var(--accent-border); border-radius:12px;">'
        f'<div style="font-weight:700; color:var(--accent); font-size:0.92rem; '
        f'margin-bottom:6px;">Get notified when leaderboard launches</div>'
        f'<div style="font-size:0.82rem; color:var(--text-secondary);">'
        f'Early adopters get free Pro for 1 month + first dibs on friend invite codes.'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    with st.form("leaderboard_waitlist", clear_on_submit=True):
        wc1, wc2 = st.columns([3, 1])
        with wc1:
            wl_email = st.text_input(
                "Email",
                placeholder="you@example.com",
                label_visibility="collapsed",
                key="leaderboard_wl_email",
            )
        with wc2:
            submitted = st.form_submit_button("Notify me", use_container_width=True, type="primary")
        if submitted:
            r = waitlist.signup(
                wl_email,
                source="leaderboard-teaser",
                interest="leaderboard",
            )
            if r.get("ok"):
                st.toast("You're on the list — we'll email when leaderboard launches.",
                         icon=":material/check_circle:")
                st.rerun()
            else:
                err_msg = {
                    "invalid_email": "That doesn't look like a valid email.",
                    "already_signed_up": "You're already on the list.",
                }.get(r.get("error"), "Could not sign up — try again.")
                st.warning(err_msg)

    st.caption(
        f"{n_signups} {'person has' if n_signups == 1 else 'people have'} joined the leaderboard waitlist · "
        "Privacy: opt-in only, aggregate stats, friend-only by default."
    )


# ============================================================
# PAGE: SETTINGS
# ============================================================
def render_pulse_pro_section():
    """Pricing + waitlist + referral + account info — embedded inside Settings."""
    st.markdown("##### Pulse Pro — coming soon")
    st.caption(
        "Pulse is free forever for local use. Pro adds cloud sync, mobile, "
        "AI assistant, cross-provider tracking, and bank integration."
    )

    # Pricing tiers — 3 column comparison
    pp1, pp2, pp3 = st.columns(3)

    def tier_card(col, name: str, price: str, sub: str, perks: list[str], cta: str | None = None):
        with col:
            features = "".join(
                f'<li style="font-size:0.82rem; color:var(--text-secondary); margin-bottom:3px;">{escape(p)}</li>'
                for p in perks
            )
            cta_html = (
                f'<div style="margin-top:10px; font-size:0.78rem; color:var(--text-secondary);">{escape(cta)}</div>'
                if cta else ""
            )
            st.markdown(
                f'<div style="background:var(--bg-card); border:1px solid var(--border); '
                f'border-radius:10px; padding:14px; height:100%; min-height:280px;">'
                f'<div style="font-size:0.7rem; color:var(--text-secondary); text-transform:uppercase; '
                f'letter-spacing:0.05em; font-weight:600;">{escape(name)}</div>'
                f'<div style="font-size:1.5rem; font-weight:700; color:var(--text-primary); '
                f'margin-top:4px;">{escape(price)}</div>'
                f'<div style="font-size:0.78rem; color:var(--text-secondary); margin-bottom:10px;">{escape(sub)}</div>'
                f'<ul style="padding-left:18px; margin:0;">{features}</ul>'
                f'{cta_html}'
                f'</div>',
                unsafe_allow_html=True,
            )

    tier_card(pp1, "Free", "$0", "forever, local",
              ["Subscription tracker", "AI token analytics (Claude Code)",
               "App usage tracking", "Windows alerts", "CSV export",
               "Local backup", "1 device"],
              cta="You are here.")
    tier_card(pp2, "Pro", "$9 / mo", "billed monthly or $89/yr",
              ["Everything in Free", "Cloud sync (encrypted)",
               "Mobile companion app", "Web dashboard",
               "AI assistant — Ask Pulse", "Cross-provider tracking (OpenAI, Gemini, Cursor)",
               "Receipt OCR", "Email digest + push",
               "Unlimited devices, unlimited history"],
              cta="Coming Q3 2026 — join waitlist below")
    tier_card(pp3, "Team", "$19 /user/mo", "for small teams & families",
              ["Everything in Pro", "Shared subscription pool",
               "Per-user attribution", "Approval workflow",
               "Tax categorization", "Annual tax pack PDF",
               "Slack/LINE integrations"],
              cta="Coming Q4 2026")

    st.markdown("---")

    # Waitlist signup
    st.markdown("##### Join the Pro waitlist")
    st.caption("Get early access + lifetime deal pricing when Pro launches.")
    n_signups = waitlist.count()
    st.caption(f"{n_signups} {'person has' if n_signups == 1 else 'people have'} signed up so far.")

    wl1, wl2 = st.columns([3, 1])
    with wl1:
        email = st.text_input(
            "Email", placeholder="you@example.com",
            label_visibility="collapsed", key="waitlist_email",
        )
    with wl2:
        if st.button("Join waitlist", type="primary", use_container_width=True):
            result = waitlist.signup(email or "", source="settings", interest="pro")
            if result.get("ok"):
                st.success("You're on the list. We'll email when Pro launches.")
                telemetry.track("waitlist_signup", {"interest": "pro"})
            else:
                err = result.get("error", "unknown")
                msgs = {
                    "invalid_email": "Please enter a valid email address.",
                    "already_signed_up": "This email is already on the waitlist.",
                }
                st.warning(msgs.get(err, f"Failed: {err}"))

    st.markdown("---")

    # Referral code
    st.markdown("##### Refer a friend")
    st.caption("Both of you get a free month of Pro when it launches.")
    rc1, rc2 = st.columns([1, 1])
    with rc1:
        my_code = referrals.my_code()
        st.markdown(
            f'<div style="font-size:0.78rem; color:var(--text-secondary);">Your referral code</div>'
            f'<div style="font-size:1.4rem; font-weight:700; '
            f'font-family: ui-monospace, Consolas, monospace; color:var(--text-primary); '
            f'letter-spacing:0.1em;">{my_code}</div>',
            unsafe_allow_html=True,
        )
    with rc2:
        with st.form("redeem_form", clear_on_submit=True):
            redeem_code = st.text_input(
                "Got a code from a friend?",
                placeholder="ABCD2345",
                max_chars=8,
            )
            if st.form_submit_button("Redeem"):
                r = referrals.redeem(redeem_code or "")
                if r.get("ok"):
                    st.success("Code stored — you'll get credit when Pro launches.")
                    telemetry.track("referral_redeemed")
                else:
                    err_msgs = {
                        "invalid_format": "Codes are 8 characters.",
                        "cannot_redeem_own_code": "That's your own code.",
                        "already_redeemed": "This code is already redeemed.",
                    }
                    st.warning(err_msgs.get(r.get("error"), "Could not redeem"))

    st.markdown("---")

    # Account info
    st.markdown("##### Account")
    ac1, ac2 = st.columns(2)
    with ac1:
        st.markdown(
            f'<div style="font-size:0.78rem; color:var(--text-secondary);">Pulse account ID</div>'
            f'<div style="font-family: ui-monospace, Consolas, monospace; '
            f'font-size:0.88rem; color:var(--text-primary);">{account.short_id()}…</div>'
            f'<div style="font-size:0.72rem; color:var(--text-muted);">'
            f'Anonymous local UUID. Will be used to migrate your data when cloud ships.'
            f'</div>',
            unsafe_allow_html=True,
        )
    with ac2:
        opt_in = st.checkbox(
            "Help improve Pulse with anonymous usage data",
            value=telemetry.is_opted_in(),
            help=("No personal data, no email, no DB content sent. "
                  "Just feature names and counts. Opt out anytime."),
        )
        if opt_in != telemetry.is_opted_in():
            set_setting("telemetry_opt_in", "1" if opt_in else "0")
            st.success("Updated")
            st.rerun()


def render_settings():
    page_header("Settings", f"{APP_NAME} · v1.0 · Local-first, private by design")

    tab_prefs, tab_pro, tab_data, tab_adv = st.tabs(
        ["Preferences", "Pulse Pro", "Data & backup", "Advanced"]
    )

    # ====== PREFERENCES TAB ======
    with tab_prefs:
        _render_settings_preferences()
    with tab_pro:
        render_pulse_pro_section()
    with tab_data:
        _render_settings_data()
    with tab_adv:
        _render_settings_advanced()


def _render_settings_preferences():
    """Display + plan + budgets + alerts."""
    # ── PREFERENCES (display + plan + budgets in one form) ──────
    st.markdown("##### Preferences")
    st.caption("Theme is in the sidebar (sun/moon icon).")
    with st.form("prefs_form"):
        p1, p2, p3, p4 = st.columns(4)
        currencies = ["THB", "USD", "EUR", "GBP", "JPY", "SGD", "MYR",
                      "CNY", "KRW", "AUD", "CAD", "HKD", "INR", "PHP", "IDR"]
        cur_now = current_currency()
        with p1:
            new_cur = st.selectbox(
                "Currency", currencies,
                index=currencies.index(cur_now) if cur_now in currencies else 0,
            )
        with p2:
            new_plan = st.number_input(
                "Plan / mo (USD)", min_value=0.0,
                value=plan_monthly_usd(), step=10.0,
                help="What you pay for Claude Max / ChatGPT Pro / etc.",
            )
        with p3:
            new_daily = st.number_input(
                "Daily budget (USD)", min_value=0.0,
                value=setting_float("token_daily_budget_usd", 0.0), step=10.0,
                help="0 = disabled",
            )
        with p4:
            new_monthly = st.number_input(
                "Monthly budget (USD)", min_value=0.0,
                value=setting_float("token_monthly_budget_usd", 0.0), step=50.0,
                help="0 = disabled",
            )
        if st.form_submit_button("Save preferences", type="primary"):
            set_setting("display_currency", new_cur)
            set_setting("plan_monthly_usd", str(new_plan))
            set_setting("token_daily_budget_usd", str(new_daily))
            set_setting("token_monthly_budget_usd", str(new_monthly))
            st.cache_data.clear()
            st.success("Saved")
            st.rerun()

    st.markdown("---")

    # ── ALERTS (3 inline toggles) ───────────────────────────────
    st.markdown("##### Alerts")
    with st.form("alerts_form"):
        a1, a2, a3 = st.columns(3)
        with a1:
            n_renew = st.checkbox(
                "Subscription renewals",
                value=setting_bool("alerts_renewals_enabled", True),
            )
        with a2:
            n_spike = st.checkbox(
                "AI cost spikes",
                value=setting_bool("alerts_token_spike_enabled", True),
            )
        with a3:
            n_dead = st.checkbox(
                "Unused subscriptions",
                value=setting_bool("alerts_dead_subs_enabled", True),
            )
        if st.form_submit_button("Save alerts", type="primary"):
            set_setting("alerts_renewals_enabled", "1" if n_renew else "0")
            set_setting("alerts_token_spike_enabled", "1" if n_spike else "0")
            set_setting("alerts_dead_subs_enabled", "1" if n_dead else "0")
            st.success("Saved")


def _render_settings_data():
    """Backup, restore, CSV import/export, ICS export."""
    from backup import backup_now, list_backups, restore_from_backup
    from ics_export import build_ics

    backups = list_backups()
    last_str = backups[0]["created"][:16].replace("T", " ") if backups else "never"

    st.markdown("##### Data & backup")
    st.caption(f"Auto-backup runs daily — last: {last_str}")

    db1, db2, db3, db4 = st.columns(4)
    with db1:
        if st.button("Back up now", use_container_width=True):
            with st.spinner("Creating backup…"):
                p = backup_now("manual")
            st.success(f"Saved {p.name}")
            st.rerun()
    with db2:
        st.download_button(
            "Calendar .ics",
            data=build_ics(),
            file_name="pulse-subscriptions.ics",
            mime="text/calendar",
            use_container_width=True,
        )
    with db3:
        all_subs_full = load_subscriptions(active_only=False)
        csv_buf = io.StringIO()
        all_subs_full.to_csv(csv_buf, index=False)
        st.download_button(
            "Export CSV",
            data=csv_buf.getvalue(),
            file_name="pulse-subscriptions.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with db4:
        if st.button("Import CSV", use_container_width=True):
            st.session_state["show_csv_import_settings"] = True
            st.rerun()

    # Inline CSV import + restore
    if st.session_state.get("show_csv_import_settings"):
        with st.expander("Import from CSV", expanded=True):
            st.caption(
                "Required columns: `name, cost, currency, billing_cycle`. "
                "Optional: `next_billing_date, last_charge_date, email_sender, "
                "linked_process, cancel_url, tag, notes`."
            )
            uploaded = st.file_uploader("Upload CSV", type=["csv"], key="csv_uploader_settings")
            if uploaded is not None:
                try:
                    df = pd.read_csv(uploaded)
                    st.dataframe(df.head(20), hide_index=True, use_container_width=True)
                    if st.button(f"Import {len(df)} rows", type="primary", key="do_csv_import"):
                        conn = get_conn()
                        n = 0
                        for _, row in df.iterrows():
                            try:
                                conn.execute(
                                    "INSERT INTO subscriptions "
                                    "(name, cost, currency, billing_cycle, next_billing_date, "
                                    " last_charge_date, email_sender, linked_process, cancel_url, "
                                    " tag, notes, active) "
                                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)",
                                    (
                                        row.get("name"),
                                        float(row.get("cost", 0) or 0),
                                        row.get("currency", "USD"),
                                        row.get("billing_cycle", "monthly"),
                                        row.get("next_billing_date") or None,
                                        row.get("last_charge_date") or None,
                                        row.get("email_sender") or None,
                                        row.get("linked_process") or None,
                                        row.get("cancel_url") or None,
                                        row.get("tag") or None,
                                        row.get("notes") or None,
                                    ),
                                )
                                n += 1
                            except Exception as e:
                                st.warning(f"Row '{row.get('name')}' failed: {e}")
                        conn.commit()
                        st.session_state["show_csv_import_settings"] = False
                        st.success(f"Imported {n} subscriptions")
                        st.rerun()
                except Exception as e:
                    st.error(f"Failed to read CSV: {e}")
            if st.button("Close", key="close_csv_settings"):
                st.session_state["show_csv_import_settings"] = False
                st.rerun()

    if backups:
        with st.expander("Restore from backup"):
            options = [b["name"] for b in backups]
            sel = st.selectbox("Pick a snapshot", options, key="restore_pick")
            confirm = st.checkbox("I understand this will overwrite current data",
                                  key="restore_confirm")
            if st.button("Restore", disabled=not confirm, type="primary"):
                try:
                    p = next(Path(b["path"]) for b in backups if b["name"] == sel)
                    restore_from_backup(p)
                    st.cache_data.clear()
                    st.success(f"Restored from {sel}. Refresh (Ctrl+R).")
                except Exception as e:
                    st.error(f"Restore failed: {e}")


def _render_settings_advanced():
    """Power-user settings: alert tuning, tracking, AI pricing mode, app categories,
    currency converter, tools, and diagnostics."""
    # Show what's-new at top of Advanced so users discover it
    changelog_path = Path(__file__).parent / "CHANGELOG.md"
    if changelog_path.exists():
        with st.expander("What's new in Pulse", expanded=False):
            st.markdown(changelog_path.read_text(encoding="utf-8"))
    # --- Renewal alert timing + spike multiplier (sub-options for alerts) ---
    st.markdown("**Alert tuning**")
    with st.form("alert_tune_form"):
        tc1, tc2 = st.columns(2)
        with tc1:
            renew_days = st.number_input(
                "Renewal alert (days ahead)", min_value=1, max_value=30,
                value=setting_int("alerts_renewals_days_ahead", 3),
            )
        with tc2:
            spike_x = st.slider(
                "Spike trigger (× 30-day average)",
                min_value=2.0, max_value=10.0,
                value=setting_float("alerts_token_spike_multiplier", 3.0),
                step=0.5,
            )
        if st.form_submit_button("Save"):
            set_setting("alerts_renewals_days_ahead", str(int(renew_days)))
            set_setting("alerts_token_spike_multiplier", str(spike_x))
            st.success("Saved")

    # --- Tracking + AI cost mode (single form) ---
    st.markdown("**Tracking & calculation**")
    with st.form("track_form"):
        tk1, tk2 = st.columns([1, 2])
        with tk1:
            idle_thresh = st.slider(
                "Pause tracking after (min idle)",
                min_value=1, max_value=10,
                value=int(setting_int("idle_threshold_sec", 120) / 60),
            )
        with tk2:
            modes = ["per_model", "sonnet"]
            labels = {
                "per_model": "Per-model rate (accurate)",
                "sonnet": "Uniform Sonnet rate (matches ccusage)",
            }
            current_mode = get_setting("token_pricing_mode", "per_model")
            new_mode = st.radio(
                "AI pricing mode",
                modes,
                index=modes.index(current_mode) if current_mode in modes else 0,
                format_func=lambda m: labels[m],
                horizontal=False,
            )
        if st.form_submit_button("Save"):
            set_setting("idle_threshold_sec", str(idle_thresh * 60))
            set_setting("token_pricing_mode", new_mode)
            st.cache_data.clear()
            st.success("Saved")
            st.rerun()

    # --- Currency converter ---
    st.markdown("**Currency converter**")
    rates_data = cached_fx_rates()
    avail = ["USD"] + [c for c in fx.list_currencies(rates_data) if c != "USD"]
    if current_currency() not in avail:
        avail.insert(0, current_currency())
    cv1, cv2, cv3 = st.columns([1, 1, 2])
    with cv1:
        from_cur = st.selectbox("From", avail, index=avail.index("USD"), key="conv_from_set")
    with cv2:
        to_cur = st.selectbox("To", avail, index=avail.index(current_currency()), key="conv_to_set")
    with cv3:
        amt = st.number_input("Amount", min_value=0.0, value=100.0, step=10.0, key="conv_amt_set")
    result = fx.convert(amt, from_cur, to_cur, rates_data)
    per = fx.convert(1.0, from_cur, to_cur, rates_data)
    st.markdown(
        f'<div style="font-size:1.1rem; font-weight:700; '
        f'font-variant-numeric:tabular-nums; color:var(--text-primary);">'
        f'{fx.symbol(to_cur)}{result:,.2f} {to_cur}</div>'
        f'<div style="font-size:0.75rem; color:var(--text-secondary);">'
        f'1 {from_cur} = {per:.4f} {to_cur} · {rates_data.get("source", "?")} '
        f'({rates_data.get("date", "?")})</div>',
        unsafe_allow_html=True,
    )

    # --- App categories ---
    st.markdown("**App categories**")
    st.caption("Override how Pulse categorizes apps. Useful for misclassifications "
               "or flagging personal apps as 'distraction'.")
    conn = get_conn()
    since30 = (datetime.now() - timedelta(days=30)).isoformat(timespec="seconds")
    top_apps = pd.read_sql_query(
        "SELECT process_name, SUM(COALESCE(duration_seconds, 0))/3600.0 AS hours "
        "FROM app_activity WHERE started_at > ? "
        "GROUP BY process_name ORDER BY hours DESC LIMIT 15",
        conn, params=(since30,),
    )
    if top_apps.empty:
        st.caption("No app activity yet — come back after Pulse has been running a while.")
    else:
        cat_options = categories.all_categories()
        for _, row in top_apps.iterrows():
            proc = row["process_name"]
            cur_cat, cur_dist = categories.classify(proc)
            ec1, ec2, ec3, ec4 = st.columns([3, 2, 1, 1])
            with ec1:
                st.markdown(f"**{escape(proc)}** "
                            f"<span style='color:var(--text-secondary); font-size:0.78rem;'>"
                            f"{row['hours']:.1f}h/30d</span>",
                            unsafe_allow_html=True)
            with ec2:
                new_cat = st.selectbox(
                    "Category", cat_options,
                    index=cat_options.index(cur_cat) if cur_cat in cat_options else 0,
                    label_visibility="collapsed",
                    key=f"cat_{proc}",
                )
            with ec3:
                new_dist = st.checkbox("Distraction", value=cur_dist,
                                       key=f"dist_{proc}",
                                       label_visibility="collapsed")
            with ec4:
                if st.button("Save", key=f"save_cat_{proc}",
                              use_container_width=True):
                    categories.set_override(proc, new_cat, new_dist)
                    st.cache_data.clear()
                    st.success(f"{proc} -> {new_cat}")
                    st.rerun()

    # --- Tools ---
    st.markdown("**Tools**")
    tl1, tl2, tl3 = st.columns(3)
    with tl1:
        if st.button("Test toast notification", use_container_width=True):
            from notifications import toast
            ok = toast("Pulse", "Test notification — toasts work.")
            st.success("Sent") if ok else st.warning("Failed — see logs/notifications.log")
    with tl2:
        if st.button("Run alert checks now", use_container_width=True):
            from alerts import run_all_checks
            result = run_all_checks()
            st.info(f"Fired: {result}")
    with tl3:
        if st.button("Show welcome wizard", use_container_width=True):
            set_setting("onboarded", "")
            st.rerun()

    # --- Diagnostics ---
    st.markdown("**Diagnostics**")
    from db import DB_PATH
    db_size_mb = DB_PATH.stat().st_size / 1024 / 1024 if DB_PATH.exists() else 0
    n_subs = conn.execute("SELECT COUNT(*) AS n FROM subscriptions").fetchone()["n"]
    n_active = conn.execute("SELECT COUNT(*) AS n FROM subscriptions WHERE active = 1").fetchone()["n"]
    n_apps = conn.execute("SELECT COUNT(*) AS n FROM app_activity").fetchone()["n"]
    n_tokens = conn.execute("SELECT COUNT(*) AS n FROM token_usage").fetchone()["n"]
    rates = cached_fx_rates()
    rate_now = rates["rates"].get(current_currency(), 1.0)
    st.markdown(
        f"<div style='font-size:0.82rem; color:var(--text-secondary); line-height:1.7;'>"
        f"DB: <strong>{db_size_mb:.1f} MB</strong> · "
        f"Subs: <strong>{n_active}/{n_subs}</strong> · "
        f"Activity: <strong>{n_apps:,}</strong> rows · "
        f"Tokens: <strong>{n_tokens:,}</strong> rows<br>"
        f"FX: 1 USD = {rate_now:.4f} {current_currency()} "
        f"({rates.get('source', '?')}, {rates.get('date', '?')})"
        f"</div>",
        unsafe_allow_html=True,
    )

    with st.expander("Tracker log + alert history"):
        alerts_df = pd.read_sql_query(
            "SELECT kind, body, sent_at FROM alert_log ORDER BY sent_at DESC LIMIT 10",
            conn,
        )
        if not alerts_df.empty:
            st.dataframe(alerts_df, hide_index=True,
                         use_container_width=True, height=160)
        else:
            st.caption("(no alerts yet)")
        log_path = Path(__file__).parent / "logs" / "tracker.log"
        if log_path.exists():
            with open(log_path, "r", encoding="utf-8") as f:
                tail = f.readlines()[-15:]
            st.code("".join(tail) or "(empty)", language=None)


# ============================================================
# PAGE: HEALTH
# ============================================================
def render_health():
    # Marketing-style about page — full Pulse brand identity (real SVG)
    st.markdown(
        '<div style="display:flex; align-items:center; gap:18px; margin-bottom:10px;">'
        '<div style="width:72px; height:72px; flex-shrink:0; '
        'filter:drop-shadow(0 2px 12px rgba(0,229,160,0.4));">'
        + _PULSE_LOGO_SVG +
        '</div>'
        f'<div>'
        f'<h1 style="margin:0;">{APP_NAME}</h1>'
        f'<div style="color:var(--text-secondary); font-size:0.95rem;">{APP_TAGLINE}</div>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown("")
    st.markdown(
        f"""
        **{APP_NAME}** helps you see where your subscriptions, AI usage, and computer time
        actually go — and saves you money by catching unused subscriptions before
        they auto-renew.

        - **Local-first.** All data lives on your computer. Nothing is sent to a server.
        - **Private by design.** No accounts, no logins, no telemetry.
        - **Always working.** A small background process tracks what you use, even when
          the dashboard is closed.
        """
    )

    # 3-pillar feature highlight cards
    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown(
            '<div style="background:var(--accent-bg); border:1px solid var(--accent-border); '
            'border-radius:10px; padding:14px; height:100%;">'
            '<div style="font-size:1.4rem;">💳</div>'
            '<div style="font-weight:600; margin-top:4px;">Subscriptions</div>'
            '<div style="font-size:0.85rem; color:var(--text-secondary);">Track every recurring charge. '
            'Get warned before they renew. Spot the dead ones.</div></div>',
            unsafe_allow_html=True,
        )
    with p2:
        st.markdown(
            '<div style="background:var(--accent-bg); border:1px solid var(--accent-border); '
            'border-radius:10px; padding:14px; height:100%;">'
            '<div style="font-size:1.4rem;">🤖</div>'
            '<div style="font-weight:600; margin-top:4px;">AI usage</div>'
            '<div style="font-size:0.85rem; color:var(--text-secondary);">See exactly what your AI '
            'subscription is worth — token equivalent vs flat plan cost.</div></div>',
            unsafe_allow_html=True,
        )
    with p3:
        st.markdown(
            '<div style="background:var(--success-bg); border:1px solid var(--success-border); '
            'border-radius:10px; padding:14px; height:100%;">'
            '<div style="font-size:1.4rem;">⏱️</div>'
            '<div style="font-weight:600; margin-top:4px;">Activity</div>'
            '<div style="font-size:0.85rem; color:var(--text-secondary);">Time per app, '
            'auto-categorized. Find what you actually use vs what you pay for.</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("")
    st.markdown(f"Version 1.0 — local-only, no account required.")
    st.caption("Made with ♥ in Bangkok.")

    # Diagnostics — in expander, collapsed by default
    st.markdown("---")
    with st.expander("Diagnostics — for troubleshooting", expanded=False):
        from db import DB_PATH
        db_size_mb = DB_PATH.stat().st_size / 1024 / 1024 if DB_PATH.exists() else 0
        fx_path = Path(__file__).parent / "data" / "fx_cache.json"
        fx_age = "—"
        if fx_path.exists():
            age_h = (datetime.now().timestamp() - fx_path.stat().st_mtime) / 3600
            fx_age = f"{age_h:.1f}h ago"

        conn = get_conn()
        n_subs = conn.execute("SELECT COUNT(*) AS n FROM subscriptions").fetchone()["n"]
        n_active = conn.execute("SELECT COUNT(*) AS n FROM subscriptions WHERE active = 1").fetchone()["n"]
        n_apps = conn.execute("SELECT COUNT(*) AS n FROM app_activity").fetchone()["n"]
        n_tokens = conn.execute("SELECT COUNT(*) AS n FROM token_usage").fetchone()["n"]

        k1, k2, k3, k4 = st.columns(4)
        with k1: kpi_card("Database size", f"{db_size_mb:.1f} MB")
        with k2: kpi_card("Subscriptions", f"{n_active} active / {n_subs} total")
        with k3: kpi_card("App records", f"{n_apps:,}")
        with k4: kpi_card("Token records", f"{n_tokens:,}")

        st.markdown("**Last sync**")
        syncs = get_sync_status()
        if syncs:
            df = pd.DataFrame(syncs)
            st.dataframe(df, hide_index=True, use_container_width=True, height=110)
        else:
            st.caption("No syncs yet — visit AI usage and click Sync now.")

        rates = cached_fx_rates()
        rate_now = rates["rates"].get(current_currency(), 1.0)
        st.markdown(
            f"**Exchange rate** — 1 USD = {rate_now:.4f} {current_currency()} "
            f"(`{rates.get('source', '?')}`, {rates.get('date', '?')}, cached {fx_age})"
        )

        st.markdown("**Recent alerts**")
        alerts_df = pd.read_sql_query(
            "SELECT kind, target_id, body, sent_at FROM alert_log "
            "ORDER BY sent_at DESC LIMIT 20",
            conn,
        )
        if alerts_df.empty:
            st.caption("(no alerts sent yet)")
        else:
            st.dataframe(alerts_df, hide_index=True, use_container_width=True, height=180)

        st.markdown("**Tracker log (last 20 lines)**")
        log_path = Path(__file__).parent / "logs" / "tracker.log"
        if log_path.exists():
            with open(log_path, "r", encoding="utf-8") as f:
                tail = f.readlines()[-20:]
            st.code("".join(tail) or "(empty)", language=None)
        else:
            st.caption("(no log yet)")


# ============================================================
# PAGE: OVERVIEW (Home)
# ============================================================
def compute_streak() -> int:
    """Consecutive days (counting today or yesterday as start) with AI usage."""
    conn = get_conn()
    rows = conn.execute(
        "SELECT DISTINCT DATE(timestamp, 'localtime') AS d FROM token_usage "
        "WHERE source = 'claude_code_log' ORDER BY d DESC LIMIT 365"
    ).fetchall()
    if not rows:
        return 0
    try:
        dates = [datetime.fromisoformat(r["d"]).date() for r in rows]
    except Exception:
        return 0
    today = date.today()
    if dates[0] == today:
        start = today
    elif dates[0] == today - timedelta(days=1):
        start = dates[0]
    else:
        return 0
    streak = 1
    for i in range(1, len(dates)):
        if dates[i] == start - timedelta(days=streak):
            streak += 1
        else:
            break
    return streak


def _render_overview_plan_roi(token_cost: float, today_d) -> None:
    """Hero ROI card — celebrates value, shown at the top of Overview."""
    if token_cost <= 0:
        return
    plan = plan_monthly_usd()
    if plan <= 0:
        return
    days_elapsed = today_d.day
    plan_so_far = plan * (days_elapsed / 30.0)
    roi = token_cost / max(plan_so_far, 0.01)
    savings_so_far = max(token_cost - plan_so_far, 0)
    deficit_so_far = max(plan_so_far - token_cost, 0)
    roi_quip = quips.for_roi(roi)

    if roi >= 10:
        title, badge_text = "Legendary value", "Top 1% efficiency"
        emotion = "You're an absolute power user this month."
        stars_filled = 5
        tone_bg, tone_border, tone_color = "var(--success-bg)", "var(--success-border)", "var(--success)"
    elif roi >= 5:
        title, badge_text = "Excellent value", "Power user"
        emotion = "Outstanding ROI — keep going."
        stars_filled = 5
        tone_bg, tone_border, tone_color = "var(--success-bg)", "var(--success-border)", "var(--success)"
    elif roi >= 2:
        title, badge_text = "Great value", "Smart spender"
        emotion = "Plan more than pays for itself."
        stars_filled = 4
        tone_bg, tone_border, tone_color = "var(--success-bg)", "var(--success-border)", "var(--success)"
    elif roi >= 1:
        title, badge_text = "Plan paying off", "Break-even"
        emotion = "Covering its cost — use more to unlock bigger savings."
        stars_filled = 3
        tone_bg, tone_border, tone_color = "var(--accent-bg)", "var(--accent-border)", "var(--accent)"
    elif roi >= 0.5:
        title, badge_text = "Underused", "Below break-even"
        emotion = "Use the plan more this month, or pay per-API."
        stars_filled = 2
        tone_bg, tone_border, tone_color = "var(--warning-bg)", "var(--warning-border)", "var(--warning)"
    else:
        title, badge_text = "Plan idle", "Consider downgrading"
        emotion = "AI usage far below plan cost this month."
        stars_filled = 1
        tone_bg, tone_border, tone_color = "var(--warning-bg)", "var(--warning-border)", "var(--warning)"

    stars_html = (
        '<span style="color:' + tone_color + '; letter-spacing:3px; font-size:0.95rem;">'
        + ("★" * stars_filled)
        + '<span style="color:var(--border-strong);">'
        + ("★" * (5 - stars_filled))
        + '</span></span>'
    )
    coverage_pct = min((plan_so_far / token_cost) * 100, 100) if token_cost > 0 else 0

    if savings_so_far > 0:
        saved_block = (
            f'<div style="margin-top:12px; padding:10px 12px; background:var(--bg-card); '
            f'border:1px solid var(--border); border-radius:10px;">'
            f'<div style="font-size:0.68rem; color:var(--text-secondary); '
            f'text-transform:uppercase; letter-spacing:0.06em; font-weight:600;">'
            f'SAVED THIS MONTH</div>'
            f'<div style="font-size:1.6rem; font-weight:800; color:{tone_color}; '
            f'line-height:1.1; margin-top:2px; font-variant-numeric:tabular-nums;">'
            f'{fmt_local_compact(savings_so_far)}</div>'
            f'<div style="font-size:0.74rem; color:var(--text-muted);">'
            f'{fmt_usd_ref(savings_so_far, 0)} vs paying per-API</div></div>'
        )
    elif deficit_so_far > 0:
        saved_block = (
            f'<div style="margin-top:12px; padding:10px 12px; background:var(--bg-card); '
            f'border:1px solid var(--border); border-radius:10px;">'
            f'<div style="font-size:0.68rem; color:var(--text-secondary); '
            f'text-transform:uppercase; letter-spacing:0.06em; font-weight:600;">'
            f'AHEAD ON PLAN</div>'
            f'<div style="font-size:1.4rem; font-weight:700; color:{tone_color}; '
            f'line-height:1.1; margin-top:2px;">'
            f'-{fmt_local_compact(deficit_so_far)}</div>'
            f'<div style="font-size:0.74rem; color:var(--text-muted);">'
            f'so far this month</div></div>'
        )
    else:
        saved_block = ""

    quip_html = (
        f'<div style="margin-top:6px; font-size:0.78rem; color:{tone_color}; '
        f'font-style:italic;">{escape(roi_quip)}</div>'
        if roi_quip else ""
    )

    st.markdown(
        f'<div style="background:{tone_bg}; border:1px solid {tone_border}; '
        f'border-radius:14px; padding:16px 18px; margin-bottom:14px;">'
        f'<div style="display:flex; justify-content:space-between; align-items:center; '
        f'margin-bottom:8px;">'
        f'<div>'
        f'<div style="font-size:0.68rem; color:{tone_color}; '
        f'text-transform:uppercase; letter-spacing:0.06em; font-weight:700;">{title}</div>'
        f'<div style="font-size:0.74rem; color:var(--text-muted); margin-top:1px;">'
        f'{badge_text}</div>'
        f'</div>'
        f'<div>{stars_html}</div>'
        f'</div>'
        f'<div style="font-size:2.4rem; font-weight:800; color:{tone_color}; '
        f'line-height:1; font-variant-numeric:tabular-nums; letter-spacing:-0.02em;">'
        f'{roi:.1f}<span style="font-size:1.3rem; margin-left:4px;">×</span></div>'
        f'<div style="font-size:0.74rem; color:var(--text-secondary); '
        f'margin-top:2px;">return on plan cost (this month)</div>'
        f'<div style="font-size:0.88rem; color:var(--text-primary); '
        f'margin-top:8px; line-height:1.4;">{emotion}</div>'
        f'<div style="margin-top:10px;">'
        f'<div style="display:flex; justify-content:space-between; '
        f'font-size:0.7rem; color:var(--text-secondary); margin-bottom:3px;">'
        f'<span>Plan: <strong style="color:var(--text-primary);">'
        f'{fmt_local_compact(plan_so_far)}</strong></span>'
        f'<span>API: <strong style="color:var(--text-primary);">'
        f'{fmt_local_compact(token_cost)}</strong></span>'
        f'</div>'
        f'<div style="height:6px; background:var(--bg-hover); border-radius:3px; '
        f'overflow:hidden; position:relative;">'
        f'<div style="position:absolute; left:0; top:0; bottom:0; '
        f'width:{coverage_pct:.1f}%; '
        f'background:linear-gradient(90deg, {tone_color}, var(--accent));"></div>'
        f'</div></div>'
        f'{saved_block}'
        f'{quip_html}'
        f'</div>',
        unsafe_allow_html=True,
    )


def render_overview():
    import os, getpass
    user_display = getpass.getuser().capitalize()
    hour = datetime.now().hour
    if hour < 12:    greeting = "Good morning"
    elif hour < 18:  greeting = "Good afternoon"
    else:            greeting = "Good evening"

    streak = compute_streak()
    # Streak chip — gains a soft glow at "elite" level (30+ days)
    streak_class = " pulse-streak-elite" if streak >= 30 else ""
    streak_html = (
        f'<span class="pulse-streak-chip{streak_class}" '
        f'style="display:inline-block; margin-left:10px; padding:3px 11px; '
        f'background:var(--accent-bg); color:var(--accent); font-size:0.78rem; '
        f'font-weight:600; border:1px solid var(--accent-border); '
        f'border-radius:999px; vertical-align:middle;">{streak}-day streak</span>'
        if streak >= 2 else ""
    )

    # Pick a tagline quip — replaces the generic subtitle when conditions trigger
    streak_quip = quips.for_streak(streak)
    subtitle = streak_quip or "Here's where your money and time went."

    # Greeting + animated ECG line — Pulse's signature visual element.
    # Subtle pulse animation reinforces brand identity without being noisy.
    st.markdown(
        f'<div style="margin-bottom:22px;">'
        f'<h1 style="margin-bottom:4px;">{greeting}, {escape(user_display)}{streak_html}</h1>'
        f'<div style="font-size:0.92rem; color:var(--text-secondary); margin-bottom:14px;">'
        f'{escape(subtitle)}</div>'
        f'<div class="pulse-ecg-line"></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # ----- Plan ROI hero (moved to top — celebrate first) -----
    today_d = date.today()
    conn = get_conn()
    this_month_start = today_d.replace(day=1).isoformat()
    tk_row_top = conn.execute(
        "SELECT COALESCE(SUM(cost_usd), 0) AS c FROM token_usage WHERE timestamp >= ?",
        (this_month_start,)
    ).fetchone()
    token_cost_top = float(tk_row_top["c"] or 0)
    _render_overview_plan_roi(token_cost_top, today_d)

    # ----- Top KPI strip -----
    all_subs = load_subscriptions(active_only=False)
    active_subs = all_subs[all_subs["active"] == 1]

    real_monthly = 0.0
    wasted_monthly = 0.0
    needs_attention = 0
    upcoming = []
    today_d = date.today()
    for _, row in active_subs.iterrows():
        d = row.to_dict()
        color, _, _ = smart_status(d)
        me_usd = monthly_equiv_usd(d)
        if color == "red":
            wasted_monthly += me_usd
        else:
            real_monthly += me_usd
        if color in ("amber", "blue"):
            needs_attention += 1
        # Renewals in next 14 days
        nb = d.get("next_billing_date")
        if nb:
            try:
                nb_d = datetime.fromisoformat(nb).date()
                days_left = (nb_d - today_d).days
                if 0 <= days_left <= 14:
                    upcoming.append((days_left, d["name"], d["cost"], d["currency"]))
            except Exception:
                pass

    # Token spend this month + last month (for comparison)
    conn = get_conn()
    this_month_start = today_d.replace(day=1).isoformat()
    last_month_start = (today_d.replace(day=1) - timedelta(days=1)).replace(day=1).isoformat()
    last_month_end = today_d.replace(day=1).isoformat()  # exclusive

    tk_row = conn.execute(
        "SELECT COALESCE(SUM(cost_usd), 0) AS c, COUNT(*) AS n "
        "FROM token_usage WHERE timestamp >= ?", (this_month_start,)
    ).fetchone()
    token_cost = float(tk_row["c"] or 0)
    token_msgs = int(tk_row["n"] or 0)

    # Same-day-of-month last month (so "1st-10th this month" vs "1st-10th last")
    last_month_same_day = conn.execute(
        "SELECT COALESCE(SUM(cost_usd), 0) AS c FROM token_usage "
        "WHERE timestamp >= ? AND timestamp < DATE(?, '+' || ? || ' days')",
        (last_month_start, last_month_start, str(today_d.day - 1))
    ).fetchone()
    token_cost_last_period = float(last_month_same_day["c"] or 0)

    # App hours this week + last week
    week_start = (today_d - timedelta(days=7)).isoformat()
    last_week_start = (today_d - timedelta(days=14)).isoformat()
    app_row = conn.execute(
        "SELECT COALESCE(SUM(duration_seconds), 0) AS s "
        "FROM app_activity WHERE started_at >= ?", (week_start,)
    ).fetchone()
    app_hours = (app_row["s"] or 0) / 3600
    app_row_last = conn.execute(
        "SELECT COALESCE(SUM(duration_seconds), 0) AS s "
        "FROM app_activity WHERE started_at >= ? AND started_at < ?",
        (last_week_start, week_start)
    ).fetchone()
    app_hours_last = (app_row_last["s"] or 0) / 3600

    # Helper: format trend delta
    def trend_str(now, before):
        if before <= 0:
            return ""
        delta_pct = (now - before) / before * 100
        if abs(delta_pct) < 2:
            return "≈ same as last period"
        sign = "↑" if delta_pct > 0 else "↓"
        color = "var(--danger)" if delta_pct > 0 else "var(--success)"
        return f'<span style="color:{color}; font-weight:600;">{sign} {abs(delta_pct):.0f}%</span> vs last period'

    token_trend = trend_str(token_cost, token_cost_last_period)
    app_trend = trend_str(app_hours, app_hours_last)

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        kpi_card("Subscriptions",
                 f"{fmt_local_compact(real_monthly)}/mo",
                 fmt_usd_ref(real_monthly))
    with k2:
        kpi_card("AI this month",
                 fmt_local_compact(token_cost),
                 token_trend or f"{token_msgs:,} messages")
    with k3:
        kpi_card("App hours (7d)",
                 f"{app_hours:.1f}h",
                 app_trend or f"{len(active_subs)} active subs")
    with k4:
        if wasted_monthly > 0:
            wasted_quip = quips.for_wasted(fmt_local_compact(wasted_monthly), True)
            kpi_card("Likely wasted",
                     f"{fmt_local_compact(wasted_monthly)}/mo",
                     wasted_quip or fmt_usd_ref(wasted_monthly),
                     color="danger")
        elif needs_attention:
            kpi_card("Need attention", f"{needs_attention}",
                     "items to verify", color="warning")
        else:
            healthy_quip = quips.for_healthy_stack(len(active_subs), wasted_monthly, needs_attention)
            kpi_card("All good", "—",
                     healthy_quip or "no issues detected",
                     color="success")

    st.markdown("")

    # ----- Two-column: upcoming renewals + insights — equal widths + matched boxes -----
    # Both columns use min-height so content (2-3 lines) fits without clipping
    # while still keeping visual rhythm matched.
    BOX_STYLE = (
        "padding:14px 16px; border-radius:10px; margin-bottom:12px; "
        "min-height:90px; box-sizing:border-box; "
        "display:flex; flex-direction:column; justify-content:center;"
    )
    cl, cr = st.columns([1, 1])
    with cl:
        st.markdown("##### Upcoming renewals (next 14 days)")
        if upcoming:
            upcoming.sort()
            for days_left, name, cost, ccy in upcoming[:5]:
                badge_color = "var(--danger)" if days_left < 3 else ("var(--warning)" if days_left < 7 else "var(--success)")
                lbl = "today" if days_left == 0 else f"in {days_left}d"
                st.markdown(
                    f'<div style="{BOX_STYLE} '
                    f'display:flex; justify-content:space-between; align-items:center; '
                    f'border:1px solid var(--border); background:var(--bg-card);">'
                    f'<div>'
                    f'<div style="font-weight:600; font-size:0.92rem;">{escape(name)}</div>'
                    f'<div style="font-size:0.78rem; color:{badge_color}; font-weight:600;">renews {lbl}</div>'
                    f'</div>'
                    f'<div style="text-align:right; font-variant-numeric:tabular-nums;">'
                    f'<div style="font-weight:600;">{fx.symbol(ccy)}{cost:,.2f}</div>'
                    f'<div style="font-size:0.75rem; color:var(--text-secondary);">{ccy}</div>'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        else:
            pulse_empty(
                "Quiet ahead",
                "No renewals in the next 2 weeks. Enjoy the breathing room.",
                ICON_CALENDAR_EMPTY,
            )

    with cr:
        st.markdown("##### Insights")
        # Find highest-cost project this month
        top_project = pd.read_sql_query(
            "SELECT project_tag, SUM(cost_usd) AS c "
            "FROM token_usage WHERE timestamp >= ? "
            "GROUP BY project_tag ORDER BY c DESC LIMIT 1",
            conn, params=(this_month_start,)
        )
        if not top_project.empty and top_project.iloc[0]["c"]:
            p = top_project.iloc[0]
            st.markdown(
                f'<div style="{BOX_STYLE} background:{ACCENT_BG}; '
                f'border:1px solid {ACCENT_BORDER};">'
                f'<div style="font-size:0.78rem; color:var(--text-secondary);">Top AI spend this month</div>'
                f'<div style="font-weight:600; margin-top:2px;">{escape(p["project_tag"] or "untagged")}</div>'
                f'<div style="font-variant-numeric:tabular-nums; color:var(--text-primary);">{fmt_local(p["c"], 0)}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        if wasted_monthly > 0:
            wasted_yr = wasted_monthly * 12
            st.markdown(
                f'<div style="{BOX_STYLE} background:var(--danger-bg); '
                f'border:1px solid var(--danger-border);">'
                f'<div style="font-size:0.78rem; color:var(--danger);">Possible savings</div>'
                f'<div style="font-weight:600; margin-top:2px; color:var(--text-primary);">'
                f'Cancel idle subs to save {fmt_local(wasted_yr, 0)}/yr</div>'
                f'<div style="font-size:0.75rem; color:var(--text-primary);">{fmt_usd_ref(wasted_yr, 0)}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        if needs_attention > 0:
            st.markdown(
                f'<div style="{BOX_STYLE} background:var(--warning-bg); '
                f'border:1px solid var(--warning-border);">'
                f'<div style="font-size:0.78rem; color:var(--warning);">Action needed</div>'
                f'<div style="font-weight:600; margin-top:2px; color:var(--warning);">'
                f'{needs_attention} subscription(s) need verification</div>'
                f'<div style="font-size:0.75rem; color:var(--warning);">'
                f'Check the Subscriptions tab</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        if upcoming and not (wasted_monthly > 0 or needs_attention > 0):
            st.markdown(
                f'<div style="{BOX_STYLE} background:var(--success-bg); '
                f'border:1px solid var(--success-border);">'
                f'<div style="font-size:0.78rem; color:var(--success);">Healthy stack</div>'
                f'<div style="font-weight:600; margin-top:2px; color:var(--text-primary);">No issues detected</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # ----- Savings tracker (cumulative lifetime savings) -----
    savings_row = conn.execute(
        "SELECT COUNT(*) AS n, COALESCE(SUM(cancelled_monthly_usd), 0) AS sum "
        "FROM subscriptions WHERE cancelled_at IS NOT NULL "
        "AND cancelled_monthly_usd IS NOT NULL"
    ).fetchone()
    n_cancelled = int(savings_row["n"] or 0)
    monthly_saved = float(savings_row["sum"] or 0)
    # Compute lifetime savings since first cancel
    if n_cancelled > 0:
        first_cancel_row = conn.execute(
            "SELECT MIN(cancelled_at) AS first_c FROM subscriptions "
            "WHERE cancelled_at IS NOT NULL AND cancelled_monthly_usd IS NOT NULL"
        ).fetchone()
        first_cancel_iso = first_cancel_row["first_c"]
        try:
            first_cancel_d = datetime.fromisoformat(first_cancel_iso[:19]).date()
            months_since = max((today_d - first_cancel_d).days / 30.4375, 0.1)
            lifetime_saved = monthly_saved * months_since
        except Exception:
            lifetime_saved = monthly_saved
        st.markdown(
            f'<div class="pulse-savings-shimmer" '
            f'style="border:1px solid var(--success-border); '
            f'border-radius:10px; padding:12px 16px; margin-top:12px; font-size:0.88rem;">'
            f'<div style="font-weight:700; margin-bottom:4px; color:var(--success);">'
            f'Lifetime savings</div>'
            f'<div style="color:var(--text-secondary);">'
            f'You\'ve cancelled <strong>{n_cancelled}</strong> subscription(s), '
            f'saving roughly <strong style="color:var(--text-primary);">'
            f'{fmt_local_compact(lifetime_saved)}</strong> '
            f'<span style="color:var(--text-muted);">({fmt_usd_ref(lifetime_saved, 0)})</span> '
            f'since you started using Pulse — '
            f'<strong style="color:var(--text-primary);">{fmt_local_compact(monthly_saved)}/mo</strong> ongoing'
            f'</div></div>',
            unsafe_allow_html=True,
        )

    # Plan ROI display moved to top of render_overview (called as
    # _render_overview_plan_roi right after the greeting).

    # Spend-today quip if it's notably high or spiking
    today_iso = today_d.isoformat()
    today_cost = float(conn.execute(
        "SELECT COALESCE(SUM(cost_usd), 0) AS c FROM token_usage WHERE DATE(timestamp, 'localtime') = ?",
        (today_iso,)
    ).fetchone()["c"] or 0)
    avg_cost_30d = float(conn.execute(
        """
        SELECT COALESCE(AVG(daily), 0) AS avg_c FROM (
          SELECT DATE(timestamp, 'localtime') AS d, SUM(cost_usd) AS daily
          FROM token_usage
          WHERE DATE(timestamp, 'localtime') >= DATE('now', 'localtime', '-30 days')
            AND DATE(timestamp, 'localtime') < ?
          GROUP BY d
        )
        """,
        (today_iso,)
    ).fetchone()["avg_c"] or 0)

    high_quip = quips.for_today_spend(today_cost, plan_monthly_usd() / 30.0) \
                or quips.for_spike(today_cost, avg_cost_30d)
    if high_quip:
        st.markdown(
            f'<div style="margin-top:8px; padding:10px 14px; background:var(--warning-bg); '
            f'border:1px solid var(--warning-border); border-radius:8px; font-size:0.88rem; '
            f'color:var(--text-primary); font-style:italic;">'
            f'{escape(high_quip)} · today\'s AI spend: '
            f'<strong>{fmt_local_compact(today_cost)}</strong></div>',
            unsafe_allow_html=True,
        )


# ============================================================
# Route
# ============================================================
if page == "Overview":
    render_overview()
elif page == "Subscriptions":
    render_subscriptions()
elif page == "Activity":
    render_apps()
elif page == "AI usage":
    render_tokens()
elif page == "Settings":
    render_settings()
