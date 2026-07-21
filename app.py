"""HireFlow Analytics Streamlit application entry point."""

from __future__ import annotations

import streamlit as st

from components.sidebar import render_sidebar
from pages import Analytics, Dashboard

PAGE_ROUTES = {
    "Dashboard": Dashboard.render_page,
    "Analytics": Analytics.render_page,
}


def main() -> None:
    """Render the main HireFlow Analytics application with page navigation."""
    st.set_page_config(
        page_title="HireFlow Analytics",
        layout="wide",
    )

    selected_page = render_sidebar()
    page_handler = PAGE_ROUTES.get(selected_page)
    if page_handler is None:
        st.info("Select a page from the sidebar to continue.")
        return

    page_handler()


if __name__ == "__main__":
    main()
