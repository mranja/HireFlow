"""Reports page for HireFlow Analytics."""

from __future__ import annotations

import streamlit as st


def _apply_page_style() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            max-width: 1440px;
            padding-top: 1.5rem;
            padding-bottom: 2.5rem;
        }
        .hf-breadcrumb {
            color: #667085;
            font-size: 0.92rem;
            margin-bottom: 0.35rem;
        }
        .hf-page-title {
            color: #101828;
            font-size: 2.1rem;
            font-weight: 700;
            margin-bottom: 0.35rem;
        }
        .hf-page-subtitle {
            color: #475467;
            font-size: 1rem;
            margin-bottom: 1rem;
        }
        .hf-report-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 1.25rem;
            margin-bottom: 1rem;
        }
        .hf-report-title {
            color: #101828;
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        .hf-report-description {
            color: #475467;
            font-size: 0.95rem;
            line-height: 1.6;
            margin-bottom: 1rem;
        }
        .hf-button-disabled {
            background: #e2e8f0;
            border: none;
            border-radius: 8px;
            color: #475467;
            padding: 0.75rem 1rem;
            cursor: not-allowed;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_header() -> None:
    st.markdown('<div class="hf-breadcrumb">Dashboard &gt; Reports</div>', unsafe_allow_html=True)
    st.markdown('<div class="hf-page-title">Reports</div>', unsafe_allow_html=True)
    st.markdown(
        (
            '<div class="hf-page-subtitle">'
            'Report exports and insights will be enabled once backend reporting data is available.'
            '</div>'
        ),
        unsafe_allow_html=True,
    )


def render_page() -> None:
    _apply_page_style()
    _render_header()

    st.info("No report data available. Report generation will appear after backend integration.")

    for title, details in [
        ("Candidate Pipeline Report", "Summarize candidate progress and stage performance."),
        ("Interview Feedback Report", "Review interview outcomes and ratings once available."),
        ("Department Hiring Report", "Track department-level hiring trends and capacity."),
    ]:
        st.markdown(
            f'<div class="hf-report-card">'
            f'<div class="hf-report-title">{title}</div>'
            f'<div class="hf-report-description">{details}</div>'
            '<div class="hf-button-disabled">Export report</div>'
            '</div>',
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    st.set_page_config(page_title="Reports | HireFlow Analytics", layout="wide")
    render_page()
