"""Reusable table components for HireFlow Analytics."""

from __future__ import annotations

import pandas as pd
import streamlit as st


def candidate_table(df: pd.DataFrame) -> None:
    """Display the candidate table with responsive sizing and useful labels."""
    st.dataframe(
        df,
        hide_index=True,
        width="stretch",
        height=520,
        column_config={
            "Candidate ID": st.column_config.TextColumn("Candidate ID"),
            "Name": st.column_config.TextColumn("Name"),
            "Email": st.column_config.TextColumn("Email"),
            "Phone": st.column_config.TextColumn("Phone"),
            "Department": st.column_config.TextColumn("Department"),
            "Position": st.column_config.TextColumn("Position"),
            "Experience": st.column_config.NumberColumn(
                "Experience",
                help="Years of professional experience",
                format="%d yrs",
            ),
            "Current Stage": st.column_config.TextColumn("Current Stage"),
            "Recruiter": st.column_config.TextColumn("Recruiter"),
            "Applied Date": st.column_config.DateColumn("Applied Date"),
            "Status": st.column_config.TextColumn("Status"),
        },
    )
