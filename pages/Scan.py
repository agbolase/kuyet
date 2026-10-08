"""Leaf disease scanner page."""

import streamlit as st

from scanner_ui import render_scanner
from ui_theme import inject_global_styles, render_site_nav

st.set_page_config(
    page_title="Scan | TomatoCare",
    page_icon="🍅",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None,
)
render_site_nav("scan")
inject_global_styles()
with st.container(key="scan_page"):
    render_scanner()
