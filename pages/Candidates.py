"""Candidate Management page for HireFlow Analytics."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from components.filters import (
    department_filter,
    position_filter,
    search_box,
    stage_filter,
)
from components.forms import candidate_form
from components.tables import candidate_table
from utils.candidates import (
    filter_candidates,
    load_candidates,
    save_candidate,
    search_candidates,
)


def _apply_page_style() -> None:
    """Apply light dashboard styling for the Candidates module."""
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.75rem;
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
            margin-bottom: 1.2rem;
        }
        .hf-section-title {
            color: #101828;
            font-size: 1.05rem;
            font-weight: 700;
            margin-top: 0.2rem;
            margin-bottom: 0.35rem;
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
    st.markdown('<div class="hf-breadcrumb">Dashboard &gt; Candidates</div>', unsafe_allow_html=True)
    st.markdown('<div class="hf-page-title">Candidate Management</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hf-page-subtitle">Search, filter, and add recruitment pipeline candidates.</div>',
        unsafe_allow_html=True,
    )


def _render_toolbar() -> tuple[str, str, str, str]:
    """Render search, filters, refresh, and add actions."""
    with st.container(border=True):
        search_col, dept_col, stage_col, pos_col, refresh_col, add_col = st.columns(
            [2.1, 1.25, 1.25, 1.45, 0.8, 1.1]
        )

        with search_col:
            search_term = search_box()

        with dept_col:
            department = department_filter()

        with stage_col:
            stage = stage_filter()

        with pos_col:
            position = position_filter()

        with refresh_col:
            st.write("")
            st.write("")
            if st.button("Refresh", width="stretch"):
                st.rerun()

        with add_col:
            st.write("")
            st.write("")
            if st.button("Add Candidate", type="primary", width="stretch"):
                st.session_state["show_candidate_form"] = True

    return search_term, department, stage, position


def _render_summary_metrics(candidates: pd.DataFrame, filtered: pd.DataFrame) -> None:
    """Render quick candidate list metrics."""
    active_candidates = int((filtered["Status"] == "Active").sum())
    offer_stage_candidates = int((filtered["Current Stage"] == "Offer").sum())
    hired_candidates = int(filtered["Status"].isin(["Hired"]).sum())

    metric_cols = st.columns(4)
    metric_cols[0].metric("Total Candidates", len(candidates))
    metric_cols[1].metric("Filtered Results", len(filtered))
    metric_cols[2].metric("Active Pipeline", active_candidates)
    metric_cols[3].metric("Offer Stage", offer_stage_candidates + hired_candidates)


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


def render_page() -> None:
    """Render the complete Candidate Management module."""
    st.set_page_config(
        page_title="Candidates | HireFlow Analytics",
        layout="wide",
    )
    _apply_page_style()
    _render_header()

    success_message = st.session_state.pop("candidate_success", None)
    if success_message:
        st.success(success_message)

    candidates = load_candidates()
    search_term, department, stage, position = _render_toolbar()

    searched_candidates = search_candidates(candidates, search_term)
    filtered_candidates = filter_candidates(
        searched_candidates,
        department=department,
        stage=stage,
        position=position,
    )

    st.write("")
    _render_add_candidate_panel()

    st.write("")
    _render_summary_metrics(candidates, filtered_candidates)

    st.write("")
    st.markdown('<div class="hf-section-title">Candidate List</div>', unsafe_allow_html=True)
    candidate_table(filtered_candidates)


render_page()
