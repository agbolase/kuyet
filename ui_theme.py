"""Shared TomatoCare landing theme and site navigation."""

from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
IMAGES = ROOT / "images"

THEME_DARK = "dark"
THEME_LIGHT = "light"


def image_data_uri(filename: str) -> str:
    path = IMAGES / filename
    mime = "image/jpeg" if path.suffix.lower() in {".jpg", ".jpeg"} else "image/png"
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}"


def current_theme() -> str:
    theme = st.session_state.get("tc_theme", THEME_DARK)
    if theme not in (THEME_DARK, THEME_LIGHT):
        theme = THEME_DARK
    st.session_state["tc_theme"] = theme
    return theme


def toggle_theme() -> None:
    if st.session_state.get("tc_theme", THEME_DARK) == THEME_DARK:
        st.session_state["tc_theme"] = THEME_LIGHT
    else:
        st.session_state["tc_theme"] = THEME_DARK


def _theme_variables(theme: str) -> str:
    if theme == THEME_LIGHT:
        return """
:root {
  color-scheme: light;
  --tc-bg: #f2faf5;
  --tc-bg-soft: #ffffff;
  --tc-card: rgba(255, 255, 255, 0.96);
  --tc-green: #1fa862;
  --tc-green-dark: #168a4f;
  --tc-tomato: #d45342;
  --tc-text: #102019;
  --tc-muted: #5a7166;
  --tc-border: rgba(31, 168, 98, 0.35);
  --tc-nav-border: rgba(16, 32, 25, 0.08);
  --tc-hero-scrim: linear-gradient(
    90deg,
    rgba(242, 250, 245, 0.96) 0%,
    rgba(242, 250, 245, 0.82) 45%,
    rgba(242, 250, 245, 0.45) 100%
  );
  --tc-hero-bg-filter: saturate(1.05) brightness(0.92);
  --tc-lead: rgba(16, 32, 25, 0.78);
  --tc-glow-green: rgba(31, 168, 98, 0.14);
  --tc-glow-tomato: rgba(212, 83, 66, 0.1);
  --tc-panel-bg: rgba(255, 255, 255, 0.82);
  --tc-panel-border: rgba(16, 32, 25, 0.08);
  --tc-badge-bg: rgba(255, 255, 255, 0.88);
  --tc-btn-secondary-bg: rgba(16, 32, 25, 0.04);
  --tc-btn-secondary-border: rgba(16, 32, 25, 0.12);
  --tc-icon-btn-bg: rgba(16, 32, 25, 0.04);
  --tc-icon-btn-border: rgba(16, 32, 25, 0.1);
  --tc-card-shadow: 0 18px 44px rgba(16, 32, 25, 0.12);
  --tc-primary-btn-text: #ffffff;
  --tc-block-border-bg: rgba(255, 255, 255, 0.9);
  --tc-block-border-color: rgba(16, 32, 25, 0.12);
  --tc-streamlit-input-bg: #ffffff;
}
"""
    return """
:root {
  color-scheme: dark;
  --tc-bg: #071410;
  --tc-bg-soft: #0c1c16;
  --tc-card: rgba(12, 28, 22, 0.92);
  --tc-green: #3ddc84;
  --tc-green-dark: #2bb86a;
  --tc-tomato: #e06b5a;
  --tc-text: #e8f5ec;
  --tc-muted: #8fa89a;
  --tc-border: rgba(61, 220, 132, 0.28);
  --tc-nav-border: rgba(255, 255, 255, 0.06);
  --tc-hero-scrim: linear-gradient(
    90deg,
    rgba(7, 20, 16, 0.94) 0%,
    rgba(7, 20, 16, 0.72) 45%,
    rgba(7, 20, 16, 0.35) 100%
  );
  --tc-hero-bg-filter: saturate(1.05) brightness(0.55);
  --tc-lead: rgba(232, 245, 236, 0.82);
  --tc-glow-green: rgba(61, 220, 132, 0.12);
  --tc-glow-tomato: rgba(224, 107, 90, 0.08);
  --tc-panel-bg: rgba(255, 255, 255, 0.03);
  --tc-panel-border: rgba(255, 255, 255, 0.08);
  --tc-badge-bg: rgba(7, 20, 16, 0.72);
  --tc-btn-secondary-bg: rgba(255, 255, 255, 0.06);
  --tc-btn-secondary-border: rgba(255, 255, 255, 0.12);
  --tc-icon-btn-bg: rgba(255, 255, 255, 0.04);
  --tc-icon-btn-border: rgba(255, 255, 255, 0.08);
  --tc-card-shadow: 0 24px 60px rgba(0, 0, 0, 0.35);
  --tc-primary-btn-text: #04210f;
  --tc-block-border-bg: rgba(255, 255, 255, 0.03);
  --tc-block-border-color: rgba(255, 255, 255, 0.1);
  --tc-streamlit-input-bg: rgba(255, 255, 255, 0.06);
}
"""


BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&display=swap');

section[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarNav"],
[data-testid="stSidebarUserContent"],
[data-testid="stSidebarHeader"] {
  display: none !important;
  width: 0 !important;
  min-width: 0 !important;
}
section.main {
  margin-left: 0 !important;
  max-width: 100% !important;
}
html.tc-coarse-pointer section.main:has([class*="home_screen"]),
html.tc-coarse-pointer section.main:has([class*="home_screen"]) .block-container {
  overflow: visible !important;
  max-height: none !important;
  padding-bottom: max(0.5rem, env(safe-area-inset-bottom, 0px)) !important;
}
@media (min-width: 769px) and (hover: hover) and (pointer: fine) {
  section.main:has([class*="home_screen"]) {
    overflow: hidden !important;
    max-height: 100dvh !important;
  }
  section.main:has([class*="home_screen"]) .block-container {
    overflow: hidden !important;
    max-height: 100dvh !important;
    padding-bottom: 0.25rem !important;
  }
  [class*="home_screen"] {
    height: calc(100dvh - 0.35rem);
    max-height: calc(100dvh - 0.35rem);
    overflow: hidden;
  }
}
header[data-testid="stHeader"] {
  display: none !important;
  height: 0 !important;
  min-height: 0 !important;
}
html, body, [data-testid="stAppViewContainer"], .stApp, section.main {
  overflow-x: hidden !important;
  max-width: 100% !important;
  -webkit-text-size-adjust: 100%;
  text-size-adjust: 100%;
}
.stApp {
  background: radial-gradient(1200px 600px at 10% -10%, var(--tc-glow-green), transparent 55%),
              radial-gradient(900px 500px at 90% 0%, var(--tc-glow-tomato), transparent 50%),
              var(--tc-bg) !important;
  color: var(--tc-text);
  font-family: "DM Sans", system-ui, sans-serif;
  min-height: 100dvh;
}
.block-container {
  padding-top: 0 !important;
  padding-bottom: 1.5rem !important;
  padding-left: clamp(0.75rem, 2.5vw, 1.25rem) !important;
  padding-right: clamp(0.75rem, 2.5vw, 1.25rem) !important;
  max-width: min(1180px, 100%) !important;
  width: 100% !important;
}
#MainMenu, footer, [data-testid="stToolbar"],
[data-testid="stMainMenuPopover"],
[data-testid="stHeaderActionElements"],
button[data-testid="baseButton-header"] {
  visibility: hidden !important;
  display: none !important;
  height: 0 !important;
  width: 0 !important;
  overflow: hidden !important;
  pointer-events: none !important;
}

[class*="site_nav"] {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: color-mix(in srgb, var(--tc-bg) 78%, transparent);
  backdrop-filter: blur(10px);
  padding: 0.15rem 0 0.35rem;
  margin: 0 0 0.25rem;
  border-bottom: 1px solid var(--tc-nav-border);
}
[class*="site_nav"] .stButton > button {
  border: none !important;
  box-shadow: none !important;
  background: transparent !important;
  color: var(--tc-muted) !important;
  font-weight: 500 !important;
  font-size: 0.92rem !important;
  padding: 0.35rem 0.55rem !important;
}
[class*="site_nav"] .stButton > button:hover:not(:disabled) {
  color: var(--tc-text) !important;
  background: rgba(255, 255, 255, 0.04) !important;
}
[class*="site_nav"] .stButton > button:disabled {
  color: var(--tc-green) !important;
  font-weight: 600 !important;
  opacity: 1 !important;
}
[class*="nav_logo"] .stButton > button {
  font-weight: 700 !important;
  font-size: 1.02rem !important;
  color: var(--tc-text) !important;
}
[class*="nav_scan_now"] .stButton > button {
  border-radius: 999px !important;
  padding: 0.55rem 1.15rem !important;
  font-weight: 600 !important;
  background: linear-gradient(180deg, var(--tc-green), var(--tc-green-dark)) !important;
  color: var(--tc-primary-btn-text) !important;
  box-shadow: 0 10px 28px rgba(61, 220, 132, 0.25);
}
[class*="site_nav"] .tc-nav-link {
  color: var(--tc-muted) !important;
  text-decoration: none !important;
  font-size: 0.92rem;
  font-weight: 500;
  display: inline-block;
  padding: 0.45rem 0.55rem;
}
[class*="site_nav"] .tc-nav-link:hover {
  color: var(--tc-text) !important;
}
[class*="hero_cta_row"] {
  position: relative;
  z-index: 2;
  margin: 0.65rem 0 0;
  max-width: min(22rem, 100%);
  padding: 0;
}
[class*="hero_cta_row"] > div,
[class*="hero_cta_row"] [data-testid="stVerticalBlock"] {
  gap: 0.5rem !important;
}
[class*="hero_cta_row"] [data-testid="stMarkdown"] {
  margin: 0 !important;
  padding: 0 !important;
  width: 100%;
}
[class*="hero_cta_row"] .stButton > button {
  width: 100%;
  min-height: 2.75rem;
  border-radius: 999px !important;
  font-weight: 600 !important;
}
[class*="hero_cta_row"] .stButton > button[kind="primary"] {
  background: linear-gradient(180deg, var(--tc-green), var(--tc-green-dark)) !important;
  color: var(--tc-primary-btn-text) !important;
  border: none !important;
}
.tc-hero-learn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-height: 2.75rem;
  padding: 0.55rem 1rem;
  box-sizing: border-box;
  border-radius: 999px;
  font-weight: 600;
  font-size: 0.92rem;
  text-decoration: none !important;
  color: var(--tc-text) !important;
  border: 1px solid var(--tc-btn-secondary-border);
  background: var(--tc-btn-secondary-bg);
}
.tc-hero-learn:hover {
  background: color-mix(in srgb, var(--tc-btn-secondary-bg) 70%, var(--tc-text) 8%);
}
section.main .block-container {
  position: relative;
  z-index: 2;
}

