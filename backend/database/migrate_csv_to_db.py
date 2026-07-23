"""Migrate candidate data from CSV to SQLite and seed with interview data.

This script:
1. Loads all candidates from data/candidates.csv
2. Creates interviews for candidates at various pipeline stages
3. Seeds everything into the SQLite database (idempotent)

Run from the repo root:
    python -m HireFlow.backend.database.migrate_csv_to_db
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path
from typing import Generator

import pandas as pd

from HireFlow.backend.database.database import CANDIDATES_TABLE_SQL
from HireFlow.backend.database.interviews_db import INTERVIEWS_TABLE_SQL
from HireFlow.backend.utils.constants import (
    CANDIDATES_CSV_PATH,
    INTERVIEW_RESULTS,
    INTERVIEW_ROUNDS,
    INTERVIEWERS,
    RECOMMENDATIONS,
    SQLITE_DB_PATH,
)


@contextmanager
def _conn() -> Generator[sqlite3.Connection, None, None]:
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


def _ensure_tables() -> None:
    """Create tables if they don't exist."""
    with _conn() as conn:
        conn.execute(CANDIDATES_TABLE_SQL)
        conn.execute(INTERVIEWS_TABLE_SQL)


def _load_csv_candidates() -> list[tuple]:
    """Load candidates from CSV and convert to database format."""
    candidates = []
    df = pd.read_csv(CANDIDATES_CSV_PATH)
    
    for _, row in df.iterrows():
        candidate_id = str(row.get("Candidate ID", "")).strip()
        if not candidate_id:
            continue
        
        # Handle Experience column safely - handle NaN values
        exp_value = row.get("Experience", 0)
        if pd.isna(exp_value):
            experience = 0
        else:
            experience = int(pd.to_numeric(exp_value, errors="coerce") or 0)
            
        candidate = (
            candidate_id,
            str(row.get("Name", "")).strip(),
            str(row.get("Email", "")).strip(),
            str(row.get("Phone", "")).strip(),
            str(row.get("Department", "")).strip(),
            str(row.get("Position", "")).strip(),
            experience,
            str(row.get("Current Stage", "Applied")).strip(),
            str(row.get("Recruiter", "")).strip(),
            str(row.get("Applied Date", "")).strip(),
            str(row.get("Status", "Active")).strip(),
            str(row.get("Drop-off Reason", "")).strip(),
        )
        candidates.append(candidate)
    
    return candidates


