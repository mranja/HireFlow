"""Tests for backend/database/seed.py.

Each test runs against a throwaway SQLite file (via monkeypatching), so the
live hireflow.db is never touched.
"""

from __future__ import annotations

import sqlite3

import pytest

from HireFlow.backend.database import database as db
from HireFlow.backend.database import seed as seed_module
from HireFlow.backend.database.seed import (
    SEED_CANDIDATES,
    SEED_INTERVIEWS,
    run_seed,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    """Redirect every DB write to a throwaway file inside tmp_path."""
    test_db_path = tmp_path / "test_seed.db"

    # Patch the path in both the database module and the seed module so they
    # resolve to the same file.
    monkeypatch.setattr(db, "SQLITE_DB_PATH", test_db_path)
    monkeypatch.setattr(seed_module, "SQLITE_DB_PATH", test_db_path)
    yield test_db_path


def _count(table: str, test_db_path) -> int:
    """Return the number of rows in *table* using a direct sqlite3 connection."""
    conn = sqlite3.connect(test_db_path)
    try:
        row = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
        return row[0]
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_run_seed_inserts_all_candidates(tmp_path, monkeypatch):
    """run_seed() inserts every row in SEED_CANDIDATES."""
    test_db_path = tmp_path / "test_seed.db"
    monkeypatch.setattr(db, "SQLITE_DB_PATH", test_db_path)
    monkeypatch.setattr(seed_module, "SQLITE_DB_PATH", test_db_path)

    run_seed()

    assert _count("candidates", test_db_path) == len(SEED_CANDIDATES)


def test_run_seed_inserts_all_interviews(tmp_path, monkeypatch):
    """run_seed() inserts every row in SEED_INTERVIEWS."""
    test_db_path = tmp_path / "test_seed.db"
    monkeypatch.setattr(db, "SQLITE_DB_PATH", test_db_path)
    monkeypatch.setattr(seed_module, "SQLITE_DB_PATH", test_db_path)

    run_seed()

    assert _count("interviews", test_db_path) == len(SEED_INTERVIEWS)


def test_run_seed_is_idempotent(tmp_path, monkeypatch):
    """Calling run_seed() twice does not duplicate rows."""
    test_db_path = tmp_path / "test_seed.db"
    monkeypatch.setattr(db, "SQLITE_DB_PATH", test_db_path)
    monkeypatch.setattr(seed_module, "SQLITE_DB_PATH", test_db_path)

    run_seed()
    run_seed()  # second call must be a no-op

    assert _count("candidates", test_db_path) == len(SEED_CANDIDATES)
    assert _count("interviews", test_db_path) == len(SEED_INTERVIEWS)


def test_seed_candidates_cover_all_departments():
    """SEED_CANDIDATES must include at least one row per expected department."""
    from HireFlow.backend.utils.constants import DEPARTMENTS

    seeded_depts = {row[4] for row in SEED_CANDIDATES}  # index 4 = department
    assert seeded_depts == set(DEPARTMENTS)


def test_seed_candidates_cover_all_statuses():
    """SEED_CANDIDATES must include at least one row for every valid status."""
    from HireFlow.backend.utils.constants import STATUSES

    seeded_statuses = {row[10] for row in SEED_CANDIDATES}  # index 10 = status
    assert seeded_statuses == set(STATUSES)


def test_seed_candidates_cover_all_drop_off_reasons():
    """Every DROP_OFF_REASON must appear on at least one rejected candidate."""
    from HireFlow.backend.utils.constants import DROP_OFF_REASONS

    seeded_reasons = {
        row[11] for row in SEED_CANDIDATES if row[11]
    }  # index 11 = drop_off_reason (non-empty only)
    assert seeded_reasons == set(DROP_OFF_REASONS)


def test_seed_candidates_unique_ids():
    """Every candidate_id in SEED_CANDIDATES is unique."""
    ids = [row[0] for row in SEED_CANDIDATES]
    assert len(ids) == len(set(ids))


def test_seed_interviews_unique_ids():
    """Every interview_id in SEED_INTERVIEWS is unique."""
    ids = [row[0] for row in SEED_INTERVIEWS]
    assert len(ids) == len(set(ids))


def test_seed_interviews_reference_valid_candidates():
    """Every candidate_id in SEED_INTERVIEWS must exist in SEED_CANDIDATES."""
    valid_cids = {row[0] for row in SEED_CANDIDATES}
    for interview in SEED_INTERVIEWS:
        assert interview[1] in valid_cids, (
            f"Interview {interview[0]} references unknown candidate {interview[1]}"
        )


def test_seed_candidates_all_have_required_fields():
    """No candidate row has an empty name, email, department, position, or stage."""
    for row in SEED_CANDIDATES:
        cid, name, email, _phone, dept, pos, _exp, stage, _rec, _date, _status, _reason = row
        assert name,  f"{cid}: name is empty"
        assert email, f"{cid}: email is empty"
        assert dept,  f"{cid}: department is empty"
        assert pos,   f"{cid}: position is empty"
        assert stage, f"{cid}: current_stage is empty"


def test_seed_rejected_candidates_have_drop_off_reason():
    """Every candidate with status='Rejected' must have a non-empty drop_off_reason."""
    for row in SEED_CANDIDATES:
        cid, _name, _email, _phone, _dept, _pos, _exp, _stage, _rec, _date, status, reason = row
        if status == "Rejected":
            assert reason, f"{cid}: Rejected candidate has no drop_off_reason"


def test_seed_non_rejected_candidates_have_no_drop_off_reason():
    """Non-rejected candidates should have an empty drop_off_reason string."""
    for row in SEED_CANDIDATES:
        cid, _name, _email, _phone, _dept, _pos, _exp, _stage, _rec, _date, status, reason = row
        if status != "Rejected":
            assert reason == "", (
                f"{cid}: Non-rejected candidate has unexpected drop_off_reason={reason!r}"
            )
