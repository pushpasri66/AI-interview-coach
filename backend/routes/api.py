import jwt
import datetime
from typing import Optional, Tuple
from flask import Blueprint, request, jsonify, current_app
from flask_login import current_user
from backend.models.user import User
from AI.digital_twin.digital_twin_engine import DigitalTwinEngine

api_bp = Blueprint("api", __name__, url_prefix="/api")


def get_authenticated_user() -> Tuple[Optional[User], Optional[str]]:

    """Helper to authenticate user via Flask-Login session or Bearer JWT token."""
    # 1. Check Flask-Login session
    if current_user and current_user.is_authenticated:
        return current_user, None

    # 2. Check Bearer JWT Header
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1].strip()
        try:
            decoded = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            user_id = decoded.get("user_id")
            if user_id:
                user = User.query.get(int(user_id))
                if user:
                    return user, None
                return None, "User associated with token not found."
            return None, "Invalid token payload."
        except jwt.ExpiredSignatureError:
            return None, "Authentication token has expired."
        except Exception:
            return None, "Invalid authentication token."

    return None, "Authentication required. Please log in or provide a valid Bearer token."


@api_bp.route("/career/digital-twin", methods=["GET"])
def get_career_digital_twin():
    """GET /api/career/digital-twin
    Returns structured AI Career Digital Twin state, multi-dimensional scores,
    job compatibility, skill gaps, strengths, weaknesses, recommendations, and predictions.
    """
    user, auth_error = get_authenticated_user()
    if not user:
        return jsonify({
            "success": False,
            "error": auth_error
        }), 401

    try:
        engine = DigitalTwinEngine()
        twin_data = engine.get_digital_twin_state(user_id=user.id, auto_sync=True)

        return jsonify({
            "success": True,
            "candidate": {
                "id": user.id,
                "fullname": user.fullname,
                "email": user.email
            },
            "digital_twin": twin_data
        }), 200

    except ValueError as ve:
        return jsonify({
            "success": False,
            "error": str(ve)
        }), 404
    except Exception as e:
        current_app.logger.error(f"Error retrieving digital twin for user #{user.id}: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Failed to compute Career Digital Twin state."
        }), 500


