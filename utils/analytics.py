"""Aggregate analytics helpers for HireFlow Analytics."""

from __future__ import annotations

from typing import Final

import numpy as np
import pandas as pd

from utils.constants import ALL_FILTER_OPTION


_DATE_COLUMNS: Final[tuple[str, ...]] = ("Applied Date", "Date")


def _ensure_dataframe(df: pd.DataFrame) -> pd.DataFrame:
	"""Return a defensive copy so callers keep their original frame intact."""
	if df is None:
		return pd.DataFrame()
	return df.copy()


def _normalise_text_series(series: pd.Series) -> pd.Series:
	"""Convert a series to clean string values with missing data removed."""
	return series.fillna("").astype(str).str.strip()


def _add_period_column(df: pd.DataFrame, date_column: str, freq: str) -> pd.DataFrame:
	"""Attach a normalized period column used for trend aggregation."""
	frame = df.copy()
	parsed_dates = pd.to_datetime(frame[date_column], errors="coerce")
	frame = frame.loc[parsed_dates.notna()].copy()
	frame[date_column] = parsed_dates.loc[parsed_dates.notna()]

	if freq == "M":
		frame["Period"] = frame[date_column].dt.to_period("M").dt.to_timestamp()
	elif freq == "W":
		frame["Period"] = frame[date_column].dt.to_period("W").dt.start_time
	else:
		frame["Period"] = frame[date_column].dt.floor("D")

	return frame


def department_breakdown(
	df: pd.DataFrame,
	department_column: str = "Department",
	value_column: str | None = None,
) -> pd.DataFrame:
	"""Return department-level counts or summed values for dashboard charts."""
	frame = _ensure_dataframe(df)
	if department_column not in frame.columns:
		return pd.DataFrame(columns=["Department", "Count"])

	if value_column and value_column in frame.columns:
		values = pd.to_numeric(frame[value_column], errors="coerce").fillna(0)
		breakdown = (
			frame.assign(**{value_column: values})
			.groupby(department_column, dropna=False)[value_column]
			.sum()
			.reset_index(name="Value")
		)
	else:
		breakdown = (
			frame.groupby(department_column, dropna=False)
			.size()
			.reset_index(name="Count")
		)

	breakdown[department_column] = _normalise_text_series(breakdown[department_column])
	breakdown = breakdown[breakdown[department_column] != ""]
	breakdown = breakdown.sort_values(
		by=breakdown.columns[-1], ascending=False, kind="mergesort"
	).reset_index(drop=True)
	return breakdown.rename(columns={department_column: "Department"})


def outcome_distribution(
	df: pd.DataFrame,
	outcome_column: str = "Status",
	normalize: bool = False,
) -> pd.DataFrame:
	"""Return status/result distribution for pie or bar charts."""
	frame = _ensure_dataframe(df)
	if outcome_column not in frame.columns:
		return pd.DataFrame(columns=[outcome_column, "Count"])

	outcomes = _normalise_text_series(frame[outcome_column])
	outcomes = outcomes[outcomes != ""]
	if outcomes.empty:
		return pd.DataFrame(columns=[outcome_column, "Count"])

	distribution = outcomes.value_counts(dropna=False).rename_axis(outcome_column).reset_index(name="Count")
	distribution["Share"] = np.where(
		distribution["Count"].sum() > 0,
		distribution["Count"] / distribution["Count"].sum(),
		0.0,
	)

	if normalize:
		distribution["Count"] = distribution["Share"]

	distribution = distribution.sort_values(by="Count", ascending=False, kind="mergesort")
	return distribution.reset_index(drop=True)


def trend_over_time(
	df: pd.DataFrame,
	date_column: str = "Applied Date",
	freq: str = "M",
	group_column: str | None = None,
) -> pd.DataFrame:
	"""Return a time series trend suitable for line charts."""
	frame = _ensure_dataframe(df)

	if date_column not in frame.columns:
		for candidate_column in _DATE_COLUMNS:
			if candidate_column in frame.columns:
				date_column = candidate_column
				break
		else:
			return pd.DataFrame(columns=["Period", "Count"])

	if group_column and group_column in frame.columns:
		frame[group_column] = _normalise_text_series(frame[group_column])
		frame = frame[frame[group_column] != ""]

	frame = _add_period_column(frame, date_column, freq)
	if frame.empty:
		return pd.DataFrame(columns=["Period", "Count"])

	group_keys: list[str] = ["Period"]
	if group_column and group_column in frame.columns:
		group_keys.append(group_column)

	trend = (
		frame.groupby(group_keys, dropna=False)
		.size()
		.reset_index(name="Count")
		.sort_values(by=group_keys, kind="mergesort")
		.reset_index(drop=True)
	)

	if freq not in {"D", "W", "M"}:
		trend["Period"] = pd.to_datetime(trend["Period"])

	return trend


def summarize_recruitment_metrics(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
	"""Return the three core analytics breakdowns used by the dashboard."""
	frame = _ensure_dataframe(df)

	return {
		"department_breakdown": department_breakdown(frame),
		"outcome_distribution": outcome_distribution(frame),
		"trend_over_time": trend_over_time(frame),
	}


def filter_analytics_frame(
	df: pd.DataFrame,
	department: str = ALL_FILTER_OPTION,
	status: str = ALL_FILTER_OPTION,
) -> pd.DataFrame:
	"""Filter an analytics dataframe using the common dashboard filters."""
	frame = _ensure_dataframe(df)

	if department and department != ALL_FILTER_OPTION and "Department" in frame.columns:
		frame = frame.loc[_normalise_text_series(frame["Department"]) == department]

	if status and status != ALL_FILTER_OPTION and "Status" in frame.columns:
		frame = frame.loc[_normalise_text_series(frame["Status"]) == status]

	return frame.reset_index(drop=True)
