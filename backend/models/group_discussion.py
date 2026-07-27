from datetime import datetime
from backend.database import db


class GroupDiscussion(db.Model):
    """Database model storing AI mock group discussion sessions and leadership metrics."""

    __tablename__ = "group_discussions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic = db.Column(db.String(255), nullable=False)
    speaking_time_sec = db.Column(db.Integer, default=120)
    leadership_score = db.Column(db.Integer, default=85)
    communication_score = db.Column(db.Integer, default=88)
    overall_score = db.Column(db.Integer, default=86)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<GroupDiscussion id={self.id} user_id={self.user_id} topic={self.topic}>"
