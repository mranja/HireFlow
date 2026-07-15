"""Interview feedback module frontend for HireFlow Analytics."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import date, datetime
from hashlib import sha1
from html import escape
from typing import Any

import pandas as pd
import streamlit as st

from components.filters import DEPARTMENT_OPTIONS

INTERVIEW_ROUNDS = [
    "Screening",
    "Assessment",
    "Technical Interview",
    "HR Interview",
    "Final Interview",
]

INTERVIEW_STATUS_OPTIONS = [
    "Scheduled",
    "In Progress",
    "Completed",
    "Pending Feedback",
    "Cancelled",
    "Pass",
    "Hold",
    "Reject",
]

TIMELINE_STAGES = [
    "Applied",
    "Screening",
    "Assessment",
    "Technical Interview",
    "HR Interview",
    "Offer",
    "Accepted",
    "Joined",
]

STAGE_ALIASES = {
    "Technical": "Technical Interview",
    "HR": "HR Interview",
}

INTERVIEW_TABLE_COLUMNS = [
    "Candidate Name",
    "Position",
    "Department",
    "Interview Round",
    "Interview Date",
    "Interviewer",
    "Status",
    "Overall Rating",
]

INTERVIEW_DATA_COLUMNS = [
    "Interview ID",
    "Candidate ID",
    *INTERVIEW_TABLE_COLUMNS,
    "Recruiter",
    "Current Stage",
    "Applied Date",
    "Email",
    "Phone",
    "Address",
    "Skills",
    "Education",
    "Certifications",
    "Expected Salary",
    "Resume Status",
]

CANDIDATE_FORM_FIELDS = [
    "Candidate Name",
    "Position",
    "Department",
    "Recruiter",
    "Current Stage",
]

CANDIDATE_DETAIL_FIELDS = [
    "Department",
    "Position",
    "Current Stage",
    "Recruiter",
    "Applied Date",
    "Email",
    "Phone",
    "Address",
    "Skills",
    "Education",
    "Certifications",
    "Expected Salary",
    "Resume Status",
]

RATING_FIELDS = [
    "Technical Skills",
    "Communication",
    "Problem Solving",
    "Culture Fit",
    "Confidence",
    "Overall Recommendation",
]

FEEDBACK_TEXT_FIELDS = [
    "Strengths",
    "Weaknesses",
    "General Comments",
]


def _apply_page_style() -> None:
    """Apply module-level styling that matches the HireFlow dashboard."""
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
            margin-bottom: 0.2rem;
        }
        .hf-page-title {
            color: #101828;
            font-size: 2.1rem;
            font-weight: 700;
            letter-spacing: 0;
            line-height: 1.2;
            margin-bottom: 0.2rem;
        }
        .hf-page-subtitle {
            color: #475467;
            font-size: 1rem;
            margin-bottom: 1rem;
        }
        .hf-section-title {
            color: #101828;
            font-size: 1.05rem;
            font-weight: 700;
            margin: 0.2rem 0 0.45rem;
        }
        .hf-empty-state {
            background: #f9fafb;
            border: 1px dashed #d0d5dd;
            border-radius: 8px;
            color: #475467;
            padding: 1rem;
        }
        .hf-profile-header {
            align-items: center;
            display: flex;
            gap: 1rem;
            margin-bottom: 1rem;
        }
        .hf-avatar {
            align-items: center;
            background: #175cd3;
            border-radius: 999px;
            color: #ffffff;
            display: flex;
            flex: 0 0 auto;
            font-size: 1.35rem;
            font-weight: 700;
            height: 76px;
            justify-content: center;
            width: 76px;
        }
        .hf-profile-name {
            color: #101828;
            font-size: 1.35rem;
            font-weight: 700;
            line-height: 1.25;
            margin: 0;
            overflow-wrap: anywhere;
        }
        .hf-profile-meta {
            color: #475467;
            font-size: 0.95rem;
            margin-top: 0.25rem;
            overflow-wrap: anywhere;
        }
        .hf-chip-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 0.55rem;
        }
        .hf-chip {
            border-radius: 999px;
            display: inline-flex;
            font-size: 0.8rem;
            font-weight: 700;
            padding: 0.22rem 0.65rem;
        }
        .hf-chip-blue {
            background: #eff8ff;
            color: #175cd3;
        }
        .hf-chip-green {
            background: #ecfdf3;
            color: #067647;
        }
        .hf-chip-amber {
            background: #fffaeb;
            color: #b54708;
        }
        .hf-chip-red {
            background: #fef3f2;
            color: #b42318;
        }
        .hf-detail-group {
            border-bottom: 1px solid #eaecf0;
            min-height: 64px;
            padding: 0.55rem 0;
        }
        .hf-detail-label {
            color: #667085;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0;
            margin-bottom: 0.2rem;
            text-transform: uppercase;
        }
        .hf-detail-value {
            color: #101828;
            font-size: 0.96rem;
            font-weight: 600;
            overflow-wrap: anywhere;
        }
        .hf-timeline-item {
            align-items: center;
            background: #ffffff;
            border: 1px solid #eaecf0;
            border-radius: 8px;
            color: #344054;
            display: flex;
            font-weight: 700;
            min-height: 44px;
            padding: 0.65rem 0.8rem;
        }
        .hf-timeline-current {
            background: #eff8ff;
            border-color: #84caff;
            color: #175cd3;
        }
        .hf-timeline-arrow {
            color: #98a2b3;
            font-size: 1.1rem;
            line-height: 1.4;
            text-align: center;
        }
        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #eaecf0;
            border-radius: 8px;
            box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
            padding: 1rem;
        }
        div[data-testid="stForm"] {
            border: 1px solid #d0d5dd;
            border-radius: 8px;
            padding: 1.25rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_header() -> None:
    """Render the page heading."""
    st.markdown(
        '<div class="hf-breadcrumb">Dashboard &gt; Interviews</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="hf-page-title">Interview Feedback</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        (
            '<div class="hf-page-subtitle">'
            "Review interview schedules, capture structured feedback, "
            "and track candidate progress through the hiring process."
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def _empty_interview_dataframe() -> pd.DataFrame:
    """Return an empty, schema-ready dataframe for backend integration."""
    return pd.DataFrame(columns=INTERVIEW_DATA_COLUMNS)


def _records_to_dataframe(
    records: pd.DataFrame | Sequence[Mapping[str, Any]] | None,
    
) -> pd.DataFrame:
    """Normalize backend-provided records into the interview UI schema."""
    if records is None:
        return _empty_interview_dataframe()

    if isinstance(records, pd.DataFrame):
        dataframe = records.copy()
    else:
        dataframe = pd.DataFrame(records)

    for column in INTERVIEW_DATA_COLUMNS:
        if column not in dataframe.columns:
            dataframe[column] = ""

    return dataframe[INTERVIEW_DATA_COLUMNS].copy()


def _summary_defaults() -> dict[str, Any]:
    """Return empty-state KPI values."""
    return {
        "Upcoming Interviews": 0,
        "Completed Interviews": 0,
        "Pending Feedback": 0,
        "Average Rating": "N/A",
    }


def _summary_from_interviews(interviews: pd.DataFrame) -> dict[str, Any]:
    """Calculate frontend KPI values from provided interview rows."""
    if interviews.empty:
        return _summary_defaults()

    status_series = interviews["Status"].astype("string").fillna("")
    ratings = pd.to_numeric(interviews["Overall Rating"], errors="coerce").dropna()

    summary = _summary_defaults()
    summary["Upcoming Interviews"] = int(
        status_series.str.lower().isin(["scheduled", "in progress"]).sum()
    )
    summary["Completed Interviews"] = int(
        status_series.str.lower().eq("completed").sum()
    )
    summary["Pending Feedback"] = int(
        status_series.str.lower().eq("pending feedback").sum()
    )
    if not ratings.empty:
        summary["Average Rating"] = f"{ratings.mean():.1f}/5"

    return summary


def _render_summary_cards(
    interviews: pd.DataFrame,
    summary_metrics: Mapping[str, Any] | None = None,
) -> None:
    """Render interview KPI cards."""
    summary = _summary_from_interviews(interviews)
    if summary_metrics:
        summary.update(
            {
                key: summary_metrics.get(key, value)
                for key, value in summary.items()
            }
        )

    metric_cols = st.columns(4)
    metric_cols[0].metric(
        "Upcoming Interviews",
        str(summary["Upcoming Interviews"]),
    )
    metric_cols[1].metric(
        "Completed Interviews",
        str(summary["Completed Interviews"]),
    )
    metric_cols[2].metric(
        "Pending Feedback",
        str(summary["Pending Feedback"]),
    )
    metric_cols[3].metric("Average Rating", str(summary["Average Rating"]))


def _clear_selected_interview() -> None:
    """Clear the selected interview when list filters change."""
    st.session_state.pop("interview_selected_record", None)
    st.session_state.pop("interview_active_record_key", None)


def _option_values(
    dataframe: pd.DataFrame,
    column: str,
    fallback_options: Sequence[str],
) -> list[str]:
    """Build filter options from configured values and backend data."""
    configured_values = [str(value) for value in fallback_options]
    if column not in dataframe.columns or dataframe.empty:
        return configured_values

    data_values = [
        str(value).strip()
        for value in dataframe[column].dropna().tolist()
        if str(value).strip()
    ]
    return list(dict.fromkeys([*configured_values, *sorted(set(data_values))]))


def _render_toolbar(
    interviews: pd.DataFrame,
) -> tuple[str, list[str], list[str], list[str]]:
    """Render interview search, filters, and refresh control."""
    with st.container(border=True):
        search_col, dept_col, round_col, status_col, refresh_col = st.columns(
            [1.55, 1.15, 1.15, 1.15, 0.8]
        )

        with search_col:
            search_term = st.text_input(
                "Search Interview",
                placeholder="Search candidate, position, or interviewer",
                key="interview_search",
                on_change=_clear_selected_interview,
            )

        with dept_col:
            departments = st.multiselect(
                "Department Filter",
                options=_option_values(
                    interviews,
                    "Department",
                    DEPARTMENT_OPTIONS,
                ),
                placeholder="All departments",
                key="interview_department_filter",
                on_change=_clear_selected_interview,
            )

        with round_col:
            rounds = st.multiselect(
                "Round Filter",
                options=_option_values(
                    interviews,
                    "Interview Round",
                    INTERVIEW_ROUNDS,
                ),
                placeholder="All rounds",
                key="interview_round_filter",
                on_change=_clear_selected_interview,
            )

        with status_col:
            statuses = st.multiselect(
                "Status Filter",
                options=_option_values(
                    interviews,
                    "Status",
                    INTERVIEW_STATUS_OPTIONS,
                ),
                placeholder="All statuses",
                key="interview_status_filter",
                on_change=_clear_selected_interview,
            )

        with refresh_col:
            st.write("")
            if st.button("Refresh", width="stretch"):
                st.rerun()

    return search_term, departments, rounds, statuses


def _filter_interviews(
    interviews: pd.DataFrame,
    search_term: str,
    departments: Sequence[str],
    rounds: Sequence[str],
    statuses: Sequence[str],
) -> pd.DataFrame:
    """Apply list-view search and filters to interview records."""
    filtered = interviews.copy()

    if search_term.strip():
        search_text = search_term.strip()
        searchable_columns = [
            "Candidate Name",
            "Position",
            "Department",
            "Interviewer",
        ]
        mask = pd.Series(False, index=filtered.index)
        for column in searchable_columns:
            mask = mask | (
                filtered[column]
                .astype("string")
                .fillna("")
                .str.contains(search_text, case=False, regex=False)
            )
        filtered = filtered.loc[mask]

    if departments:
        filtered = filtered[filtered["Department"].isin(departments)]
    if rounds:
        filtered = filtered[filtered["Interview Round"].isin(rounds)]
    if statuses:
        filtered = filtered[filtered["Status"].isin(statuses)]

    return filtered.copy()


def _table_column_config() -> dict[str, Any]:
    """Return column configuration for the interview list."""
    return {
        "Candidate Name": st.column_config.TextColumn("Candidate Name"),
        "Position": st.column_config.TextColumn("Position"),
        "Department": st.column_config.TextColumn("Department"),
        "Interview Round": st.column_config.TextColumn("Interview Round"),
        "Interview Date": st.column_config.DateColumn("Interview Date"),
        "Interviewer": st.column_config.TextColumn("Interviewer"),
        "Status": st.column_config.TextColumn("Status"),
        "Overall Rating": st.column_config.NumberColumn(
            "Overall Rating",
            help="Rating on a 5-point scale",
            min_value=0,
            max_value=5,
            format="%.1f",
        ),
    }


def _selection_rows(selection_event: Any) -> list[int]:
    """Extract selected dataframe row positions across Streamlit versions."""
    if selection_event is None:
        return []

    selection = getattr(selection_event, "selection", None)
    if selection is None and isinstance(selection_event, dict):
        selection = selection_event.get("selection")

    if selection is None:
        return []

    rows = getattr(selection, "rows", None)
    if rows is None and isinstance(selection, dict):
        rows = selection.get("rows")

    return list(rows or [])


def _record_key(record: Mapping[str, Any]) -> str:
    """Build a stable key for selected interview state."""
    key_parts = [
        _safe_value(record, "Interview ID", ""),
        _safe_value(record, "Candidate ID", ""),
        _safe_value(record, "Candidate Name", ""),
        _safe_value(record, "Interview Date", ""),
        _safe_value(record, "Interview Round", ""),
    ]
    return "|".join(key_parts)


def _matching_session_record(
    interviews: pd.DataFrame,
) -> dict[str, Any] | None:
    """Return the stored selection if it still exists in the active table."""
    stored_record = st.session_state.get("interview_selected_record")
    if not isinstance(stored_record, dict) or interviews.empty:
        return None

    stored_key = _record_key(stored_record)
    for _, row in interviews.iterrows():
        row_record = row.to_dict()
        if _record_key(row_record) == stored_key:
            return row_record

    _clear_selected_interview()
    return None


def _render_interview_table(interviews: pd.DataFrame) -> dict[str, Any] | None:
    """Render the interview list and return the selected record."""
    table_df = interviews[INTERVIEW_TABLE_COLUMNS].copy()
    table_height = 168 if table_df.empty else min(520, 72 + (len(table_df) * 38))

    selection_event = st.dataframe(
        table_df,
        hide_index=True,
        width="stretch",
        height=table_height,
        column_config=_table_column_config(),
        on_select="rerun",
        selection_mode="single-row",
        key="interview_management_table",
    )

    if table_df.empty:
        st.info("No interview records available.")
        return None

    selected_rows = _selection_rows(selection_event)
    if selected_rows:
        selected_record = interviews.iloc[selected_rows[0]].to_dict()
        st.session_state["interview_selected_record"] = selected_record
        return selected_record

    return _matching_session_record(interviews)


def _safe_value(
    record: Mapping[str, Any] | None,
    field_name: str,
    default: str = "Not provided",
) -> str:
    """Return a display-safe record value."""
    if record is None:
        return default

    value = record.get(field_name, default)
    if isinstance(value, (list, tuple, set)):
        joined_value = ", ".join(str(item) for item in value if str(item).strip())
        return joined_value or default

    try:
        if pd.isna(value):
            return default
    except (TypeError, ValueError):
        pass

    text_value = str(value).strip()
    return text_value or default


def _html(value: Any) -> str:
    """Escape values before rendering them as HTML."""
    return escape(str(value), quote=True)


def _normalise_stage(stage: Any) -> str:
    """Return the timeline stage name used by the UI."""
    stage_value = str(stage or "").strip()
    return STAGE_ALIASES.get(stage_value, stage_value)


def _initials(name: str) -> str:
    """Return initials for the profile placeholder."""
    parts = [part for part in name.split() if part]
    if not parts:
        return "HF"
    return "".join(part[0].upper() for part in parts[:2])


def _status_chip_class(status: str) -> str:
    """Return the status chip style."""
    normalized_status = status.lower()
    if normalized_status in {"completed", "pass"}:
        return "hf-chip-green"
    if normalized_status in {"pending feedback", "hold", "in progress"}:
        return "hf-chip-amber"
    if normalized_status in {"reject", "cancelled"}:
        return "hf-chip-red"
    return "hf-chip-blue"


def _parse_date(value: Any) -> date:
    """Parse a backend date value for Streamlit date_input."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value

    parsed = pd.to_datetime(value, errors="coerce")
    if pd.isna(parsed):
        return date.today()
    return parsed.date()


