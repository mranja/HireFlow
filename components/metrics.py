"""Reusable KPI card components for HireFlow Analytics."""

from __future__ import annotations

from typing import Any, Sequence

import streamlit as st


def _apply_metrics_style() -> None:
    """Inject shared styles for KPI cards."""
    st.markdown(
        """
        <style>
        .hf-kpi-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 1rem 1rem 1.1rem;
            min-height: 165px;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04);
        }
        .hf-kpi-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            border-radius: 12px;
            background: rgba(37, 99, 235, 0.08);
            color: #2563eb;
            font-size: 1.1rem;
            margin-bottom: 0.7rem;
        }
        .hf-kpi-title {
            color: #101828;
            font-size: 0.95rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }
        .hf-kpi-subtitle {
            color: #475467;
            font-size: 0.9rem;
            line-height: 1.5;
            margin-top: 0.35rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_card(
    title: str,
    value: str | int,
    icon: str,
    subtitle: str = "Waiting for backend integration.",
    trend_placeholder: str | None = None,
    status_color: str = "#2563eb",
) -> None:
    """Render a reusable KPI card with a placeholder-friendly layout."""
    _apply_metrics_style()

    with st.container():
        st.markdown(
            f"""
            <div class="hf-kpi-card" style="border-left: 4px solid {status_color};">
                <div class="hf-kpi-icon" style="background: {status_color}12; color: {status_color};">{icon}</div>
                <div class="hf-kpi-title">{title}</div>
                <div class="hf-kpi-subtitle">{subtitle}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.metric(
            label="",
            value=str(value),
            delta=trend_placeholder or "Awaiting data",
            delta_color="off",
        )


def render_kpi_grid(kpi_items: Sequence[dict[str, Any]], columns: int = 3) -> None:
    """Render a responsive grid of KPI cards from a sequence of dictionaries."""
    if not kpi_items:
        st.caption("No dashboard data available.")
        return

    card_columns = st.columns(columns, gap="large")
    for column, item in zip(card_columns, kpi_items):
        with column:
            render_kpi_card(
                title=str(item.get("title", "Metric")),
                value=str(item.get("value", "0")),
                icon=str(item.get("icon", "📊")),
                subtitle=str(item.get("subtitle", "Waiting for backend integration.")),
                trend_placeholder=str(item.get("trend_placeholder", "Awaiting data")),
                status_color=str(item.get("status_color", "#2563eb")),
            )
