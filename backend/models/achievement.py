from datetime import datetime
from backend.database import db


class Achievement(db.Model):
    """Database model tracking candidate unlocked badges and milestone accomplishments."""
    __tablename__ = "achievements"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    badge_title = db.Column(db.String(100), nullable=False)
    badge_icon = db.Column(db.String(50), default="fa-trophy")
    description = db.Column(db.String(255), nullable=False)
    unlocked_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Achievement id={self.id} user_id={self.user_id} title={self.badge_title}>"