def _feedback_key(field_name: str) -> str:
    """Build a stable feedback form widget key."""
    return f"interview_feedback_{field_name}"


def _reset_feedback_form() -> None:
    """Clear feedback form widgets."""
    field_names = [
        "round",
        "date",
        "interviewer",
        "decision",
        *[field.lower().replace(" ", "_") for field in RATING_FIELDS],
        *[field.lower().replace(" ", "_") for field in FEEDBACK_TEXT_FIELDS],
    ]
    for field_name in field_names:
        st.session_state.pop(_feedback_key(field_name), None)


def _sync_feedback_form(record: Mapping[str, Any] | None) -> None:
    """Reset feedback draft values when the selected interview changes."""
    if record is None:
        return

    current_key = _record_key(record)
    if st.session_state.get("interview_active_record_key") != current_key:
        _reset_feedback_form()
        st.session_state["interview_active_record_key"] = current_key


def _render_section_title(title: str) -> None:
    """Render a section title."""
    st.markdown(
        f'<div class="hf-section-title">{_html(title)}</div>',
        unsafe_allow_html=True,
    )


def _render_empty_state(message: str) -> None:
    """Render a professional empty-state block."""
    st.markdown(
        f'<div class="hf-empty-state">{_html(message)}</div>',
        unsafe_allow_html=True,
    )


