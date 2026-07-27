from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from backend.database import db
from backend.utils.forms import ProfileUpdateForm, ChangePasswordForm

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Renders user profile and handles name updates & password changes."""
    profile_form = ProfileUpdateForm(fullname=current_user.fullname)
    password_form = ChangePasswordForm()

    action = request.form.get("action")

    if request.method == "POST":
        if action == "update_profile" and profile_form.validate_on_submit():
            new_fullname = profile_form.fullname.data.strip()
            current_user.fullname = new_fullname
            db.session.commit()

            current_app.logger.info(f"User {current_user.email} updated full name to: {new_fullname}")
            flash("Profile updated successfully!", "success")
            return redirect(url_for("profile.profile"))

        elif action == "change_password" and password_form.validate_on_submit():
            current_password = password_form.current_password.data
            new_password = password_form.new_password.data

            if not current_user.check_password(current_password):
                flash("Incorrect current password.", "danger")
            else:
                current_user.set_password(new_password)
                db.session.commit()

                current_app.logger.info(f"User {current_user.email} updated password.")
                flash("Password updated successfully!", "success")
                return redirect(url_for("profile.profile"))

    return render_template(
        "profile.html",
        user=current_user,
        profile_form=profile_form,
        password_form=password_form
    )