[class*="site_nav"] [data-testid="stHorizontalBlock"] {
  flex-wrap: nowrap !important;
  align-items: center !important;
  gap: 0.25rem !important;
  width: 100% !important;
}
[class*="site_nav"] [data-testid="column"] {
  min-width: 0 !important;
}
[class*="site_nav"] [data-testid="column"] [data-testid="stHorizontalBlock"] {
  flex-wrap: nowrap !important;
  justify-content: center !important;
}
[class*="site_nav"] [data-testid="column"] .stButton > button {
  width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
[class*="site_nav"] [data-testid="column"]:nth-child(2) .stButton > button {
  font-size: clamp(0.78rem, 1.6vw, 0.92rem) !important;
  padding: 0.3rem 0.4rem !important;
}
[class*="nav_desktop_row"] {
  display: none !important;
}
[class*="nav_mobile_bar"] {
  display: block !important;
}
@media (min-width: 769px) and (hover: hover) and (pointer: fine) {
  [class*="nav_desktop_row"] {
    display: block !important;
  }
  [class*="nav_mobile_bar"],
  [class*="nav_mobile_drawer"],
  [class*="nav_mobile_backdrop"] {
    display: none !important;
  }
}
[class*="nav_mobile_bar"] [data-testid="stHorizontalBlock"] {
  flex-direction: row !important;
  flex-wrap: nowrap !important;
  align-items: center !important;
  width: 100% !important;
}
[class*="nav_mobile_bar"] [data-testid="column"] {
  width: auto !important;
  min-width: 0 !important;
  flex: 0 1 auto !important;
}
[class*="nav_mobile_bar"] [data-testid="column"]:first-child {
  flex: 1 1 auto !important;
}
[class*="nav_mobile_bar"] [data-testid="column"]:last-child [data-testid="stHorizontalBlock"] {
  flex-wrap: nowrap !important;
  justify-content: flex-end !important;
}
[class*="nav_hamburger"] button,
[class*="nav_mobile_bar"] [class*="m_theme_toggle"] button {
  width: 2.75rem !important;
  min-width: 2.75rem !important;
  min-height: 2.75rem !important;
  padding: 0 !important;
  border-radius: 0.55rem !important;
  border: 1px solid var(--tc-icon-btn-border) !important;
  background: var(--tc-icon-btn-bg) !important;
  color: var(--tc-text) !important;
  font-size: 1.25rem !important;
  line-height: 1 !important;
}
[class*="nav_hamburger"] button:hover,
[class*="nav_mobile_bar"] [class*="m_theme_toggle"] button:hover {
  border-color: var(--tc-border) !important;
  background: rgba(255, 255, 255, 0.06) !important;
}
.stApp:has([class*="nav_mobile_drawer"]) {
  overflow: hidden !important;
  max-height: 100dvh !important;
}
[class*="nav_mobile_backdrop"] {
  display: block !important;
}
[class*="nav_mobile_backdrop"] .stButton {
  position: fixed !important;
  inset: 0 !important;
  z-index: 1001 !important;
  margin: 0 !important;
  padding: 0 !important;
  width: 100% !important;
  height: 100% !important;
}
[class*="nav_mobile_backdrop"] .stButton > button {
  position: fixed !important;
  inset: 0 !important;
  width: 100% !important;
  height: 100% !important;
  min-height: 100% !important;
  opacity: 0 !important;
  cursor: pointer !important;
  background: rgba(0, 0, 0, 0.45) !important;
  border: none !important;
  border-radius: 0 !important;
  padding: 0 !important;
}
[class*="nav_mobile_drawer"] {
  display: block !important;
  position: fixed !important;
  top: calc(env(safe-area-inset-top, 0px) + 3.15rem);
  left: max(0.65rem, env(safe-area-inset-left));
  right: max(0.65rem, env(safe-area-inset-right));
  z-index: 1002 !important;
  background: color-mix(in srgb, var(--tc-bg) 94%, transparent);
  backdrop-filter: blur(14px);
  border: 1px solid var(--tc-nav-border);
  border-radius: 0.85rem;
  padding: 0.5rem 0.35rem 0.65rem;
  box-shadow: var(--tc-card-shadow);
  max-height: calc(
    100dvh - env(safe-area-inset-top, 0px) - env(safe-area-inset-bottom, 0px) - 4rem
  );
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}
[class*="nav_mobile_drawer"] .stButton > button {
  width: 100% !important;
  justify-content: flex-start !important;
  text-align: left !important;
  min-height: 3rem !important;
  font-size: 1rem !important;
  padding: 0.65rem 0.85rem !important;
  border-radius: 0.55rem !important;
}
[class*="nav_mobile_drawer"] .stButton > button:disabled {
  background: rgba(61, 220, 132, 0.12) !important;
}
[class*="nav_mobile_drawer"] [class*="nav_m_scan"] .stButton > button[kind="primary"] {
  margin-top: 0.35rem;
  min-height: 3rem !important;
  border-radius: 999px !important;
}
.tc-page-content {
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
}

.tc-nav-row {
  border-bottom: 1px solid var(--tc-nav-border);
  margin-bottom: 0.5rem;
  padding-bottom: 0.35rem;
}
.tc-nav-wrap {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.35rem 0 0.15rem;
}
.tc-logo {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  font-weight: 700;
  font-size: 1.05rem;
  color: var(--tc-text);
  text-decoration: none;
}
.tc-logo-badge {
  width: 1.65rem;
  height: 1.65rem;
  border-radius: 999px;
  background: linear-gradient(145deg, #ff6b57, #c0392b);
  box-shadow: 0 0 0 2px rgba(224, 107, 90, 0.35);
}
.tc-nav-links {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.35rem;
  flex-wrap: wrap;
}
.tc-nav-link {
  color: var(--tc-muted) !important;
  text-decoration: none !important;
  font-size: 0.92rem;
  font-weight: 500;
  transition: color 0.15s ease;
}
.tc-nav-link:visited { color: var(--tc-muted) !important; }
.tc-nav-link:hover { color: var(--tc-text) !important; }
.tc-nav-link.active { color: var(--tc-green) !important; }
.tc-nav-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.65rem;
}
.tc-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  border-radius: 999px;
  padding: 0.55rem 1.15rem;
  font-weight: 600;
  font-size: 0.92rem;
  text-decoration: none;
  border: none;
  cursor: pointer;
  transition: transform 0.12s ease, background 0.12s ease;
}
.tc-btn:hover { transform: translateY(-1px); }
.tc-btn-primary {
  background: linear-gradient(180deg, var(--tc-green), var(--tc-green-dark));
  color: var(--tc-primary-btn-text);
  box-shadow: 0 10px 28px rgba(61, 220, 132, 0.25);
}
.tc-btn-secondary {
  background: var(--tc-btn-secondary-bg);
  color: var(--tc-text);
  border: 1px solid var(--tc-btn-secondary-border);
}
.tc-btn-lg { padding: 0.85rem 1.35rem; font-size: 1rem; }

