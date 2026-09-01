from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    """Renders main landing page."""
    return render_template("index.html")


@main_bp.route("/about")
def about():
    """Renders about platform page."""
    return render_template("about.html")


@main_bp.route("/init-db")
def init_db():
    """Manual endpoint to initialize database tables."""
    try:
        from backend.database import db
        db.create_all()
        return "Database tables created successfully! <a href='/'>Go to Home</a>", 200
    except Exception as e:
        return f"Failed to create tables: {str(e)}", 500
