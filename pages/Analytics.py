"""Analytics dashboard page for HireFlow Analytics."""

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
        .hf-chart-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 1.25rem;
            min-height: 260px;
        }
        .hf-chart-title {
            color: #101828;
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        .hf-chart-text {
            color: #475467;
            font-size: 0.95rem;
            line-height: 1.6;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_header() -> None:
    st.markdown('<div class="hf-breadcrumb">Dashboard &gt; Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="hf-page-title">Analytics</div>', unsafe_allow_html=True)
    st.markdown(
        (
            '<div class="hf-page-subtitle">'
            'Interactive analytics panels will become active once backend metrics are integrated.'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def render_page() -> None:
    _apply_page_style()
    _render_header()
    st.info("No analytics data available. Metrics will load after backend integration.")

    with st.container():
        left, right = st.columns(2, gap="large")
        with left:
            st.markdown(
                '<div class="hf-chart-card">'
                '<div class="hf-chart-title">Funnel Analytics</div>'
                '<div class="hf-chart-text">This visualization will populate once recruitment pipeline data is connected.</div>'
                '</div>',
                unsafe_allow_html=True,
            )
        with right:
            st.markdown(
                '<div class="hf-chart-card">'
                '<div class="hf-chart-title">Department Performance</div>'
                '<div class="hf-chart-text">Department analytics will display here after backend data is available.</div>'
                '</div>',
                unsafe_allow_html=True,
            )

    st.write("")
    st.markdown(
        '<div class="hf-chart-card">'
        '<div class="hf-chart-title">Hiring Trends</div>'
        '<div class="hf-chart-text">Trend charts and heatmaps will render after the analytics backend is connected.</div>'
        '</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    st.set_page_config(page_title="Analytics | HireFlow Analytics", layout="wide")
    render_page()
