import json
from datetime import datetime
from backend.database import db


class CareerRecommendation(db.Model):
    """Database model storing generated career recommendations, match percentages, and learning roadmaps."""
    __tablename__ = "career_recommendations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    recommended_role = db.Column(db.String(100), nullable=False)
    matching_percentage = db.Column(db.Integer, default=75, nullable=False)
    missing_skills = db.Column(db.Text, nullable=True)  # JSON formatted string
    suggested_courses = db.Column(db.Text, nullable=True)  # JSON formatted string
    roadmap = db.Column(db.Text, nullable=True)  # JSON formatted string
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def get_missing_skills(self) -> list:
        if not self.missing_skills:
            return []
        try:
            return json.loads(self.missing_skills)
        except Exception:
            return [s.strip() for s in self.missing_skills.split(",") if s.strip()]

    def get_suggested_courses(self) -> list:
        if not self.suggested_courses:
            return []
        try:
            return json.loads(self.suggested_courses)
        except Exception:
            return []

    def get_roadmap(self) -> dict:
        if not self.roadmap:
            return {}
        try:
            return json.loads(self.roadmap)
        except Exception:
            return {}

    def __repr__(self) -> str:
        return f"<CareerRecommendation id={self.id} user_id={self.user_id} role={self.recommended_role} match={self.matching_percentage}%>"