[class*="theme_toggle"] button {
  width: 2.35rem;
  min-height: 2.35rem;
  padding: 0 !important;
  border-radius: 0.55rem !important;
  border: 1px solid var(--tc-icon-btn-border) !important;
  background: var(--tc-icon-btn-bg) !important;
  color: var(--tc-muted) !important;
  font-size: 1rem !important;
  line-height: 1 !important;
}
[class*="theme_toggle"] button:hover {
  color: var(--tc-text) !important;
  border-color: var(--tc-border) !important;
}
.tc-nav-scan-cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  white-space: nowrap;
}

.tc-hero {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr);
  gap: 2rem;
  align-items: center;
  padding: 2.5rem 0 3rem;
  min-height: min(72vh, 720px);
}
.tc-hero-single {
  grid-template-columns: minmax(0, 1fr);
}
.tc-home-backdrop {
  position: fixed;
  inset: 0;
  z-index: 0;
  background-size: cover;
  background-position: center center;
  background-repeat: no-repeat;
  filter: var(--tc-hero-bg-filter);
  pointer-events: none;
}
.tc-home-backdrop::after {
  content: "";
  position: absolute;
  inset: 0;
  background: var(--tc-hero-scrim);
  pointer-events: none;
}
[class*="home_screen"] {
  position: relative;
  z-index: 2;
  min-height: calc(100dvh - 0.35rem);
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  gap: 0.35rem;
  box-sizing: border-box;
  overflow-x: hidden;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}
