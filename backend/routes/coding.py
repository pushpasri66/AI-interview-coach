"""
Coding interview routes for the AI Interview Coach platform.

Provides web endpoints for the AI-powered coding interview sandbox,
including challenge display, code submission, and result review.
"""
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user

coding_bp = Blueprint("coding", __name__, url_prefix="/coding")


@coding_bp.route("/")
@login_required
def coding_home():
    """Render the coding interview sandbox landing page."""
    return render_template("coding/index.html")


@coding_bp.route("/challenge/<int:challenge_id>")
@login_required
def coding_challenge(challenge_id: int):
    """Render a specific coding challenge by ID."""
    # TODO: Fetch challenge from database by challenge_id
    return render_template("coding/challenge.html", challenge_id=challenge_id)


@coding_bp.route("/submit", methods=["POST"])
@login_required
def submit_code():
    """
    Accept a code submission and return evaluation results.

    Expected JSON body: { "challenge_id": int, "language": str, "code": str }
    """
    data = request.get_json(silent=True) or {}
    challenge_id = data.get("challenge_id")
    language = data.get("language", "python")
    code = data.get("code", "")

    if not challenge_id or not code:
        return jsonify({"success": False, "error": "challenge_id and code are required."}), 400

    # TODO: Integrate sandboxed code execution engine
    return jsonify({
        "success": True,
        "challenge_id": challenge_id,
        "language": language,
        "result": "pending",
        "message": "Code submission received. Evaluation engine not yet configured.",
    })


@coding_bp.route("/results/<int:challenge_id>")
@login_required
def coding_results(challenge_id: int):
    """Return the evaluation results for a submitted challenge."""
    # TODO: Fetch stored results from database
    return jsonify({
        "success": True,
        "challenge_id": challenge_id,
        "user_id": current_user.id,
        "status": "not_attempted",
    })