def _generate_interviews_for_candidates(candidates: list[tuple]) -> list[tuple]:
    """Generate realistic interview data for candidates at various stages.
    
    Interview rules:
    - Candidates at "Applied" stage: no interviews yet
    - Candidates at "Screening" stage: 1 screening interview
    - Candidates at "Assessment" or later: 2+ interviews
    - Hired candidates: 3+ interviews including HR round
    """
    interviews = []
    interview_counter = 1
    
    # Define interview feedback templates
    feedback_templates = {
        "excellent": {
            "rating": 5,
            "recommendation": "Strong Hire",
            "comments": "Exceptional skills and cultural fit.",
            "strengths": "Problem-solving, communication, leadership",
            "weaknesses": "None identified",
            "result": "Selected",
        },
        "good": {
            "rating": 4,
            "recommendation": "Hire",
            "comments": "Strong candidate with good potential.",
            "strengths": "Technical skills, collaboration",
            "weaknesses": "Minor gaps in one area",
            "result": "Selected",
        },
        "average": {
            "rating": 3,
            "recommendation": "Hire",
            "comments": "Meets requirements with room for growth.",
            "strengths": "Willingness to learn, reliability",
            "weaknesses": "Needs onboarding support",
            "result": "Selected",
        },
        "poor": {
            "rating": 2,
            "recommendation": "No Hire",
            "comments": "Gaps in key competencies.",
            "strengths": "Enthusiasm, communication",
            "weaknesses": "Insufficient technical depth",
            "result": "Rejected",
        },
    }
    
    for candidate in candidates:
        candidate_id, name, email, phone, dept, position, exp, stage, recruiter, applied_date, status, dropoff = candidate
        
        # Skip candidates with no interviews
        if stage in ("Applied",):
            continue
        
        # Determine interview count based on stage
        if stage in ("Screening",):
            rounds_to_create = 1
        elif stage in ("Assessment", "Technical"):
            rounds_to_create = 2
        elif stage in ("HR", "Offer", "Accepted", "Joined"):
            rounds_to_create = 3
        else:
            rounds_to_create = 0
        
        # Create interviews
        try:
            base_date = datetime.strptime(applied_date, "%Y-%m-%d") if applied_date and applied_date != "nan" else datetime.now()
        except (ValueError, TypeError):
            base_date = datetime.now()
        
        for round_num in range(rounds_to_create):
            round_name = INTERVIEW_ROUNDS[min(round_num, len(INTERVIEW_ROUNDS) - 1)]
            interviewer = INTERVIEWERS[round_num % len(INTERVIEWERS)]
            
            # Determine feedback quality based on current stage and status
            if status == "Hired":
                quality = "excellent"
            elif status == "Active" and stage in ("HR", "Offer"):
                quality = "good"
            elif status == "Active":
                quality = "good" if exp >= 5 else "average"
            elif status == "Rejected":
                quality = "poor"
            else:
                quality = "average"
            
            feedback = feedback_templates[quality]
            interview_date = (base_date + timedelta(days=7 * (round_num + 1))).strftime("%Y-%m-%d")
            
            interview = (
                f"HF-INT-{interview_counter:03d}",
                candidate_id,
                round_name,
                interviewer,
                feedback["rating"],
                feedback["recommendation"],
                feedback["comments"],
                feedback["strengths"],
                feedback["weaknesses"],
                interview_date,
                feedback["result"],
            )
            interviews.append(interview)
            interview_counter += 1
    
    return interviews


def _seed_candidates(conn: sqlite3.Connection, candidates: list[tuple]) -> tuple[int, int]:
    """Insert candidates into database; return (inserted, skipped) counts."""
    inserted = skipped = 0
    for row in candidates:
        cursor = conn.execute(
            """
            INSERT OR IGNORE INTO candidates
                (candidate_id, name, email, phone, department, position,
                 experience, current_stage, recruiter, applied_date,
                 status, drop_off_reason)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            row,
        )
        if cursor.rowcount:
            inserted += 1
        else:
            skipped += 1
    return inserted, skipped


def _seed_interviews(conn: sqlite3.Connection, interviews: list[tuple]) -> tuple[int, int]:
    """Insert interviews into database; return (inserted, skipped) counts."""
    inserted = skipped = 0
    for row in interviews:
        cursor = conn.execute(
            """
            INSERT OR IGNORE INTO interviews
                (interview_id, candidate_id, round, interviewer,
                 rating, recommendation, comments, strengths, weaknesses,
                 date, result)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            row,
        )
        if cursor.rowcount:
            inserted += 1
        else:
            skipped += 1
    return inserted, skipped


def run_migration() -> None:
    """Migrate CSV data to SQLite and seed with interviews."""
    print("[migrate] Starting CSV to SQLite migration...")
    
    # Ensure tables exist
    _ensure_tables()
    
    # Load candidates from CSV
    print("[migrate] Loading candidates from CSV...")
    csv_candidates = _load_csv_candidates()
    print(f"[migrate] Loaded {len(csv_candidates)} candidates from CSV")
    
    # Generate interviews for loaded candidates
    print("[migrate] Generating interview data...")
    interviews = _generate_interviews_for_candidates(csv_candidates)
    print(f"[migrate] Generated {len(interviews)} interview records")
    
    # Seed everything into database
    with _conn() as conn:
        c_ins, c_skip = _seed_candidates(conn, csv_candidates)
        i_ins, i_skip = _seed_interviews(conn, interviews)
    
    print(
        f"\n[migrate] ✓ Migration complete!\n"
        f"  Candidates: {c_ins} inserted, {c_skip} skipped\n"
        f"  Interviews: {i_ins} inserted, {i_skip} skipped"
    )


if __name__ == "__main__":
    run_migration()
