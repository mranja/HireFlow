"""Candidate Management page for HireFlow Analytics."""

from __future__ import annotations

from html import escape
from typing import Any

import pandas as pd
import streamlit as st

from components.filters import (
    department_filter,
    experience_filter,
    search_box,
    stage_filter,
    status_filter,
)
from components.forms import candidate_form
from components.pagination import paginate_dataframe
from utils.candidates import load_candidates, save_candidate
from utils.search import filter_candidates, get_experience_bucket, search_candidates

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

STATUS_ALIASES = {
    "Hired": "Joined",
}

PROFILE_COLUMNS = [
    "Candidate ID",
    "Name",
    "Email",
    "Phone",
    "Department",
    "Position",
    "Experience",
    "Current Stage",
    "Recruiter",
    "Applied Date",
    "Status",
]

SKILL_LIBRARY = {
    "Frontend Developer": ["React", "TypeScript", "CSS", "Accessibility"],
    "Backend Developer": ["Python", "APIs", "Databases", "Cloud Services"],
    "QA Engineer": ["Automation", "Regression Testing", "Selenium", "Test Plans"],
    "Data Analyst": ["SQL", "Python", "Dashboards", "Statistics"],
    "UI Designer": ["Figma", "Design Systems", "Prototyping", "Research"],
}


