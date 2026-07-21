"""Reusable dataframe pagination controls."""

from __future__ import annotations

from math import ceil
from typing import Any

import pandas as pd
import streamlit as st

PAGE_SIZE_OPTIONS = (5, 10, 20, 50)


def _clamp_page(page: int, total_pages: int) -> int:
    """Keep the active page inside the available page range."""
    return max(1, min(page, total_pages))


def _showing_text(start: int, end: int, total_rows: int) -> str:
    """Return the human-readable pagination summary."""
    if total_rows == 0:
        return "Showing 0-0 of 0 Candidates"
    return f"Showing {start + 1}-{end} of {total_rows} Candidates"


def paginate_dataframe(
    df: pd.DataFrame,
    page_key: str = "candidate_current_page",
    page_size_key: str = "candidate_page_size",
    page_size_options: tuple[int, ...] = PAGE_SIZE_OPTIONS,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Render pagination controls and return the active dataframe slice."""
    if not page_size_options:
        raise ValueError("page_size_options must include at least one value.")

    total_rows = len(df)
    default_size = page_size_options[1] if len(page_size_options) > 1 else page_size_options[0]

    if page_size_key not in st.session_state:
        st.session_state[page_size_key] = default_size
    if page_key not in st.session_state:
        st.session_state[page_key] = 1

    control_cols = st.columns([1.1, 1.25, 3.2, 0.9, 0.9])

    with control_cols[0]:
        page_size = st.selectbox(
            "Rows per page",
            options=list(page_size_options),
            key=page_size_key,
        )

    previous_page_size_key = f"{page_size_key}_previous"
    if st.session_state.get(previous_page_size_key) != page_size:
        st.session_state[previous_page_size_key] = page_size
        st.session_state[page_key] = 1

    total_pages = max(1, ceil(total_rows / int(page_size)))
    current_page = _clamp_page(int(st.session_state[page_key]), total_pages)
    st.session_state[page_key] = current_page

    start_index = (current_page - 1) * int(page_size)
    end_index = min(start_index + int(page_size), total_rows)
    page_df = df.iloc[start_index:end_index].copy()

    with control_cols[1]:
        st.write("")
        st.caption(f"Page {current_page} of {total_pages}")

    with control_cols[2]:
        st.write("")
        st.caption(_showing_text(start_index, end_index, total_rows))

    with control_cols[3]:
        st.write("")
        if st.button("Previous", disabled=current_page <= 1, width="stretch"):
            st.session_state[page_key] = current_page - 1
            st.rerun()

    with control_cols[4]:
        st.write("")
        if st.button("Next", disabled=current_page >= total_pages, width="stretch"):
            st.session_state[page_key] = current_page + 1
            st.rerun()

    metadata = {
        "current_page": current_page,
        "page_size": int(page_size),
        "total_pages": total_pages,
        "total_rows": total_rows,
        "start_index": start_index,
        "end_index": end_index,
    }
    return page_df, metadata
