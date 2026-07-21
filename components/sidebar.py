"""Sidebar utilities for the Streamlit application shell."""

from __future__ import annotations

import streamlit as st

PAGE_OPTIONS = [
    "Dashboard",
    "Analytics",
]


def render_sidebar() -> str:
    """Render the global HireFlow sidebar navigation."""
    with st.sidebar:
        st.title("HireFlow Analytics")
        st.caption("Recruitment analytics workspace")
        st.divider()
        selected_page = st.radio(
            "Navigation",
            options=PAGE_OPTIONS,
            index=0,
            key="hireflow_sidebar_nav",
        )
        st.divider()
        st.markdown(
            "Use the sidebar to switch between the main HR analytics views."
        )
    return selected_page
