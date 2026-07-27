from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

from backend.database import db
from backend.models.user import User
from backend.models.resume import Resume, ResumeAnalysis
from backend.models.recruiter import Recruiter

recruiter_bp = Blueprint("recruiter", __name__, url_prefix="/recruiter")


@recruiter_bp.route("/dashboard")
@login_required
def dashboard():
    """Renders Recruiter & Enterprise Company Portal dashboard."""
    candidates = User.query.limit(20).all()
    candidate_cards = []

    for c in candidates:
        latest_res = Resume.query.filter_by(user_id=c.id).order_by(Resume.upload_date.desc()).first()
        score = 85
        if latest_res:
            analysis = ResumeAnalysis.query.filter_by(resume_id=latest_res.id).first()
            if analysis:
                score = analysis.ats_score

        candidate_cards.append({
            "id": c.id,
            "fullname": c.fullname,
            "email": c.email,
            "ats_score": score,
            "status": "Shortlisted" if score >= 80 else "Under Review"
        })

    return jsonify({"success": True, "candidates": candidate_cards})


@recruiter_bp.route("/post_job", methods=["POST"])
@login_required
def post_job():
    """Posts corporate recruiter hiring vacancy."""
    data = request.get_json(silent=True) or request.form
    company = data.get("company_name", "Tech Corp")
    role = data.get("job_role", "AI Engineer")
    reqs = data.get("requirements", "Python, Flask, PyTorch, Docker")

    rec = Recruiter(recruiter_id=current_user.id, company_name=company, job_role=role, requirements=reqs)
    db.session.add(rec)
    db.session.commit()

    return jsonify({"success": True, "message": "Job requirement posted successfully.", "recruiter_id": rec.id})
