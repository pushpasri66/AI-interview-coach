from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user

from backend.database import db
from backend.models.skill import Skill
from backend.models.recommendation import CareerRecommendation
from backend.services.recommendation_service import RecommendationService
try:
    from AI.models.job_analyzer import JobAnalyzer
except ImportError:
    class JobAnalyzer:  # Stub — AI module not yet implemented
        def analyze_job_description(self, job_text, skills):
            return {"match_score": 0, "matched_keywords": [], "missing_keywords": [],
                    "recommendation": "AI job analysis module is not yet configured.", "error": True}

career_bp = Blueprint("career", __name__, url_prefix="/career")


@career_bp.route("/dashboard")
@login_required
def dashboard():
    """Renders main Career Recommendation Dashboard."""
    rec_svc = RecommendationService()
    recommendations = rec_svc.recommend_roles(current_user.id)
    return render_template("career_dashboard.html", recommendations=recommendations)


@career_bp.route("/recommendations")
@login_required
def recommendations():
    """Renders career recommendation cards."""
    rec_svc = RecommendationService()
    recs = rec_svc.recommend_roles(current_user.id)
    return render_template("career_dashboard.html", recommendations=recs)


@career_bp.route("/skill-gap")
@login_required
def skill_gap():
    """Renders Skill Gap Analyzer page."""
    target_role = request.args.get("role", "AI Engineer")
    rec_svc = RecommendationService()
    gaps = rec_svc.find_skill_gaps(current_user.id, target_role=target_role)
    return render_template("skill_gap.html", gaps=gaps, target_role=target_role)


@career_bp.route("/roadmap")
@login_required
def roadmap():
    """Renders Personalized 4-Month Learning Roadmap page."""
    target_role = request.args.get("role", "AI Engineer")
    rec_svc = RecommendationService()
    plan = rec_svc.create_learning_plan(current_user.id, target_role=target_role)
    return render_template("roadmap.html", plan=plan)


@career_bp.route("/job-match")
@login_required
def job_match():
    """Renders Job Description Compatibility Analyzer page."""
    return render_template("job_match.html")


@career_bp.route("/analyze-job", methods=["POST"])
@login_required
def analyze_job():
    """Analyzes job description text and computes compatibility match score."""
    job_text = request.form.get("job_description", "").strip()

    if not job_text:
        flash("Please paste a job description to analyze.", "warning")
        return redirect(url_for("career.job_match"))

    # Extract user skills
    skills = Skill.query.filter_by(user_id=current_user.id).all()
    skill_names = [s.skill_name for s in skills] if skills else ["Python", "SQL", "Machine Learning", "Flask"]

    analyzer = JobAnalyzer()
    res = analyzer.analyze_job_description(job_text, skill_names)

    return render_template("job_match.html", result=res, job_text=job_text)


@career_bp.route("/generate-roadmap", methods=["POST"])
@login_required
def generate_roadmap():
    """Generates roadmap JSON for target role."""
    target_role = request.form.get("target_role", "AI Engineer")
    rec_svc = RecommendationService()
    plan = rec_svc.create_learning_plan(current_user.id, target_role=target_role)
    return jsonify({"success": True, "plan": plan})


@career_bp.route("/digital-twin", methods=["GET"])
@login_required
def digital_twin_json():
    """Returns candidate's Career Digital Twin structured data."""
    from AI.digital_twin.digital_twin_engine import DigitalTwinEngine
    engine = DigitalTwinEngine()
    twin_data = engine.get_digital_twin_state(user_id=current_user.id, auto_sync=True)
    return jsonify({
        "success": True,
        "candidate": {
            "id": current_user.id,
            "fullname": current_user.fullname,
            "email": current_user.email
        },
        "digital_twin": twin_data
    })


@career_bp.route("/intelligence", methods=["GET"])
@career_bp.route("/career-intelligence", methods=["GET"])
@login_required
def career_intelligence():
    """Renders Advanced AI Career Intelligence Dashboard."""
    from AI.digital_twin.digital_twin_engine import DigitalTwinEngine
    engine = DigitalTwinEngine()
    twin_data = engine.get_digital_twin_state(user_id=current_user.id, auto_sync=True)
    return render_template("career_intelligence.html", twin_data=twin_data)


