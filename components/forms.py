"""Reusable Streamlit forms."""

from __future__ import annotations

import re
from datetime import date
from typing import Any

import streamlit as st

from HireFlow.backend.utils.constants import DEPARTMENTS, POSITIONS, RECRUITERS, STAGES

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def _form_key(form_key: str, field_name: str) -> str:
    """Build a stable session-state key for a form field."""
    return f"{form_key}_{field_name}"


def _reset_form(form_key: str) -> None:
    """Clear all candidate form widget values from session state."""
    field_names = [
        "name",
        "email",
        "phone",
        "department",
        "position",
        "experience",
        "stage",
        "recruiter",
        "applied_date",
    ]

    for field_name in field_names:
        st.session_state.pop(_form_key(form_key, field_name), None)


def validate_candidate(candidate: dict[str, Any]) -> list[str]:
    """Validate candidate form data and return user-facing error messages."""
    errors: list[str] = []
    phone_digits = re.sub(r"\D", "", str(candidate.get("Phone", "")))

    if not str(candidate.get("Name", "")).strip():
        errors.append("Candidate name cannot be empty.")

    if not EMAIL_PATTERN.match(str(candidate.get("Email", "")).strip()):
        errors.append("Enter a valid email address.")

    if len(phone_digits) < 10 or len(phone_digits) > 15:
        errors.append("Enter a valid phone number with 10 to 15 digits.")

    if not candidate.get("Department"):
        errors.append("Department is required.")

    if not candidate.get("Position"):
        errors.append("Position is required.")

    return errors


def candidate_form(form_key: str = "candidate_form") -> dict[str, Any] | None:
    """Render the Add Candidate form and return validated candidate data."""
    with st.form(form_key, clear_on_submit=False):
        st.subheader("Personal Information")
        personal_left, personal_mid, personal_right = st.columns(3)

        with personal_left:
            name = st.text_input(
                "Candidate Name",
                placeholder="Enter full name",
                key=_form_key(form_key, "name"),
            )

        with personal_mid:
            email = st.text_input(
                "Email",
                placeholder="candidate@example.com",
                key=_form_key(form_key, "email"),
            )

        with personal_right:
            phone = st.text_input(
                "Phone",
                placeholder="+91 98765 43210",
                key=_form_key(form_key, "phone"),
            )

        st.subheader("Professional Information")
        professional_left, professional_mid, professional_right = st.columns(3)

        with professional_left:
            department = st.selectbox(
                "Department",
                ["", *DEPARTMENTS],
                format_func=lambda value: "Select department" if value == "" else value,
                key=_form_key(form_key, "department"),
            )

        with professional_mid:
            position = st.selectbox(
                "Position",
                ["", *POSITIONS],
                format_func=lambda value: "Select position" if value == "" else value,
                key=_form_key(form_key, "position"),
            )

        with professional_right:
            experience = st.number_input(
                "Experience",
                min_value=0,
                max_value=50,
                step=1,
                key=_form_key(form_key, "experience"),
            )

        st.subheader("Recruitment")
        recruitment_left, recruitment_mid, recruitment_right = st.columns(3)

        with recruitment_left:
            current_stage = st.selectbox(
                "Current Stage",
                STAGES,
                key=_form_key(form_key, "stage"),
            )

        with recruitment_mid:
            recruiter = st.selectbox(
                "Recruiter",
                RECRUITERS,
                key=_form_key(form_key, "recruiter"),
            )

        with recruitment_right:
            applied_date = st.date_input(
                "Applied Date",
                value=date.today(),
                key=_form_key(form_key, "applied_date"),
            )

        submit_col, reset_col, spacer_col = st.columns([1.2, 1.2, 5])
        with submit_col:
            save_clicked = st.form_submit_button(
                "Save Candidate",
                type="primary",
                width="stretch",
            )
        with reset_col:
            reset_clicked = st.form_submit_button(
                "Reset Form",
                width="stretch",
            )

    if reset_clicked:
        _reset_form(form_key)
        st.rerun()

    if not save_clicked:
        return None

    candidate = {
        "Name": name.strip(),
        "Email": email.strip(),
        "Phone": phone.strip(),
        "Department": department,
        "Position": position,
        "Experience": int(experience),
        "Current Stage": current_stage,
        "Recruiter": recruiter,
        "Applied Date": applied_date.strftime("%Y-%m-%d"),
        "Status": "Active",
    }

    errors = validate_candidate(candidate)
    if errors:
        for error in errors:
            st.error(error)
        return None

    return candidate
