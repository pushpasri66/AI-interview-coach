from datetime import datetime
from backend.database import db


class CareerPlan(db.Model):
    """Database model storing candidate 6-month and 12-month career development plans."""

    __tablename__ = "career_plans"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    target_role = db.Column(db.String(100), nullable=False)
    duration_months = db.Column(db.Integer, default=6, nullable=False)  # 6 or 12
    skills_to_learn = db.Column(db.Text, nullable=True)
    projects_to_build = db.Column(db.Text, nullable=True)
    certifications = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<CareerPlan id={self.id} user_id={self.user_id} role={self.target_role}>"
