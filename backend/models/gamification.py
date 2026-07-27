import json
from datetime import datetime
from backend.database import db


class Gamification(db.Model):
    """Database model tracking candidate experience points, levels, active streak days, and unlocked badges."""

    __tablename__ = "gamification"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    points = db.Column(db.Integer, default=150, nullable=False)
    level = db.Column(db.Integer, default=1, nullable=False)
    badges = db.Column(db.Text, nullable=True)  # JSON list string
    streak = db.Column(db.Integer, default=3, nullable=False)  # consecutive practice days
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def get_badges_list(self) -> list:
        if not self.badges:
            return ["First Interview Completed", "ATS Master"]
        try:
            return json.loads(self.badges)
        except Exception:
            return ["First Interview Completed", "ATS Master"]

    def add_points(self, pts: int) -> None:
        self.points += pts
        self.level = max(1, self.points // 100)

    def __repr__(self) -> str:
        return f"<Gamification user_id={self.user_id} points={self.points} level={self.level}>"
