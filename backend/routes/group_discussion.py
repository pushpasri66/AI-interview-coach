from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

from backend.database import db
from backend.models.group_discussion import GroupDiscussion

gd_bp = Blueprint("group_discussion", __name__, url_prefix="/group-discussion")


@gd_bp.route("/")
@login_required
def index():
    """Renders AI Mock Group Discussion platform interface."""
    history = GroupDiscussion.query.filter_by(user_id=current_user.id).order_by(GroupDiscussion.created_at.desc()).all()
    return render_template("group_discussion.html", history=history)


@gd_bp.route("/start", methods=["POST"])
@login_required
def start_discussion():
    """Simulates AI Mock Group Discussion with AI Moderator and virtual candidate participants."""
    data = request.get_json(silent=True) or request.form
    topic = data.get("topic", "Impact of Artificial Intelligence on Future Employment")

    # Simulate GD evaluation scores
    gd_rec = GroupDiscussion(
        user_id=current_user.id,
        topic=topic,
        speaking_time_sec=140,
        leadership_score=88,
        communication_score=90,
        overall_score=89
    )
    db.session.add(gd_rec)
    db.session.commit()

    return jsonify({
        "success": True,
        "session_id": gd_rec.id,
        "topic": topic,
        "ai_moderator_statement": f"Welcome everyone. Today's group discussion topic is: '{topic}'. Let's hear opening remarks.",
        "ai_participants": [
            {"name": "Participant Alex (AI)", "point": "AI creates new engineering roles while automating repetitive tasks."},
            {"name": "Participant Sarah (AI)", "point": "We must focus on ethical AI governance and continuous workforce reskilling."}
        ],
        "scores": {
            "leadership": 88,
            "communication": 90,
            "overall": 89
        }
    })
