"""Reusable candidate search and filtering helpers."""

from __future__ import annotations

from collections.abc import Iterable
import re

import pandas as pd

SEARCHABLE_COLUMNS = ("Name", "Email", "Phone", "Position")


def search_candidates(df: pd.DataFrame, keyword: str) -> pd.DataFrame:
    """Search candidates by name, email, phone, or position."""
    search_term = str(keyword or "").strip()
    if not search_term:
        return df.copy()

    available_columns = [column for column in SEARCHABLE_COLUMNS if column in df.columns]
    if not available_columns:
        return df.iloc[0:0].copy()

    escaped_term = re.escape(search_term)
    matches = pd.Series(False, index=df.index)

    for column in available_columns:
        column_matches = (
            df[column]
            .astype("string")
            .fillna("")
            .str.contains(escaped_term, case=False, regex=True)
        )
        matches = matches | column_matches

    return df.loc[matches].copy()


def _to_int(value: object, default: int = 0) -> int:
    """Convert scalar values to int without leaking NaN into filters."""
    numeric_value = pd.to_numeric(value, errors="coerce")
    if pd.isna(numeric_value):
        return default
    return int(numeric_value)


def get_experience_bucket(experience: object) -> str:
    """Map numeric experience to a candidate filter band."""
    years = _to_int(experience)
    if years <= 1:
        return "0-1 Years"
    if years <= 4:
        return "2-4 Years"
    if years <= 8:
        return "5-8 Years"
    return "8+ Years"


def _selected_values(values: Iterable[str] | None) -> list[str]:
    """Return cleaned selected filter values."""
    if values is None:
        return []
    return [str(value) for value in values if str(value).strip()]


def filter_candidates(
    df: pd.DataFrame,
    departments: Iterable[str] | None = None,
    stages: Iterable[str] | None = None,
    experience_bands: Iterable[str] | None = None,
    statuses: Iterable[str] | None = None,
) -> pd.DataFrame:
    """Filter candidates by department, stage, experience, and status."""
    filtered = df.copy()
    selected_departments = _selected_values(departments)
    selected_stages = _selected_values(stages)
    selected_experience = _selected_values(experience_bands)
    selected_statuses = _selected_values(statuses)

    if selected_experience and "Experience Band" not in filtered.columns:
        filtered["Experience Band"] = filtered["Experience"].map(
            get_experience_bucket
        )

    if selected_departments:
        filtered = filtered[filtered["Department"].isin(selected_departments)]

    if selected_stages:
        filtered = filtered[filtered["Current Stage"].isin(selected_stages)]

    if selected_experience:
        filtered = filtered[filtered["Experience Band"].isin(selected_experience)]

    if selected_statuses:
        filtered = filtered[filtered["Status"].isin(selected_statuses)]

    return filtered.copy()
