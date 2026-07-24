"""Analytics dashboard page for HireFlow Analytics."""

from __future__ import annotations

from typing import Any, Sequence

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from components.charts import render_bar_chart
from components.metrics import render_kpi_grid

DEFAULT_RECRUITMENT_STAGES: tuple[str, ...] = (
    "Applied",
    "Screening",
    "Assessment",
    "Technical Interview",
    "HR Interview",
    "Offer",
    "Accepted",
    "Joined",
)


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
        .hf-stage-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 0.85rem 1rem;
            margin-bottom: 0.55rem;
            box-shadow: 0 8px 22px rgba(15, 23, 42, 0.03);
        }
        .hf-stage-name {
            color: #101828;
            font-size: 0.95rem;
            font-weight: 700;
            margin-bottom: 0.3rem;
        }
        .hf-stage-meta {
            color: #475467;
            font-size: 0.87rem;
            line-height: 1.45;
        }
        .hf-stage-connector {
            text-align: center;
            color: #2563eb;
            font-size: 1.2rem;
            margin: 0.1rem 0 0.45rem;
        }
        .hf-empty-state {
            background: #f8fafc;
            border: 1px dashed #cbd5e1;
            border-radius: 14px;
            padding: 1rem 1.1rem;
            color: #475467;
            line-height: 1.6;
        }
        .hf-analytics-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 1rem 1.1rem;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04);
        }
        .hf-insight-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 0.9rem 1rem;
            min-height: 108px;
            box-shadow: 0 8px 22px rgba(15, 23, 42, 0.03);
        }
        .hf-insight-label {
            color: #667085;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 0.35rem;
        }
        .hf-insight-value {
            color: #101828;
            font-size: 1rem;
            font-weight: 700;
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
            'A production-ready recruitment analytics workspace for funnel health, conversion tracking, and reporting.'
            '</div>'
        ),
        unsafe_allow_html=True,
    )
    st.caption("The recruitment funnel and analytics panels are prepared for future backend integration.")


def _build_placeholder_kpis() -> list[dict[str, Any]]:
    return [
        {
            "title": "Total Applicants",
            "value": "—",
            "icon": "👥",
            "subtitle": "Placeholder for applicant volume.",
            "trend_placeholder": "Awaiting data",
            "status_color": "#2563eb",
        },
        {
            "title": "Overall Conversion Rate",
            "value": "—",
            "icon": "📈",
            "subtitle": "Placeholder for applicant-to-offer performance.",
            "trend_placeholder": "Awaiting data",
            "status_color": "#7c3aed",
        },
        {
            "title": "Total Drop-offs",
            "value": "—",
            "icon": "📉",
            "subtitle": "Placeholder for funnel loss tracking.",
            "trend_placeholder": "Awaiting data",
            "status_color": "#f59e0b",
        },
        {
            "title": "Final Hires",
            "value": "—",
            "icon": "✅",
            "subtitle": "Placeholder for accepted and joined hires.",
            "trend_placeholder": "Awaiting data",
            "status_color": "#16a34a",
        },
        {
            "title": "Hiring Efficiency",
            "value": "—",
            "icon": "⚡",
            "subtitle": "Placeholder for hiring throughput.",
            "trend_placeholder": "Awaiting data",
            "status_color": "#0f766e",
        },
    ]


def _render_overview_kpis() -> None:
    render_kpi_grid(_build_placeholder_kpis(), columns=5)


def _get_recruitment_funnel_data() -> Sequence[dict[str, Any]] | None:
    """Return recruitment funnel data when the backend is connected.

    The UI is intentionally designed to accept stage dictionaries with values
    such as stage_name, candidate_count, conversion_rate, and drop_off_rate.
    """
    return None


