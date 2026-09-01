"""
Application-wide constants for the AI Interview Coach platform.
"""

# ──────────────────────────────────────────────
# File Upload
# ──────────────────────────────────────────────
ALLOWED_RESUME_EXTENSIONS = {"pdf", "docx"}
ALLOWED_AUDIO_EXTENSIONS = {"wav", "mp3", "ogg", "webm"}
ALLOWED_VIDEO_EXTENSIONS = {"mp4", "webm"}
ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_FILE_SIZE_BYTES = 16 * 1024 * 1024  # 16 MB

# ──────────────────────────────────────────────
# Interview
# ──────────────────────────────────────────────
INTERVIEW_TYPES = ["hr", "technical", "coding", "behavioral", "system_design"]
DIFFICULTY_LEVELS = ["easy", "medium", "hard"]
MAX_INTERVIEW_QUESTIONS = 20

# ──────────────────────────────────────────────
# Scoring
# ──────────────────────────────────────────────
SCORE_MAX = 100
SCORE_PASS_THRESHOLD = 60
ATS_SCORE_WEIGHTS = {
    "keywords": 0.40,
    "format": 0.20,
    "experience": 0.20,
    "education": 0.10,
    "skills": 0.10,
}

# ──────────────────────────────────────────────
# Career / Roles
# ──────────────────────────────────────────────
CAREER_ROLES = [
    "AI Engineer",
    "Machine Learning Engineer",
    "Data Scientist",
    "Data Analyst",
    "Software Engineer",
    "Full Stack Developer",
    "Cloud Engineer",
    "DevOps Engineer",
    "Cybersecurity Engineer",
]

# ──────────────────────────────────────────────
# Pagination
# ──────────────────────────────────────────────
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

# ──────────────────────────────────────────────
# JWT
# ──────────────────────────────────────────────
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 24

# ──────────────────────────────────────────────
# Report types
# ──────────────────────────────────────────────
REPORT_TYPES = [
    "intelligence_dossier",
    "readiness_report",
    "skill_gap_report",
    "job_application_strategy",
]
