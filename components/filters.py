"""Reusable Streamlit filter controls."""

from __future__ import annotations

import streamlit as st

from utils.constants import (
    ALL_FILTER_OPTION,
    DEPARTMENTS,
    POSITIONS,
    STAGES,
)


def search_box(key: str = "candidate_search") -> str:
    """Render the candidate search input."""
    return st.text_input(
        "Search Candidate",
        placeholder="Search by name, email, or position",
        key=key,
    )


def department_filter(key: str = "candidate_department_filter") -> str:
    """Render the department select filter."""
    return st.selectbox(
        "Department",
        [ALL_FILTER_OPTION, *DEPARTMENTS],
        key=key,
    )


def stage_filter(key: str = "candidate_stage_filter") -> str:
    """Render the recruitment stage select filter."""
    return st.selectbox(
        "Stage",
        [ALL_FILTER_OPTION, *STAGES],
        key=key,
    )


def position_filter(key: str = "candidate_position_filter") -> str:
    """Render the position select filter."""
    return st.selectbox(
        "Position",
        [ALL_FILTER_OPTION, *POSITIONS],
        key=key,
    )
