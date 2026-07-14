"""Tests for update_candidate / delete_candidate against SQLite."""
import sqlite3

import pytest

from HireFlow.backend.database import database as db

@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    """Point SQLITE_DB_PATH at a throwaway file for each test."""
    test_db_path = tmp_path / "test_hireflow.db"
    monkeypatch.setattr(db, "SQLITE_DB_PATH", test_db_path)
    db.init_db()
    with db._get_connection() as conn:
        conn.execute(
            """INSERT INTO candidates
               (candidate_id, name, email, department, position,
                current_stage, applied_date, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            ("HF-CAND-001", "Test Candidate", "test@example.com",
             "Engineering", "Backend Developer", "Applied",
             "2026-07-01", "Active"),
        )
    yield


def _fetch(candidate_id="HF-CAND-001"):
    with db._get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM candidates WHERE candidate_id = ?", (candidate_id,)
        ).fetchone()
    return dict(row) if row else None


def test_update_candidate_stage():
    db.update_candidate("HF-CAND-001", {"Current Stage": "Screening"})
    assert _fetch()["current_stage"] == "Screening"


def test_update_ignores_unknown_fields():
    db.update_candidate("HF-CAND-001", {"Status": "Hired", "Not A Field": "x"})
    row = _fetch()
    assert row["status"] == "Hired"
    assert "Not A Field" not in row


def test_update_raises_on_missing_candidate():
    with pytest.raises(db.CandidateNotFoundError):
        db.update_candidate("HF-CAND-999", {"Status": "Hired"})


def test_update_raises_with_no_valid_fields():
    with pytest.raises(ValueError):
        db.update_candidate("HF-CAND-001", {"Not A Field": "x"})


def test_delete_candidate():
    db.delete_candidate("HF-CAND-001")
    assert _fetch() is None


def test_delete_raises_on_missing_candidate():
    with pytest.raises(db.CandidateNotFoundError):
        db.delete_candidate("HF-CAND-999")


def test_update_raises_with_empty_dict():
    with pytest.raises(ValueError):
        db.update_candidate("HF-CAND-001", {})


def test_init_db_is_idempotent():
    db.init_db()
    db.init_db()
    assert _fetch() is not None


def test_update_email_to_existing_email_raises():
    with db._get_connection() as conn:
        conn.execute(
            """INSERT INTO candidates
               (candidate_id, name, email, department, position,
                current_stage, applied_date, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            ("HF-CAND-002", "Other Candidate", "other@example.com",
             "Sales", "SDR", "Applied", "2026-07-02", "Active"),
        )

    with pytest.raises(sqlite3.IntegrityError):
        db.update_candidate("HF-CAND-002", {"Email": "test@example.com"})


def test_update_drop_off_reason():
    db.update_candidate("HF-CAND-001", {"Drop-off Reason": "Ghosted"})
    assert _fetch()["drop_off_reason"] == "Ghosted"


def test_new_candidate_has_empty_drop_off_reason_by_default():
    assert _fetch()["drop_off_reason"] == ""


def test_update_candidate_stage_valid():
    db.update_candidate_stage("HF-CAND-001", "Technical")
    assert _fetch()["current_stage"] == "Technical"


def test_update_candidate_stage_rejects_invalid_stage():
    with pytest.raises(ValueError):
        db.update_candidate_stage("HF-CAND-001", "Not A Real Stage")


def test_update_candidate_stage_raises_on_missing_candidate():
    with pytest.raises(db.CandidateNotFoundError):
        db.update_candidate_stage("HF-CAND-999", "Technical")


def test_mark_candidate_dropped_sets_status_and_reason():
    db.mark_candidate_dropped("HF-CAND-001", "Ghosted")
    row = _fetch()
    assert row["status"] == "Rejected"
    assert row["drop_off_reason"] == "Ghosted"


def test_mark_candidate_dropped_rejects_invalid_reason():
    with pytest.raises(ValueError):
        db.mark_candidate_dropped("HF-CAND-001", "Not A Real Reason")


def test_mark_candidate_dropped_raises_on_missing_candidate():
    with pytest.raises(db.CandidateNotFoundError):
        db.mark_candidate_dropped("HF-CAND-999", "Ghosted")