def _apply_page_style() -> None:
    """Apply dashboard styling for the Candidates module."""
    st.markdown(
        """
        <style>
        .hf-page-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 1rem 1.1rem;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04);
        }
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2.5rem;
            max-width: 1440px;
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
            margin: 0.2rem 0 0.35rem;
        }
        .hf-profile-header {
            align-items: center;
            display: flex;
            gap: 1rem;
        }
        .hf-avatar {
            align-items: center;
            background: #175cd3;
            border-radius: 999px;
            color: #ffffff;
            display: flex;
            font-size: 1.35rem;
            font-weight: 700;
            height: 76px;
            justify-content: center;
            width: 76px;
        }
        .hf-profile-name {
            color: #101828;
            font-size: 1.55rem;
            font-weight: 700;
            line-height: 1.2;
            margin: 0;
        }
        .hf-profile-meta {
            color: #475467;
            font-size: 0.95rem;
            margin-top: 0.2rem;
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
        .hf-field-card {
            background: #ffffff;
            border: 1px solid #eaecf0;
            border-radius: 8px;
            min-height: 82px;
            padding: 0.85rem;
        }
        .hf-field-label {
            color: #667085;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0;
            margin-bottom: 0.25rem;
            text-transform: uppercase;
        }
        .hf-field-value {
            color: #101828;
            font-size: 0.98rem;
            font-weight: 600;
            overflow-wrap: anywhere;
        }
        .hf-tag {
            background: #f2f4f7;
            border: 1px solid #eaecf0;
            border-radius: 999px;
            color: #344054;
            display: inline-flex;
            font-size: 0.82rem;
            font-weight: 600;
            margin: 0 0.35rem 0.35rem 0;
            padding: 0.22rem 0.65rem;
        }
        .hf-stage {
            background: #ffffff;
            border: 1px solid #eaecf0;
            border-radius: 8px;
            color: #344054;
            font-weight: 700;
            padding: 0.65rem 0.8rem;
        }
        .hf-stage-current {
            background: #eff8ff;
            border-color: #84caff;
            color: #175cd3;
        }
        .hf-stage-arrow {
            color: #98a2b3;
            font-size: 1.1rem;
            line-height: 1.5;
            text-align: center;
        }
        div[data-testid="stMetric"] {
            background: #ffffff;
            border: 1px solid #eaecf0;
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
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
    """Render title and breadcrumb."""
    st.markdown(
        '<div class="hf-breadcrumb">Dashboard &gt; Candidates</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="hf-page-title">Candidate Management</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        (
            '<div class="hf-page-subtitle">'
            "Search, filter, review, and manage recruitment pipeline candidates."
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def _reset_candidate_page() -> None:
    """Reset pagination whenever search or filters change."""
    st.session_state["candidate_current_page"] = 1


def _normalise_stage(stage: Any) -> str:
    """Return the display stage used by the candidate management UI."""
    value = str(stage or "").strip()
    return STAGE_ALIASES.get(value, value)


def _normalise_status(status: Any, stage: Any = "") -> str:
    """Return the display status used by the candidate management UI."""
    value = str(status or "").strip()
    stage_value = _normalise_stage(stage)
    if stage_value == "Joined":
        return "Joined"
    return STATUS_ALIASES.get(value, value or "Active")


def _prepare_candidate_view(candidates: pd.DataFrame) -> pd.DataFrame:
    """Create a display-safe dataframe without mutating storage data."""
    prepared = candidates.copy()

    for column in PROFILE_COLUMNS:
        if column not in prepared.columns:
            prepared[column] = ""

    prepared["Current Stage"] = prepared["Current Stage"].map(_normalise_stage)
    prepared["Status"] = prepared.apply(
        lambda row: _normalise_status(row["Status"], row["Current Stage"]),
        axis=1,
    )
    prepared["Experience Band"] = prepared["Experience"].map(get_experience_bucket)
    return prepared


def _to_int(value: Any, default: int = 0) -> int:
    """Convert scalar values to int without leaking NaN into the UI."""
    numeric_value = pd.to_numeric(value, errors="coerce")
    if pd.isna(numeric_value):
        return default
    return int(numeric_value)


def _html(value: Any) -> str:
    """Escape values before rendering them inside unsafe HTML blocks."""
    return escape(str(value), quote=True)


def _render_toolbar() -> tuple[str, list[str], list[str], list[str], list[str]]:
    """Render search, filters, refresh, and add actions."""
    with st.container(border=True):
        search_col, dept_col, stage_col, exp_col, status_col = st.columns(
            [1.6, 1.1, 1.25, 1.1, 1.1]
        )

        with search_col:
            search_term = search_box(on_change=_reset_candidate_page)

        with dept_col:
            departments = department_filter(on_change=_reset_candidate_page)

        with stage_col:
            stages = stage_filter(on_change=_reset_candidate_page)

        with exp_col:
            experience_bands = experience_filter(on_change=_reset_candidate_page)

        with status_col:
            statuses = status_filter(on_change=_reset_candidate_page)

        action_left, action_right, spacer = st.columns([1.1, 1.25, 5.5])
        with action_left:
            if st.button("Refresh", width="stretch"):
                st.rerun()

        with action_right:
            if st.button("Add Candidate", type="primary", width="stretch"):
                st.session_state["show_candidate_form"] = True

    return search_term, departments, stages, experience_bands, statuses


def _render_summary_metrics(candidates: pd.DataFrame, filtered: pd.DataFrame) -> None:
    """Render quick candidate list metrics."""
    active_candidates = int((filtered["Status"] == "Active").sum())
    offer_candidates = int(filtered["Current Stage"].isin(["Offer", "Accepted"]).sum())
    joined_candidates = int((filtered["Status"] == "Joined").sum())

    metric_cols = st.columns(4)
    metric_cols[0].metric("Total Candidates", len(candidates))
    metric_cols[1].metric("Filtered Results", len(filtered))
    metric_cols[2].metric("Active Pipeline", active_candidates)
    metric_cols[3].metric("Offers / Joined", offer_candidates + joined_candidates)


def _render_add_candidate_panel() -> None:
    """Render the candidate creation workflow."""
    if not st.session_state.get("show_candidate_form", False):
        return

    with st.expander("Add Candidate", expanded=True):
        candidate = candidate_form()
        if candidate is None:
            return

        try:
            save_candidate(candidate)
        except ValueError as exc:
            st.error(str(exc))
            return

        st.session_state["candidate_success"] = (
            f"{candidate['Name']} was added to the candidate pipeline."
        )
        st.session_state["show_candidate_form"] = False
        st.rerun()


def _table_column_config() -> dict[str, Any]:
    """Return dataframe column configuration for candidate listing."""
    return {
        "Candidate ID": st.column_config.TextColumn("Candidate ID"),
        "Name": st.column_config.TextColumn("Name"),
        "Email": st.column_config.TextColumn("Email"),
        "Phone": st.column_config.TextColumn("Phone"),
        "Department": st.column_config.TextColumn("Department"),
        "Position": st.column_config.TextColumn("Position"),
        "Experience": st.column_config.NumberColumn(
            "Experience",
            help="Years of professional experience",
            format="%d yrs",
        ),
        "Current Stage": st.column_config.TextColumn("Current Stage"),
        "Recruiter": st.column_config.TextColumn("Recruiter"),
        "Applied Date": st.column_config.DateColumn("Applied Date"),
        "Status": st.column_config.TextColumn("Status"),
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


def _render_candidate_table(df: pd.DataFrame) -> None:
    """Render the paginated candidate table and store the selected candidate."""
    if df.empty:
        st.info("No candidates match the current search and filters.")
        return

    paginated_df, _ = paginate_dataframe(df)
    table_df = paginated_df[PROFILE_COLUMNS].copy()
    table_height = min(520, 68 + (len(table_df) * 38))

    selection_event = st.dataframe(
        table_df,
        hide_index=True,
        width="stretch",
        height=table_height,
        column_config=_table_column_config(),
        on_select="rerun",
        selection_mode="single-row",
        key="candidate_management_table",
    )

    selected_rows = _selection_rows(selection_event)
    if selected_rows:
        selected_candidate_id = str(
            table_df.iloc[selected_rows[0]]["Candidate ID"]
        )
        st.session_state["candidate_profile_id"] = selected_candidate_id


def _candidate_options(df: pd.DataFrame) -> dict[str, str]:
    """Return candidate selectbox labels keyed by Candidate ID."""
    labels: dict[str, str] = {}
    for _, row in df.iterrows():
        labels[str(row["Candidate ID"])] = (
            f"{row['Name']} - {row['Position']} ({row['Current Stage']})"
        )
    return labels


def _sync_selected_candidate(df: pd.DataFrame) -> str | None:
    """Keep the selected candidate ID valid for the filtered result set."""
    if df.empty:
        st.session_state.pop("candidate_profile_id", None)
        return None

    candidate_ids = [str(value) for value in df["Candidate ID"].tolist()]
    selected_id = str(st.session_state.get("candidate_profile_id", ""))
    if selected_id not in candidate_ids:
        selected_id = candidate_ids[0]
        st.session_state["candidate_profile_id"] = selected_id

    return selected_id


def _render_profile_selector(df: pd.DataFrame) -> str | None:
    """Render the candidate profile selector."""
    selected_id = _sync_selected_candidate(df)
    if selected_id is None:
        return None

    labels = _candidate_options(df)
    candidate_ids = list(labels.keys())
    selected_index = candidate_ids.index(selected_id)

    return st.selectbox(
        "Profile",
        options=candidate_ids,
        index=selected_index,
        format_func=lambda candidate_id: labels[candidate_id],
        key="candidate_profile_id",
    )


def _candidate_by_id(df: pd.DataFrame, candidate_id: str) -> pd.Series | None:
    """Return the selected candidate record."""
    matches = df[df["Candidate ID"].astype(str) == str(candidate_id)]
    if matches.empty:
        return None
    return matches.iloc[0]


def _safe_value(candidate: pd.Series, key: str, default: str = "Not provided") -> str:
    """Return a display-safe candidate value."""
    value = candidate.get(key, default)
    if pd.isna(value) or str(value).strip() == "":
        return default
    return str(value)


def _initials(name: str) -> str:
    """Return initials for the profile avatar."""
    parts = [part for part in name.split() if part]
    if not parts:
        return "HF"
    return "".join(part[0].upper() for part in parts[:2])


def _status_chip_class(status: str) -> str:
    """Return the CSS class for a status chip."""
    if status == "Active":
        return "hf-chip-green"
    if status == "On Hold":
        return "hf-chip-amber"
    if status == "Rejected":
        return "hf-chip-red"
    return "hf-chip-blue"


def _render_field_card(label: str, value: Any) -> None:
    """Render a compact label-value card."""
    st.markdown(
        f"""
        <div class="hf-field-card">
            <div class="hf-field-label">{_html(label)}</div>
            <div class="hf-field-value">{_html(value)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _candidate_skills(candidate: pd.Series) -> list[str]:
    """Return candidate skills from data or a role-based default."""
    raw_skills = _safe_value(candidate, "Skills", "")
    if raw_skills:
        return [skill.strip() for skill in raw_skills.split(",") if skill.strip()]
    return SKILL_LIBRARY.get(_safe_value(candidate, "Position", ""), ["Communication"])


def _expected_salary(candidate: pd.Series) -> str:
    """Return expected salary from data or an experience-based estimate."""
    salary = _safe_value(candidate, "Expected Salary", "")
    if salary:
        return salary

    experience = _to_int(candidate.get("Experience", 0))
    lower_bound = max(6, 5 + experience * 2)
    upper_bound = lower_bound + 4
    return f"INR {lower_bound}-{upper_bound} LPA"


def _interview_score(candidate: pd.Series) -> int:
    """Return interview score from data or a deterministic pipeline estimate."""
    score = pd.to_numeric(candidate.get("Interview Score", ""), errors="coerce")
    if not pd.isna(score):
        return int(score)

    stage = _safe_value(candidate, "Current Stage", "Applied")
    stage_index = TIMELINE_STAGES.index(stage) if stage in TIMELINE_STAGES else 0
    experience = _to_int(candidate.get("Experience", 0))
    return min(96, 68 + stage_index * 3 + min(experience, 10))


def _offers_count(candidate: pd.Series) -> int:
    """Return offer count for candidate metrics."""
    stage = _safe_value(candidate, "Current Stage", "")
    status = _safe_value(candidate, "Status", "")
    return int(stage in {"Offer", "Accepted", "Joined"} or status == "Joined")


def _render_profile_header(candidate: pd.Series) -> None:
    """Render profile picture, identity, stage, and status."""
    name = _safe_value(candidate, "Name")
    status = _safe_value(candidate, "Status", "Active")
    stage = _safe_value(candidate, "Current Stage", "Applied")
    position = _safe_value(candidate, "Position")
    department = _safe_value(candidate, "Department")

    left_col, right_col = st.columns([3.4, 1.4])
    with left_col:
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
                        <span class="hf-chip {_status_chip_class(status)}">{_html(status)}</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right_col:
        st.metric("Current Stage", stage)


def _render_candidate_metrics(candidate: pd.Series) -> None:
    """Render candidate-level metric cards."""
    metric_cols = st.columns(5)
    metric_cols[0].metric("Experience", f"{candidate['Experience']} yrs")
    metric_cols[1].metric("Interview Score", f"{_interview_score(candidate)}%")
    metric_cols[2].metric("Applications", "1")
    metric_cols[3].metric("Offers", str(_offers_count(candidate)))
    metric_cols[4].metric("Status", _safe_value(candidate, "Status", "Active"))


def _render_overview_tab(candidate: pd.Series) -> None:
    """Render candidate overview details."""
    _render_candidate_metrics(candidate)
    st.write("")

    row_one = st.columns(4)
    details = [
        ("Department", _safe_value(candidate, "Department")),
        ("Position", _safe_value(candidate, "Position")),
        ("Experience", f"{candidate['Experience']} Years"),
        ("Recruiter", _safe_value(candidate, "Recruiter")),
    ]
    for column, (label, value) in zip(row_one, details, strict=True):
        with column:
            _render_field_card(label, value)

    row_two = st.columns(4)
    contact_details = [
        ("Applied Date", _safe_value(candidate, "Applied Date")),
        ("Expected Salary", _expected_salary(candidate)),
        ("Email", _safe_value(candidate, "Email")),
        ("Phone", _safe_value(candidate, "Phone")),
    ]
    for column, (label, value) in zip(row_two, contact_details, strict=True):
        with column:
            _render_field_card(label, value)

    st.write("")
    _render_field_card("Address", _safe_value(candidate, "Address"))

    st.write("")
    with st.expander("Skills", expanded=True):
        tags = "".join(
            f'<span class="hf-tag">{_html(skill)}</span>'
            for skill in _candidate_skills(candidate)
        )
        st.markdown(tags, unsafe_allow_html=True)

    education_col, certification_col = st.columns(2)
    with education_col:
        with st.expander("Education", expanded=True):
            st.write(
                _safe_value(
                    candidate,
                    "Education",
                    "Bachelor's degree or equivalent professional experience",
                )
            )

    with certification_col:
        with st.expander("Certifications", expanded=True):
            st.write(_safe_value(candidate, "Certifications", "No certifications recorded"))


def _render_interview_history_tab(candidate: pd.Series) -> None:
    """Render interview history and feedback details."""
    stage = _safe_value(candidate, "Current Stage", "Applied")
    recruiter = _safe_value(candidate, "Recruiter", "Recruiting Team")
    score = _interview_score(candidate)

    history = [
        ("Screening", "Completed" if stage in TIMELINE_STAGES[1:] else "Pending"),
        (
            "Assessment",
            "Completed" if stage in TIMELINE_STAGES[2:] else "Pending",
        ),
        (
            "Technical Interview",
            "Completed" if stage in TIMELINE_STAGES[3:] else "Pending",
        ),
        ("HR Interview", "Completed" if stage in TIMELINE_STAGES[4:] else "Pending"),
    ]

    for round_name, result in history:
        with st.container(border=True):
            cols = st.columns([1.4, 1, 1, 2.2])
            cols[0].markdown(f"**{round_name}**")
            cols[1].write(result)
            cols[2].write(f"{score}%" if result == "Completed" else "-")
            cols[3].write(f"Owner: {recruiter}")

    with st.expander("Feedback", expanded=True):
        feedback = _safe_value(
            candidate,
            "Feedback",
            (
                "Candidate profile is aligned with the current role requirements. "
                "Next action should be based on the active recruitment stage."
            ),
        )
        st.write(feedback)


def _render_documents_tab(candidate: pd.Series) -> None:
    """Render resume and document controls."""
    resume_name = f"{_safe_value(candidate, 'Candidate ID')}_resume.txt"
    resume_uploaded = "Yes" if _safe_value(candidate, "Resume", "") else "Profile Summary"
    resume_text = "\n".join(
        [
            f"Candidate: {_safe_value(candidate, 'Name')}",
            f"Email: {_safe_value(candidate, 'Email')}",
            f"Phone: {_safe_value(candidate, 'Phone')}",
            f"Position: {_safe_value(candidate, 'Position')}",
            f"Department: {_safe_value(candidate, 'Department')}",
            f"Experience: {_safe_value(candidate, 'Experience')} years",
            f"Skills: {', '.join(_candidate_skills(candidate))}",
        ]
    )

    doc_cols = st.columns(3)
    with doc_cols[0]:
        st.metric("Resume Uploaded", resume_uploaded)
    with doc_cols[1]:
        st.metric("Documents", "1")
    with doc_cols[2]:
        st.metric("Last Updated", _safe_value(candidate, "Applied Date"))

    st.download_button(
        "Download Resume",
        data=resume_text,
        file_name=resume_name,
        mime="text/plain",
        width="stretch",
    )


def _render_timeline_tab(candidate: pd.Series) -> None:
    """Render interview timeline with current stage highlighted."""
    current_stage = _safe_value(candidate, "Current Stage", "Applied")

    for index, stage in enumerate(TIMELINE_STAGES):
        stage_class = "hf-stage hf-stage-current" if stage == current_stage else "hf-stage"
        st.markdown(
            f'<div class="{stage_class}">{_html(stage)}</div>',
            unsafe_allow_html=True,
        )
        if index < len(TIMELINE_STAGES) - 1:
            st.markdown(
                '<div class="hf-stage-arrow">&darr;</div>',
                unsafe_allow_html=True,
            )


def _render_candidate_details(candidate: pd.Series) -> None:
    """Render the full candidate details dashboard."""
    with st.container(border=True):
        _render_profile_header(candidate)
        st.write("")

        overview_tab, interview_tab, documents_tab, timeline_tab = st.tabs(
            ["Overview", "Interview History", "Documents", "Timeline"]
        )

        with overview_tab:
            _render_overview_tab(candidate)

        with interview_tab:
            _render_interview_history_tab(candidate)

        with documents_tab:
            _render_documents_tab(candidate)

        with timeline_tab:
            _render_timeline_tab(candidate)


def render_page() -> None:
    """Render the complete Candidate Management module."""
    _apply_page_style()
    _render_header()

    success_message = st.session_state.pop("candidate_success", None)
    if success_message:
        st.success(success_message)

    candidates = _prepare_candidate_view(load_candidates())
    search_term, departments, stages, experience_bands, statuses = _render_toolbar()

    searched_candidates = search_candidates(candidates, search_term)
    filtered_candidates = filter_candidates(
        searched_candidates,
        departments=departments,
        stages=stages,
        experience_bands=experience_bands,
        statuses=statuses,
    )

    st.write("")
    _render_add_candidate_panel()

    st.write("")
    _render_summary_metrics(candidates, filtered_candidates)

    st.write("")
    st.markdown(
        '<div class="hf-section-title">Candidate List</div>',
        unsafe_allow_html=True,
    )
    _render_candidate_table(filtered_candidates)

    st.write("")
    st.markdown(
        '<div class="hf-section-title">Candidate Details</div>',
        unsafe_allow_html=True,
    )
    selected_candidate_id = _render_profile_selector(filtered_candidates)
    if selected_candidate_id is None:
        return

    selected_candidate = _candidate_by_id(filtered_candidates, selected_candidate_id)
    if selected_candidate is not None:
        _render_candidate_details(selected_candidate)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Candidates | HireFlow Analytics",
        layout="wide",
    )
    render_page()
