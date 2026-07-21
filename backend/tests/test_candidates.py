"""Tests for update_candidate_stage / mark_candidate_dropped (CSV layer)."""
import pandas as pd
import pytest

from HireFlow.backend.utils import candidates as c

@pytest.fixture
def seeded_csv(tmp_path):
    """A CSV with one seeded candidate, returns its path."""
    csv_path = tmp_path / "candidates.csv"
    record = {
        "Candidate ID": "HF-CAND-001",
        "Name": "Test Candidate",
        "Email": "test@example.com",
        "Phone": "1234567890",
        "Department": "Engineering",
        "Position": "Backend Developer",
        "Experience": 3,
        "Current Stage": "Applied",
        "Recruiter": "Aisha Sharma",
        "Applied Date": "2026-07-01",
        "Status": "Active",
        "Drop-off Reason": "",
    }
    pd.DataFrame([record], columns=c.CANDIDATE_COLUMNS).to_csv(csv_path, index=False)
    return csv_path


def _row(csv_path, candidate_id="HF-CAND-001"):
    df = c.load_candidates(csv_path)
    return df[df["Candidate ID"] == candidate_id].iloc[0]


def test_update_candidate_stage_valid(seeded_csv):
    c.update_candidate_stage("HF-CAND-001", "Technical", seeded_csv)
    assert _row(seeded_csv)["Current Stage"] == "Technical"


def test_update_candidate_stage_rejects_invalid_stage(seeded_csv):
    with pytest.raises(ValueError):
        c.update_candidate_stage("HF-CAND-001", "Not A Real Stage", seeded_csv)


def test_update_candidate_stage_raises_on_missing_candidate(seeded_csv):
    with pytest.raises(c.CandidateNotFoundError):
        c.update_candidate_stage("HF-CAND-999", "Technical", seeded_csv)


def test_mark_candidate_dropped_sets_status_and_reason(seeded_csv):
    c.mark_candidate_dropped("HF-CAND-001", "Ghosted", seeded_csv)
    row = _row(seeded_csv)
    assert row["Status"] == "Rejected"
    assert row["Drop-off Reason"] == "Ghosted"


def test_mark_candidate_dropped_rejects_invalid_reason(seeded_csv):
    with pytest.raises(ValueError):
        c.mark_candidate_dropped("HF-CAND-001", "Not A Real Reason", seeded_csv)


def test_mark_candidate_dropped_raises_on_missing_candidate(seeded_csv):
    with pytest.raises(c.CandidateNotFoundError):
        c.mark_candidate_dropped("HF-CAND-999", "Ghosted", seeded_csv)


def test_update_stage_only_touches_matched_candidate(tmp_path):
    """A second unrelated candidate in the CSV should stay untouched."""
    csv_path = tmp_path / "candidates.csv"
    records = [
        {
            "Candidate ID": "HF-CAND-001", "Name": "A", "Email": "a@example.com",
            "Phone": "1", "Department": "Engineering", "Position": "Backend Developer",
            "Experience": 3, "Current Stage": "Applied", "Recruiter": "Aisha Sharma",
            "Applied Date": "2026-07-01", "Status": "Active", "Drop-off Reason": "",
        },
        {
            "Candidate ID": "HF-CAND-002", "Name": "B", "Email": "b@example.com",
            "Phone": "2", "Department": "Sales", "Position": "QA Engineer",
            "Experience": 2, "Current Stage": "Screening", "Recruiter": "Daniel Lewis",
            "Applied Date": "2026-07-02", "Status": "Active", "Drop-off Reason": "",
        },
    ]
    pd.DataFrame(records, columns=c.CANDIDATE_COLUMNS).to_csv(csv_path, index=False)

    c.update_candidate_stage("HF-CAND-001", "Technical", csv_path)

    assert _row(csv_path, "HF-CAND-001")["Current Stage"] == "Technical"
    assert _row(csv_path, "HF-CAND-002")["Current Stage"] == "Screening"