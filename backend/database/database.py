"""SQLite database layer for candidate management."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from typing import Any

import pandas as pd

from HireFlow.backend.utils.constants import (
    DROP_OFF_REASONS,
    SQLITE_DB_PATH,
    STAGES,
)

# Mapping between CSV/display column names and SQLite column names.
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
    "Drop-off Reason": "drop_off_reason",
}

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
    status TEXT NOT NULL DEFAULT 'Active',
    drop_off_reason TEXT DEFAULT ''
)
"""


class CandidateNotFoundError(Exception):
    """Raised when a candidate_id does not exist."""


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
    """Initialize the SQLite database."""
    with _get_connection() as conn:
        conn.execute(CANDIDATES_TABLE_SQL)


def _row_exists(conn: sqlite3.Connection, candidate_id: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM candidates WHERE candidate_id = ?",
        (candidate_id,),
    ).fetchone()

    return row is not None


def get_all_candidates() -> pd.DataFrame:
    """
    Return all candidates as a DataFrame with the same column names
    used by the CSV backend.
    """
    init_db()

    with _get_connection() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM candidates
            ORDER BY applied_date DESC, candidate_id
            """
        ).fetchall()

    if not rows:
        return pd.DataFrame(columns=_COLUMN_TO_SQL.keys())

    candidates = []

    for row in rows:
        candidate = {}

        for sql_col, value in dict(row).items():
            display_col = _SQL_TO_COLUMN.get(sql_col)
            if display_col:
                candidate[display_col] = value

        candidates.append(candidate)

    return pd.DataFrame(candidates)


def insert_candidate(candidate: dict[str, Any]) -> int:
    """
    Insert a candidate into SQLite.

    Returns:
        SQLite row id.
    """
    init_db()

    sql_candidate = {}

    for display_col, sql_col in _COLUMN_TO_SQL.items():
        sql_candidate[sql_col] = candidate.get(display_col)

    columns = ", ".join(sql_candidate.keys())
    placeholders = ", ".join("?" for _ in sql_candidate)
    values = list(sql_candidate.values())

    with _get_connection() as conn:
        cursor = conn.execute(
            f"""
            INSERT INTO candidates ({columns})
            VALUES ({placeholders})
            """,
            values,
        )

        return cursor.lastrowid


def update_candidate(candidate_id: str, updates: dict[str, Any]) -> None:
    """
    Update an existing candidate.

    Raises:
        ValueError:
            If no valid fields were provided.

        CandidateNotFoundError:
            If candidate does not exist.
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
            raise CandidateNotFoundError(
                f"No candidate with id={candidate_id!r}"
            )

        set_clause = ", ".join(f"{col} = ?" for col in valid_updates)

        values = list(valid_updates.values())
        values.append(candidate_id)

        conn.execute(
            f"""
            UPDATE candidates
            SET {set_clause}
            WHERE candidate_id = ?
            """,
            values,
        )


def delete_candidate(candidate_id: str) -> None:
    """
    Delete a candidate.

    Raises:
        CandidateNotFoundError:
            If candidate does not exist.
    """
    init_db()

    with _get_connection() as conn:
        if not _row_exists(conn, candidate_id):
            raise CandidateNotFoundError(
                f"No candidate with id={candidate_id!r}"
            )

        conn.execute(
            """
            DELETE FROM candidates
            WHERE candidate_id = ?
            """,
            (candidate_id,),
        )


def update_candidate_stage(candidate_id: str, new_stage: str) -> None:
    """
    Update a candidate's pipeline stage.
    """
    if new_stage not in STAGES:
        raise ValueError(
            f"{new_stage!r} is not a valid pipeline stage."
        )

    update_candidate(
        candidate_id,
        {
            "Current Stage": new_stage,
        },
    )


def mark_candidate_dropped(
    candidate_id: str,
    drop_off_reason: str,
) -> None:
    """
    Mark a candidate as rejected and store the drop-off reason.
    """
    if drop_off_reason not in DROP_OFF_REASONS:
        raise ValueError(
            f"{drop_off_reason!r} is not a valid drop-off reason."
        )

    update_candidate(
        candidate_id,
        {
            "Status": "Rejected",
            "Drop-off Reason": drop_off_reason,
        },
    )