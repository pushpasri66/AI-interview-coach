"""
Score model for the AI Interview Coach platform.

Provides a unified score record per interview session, aggregating
individual question scores and AI analysis sub-scores into a single
persistent snapshot for leaderboard and analytics queries.
"""
from datetime import datetime
from backend.database import db


class Score(db.Model):
    """Aggregated score record for a completed interview session."""

    __tablename__ = "scores"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id"), nullable=False, unique=True, index=True)

    # Core scores (0–100)
    overall_score = db.Column(db.Float, nullable=False, default=0.0)
    answer_score = db.Column(db.Float, nullable=True)        # Content quality
    communication_score = db.Column(db.Float, nullable=True) # Grammar & fluency
    confidence_score = db.Column(db.Float, nullable=True)    # Voice / emotion analysis
    eye_contact_score = db.Column(db.Float, nullable=True)   # Face analysis
    technical_score = db.Column(db.Float, nullable=True)     # Technical accuracy

    # Grade derived from overall_score
    grade = db.Column(db.String(5), nullable=True)           # A+, A, B, C, D, F

    # Metadata
    total_questions = db.Column(db.Integer, nullable=True)
    answered_questions = db.Column(db.Integer, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @staticmethod
    def compute_grade(score: float) -> str:
        """Return a letter grade for a numeric *score* (0–100)."""
        if score >= 90:
            return "A+"
        if score >= 80:
            return "A"
        if score >= 70:
            return "B"
        if score >= 60:
            return "C"
        if score >= 50:
            return "D"
        return "F"

    def to_dict(self) -> dict:
        """Return a JSON-serialisable dict representation."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "interview_id": self.interview_id,
            "overall_score": self.overall_score,
            "answer_score": self.answer_score,
            "communication_score": self.communication_score,
            "confidence_score": self.confidence_score,
            "eye_contact_score": self.eye_contact_score,
            "technical_score": self.technical_score,
            "grade": self.grade,
            "total_questions": self.total_questions,
            "answered_questions": self.answered_questions,
            "duration_seconds": self.duration_seconds,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        return f"<Score id={self.id} interview_id={self.interview_id} overall={self.overall_score}>"
