"""Reusable Plotly chart components for HireFlow Analytics."""

from __future__ import annotations

from typing import Any, Sequence

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DEFAULT_CHART_COLORS = ["#2563eb", "#10b981", "#f59e0b", "#8b5cf6", "#ef4444", "#0f766e"]


def _coerce_dataframe(data: Any) -> pd.DataFrame | None:
    """Convert supported data inputs into a pandas DataFrame safely."""
    if data is None:
        return None

    if isinstance(data, pd.DataFrame):
        return data.copy()

    if isinstance(data, dict):
        return pd.DataFrame([data])

    if isinstance(data, (list, tuple)):
        if not data:
            return pd.DataFrame()
        if isinstance(data[0], dict):
            return pd.DataFrame(data)
        return pd.DataFrame({"value": list(data)})

    return None


def _render_empty_placeholder(message: str = "No chart data available.") -> None:
    """Render a professional empty-state message for charts."""
    st.info(message, icon="📊")


def _build_common_layout(title: str, x_axis_title: str | None = None, y_axis_title: str | None = None) -> dict[str, Any]:
    """Create a shared Plotly layout configuration for consistent styling."""
    return {
        "template": "plotly_white",
        "margin": dict(l=24, r=24, t=60, b=24),
        "paper_bgcolor": "white",
        "plot_bgcolor": "white",
        "title": {"text": title, "x": 0.05, "xanchor": "left", "font": {"size": 18, "family": "Inter, Arial, sans-serif"}},
        "font": {"family": "Inter, Arial, sans-serif", "size": 13, "color": "#334155"},
        "legend": {"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "left", "x": 0.0},
        "xaxis": {"title": x_axis_title or "", "showgrid": False, "zeroline": False},
        "yaxis": {"title": y_axis_title or "", "showgrid": True, "gridcolor": "#e2e8f0"},
    }


def render_bar_chart(
    data: Any,
    x_column: str | None,
    y_column: str | None,
    title: str = "Bar Chart",
    height: int = 350,
    color: str | None = None,
    orientation: str = "vertical",
    legend: bool = True,
    x_axis_title: str | None = None,
    y_axis_title: str | None = None,
) -> None:
    """Render a reusable vertical or horizontal bar chart."""
    dataframe = _coerce_dataframe(data)
    if dataframe is None or dataframe.empty:
        _render_empty_placeholder()
        return

    if not x_column or not y_column:
        _render_empty_placeholder("Chart configuration is incomplete.")
        return

    if x_column not in dataframe.columns or y_column not in dataframe.columns:
        _render_empty_placeholder("Required chart columns are missing.")
        return

    chart_frame = dataframe[[x_column, y_column]].dropna()
    if chart_frame.empty:
        _render_empty_placeholder("No chart data available for the selected columns.")
        return

    chart_frame = chart_frame.copy()
    chart_frame[y_column] = pd.to_numeric(chart_frame[y_column], errors="coerce")
    chart_frame = chart_frame.dropna(subset=[y_column])

    if chart_frame.empty:
        _render_empty_placeholder("No numeric values available for plotting.")
        return

    normalized_orientation = orientation.lower()
    horizontal = normalized_orientation in {"horizontal", "h", "horizontal-bar"}

    fig = go.Figure()
    trace = go.Bar(
        x=chart_frame[x_column] if not horizontal else chart_frame[y_column],
        y=chart_frame[y_column] if not horizontal else chart_frame[x_column],
        orientation="h" if horizontal else "v",
        marker=dict(color=color or DEFAULT_CHART_COLORS[0], line=dict(color="rgba(15, 23, 42, 0.08)", width=1)),
        name=title,
        hovertemplate="<b>%{x}</b><br>%{y}<extra></extra>",
    )
    fig.add_trace(trace)

    layout = _build_common_layout(title, x_axis_title=x_axis_title, y_axis_title=y_axis_title)
    layout["showlegend"] = legend
    fig.update_layout(**layout)

    st.plotly_chart(fig, use_container_width=True, height=height)


def render_pie_chart(
    data: Any,
    labels_column: str | None,
    values_column: str | None,
    title: str = "Pie Chart",
    height: int = 380,
    legend: bool = True,
    show_percentages: bool = True,
    color_sequence: Sequence[str] | None = None,
) -> None:
    """Render a reusable pie chart with percentage labels and legend support."""
    dataframe = _coerce_dataframe(data)
    if dataframe is None or dataframe.empty:
        _render_empty_placeholder()
        return

    if not labels_column or not values_column:
        _render_empty_placeholder("Pie chart configuration is incomplete.")
        return

    if labels_column not in dataframe.columns or values_column not in dataframe.columns:
        _render_empty_placeholder("Required pie chart columns are missing.")
        return

    chart_frame = dataframe[[labels_column, values_column]].dropna()
    if chart_frame.empty:
        _render_empty_placeholder("No pie chart data available.")
        return

    chart_frame[values_column] = pd.to_numeric(chart_frame[values_column], errors="coerce")
    chart_frame = chart_frame.dropna(subset=[values_column])
    if chart_frame.empty:
        _render_empty_placeholder("No numeric values available for the pie chart.")
        return

    fig = go.Figure(
        data=[
            go.Pie(
                labels=chart_frame[labels_column].astype(str),
                values=chart_frame[values_column],
                hole=0,
                marker=dict(colors=color_sequence or DEFAULT_CHART_COLORS),
                textinfo="percent+label" if show_percentages else "label+value",
                hovertemplate="<b>%{label}</b><br>%{value}<br>%{percent}<extra></extra>",
            )
        ]
    )

    layout = _build_common_layout(title)
    layout["showlegend"] = legend
    layout["height"] = height
    fig.update_layout(**layout)

    st.plotly_chart(fig, use_container_width=True, height=height)


def render_line_chart(
    data: Any,
    x_column: str | None,
    y_column: str | Sequence[str] | None,
    title: str = "Line Chart",
    height: int = 350,
    color: str | Sequence[str] | None = None,
    markers: bool = True,
    legend: bool = True,
    x_axis_title: str | None = None,
    y_axis_title: str | None = None,
) -> None:
    """Render a reusable multi-series line chart."""
    dataframe = _coerce_dataframe(data)
    if dataframe is None or dataframe.empty:
        _render_empty_placeholder()
        return

    if not x_column or not y_column:
        _render_empty_placeholder("Line chart configuration is incomplete.")
        return

    if x_column not in dataframe.columns:
        _render_empty_placeholder("The x-axis column is missing.")
        return

    if isinstance(y_column, str):
        series_columns = [y_column]
    else:
        series_columns = [column for column in y_column if isinstance(column, str)]

    if not series_columns:
        _render_empty_placeholder("No value columns were provided for the line chart.")
        return

    missing_columns = [column for column in series_columns if column not in dataframe.columns]
    if missing_columns:
        _render_empty_placeholder("One or more line chart columns are missing.")
        return

    fig = go.Figure()
    colors = list(color) if isinstance(color, Sequence) and not isinstance(color, str) else [color or DEFAULT_CHART_COLORS[0]]

    for index, column_name in enumerate(series_columns):
        chart_frame = dataframe[[x_column, column_name]].dropna()
        if chart_frame.empty:
            continue

        chart_frame[column_name] = pd.to_numeric(chart_frame[column_name], errors="coerce")
        chart_frame = chart_frame.dropna(subset=[column_name])
        if chart_frame.empty:
            continue

        trace_color = colors[index % len(colors)] if index < len(colors) else DEFAULT_CHART_COLORS[index % len(DEFAULT_CHART_COLORS)]
        fig.add_trace(
            go.Scatter(
                x=chart_frame[x_column],
                y=chart_frame[column_name],
                mode="lines+markers" if markers else "lines",
                name=column_name,
                line=dict(color=trace_color, width=2.5),
                marker=dict(color=trace_color, size=7),
                hovertemplate="<b>%{x}</b><br>%{y}<extra></extra>",
            )
        )

    if len(fig.data) == 0:
        _render_empty_placeholder("No numeric values available for the line chart.")
        return

    layout = _build_common_layout(title, x_axis_title=x_axis_title, y_axis_title=y_axis_title)
    layout["showlegend"] = legend
    layout["height"] = height
    fig.update_layout(**layout)

    st.plotly_chart(fig, use_container_width=True, height=height)
