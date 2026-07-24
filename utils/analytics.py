"""Aggregate analytics helpers for HireFlow Analytics."""

from __future__ import annotations

from collections.abc import Sequence
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


def _normalise_filter_values(value: str | Sequence[str] | None) -> list[str]:
	"""Normalize a single filter value or a multi-select into text values."""
	if value is None:
		return []

	if isinstance(value, str):
		cleaned = value.strip()
		if not cleaned or cleaned == ALL_FILTER_OPTION:
			return []
		return [cleaned]

	normalised = []
	for item in value:
		cleaned = str(item).strip()
		if cleaned and cleaned != ALL_FILTER_OPTION:
			normalised.append(cleaned)
	return normalised


def _filter_text_column(
	frame: pd.DataFrame,
	column: str,
	value: str | Sequence[str] | None,
) -> pd.DataFrame:
	"""Filter a frame by text values when the requested column exists."""
	values = _normalise_filter_values(value)
	if not values or column not in frame.columns:
		return frame

	text_values = _normalise_text_series(frame[column])
	return frame.loc[text_values.isin(values)]


def _filter_date_range(
	frame: pd.DataFrame,
	date_column: str,
	start_date: str | None = None,
	end_date: str | None = None,
) -> pd.DataFrame:
	"""Filter a frame by a date range when the requested column exists."""
	if date_column not in frame.columns or (start_date is None and end_date is None):
		return frame

	parsed_dates = pd.to_datetime(frame[date_column], errors="coerce")
	mask = parsed_dates.notna()

	if start_date:
		mask &= parsed_dates >= pd.to_datetime(start_date, errors="coerce")
	if end_date:
		mask &= parsed_dates <= pd.to_datetime(end_date, errors="coerce")

	filtered = frame.loc[mask].copy()
	filtered[date_column] = parsed_dates.loc[mask]
	return filtered


def _apply_analytics_filters(
	frame: pd.DataFrame,
	*,
	department: str | Sequence[str] | None = ALL_FILTER_OPTION,
	status: str | Sequence[str] | None = ALL_FILTER_OPTION,
	recruiter: str | Sequence[str] | None = ALL_FILTER_OPTION,
	interviewer: str | Sequence[str] | None = ALL_FILTER_OPTION,
	stage: str | Sequence[str] | None = ALL_FILTER_OPTION,
	result: str | Sequence[str] | None = ALL_FILTER_OPTION,
	date_column: str | None = None,
	start_date: str | None = None,
	end_date: str | None = None,
) -> pd.DataFrame:
	"""Apply the common analytics filters in a single Pandas pass."""
	filtered = frame.copy()
	filtered = _filter_text_column(filtered, "Department", department)
	filtered = _filter_text_column(filtered, "Status", status)
	filtered = _filter_text_column(filtered, "Recruiter", recruiter)
	filtered = _filter_text_column(filtered, "Interviewer", interviewer)
	filtered = _filter_text_column(filtered, "Current Stage", stage)
	filtered = _filter_text_column(filtered, "Result", result)

	if date_column:
		filtered = _filter_date_range(filtered, date_column, start_date, end_date)

	return filtered.reset_index(drop=True)


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
	*,
	department: str | Sequence[str] | None = ALL_FILTER_OPTION,
	status: str | Sequence[str] | None = ALL_FILTER_OPTION,
	recruiter: str | Sequence[str] | None = ALL_FILTER_OPTION,
) -> pd.DataFrame:
	"""Return department-level counts or summed values for dashboard charts."""
	frame = _apply_analytics_filters(
		_ensure_dataframe(df),
		department=department,
		status=status,
		recruiter=recruiter,
	)
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


