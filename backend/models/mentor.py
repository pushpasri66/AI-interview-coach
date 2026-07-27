from datetime import datetime
from backend.database import db


class MentorSession(db.Model):
    """Database model for tracking candidate AI mentor advisory sessions."""

    __tablename__ = "mentor_sessions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic = db.Column(db.String(150), nullable=False)
    advice_given = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<MentorSession id={self.id} user_id={self.user_id} topic={self.topic}>"
