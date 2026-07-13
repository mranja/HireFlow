"""Sidebar utilities for the Streamlit application shell."""

from __future__ import annotations

import streamlit as st


def render_sidebar() -> None:
    """Render the global HireFlow sidebar content."""
    with st.sidebar:
        st.title("HireFlow Analytics")
        st.caption("Recruitment analytics workspace")
        st.divider()
        st.markdown("Use the navigation menu to open Candidates and other modules.")
