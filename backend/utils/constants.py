"""Shared constants for HireFlow Analytics."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]  # HireFlow root directory
DATA_DIR = BASE_DIR / "data"
DATABASE_DIR = BASE_DIR / "database"

CANDIDATES_CSV_PATH = DATA_DIR / "candidates.csv"
INTERVIEWS_CSV_PATH = DATA_DIR / "interviews.csv"
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

INTERVIEW_COLUMNS = [
    "Interview ID",
    "Candidate ID",
    "Round",
    "Interviewer",
    "Rating",
    "Recommendation",
    "Comments",
    "Strengths",
    "Weaknesses",
    "Date",
    "Result",
]

DEPARTMENTS = ["Engineering", "Marketing", "Sales", "HR", "Finance"]

STAGES = [
    "Applied", "Screening", "Assessment", "Technical",
    "HR", "Offer", "Accepted", "Joined",
]

# Subset of STAGES that actually involve an interview round.
INTERVIEW_ROUNDS = ["Screening", "Assessment", "Technical", "HR"]

POSITIONS = [
    "Frontend Developer", "Backend Developer", "QA Engineer",
    "Data Analyst", "UI Designer",
]

RECRUITERS = ["Aisha Sharma", "Daniel Lewis", "Maya Patel", "Noah Bennett", "Priya Nair"]

# Reusing the recruiter roster as the interviewer pool for now — same people
# can conduct interviews. Split into a dedicated INTERVIEWERS list later if
# the team needs interviewer != recruiter.
INTERVIEWERS = RECRUITERS

STATUSES = ["Active", "On Hold", "Rejected", "Hired"]

DROP_OFF_REASONS = ["Rejected", "Withdrawn", "Ghosted", "RoleCancelled"]

RECOMMENDATIONS = ["Strong Hire", "Hire", "No Hire", "Strong No Hire"]

INTERVIEW_RESULTS = ["Selected", "Rejected", "Pending"]

ALL_FILTER_OPTION = "All"