import re
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from backend.database import db


class User(UserMixin, db.Model):
    """User Database Model representing candidates and admins."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    profile_pic = db.Column(db.String(255), nullable=True, default="default.png")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)

    # Relationships
    resumes = db.relationship("Resume", backref="user", lazy=True, cascade="all, delete-orphan")
    interviews = db.relationship("Interview", backref="user", lazy=True, cascade="all, delete-orphan")
    digital_twin = db.relationship("DigitalTwin", backref="user", uselist=False, lazy=True, cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        """Hashes raw password using scrypt/pbkdf2 via Werkzeug security."""
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verifies raw password against stored hash."""
        if not self.password_hash or not password:
            return False
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def validate_password_strength(password: str) -> tuple[bool, str]:
        """Validates password strength (length >= 8, uppercase, lowercase, digit, special char)."""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter."
        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter."
        if not re.search(r"[0-9]", password):
            return False, "Password must contain at least one digit."
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Password must contain at least one special character (!@#$%^&*)."
        return True, "Password strength is valid."

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"