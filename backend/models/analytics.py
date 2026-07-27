from datetime import datetime
from backend.database import db


class PerformanceAnalytics(db.Model):
    """Database model storing historical candidate performance analytics across interview sessions."""
    __tablename__ = "performance_analytics"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id", ondelete="CASCADE"), nullable=True, index=True)
    ats_score = db.Column(db.Integer, default=0, nullable=False)
    technical_score = db.Column(db.Integer, default=0, nullable=False)
    communication_score = db.Column(db.Integer, default=0, nullable=False)
    confidence_score = db.Column(db.Integer, default=0, nullable=False)
    emotion_score = db.Column(db.Integer, default=0, nullable=False)
    eye_contact_score = db.Column(db.Integer, default=0, nullable=False)
    overall_score = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<PerformanceAnalytics id={self.id} user_id={self.user_id} overall_score={self.overall_score}>"
