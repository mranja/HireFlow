"""Shared constants for HireFlow Analytics."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATABASE_DIR = BASE_DIR / "database"

CANDIDATES_CSV_PATH = DATA_DIR / "candidates.csv"
SQLITE_DB_PATH = DATABASE_DIR / "hireflow.db"

CANDIDATE_COLUMNS = [
    "Candidate ID",
    "Name",
    "Email",
    "Phone",
    "Department",
    "Position",
    "Experience",
    "Current Stage",
    "Recruiter",
    "Applied Date",
    "Status",
    "Drop-off Reason",
]

DEPARTMENTS = [
    "Engineering",
    "Marketing",
    "Sales",
    "HR",
    "Finance",
]

STAGES = [
    "Applied",
    "Screening",
    "Assessment",
    "Technical",
    "HR",
    "Offer",
    "Accepted",
    "Joined",
]

POSITIONS = [
    "Frontend Developer",
    "Backend Developer",
    "QA Engineer",
    "Data Analyst",
    "UI Designer",
]

RECRUITERS = [
    "Aisha Sharma",
    "Daniel Lewis",
    "Maya Patel",
    "Noah Bennett",
    "Priya Nair",
]

STATUSES = [
    "Active",
    "On Hold",
    "Rejected",
    "Hired",
]

# Only meaningful once a candidate has left the pipeline (Status = Rejected,
# or Current Stage abandoned mid-funnel). Empty string means still active.
DROP_OFF_REASONS = [
    "Rejected",
    "Withdrawn",
    "Ghosted",
    "RoleCancelled",
]

ALL_FILTER_OPTION = "All"