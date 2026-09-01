"""
General-purpose helper utilities for the AI Interview Coach platform.
"""
import os
import re
import uuid
import hashlib
from datetime import datetime
from werkzeug.utils import secure_filename

from backend.utils.constants import (
    ALLOWED_RESUME_EXTENSIONS,
    ALLOWED_AUDIO_EXTENSIONS,
    ALLOWED_VIDEO_EXTENSIONS,
    ALLOWED_IMAGE_EXTENSIONS,
)


# ──────────────────────────────────────────────
# File helpers
# ──────────────────────────────────────────────

def allowed_file(filename: str, category: str = "resume") -> bool:
    """Return True if *filename* has an extension permitted for *category*."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    mapping = {
        "resume": ALLOWED_RESUME_EXTENSIONS,
        "audio": ALLOWED_AUDIO_EXTENSIONS,
        "video": ALLOWED_VIDEO_EXTENSIONS,
        "image": ALLOWED_IMAGE_EXTENSIONS,
    }
    return ext in mapping.get(category, set())


def generate_unique_filename(original_filename: str) -> str:
    """Prepend a UUID to *original_filename* to avoid collisions."""
    safe = secure_filename(original_filename)
    unique_id = uuid.uuid4().hex[:12]
    return f"{unique_id}_{safe}"


def get_file_size(filepath: str) -> int:
    """Return file size in bytes, or 0 if the file does not exist."""
    try:
        return os.path.getsize(filepath)
    except OSError:
        return 0


# ──────────────────────────────────────────────
# String helpers
# ──────────────────────────────────────────────

def sanitize_input(text: str, max_length: int = 1000) -> str:
    """Strip leading/trailing whitespace and truncate to *max_length* characters."""
    if not isinstance(text, str):
        return ""
    return text.strip()[:max_length]


def slugify(text: str) -> str:
    """Convert *text* to a URL-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return re.sub(r"^-+|-+$", "", text)


def truncate(text: str, max_length: int = 200, suffix: str = "…") -> str:
    """Truncate *text* to *max_length* characters, appending *suffix* if needed."""
    if not text or len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + suffix


# ──────────────────────────────────────────────
# Date / time helpers
# ──────────────────────────────────────────────

def format_datetime(dt: datetime, fmt: str = "%B %d, %Y %H:%M") -> str:
    """Return *dt* as a human-readable string, or empty string if *dt* is None."""
    if dt is None:
        return ""
    return dt.strftime(fmt)


def time_ago(dt: datetime) -> str:
    """Return a human-readable relative time string (e.g. '3 hours ago')."""
    if dt is None:
        return ""
    delta = datetime.utcnow() - dt
    seconds = int(delta.total_seconds())
    if seconds < 60:
        return "just now"
    if seconds < 3600:
        return f"{seconds // 60} minutes ago"
    if seconds < 86400:
        return f"{seconds // 3600} hours ago"
    if seconds < 2592000:
        return f"{delta.days} days ago"
    return format_datetime(dt, "%B %d, %Y")


# ──────────────────────────────────────────────
# Numeric / scoring helpers
# ──────────────────────────────────────────────

def clamp(value: float, min_val: float = 0.0, max_val: float = 100.0) -> float:
    """Clamp *value* to [*min_val*, *max_val*]."""
    return max(min_val, min(max_val, value))


def percentage(part: float, total: float, decimals: int = 1) -> float:
    """Return (part / total) * 100 rounded to *decimals*, or 0.0 if total is 0."""
    if not total:
        return 0.0
    return round((part / total) * 100, decimals)


# ──────────────────────────────────────────────
# Hash helpers
# ──────────────────────────────────────────────

def sha256_file(filepath: str) -> str:
    """Return the SHA-256 hex digest of a file for integrity checks."""
    h = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
    except OSError:
        return ""
    return h.hexdigest()