def _normalize_funnel_data(data: Sequence[dict[str, Any]] | None) -> list[dict[str, Any]]:
    if not data:
        return []

    normalized: list[dict[str, Any]] = []
    for stage_name in DEFAULT_RECRUITMENT_STAGES:
        match = None
        for item in data:
            candidate_name = str(
                item.get("stage_name") or item.get("stage") or item.get("name") or ""
            ).strip()
            if candidate_name.lower() == stage_name.lower():
                match = item
                break

        if match is None:
            continue

        candidate_count_raw = match.get("candidate_count") or match.get("count") or match.get("value")
        candidate_count = None
        if candidate_count_raw is not None:
            try:
                candidate_count = int(float(candidate_count_raw))
            except (TypeError, ValueError):
                candidate_count = None

        conversion_rate_raw = match.get("conversion_rate")
        conversion_rate = None
        if conversion_rate_raw is not None:
            try:
                conversion_rate = round(float(conversion_rate_raw), 1)
            except (TypeError, ValueError):
                conversion_rate = None

        drop_off_rate_raw = match.get("drop_off_rate")
        drop_off_rate = None
        if drop_off_rate_raw is not None:
            try:
                drop_off_rate = round(float(drop_off_rate_raw), 1)
            except (TypeError, ValueError):
                drop_off_rate = None

        normalized.append(
            {
                "stage_name": stage_name,
                "candidate_count": candidate_count,
                "conversion_rate": conversion_rate,
                "drop_off_rate": drop_off_rate,
            }
        )

    return normalized


