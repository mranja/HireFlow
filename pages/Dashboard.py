"""Overview dashboard page for HireFlow Analytics."""

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
        .hf-placeholder-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 1.25rem;
            min-height: 180px;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04);
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
    st.markdown('<div class="hf-breadcrumb">Home &gt; Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="hf-page-title">Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        (
            '<div class="hf-page-subtitle">'
            'A polished, enterprise-ready view of hiring health and people operations.'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    header_col, action_col = st.columns([3.2, 1.1], gap="small")
    with header_col:
        st.caption(
            "Welcome back, HR leadership team. The dashboard is prepared for live recruitment metrics once backend integration is enabled."
        )
    with action_col:
        st.caption("Last updated: Awaiting backend sync")
        st.button("Refresh", disabled=True, use_container_width=True)


def _render_kpi_section() -> None:
    kpi_items = [
        {
            "title": "Total Candidates",
            "value": "0",
            "icon": "👥",
            "subtitle": "Placeholder KPI for future candidate volume.",
            "trend_placeholder": "Pending data",
            "status_color": "#2563eb",
        },
        {
            "title": "Active Recruiters",
            "value": "0",
            "icon": "🤝",
            "subtitle": "Placeholder KPI for team availability.",
            "trend_placeholder": "Pending data",
            "status_color": "#7c3aed",
        },
        {
            "title": "Open Positions",
            "value": "0",
            "icon": "💼",
            "subtitle": "Placeholder KPI for current hiring demand.",
            "trend_placeholder": "Pending data",
            "status_color": "#0f766e",
        },
        {
            "title": "Scheduled Interviews",
            "value": "0",
            "icon": "📅",
            "subtitle": "Placeholder KPI for interview load.",
            "trend_placeholder": "Pending data",
            "status_color": "#ea580c",
        },
        {
            "title": "Departments",
            "value": "0",
            "icon": "🏢",
            "subtitle": "Placeholder KPI for hiring coverage.",
            "trend_placeholder": "Pending data",
            "status_color": "#db2777",
        },
        {
            "title": "Offers Released",
            "value": "0",
            "icon": "🎯",
            "subtitle": "Placeholder KPI for offer activity.",
            "trend_placeholder": "Pending data",
            "status_color": "#16a34a",
        },
    ]
    render_kpi_grid(kpi_items, columns=3)


def _render_analytics_placeholders() -> None:
    with st.container():
        analytics_cols = st.columns(3, gap="large")
        placeholder_cards = [
            (
                "Recruitment Trend",
                "The recruitment trend view will appear once historical hiring data is available.",
            ),
            (
                "Hiring Funnel",
                "The funnel breakdown will render after candidate pipeline metrics are connected.",
            ),
            (
                "Department Distribution",
                "This section will display department-wise hiring balance when backend analytics are ready.",
            ),
        ]

        for column, (title, description) in zip(analytics_cols, placeholder_cards):
            with column:
                st.markdown(
                    f"""
                    <div class="hf-placeholder-card">
                        <div class="hf-card-title">{title}</div>
                        <div class="hf-card-text">{description}</div>
                        <div class="hf-pill">Waiting for data</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def _render_activity_sections() -> None:
    st.divider()
    st.markdown('<div class="hf-section-title">Recent Activity</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hf-placeholder-card">'
        '<div class="hf-card-title">No recent activity available.</div>'
        '<div class="hf-card-text">Activity feed entries will appear after workflow events are connected.</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.write("")
    st.markdown('<div class="hf-section-title">Upcoming Interviews</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hf-placeholder-card">'
        '<div class="hf-card-title">No upcoming interviews.</div>'
        '<div class="hf-card-text">Interview scheduling data will display here after backend integration.</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.write("")
    st.markdown('<div class="hf-section-title">Recent Candidates</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hf-placeholder-card">'
        '<div class="hf-card-title">No candidates available.</div>'
        '<div class="hf-card-text">Candidate activity will show up once the data layer is connected.</div>'
        '</div>',
        unsafe_allow_html=True,
    )


def render_page() -> None:
    """Render the dashboard layout with placeholder sections for future integration."""
    _apply_page_style()
    _render_header()
    st.divider()

    st.markdown('<div class="hf-section-title">KPI Overview</div>', unsafe_allow_html=True)
    _render_kpi_section()

    st.divider()
    st.markdown('<div class="hf-section-title">Analytics Overview</div>', unsafe_allow_html=True)
    _render_analytics_placeholders()

    _render_activity_sections()


if __name__ == "__main__":
    st.set_page_config(page_title="Dashboard | HireFlow Analytics", layout="wide")
    render_page()