def _render_read_only_candidate_info(record: Mapping[str, Any]) -> None:
    """Render read-only candidate fields inside the feedback form."""
    first_row = st.columns(3)
    second_row = st.columns(2)
    field_columns = [*first_row, *second_row]
    record_suffix = sha1(_record_key(record).encode("utf-8")).hexdigest()[:12]

    for column, field_name in zip(field_columns, CANDIDATE_FORM_FIELDS, strict=True):
        with column:
            st.text_input(
                field_name,
                value=_safe_value(record, field_name),
                disabled=True,
                key=(
                    f"readonly_{field_name.lower().replace(' ', '_')}_"
                    f"{record_suffix}"
                ),
            )


def _round_index(record: Mapping[str, Any]) -> int | None:
    """Return the selected interview round index, if known."""
    current_round = _safe_value(record, "Interview Round", "")
    if current_round in INTERVIEW_ROUNDS:
        return INTERVIEW_ROUNDS.index(current_round)
    return None


def _render_feedback_form(record: Mapping[str, Any] | None) -> None:
    """Render the interview feedback form."""
    if record is None:
        _render_empty_state("No candidate selected.")
        st.caption("Select an interview record to open the feedback form.")
        return

    _sync_feedback_form(record)

    with st.form("interview_feedback_form", clear_on_submit=False):
        st.subheader("Candidate Information")
        _render_read_only_candidate_info(record)

        st.subheader("Interview Information")
        interview_cols = st.columns(3)
        with interview_cols[0]:
            st.selectbox(
                "Interview Round",
                options=INTERVIEW_ROUNDS,
                index=_round_index(record),
                placeholder="Select round",
                key=_feedback_key("round"),
            )
        with interview_cols[1]:
            st.date_input(
                "Interview Date",
                value=_parse_date(_safe_value(record, "Interview Date", "")),
                key=_feedback_key("date"),
            )
        with interview_cols[2]:
            st.text_input(
                "Interviewer Name",
                value=_safe_value(record, "Interviewer", ""),
                placeholder="Enter interviewer name",
                key=_feedback_key("interviewer"),
            )

        st.subheader("Ratings")
        rating_columns = st.columns(3)
        for index, rating_field in enumerate(RATING_FIELDS):
            with rating_columns[index % 3]:
                st.slider(
                    rating_field,
                    min_value=0,
                    max_value=5,
                    value=0,
                    help="Use 0 when this rating has not been captured yet.",
                    key=_feedback_key(rating_field.lower().replace(" ", "_")),
                )

        st.subheader("Feedback")
        feedback_columns = st.columns(3)
        for column, field_name in zip(
            feedback_columns,
            FEEDBACK_TEXT_FIELDS,
            strict=True,
        ):
            with column:
                st.text_area(
                    field_name,
                    placeholder=f"Enter {field_name.lower()}",
                    height=140,
                    key=_feedback_key(field_name.lower().replace(" ", "_")),
                )

        decision = st.radio(
            "Decision",
            options=["Pass", "Hold", "Reject"],
            horizontal=True,
            index=None,
            key=_feedback_key("decision"),
        )

        submit_col, reset_col, spacer_col = st.columns([1.1, 1.1, 4.8])
        with submit_col:
            save_clicked = st.form_submit_button(
                "Save Feedback",
                type="primary",
                width="stretch",
            )
        with reset_col:
            reset_clicked = st.form_submit_button(
                "Reset Form",
                width="stretch",
            )
        with spacer_col:
            st.write("")

    if reset_clicked:
        _reset_feedback_form()
        st.rerun()

    if save_clicked and not decision:
        st.warning("Select a decision before saving feedback.")
    elif save_clicked:
        st.info(
            "Feedback capture is ready for backend integration; "
            "no interview data has been persisted."
        )


