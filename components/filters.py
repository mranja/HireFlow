"""Reusable Streamlit search and filter controls."""

from __future__ import annotations

from collections.abc import Callable

import streamlit as st

DEPARTMENT_OPTIONS = [
    "Engineering",
    "Marketing",
    "Sales",
    "Finance",
    "HR",
    "Operations",
]

STAGE_OPTIONS = [
    "Applied",
    "Screening",
    "Assessment",
    "Technical Interview",
    "HR Interview",
    "Offer",
    "Accepted",
    "Joined",
]

EXPERIENCE_OPTIONS = [
    "0-1 Years",
    "2-4 Years",
    "5-8 Years",
    "8+ Years",
]

STATUS_OPTIONS = [
    "Active",
    "Rejected",
    "On Hold",
    "Joined",
]

POSITION_OPTIONS = [
    "Frontend Developer",
    "Backend Developer",
    "QA Engineer",
    "Data Analyst",
    "UI Designer",
]

FilterChangeHandler = Callable[[], None] | None


def search_box(
    key: str = "candidate_search",
    on_change: FilterChangeHandler = None,
) -> str:
    """Render the candidate search input."""
    return st.text_input(
        "Search",
        placeholder="Search name, email, phone, or position",
        key=key,
        on_change=on_change,
    )


def department_filter(
    key: str = "candidate_department_filter",
    on_change: FilterChangeHandler = None,
) -> list[str]:
    """Render a reusable department multiselect filter."""
    return st.multiselect(
        "Department",
        options=DEPARTMENT_OPTIONS,
        placeholder="All departments",
        key=key,
        on_change=on_change,
    )


def stage_filter(
    key: str = "candidate_stage_filter",
    on_change: FilterChangeHandler = None,
) -> list[str]:
    """Render a reusable recruitment-stage multiselect filter."""
    return st.multiselect(
        "Stage",
        options=STAGE_OPTIONS,
        placeholder="All stages",
        key=key,
        on_change=on_change,
    )


def experience_filter(
    key: str = "candidate_experience_filter",
    on_change: FilterChangeHandler = None,
) -> list[str]:
    """Render a reusable experience-band multiselect filter."""
    return st.multiselect(
        "Experience",
        options=EXPERIENCE_OPTIONS,
        placeholder="All experience",
        key=key,
        on_change=on_change,
    )


def status_filter(
    key: str = "candidate_status_filter",
    on_change: FilterChangeHandler = None,
) -> list[str]:
    """Render a reusable candidate-status multiselect filter."""
    return st.multiselect(
        "Status",
        options=STATUS_OPTIONS,
        placeholder="All statuses",
        key=key,
        on_change=on_change,
    )


def position_filter(
    key: str = "candidate_position_filter",
    on_change: FilterChangeHandler = None,
) -> list[str]:
    """Render a reusable position filter for existing pages."""
    return st.multiselect(
        "Position",
        options=POSITION_OPTIONS,
        placeholder="All positions",
        key=key,
        on_change=on_change,
    )
