"""Tests for aggregate analytics helpers."""

from __future__ import annotations

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


def test_department_breakdown_counts_rows():
    result = a.department_breakdown(_sample_frame())

    assert list(result.columns) == ["Department", "Count"]
    assert result.iloc[0]["Department"] == "Engineering"
    assert result.iloc[0]["Count"] == 2
    assert result.loc[result["Department"] == "Sales", "Count"].iloc[0] == 2


def test_outcome_distribution_returns_counts_and_share():
    result = a.outcome_distribution(_sample_frame())

    assert list(result.columns) == ["Status", "Count", "Share"]
    assert result.loc[result["Status"] == "Active", "Count"].iloc[0] == 3
    assert round(result["Share"].sum(), 6) == 1.0


def test_trend_over_time_groups_by_month():
    result = a.trend_over_time(_sample_frame(), freq="M")

    assert list(result.columns) == ["Period", "Count"]
    assert result["Count"].sum() == 5
    assert len(result) == 2


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
