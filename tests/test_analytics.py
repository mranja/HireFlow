"""Tests for aggregate analytics helpers."""

from __future__ import annotations

import math

import pandas as pd

from utils import analytics as a


def _sample_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Candidate ID": "HF-CAND-001",
                "Department": "Engineering",
                "Status": "Active",
                "Applied Date": "2026-06-01",
            },
            {
                "Candidate ID": "HF-CAND-002",
                "Department": "Engineering",
                "Status": "Hired",
                "Applied Date": "2026-06-02",
            },
            {
                "Candidate ID": "HF-CAND-003",
                "Department": "Sales",
                "Status": "Rejected",
                "Applied Date": "2026-07-01",
            },
            {
                "Candidate ID": "HF-CAND-004",
                "Department": "Sales",
                "Status": "Active",
                "Applied Date": "2026-07-01",
            },
            {
                "Candidate ID": "HF-CAND-005",
                "Department": "HR",
                "Status": "Active",
                "Applied Date": "2026-07-03",
            },
        ]
    )


def _interview_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Candidate ID": "HF-CAND-001",
                "Department": "Engineering",
                "Interviewer": "Aisha Sharma",
                "Rating": 5,
                "Result": "Selected",
                "Status": "Active",
                "Applied Date": "2026-06-01",
            },
            {
                "Candidate ID": "HF-CAND-002",
                "Department": "Engineering",
                "Interviewer": "Aisha Sharma",
                "Rating": 4,
                "Result": "Selected",
                "Status": "Active",
                "Applied Date": "2026-06-02",
            },
            {
                "Candidate ID": "HF-CAND-003",
                "Department": "Sales",
                "Interviewer": "Daniel Lewis",
                "Rating": 2,
                "Result": "Rejected",
                "Status": "Rejected",
                "Applied Date": "2026-07-01",
            },
            {
                "Candidate ID": "HF-CAND-004",
                "Department": "Sales",
                "Interviewer": "Daniel Lewis",
                "Rating": 3,
                "Result": "Rejected",
                "Status": "Rejected",
                "Applied Date": "2026-07-01",
            },
            {
                "Candidate ID": "HF-CAND-005",
                "Department": "HR",
                "Interviewer": "Priya Nair",
                "Rating": 4,
                "Result": "Selected",
                "Status": "Active",
                "Applied Date": "2026-07-03",
            },
            {
                "Candidate ID": "HF-CAND-006",
                "Department": "HR",
                "Interviewer": "Priya Nair",
                "Rating": 1,
                "Result": "Rejected",
                "Status": "Rejected",
                "Applied Date": "2026-07-04",
            },
        ]
    )


def test_department_breakdown_counts_rows():
    result = a.department_breakdown(_sample_frame())

    assert list(result.columns) == ["Department", "Count"]
    assert result.iloc[0]["Department"] == "Engineering"
    assert result.iloc[0]["Count"] == 2
    assert result.loc[result["Department"] == "Sales", "Count"].iloc[0] == 2


def test_department_breakdown_applies_filters():
    result = a.department_breakdown(
        _sample_frame(), department="Engineering", status="Active"
    )

    assert list(result.columns) == ["Department", "Count"]
    assert len(result) == 1
    assert result.iloc[0]["Department"] == "Engineering"
    assert result.iloc[0]["Count"] == 1


def test_compare_departments_returns_side_by_side_metrics():
    result = a.compare_departments(
        _sample_frame(), left_department="Engineering", right_department="HR"
    )

    assert list(result.columns) == ["Department", "Metric", "Share", "Delta vs Baseline"]
    assert list(result["Department"]) == ["Engineering", "HR"]
    assert result.loc[result["Department"] == "Engineering", "Metric"].iloc[0] == 2
    assert result.loc[result["Department"] == "HR", "Metric"].iloc[0] == 1
    assert result.loc[result["Department"] == "HR", "Delta vs Baseline"].iloc[0] == -1


def test_outcome_distribution_returns_counts_and_share():
    result = a.outcome_distribution(_sample_frame())

    assert list(result.columns) == ["Status", "Count", "Share"]
    assert result.loc[result["Status"] == "Active", "Count"].iloc[0] == 3
    assert round(result["Share"].sum(), 6) == 1.0


def test_outcome_distribution_can_filter_department():
    result = a.outcome_distribution(_sample_frame(), department="Sales")

    assert result["Count"].sum() == 2
    assert set(result["Status"]) == {"Active", "Rejected"}


def test_trend_over_time_groups_by_month():
    result = a.trend_over_time(_sample_frame(), freq="M")

    assert list(result.columns) == ["Period", "Count"]
    assert result["Count"].sum() == 5
    assert len(result) == 2


def test_trend_over_time_can_filter_department():
    result = a.trend_over_time(_sample_frame(), freq="D", department="Sales")

    assert result["Count"].sum() == 2
    assert len(result) == 1


def test_trend_over_time_can_group_by_status():
    result = a.trend_over_time(_sample_frame(), freq="D", group_column="Status")

    assert list(result.columns) == ["Period", "Status", "Count"]
    assert result.loc[result["Status"] == "Active", "Count"].sum() == 3


def test_filter_analytics_frame_filters_department_and_status():
    result = a.filter_analytics_frame(
        _sample_frame(), department="Engineering", status="Active"
    )

    assert len(result) == 1
    assert result.iloc[0]["Candidate ID"] == "HF-CAND-001"


def test_interviewer_performance_returns_summary_and_correlation():
    result = a.interviewer_performance(_interview_frame())

    assert set(result) == {"summary", "rating_selection_correlation"}
    summary = result["summary"]

    assert list(summary.columns) == [
        "Interviewer",
        "Interview Count",
        "Average Rating",
        "Selected Count",
        "Selection Rate",
    ]
    assert summary.loc[summary["Interviewer"] == "Aisha Sharma", "Average Rating"].iloc[0] == 4.5
    assert summary.loc[summary["Interviewer"] == "Aisha Sharma", "Selection Rate"].iloc[0] == 1.0
    assert summary.loc[summary["Interviewer"] == "Daniel Lewis", "Selection Rate"].iloc[0] == 0.0
    assert not math.isnan(result["rating_selection_correlation"])
    assert result["rating_selection_correlation"] > 0


def test_summarize_recruitment_metrics_returns_all_sections():
    summary = a.summarize_recruitment_metrics(_sample_frame())

    assert set(summary) == {
        "department_breakdown",
        "outcome_distribution",
        "trend_over_time",
    }
    assert not summary["department_breakdown"].empty
    assert not summary["outcome_distribution"].empty
    assert not summary["trend_over_time"].empty


def test_summarize_recruitment_metrics_accepts_filters():
    summary = a.summarize_recruitment_metrics(
        _sample_frame(), department="Sales", status="Active"
    )

    assert summary["department_breakdown"].iloc[0]["Department"] == "Sales"
    assert summary["department_breakdown"].iloc[0]["Count"] == 1
    assert summary["outcome_distribution"].iloc[0]["Count"] == 1