[class*="home_screen"] > div {
  display: flex !important;
  flex-direction: column !important;
  flex: 1 1 auto !important;
  min-height: min(100%, 100dvh) !important;
  justify-content: flex-start !important;
  gap: 0.35rem !important;
}
[class*="home_screen"] [class*="site_nav"] {
  position: relative;
  top: auto;
  flex: 0 0 auto;
  margin-bottom: 0.1rem;
  padding-top: 0;
}
[class*="home_fold"] {
  position: relative;
  z-index: 2;
  box-sizing: border-box;
  flex: 0 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  gap: 0.4rem;
  padding-top: clamp(1rem, 5dvh, 2rem);
  padding-bottom: 0.35rem;
  margin-left: calc(-1 * clamp(0.75rem, 2.5vw, 1.25rem));
  margin-right: calc(-1 * clamp(0.75rem, 2.5vw, 1.25rem));
  padding-left: clamp(0.75rem, 2.5vw, 1.25rem);
  padding-right: clamp(0.75rem, 2.5vw, 1.25rem);
}
[class*="home_contact"] {
  flex: 0 0 auto;
  z-index: 2;
  margin-top: auto;
  padding-top: 0.75rem;
  padding-bottom: max(0.5rem, env(safe-area-inset-bottom, 0px));
}
[class*="home_fold"] > div {
  width: 100%;
  justify-content: flex-start !important;
}
[class*="home_fold"] [data-testid="stVerticalBlock"] {
  gap: 0.55rem;
  justify-content: flex-start !important;
}
.tc-hero-fullscreen {
  position: relative;
  width: 100%;
  min-height: 0;
  padding: 0;
  margin: 0;
  display: block;
  overflow: visible;
}
.tc-hero-bg,
.tc-hero::before {
  pointer-events: none;
}
.tc-hero:not(.tc-hero-fullscreen)::before {
  content: "";
  position: absolute;
  inset: -2rem -3rem auto -3rem;
  height: 120%;
  background: var(--tc-hero-scrim);
  pointer-events: none;
  z-index: 0;
}
.tc-hero > * { position: relative; z-index: 1; }
.tc-hero-content {
  max-width: min(40rem, 100%);
  width: 100%;
}
.tc-hero-bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center center;
  background-repeat: no-repeat;
  filter: var(--tc-hero-bg-filter);
  border-radius: 0;
  z-index: 0;
  pointer-events: none;
}
.tc-hero h1,
.tc-hero-content h1 {
  font-size: clamp(1.65rem, 3.2dvh + 1rem, 2.65rem);
  line-height: 1.08;
  letter-spacing: -0.03em;
  margin: 0 0 0.45rem;
  font-weight: 700;
  color: var(--tc-text);
}
.tc-hero h1 .tomato,
.tc-hero-content h1 .tomato { color: var(--tc-tomato); }
.tc-hero p.lead,
.tc-hero-content p.lead {
  color: var(--tc-lead);
  font-size: clamp(0.92rem, 1.1dvh + 0.75rem, 1.05rem);
  line-height: 1.55;
  max-width: 34rem;
  margin: 0 0 0.55rem;
}
.tc-hero-cta { display: flex; flex-wrap: wrap; gap: 0.85rem; align-items: center; }

.tc-card {
  background: var(--tc-card);
  border: 1px solid var(--tc-border);
  border-radius: 1.15rem;
  overflow: hidden;
  box-shadow: var(--tc-card-shadow);
}
.tc-card img {
  display: block;
  width: 100%;
  height: 220px;
  object-fit: cover;
}
.tc-card-body { padding: 1.15rem 1.25rem 1.35rem; }
.tc-card-body h3 {
  margin: 0 0 0.45rem;
  font-size: 1.05rem;
  color: var(--tc-text);
}
.tc-card-body p {
  margin: 0;
  color: var(--tc-muted);
  line-height: 1.55;
  font-size: 0.95rem;
}
.tc-badge {
  position: absolute;
  top: 0.85rem;
  left: 0.85rem;
  background: var(--tc-badge-bg);
  border: 1px solid var(--tc-border);
  color: var(--tc-green);
  padding: 0.35rem 0.65rem;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 600;
}
.tc-card-media { position: relative; }

