"""Database access placeholders for future SQLite integration."""

from __future__ import annotations

from typing import Any

import pandas as pd


def get_all_candidates() -> pd.DataFrame:
    """Return every candidate from SQLite when the database layer is enabled."""
    raise NotImplementedError("SQLite candidate retrieval is not implemented yet.")


def insert_candidate(candidate: dict[str, Any]) -> int:
    """Insert a candidate into SQLite and return the inserted row ID."""
    raise NotImplementedError("SQLite candidate insertion is not implemented yet.")


def update_candidate(candidate_id: str, updates: dict[str, Any]) -> None:
    """Update an existing candidate in SQLite."""
    raise NotImplementedError("SQLite candidate updates are not implemented yet.")


def delete_candidate(candidate_id: str) -> None:
    """Delete a candidate from SQLite."""
    raise NotImplementedError("SQLite candidate deletion is not implemented yet.")
