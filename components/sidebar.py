"""Sidebar utilities for the Streamlit application shell."""

from __future__ import annotations

import streamlit as st

<<<<<<< HEAD
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
=======

def render_sidebar() -> None:
    """Render the global HireFlow sidebar content."""
>>>>>>> 7f1d561fe854ff79ec4ca6fdf2bd11bb2e359dc2
    with st.sidebar:
        st.title("HireFlow Analytics")
        st.caption("Recruitment analytics workspace")
        st.divider()
<<<<<<< HEAD
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
=======
        st.markdown("Use the navigation menu to open Candidates and other modules.")
>>>>>>> 7f1d561fe854ff79ec4ca6fdf2bd11bb2e359dc2