.tc-section {
  padding: 2rem 0 1rem;
  scroll-margin-top: 4.5rem;
  max-width: 100%;
  position: relative;
  z-index: 2;
}
.tc-section-contact {
  margin: 0;
  padding: 0.65rem 0 0.35rem;
  border-top: 1px solid var(--tc-nav-border);
  background: color-mix(in srgb, var(--tc-bg) 92%, transparent);
}
.tc-section-contact h2 {
  font-size: 1rem !important;
  margin: 0 0 0.2rem !important;
}
.tc-section-contact p {
  font-size: 0.82rem !important;
  line-height: 1.4 !important;
  margin: 0 !important;
}
.tc-section h2 {
  font-size: 1.65rem;
  margin: 0 0 0.75rem;
  color: var(--tc-text);
}
.tc-section p, .tc-section li {
  color: var(--tc-muted);
  line-height: 1.65;
}
.tc-grid-2 {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.25rem;
}
.tc-panel {
  background: var(--tc-panel-bg);
  border: 1px solid var(--tc-panel-border);
  border-radius: 1rem;
  padding: 1.25rem 1.35rem;
}

@media (max-width: 900px) {
  .tc-hero { grid-template-columns: 1fr; min-height: auto; }
  .tc-grid-2 { grid-template-columns: 1fr; }
}

