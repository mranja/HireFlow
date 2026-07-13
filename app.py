"""HireFlow Analytics Streamlit application entry point."""

from __future__ import annotations

import streamlit as st

from components.sidebar import render_sidebar


def main() -> None:
    """Render the Streamlit application shell."""
    st.set_page_config(
        page_title="HireFlow Analytics",
        layout="wide",
    )
    render_sidebar()

    st.title("HireFlow Analytics")
    st.caption("Production-ready recruitment analytics built with Streamlit.")

    st.info("Open the Candidates page from the sidebar to manage candidate data.")


if __name__ == "__main__":
    main()