def compare_departments(
	df: pd.DataFrame,
	left_department: str | None = None,
	right_department: str | None = None,
	department_column: str = "Department",
	value_column: str | None = None,
	*,
	department: str | Sequence[str] | None = ALL_FILTER_OPTION,
	status: str | Sequence[str] | None = ALL_FILTER_OPTION,
	recruiter: str | Sequence[str] | None = ALL_FILTER_OPTION,
) -> pd.DataFrame:
	"""Compare two departments side-by-side using the chosen metric."""
	breakdown = department_breakdown(
		df,
		department_column=department_column,
		value_column=value_column,
		department=department,
		status=status,
		recruiter=recruiter,
	)
	if breakdown.empty:
		return pd.DataFrame(columns=["Department", "Metric", "Share", "Delta vs Baseline"])

	metric_column = breakdown.columns[-1]
	ordered_departments = breakdown["Department"].tolist()

	if left_department is None:
		left_department = ordered_departments[0]
	if right_department is None:
		right_department = ordered_departments[1] if len(ordered_departments) > 1 else None

	selected_departments = [department for department in [left_department, right_department] if department]
	if not selected_departments:
		return pd.DataFrame(columns=["Department", "Metric", "Share", "Delta vs Baseline"])

	comparison = breakdown.loc[breakdown["Department"].isin(selected_departments)].copy()
	comparison = comparison.set_index("Department").reindex(selected_departments).dropna(how="all")
	if comparison.empty:
		return pd.DataFrame(columns=["Department", "Metric", "Share", "Delta vs Baseline"])

	comparison = comparison.reset_index()
	comparison = comparison.rename(columns={metric_column: "Metric"})
	total_metric = comparison["Metric"].sum()
	comparison["Share"] = np.where(total_metric > 0, comparison["Metric"] / total_metric, 0.0)
	comparison["Delta vs Baseline"] = comparison["Metric"] - comparison.loc[0, "Metric"]
	return comparison[["Department", "Metric", "Share", "Delta vs Baseline"]]


def outcome_distribution(
	df: pd.DataFrame,
	outcome_column: str = "Status",
	normalize: bool = False,
	*,
	department: str | Sequence[str] | None = ALL_FILTER_OPTION,
	status: str | Sequence[str] | None = ALL_FILTER_OPTION,
	recruiter: str | Sequence[str] | None = ALL_FILTER_OPTION,
	interviewer: str | Sequence[str] | None = ALL_FILTER_OPTION,
) -> pd.DataFrame:
	"""Return status/result distribution for pie or bar charts."""
	frame = _apply_analytics_filters(
		_ensure_dataframe(df),
		department=department,
		status=status,
		recruiter=recruiter,
		interviewer=interviewer,
	)
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
	*,
	department: str | Sequence[str] | None = ALL_FILTER_OPTION,
	status: str | Sequence[str] | None = ALL_FILTER_OPTION,
	recruiter: str | Sequence[str] | None = ALL_FILTER_OPTION,
	interviewer: str | Sequence[str] | None = ALL_FILTER_OPTION,
	start_date: str | None = None,
	end_date: str | None = None,
) -> pd.DataFrame:
	"""Return a time series trend suitable for line charts."""
	frame = _apply_analytics_filters(
		_ensure_dataframe(df),
		department=department,
		status=status,
		recruiter=recruiter,
		interviewer=interviewer,
		date_column=date_column,
		start_date=start_date,
		end_date=end_date,
	)

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


