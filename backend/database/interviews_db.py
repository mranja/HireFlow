"""SQLite database layer for interview management."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from typing import Any, Generator

import pandas as pd

from HireFlow.backend.utils.constants import SQLITE_DB_PATH


@contextmanager
def _get_connection() -> Generator[sqlite3.Connection, None, None]:
    """Get a database connection with proper setup."""
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
    """Return all interviews as a DataFrame."""
    with _get_connection() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM interviews
            ORDER BY date DESC, interview_id
            """
        ).fetchall()
    
    if not rows:
        return pd.DataFrame(columns=[
            "Interview ID", "Candidate ID", "Round", "Interviewer",
            "Rating", "Recommendation", "Comments", "Strengths", "Weaknesses", "Date", "Result"
        ])
    
    interviews = []
    for row in rows:
        interview = {
            "Interview ID": row["interview_id"],
            "Candidate ID": row["candidate_id"],
            "Round": row["round"],
            "Interviewer": row["interviewer"],
            "Rating": row["rating"],
            "Recommendation": row["recommendation"],
            "Comments": row["comments"],
            "Strengths": row["strengths"],
            "Weaknesses": row["weaknesses"],
            "Date": row["date"],
            "Result": row["result"],
        }
        interviews.append(interview)
    
    return pd.DataFrame(interviews)


def get_interviews_for_candidate(candidate_id: str) -> pd.DataFrame:
    """Return all interviews for a specific candidate."""
    with _get_connection() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM interviews
            WHERE candidate_id = ?
            ORDER BY date ASC
            """,
            (candidate_id,),
        ).fetchall()
    
    if not rows:
        return pd.DataFrame(columns=[
            "Interview ID", "Candidate ID", "Round", "Interviewer",
            "Rating", "Recommendation", "Comments", "Strengths", "Weaknesses", "Date", "Result"
        ])
    
    interviews = []
    for row in rows:
        interview = {
            "Interview ID": row["interview_id"],
            "Candidate ID": row["candidate_id"],
            "Round": row["round"],
            "Interviewer": row["interviewer"],
            "Rating": row["rating"],
            "Recommendation": row["recommendation"],
            "Comments": row["comments"],
            "Strengths": row["strengths"],
            "Weaknesses": row["weaknesses"],
            "Date": row["date"],
            "Result": row["result"],
        }
        interviews.append(interview)
    
    return pd.DataFrame(interviews)


def insert_interview(interview: dict[str, Any]) -> int:
    """Insert an interview and return the inserted row ID."""
    with _get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO interviews
                (interview_id, candidate_id, round, interviewer,
                 rating, recommendation, comments, strengths, weaknesses, date, result)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                interview.get("Interview ID"),
                interview.get("Candidate ID"),
                interview.get("Round"),
                interview.get("Interviewer"),
                interview.get("Rating", 0),
                interview.get("Recommendation"),
                interview.get("Comments"),
                interview.get("Strengths"),
                interview.get("Weaknesses"),
                interview.get("Date"),
                interview.get("Result"),
            ),
        )
    return cursor.lastrowid


def update_interview(interview_id: str, updates: dict[str, Any]) -> None:
    """Update an existing interview."""
    _UPDATABLE_FIELDS = {
        "round", "interviewer", "rating", "recommendation",
        "comments", "strengths", "weaknesses", "date", "result",
    }
    
    valid_updates = {k: v for k, v in updates.items() if k.lower() in _UPDATABLE_FIELDS}
    if not valid_updates:
        raise ValueError("No valid fields provided to update.")
    
    set_clause = ", ".join(f"{k} = ?" for k in valid_updates.keys())
    values = list(valid_updates.values())
    values.append(interview_id)
    
    with _get_connection() as conn:
        conn.execute(
            f"""
            UPDATE interviews
            SET {set_clause}
            WHERE interview_id = ?
            """,
            values,
        )


def delete_interview(interview_id: str) -> None:
    """Delete an interview by ID."""
    with _get_connection() as conn:
        conn.execute(
            """
            DELETE FROM interviews
            WHERE interview_id = ?
            """,
            (interview_id,),
        )