"""Candidate data access helpers backed by CSV storage.

The functions in this module intentionally hide the storage format from the
Streamlit pages. A future SQLite repository can keep the same function names
and return shapes without forcing UI changes.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Mapping

import pandas as pd

from utils.constants import (
    ALL_FILTER_OPTION,
    CANDIDATE_COLUMNS,
    CANDIDATES_CSV_PATH,
)


def _ensure_candidates_file(csv_path: Path) -> None:
    """Create the candidate CSV with the expected headers if it is missing."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    if not csv_path.exists():
        pd.DataFrame(columns=CANDIDATE_COLUMNS).to_csv(csv_path, index=False)


def _normalise_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Return a dataframe with all required columns in the expected order."""
    normalised = df.copy()

    for column in CANDIDATE_COLUMNS:
        if column not in normalised.columns:
            normalised[column] = ""

    normalised = normalised[CANDIDATE_COLUMNS]
    normalised["Experience"] = (
        pd.to_numeric(normalised["Experience"], errors="coerce")
        .fillna(0)
        .astype(int)
    )

    text_columns = [col for col in CANDIDATE_COLUMNS if col != "Experience"]
    normalised[text_columns] = normalised[text_columns].fillna("").astype(str)
    return normalised


def load_candidates(csv_path: Path = CANDIDATES_CSV_PATH) -> pd.DataFrame:
    """Load candidate records from CSV as a normalized dataframe."""
    _ensure_candidates_file(csv_path)

    df = pd.read_csv(
        csv_path,
        dtype={
            "Candidate ID": "string",
            "Name": "string",
            "Email": "string",
            "Phone": "string",
            "Department": "string",
            "Position": "string",
            "Current Stage": "string",
            "Recruiter": "string",
            "Applied Date": "string",
            "Status": "string",
        },
    )
    return _normalise_dataframe(df)


def _generate_candidate_id(existing_candidates: pd.DataFrame) -> str:
    """Generate the next stable Candidate ID using the HF-CAND-000 format."""
    if existing_candidates.empty:
        return "HF-CAND-001"

    id_numbers = (
        existing_candidates["Candidate ID"]
        .astype(str)
        .str.extract(r"(\d+)$")[0]
        .dropna()
        .astype(int)
    )

    next_number = 1 if id_numbers.empty else int(id_numbers.max()) + 1
    return f"HF-CAND-{next_number:03d}"


def _prepare_candidate_record(
    candidate: Mapping[str, Any],
    existing_candidates: pd.DataFrame,
) -> dict[str, Any]:
    """Convert form data into a CSV-ready candidate record."""
    record = {column: candidate.get(column, "") for column in CANDIDATE_COLUMNS}
    record["Candidate ID"] = record["Candidate ID"] or _generate_candidate_id(
        existing_candidates
    )
    record["Experience"] = int(record.get("Experience") or 0)
    record["Status"] = record["Status"] or "Active"
    return record


def save_candidate(
    candidate: Mapping[str, Any],
    csv_path: Path = CANDIDATES_CSV_PATH,
) -> pd.DataFrame:
    """Append a new candidate to CSV and return the refreshed dataframe."""
    candidates = load_candidates(csv_path)
    record = _prepare_candidate_record(candidate, candidates)

    existing_emails = candidates["Email"].str.lower().tolist()
    if str(record["Email"]).lower() in existing_emails:
        raise ValueError("A candidate with this email already exists.")

    updated_candidates = pd.concat(
        [candidates, pd.DataFrame([record], columns=CANDIDATE_COLUMNS)],
        ignore_index=True,
    )
    updated_candidates.to_csv(csv_path, index=False)
    return updated_candidates


def search_candidates(df: pd.DataFrame, search_term: str) -> pd.DataFrame:
    """Search candidates by name, email, or position."""
    if not search_term or not search_term.strip():
        return df.copy()

    escaped_term = re.escape(search_term.strip())
    searchable_columns = ["Name", "Email", "Position"]
    search_mask = pd.Series(False, index=df.index)

    for column in searchable_columns:
        search_mask = search_mask | df[column].str.contains(
            escaped_term,
            case=False,
            na=False,
            regex=True,
        )

    return df.loc[search_mask].copy()


def filter_candidates(
    df: pd.DataFrame,
    department: str = ALL_FILTER_OPTION,
    stage: str = ALL_FILTER_OPTION,
    position: str = ALL_FILTER_OPTION,
) -> pd.DataFrame:
    """Filter candidates by department, recruitment stage, and position."""
    filtered_df = df.copy()

    if department and department != ALL_FILTER_OPTION:
        filtered_df = filtered_df[filtered_df["Department"] == department]

    if stage and stage != ALL_FILTER_OPTION:
        filtered_df = filtered_df[filtered_df["Current Stage"] == stage]

    if position and position != ALL_FILTER_OPTION:
        filtered_df = filtered_df[filtered_df["Position"] == position]

    return filtered_df.copy()
