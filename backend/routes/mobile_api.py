import jwt
import datetime
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash

from backend.database import db
from backend.models.user import User
from backend.models.interview import Interview
from backend.services.analytics_service import AnalyticsService

mobile_api_bp = Blueprint("mobile_api", __name__, url_prefix="/api/mobile")


def generate_jwt_token(user_id: int) -> str:
    """Generates PyJWT token valid for 7 days."""
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
        "iat": datetime.datetime.utcnow()
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def decode_jwt_token(token: str) -> dict:
    """Decodes and validates PyJWT token."""
    try:
        return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    except Exception:
        return None


@mobile_api_bp.route("/login", methods=["POST"])
def mobile_login():
    """Authenticates candidate credentials and returns JWT bearer token."""
    data = request.get_json(silent=True) or request.form
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"success": False, "error": "Missing email or password."}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"success": False, "error": "Invalid email or password credentials."}), 401

    token = generate_jwt_token(user.id)
    return jsonify({
        "success": True,
        "token": token,
        "user": {
            "id": user.id,
            "fullname": user.fullname,
            "email": user.email
        }
    })


@mobile_api_bp.route("/profile", methods=["GET"])
def mobile_profile():
    """Returns candidate profile information via JWT authentication."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"success": False, "error": "Missing or invalid Authorization header."}), 401

    token = auth_header.split(" ")[1]
    decoded = decode_jwt_token(token)
    if not decoded:
        return jsonify({"success": False, "error": "Invalid or expired JWT token."}), 401

    user = User.query.get(decoded["user_id"])
    if not user:
        return jsonify({"success": False, "error": "User not found."}), 404

    return jsonify({
        "success": True,
        "user": {
            "id": user.id,
            "fullname": user.fullname,
            "email": user.email,
            "created_at": user.created_at.strftime("%Y-%m-%d")
        }
    })


@mobile_api_bp.route("/progress", methods=["GET"])
def mobile_progress():
    """Returns candidate analytics progress data for mobile clients."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"success": False, "error": "Missing Authorization header."}), 401

    token = auth_header.split(" ")[1]
    decoded = decode_jwt_token(token)
    if not decoded:
        return jsonify({"success": False, "error": "Invalid token."}), 401

    analytics_svc = AnalyticsService()
    growth = analytics_svc.calculate_progress(decoded["user_id"])
    stats = analytics_svc.generate_statistics(decoded["user_id"])

    return jsonify({
        "success": True,
        "growth": growth,
        "stats": stats
    })


@mobile_api_bp.route("/interview", methods=["POST"])
def mobile_interview():
    """Generates an interview session for mobile application."""
    data = request.get_json(silent=True) or request.form
    auth_header = request.headers.get("Authorization")

    user_id = 1
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        decoded = decode_jwt_token(token)
        if decoded:
            user_id = decoded["user_id"]

    interview_type = data.get("interview_type", "hr")
    difficulty = data.get("difficulty", "medium")

    interview_obj = Interview(user_id=user_id, interview_type=interview_type, difficulty=difficulty)
    db.session.add(interview_obj)
    db.session.commit()

    return jsonify({
        "success": True,
        "interview_id": interview_obj.id,
        "interview_type": interview_type,
        "difficulty": difficulty
    })