def interviewer_performance(
	df: pd.DataFrame,
	interviewer_column: str = "Interviewer",
	rating_column: str = "Rating",
	result_column: str = "Result",
	selected_value: str = "Selected",
	*,
	department: str | Sequence[str] | None = ALL_FILTER_OPTION,
	status: str | Sequence[str] | None = ALL_FILTER_OPTION,
	interviewer: str | Sequence[str] | None = ALL_FILTER_OPTION,
) -> dict[str, pd.DataFrame | float]:
	"""Summarize interviewer quality and correlate rating with selection rate."""
	frame = _apply_analytics_filters(
		_ensure_dataframe(df),
		department=department,
		status=status,
		interviewer=interviewer,
	)
	if interviewer_column not in frame.columns:
		return {
			"summary": pd.DataFrame(
				columns=["Interviewer", "Interview Count", "Average Rating", "Selected Count", "Selection Rate"]
			),
			"rating_selection_correlation": float("nan"),
		}

	working = frame.copy()
	working[interviewer_column] = _normalise_text_series(working[interviewer_column])
	working = working[working[interviewer_column] != ""]
	if working.empty:
		return {
			"summary": pd.DataFrame(
				columns=["Interviewer", "Interview Count", "Average Rating", "Selected Count", "Selection Rate"]
			),
			"rating_selection_correlation": float("nan"),
		}

	working[rating_column] = pd.to_numeric(working.get(rating_column), errors="coerce")
	working[rating_column] = working[rating_column].fillna(0)
	if result_column in working.columns:
		selected_mask = _normalise_text_series(working[result_column]).str.casefold() == selected_value.casefold()
	else:
		selected_mask = pd.Series(False, index=working.index)

	summary = (
		working.assign(_selected=selected_mask.astype(int))
		.groupby(interviewer_column, dropna=False)
		.agg(
			Interview_Count=(interviewer_column, "size"),
			Average_Rating=(rating_column, "mean"),
			Selected_Count=("_selected", "sum"),
		)
		.reset_index()
	)
	summary["Selection Rate"] = np.where(
		summary["Interview_Count"] > 0,
		summary["Selected_Count"] / summary["Interview_Count"],
		0.0,
	)
	summary = summary.rename(
		columns={
			interviewer_column: "Interviewer",
			"Interview_Count": "Interview Count",
			"Average_Rating": "Average Rating",
			"Selected_Count": "Selected Count",
		}
	).sort_values(by=["Average Rating", "Selection Rate"], ascending=False, kind="mergesort").reset_index(drop=True)

	if len(summary) >= 2 and summary["Average Rating"].nunique() > 1 and summary["Selection Rate"].nunique() > 1:
		correlation = float(summary["Average Rating"].corr(summary["Selection Rate"]))
	else:
		correlation = float("nan")

	return {
		"summary": summary,
		"rating_selection_correlation": correlation,
	}


def summarize_recruitment_metrics(
	df: pd.DataFrame,
	*,
	department: str | Sequence[str] | None = ALL_FILTER_OPTION,
	status: str | Sequence[str] | None = ALL_FILTER_OPTION,
	recruiter: str | Sequence[str] | None = ALL_FILTER_OPTION,
) -> dict[str, pd.DataFrame]:
	"""Return the three core analytics breakdowns used by the dashboard."""
	frame = _ensure_dataframe(df)

	return {
		"department_breakdown": department_breakdown(
			frame,
			department=department,
			status=status,
			recruiter=recruiter,
		),
		"outcome_distribution": outcome_distribution(
			frame,
			department=department,
			status=status,
			recruiter=recruiter,
		),
		"trend_over_time": trend_over_time(
			frame,
			department=department,
			status=status,
			recruiter=recruiter,
		),
	}


def filter_analytics_frame(
	df: pd.DataFrame,
	department: str | Sequence[str] | None = ALL_FILTER_OPTION,
	status: str | Sequence[str] | None = ALL_FILTER_OPTION,
	recruiter: str | Sequence[str] | None = ALL_FILTER_OPTION,
	interviewer: str | Sequence[str] | None = ALL_FILTER_OPTION,
	stage: str | Sequence[str] | None = ALL_FILTER_OPTION,
	result: str | Sequence[str] | None = ALL_FILTER_OPTION,
) -> pd.DataFrame:
	"""Filter an analytics dataframe using the common dashboard filters."""
	return _apply_analytics_filters(
		_ensure_dataframe(df),
		department=department,
		status=status,
		recruiter=recruiter,
		interviewer=interviewer,
		stage=stage,
		result=result,
	)
