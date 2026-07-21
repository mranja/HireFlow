"""Overview dashboard page for HireFlow Analytics."""

from __future__ import annotations

import streamlit as st


def _apply_page_style() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 1440px;
            padding-top: 1.5rem;
            padding-bottom: 2.5rem;
        }
        .hf-breadcrumb {
            color: #667085;
            font-size: 0.92rem;
            margin-bottom: 0.35rem;
        }
        .hf-page-title {
            color: #101828;
            font-size: 2.1rem;
            font-weight: 700;
            margin-bottom: 0.35rem;
        }
        .hf-page-subtitle {
            color: #475467;
            font-size: 1rem;
            margin-bottom: 1rem;
        }
        .hf-placeholder-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 1.25rem;
            min-height: 180px;
        }
        .hf-card-title {
            color: #101828;
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        .hf-card-text {
            color: #475467;
            font-size: 0.95rem;
            line-height: 1.6;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_header() -> None:
    st.markdown('<div class="hf-breadcrumb">Home &gt; Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="hf-page-title">Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        (
            '<div class="hf-page-subtitle">'
            'Central hiring metrics and recruitment health will populate here after backend integration.'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def render_page() -> None:
    _apply_page_style()
    _render_header()

    st.info("No dashboard data available. Data will appear after backend integration.")

    metrics = st.columns(4, gap="large")
    metrics[0].metric("Total Candidates", "—")
    metrics[1].metric("Open Interviews", "—")
    metrics[2].metric("Departments Hiring", "—")
    metrics[3].metric("Offer Rate", "—")

    st.divider()
    st.markdown(
        '<div class="hf-placeholder-card">'
        '<div class="hf-card-title">Pipeline Summary</div>'
        '<div class="hf-card-text">The recruitment pipeline summary will appear once candidate and interview data are available.</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.write("")
    st.markdown(
        '<div class="hf-placeholder-card">'
        '<div class="hf-card-title">Hiring Velocity</div>'
        '<div class="hf-card-text">This chart will render after backend analytics are connected.</div>'
        '</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    st.set_page_config(page_title="Dashboard | HireFlow Analytics", layout="wide")
    render_page()
