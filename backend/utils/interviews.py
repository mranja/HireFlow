"""Interview data access helpers backed by CSV storage.

Mirrors utils/candidates.py: functions hide the storage format from
Streamlit pages, so a future SQLite repository can keep the same function
names and return shapes without forcing UI changes.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

import pandas as pd

from HireFlow.backend.utils.candidates import load_candidates
from HireFlow.backend.utils.constants import (
    CANDIDATES_CSV_PATH,
    INTERVIEW_COLUMNS,
    INTERVIEW_RESULTS,
    INTERVIEW_ROUNDS,
    INTERVIEWERS,
    INTERVIEWS_CSV_PATH,
    RECOMMENDATIONS,
)


class InterviewNotFoundError(Exception):
    """Raised when an interview_id does not exist in the CSV store."""


def _ensure_interviews_file(csv_path: Path) -> None:
    """Create the interviews CSV with the expected headers if missing."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    if not csv_path.exists():
        pd.DataFrame(columns=INTERVIEW_COLUMNS).to_csv(csv_path, index=False)


def _normalise_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Return a dataframe with all required columns in the expected order."""
    normalised = df.copy()

    for column in INTERVIEW_COLUMNS:
        if column not in normalised.columns:
            normalised[column] = ""

    normalised = normalised[INTERVIEW_COLUMNS]
    normalised["Rating"] = (
        pd.to_numeric(normalised["Rating"], errors="coerce").fillna(0).astype(int)
    )

    text_columns = [col for col in INTERVIEW_COLUMNS if col != "Rating"]
    normalised[text_columns] = normalised[text_columns].fillna("").astype(str)
    return normalised


def load_interviews(csv_path: Path = INTERVIEWS_CSV_PATH) -> pd.DataFrame:
    """Load interview records from CSV as a normalized dataframe."""
    _ensure_interviews_file(csv_path)

    df = pd.read_csv(
        csv_path,
        dtype={
            col: "string" for col in INTERVIEW_COLUMNS if col != "Rating"
        },
    )
    return _normalise_dataframe(df)


def _generate_interview_id(existing_interviews: pd.DataFrame) -> str:
    """Generate the next stable Interview ID using the HF-INT-000 format."""
    if existing_interviews.empty:
        return "HF-INT-001"

    id_numbers = (
        existing_interviews["Interview ID"]
        .astype(str)
        .str.extract(r"(\d+)$")[0]
        .dropna()
        .astype(int)
    )

    next_number = 1 if id_numbers.empty else int(id_numbers.max()) + 1
    return f"HF-INT-{next_number:03d}"


def _validate_interview_fields(interview: Mapping[str, Any]) -> list[str]:
    """Validate interview form data and return user-facing error messages."""
    errors: list[str] = []

    if not str(interview.get("Candidate ID", "")).strip():
        errors.append("Candidate ID is required.")

    round_value = interview.get("Round")
    if round_value not in INTERVIEW_ROUNDS:
        errors.append(f"Round must be one of {INTERVIEW_ROUNDS}.")

    interviewer = interview.get("Interviewer")
    if interviewer not in INTERVIEWERS:
        errors.append(f"Interviewer must be one of {INTERVIEWERS}.")

    rating = interview.get("Rating")
    try:
        rating_int = int(rating)
        if not 1 <= rating_int <= 5:
            errors.append("Rating must be between 1 and 5.")
    except (TypeError, ValueError):
        errors.append("Rating must be a number between 1 and 5.")

    recommendation = interview.get("Recommendation")
    if recommendation not in RECOMMENDATIONS:
        errors.append(f"Recommendation must be one of {RECOMMENDATIONS}.")

    result = interview.get("Result")
    if result not in INTERVIEW_RESULTS:
        errors.append(f"Result must be one of {INTERVIEW_RESULTS}.")

    return errors


def _prepare_interview_record(
    interview: Mapping[str, Any],
    existing_interviews: pd.DataFrame,
) -> dict[str, Any]:
    """Convert form data into a CSV-ready interview record."""
    record = {column: interview.get(column, "") for column in INTERVIEW_COLUMNS}
    record["Interview ID"] = record["Interview ID"] or _generate_interview_id(
        existing_interviews
    )
    record["Rating"] = int(record.get("Rating") or 0)
    return record


def save_interview(
    interview: Mapping[str, Any],
    csv_path: Path = INTERVIEWS_CSV_PATH,
    candidates_csv_path: Path = CANDIDATES_CSV_PATH,
) -> pd.DataFrame:
    """Append a new interview to CSV and return the refreshed dataframe.

    Raises:
        ValueError: if required fields are missing/invalid, or if
            Candidate ID doesn't reference an existing candidate.
    """
    errors = _validate_interview_fields(interview)
    if errors:
        raise ValueError(" ".join(errors))

    candidates = load_candidates(candidates_csv_path)
    candidate_id = str(interview["Candidate ID"]).strip()
    if not (candidates["Candidate ID"] == candidate_id).any():
        raise ValueError(f"No candidate with id={candidate_id!r} exists.")

    interviews = load_interviews(csv_path)
    record = _prepare_interview_record(interview, interviews)
    record["Candidate ID"] = candidate_id

    updated_interviews = pd.concat(
        [interviews, pd.DataFrame([record], columns=INTERVIEW_COLUMNS)],
        ignore_index=True,
    )
    updated_interviews.to_csv(csv_path, index=False)
    return updated_interviews


def get_interviews_for_candidate(
    df: pd.DataFrame, candidate_id: str
) -> pd.DataFrame:
    """Return all interview rounds for a single candidate."""
    return df.loc[df["Candidate ID"] == candidate_id].copy()


def _locate_interview(interviews: pd.DataFrame, interview_id: str) -> pd.Series:
    """Return the boolean mask for interview_id, raising if not found."""
    match = interviews["Interview ID"] == interview_id
    if not match.any():
        raise InterviewNotFoundError(f"No interview with id={interview_id!r}")
    return match


_UPDATABLE_FIELDS = {
    "Round", "Interviewer", "Rating", "Recommendation",
    "Comments", "Strengths", "Weaknesses", "Date", "Result",
}


def update_interview(
    interview_id: str,
    updates: Mapping[str, Any],
    csv_path: Path = INTERVIEWS_CSV_PATH,
) -> pd.DataFrame:
    """Update one or more fields on an existing interview record.

    Unknown keys in `updates` are ignored rather than raising.

    Raises:
        ValueError: if no valid fields were provided.
        InterviewNotFoundError: if interview_id doesn't exist.
    """
    valid_updates = {k: v for k, v in updates.items() if k in _UPDATABLE_FIELDS}
    if not valid_updates:
        raise ValueError("No valid fields provided to update.")

    interviews = load_interviews(csv_path)
    match = _locate_interview(interviews, interview_id)

    for column, value in valid_updates.items():
        interviews.loc[match, column] = value

    interviews.to_csv(csv_path, index=False)
    return interviews


def delete_interview(
    interview_id: str,
    csv_path: Path = INTERVIEWS_CSV_PATH,
) -> pd.DataFrame:
    """Delete an interview record by id.

    Raises:
        InterviewNotFoundError: if interview_id doesn't exist.
    """
    interviews = load_interviews(csv_path)
    match = _locate_interview(interviews, interview_id)

    remaining = interviews.loc[~match].copy()
    remaining.to_csv(csv_path, index=False)
    return remaining