def _build_funnel_metrics(stages: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    if not stages:
        return []

    prepared_stages: list[dict[str, Any]] = []
    initial_count = None
    for stage in stages:
        candidate_count = stage.get("candidate_count")
        if candidate_count is not None and candidate_count >= 0:
            initial_count = candidate_count if initial_count is None else initial_count
        prepared_stages.append(dict(stage))

    if initial_count is None or initial_count <= 0:
        return prepared_stages

    for index, stage in enumerate(prepared_stages):
        candidate_count = stage.get("candidate_count")
        if candidate_count is None:
            stage["conversion_rate"] = None
            stage["drop_off_rate"] = None
            continue

        if index == 0:
            stage["conversion_rate"] = 100.0
        else:
            stage["conversion_rate"] = round((candidate_count / initial_count) * 100, 1)

        if index == 0:
            stage["drop_off_rate"] = None
        else:
            previous_count = prepared_stages[index - 1].get("candidate_count")
            if previous_count is None or previous_count <= 0:
                stage["drop_off_rate"] = None
            else:
                stage["drop_off_rate"] = round(((previous_count - candidate_count) / previous_count) * 100, 1)

    return prepared_stages


def _render_funnel_chart(stages: Sequence[dict[str, Any]]) -> None:
    counts = [stage.get("candidate_count") or 0 for stage in stages]
    labels = [stage.get("stage_name") or "Stage" for stage in stages]

    figure = go.Figure(
        go.Funnel(
            y=labels,
            x=counts,
            text=[f"{stage.get('candidate_count') if stage.get('candidate_count') is not None else '—'}" for stage in stages],
            textposition="inside",
            connector={"line": {"color": "#94a3b8", "width": 2}},
            marker={
                "color": ["#2563eb", "#4f46e5", "#7c3aed", "#0f766e", "#0891b2", "#f59e0b", "#16a34a", "#ef4444"],
                "line": {"color": "rgba(15, 23, 42, 0.08)", "width": 1},
            },
            hovertemplate="<b>%{y}</b><br>Candidate count: %{x}<extra></extra>",
        )
    )

    figure.update_layout(
        template="plotly_white",
        margin=dict(l=24, r=24, t=30, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=420,
        font=dict(family="Inter, Arial, sans-serif", size=13, color="#334155"),
    )

    st.plotly_chart(figure, use_container_width=True, height=420)


def _render_stage_breakdown(stages: Sequence[dict[str, Any]]) -> None:
    for index, stage in enumerate(stages):
        with st.container():
            st.markdown(
                (
                    '<div class="hf-stage-card">'
                    f'<div class="hf-stage-name">{stage.get("stage_name")}</div>'
                    f'<div class="hf-stage-meta">Candidate count: <strong>{stage.get("candidate_count") if stage.get("candidate_count") is not None else "—"}</strong></div>'
                    f'<div class="hf-stage-meta">Conversion rate: <strong>{stage.get("conversion_rate") if stage.get("conversion_rate") is not None else "—"}%</strong></div>'
                    f'<div class="hf-stage-meta">Drop-off: <strong>{stage.get("drop_off_rate") if stage.get("drop_off_rate") is not None else "—"}%</strong></div>'
                    '</div>'
                ),
                unsafe_allow_html=True,
            )

        if index < len(stages) - 1:
            st.markdown('<div class="hf-stage-connector">↓</div>', unsafe_allow_html=True)


def _render_funnel_section() -> None:
    st.divider()
    st.markdown('<div class="hf-section-title">Recruitment Funnel</div>', unsafe_allow_html=True)

    funnel_data = _build_funnel_metrics(_normalize_funnel_data(_get_recruitment_funnel_data()))

    if not funnel_data:
        st.markdown(
            '<div class="hf-empty-state">No recruitment analytics available.<br/>Waiting for backend integration.</div>',
            unsafe_allow_html=True,
        )
        return

    with st.container():
        funnel_column, breakdown_column = st.columns([0.64, 0.36], gap="large")
        with funnel_column:
            _render_funnel_chart(funnel_data)
        with breakdown_column:
            _render_stage_breakdown(funnel_data)


def _get_department_comparison_data() -> Sequence[dict[str, Any]] | None:
    """Return department comparison data when the backend is connected."""
    return None


def _normalize_department_comparison_data(data: Sequence[dict[str, Any]] | None) -> pd.DataFrame | None:
    """Normalize future department comparison payloads into a reusable DataFrame."""
    if data is None:
        return None

    if isinstance(data, pd.DataFrame):
        dataframe = data.copy()
    elif isinstance(data, dict):
        dataframe = pd.DataFrame([data])
    elif isinstance(data, (list, tuple)):
        if not data:
            return pd.DataFrame()
        if isinstance(data[0], dict):
            dataframe = pd.DataFrame(data)
        else:
            return pd.DataFrame({"Department": list(data)})
    else:
        return None

    column_aliases = {
        "Department": ["department", "department_name", "dept", "team"],
        "Total Applications": ["total_applications", "applications_received", "applications", "applications_count"],
        "Candidates Shortlisted": ["candidates_shortlisted", "shortlisted", "shortlisted_candidates"],
        "Interviews Conducted": ["interviews_conducted", "interviews", "interview_count"],
        "Offers Released": ["offers_released", "offers", "offer_count"],
        "Hires": ["hires", "total_hires", "joined"],
        "Hiring Rate": ["hiring_rate", "hire_rate", "success_rate"],
        "Average Time to Hire": ["average_time_to_hire", "time_to_hire", "avg_time_to_hire"],
        "Status": ["status", "performance_status"],
    }

    normalized_columns = {column: column for column in dataframe.columns}
    for target_column, aliases in column_aliases.items():
        for alias in aliases:
            if alias in dataframe.columns:
                normalized_columns[alias] = target_column
                break

    dataframe = dataframe.rename(columns=normalized_columns)

    expected_columns = [
        "Department",
        "Total Applications",
        "Candidates Shortlisted",
        "Interviews Conducted",
        "Offers Released",
        "Hires",
        "Hiring Rate",
        "Average Time to Hire",
        "Status",
    ]
    for column_name in expected_columns:
        if column_name not in dataframe.columns:
            dataframe[column_name] = pd.NA

    return dataframe


def _render_department_comparison_filters() -> tuple[str, str, str]:
    """Render placeholder filters for the department comparison section."""
    st.markdown('<div class="hf-section-title">Filters</div>', unsafe_allow_html=True)
    filter_columns = st.columns([1.2, 1.2, 1.1, 0.8], gap="medium")

    with filter_columns[0]:
        st.selectbox("Department Selector", options=["All Departments", "Engineering", "Marketing", "Sales", "Finance", "HR", "Operations"], index=0, key="department_comparison_department")
    with filter_columns[1]:
        st.date_input("Date Range", value=(None, None), key="department_comparison_date_range")
    with filter_columns[2]:
        st.selectbox(
            "Hiring Metric",
            options=["Total Hires", "Hiring Rate", "Interviews Conducted", "Applications Received"],
            index=0,
            key="department_comparison_metric",
        )
    with filter_columns[3]:
        if st.button("Reset Filters", key="department_comparison_reset"):
            st.caption("Filter reset placeholders are ready for future integration.")

    st.caption("Filtering logic will be connected once the backend endpoint is available.")
    return (
        st.session_state.get("department_comparison_department", "All Departments") or "All Departments",
        "",
        st.session_state.get("department_comparison_metric", "Total Hires") or "Total Hires",
    )


def _render_department_comparison_table(dataframe: pd.DataFrame | None) -> None:
    """Render the ranked department comparison table with an empty state."""
    st.divider()
    st.markdown('<div class="hf-section-title">Ranked Department Table</div>', unsafe_allow_html=True)

    if dataframe is None or dataframe.empty:
        st.markdown(
            '<div class="hf-empty-state">No department analytics available.<br/>Waiting for backend integration.</div>',
            unsafe_allow_html=True,
        )
        return

    display_frame = dataframe.copy()
    display_frame = display_frame.replace({pd.NA: None})
    if "Rank" not in display_frame.columns:
        display_frame.insert(0, "Rank", range(1, len(display_frame) + 1))

    table_columns = [
        "Rank",
        "Department",
        "Total Applications",
        "Candidates Shortlisted",
        "Interviews Conducted",
        "Offers Released",
        "Hires",
        "Hiring Rate",
        "Average Time to Hire",
        "Status",
    ]
    display_frame = display_frame[[column for column in table_columns if column in display_frame.columns]]

    st.dataframe(
        display_frame,
        hide_index=True,
        width="stretch",
        height=360,
        use_container_width=True,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", format="%d"),
            "Department": st.column_config.TextColumn("Department"),
            "Total Applications": st.column_config.NumberColumn("Total Applications", format="%d"),
            "Candidates Shortlisted": st.column_config.NumberColumn("Candidates Shortlisted", format="%d"),
            "Interviews Conducted": st.column_config.NumberColumn("Interviews Conducted", format="%d"),
            "Offers Released": st.column_config.NumberColumn("Offers Released", format="%d"),
            "Hires": st.column_config.NumberColumn("Hires", format="%d"),
            "Hiring Rate": st.column_config.NumberColumn("Hiring Rate", format="%.1f %%"),
            "Average Time to Hire": st.column_config.TextColumn("Average Time to Hire"),
            "Status": st.column_config.TextColumn("Status"),
        },
    )


def _render_department_comparison_chart(dataframe: pd.DataFrame | None, metric_name: str) -> None:
    """Render a reusable bar chart for department comparison metrics."""
    st.divider()
    st.markdown('<div class="hf-section-title">Department Comparison Bar Chart</div>', unsafe_allow_html=True)

    if dataframe is None or dataframe.empty:
        st.markdown(
            '<div class="hf-empty-state">No department analytics available.<br/>Waiting for backend integration.</div>',
            unsafe_allow_html=True,
        )
        return

    metric_mapping = {
        "Total Hires": "Hires",
        "Hiring Rate": "Hiring Rate",
        "Interviews Conducted": "Interviews Conducted",
        "Applications Received": "Total Applications",
    }
    y_column = metric_mapping.get(metric_name, "Hires")
    chart_frame = dataframe[["Department", y_column]].copy()
    chart_frame = chart_frame.dropna(subset=[y_column])

    if chart_frame.empty:
        st.markdown(
            '<div class="hf-empty-state">No department analytics available.<br/>Waiting for backend integration.</div>',
            unsafe_allow_html=True,
        )
        return

    render_bar_chart(
        chart_frame,
        x_column="Department",
        y_column=y_column,
        title=f"Department Comparison by {metric_name}",
        height=360,
        color="#2563eb",
    )


def _render_department_insights(dataframe: pd.DataFrame | None) -> None:
    """Render performance-insight placeholders for the department comparison section."""
    st.divider()
    st.markdown('<div class="hf-section-title">Performance Insights</div>', unsafe_allow_html=True)

    if dataframe is None or dataframe.empty:
        st.markdown(
            '<div class="hf-empty-state">Insights will be available after backend integration.</div>',
            unsafe_allow_html=True,
        )
        return

    insight_items = [
        ("Top Performing Department", "Awaiting backend data"),
        ("Lowest Performing Department", "Awaiting backend data"),
        ("Highest Hiring Rate", "Awaiting backend data"),
        ("Longest Hiring Time", "Awaiting backend data"),
        ("Hiring Trend Summary", "Awaiting backend data"),
    ]

    insight_columns = st.columns(3, gap="medium")
    for index, (label, value) in enumerate(insight_items):
        with insight_columns[index % 3]:
            st.markdown(
                (
                    '<div class="hf-insight-card">'
                    f'<div class="hf-insight-label">{label}</div>'
                    f'<div class="hf-insight-value">{value}</div>'
                    '</div>'
                ),
                unsafe_allow_html=True,
            )


def _render_department_comparison_section() -> None:
    """Render the department comparison frontend section with placeholders for future data."""
    st.divider()
    st.markdown('<div class="hf-page-title">Department Performance Comparison</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hf-page-subtitle">Compare department-level hiring effectiveness, engagement, and conversion metrics in a polished executive-ready view.</div>',
        unsafe_allow_html=True,
    )

    header_columns = st.columns([0.72, 0.28], gap="medium")
    with header_columns[0]:
        st.caption("Last updated: Pending backend sync")
    with header_columns[1]:
        st.button("Export", disabled=True, key="department_comparison_export")

    department_data = _get_department_comparison_data()
    comparison_frame = _normalize_department_comparison_data(department_data)

    _render_department_comparison_filters()
    _render_department_comparison_table(comparison_frame)
    _render_department_comparison_chart(comparison_frame, st.session_state.get("department_comparison_metric", "Total Hires") or "Total Hires")
    _render_department_insights(comparison_frame)


def _render_conversion_summary(stages: Sequence[dict[str, Any]]) -> None:
    st.divider()
    st.markdown('<div class="hf-section-title">Conversion Summary</div>', unsafe_allow_html=True)

    if not stages:
        st.info("Conversion summary will appear after backend integration.", icon="📊")
        return

    summary_data = [
        {"stage": stage.get("stage_name", "Stage"), "count": stage.get("candidate_count") or 0}
        for stage in stages
    ]
    render_bar_chart(summary_data, x_column="stage", y_column="count", title="Stage Volume Summary", height=300, color="#2563eb")


def _render_drop_off_insights(stages: Sequence[dict[str, Any]]) -> None:
    st.divider()
    st.markdown('<div class="hf-section-title">Drop-off Insights</div>', unsafe_allow_html=True)

    if not stages:
        st.info("Drop-off insights will appear after backend integration.", icon="🧭")
        return

    insights_data = []
    for index in range(1, len(stages)):
        previous_stage = stages[index - 1]
        current_stage = stages[index]
        previous_count = previous_stage.get("candidate_count")
        current_count = current_stage.get("candidate_count")
        if previous_count is None or current_count is None or previous_count <= 0:
            continue
        drop_off = round(((previous_count - current_count) / previous_count) * 100, 1)
        insights_data.append(
            {
                "stage": f"{previous_stage.get('stage_name')} → {current_stage.get('stage_name')}",
                "drop_off": drop_off,
            }
        )

    if not insights_data:
        st.info("Drop-off insights will appear once candidate counts are available.", icon="🧭")
        return

    render_bar_chart(insights_data, x_column="stage", y_column="drop_off", title="Drop-off by Stage Pair", height=300, color="#f59e0b")


def _render_recommendations_placeholder() -> None:
    st.divider()
    st.markdown('<div class="hf-section-title">Recommendations</div>', unsafe_allow_html=True)
    with st.expander("Suggested next steps", expanded=False):
        st.write(
            "- Connect backend funnel data to populate stage counts and conversion percentages.\n"
            "- Add department, recruiter, and date-range filters for segmentation.\n"
            "- Extend the funnel with drill-down analytics for drop-off hotspots."
        )


def render_page() -> None:
    """Render the analytics landing page with a recruitment funnel overview."""
    _apply_page_style()
    _render_header()
    st.divider()
    _render_overview_kpis()
    funnel_data = _build_funnel_metrics(_normalize_funnel_data(_get_recruitment_funnel_data()))
    _render_funnel_section()
    _render_conversion_summary(funnel_data)
    _render_drop_off_insights(funnel_data)
    _render_department_comparison_section()
    _render_recommendations_placeholder()


if __name__ == "__main__":
    st.set_page_config(page_title="Analytics | HireFlow Analytics", layout="wide")
    render_page()
