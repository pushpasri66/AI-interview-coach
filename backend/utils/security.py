"""
Security utilities for the AI Interview Coach platform.

Provides token generation, JWT helpers, and request security checks
that complement Flask-Login session authentication.
"""
import os
import hmac
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app, request, jsonify
from flask_login import current_user


# ──────────────────────────────────────────────
# Token generation
# ──────────────────────────────────────────────

def generate_secure_token(nbytes: int = 32) -> str:
    """Return a cryptographically secure URL-safe token."""
    return secrets.token_urlsafe(nbytes)


def constant_time_compare(val1: str, val2: str) -> bool:
    """Compare two strings in constant time to prevent timing attacks."""
    return hmac.compare_digest(val1.encode(), val2.encode())


# ──────────────────────────────────────────────
# JWT helpers
# ──────────────────────────────────────────────

def create_jwt_token(user_id: int, expires_hours: int = 24) -> str:
    """Create a signed JWT token for mobile/API authentication."""
    payload = {
        "user_id": user_id,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=expires_hours),
    }
    secret = current_app.config.get("SECRET_KEY", "")
    return jwt.encode(payload, secret, algorithm="HS256")


def decode_jwt_token(token: str) -> dict | None:
    """
    Decode and validate a JWT token.

    Returns the decoded payload dict, or None if the token is invalid/expired.
    """
    secret = current_app.config.get("SECRET_KEY", "")
    try:
        return jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        current_app.logger.warning("JWT token has expired.")
        return None
    except jwt.InvalidTokenError as exc:
        current_app.logger.warning(f"Invalid JWT token: {exc}")
        return None


# ──────────────────────────────────────────────
# Request guards
# ──────────────────────────────────────────────

def get_bearer_token() -> str | None:
    """Extract a Bearer token from the Authorization header, or return None."""
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:]
    return None


def jwt_required(f):
    """
    Decorator that enforces JWT authentication on API routes.

    Accepts either:
    - An ``Authorization: Bearer <token>`` header, or
    - An active Flask-Login session (current_user.is_authenticated)
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Allow session-authenticated users through without a token
        if current_user.is_authenticated:
            return f(*args, **kwargs)

        token = get_bearer_token()
        if not token:
            return jsonify({"success": False, "error": "Authentication required."}), 401

        payload = decode_jwt_token(token)
        if not payload:
            return jsonify({"success": False, "error": "Invalid or expired token."}), 401

        return f(*args, **kwargs)

    return decorated


# ──────────────────────────────────────────────
# File security
# ──────────────────────────────────────────────

def safe_join(base_dir: str, *parts: str) -> str:
    """
    Safely join path components under *base_dir*.

    Raises ValueError if the resulting path escapes *base_dir* (path traversal).
    """
    base = os.path.realpath(base_dir)
    target = os.path.realpath(os.path.join(base_dir, *parts))
    if not target.startswith(base + os.sep) and target != base:
        raise ValueError(f"Path traversal detected: {target!r}")
    return target
