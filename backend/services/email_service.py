"""
Email notification service for the AI Interview Coach platform.

Sends transactional emails (welcome, interview summary, password reset)
via Flask-Mail when credentials are configured, and silently logs to the
app logger when MAIL_USERNAME is not set (useful in development).
"""
import os
from flask import current_app, render_template_string


# ──────────────────────────────────────────────
# Email templates (inline fallbacks)
# ──────────────────────────────────────────────

_WELCOME_TEMPLATE = """
Subject: Welcome to AI Interview Coach!

Hi {{ name }},

Your account has been created successfully.
Start your interview journey at {{ app_url }}.

Good luck!
The AI Interview Coach Team
"""

_INTERVIEW_SUMMARY_TEMPLATE = """
Subject: Your Interview Summary — Score: {{ score }}/100

Hi {{ name }},

Here is a summary of your recent interview session:
- Interview Type: {{ interview_type }}
- Overall Score:  {{ score }}/100
- Grade:          {{ grade }}

{{ summary }}

Keep practicing — you're getting better every day!
The AI Interview Coach Team
"""

_PASSWORD_RESET_TEMPLATE = """
Subject: Password Reset Request

Hi {{ name }},

Click the link below to reset your password (valid for 1 hour):
{{ reset_url }}

If you did not request a password reset, please ignore this email.

The AI Interview Coach Team
"""


def _is_mail_configured() -> bool:
    """Return True if mail credentials are set in the current app config."""
    username = current_app.config.get("MAIL_USERNAME", "")
    return bool(username and username != "your-email@gmail.com")


def _send(subject: str, recipient: str, body: str) -> bool:
    """
    Internal helper — attempt to send *body* to *recipient* via Flask-Mail.

    Falls back to logging when mail is not configured.
    Returns True on success, False on failure.
    """
    if not _is_mail_configured():
        current_app.logger.info(
            f"[EmailService] Mail not configured. Would send '{subject}' to {recipient}."
        )
        return False

    try:
        from flask_mail import Mail, Message  # type: ignore
        mail = Mail(current_app)
        msg = Message(
            subject=subject,
            recipients=[recipient],
            body=body,
            sender=current_app.config.get("MAIL_USERNAME"),
        )
        mail.send(msg)
        current_app.logger.info(f"[EmailService] Email '{subject}' sent to {recipient}.")
        return True
    except Exception as exc:
        current_app.logger.error(f"[EmailService] Failed to send email to {recipient}: {exc}")
        return False


# ──────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────

def send_welcome_email(user_email: str, user_name: str) -> bool:
    """Send a welcome email to a newly registered user."""
    app_url = os.getenv("APP_URL", "http://localhost:5000")
    body = render_template_string(
        _WELCOME_TEMPLATE, name=user_name, app_url=app_url
    )
    return _send("Welcome to AI Interview Coach!", user_email, body)


def send_interview_summary_email(
    user_email: str,
    user_name: str,
    interview_type: str,
    score: int,
    grade: str,
    summary: str,
) -> bool:
    """Send an interview performance summary email."""
    body = render_template_string(
        _INTERVIEW_SUMMARY_TEMPLATE,
        name=user_name,
        interview_type=interview_type,
        score=score,
        grade=grade,
        summary=summary,
    )
    return _send(f"Your Interview Summary — Score: {score}/100", user_email, body)


def send_password_reset_email(user_email: str, user_name: str, reset_url: str) -> bool:
    """Send a password reset link email."""
    body = render_template_string(
        _PASSWORD_RESET_TEMPLATE, name=user_name, reset_url=reset_url
    )
    return _send("Password Reset Request — AI Interview Coach", user_email, body)
