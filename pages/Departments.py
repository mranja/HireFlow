"""Department Management page for HireFlow Analytics."""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st


DEPARTMENT_COLUMNS = [
    "Department Name",
    "Department Head",
    "Recruiters",
    "Candidates",
    "Open Positions",
    "Status",
    "Created Date",
]

DEPARTMENT_STATUSES = [
    "Active",
    "Hiring",
    "Paused",
    "Inactive",
]

SORT_OPTIONS = [
    "Department Name",
    "Department Head",
    "Recruiters",
    "Candidates",
    "Open Positions",
    "Created Date",
]

ACTIVITY_EVENTS = [
    ("Department Created", "Date placeholder will appear after backend connection."),
    ("Recruiter Assigned", "Recruiter details will display once available."),
    ("Job Opened", "Open position entries will be populated later."),
    ("Candidate Assigned", "Candidate assignment updates will appear here."),
    ("Hiring Completed", "Completion status will render after backend integration."),
]


def _apply_page_style() -> None:
    """Apply consistent department management page styling."""
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 1440px;
            padding-bottom: 2.5rem;
            padding-top: 1.5rem;
        }
        .hf-breadcrumb {
            color: #667085;
            font-size: 0.92rem;
            margin-bottom: 0.25rem;
        }
        .hf-page-title {
            color: #101828;
            font-size: 2.1rem;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 0.35rem;
        }
        .hf-page-subtitle {
            color: #475467;
            font-size: 1rem;
            margin-bottom: 1.5rem;
        }
        .hf-section-title {
            color: #101828;
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 0.75rem;
        }
        .hf-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 18px;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
            padding: 1.25rem;
        }
        .hf-small-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 1rem;
            min-height: 148px;
        }
        .hf-card-label {
            color: #475569;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            margin-bottom: 0.35rem;
            text-transform: uppercase;
        }
        .hf-card-value {
            color: #0f172a;
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        .hf-card-note {
            color: #64748b;
            font-size: 0.9rem;
            line-height: 1.6;
        }
        .hf-metric-grid {
            gap: 1rem;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        }
        .hf-table-placeholder {
            border: 1px dashed #cbd5e1;
            border-radius: 16px;
            padding: 1.25rem;
            background: #f8fafc;
            color: #334155;
            margin-top: 0.75rem;
        }
        .hf-chart-placeholder {
            background: #f8fafc;
            border: 1px dashed #cbd5e1;
            border-radius: 16px;
            min-height: 260px;
            padding: 1rem;
            color: #475569;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .hf-activity-item {
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            background: #ffffff;
            padding: 1rem;
            margin-bottom: 0.8rem;
        }
        .hf-activity-title {
            color: #0f172a;
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }
        .hf-activity-meta {
            color: #64748b;
            font-size: 0.92rem;
            line-height: 1.5;
        }
        .hf-detail-label {
            color: #475569;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.03em;
            margin-bottom: 0.35rem;
            text-transform: uppercase;
        }
        .hf-detail-value {
            color: #0f172a;
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        .hf-details-grid {
            gap: 1rem;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        }
        .hf-disabled-button {
            opacity: 0.65;
        }
        div[data-testid="stMetric"] {
            border-radius: 16px;
            box-shadow: none;
            border: 1px solid #e2e8f0;
            background: #ffffff;
            padding: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_header() -> None:
    """Render the department management page header and description."""
    st.markdown('<div class="hf-breadcrumb">Dashboard &gt; Departments</div>', unsafe_allow_html=True)
    st.markdown('<div class="hf-page-title">Department Management</div>', unsafe_allow_html=True)
    st.markdown(
        (
            '<div class="hf-page-subtitle">'
            'Review department performance, operational health, and hiring readiness. '
<<<<<<< HEAD
            'All data will populate automatically after backend integration.'
            '</div>'
=======
            'All data will populate automatically after backend integration.'</div>'
>>>>>>> 7f1d561fe854ff79ec4ca6fdf2bd11bb2e359dc2
        ),
        unsafe_allow_html=True,
    )


def _empty_department_dataframe() -> pd.DataFrame:
    """Return an empty dataframe with the expected department schema."""
    return pd.DataFrame(columns=DEPARTMENT_COLUMNS)


def _render_summary_metrics() -> None:
    """Render top KPI cards for departments."""
    cols = st.columns(5, gap="large")
    cols[0].metric("Total Departments", "—")
    cols[1].metric("Active Departments", "—")
    cols[2].metric("Total Recruiters", "—")
    cols[3].metric("Total Candidates", "—")
    cols[4].metric("Open Positions", "—")


def _render_toolbar() -> None:
    """Render search, status, sort, and refresh controls."""
    with st.container():
        search_col, status_col, sort_col, refresh_col = st.columns([1.6, 1.1, 1.1, 0.7], gap="large")

        with search_col:
            st.text_input(
                "Search Department",
                placeholder="Search by department name or department head",
                key="department_search",
            )

        with status_col:
            st.multiselect(
                "Status Filter",
                options=DEPARTMENT_STATUSES,
                placeholder="All statuses",
                key="department_status_filter",
            )

        with sort_col:
            st.selectbox(
                "Sort by",
                options=SORT_OPTIONS,
                index=0,
                key="department_sort",
            )

        with refresh_col:
            st.write("")
            st.button("Refresh", on_click=lambda: None, use_container_width=True)


def _render_department_table() -> None:
    """Render the department table layout with an enterprise empty state."""
    st.subheader("Department List")
    st.markdown(
        'Use the search, status filter, and sort controls to narrow your department list.',
    )

    department_df = _empty_department_dataframe()
    if department_df.empty:
        st.markdown(
<<<<<<< HEAD
            (
                '<div class="hf-table-placeholder">'
                '<strong>No departments available.</strong> '
                'Department records will appear here after backend integration.'
                '</div>'
            ),
=======
            '<div class="hf-table-placeholder">'
            '<strong>No departments available.</strong> '
            'Department records will appear here after backend integration.'</div>',
>>>>>>> 7f1d561fe854ff79ec4ca6fdf2bd11bb2e359dc2
            unsafe_allow_html=True,
        )
        st.dataframe(department_df, hide_index=True, use_container_width=True)
        return

    st.dataframe(department_df, hide_index=True, use_container_width=True)


def _render_department_details() -> None:
    """Render the left-hand department details panel."""
    st.subheader("Department Details")
    with st.expander("Department overview", expanded=True):
        with st.container():
            cols = st.columns([1.05, 1], gap="large")
            with cols[0]:
                st.markdown(
                    '<div class="hf-small-card">'
                    '<div class="hf-detail-label">Department Name</div>'
                    '<div class="hf-detail-value">No department selected</div>'
                    '<div class="hf-detail-label">Department Description</div>'
                    '<div class="hf-detail-value">Department information will appear after backend integration.</div>'
                    '<div class="hf-detail-label">Department Head</div>'
                    '<div class="hf-detail-value">—</div>'
                    '<div class="hf-detail-label">Team Size</div>'
                    '<div class="hf-detail-value">—</div>'
                    '</div>',
                    unsafe_allow_html=True,
                )
            with cols[1]:
                st.markdown(
                    '<div class="hf-small-card">'
                    '<div class="hf-detail-label">Number of Recruiters</div>'
                    '<div class="hf-detail-value">—</div>'
                    '<div class="hf-detail-label">Active Candidates</div>'
                    '<div class="hf-detail-value">—</div>'
                    '<div class="hf-detail-label">Open Positions</div>'
                    '<div class="hf-detail-value">—</div>'
                    '<div class="hf-detail-label">Hiring Status</div>'
                    '<div class="hf-detail-value">Awaiting data</div>'
                    '</div>',
                    unsafe_allow_html=True,
                )

        st.markdown(
            '<div class="hf-small-card" style="margin-top: 1rem;">'
            '<div class="hf-details-grid">'
            '<div><div class="hf-detail-label">Contact Email</div><div class="hf-detail-value">—</div></div>'
            '<div><div class="hf-detail-label">Contact Number</div><div class="hf-detail-value">—</div></div>'
            '<div><div class="hf-detail-label">Last Updated</div><div class="hf-detail-value">—</div></div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )


def _render_statistics_section() -> None:
    """Render the department statistics section ready for Plotly charts."""
    st.subheader("Department Statistics")
    st.markdown(
        'These charts will display once department analytics data is connected to the backend.',
    )

    stat_cols = st.columns(2, gap="large")
    with stat_cols[0]:
        st.metric("Candidates per Department", "—")
        st.markdown(
            '<div class="hf-chart-placeholder">Chart placeholder for candidates per department</div>',
            unsafe_allow_html=True,
        )
    with stat_cols[1]:
        st.metric("Recruiters per Department", "—")
        st.markdown(
            '<div class="hf-chart-placeholder">Chart placeholder for recruiters per department</div>',
            unsafe_allow_html=True,
        )

    stat_cols = st.columns(2, gap="large")
    with stat_cols[0]:
        st.metric("Open Positions", "—")
        st.markdown(
            '<div class="hf-chart-placeholder">Chart placeholder for open positions</div>',
            unsafe_allow_html=True,
        )
    with stat_cols[1]:
        st.metric("Hiring Progress", "—")
        st.markdown(
            '<div class="hf-chart-placeholder">Chart placeholder for hiring progress</div>',
            unsafe_allow_html=True,
        )


def _render_activity_timeline() -> None:
    """Render the department activity timeline placeholders."""
    st.subheader("Department Activity Timeline")
    st.markdown(
        'This timeline will show department activity events after backend integration.',
    )

    with st.expander("Department activity timeline", expanded=True):
        for title, description in ACTIVITY_EVENTS:
            st.markdown(
                f"""
                <div class="hf-activity-item">
                    <div class="hf-activity-title">{title}</div>
                    <div class="hf-activity-meta">{description}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_action_panel() -> None:
    """Render action buttons that are disabled until backend integration."""
    st.subheader("Action Panel")
    button_rows = [
        ["Add Department", "Edit Department", "Delete Department"],
        ["Assign Recruiter", "View Candidates", "View Analytics"],
    ]

    for row in button_rows:
        cols = st.columns(3, gap="large")
        for index, label in enumerate(row):
            cols[index].button(label, disabled=True, use_container_width=True)


def main() -> None:
    """Render the Department Management page."""
    _apply_page_style()
    _render_header()
    _render_summary_metrics()
    st.divider()
    _render_toolbar()
    _render_department_table()
    st.divider()
    _render_department_details()
    st.divider()
    _render_statistics_section()
    st.divider()
    _render_activity_timeline()
    st.divider()
    _render_action_panel()


if __name__ == "__main__":
<<<<<<< HEAD
    st.set_page_config(
        page_title="Departments | HireFlow Analytics",
        layout="wide",
    )
=======
>>>>>>> 7f1d561fe854ff79ec4ca6fdf2bd11bb2e359dc2
    main()
