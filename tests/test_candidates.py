from pathlib import Path

import pandas as pd
import pytest

from utils.candidates import (
    _generate_candidate_id,
    _normalise_dataframe,
    filter_candidates,
    load_candidates,
    save_candidate,
    search_candidates,
)


@pytest.fixture
def sample_candidates():
    return pd.DataFrame(
        [
            {
                "Candidate ID": "HF-CAND-001",
                "Name": "John Doe",
                "Email": "john@test.com",
                "Phone": "1111111111",
                "Department": "Engineering",
                "Position": "Backend Engineer",
                "Experience": 3,
                "Current Stage": "Screening",
                "Recruiter": "Alice",
                "Applied Date": "2026-07-01",
                "Status": "Active",
            },
            {
                "Candidate ID": "HF-CAND-002",
                "Name": "Jane Smith",
                "Email": "jane@test.com",
                "Phone": "2222222222",
                "Department": "HR",
                "Position": "HR Manager",
                "Experience": 5,
                "Current Stage": "Interview",
                "Recruiter": "Bob",
                "Applied Date": "2026-07-02",
                "Status": "Active",
            },
            {
                "Candidate ID": "HF-CAND-003",
                "Name": "Johnny Walker",
                "Email": "walker@test.com",
                "Phone": "3333333333",
                "Department": "Engineering",
                "Position": "Frontend Engineer",
                "Experience": 2,
                "Current Stage": "Offer",
                "Recruiter": "Alice",
                "Applied Date": "2026-07-03",
                "Status": "Rejected",
            },
        ]
    )


# ----------------------------
# LOAD
# ----------------------------

def test_load_candidates_creates_missing_csv(tmp_path):
    csv = tmp_path / "candidates.csv"

    df = load_candidates(csv)

    assert csv.exists()
    assert df.empty


# ----------------------------
# NORMALISATION
# ----------------------------

def test_normalise_dataframe_adds_missing_columns():
    df = pd.DataFrame({"Name": ["John"]})

    result = _normalise_dataframe(df)

    assert "Email" in result.columns
    assert "Experience" in result.columns


def test_normalise_dataframe_converts_experience():
    df = pd.DataFrame(
        {
            "Experience": ["5", "abc", None]
        }
    )

    result = _normalise_dataframe(df)

    assert result["Experience"].tolist() == [5, 0, 0]


# ----------------------------
# ID GENERATION
# ----------------------------

def test_generate_candidate_id_empty():
    df = pd.DataFrame(columns=["Candidate ID"])

    assert _generate_candidate_id(df) == "HF-CAND-001"


def test_generate_candidate_id_next(sample_candidates):
    assert _generate_candidate_id(sample_candidates) == "HF-CAND-004"


# ----------------------------
# SAVE
# ----------------------------

def test_save_candidate(tmp_path):
    csv = tmp_path / "candidates.csv"

    candidate = {
        "Name": "Alex",
        "Email": "alex@test.com",
        "Phone": "123",
        "Department": "Engineering",
        "Position": "Developer",
        "Experience": 2,
        "Current Stage": "Applied",
        "Recruiter": "Alice",
        "Applied Date": "2026-07-10",
    }

    result = save_candidate(candidate, csv)

    assert len(result) == 1
    assert result.iloc[0]["Email"] == "alex@test.com"


def test_duplicate_email(tmp_path):
    csv = tmp_path / "candidates.csv"

    candidate = {
        "Name": "Alex",
        "Email": "alex@test.com",
        "Phone": "123",
        "Department": "Engineering",
        "Position": "Developer",
        "Experience": 2,
        "Current Stage": "Applied",
        "Recruiter": "Alice",
        "Applied Date": "2026-07-10",
    }

    save_candidate(candidate, csv)

    with pytest.raises(ValueError):
        save_candidate(candidate, csv)


# ----------------------------
# SEARCH
# ----------------------------

def test_search_by_name(sample_candidates):
    result = search_candidates(sample_candidates, "John")

    assert len(result) == 2


def test_search_by_email(sample_candidates):
    result = search_candidates(sample_candidates, "jane@test.com")

    assert len(result) == 1


def test_search_by_position(sample_candidates):
    result = search_candidates(sample_candidates, "Backend")

    assert len(result) == 1


def test_search_case_insensitive(sample_candidates):
    result = search_candidates(sample_candidates, "john")

    assert len(result) == 2


def test_search_empty_returns_all(sample_candidates):
    result = search_candidates(sample_candidates, "")

    assert len(result) == len(sample_candidates)


def test_search_whitespace_returns_all(sample_candidates):
    result = search_candidates(sample_candidates, "   ")

    assert len(result) == len(sample_candidates)


def test_search_non_existing(sample_candidates):
    result = search_candidates(sample_candidates, "XYZ")

    assert result.empty


def test_search_special_characters(sample_candidates):
    result = search_candidates(sample_candidates, "@@@")

    assert result.empty


def test_search_sql_injection(sample_candidates):
    result = search_candidates(sample_candidates, "' OR 1=1 --")

    assert result.empty


# ----------------------------
# FILTER
# ----------------------------

def test_filter_department(sample_candidates):
    result = filter_candidates(
        sample_candidates,
        department="Engineering"
    )

    assert len(result) == 2


def test_filter_stage(sample_candidates):
    result = filter_candidates(
        sample_candidates,
        stage="Offer"
    )

    assert len(result) == 1


def test_filter_position(sample_candidates):
    result = filter_candidates(
        sample_candidates,
        position="HR Manager"
    )

    assert len(result) == 1


def test_filter_multiple(sample_candidates):
    result = filter_candidates(
        sample_candidates,
        department="Engineering",
        stage="Offer",
    )

    assert len(result) == 1


def test_filter_invalid_department(sample_candidates):
    result = filter_candidates(
        sample_candidates,
        department="Finance"
    )

    assert result.empty


def test_filter_no_filters_returns_all(sample_candidates):
    result = filter_candidates(sample_candidates)

    assert len(result) == len(sample_candidates)


# ----------------------------
# DATABASE PLACEHOLDER
# ----------------------------

from database import (
    delete_candidate,
    get_all_candidates,
    insert_candidate,
    update_candidate,
)


def test_database_get_all_candidates():
    with pytest.raises(NotImplementedError):
        get_all_candidates()


def test_database_insert():
    with pytest.raises(NotImplementedError):
        insert_candidate({})


def test_database_update():
    with pytest.raises(NotImplementedError):
        update_candidate("HF-CAND-001", {})


def test_database_delete():
    with pytest.raises(NotImplementedError):
        delete_candidate("HF-CAND-001")
