from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from backend.models.user import User


class RegistrationForm(FlaskForm):
    """Form for user registration."""
    fullname = StringField(
        "Full Name",
        validators=[
            DataRequired(message="Full Name is required."),
            Length(min=2, max=100, message="Full Name must be between 2 and 100 characters.")
        ]
    )
    email = StringField(
        "Email Address",
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Please enter a valid email address.")
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required."),
            Length(min=8, message="Password must be at least 8 characters long.")
        ]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(message="Please confirm your password."),
            EqualTo("password", message="Passwords do not match.")
        ]
    )
    submit = SubmitField("Create Account")

    def validate_email(self, email):
        """Validates that email is unique."""
        user = User.query.filter_by(email=email.data.strip().lower()).first()
        if user:
            raise ValidationError("An account with this email already exists.")


class LoginForm(FlaskForm):
    """Form for user authentication."""
    email = StringField(
        "Email Address",
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Please enter a valid email address.")
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required.")
        ]
    )
    submit = SubmitField("Login")


class ProfileUpdateForm(FlaskForm):
    """Form for updating user profile info."""
    fullname = StringField(
        "Full Name",
        validators=[
            DataRequired(message="Full Name is required."),
            Length(min=2, max=100, message="Full Name must be between 2 and 100 characters.")
        ]
    )
    submit = SubmitField("Update Full Name")


class ChangePasswordForm(FlaskForm):
    """Form for changing user password."""
    current_password = PasswordField(
        "Current Password",
        validators=[
            DataRequired(message="Current password is required.")
        ]
    )
    new_password = PasswordField(
        "New Password",
        validators=[
            DataRequired(message="New password is required."),
            Length(min=8, message="New password must be at least 8 characters long.")
        ]
    )
    confirm_new_password = PasswordField(
        "Confirm New Password",
        validators=[
            DataRequired(message="Please confirm your new password."),
            EqualTo("new_password", message="New passwords do not match.")
        ]
    )
    submit = SubmitField("Update Password")
