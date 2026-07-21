"""Reusable Streamlit components for the recruitment pipeline UI."""

from __future__ import annotations

from typing import Mapping

import streamlit as st

PIPELINE_STAGES = [
    "Applied",
    "Screening",
    "Assessment",
    "Technical Interview",
    "HR Interview",
    "Offer",
    "Accepted",
    "Joined",
]

INTERVIEW_STAGE_ROUNDS = {
    "Assessment": "Assessment Round",
    "Technical Interview": "Technical Interview Round",
    "HR Interview": "HR Interview Round",
}

STAGE_ICONS = {
    "completed": "✓",
    "current": "●",
    "upcoming": "○",
}


def render_pipeline_style() -> None:
    """Render shared CSS styling for the recruitment pipeline UI."""
    st.markdown(
        """
        <style>
        .hf-page-banner {
            border-radius: 12px;
            border: 1px solid #d1d5db;
            background: #f8fafc;
            color: #0f172a;
            padding: 1rem 1.15rem;
            margin-bottom: 1.5rem;
        }
        .hf-pipeline-grid {
            align-items: flex-start;
            display: flex;
            gap: 1rem;
            overflow-x: auto;
            padding-bottom: 0.75rem;
            width: 100%;
        }
        .hf-pipeline-stage {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            min-width: 210px;
            padding: 1rem;
            position: relative;
            flex: 0 0 auto;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.06);
        }
        .hf-pipeline-stage--completed {
            border-color: #d1fae5;
            background: #ecfdf5;
        }
        .hf-pipeline-stage--current {
            border-color: #bfdbfe;
            background: #eff6ff;
        }
        .hf-pipeline-stage--upcoming {
            border-color: #e2e8f0;
            background: #ffffff;
        }
        .hf-stage-badge {
            align-items: center;
            border-radius: 999px;
            display: inline-flex;
            font-size: 0.82rem;
            font-weight: 700;
            gap: 0.45rem;
            margin-bottom: 0.75rem;
            padding: 0.35rem 0.75rem;
        }
        .hf-stage-badge--completed {
            background: #dcfce7;
            color: #166534;
        }
        .hf-stage-badge--current {
            background: #dbeafe;
            color: #1d4ed8;
        }
        .hf-stage-badge--upcoming {
            background: #f1f5f9;
            color: #475569;
        }
        .hf-stage-title {
            color: #0f172a;
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 0.45rem;
        }
        .hf-stage-meta {
            color: #475569;
            font-size: 0.87rem;
            line-height: 1.5;
            margin-bottom: 0.25rem;
        }
        .hf-pipeline-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 20px;
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
            padding: 1.25rem;
        }
        .hf-pipeline-avatar {
            align-items: center;
            background: #c7d2fe;
            border-radius: 999px;
            color: #1e3a8a;
            display: flex;
            font-size: 1.5rem;
            font-weight: 700;
            height: 88px;
            justify-content: center;
            margin-right: 1rem;
            width: 88px;
        }
        .hf-pipeline-title {
            color: #0f172a;
            font-size: 1.4rem;
            font-weight: 700;
            margin: 0;
        }
        .hf-pipeline-subtitle {
            color: #475569;
            font-size: 0.95rem;
            margin: 0.25rem 0 0;
        }
        .hf-pipeline-label {
            color: #64748b;
            display: block;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            margin-bottom: 0.35rem;
            text-transform: uppercase;
        }
        .hf-pipeline-value {
            color: #0f172a;
            font-size: 0.96rem;
            font-weight: 600;
            margin-bottom: 0.85rem;
        }
        .hf-pipeline-metric-caption {
            color: #64748b;
            font-size: 0.92rem;
            margin-top: 0.35rem;
        }
        .hf-pipeline-empty-state {
            border: 1px dashed #cbd5e1;
            border-radius: 16px;
            background: #f8fafc;
            color: #334155;
            padding: 1.2rem;
        }
        .hf-detail-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 1.1rem;
        }
        .hf-detail-label {
            color: #475569;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            text-transform: uppercase;
            margin-bottom: 0.35rem;
        }
        .hf-detail-value {
            color: #0f172a;
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 0.9rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _sanitize_stage(stage: str) -> str:
    return stage


def _stage_status(stage: str, current_stage: str | None) -> str:
    if current_stage is None or current_stage not in PIPELINE_STAGES:
        return "upcoming"

    current_index = PIPELINE_STAGES.index(current_stage)
    stage_index = PIPELINE_STAGES.index(stage)
    if stage_index < current_index:
        return "completed"
    if stage_index == current_index:
        return "current"
    return "upcoming"


def _progress_for_stage(current_stage: str | None) -> int:
    if current_stage is None or current_stage not in PIPELINE_STAGES:
        return 0

    stage_index = PIPELINE_STAGES.index(current_stage)
    return int((stage_index + 1) / len(PIPELINE_STAGES) * 100)


def render_candidate_summary(candidate: Mapping[str, str] | None = None) -> None:
    """Render the candidate summary card with placeholders if no data is available."""
    if candidate is None:
        st.markdown(
            """
            <div class="hf-pipeline-card">
                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                    <div class="hf-pipeline-avatar">?</div>
                    <div style="flex: 1; min-width: 220px;">
                        <div class="hf-pipeline-title">No candidate selected</div>
                        <div class="hf-pipeline-subtitle">
                            The candidate profile card will populate after backend integration.
                        </div>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 1rem; margin-top: 1.35rem;">
                    <div>
                        <span class="hf-pipeline-label">Department</span>
                        <div class="hf-pipeline-value">—</div>
                    </div>
                    <div>
                        <span class="hf-pipeline-label">Position</span>
                        <div class="hf-pipeline-value">—</div>
                    </div>
                    <div>
                        <span class="hf-pipeline-label">Recruiter</span>
                        <div class="hf-pipeline-value">—</div>
                    </div>
                    <div>
                        <span class="hf-pipeline-label">Applied Date</span>
                        <div class="hf-pipeline-value">—</div>
                    </div>
                    <div>
                        <span class="hf-pipeline-label">Current Stage</span>
                        <div class="hf-pipeline-value">Awaiting data</div>
                    </div>
                    <div>
                        <span class="hf-pipeline-label">Status</span>
                        <div class="hf-pipeline-value">Pending</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        f"""
        <div class="hf-pipeline-card">
            <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                <div class="hf-pipeline-avatar">{candidate.get('initials', '?')}</div>
                <div style="flex: 1; min-width: 220px;">
                    <div class="hf-pipeline-title">{candidate.get('name', 'Candidate')}</div>
                    <div class="hf-pipeline-subtitle">{candidate.get('position', 'Position')}</div>
                </div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 1rem; margin-top: 1.35rem;">
                <div>
                    <span class="hf-pipeline-label">Department</span>
                    <div class="hf-pipeline-value">{candidate.get('department', '—')}</div>
                </div>
                <div>
                    <span class="hf-pipeline-label">Recruiter</span>
                    <div class="hf-pipeline-value">{candidate.get('recruiter', '—')}</div>
                </div>
                <div>
                    <span class="hf-pipeline-label">Current Stage</span>
                    <div class="hf-pipeline-value">{candidate.get('current_stage', '—')}</div>
                </div>
                <div>
                    <span class="hf-pipeline-label">Applied Date</span>
                    <div class="hf-pipeline-value">{candidate.get('applied_date', '—')}</div>
                </div>
                <div>
                    <span class="hf-pipeline-label">Overall Progress</span>
                    <div class="hf-pipeline-value">{candidate.get('progress', '—')}</div>
                </div>
                <div>
                    <span class="hf-pipeline-label">Status</span>
                    <div class="hf-pipeline-value">{candidate.get('status', '—')}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_pipeline_metrics(selected_stage: str | None = None) -> None:
    """Render KPI metrics for the current recruitment pipeline state."""
    progress = _progress_for_stage(selected_stage)
    stage_index = (
        PIPELINE_STAGES.index(selected_stage)
        if selected_stage in PIPELINE_STAGES
        else -1
    )
    completed_stages = stage_index if stage_index >= 0 else 0
    remaining_stages = len(PIPELINE_STAGES) - completed_stages - 1

    cols = st.columns(5, gap="large")
    cols[0].metric("Current Stage", selected_stage or "Awaiting data")
    cols[1].metric("Days in Current Stage", "—")
    cols[2].metric("Completed Stages", f"{completed_stages}")
    cols[3].metric("Remaining Stages", f"{max(remaining_stages, 0)}")
    cols[4].metric("Overall Progress", f"{progress}%")


def render_pipeline_timeline(selected_stage: str | None = None) -> None:
    """Render the recruitment pipeline timeline with stage state indicators."""
    stage_blocks = []
    for stage in PIPELINE_STAGES:
        status = _stage_status(stage, selected_stage)
        icon = STAGE_ICONS[status]
        label_class = f"hf-stage-badge hf-stage-badge--{status}"
        round_label = INTERVIEW_STAGE_ROUNDS.get(stage, "")
        round_html = (
            f"<div class=\"hf-stage-meta\">Round: —</div>"
            if round_label
            else ""
        )

        stage_blocks.append(
            f"""
            <div class="hf-pipeline-stage hf-pipeline-stage--{status}">
                <div class="hf-stage-badge {label_class}">
                    <span>{icon}</span>
                    <span>{status.title()}</span>
                </div>
                <div class="hf-stage-title">{_sanitize_stage(stage)}</div>
                <div class="hf-stage-meta">Date: —</div>
                <div class="hf-stage-meta">Recruiter: —</div>
                {round_html}
            </div>
            """
        )

    pipeline_html = """
    <div class="hf-pipeline-grid">
    """
    pipeline_html += "\n".join(stage_blocks)
    pipeline_html += "</div>"

    st.markdown(pipeline_html, unsafe_allow_html=True)


def render_stage_details(selected_stage: str | None = None) -> None:
    """Render stage detail panels for the selected pipeline stage."""
    stage_name = selected_stage or "Stage details will appear after backend integration"
    tabs = st.tabs(["Overview", "Comments", "Next Action"])

    with tabs[0]:
        st.markdown(
            f"""
            <div class="hf-detail-card">
                <div class="hf-detail-label">Stage Name</div>
                <div class="hf-detail-value">{stage_name}</div>
                <div class="hf-detail-label">Description</div>
                <div class="hf-detail-value">
                    This panel highlights the selected stage and displays details once backend data is connected.
                </div>
                <div class="hf-detail-label">Assigned Recruiter</div>
                <div class="hf-detail-value">—</div>
                <div class="hf-detail-label">Interview Date</div>
                <div class="hf-detail-value">—</div>
                <div class="hf-detail-label">Status</div>
                <div class="hf-detail-value">Awaiting updates</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tabs[1]:
        st.markdown(
            """
            <div class="hf-detail-card">
                <div class="hf-detail-label">Comments</div>
                <div class="hf-detail-value">
                    Candidate stage comments will appear here after the backend integration is completed.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with tabs[2]:
        st.markdown(
            """
            <div class="hf-detail-card">
                <div class="hf-detail-label">Next Action</div>
                <div class="hf-detail-value">
                    This area will surface the next hiring action for the current stage.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_pipeline_page() -> None:
    """Render the full recruitment pipeline page shell."""
    render_pipeline_style()

    st.markdown(
        '<div class="hf-page-banner">'
        '<strong>Recruitment pipeline UI is ready.</strong> Connect backend data to populate candidates, stages, and timeline progress.'
        '</div>',
        unsafe_allow_html=True,
    )

    selected_stage = st.selectbox(
        "Review stage details",
        options=PIPELINE_STAGES,
        help="Choose a stage to preview the frontend details layout.",
    )

    with st.container():
        left, right = st.columns([1.25, 1], gap="large")
        with left:
            render_candidate_summary(None)
        with right:
            render_pipeline_metrics(selected_stage)

    st.divider()
    st.subheader("Recruitment Pipeline Timeline")
    st.markdown(
        "The timeline displays every stage in the hiring journey and will update once candidate stage tracking is connected.",
    )
    render_pipeline_timeline(selected_stage)

    st.divider()
    st.subheader("Stage Details")
    render_stage_details(selected_stage)
