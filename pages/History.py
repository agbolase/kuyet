"""Scan history log page."""

import streamlit as st

from history_ui import render_history_page
from ui_theme import inject_global_styles, render_site_nav

st.set_page_config(
    page_title="History | TomatoCare",
    page_icon="🍅",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None,
)
render_site_nav("history")
inject_global_styles()
render_history_page()
