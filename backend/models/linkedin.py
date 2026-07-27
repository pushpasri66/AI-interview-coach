from datetime import datetime
from backend.database import db


class LinkedInAnalysis(db.Model):
    """Database model storing candidate LinkedIn profile evaluations and optimization recommendations."""

    __tablename__ = "linkedin_analyses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    headline_score = db.Column(db.Integer, default=80)
    summary_score = db.Column(db.Integer, default=85)
    overall_profile_score = db.Column(db.Integer, default=82)
    suggestions = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<LinkedInAnalysis id={self.id} user_id={self.user_id} score={self.overall_profile_score}>"