@api_bp.route("/career/paths", methods=["GET"])
def get_career_paths():
    """GET /api/career/paths
    Predicts and evaluates career path suitability across 9 key tech roles with match %,
    existing/missing skills, projects, certifications, preparation times, and growth levels.
    """
    user, auth_error = get_authenticated_user()
    if not user:
        return jsonify({"success": False, "error": auth_error}), 401

    try:
        from AI.career_prediction.career_path_predictor import CareerPathPredictor
        from AI.career_prediction.career_transition import CareerTransitionEngine
        from AI.career_prediction.future_role_predictor import FutureRolePredictor

        predictor = CareerPathPredictor()
        predictions = predictor.predict_for_user(user.id, persist=True)

        transition_engine = CareerTransitionEngine()
        future_role_engine = FutureRolePredictor()

        # Build transition plan to primary predicted role
        from AI.digital_twin.candidate_profile import CandidateProfile
        profile = CandidateProfile(user.id).build_snapshot()
        candidate_skills = [s["skill_name"] for s in profile.get("skills", [])]
        target_role = request.args.get("target_role", predictions["primary_role"])

        transition_plan = transition_engine.generate_transition_plan(
            current_role="Candidate",
            target_role=target_role,
            current_skills=candidate_skills
        )

        emerging_roles = future_role_engine.predict_emerging_roles(
            current_skills=candidate_skills,
            current_role=predictions["primary_role"]
        )

        return jsonify({
            "success": True,
            "candidate": {
                "id": user.id,
                "fullname": user.fullname,
                "email": user.email
            },
            "career_paths": predictions,
            "active_transition_plan": transition_plan,
            "emerging_roles_outlook": emerging_roles
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error computing career paths for User #{user.id}: {str(e)}")
        return jsonify({"success": False, "error": "Failed to calculate career path predictions."}), 500


@api_bp.route("/career/future-skills", methods=["GET"])
def get_future_skills():
    """GET /api/career/future-skills
    Predicts 1-year, 2-year, and 3-year future skill demand trajectories,
    growth percentages, importance, learning priorities, and macro trends.
    """
    user, auth_error = get_authenticated_user()
    if not user:
        return jsonify({"success": False, "error": auth_error}), 401

    try:
        from AI.future_skills.skill_demand_predictor import SkillDemandPredictor
        from AI.future_skills.trend_analyzer import TrendAnalyzer
        from AI.future_skills.emerging_skills import EmergingSkillsEngine
        from AI.digital_twin.candidate_profile import CandidateProfile

        profile = CandidateProfile(user.id).build_snapshot()
        candidate_skills = [s["skill_name"] for s in profile.get("skills", [])]

        skill_predictor = SkillDemandPredictor()
        trend_analyzer = TrendAnalyzer()
        emerging_engine = EmergingSkillsEngine()

        future_skills_data = skill_predictor.predict_future_skills_for_candidate(
            candidate_skills=candidate_skills,
            target_role=profile.get("target_role", "Software Engineer")
        )

        trend_analysis = trend_analyzer.analyze_profile_trends(candidate_skills)
        emerging_tracks = emerging_engine.recommend_for_candidate(candidate_skills)

        return jsonify({
            "success": True,
            "candidate": {
                "id": user.id,
                "fullname": user.fullname
            },
            "future_skills": future_skills_data,
            "trend_intelligence": trend_analysis,
            "emerging_breakthrough_tracks": emerging_tracks
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error computing future skills for User #{user.id}: {str(e)}")
        return jsonify({"success": False, "error": "Failed to calculate future skill predictions."}), 500


@api_bp.route("/career/skill-gaps", methods=["GET"])
def get_skill_gaps():
    """GET /api/career/skill-gaps
    Returns comprehensive personalized skill gaps analysis integrated with the candidate's Digital Twin and target role.
    """
    user, auth_error = get_authenticated_user()
    if not user:
        return jsonify({"success": False, "error": auth_error}), 401

    try:
        from AI.digital_twin.digital_twin_engine import DigitalTwinEngine
        from AI.career_prediction.role_predictor import RolePredictor

        target_role = request.args.get("role", "Software Engineer")
        engine = DigitalTwinEngine()
        twin_data = engine.get_digital_twin_state(user_id=user.id, auto_sync=False)

        role_predictor = RolePredictor()
        candidate_skills = [s["skill_name"] for s in twin_data.get("profile_summary", {}).get("skills", [])]
        
        # If specific role requested, evaluate against catalog
        if target_role in role_predictor.ROLES_CATALOG:
            role_eval = role_predictor.evaluate_role(
                role_name=target_role,
                candidate_skills=set(candidate_skills),
                candidate_scores=twin_data.get("scores", {})
            )
            gaps_list = [
                {
                    "skill": s,
                    "target_role": target_role,
                    "importance": "Critical" if s in role_eval["missing_skills"][:2] else "High",
                    "learning_timeline": "2-4 Weeks",
                    "action": f"Master {s} via practical projects to fulfill {target_role} requirements."
                }
                for s in role_eval["missing_skills"]
            ]
        else:
            gaps_list = twin_data.get("skill_gaps", [])

        return jsonify({
            "success": True,
            "target_role": target_role,
            "candidate": {
                "id": user.id,
                "fullname": user.fullname
            },
            "digital_twin_scores": twin_data.get("scores", {}),
            "skill_gaps": gaps_list,
            "total_gaps": len(gaps_list),
            "recommendations": twin_data.get("recommendations", [])
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error computing skill gaps for User #{user.id}: {str(e)}")
        return jsonify({"success": False, "error": "Failed to analyze skill gaps."}), 500


@api_bp.route("/career/interview-predictions", methods=["POST"])
def generate_interview_predictions():
    """POST /api/career/interview-predictions
    Generates likely interview questions using candidate resume, skills, projects,
    target job description, company, and role across 7 categories with probability scores.
    """
    user, auth_error = get_authenticated_user()
    if not user:
        return jsonify({"success": False, "error": auth_error}), 401

    try:
        data = request.get_json(silent=True) or request.form or {}
        target_role = data.get("target_role")
        target_company = data.get("target_company")
        job_description = data.get("job_description")

        from AI.question_prediction.question_predictor import QuestionPredictor
        predictor = QuestionPredictor()
        result = predictor.predict_and_persist_for_user(
            user_id=user.id,
            target_role=target_role,
            target_company=target_company,
            job_description=job_description
        )

        return jsonify({
            "success": True,
            "candidate": {
                "id": user.id,
                "fullname": user.fullname
            },
            "interview_predictions": result
        }), 201

    except Exception as e:
        current_app.logger.error(f"Error generating interview predictions for User #{user.id}: {str(e)}")
        return jsonify({"success": False, "error": "Failed to generate interview predictions."}), 500


@api_bp.route("/career/interview-predictions", methods=["GET"])
def get_interview_predictions():
    """GET /api/career/interview-predictions
    Retrieves the latest predicted interview questions set for the authenticated candidate.
    """
    user, auth_error = get_authenticated_user()
    if not user:
        return jsonify({"success": False, "error": auth_error}), 401

    try:
        from backend.models.question_prediction import InterviewPrediction
        from AI.question_prediction.question_predictor import QuestionPredictor

        latest_rec = InterviewPrediction.query.filter_by(user_id=user.id).order_by(InterviewPrediction.created_at.desc()).first()

        if not latest_rec:
            # Generate initial prediction on-the-fly
            predictor = QuestionPredictor()
            result = predictor.predict_and_persist_for_user(user_id=user.id)
        else:
            result = {
                "target_role": latest_rec.target_role,
                "target_company": latest_rec.target_company,
                "total_predicted_questions": latest_rec.total_predicted_questions,
                "highest_probability": latest_rec.highest_probability,
                "category_breakdown": latest_rec.get_category_breakdown(),
                "predictions": latest_rec.get_predictions(),
                "created_at": latest_rec.created_at.isoformat() if latest_rec.created_at else None
            }

        return jsonify({
            "success": True,
            "candidate": {
                "id": user.id,
                "fullname": user.fullname
            },
            "interview_predictions": result
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error retrieving interview predictions for User #{user.id}: {str(e)}")
        return jsonify({"success": False, "error": "Failed to retrieve interview predictions."}), 500


@api_bp.route("/github/analyze", methods=["GET"])
def analyze_github_profile():
    """GET /api/github/analyze
    Analyzes a candidate's GitHub profile and repositories for coding activity, repository quality,
    language distribution, project complexity, documentation, diversity, open-source impact,
    strengths, weaknesses, recommended improvements, and career relevance.
    """
    user, auth_error = get_authenticated_user()
    # Note: Allows authenticated user, or public analysis with valid username
    username = request.args.get("username", "").strip()

    if not username:
        if user and user.email:
            username = user.email.split("@")[0]
        else:
            return jsonify({
                "success": False,
                "error": "Missing required 'username' parameter (e.g. /api/github/analyze?username=octocat)."
            }), 400

    try:
        from AI.github.github_analyzer import GitHubAIAnalyzer
        analyzer = GitHubAIAnalyzer()
        user_id = user.id if user else None
        analysis = analyzer.analyze_profile(username=username, user_id=user_id, persist=True)

        return jsonify({
            "success": True,
            "github_analysis": analysis
        }), 200

    except ValueError as ve:
        return jsonify({
            "success": False,
            "error": str(ve)
        }), 404
    except Exception as e:
        current_app.logger.error(f"Error analyzing GitHub profile '{username}': {str(e)}")
        return jsonify({
            "success": False,
            "error": "Failed to complete GitHub AI profile analysis."
        }), 500


@api_bp.route("/career/job-application", methods=["POST"])
def create_job_application_package():
    """POST /api/career/job-application
    Generates a job-specific application package including tailored resume content,
    ATS keywords, personalized cover letter, screening application answers, and interview prep questions.
    """
    user, auth_error = get_authenticated_user()
    if not user:
        return jsonify({"success": False, "error": auth_error}), 401

    data = request.get_json(silent=True) or request.form or {}
    company_name = data.get("company_name", "").strip()
    target_role = data.get("target_role", "").strip()
    job_description = data.get("job_description", "").strip()

    if not company_name or not target_role:
        return jsonify({
            "success": False,
            "error": "Missing required 'company_name' or 'target_role' fields."
        }), 400

    try:
        from AI.job_application.application_engine import JobApplicationEngine
        engine = JobApplicationEngine()
        package = engine.generate_application_package(
            user_id=user.id,
            company_name=company_name,
            target_role=target_role,
            job_description=job_description,
            persist=True
        )

        return jsonify({
            "success": True,
            "job_application_package": package
        }), 201

    except Exception as e:
        current_app.logger.error(f"Error generating job application package for User #{user.id}: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Failed to generate job application package."
        }), 500


@api_bp.route("/career/job-application/history", methods=["GET"])
def get_job_application_history():
    """GET /api/career/job-application/history
    Retrieves the candidate's historical job applications and tailored packages.
    """
    user, auth_error = get_authenticated_user()
    if not user:
        return jsonify({"success": False, "error": auth_error}), 401

    try:
        from AI.job_application.application_engine import JobApplicationEngine
        engine = JobApplicationEngine()
        history = engine.get_application_history(user_id=user.id)

        return jsonify({
            "success": True,
            "candidate": {
                "id": user.id,
                "fullname": user.fullname
            },
            "total_applications": len(history),
            "applications": history
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error retrieving job application history for User #{user.id}: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Failed to retrieve job application history."
        }), 500


@api_bp.route("/career/daily-plan", methods=["GET"])
def get_daily_career_plan():
    """GET /api/career/daily-plan
    Retrieves or generates today's personalized career development plan with Explainable AI insights.
    """
    user, auth_error = get_authenticated_user()
    if not user:
        return jsonify({"success": False, "error": auth_error}), 401

    try:
        from AI.daily_planner.daily_plan_engine import DailyPlanEngine
        plan_date = request.args.get("date")  # optional YYYY-MM-DD
        engine = DailyPlanEngine()
        plan_data = engine.get_or_create_daily_plan(user_id=user.id, plan_date=plan_date)

        return jsonify({
            "success": True,
            "daily_plan": plan_data
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error retrieving daily plan for User #{user.id}: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Failed to retrieve daily career plan."
        }), 500


@api_bp.route("/career/daily-plan/complete", methods=["POST"])
def complete_daily_task():
    """POST /api/career/daily-plan/complete
    Marks a personalized daily career task complete, recalculates progress, and syncs Digital Twin.
    """
    user, auth_error = get_authenticated_user()
    if not user:
        return jsonify({"success": False, "error": auth_error}), 401

    data = request.get_json(silent=True) or request.form or {}
    task_id = str(data.get("task_id", "")).strip()
    completed = data.get("completed", True)

    if not task_id:
        return jsonify({
            "success": False,
            "error": "Missing required 'task_id' parameter."
        }), 400

    try:
        from AI.daily_planner.daily_plan_engine import DailyPlanEngine
        engine = DailyPlanEngine()
        result = engine.complete_task(user_id=user.id, task_id=task_id, completed=completed)

        if not result["success"]:
            return jsonify({
                "success": False,
                "error": f"Task '{task_id}' not found in today's daily plan."
            }), 404

        return jsonify({
            "success": True,
            "result": result
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error completing daily task for User #{user.id}: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Failed to complete daily task."
        }), 500


@api_bp.route("/career/simulate", methods=["POST"])
def simulate_career_scenario():
    """POST /api/career/simulate
    Simulates learning a skill, completing a certification, building a project, improving interview scores,
    or changing roles, and predicts the effect on readiness, job match, and salary potential.
    """
    user, auth_error = get_authenticated_user()
    if not user:
        return jsonify({"success": False, "error": auth_error}), 401

    data = request.get_json(silent=True) or request.form or {}
    scenario_title = data.get("scenario_title", "").strip() or data.get("scenario", "").strip()
    scenario_type = data.get("scenario_type", "").strip()
    target_role = data.get("target_role", "").strip() or None

    if not scenario_title:
        return jsonify({
            "success": False,
            "error": "Missing required 'scenario_title' field (e.g. 'Learn AWS + Docker')."
        }), 400

    try:
        from AI.simulator.career_simulator import AICareerSimulator
        simulator = AICareerSimulator()
        sim_result = simulator.run_simulation(
            user_id=user.id,
            scenario_title=scenario_title,
            scenario_type=scenario_type,
            target_role=target_role,
            persist=True
        )

        return jsonify({
            "success": True,
            "simulation": sim_result
        }), 201

    except Exception as e:
        current_app.logger.error(f"Error running career simulation for User #{user.id}: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Failed to execute career simulation."
        }), 500


@api_bp.route("/career/simulations", methods=["GET"])
def get_career_simulations_history():
    """GET /api/career/simulations
    Retrieves the history of past simulated career experiments for the authenticated candidate.
    """
    user, auth_error = get_authenticated_user()
    if not user:
        return jsonify({"success": False, "error": auth_error}), 401

    try:
        from AI.simulator.career_simulator import AICareerSimulator
        simulator = AICareerSimulator()
        history = simulator.get_simulation_history(user_id=user.id)

        return jsonify({
            "success": True,
            "candidate": {
                "id": user.id,
                "fullname": user.fullname
            },
            "total_simulations": len(history),
            "simulations": history
        }), 200

    except Exception as e:
        current_app.logger.error(f"Error retrieving simulation history for User #{user.id}: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Failed to retrieve simulation history."
        }), 500


@api_bp.route("/career/report", methods=["GET"])
def get_career_pdf_report():
    """GET /api/career/report
    Generates and downloads or streams a publication-grade AI Career Intelligence PDF report.
    Supports report types: 'intelligence', 'readiness', 'skill_gap', 'job_application'.
    """
    user, auth_error = get_authenticated_user()
    if not user:
        return jsonify({"success": False, "error": auth_error}), 401

    try:
        import os
        from flask import send_file
        from backend.services.career_report import CareerReportService

        report_type = request.args.get("type", "intelligence").strip()
        as_attachment = request.args.get("download", "false").lower() in ["true", "1", "yes"]

        service = CareerReportService()
        filepath = service.generate_career_pdf(user_id=user.id, report_type=report_type)

        if not os.path.exists(filepath):
            return jsonify({"success": False, "error": "Report generation failed."}), 500

        download_name = os.path.basename(filepath)
        return send_file(
            filepath,
            mimetype="application/pdf",
            as_attachment=as_attachment,
            download_name=download_name
        )

    except Exception as e:
        current_app.logger.error(f"Error generating career PDF report for User #{user.id}: {str(e)}")
        return jsonify({
            "success": False,
            "error": "Failed to generate AI career report."
        }), 500







