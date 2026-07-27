import os
from flask import Flask, render_template
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import Config, config_by_name
from backend.database import db, migrate
from backend.models.user import User
from backend.models.resume import Resume, ResumeAnalysis
from backend.models.interview import Interview, Question, Answer
from backend.models.ai_analysis import AIAnalysis, VoiceAnalysis, FaceAnalysis
from backend.models.analytics import PerformanceAnalytics
from backend.models.skill import Skill
from backend.models.recommendation import CareerRecommendation
from backend.models.achievement import Achievement
from backend.models.conversation import Conversation
from backend.models.gamification import Gamification
from backend.models.career import CareerPlan
from backend.models.job import JobPosting
from backend.models.mentor import MentorSession
from backend.models.linkedin import LinkedInAnalysis
from backend.models.certificate import Certificate
from backend.models.recruiter import Recruiter
from backend.models.group_discussion import GroupDiscussion
from backend.utils.logging_config import setup_advanced_logging
from backend.utils.errors import register_error_handlers


def create_app(config_name=None):
    """Application factory for initializing AI Interview Coach Flask app."""
    app = Flask(
        __name__,
        template_folder="frontend/templates",
        static_folder="frontend/static"
    )

    # Determine configuration mode
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app.config.from_object(config_by_name.get(config_name, Config))

    # Ensure required folders exist
    for folder in ["database", "uploads/resumes", "uploads/interview_audio", "uploads/interview_video", "uploads/recordings", "reports/interview_reports", "logs"]:
        path = os.path.join(app.root_path, "..", folder)
        os.makedirs(path, exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CSRFProtect(app)

    # Initialize Limiter
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://"
    )

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Setup Logging & Error Handlers
    setup_advanced_logging(app)
    register_error_handlers(app)

    # Register Blueprints
    from backend.routes.main import main_bp
    from backend.routes.auth import auth_bp
    from backend.routes.dashboard import dashboard_bp
    from backend.routes.profile import profile_bp
    from backend.routes.resume import resume_bp
    from backend.routes.interview import interview_bp
    from backend.routes.analysis import analysis_bp
    from backend.routes.career import career_bp
    from backend.routes.analytics import analytics_bp
    from backend.routes.leaderboard import leaderboard_bp
    from backend.routes.mobile_api import mobile_api_bp
    from backend.routes.group_discussion import gd_bp
    from backend.routes.recruiter import recruiter_bp
    from backend.routes.mobile_v2 import mobile_v2_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(interview_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(career_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(leaderboard_bp)
    app.register_blueprint(mobile_api_bp)
    app.register_blueprint(gd_bp)
    app.register_blueprint(recruiter_bp)
    app.register_blueprint(mobile_v2_bp)

    # Exempt mobile API endpoints from web CSRF check
    CSRFProtect(app).exempt(mobile_api_bp)
    CSRFProtect(app).exempt(mobile_v2_bp)

    # Apply Rate Limiting to Sensitive Routes
    limiter.limit("10 per minute")(auth_bp)
    limiter.limit("30 per minute")(interview_bp)

    # Auto-create tables within application context
    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)