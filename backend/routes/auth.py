from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from backend.database import db
from backend.models.user import User
from backend.utils.forms import RegistrationForm, LoginForm

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
@auth_bp.route("/auth/register", methods=["GET", "POST"])
def register():
    """Renders registration page and handles new user creation."""
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))

    form = RegistrationForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        fullname = form.fullname.data.strip()
        password = form.password.data

        try:
            new_user = User(
                fullname=fullname,
                email=email
            )
            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()

            current_app.logger.info(f"New user registered successfully: {email}")
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for("auth.login"))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error registering user: {str(e)}")
            flash("An error occurred during registration. Please try again.", "danger")

    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
@auth_bp.route("/auth/login", methods=["GET", "POST"])
def login():
    """Renders login page and authenticates existing users."""
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            user.last_login = datetime.utcnow()
            db.session.commit()

            login_user(user, remember=True)
            current_app.logger.info(f"User logged in successfully: {email}")

            next_page = request.args.get("next")
            if next_page and next_page.startswith("/"):
                return redirect(next_page)
            
            flash(f"Welcome back, {user.fullname}!", "success")
            return redirect(url_for("dashboard.dashboard"))

        current_app.logger.warning(f"Failed login attempt for email: {email}")
        flash("Invalid email address or password. Please try again.", "danger")

    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    """Logs out the current user and redirects to home page."""
    user_email = current_user.email
    logout_user()
    current_app.logger.info(f"User logged out: {user_email}")
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("main.home"))
