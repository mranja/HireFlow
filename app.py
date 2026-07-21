"""HireFlow Analytics Streamlit application entry point."""

from __future__ import annotations

import streamlit as st

from components.sidebar import render_sidebar
<<<<<<< HEAD
from pages import Analytics, Candidates, Dashboard, Departments, Interviews, RecruitmentPipeline, Reports

PAGE_ROUTES = {
    "Dashboard": Dashboard.render_page,
    "Candidates": Candidates.render_page,
    "Interviews": Interviews.render_page,
    "Departments": Departments.main,
    "Recruitment Pipeline": RecruitmentPipeline.main,
    "Analytics": Analytics.render_page,
    "Reports": Reports.render_page,
}


def main() -> None:
    """Render the main HireFlow Analytics application with page navigation."""
=======


def main() -> None:
    """Render the Streamlit application shell."""
>>>>>>> 7f1d561fe854ff79ec4ca6fdf2bd11bb2e359dc2
    st.set_page_config(
        page_title="HireFlow Analytics",
        layout="wide",
    )
<<<<<<< HEAD

    selected_page = render_sidebar()
    page_handler = PAGE_ROUTES.get(selected_page)
    if page_handler is None:
        st.error("The selected page is not available.")
        return

    page_handler()
=======
    render_sidebar()

    st.title("HireFlow Analytics")
    st.caption("Production-ready recruitment analytics built with Streamlit.")

    st.info("Open the Candidates page from the sidebar to manage candidate data.")
>>>>>>> 7f1d561fe854ff79ec4ca6fdf2bd11bb2e359dc2


if __name__ == "__main__":
    main()
