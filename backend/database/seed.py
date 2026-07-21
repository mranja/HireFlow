"""Seed hireflow.db with realistic dummy data.

Run from the repo root:
    python -m HireFlow.backend.database.seed

The script is **idempotent**: rows whose primary key already exists are
skipped (INSERT OR IGNORE), so it is safe to re-run after the database has
been partially populated.

Seeded tables
-------------
candidates  – 20 rows spread across all 5 departments, covering every
              pipeline stage and every status/drop-off-reason combination.
interviews  – up to 2 rounds per candidate that has passed the Screening
              stage, keeping candidate_id referential integrity intact.
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from typing import Generator

from HireFlow.backend.database.interviews_db import INTERVIEWS_TABLE_SQL
from HireFlow.backend.database.database import CANDIDATES_TABLE_SQL, init_db
from HireFlow.backend.utils.constants import SQLITE_DB_PATH


# ---------------------------------------------------------------------------
# Connection helper (mirrors database.py so we avoid circular imports)
# ---------------------------------------------------------------------------

@contextmanager
def _conn() -> Generator[sqlite3.Connection, None, None]:
    SQLITE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Dummy candidates
# Each row maps 1-to-1 to the `candidates` table columns.
# We deliberately cover:
#   • all 5 departments
#   • every pipeline stage at least once
#   • all 4 statuses (Active / On Hold / Rejected / Hired)
#   • all 4 drop-off reasons (only on Rejected rows)
# ---------------------------------------------------------------------------

SEED_CANDIDATES: list[tuple] = [
    # (candidate_id, name, email, phone, department, position,
    #  experience, current_stage, recruiter, applied_date, status, drop_off_reason)

    # ── Engineering ──────────────────────────────────────────────────────────
    ("HF-CAND-001", "Aarav Mehta",      "aarav.mehta@example.com",
     "+91 98765 43210", "Engineering", "Backend Developer",
     4, "Technical",    "Aisha Sharma",  "2026-05-01", "Active",    ""),

    ("HF-CAND-002", "Neha Kapoor",      "neha.kapoor@example.com",
     "+91 98765 43211", "Engineering", "Frontend Developer",
     2, "Screening",    "Maya Patel",    "2026-05-03", "Active",    ""),

    ("HF-CAND-003", "Rohan Iyer",       "rohan.iyer@example.com",
     "+91 98765 43212", "Engineering", "QA Engineer",
     3, "Assessment",   "Daniel Lewis",  "2026-05-05", "Active",    ""),

    ("HF-CAND-004", "Ananya Das",       "ananya.das@example.com",
     "+91 98765 43213", "Engineering", "Full Stack Developer",
     5, "Offer",        "Priya Nair",    "2026-05-08", "Active",    ""),

    ("HF-CAND-005", "Vikram Singh",     "vikram.singh@example.com",
     "+91 98765 43214", "Engineering", "DevOps Engineer",
     7, "Joined",       "Aisha Sharma",  "2026-04-20", "Hired",     ""),

    ("HF-CAND-006", "Arjun Pillai",     "arjun.pillai@example.com",
     "+91 98765 43215", "Engineering", "Cloud Engineer",
     6, "Screening",    "Maya Patel",    "2026-05-10", "Rejected",  "Rejected"),

    # ── Marketing ────────────────────────────────────────────────────────────
    ("HF-CAND-007", "Sneha Rao",        "sneha.rao@example.com",
     "+91 98765 43216", "Marketing", "UI Designer",
     4, "HR",           "Noah Bennett",  "2026-05-12", "Active",    ""),

    ("HF-CAND-008", "Kavya Reddy",      "kavya.reddy@example.com",
     "+91 98765 43217", "Marketing", "Content Strategist",
     3, "Technical",    "Priya Nair",    "2026-05-14", "Active",    ""),

    ("HF-CAND-009", "Ritika Bose",      "ritika.bose@example.com",
     "+91 98765 43218", "Marketing", "Digital Marketing Specialist",
     5, "Applied",      "Noah Bennett",  "2026-05-16", "Rejected",  "Withdrawn"),

    ("HF-CAND-010", "Deepika Arora",    "deepika.arora@example.com",
     "+91 98765 43219", "Marketing", "Product Marketing Manager",
     6, "Accepted",     "Aisha Sharma",  "2026-04-28", "Hired",     ""),

    # ── Sales ─────────────────────────────────────────────────────────────────
    ("HF-CAND-011", "Karan Shah",       "karan.shah@example.com",
     "+91 98765 43220", "Sales", "Sales Executive",
     2, "Applied",      "Daniel Lewis",  "2026-05-18", "Active",    ""),

    ("HF-CAND-012", "Rahul Verma",      "rahul.verma@example.com",
     "+91 98765 43221", "Sales", "Business Development Executive",
     4, "HR",           "Priya Nair",    "2026-05-19", "Active",    ""),

    ("HF-CAND-013", "Sanjay Ramesh",    "sanjay.ramesh@example.com",
     "+91 98765 43222", "Sales", "Sales Executive",
     3, "Screening",    "Noah Bennett",  "2026-05-20", "Rejected",  "Ghosted"),

    ("HF-CAND-014", "Rahul Chawla",     "rahul.chawla@example.com",
     "+91 98765 43223", "Sales", "Business Development Executive",
     5, "Offer",        "Aisha Sharma",  "2026-05-01", "On Hold",   ""),

    # ── HR ────────────────────────────────────────────────────────────────────
    ("HF-CAND-015", "Aishwarya Iyer",   "aishwarya.iyer@example.com",
     "+91 98765 43224", "HR", "HR Executive",
     3, "Applied",      "Maya Patel",    "2026-05-22", "Active",    ""),

    ("HF-CAND-016", "Diya Verma",       "diya.verma@example.com",
     "+91 98765 43225", "HR", "Talent Acquisition Specialist",
     4, "Assessment",   "Daniel Lewis",  "2026-05-23", "On Hold",   ""),

    ("HF-CAND-017", "Harini Venkatesh", "harini.venkatesh@example.com",
     "+91 98765 43226", "HR", "HR Executive",
     2, "Technical",    "Priya Nair",    "2026-05-24", "Rejected",  "RoleCancelled"),

    # ── Finance ───────────────────────────────────────────────────────────────
    ("HF-CAND-018", "Isha Menon",       "isha.menon@example.com",
     "+91 98765 43227", "Finance", "Data Analyst",
     6, "Technical",    "Aisha Sharma",  "2026-05-25", "Active",    ""),

    ("HF-CAND-019", "Meera Joshi",      "meera.joshi@example.com",
     "+91 98765 43228", "Finance", "Backend Developer",
     8, "Joined",       "Noah Bennett",  "2026-04-15", "Hired",     ""),

    ("HF-CAND-020", "Nisha Thomas",     "nisha.thomas@example.com",
     "+91 98765 43229", "Finance", "Accounts Executive",
     4, "HR",           "Daniel Lewis",  "2026-05-27", "Active",    ""),
]


# ---------------------------------------------------------------------------
# Dummy interviews
# Only for candidates that have progressed past Applied/Screening so the
# data is logically consistent.
# ---------------------------------------------------------------------------

SEED_INTERVIEWS: list[tuple] = [
    # (interview_id, candidate_id, round, interviewer,
    #  rating, recommendation, comments, strengths, weaknesses, date, result)

    # HF-CAND-001 (Engineering / Backend)
    ("HF-INT-001", "HF-CAND-001", "Screening", "Maya Patel",
     4, "Hire",
     "Strong fundamentals in Python and system design.",
     "Problem-solving, communication",
     "Limited cloud experience",
     "2026-05-05", "Selected"),

    ("HF-INT-002", "HF-CAND-001", "Technical", "Daniel Lewis",
     3, "Hire",
     "Solved DSA problems with minor hints. Good attitude.",
     "Algorithmic thinking",
     "Needs more practice with SQL queries",
     "2026-05-12", "Selected"),

    # HF-CAND-003 (Engineering / QA)
    ("HF-INT-003", "HF-CAND-003", "Screening", "Aisha Sharma",
     5, "Strong Hire",
     "Exceptional knowledge of testing frameworks and CI pipelines.",
     "Automation expertise, attention to detail",
     "Slightly overqualified for the role",
     "2026-05-08", "Selected"),

    # HF-CAND-004 (Engineering / Full Stack)
    ("HF-INT-004", "HF-CAND-004", "Screening", "Priya Nair",
     4, "Hire",
     "Solid React and Node.js background.",
     "Versatility, delivery focus",
     "Documentation habits could improve",
     "2026-05-12", "Selected"),

    ("HF-INT-005", "HF-CAND-004", "Technical", "Maya Patel",
     4, "Hire",
     "Built a small feature end-to-end during the live coding session.",
     "Speed, code quality",
     "Test coverage was thin",
     "2026-05-18", "Selected"),

    # HF-CAND-005 (Engineering / DevOps – Hired)
    ("HF-INT-006", "HF-CAND-005", "Screening", "Daniel Lewis",
     5, "Strong Hire",
     "7 years of DevOps; mastered Kubernetes and Terraform.",
     "Infrastructure as Code, incident response",
     "Prefers individual work over pairing",
     "2026-04-23", "Selected"),

    ("HF-INT-007", "HF-CAND-005", "Technical", "Noah Bennett",
     5, "Strong Hire",
     "Designed a CI/CD pipeline live on the whiteboard — impressive.",
     "Architecture thinking, tooling depth",
     "None identified",
     "2026-04-29", "Selected"),

    # HF-CAND-006 (Engineering / Cloud – Rejected)
    ("HF-INT-008", "HF-CAND-006", "Screening", "Aisha Sharma",
     2, "No Hire",
     "Struggled to explain basic networking concepts.",
     "Enthusiasm, willingness to learn",
     "Insufficient cloud fundamentals",
     "2026-05-13", "Rejected"),

    # HF-CAND-007 (Marketing / UI Designer)
    ("HF-INT-009", "HF-CAND-007", "Screening", "Noah Bennett",
     4, "Hire",
     "Portfolio showed strong visual design skills.",
     "Aesthetics, user empathy",
     "Limited experience with design systems",
     "2026-05-15", "Selected"),

    ("HF-INT-010", "HF-CAND-007", "Technical", "Priya Nair",
     3, "Hire",
     "Redesigned a sample screen on the spot — acceptable output.",
     "Creativity, quick turnaround",
     "Prototype fidelity could be higher",
     "2026-05-20", "Selected"),

    # HF-CAND-008 (Marketing / Content Strategist)
    ("HF-INT-011", "HF-CAND-008", "Screening", "Maya Patel",
     4, "Hire",
     "Well-structured content calendar examples in portfolio.",
     "SEO awareness, storytelling",
     "B2B writing experience limited",
     "2026-05-17", "Selected"),

    # HF-CAND-010 (Marketing / Product Marketing – Hired)
    ("HF-INT-012", "HF-CAND-010", "Screening", "Aisha Sharma",
     5, "Strong Hire",
     "Led two successful product launches at previous company.",
     "GTM strategy, cross-functional collaboration",
     "None identified",
     "2026-05-01", "Selected"),

    ("HF-INT-013", "HF-CAND-010", "HR", "Daniel Lewis",
     5, "Strong Hire",
     "Culture fit is excellent; aligns with company values.",
     "Leadership, communication",
     "None identified",
     "2026-05-06", "Selected"),

    # HF-CAND-012 (Sales / BDE)
    ("HF-INT-014", "HF-CAND-012", "Screening", "Noah Bennett",
     3, "Hire",
     "Demonstrated strong pipeline management experience.",
     "Persistence, client relationship skills",
     "Needs coaching on enterprise selling",
     "2026-05-22", "Selected"),

    # HF-CAND-014 (Sales / BDE – On Hold)
    ("HF-INT-015", "HF-CAND-014", "Screening", "Priya Nair",
     4, "Hire",
     "Good closer; met quota for three consecutive quarters.",
     "Revenue focus, negotiation",
     "Role scope is under review — hence on hold",
     "2026-05-05", "Selected"),

    # HF-CAND-016 (HR / Talent Acquisition – On Hold)
    ("HF-INT-016", "HF-CAND-016", "Screening", "Maya Patel",
     3, "Hire",
     "Sourcing methodology is sound; ATS experience is good.",
     "Candidate experience, process efficiency",
     "Leadership hiring exposure limited",
     "2026-05-26", "Pending"),

    # HF-CAND-018 (Finance / Data Analyst)
    ("HF-INT-017", "HF-CAND-018", "Screening", "Daniel Lewis",
     4, "Hire",
     "Proficient in SQL and Tableau; built dashboards for a previous role.",
     "Data storytelling, attention to detail",
     "Python scripting skills are basic",
     "2026-05-28", "Selected"),

    ("HF-INT-018", "HF-CAND-018", "Technical", "Aisha Sharma",
     3, "Hire",
     "Completed the SQL case study with minor gaps in optimisation.",
     "Accuracy, business understanding",
     "Query performance tuning needs work",
     "2026-06-03", "Selected"),

    # HF-CAND-019 (Finance – Hired)
    ("HF-INT-019", "HF-CAND-019", "Screening", "Noah Bennett",
     5, "Strong Hire",
     "8 years of backend + financial systems — exactly what we need.",
     "Domain depth, reliability",
     "None",
     "2026-04-18", "Selected"),

    ("HF-INT-020", "HF-CAND-019", "HR", "Priya Nair",
     5, "Strong Hire",
     "Salary expectations align; start date confirmed.",
     "Professionalism, cultural fit",
     "None",
     "2026-04-25", "Selected"),

    # HF-CAND-020 (Finance / Accounts Executive)
    ("HF-INT-021", "HF-CAND-020", "Screening", "Maya Patel",
     4, "Hire",
     "Solid understanding of AP/AR and month-end close processes.",
     "Accuracy, ERP experience",
     "International accounting standards exposure limited",
     "2026-05-30", "Selected"),
]


# ---------------------------------------------------------------------------
# Insert helpers
# ---------------------------------------------------------------------------

def _seed_candidates(conn: sqlite3.Connection) -> tuple[int, int]:
    """Insert seed candidates; return (inserted, skipped) counts."""
    inserted = skipped = 0
    for row in SEED_CANDIDATES:
        cursor = conn.execute(
            """
            INSERT OR IGNORE INTO candidates
                (candidate_id, name, email, phone, department, position,
                 experience, current_stage, recruiter, applied_date,
                 status, drop_off_reason)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            row,
        )
        if cursor.rowcount:
            inserted += 1
        else:
            skipped += 1
    return inserted, skipped


def _seed_interviews(conn: sqlite3.Connection) -> tuple[int, int]:
    """Insert seed interviews; return (inserted, skipped) counts."""
    inserted = skipped = 0
    for row in SEED_INTERVIEWS:
        cursor = conn.execute(
            """
            INSERT OR IGNORE INTO interviews
                (interview_id, candidate_id, round, interviewer,
                 rating, recommendation, comments, strengths, weaknesses,
                 date, result)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            row,
        )
        if cursor.rowcount:
            inserted += 1
        else:
            skipped += 1
    return inserted, skipped


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def run_seed() -> None:
    """Initialise the DB and insert dummy data. Prints a summary."""
    # Ensure both tables exist
    init_db()
    with _conn() as conn:
        conn.execute(INTERVIEWS_TABLE_SQL)

    with _conn() as conn:
        c_ins, c_skip = _seed_candidates(conn)
        i_ins, i_skip = _seed_interviews(conn)

    print(
        f"[seed] candidates → {c_ins} inserted, {c_skip} skipped\n"
        f"[seed] interviews → {i_ins} inserted, {i_skip} skipped"
    )


if __name__ == "__main__":
    run_seed()