def _render_profile_header(record: Mapping[str, Any]) -> None:
    """Render the candidate identity block."""
    name = _safe_value(record, "Candidate Name")
    position = _safe_value(record, "Position")
    department = _safe_value(record, "Department")
    status = _safe_value(record, "Status", "Waiting for interview data")
    stage = _safe_value(record, "Current Stage", "Not provided")

    st.markdown(
        f"""
        <div class="hf-profile-header">
            <div class="hf-avatar">{_html(_initials(name))}</div>
            <div>
                <p class="hf-profile-name">{_html(name)}</p>
                <div class="hf-profile-meta">
                    {_html(position)} &middot; {_html(department)}
                </div>
                <div class="hf-chip-row">
                    <span class="hf-chip hf-chip-blue">{_html(stage)}</span>
                    <span class="hf-chip {_status_chip_class(status)}">
                        {_html(status)}
                    </span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_detail_group(label: str, value: Any) -> None:
    """Render a label-value detail row."""
    st.markdown(
        f"""
        <div class="hf-detail-group">
            <div class="hf-detail-label">{_html(label)}</div>
            <div class="hf-detail-value">{_html(value)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_candidate_details_panel(record: Mapping[str, Any] | None) -> None:
    """Render the selected candidate details panel."""
    with st.container(border=True):
        _render_section_title("Candidate Details")
        if record is None:
            _render_empty_state("No candidate selected.")
            st.caption("Candidate details will appear here.")
            return

        _render_profile_header(record)

        detail_columns = st.columns(2)
        for index, field_name in enumerate(CANDIDATE_DETAIL_FIELDS):
            with detail_columns[index % 2]:
                _render_detail_group(field_name, _safe_value(record, field_name))

        st.write("")
        st.button(
            "Download Resume",
            disabled=True,
            width="stretch",
            help="Resume download will be enabled when backend storage is connected.",
        )


def _render_timeline(record: Mapping[str, Any] | None) -> None:
    """Render the interview timeline with current stage highlighted."""
    with st.container(border=True):
        _render_section_title("Interview Timeline")
        if record is None:
            _render_empty_state("No candidate selected.")
            st.caption("Interview feedback will appear here.")
            return

        current_stage = _normalise_stage(_safe_value(record, "Current Stage", ""))

        for index, stage in enumerate(TIMELINE_STAGES):
            stage_class = "hf-timeline-item"
            if stage == current_stage:
                stage_class = f"{stage_class} hf-timeline-current"

            st.markdown(
                f'<div class="{stage_class}">{_html(stage)}</div>',
                unsafe_allow_html=True,
            )
            if index < len(TIMELINE_STAGES) - 1:
                st.markdown(
                    '<div class="hf-timeline-arrow">&darr;</div>',
                    unsafe_allow_html=True,
                )


def _render_selected_interview_summary(record: Mapping[str, Any] | None) -> None:
    """Render selected interview context above the form tabs."""
    if record is None:
        st.info("Waiting for interview data.")
        return

    cols = st.columns(4)
    cols[0].metric("Round", _safe_value(record, "Interview Round", "Not set"))
    cols[1].metric("Interviewer", _safe_value(record, "Interviewer", "Not set"))
    cols[2].metric("Status", _safe_value(record, "Status", "Not set"))
    cols[3].metric(
        "Overall Rating",
        _safe_value(record, "Overall Rating", "N/A"),
    )


def render_page(
    interview_records: pd.DataFrame | Sequence[Mapping[str, Any]] | None = None,
    summary_metrics: Mapping[str, Any] | None = None,
) -> None:
    """Render the complete Interview Feedback frontend module."""
    st.set_page_config(
        page_title="Interviews | HireFlow Analytics",
        layout="wide",
    )
    _apply_page_style()
    _render_header()

    interviews = _records_to_dataframe(interview_records)
    _render_summary_cards(interviews, summary_metrics)

    st.write("")
    _render_section_title("Interview List")
    search_term, departments, rounds, statuses = _render_toolbar(interviews)
    filtered_interviews = _filter_interviews(
        interviews,
        search_term,
        departments,
        rounds,
        statuses,
    )
    selected_interview = _render_interview_table(filtered_interviews)

    st.write("")
    _render_selected_interview_summary(selected_interview)

    st.write("")
    feedback_tab, details_tab, timeline_tab = st.tabs(
        ["Feedback Form", "Candidate Details", "Timeline"]
    )

    with feedback_tab:
        _render_feedback_form(selected_interview)

    with details_tab:
        _render_candidate_details_panel(selected_interview)

    with timeline_tab:
        _render_timeline(selected_interview)


render_page()
