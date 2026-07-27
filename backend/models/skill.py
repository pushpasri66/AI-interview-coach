from datetime import datetime
from backend.database import db


class Skill(db.Model):
    """Database model tracking candidate technical & soft skills extracted from resumes or interviews."""
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_name = db.Column(db.String(100), nullable=False)
    skill_level = db.Column(db.String(50), default="Intermediate")  # Beginner, Intermediate, Advanced, Expert
    source = db.Column(db.String(50), default="Resume")  # Resume, Interview, Recommendation
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Skill id={self.id} user_id={self.user_id} skill_name={self.skill_name}>"
