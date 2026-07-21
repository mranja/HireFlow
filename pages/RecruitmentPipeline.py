"""Recruitment Pipeline page for HireFlow Analytics."""

from __future__ import annotations

import streamlit as st

from components.pipeline import render_pipeline_page


def main() -> None:
    """Render the recruitment pipeline page."""
    st.markdown(
        """
        <style>
        .block-container { max-width: 1440px; padding-top: 1.5rem; padding-bottom: 2.5rem; }
        .hf-breadcrumb { color: #667085; font-size: 0.92rem; margin-bottom: 0.25rem; }
        .hf-page-title { color: #101828; font-size: 2.1rem; font-weight: 700; margin-bottom: 0.3rem; }
        .hf-page-subtitle { color: #475467; font-size: 1rem; margin-bottom: 1rem; }
        .hf-page-card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 1rem 1.1rem; box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04); }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="hf-breadcrumb">Home &gt; Recruitment Pipeline</div>', unsafe_allow_html=True)
    st.markdown('<div class="hf-page-title">Recruitment Pipeline</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hf-page-subtitle">Track the hiring journey and visualize pipeline progress from a consistent, enterprise-ready UI.</div>',
        unsafe_allow_html=True,
    )
    st.caption("Pipeline views are prepared for live data once backend integration is connected.")
    with st.container():
        st.markdown(
            '<div class="hf-page-card">Pipeline details and stage progression will be presented here in a clean, reusable layout.</div>',
            unsafe_allow_html=True,
        )

    render_pipeline_page()


if __name__ == "__main__":
    st.set_page_config(
        page_title="Recruitment Pipeline | HireFlow Analytics",
        layout="wide",
    )
    main()
