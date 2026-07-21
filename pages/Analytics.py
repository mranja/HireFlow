"""Analytics dashboard page for HireFlow Analytics."""

from __future__ import annotations

import streamlit as st

from components.metrics import render_kpi_grid


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
        .hf-section-title {
            color: #101828;
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 0.6rem;
        }
        .hf-chart-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 1.25rem;
            min-height: 220px;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04);
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
        .hf-pill {
            display: inline-block;
            margin-top: 0.75rem;
            padding: 0.3rem 0.6rem;
            border-radius: 999px;
            background: #f5f7fb;
            color: #344054;
            font-size: 0.78rem;
            font-weight: 600;
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
            'A placeholder analytics workspace for recruitment performance views and downstream reporting.'
            '</div>'
        ),
        unsafe_allow_html=True,
    )
    st.caption("Analytics panels are prepared for future backend integration and live reporting data.")


def _render_overview_kpis() -> None:
    kpi_items = [
        {
            "title": "Conversion Rate",
            "value": "0%",
            "icon": "📈",
            "subtitle": "Placeholder for applicant-to-offer performance.",
            "trend_placeholder": "Awaiting data",
            "status_color": "#2563eb",
        },
        {
            "title": "Average Time to Hire",
            "value": "0 days",
            "icon": "⏱️",
            "subtitle": "Placeholder for hiring efficiency.",
            "trend_placeholder": "Awaiting data",
            "status_color": "#7c3aed",
        },
        {
            "title": "Offer Acceptance",
            "value": "0%",
            "icon": "✅",
            "subtitle": "Placeholder for offer success metrics.",
            "trend_placeholder": "Awaiting data",
            "status_color": "#16a34a",
        },
    ]
    render_kpi_grid(kpi_items, columns=3)


def _render_placeholder_panels() -> None:
    st.divider()
    st.markdown('<div class="hf-section-title">Analytics Panels</div>', unsafe_allow_html=True)

    with st.container():
        left, right = st.columns(2, gap="large")
        with left:
            st.markdown(
                '<div class="hf-chart-card">'
                '<div class="hf-chart-title">Funnel Analytics</div>'
                '<div class="hf-chart-text">This visualization will populate once recruitment pipeline data is connected.</div>'
                '<div class="hf-pill">Waiting for data</div>'
                '</div>',
                unsafe_allow_html=True,
            )
        with right:
            st.markdown(
                '<div class="hf-chart-card">'
                '<div class="hf-chart-title">Department Performance</div>'
                '<div class="hf-chart-text">Department analytics will display here after backend data is available.</div>'
                '<div class="hf-pill">Waiting for data</div>'
                '</div>',
                unsafe_allow_html=True,
            )

    st.write("")
    st.markdown(
        '<div class="hf-chart-card">'
        '<div class="hf-chart-title">Hiring Trends</div>'
        '<div class="hf-chart-text">Trend charts and heatmaps will render after the analytics backend is connected.</div>'
        '<div class="hf-pill">Waiting for data</div>'
        '</div>',
        unsafe_allow_html=True,
    )


def render_page() -> None:
    """Render the analytics landing page with placeholder panels."""
    _apply_page_style()
    _render_header()
    st.divider()
    _render_overview_kpis()
    _render_placeholder_panels()


if __name__ == "__main__":
    st.set_page_config(page_title="Analytics | HireFlow Analytics", layout="wide")
    render_page()
