"""
Input validators for the AI Interview Coach platform.

Provides reusable validation functions for user-submitted data,
supplementing WTForms validators at the service and API layer.
"""
import re
import os
from urllib.parse import urlparse


# ──────────────────────────────────────────────
# String validators
# ──────────────────────────────────────────────

def is_valid_email(email: str) -> bool:
    """Return True if *email* matches a basic RFC-5322-style pattern."""
    if not email or not isinstance(email, str):
        return False
    pattern = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email.strip()))


def is_non_empty_string(value: str, min_length: int = 1, max_length: int = 10_000) -> bool:
    """Return True if *value* is a non-empty string within length bounds."""
    if not isinstance(value, str):
        return False
    stripped = value.strip()
    return min_length <= len(stripped) <= max_length


def is_alphanumeric_slug(value: str, max_length: int = 100) -> bool:
    """Return True if *value* contains only letters, digits, hyphens, or underscores."""
    if not isinstance(value, str):
        return False
    return bool(re.match(r"^[a-zA-Z0-9_\-]{1,%d}$" % max_length, value))


# ──────────────────────────────────────────────
# Numeric validators
# ──────────────────────────────────────────────

def is_positive_integer(value) -> bool:
    """Return True if *value* is an integer greater than zero."""
    try:
        return int(value) > 0
    except (TypeError, ValueError):
        return False


def is_score(value) -> bool:
    """Return True if *value* is a number in the range [0, 100]."""
    try:
        score = float(value)
        return 0.0 <= score <= 100.0
    except (TypeError, ValueError):
        return False


# ──────────────────────────────────────────────
# File validators
# ──────────────────────────────────────────────

def is_allowed_extension(filename: str, allowed: set[str]) -> bool:
    """Return True if *filename* has an extension in *allowed*."""
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[-1].lower()
    return ext in allowed


def is_safe_filename(filename: str) -> bool:
    """Return True if *filename* does not contain path traversal sequences."""
    return (
        isinstance(filename, str)
        and ".." not in filename
        and "/" not in filename
        and "\\" not in filename
        and len(filename) <= 255
    )


# ──────────────────────────────────────────────
# URL validators
# ──────────────────────────────────────────────

def is_valid_url(url: str, allowed_schemes: tuple = ("http", "https")) -> bool:
    """Return True if *url* is a well-formed URL with an allowed scheme."""
    try:
        parsed = urlparse(url)
        return parsed.scheme in allowed_schemes and bool(parsed.netloc)
    except Exception:
        return False


def is_valid_github_url(url: str) -> bool:
    """Return True if *url* is a valid GitHub profile or repository URL."""
    return is_valid_url(url) and "github.com" in urlparse(url).netloc


def is_valid_linkedin_url(url: str) -> bool:
    """Return True if *url* is a valid LinkedIn profile URL."""
    return is_valid_url(url) and "linkedin.com" in urlparse(url).netloc


# ──────────────────────────────────────────────
# Interview / domain validators
# ──────────────────────────────────────────────

VALID_INTERVIEW_TYPES = {"hr", "technical", "coding", "behavioral", "system_design"}
VALID_DIFFICULTY_LEVELS = {"easy", "medium", "hard"}


def is_valid_interview_type(value: str) -> bool:
    """Return True if *value* is a recognised interview type."""
    return isinstance(value, str) and value.lower() in VALID_INTERVIEW_TYPES


def is_valid_difficulty(value: str) -> bool:
    """Return True if *value* is a recognised difficulty level."""
    return isinstance(value, str) and value.lower() in VALID_DIFFICULTY_LEVELS
