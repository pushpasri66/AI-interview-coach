from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user

from backend.database import db
from backend.models.interview import Interview
from backend.models.ai_analysis import AIAnalysis
from backend.models.achievement import Achievement
from backend.services.analytics_service import AnalyticsService
from backend.services.notification_service import NotificationService

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")


@analytics_bp.route("/dashboard")
@login_required
def dashboard():
    """Renders main AI Analytics & Performance Dashboard with Chart.js visualizations."""
    analytics_svc = AnalyticsService()
    stats = analytics_svc.generate_statistics(current_user.id)
    growth = analytics_svc.calculate_progress(current_user.id)
    ai_metrics = analytics_svc.get_candidate_ai_analytics(current_user.id)

    notif_svc = NotificationService()
    notifications = notif_svc.get_candidate_notifications(current_user.id)

    # Fetch achievements
    achievements = Achievement.query.filter_by(user_id=current_user.id).all()
    if not achievements:
        default_achievements = [
            Achievement(user_id=current_user.id, badge_title="First Step", badge_icon="fa-award", description="Completed registration & initialized candidate profile."),
            Achievement(user_id=current_user.id, badge_title="ATS Resume Analyzed", badge_icon="fa-file-invoice", description="Processed resume and obtained ATS score report."),
            Achievement(user_id=current_user.id, badge_title="Mock Interview Champion", badge_icon="fa-trophy", description="Completed AI Mock Interview session.")
        ]
        for ach in default_achievements:
            db.session.add(ach)
        db.session.commit()
        achievements = default_achievements

    interviews = Interview.query.filter_by(user_id=current_user.id).order_by(Interview.started_at.desc()).all()

    return render_template(
        "analytics.html",
        stats=stats,
        growth=growth,
        ai_metrics=ai_metrics,
        notifications=notifications,
        achievements=achievements,
        interviews=interviews
    )


@analytics_bp.route("/progress")
@login_required
def progress():
    """Returns candidate progress JSON data."""
    analytics_svc = AnalyticsService()
    growth = analytics_svc.calculate_progress(current_user.id)
    return jsonify({"success": True, "progress": growth})


@analytics_bp.route("/performance")
@login_required
def performance():
    """Returns candidate performance statistics JSON for charts."""
    analytics_svc = AnalyticsService()
    stats = analytics_svc.generate_statistics(current_user.id)
    return jsonify({"success": True, "stats": stats})
