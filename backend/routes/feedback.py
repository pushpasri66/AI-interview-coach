"""
Feedback routes for the AI Interview Coach platform.

Provides endpoints for submitting, retrieving, and managing
interview feedback entries from candidates and AI analysis.
"""
from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user

from backend.database import db
from backend.models.feedback import Feedback

feedback_bp = Blueprint("feedback", __name__, url_prefix="/feedback")


@feedback_bp.route("/submit", methods=["POST"])
@login_required
def submit_feedback():
    """
    Submit feedback for an interview session.

    Expected JSON body:
    {
        "interview_id": int,
        "rating": int (1–5),
        "comment": str (optional),
        "source": str (optional, default "user")
    }
    """
    data = request.get_json(silent=True) or {}
    interview_id = data.get("interview_id")
    rating = data.get("rating")
    comment = data.get("comment", "").strip()
    source = data.get("source", "user")

    if not interview_id:
        return jsonify({"success": False, "error": "interview_id is required."}), 400

    if rating is not None and not (1 <= int(rating) <= 5):
        return jsonify({"success": False, "error": "Rating must be between 1 and 5."}), 400

    try:
        feedback = Feedback(
            user_id=current_user.id,
            interview_id=int(interview_id),
            source=source,
            rating=int(rating) if rating is not None else None,
            comment=comment or None,
        )
        db.session.add(feedback)
        db.session.commit()

        current_app.logger.info(
            f"Feedback submitted by user {current_user.id} for interview {interview_id}."
        )
        return jsonify({"success": True, "feedback_id": feedback.id}), 201

    except Exception as exc:
        db.session.rollback()
        current_app.logger.error(f"Error saving feedback: {exc}")
        return jsonify({"success": False, "error": "Failed to save feedback."}), 500


@feedback_bp.route("/interview/<int:interview_id>")
@login_required
def get_interview_feedback(interview_id: int):
    """Return all feedback entries for a specific interview."""
    entries = Feedback.query.filter_by(
        user_id=current_user.id,
        interview_id=interview_id,
    ).order_by(Feedback.created_at.desc()).all()

    return jsonify({
        "success": True,
        "interview_id": interview_id,
        "total": len(entries),
        "feedback": [f.to_dict() for f in entries],
    })


@feedback_bp.route("/history")
@login_required
def feedback_history():
    """Return all feedback entries for the current user."""
    entries = Feedback.query.filter_by(
        user_id=current_user.id,
    ).order_by(Feedback.created_at.desc()).limit(50).all()

    return jsonify({
        "success": True,
        "total": len(entries),
        "feedback": [f.to_dict() for f in entries],
    })