@media (max-width: 768px) {
  .block-container {
    padding-left: max(0.65rem, env(safe-area-inset-left)) !important;
    padding-right: max(0.65rem, env(safe-area-inset-right)) !important;
    padding-bottom: max(0.75rem, env(safe-area-inset-bottom)) !important;
  }
  [class*="home_screen"] {
    min-height: calc(
      100dvh - env(safe-area-inset-top, 0px) - env(safe-area-inset-bottom, 0px)
    );
    padding-bottom: env(safe-area-inset-bottom, 0px);
  }
  [class*="home_fold"] {
    margin-left: calc(-1 * max(0.65rem, env(safe-area-inset-left)));
    margin-right: calc(-1 * max(0.65rem, env(safe-area-inset-right)));
    padding-left: max(0.65rem, env(safe-area-inset-left));
    padding-right: max(0.65rem, env(safe-area-inset-right));
    padding-top: clamp(1.15rem, 6dvh, 2rem);
  }
  [class*="home_contact"] {
    padding-top: 0.85rem;
  }
  .tc-hero-content h1 {
    font-size: clamp(1.45rem, 6.5vw, 2rem) !important;
    margin-bottom: 0.35rem !important;
  }
  .tc-hero-content p.lead {
    font-size: 0.88rem !important;
    line-height: 1.45 !important;
    margin-bottom: 0.4rem !important;
  }
  [class*="hero_cta_row"] {
    max-width: min(20rem, 100%);
    margin-top: 0.75rem;
  }
  [class*="hero_cta_row"] .stButton > button,
  [class*="hero_cta_row"] .tc-hero-learn {
    min-height: 2.85rem;
    font-size: 0.95rem !important;
  }
  [class*="nav_mobile_bar"] > div > [data-testid="stHorizontalBlock"] {
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
  }
  [class*="nav_mobile_bar"] > div > [data-testid="stHorizontalBlock"] > [data-testid="column"] {
    width: auto !important;
    min-width: 0 !important;
    flex: 0 1 auto !important;
  }
  [class*="nav_mobile_bar"] > div > [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child {
    flex: 1 1 auto !important;
  }
  .tc-section-contact h2 { font-size: 0.92rem !important; }
  .tc-section-contact p { font-size: 0.78rem !important; }

  [class*="site_nav"] {
    padding-top: env(safe-area-inset-top, 0px);
  }
  [class*="nav_mobile_bar"] [class*="m_logo"] .stButton > button,
  [class*="nav_mobile_bar"] [class*="nav_logo"] .stButton > button {
    font-size: 0.86rem !important;
    text-align: left;
    min-height: 2.75rem;
  }
  [class*="nav_mobile_bar"] [class*="theme_toggle"] button,
  [class*="nav_mobile_bar"] [class*="m_theme_toggle"] button,
  [class*="nav_hamburger"] button {
    min-height: 2.75rem !important;
    min-width: 2.75rem !important;
  }

  [class*="scan_page"] .block-container {
    padding-left: max(0.65rem, env(safe-area-inset-left)) !important;
    padding-right: max(0.65rem, env(safe-area-inset-right)) !important;
  }
  [class*="scan_page"] [data-testid="stHorizontalBlock"] {
    flex-wrap: wrap !important;
  }
  [class*="scan_page"] [data-testid="column"] .stButton > button {
    min-height: 2.75rem;
  }
  [data-testid="stFileUploader"] section {
    padding: 0.65rem !important;
  }
}

@media (max-width: 480px) {
  [class*="nav_logo"] .stButton > button {
    font-size: 0.8rem !important;
  }
}

@media (max-height: 720px) {
  [class*="home_fold"] { padding-top: 0.2rem; }
  .tc-hero-content h1 { font-size: clamp(1.35rem, 5vw, 1.85rem) !important; }
  .tc-hero-content p.lead { margin-bottom: 0.3rem !important; }
  [class*="hero_cta_row"] .stButton > button { min-height: 2.25rem !important; }
  .tc-section-contact { padding-top: 0.35rem; }
}

h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, .stCaption {
  color: var(--tc-text) !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
  background: var(--tc-block-border-bg) !important;
  border-color: var(--tc-block-border-color) !important;
}
[data-testid="stFileUploader"], [data-baseweb="select"], textarea, input {
  background-color: var(--tc-streamlit-input-bg) !important;
}
[data-testid="stImage"] img {
  max-width: 100% !important;
  height: auto !important;
}
[class*="scan_page"] .block-container,
[class*="scan_page"] .tc-page-content {
  max-width: min(920px, 100%) !important;
}
</style>
"""


def inject_css(css: str) -> None:
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def inject_global_styles() -> None:
    inject_css(
        """
html.tc-coarse-pointer [class*="nav_desktop_row"] {
  display: none !important;
}
html.tc-coarse-pointer [class*="nav_mobile_bar"] {
  display: block !important;
}
"""
    )
    st.markdown(
        """
<script>
(function () {
  var root = document.documentElement;
  function syncPointerMode() {
    var coarse =
      window.matchMedia("(pointer: coarse)").matches ||
      window.matchMedia("(hover: none)").matches ||
      window.innerWidth < 769;
    root.classList.toggle("tc-coarse-pointer", coarse);
  }
  syncPointerMode();
  window.addEventListener("resize", syncPointerMode, { passive: true });
})();
</script>
        """,
        unsafe_allow_html=True,
    )
    theme = current_theme()
    base = BASE_CSS.strip()
    if base.startswith("<style>"):
        base = base[len("<style>") :]
    if base.endswith("</style>"):
        base = base[: -len("</style>")]
    inject_css(f"{_theme_variables(theme)}{base}")


def _nav_key(active: str, name: str) -> str:
    """Unique widget keys per page (required for Streamlit multipage apps)."""
    return f"nav_{active}_{name}"


def _go_home() -> None:
    st.switch_page("app.py")


def _go_scan() -> None:
    st.switch_page("pages/Scan.py")


def _go_history() -> None:
    st.switch_page("pages/History.py")


def _go_contact() -> None:
    st.switch_page("app.py")


def _close_mobile_nav() -> None:
    st.session_state["tc_mobile_nav_open"] = False


def _toggle_mobile_nav() -> None:
    st.session_state["tc_mobile_nav_open"] = not st.session_state.get(
        "tc_mobile_nav_open", False
    )


def _nav_after(fn) -> None:
    def _wrapped() -> None:
        _close_mobile_nav()
        fn()

    return _wrapped


def render_site_nav(active: str = "home") -> None:
    theme = current_theme()
    theme_label = "Switch to light mode" if theme == THEME_DARK else "Switch to dark mode"
    theme_icon = "☀" if theme == THEME_DARK else "☾"

    menu_open = st.session_state.get("tc_mobile_nav_open", False)

    with st.container(key=_nav_key(active, "site_nav")):
        with st.container(key=_nav_key(active, "nav_mobile_bar")):
            logo_col, menu_col, theme_col = st.columns(
                [5.5, 1, 1], gap="small", vertical_alignment="center"
            )
            with logo_col:
                with st.container(key=_nav_key(active, "m_logo")):
                    st.button(
                        "🍅 TomatoCare",
                        key=_nav_key(active, "m_logo_btn"),
                        type="tertiary",
                        on_click=_go_home,
                    )
            with menu_col:
                with st.container(key=_nav_key(active, "nav_hamburger")):
                    st.button(
                        "",
                        key=_nav_key(active, "hamburger_btn"),
                        help="Open menu" if not menu_open else "Close menu",
                        icon=":material/close:" if menu_open else ":material/menu:",
                        on_click=_toggle_mobile_nav,
                    )
            with theme_col:
                with st.container(key=_nav_key(active, "m_theme_toggle")):
                    st.button(
                        "",
                        key=_nav_key(active, "m_theme_btn"),
                        help=theme_label,
                        icon=":material/light_mode:" if theme == THEME_DARK else ":material/dark_mode:",
                        on_click=toggle_theme,
                    )

        with st.container(key=_nav_key(active, "nav_desktop_row")):
            logo_col, links_col, actions_col = st.columns(
                [1.55, 3.55, 2.4], gap="small", vertical_alignment="center"
            )
            with logo_col:
                with st.container(key=_nav_key(active, "logo")):
                    st.button(
                        "🍅 TomatoCare",
                        key=_nav_key(active, "logo_btn"),
                        type="tertiary",
                        on_click=_go_home,
                    )
            with links_col:
                with st.container(key=_nav_key(active, "nav_links_desktop")):
                    link_a, link_b, link_c, link_d = st.columns(
                        4, gap="small", vertical_alignment="center"
                    )
                    with link_a:
                        st.button(
                            "Home",
                            key=_nav_key(active, "home"),
                            type="tertiary",
                            disabled=active == "home",
                            on_click=_go_home,
                        )
                    with link_b:
                        st.button(
                            "Scan",
                            key=_nav_key(active, "scan"),
                            type="tertiary",
                            disabled=active == "scan",
                            on_click=_go_scan,
                        )
                    with link_c:
                        st.button(
                            "History",
                            key=_nav_key(active, "history"),
                            type="tertiary",
                            disabled=active == "history",
                            on_click=_go_history,
                        )
                    with link_d:
                        if active == "home":
                            st.markdown(
                                '<a class="tc-nav-link" href="#contact">Contact</a>',
                                unsafe_allow_html=True,
                            )
                        else:
                            st.button(
                                "Contact",
                                key=_nav_key(active, "contact"),
                                type="tertiary",
                                on_click=_go_contact,
                            )
            with actions_col:
                toggle_col, scan_col = st.columns(
                    [1, 2.2], gap="small", vertical_alignment="center"
                )
                with toggle_col:
                    with st.container(key=_nav_key(active, "theme_toggle")):
                        st.button(
                            theme_icon,
                            key=_nav_key(active, "theme_btn"),
                            help=theme_label,
                            on_click=toggle_theme,
                        )
                with scan_col:
                    with st.container(key=_nav_key(active, "nav_scan_now")):
                        st.button(
                            "📷 Scan",
                            key=_nav_key(active, "scan_now_btn"),
                            type="primary",
                            on_click=_go_scan,
                        )

        if st.session_state.get("tc_mobile_nav_open", False):
            with st.container(key=_nav_key(active, "nav_mobile_backdrop")):
                st.button(
                    "Close menu",
                    key=_nav_key(active, "mobile_backdrop_btn"),
                    on_click=_close_mobile_nav,
                )
            with st.container(key=_nav_key(active, "nav_mobile_drawer")):
                st.button(
                    "Home",
                    key=_nav_key(active, "m_home"),
                    type="tertiary",
                    disabled=active == "home",
                    on_click=_nav_after(_go_home),
                )
                st.button(
                    "Scan",
                    key=_nav_key(active, "m_scan"),
                    type="tertiary",
                    disabled=active == "scan",
                    on_click=_nav_after(_go_scan),
                )
                st.button(
                    "History",
                    key=_nav_key(active, "m_history"),
                    type="tertiary",
                    disabled=active == "history",
                    on_click=_nav_after(_go_history),
                )
                if active == "home":
                    st.button(
                        "Contact",
                        key=_nav_key(active, "m_contact"),
                        type="tertiary",
                        on_click=_close_mobile_nav,
                    )
                else:
                    st.button(
                        "Contact",
                        key=_nav_key(active, "m_contact"),
                        type="tertiary",
                        on_click=_nav_after(_go_contact),
                    )
                with st.container(key=_nav_key(active, "nav_m_scan")):
                    st.button(
                        "📷 Scan a Leaf",
                        key=_nav_key(active, "m_scan_cta"),
                        type="primary",
                        on_click=_nav_after(_go_scan),
                    )


def render_landing_page() -> None:
    hero_bg = image_data_uri("images2.jpeg")

    st.markdown(
        f"""
        <div class="tc-page-content tc-page-home">
        <div class="tc-home-backdrop" style="background-image: url('{hero_bg}');"></div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(key="home_fold"):
        st.markdown(
            """
            <div class="tc-hero-content">
              <h1>Check Your <span class="tomato">Tomato</span> Leaf</h1>
              <p class="lead">
                Take or upload a picture of a tomato leaf to check for common signs of disease.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.container(key="home_hero_cta_row"):
            st.button(
                "📷 Scan a Leaf",
                type="primary",
                key="home_hero_scan_leaf",
                on_click=_go_scan,
            )
            st.markdown(
                '<a class="tc-hero-learn" href="#contact">Learn More →</a>',
                unsafe_allow_html=True,
            )

    with st.container(key="home_contact"):
        st.markdown(
            """
            <section id="contact" class="tc-section tc-section-contact">
              <h2>Contact</h2>
              <p>Questions or feedback? Contact your extension officer or project maintainer.</p>
            </section>
            </div>
            """,
            unsafe_allow_html=True,
        )
