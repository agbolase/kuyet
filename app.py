"""TomatoCare landing page and Streamlit entrypoint."""

from __future__ import annotations

import streamlit as st

from ui_theme import inject_global_styles, render_landing_page, render_site_nav


def main() -> None:
    st.set_page_config(
        page_title="TomatoCare",
        page_icon="🍅",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items=None,
    )
    inject_global_styles()
    with st.container(key="home_screen"):
        render_site_nav("home")
        render_landing_page()


if __name__ == "__main__":
    main()
