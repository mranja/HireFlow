"""Sidebar utilities for the Streamlit application shell."""

from __future__ import annotations

import streamlit as st

PAGE_OPTIONS = [
    "Dashboard",
    "Candidates",
    "Interviews",
    "Departments",
    "Recruitment Pipeline",
    "Analytics",
    "Reports",
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
            "Use the sidebar to navigate through the recruitment analytics workflow."
        )
    return selected_page
