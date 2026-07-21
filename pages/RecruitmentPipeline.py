"""Recruitment Pipeline page for HireFlow Analytics."""

from __future__ import annotations

import streamlit as st

from components.pipeline import render_pipeline_page


def main() -> None:
    """Render the recruitment pipeline page."""
    st.title("Recruitment Pipeline")
    st.caption("Visualize the candidate hiring journey and pipeline progress.")

    render_pipeline_page()


if __name__ == "__main__":
<<<<<<< HEAD
    st.set_page_config(
        page_title="Recruitment Pipeline | HireFlow Analytics",
        layout="wide",
    )
    main()
    
=======
    main()
>>>>>>> 7f1d561fe854ff79ec4ca6fdf2bd11bb2e359dc2
