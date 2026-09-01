"""
Feedback model for the AI Interview Coach platform.

Captures per-interview AI-generated and user-submitted feedback,
including text comments, star ratings, and improvement suggestions.
"""
from datetime import datetime
from backend.database import db


class Feedback(db.Model):
    """Stores feedback entries linked to an interview session."""

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id"), nullable=True, index=True)

    # Feedback content
    source = db.Column(db.String(20), nullable=False, default="ai")  # "ai" | "user" | "recruiter"
    rating = db.Column(db.Integer, nullable=True)          # 1–5 star rating
    comment = db.Column(db.Text, nullable=True)             # Free-text feedback
    strengths = db.Column(db.Text, nullable=True)           # JSON list of strengths
    improvements = db.Column(db.Text, nullable=True)        # JSON list of areas to improve
    overall_score = db.Column(db.Float, nullable=True)      # 0–100 composite score

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self) -> dict:
        """Return a JSON-serialisable dict representation."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "interview_id": self.interview_id,
            "source": self.source,
            "rating": self.rating,
            "comment": self.comment,
            "strengths": self.strengths,
            "improvements": self.improvements,
            "overall_score": self.overall_score,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        return f"<Feedback id={self.id} interview_id={self.interview_id} source={self.source!r}>"
