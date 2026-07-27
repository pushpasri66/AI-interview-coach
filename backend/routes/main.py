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
