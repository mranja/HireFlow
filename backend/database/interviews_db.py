"""SQLite stubs for interviews. Mirrors the candidates table's placeholder
pattern in database.py — implement when the SQLite backend goes live."""

from __future__ import annotations

from typing import Any

import pandas as pd

INTERVIEWS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS interviews (
    interview_id TEXT PRIMARY KEY,
    candidate_id TEXT NOT NULL REFERENCES candidates(candidate_id),
    round TEXT NOT NULL,
    interviewer TEXT NOT NULL,
    rating INTEGER DEFAULT 0,
    recommendation TEXT,
    comments TEXT,
    strengths TEXT,
    weaknesses TEXT,
    date TEXT,
    result TEXT
)
"""


def get_all_interviews() -> pd.DataFrame:
    """Return every interview from SQLite when the database layer is enabled."""
    raise NotImplementedError("SQLite interview retrieval is not implemented yet.")


def get_interviews_for_candidate(candidate_id: str) -> pd.DataFrame:
    """Return all interview rounds for one candidate from SQLite."""
    raise NotImplementedError("SQLite interview retrieval is not implemented yet.")


def insert_interview(interview: dict[str, Any]) -> int:
    """Insert an interview into SQLite and return the inserted row ID."""
    raise NotImplementedError("SQLite interview insertion is not implemented yet.")


def update_interview(interview_id: str, updates: dict[str, Any]) -> None:
    """Update an existing interview in SQLite."""
    raise NotImplementedError("SQLite interview updates are not implemented yet.")


def delete_interview(interview_id: str) -> None:
    """Delete an interview from SQLite."""
    raise NotImplementedError("SQLite interview deletion is not implemented yet.")