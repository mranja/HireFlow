"""Database access placeholders for future SQLite integration."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from typing import Any

import pandas as pd

from HireFlow.backend.utils.constants import SQLITE_DB_PATH

# CANDIDATE_COLUMNS uses display-style headers ("Candidate ID", "Current Stage")
# to match the CSV layer in utils/candidates.py. SQLite needs snake_case
# column names, so this mapping keeps the public function signatures
# (dicts keyed by CANDIDATE_COLUMNS) identical across both storage backends.
_COLUMN_TO_SQL = {
    "Candidate ID": "candidate_id",
    "Name": "name",
    "Email": "email",
    "Phone": "phone",
    "Department": "department",
    "Position": "position",
    "Experience": "experience",
    "Current Stage": "current_stage",
    "Recruiter": "recruiter",
    "Applied Date": "applied_date",
    "Status": "status",
}
# Reverse mapping, used by get_all_candidates() once it's implemented (Day 10)
# to convert SQL rows back into CANDIDATE_COLUMNS-keyed dicts for the DataFrame.
_SQL_TO_COLUMN = {sql: col for col, sql in _COLUMN_TO_SQL.items()}

CANDIDATES_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS candidates (
    candidate_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT,
    department TEXT NOT NULL,
    position TEXT NOT NULL,
    experience INTEGER DEFAULT 0,
    current_stage TEXT NOT NULL DEFAULT 'Applied',
    recruiter TEXT,
    applied_date TEXT,
    status TEXT NOT NULL DEFAULT 'Active'
)
"""


class CandidateNotFoundError(Exception):
    """Raised when a candidate_id does not exist in the database."""


@contextmanager
def _get_connection():
    SQLITE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """Create the candidates table if missing. Safe to call repeatedly."""
    with _get_connection() as conn:
        conn.execute(CANDIDATES_TABLE_SQL)


def _row_exists(conn: sqlite3.Connection, candidate_id: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM candidates WHERE candidate_id = ?", (candidate_id,)
    ).fetchone()
    return row is not None


def get_all_candidates() -> pd.DataFrame:
    """Return every candidate from SQLite when the database layer is enabled."""
    raise NotImplementedError("SQLite candidate retrieval is not implemented yet.")


def insert_candidate(candidate: dict[str, Any]) -> int:
    """Insert a candidate into SQLite and return the inserted row ID."""
    raise NotImplementedError("SQLite candidate insertion is not implemented yet.")


def update_candidate(candidate_id: str, updates: dict[str, Any]) -> None:
    """Update an existing candidate in SQLite.

    `updates` is keyed by CANDIDATE_COLUMNS names (e.g. "Current Stage",
    "Status"), matching the shape used by the CSV layer in
    utils/candidates.py so Streamlit pages don't change when this backend
    goes live. Unknown keys are ignored rather than raising.

    Raises:
        ValueError: if no recognized fields were provided.
        CandidateNotFoundError: if candidate_id doesn't exist.
    """
    valid_updates = {
        _COLUMN_TO_SQL[col]: value
        for col, value in updates.items()
        if col in _COLUMN_TO_SQL
    }
    if not valid_updates:
        raise ValueError("No valid fields provided to update.")

    init_db()
    with _get_connection() as conn:
        if not _row_exists(conn, candidate_id):
            raise CandidateNotFoundError(f"No candidate with id={candidate_id!r}")

        set_clause = ", ".join(f"{col} = ?" for col in valid_updates)
        values = [*valid_updates.values(), candidate_id]
        conn.execute(
            f"UPDATE candidates SET {set_clause} WHERE candidate_id = ?", values
        )


def delete_candidate(candidate_id: str) -> None:
    """Delete a candidate from SQLite.

    Raises:
        CandidateNotFoundError: if candidate_id doesn't exist.
    """
    init_db()
    with _get_connection() as conn:
        if not _row_exists(conn, candidate_id):
            raise CandidateNotFoundError(f"No candidate with id={candidate_id!r}")
        conn.execute("DELETE FROM candidates WHERE candidate_id = ?", (candidate_id,))