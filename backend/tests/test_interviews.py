"""Tests for utils/interviews.py (CSV layer)."""
import pandas as pd
import pytest

from HireFlow.backend.utils import candidates as c
from HireFlow.backend.utils import interviews as iv


@pytest.fixture
def seeded_candidates_csv(tmp_path):
    """A candidates CSV with one seeded candidate, returns its path."""
    csv_path = tmp_path / "candidates.csv"
    record = {
        "Candidate ID": "HF-CAND-001", "Name": "Test Candidate",
        "Email": "test@example.com", "Phone": "1234567890",
        "Department": "Engineering", "Position": "Backend Developer",
        "Experience": 3, "Current Stage": "Technical",
        "Recruiter": "Aisha Sharma", "Applied Date": "2026-07-01",
        "Status": "Active", "Drop-off Reason": "",
    }
    pd.DataFrame([record], columns=c.CANDIDATE_COLUMNS).to_csv(csv_path, index=False)
    return csv_path


@pytest.fixture
def valid_interview(seeded_candidates_csv):
    return {
        "Candidate ID": "HF-CAND-001",
        "Round": "Technical",
        "Interviewer": "Daniel Lewis",
        "Rating": 4,
        "Recommendation": "Hire",
        "Comments": "Strong problem solving.",
        "Strengths": "Communication, DSA",
        "Weaknesses": "Limited system design exposure",
        "Date": "2026-07-05",
        "Result": "Selected",
    }


def _load(csv_path):
    return iv.load_interviews(csv_path)


def test_save_interview_creates_record_with_generated_id(
    tmp_path, valid_interview, seeded_candidates_csv
):
    csv_path = tmp_path / "interviews.csv"
    result = iv.save_interview(valid_interview, csv_path, seeded_candidates_csv)
    assert result.iloc[0]["Interview ID"] == "HF-INT-001"
    assert result.iloc[0]["Candidate ID"] == "HF-CAND-001"


def test_save_interview_ids_increment(
    tmp_path, valid_interview, seeded_candidates_csv
):
    csv_path = tmp_path / "interviews.csv"
    iv.save_interview(valid_interview, csv_path, seeded_candidates_csv)
    result = iv.save_interview(valid_interview, csv_path, seeded_candidates_csv)
    assert result.iloc[1]["Interview ID"] == "HF-INT-002"


def test_save_interview_raises_for_unknown_candidate(
    tmp_path, valid_interview, seeded_candidates_csv
):
    csv_path = tmp_path / "interviews.csv"
    valid_interview["Candidate ID"] = "HF-CAND-999"
    with pytest.raises(ValueError, match="No candidate"):
        iv.save_interview(valid_interview, csv_path, seeded_candidates_csv)


def test_save_interview_raises_for_invalid_round(
    tmp_path, valid_interview, seeded_candidates_csv
):
    csv_path = tmp_path / "interviews.csv"
    valid_interview["Round"] = "Not A Real Round"
    with pytest.raises(ValueError):
        iv.save_interview(valid_interview, csv_path, seeded_candidates_csv)


def test_save_interview_raises_for_invalid_rating(
    tmp_path, valid_interview, seeded_candidates_csv
):
    csv_path = tmp_path / "interviews.csv"
    valid_interview["Rating"] = 9
    with pytest.raises(ValueError):
        iv.save_interview(valid_interview, csv_path, seeded_candidates_csv)


def test_load_interviews_creates_file_if_missing(tmp_path):
    csv_path = tmp_path / "interviews.csv"
    df = iv.load_interviews(csv_path)
    assert csv_path.exists()
    assert list(df.columns) == iv.INTERVIEW_COLUMNS
    assert df.empty


def test_get_interviews_for_candidate_filters_correctly(
    tmp_path, valid_interview, seeded_candidates_csv
):
    csv_path = tmp_path / "interviews.csv"
    iv.save_interview(valid_interview, csv_path, seeded_candidates_csv)
    all_interviews = iv.load_interviews(csv_path)
    result = iv.get_interviews_for_candidate(all_interviews, "HF-CAND-001")
    assert len(result) == 1
    result_none = iv.get_interviews_for_candidate(all_interviews, "HF-CAND-999")
    assert result_none.empty


def test_update_interview_updates_fields(
    tmp_path, valid_interview, seeded_candidates_csv
):
    csv_path = tmp_path / "interviews.csv"
    iv.save_interview(valid_interview, csv_path, seeded_candidates_csv)
    updated = iv.update_interview(
        "HF-INT-001", {"Rating": 5, "Result": "Selected"}, csv_path
    )
    row = updated.iloc[0]
    assert row["Rating"] == 5
    assert row["Result"] == "Selected"


def test_update_interview_ignores_unknown_fields(
    tmp_path, valid_interview, seeded_candidates_csv
):
    csv_path = tmp_path / "interviews.csv"
    iv.save_interview(valid_interview, csv_path, seeded_candidates_csv)
    updated = iv.update_interview("HF-INT-001", {"Rating": 5, "Nope": "x"}, csv_path)
    assert "Nope" not in updated.columns


def test_update_interview_raises_with_no_valid_fields(
    tmp_path, valid_interview, seeded_candidates_csv
):
    csv_path = tmp_path / "interviews.csv"
    iv.save_interview(valid_interview, csv_path, seeded_candidates_csv)
    with pytest.raises(ValueError):
        iv.update_interview("HF-INT-001", {"Nope": "x"}, csv_path)


def test_update_interview_raises_on_missing_id(tmp_path):
    csv_path = tmp_path / "interviews.csv"
    iv.load_interviews(csv_path)
    with pytest.raises(iv.InterviewNotFoundError):
        iv.update_interview("HF-INT-999", {"Rating": 5}, csv_path)


def test_delete_interview_removes_record(
    tmp_path, valid_interview, seeded_candidates_csv
):
    csv_path = tmp_path / "interviews.csv"
    iv.save_interview(valid_interview, csv_path, seeded_candidates_csv)
    remaining = iv.delete_interview("HF-INT-001", csv_path)
    assert remaining.empty


def test_delete_interview_raises_on_missing_id(tmp_path):
    csv_path = tmp_path / "interviews.csv"
    iv.load_interviews(csv_path)
    with pytest.raises(iv.InterviewNotFoundError):
        iv.delete_interview("HF-INT-999", csv_path)