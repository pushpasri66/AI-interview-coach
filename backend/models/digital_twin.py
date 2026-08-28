import json
from datetime import datetime
from backend.database import db


class DigitalTwin(db.Model):
    """Database model for AI Career Digital Twin representing candidate readiness and career state."""

    __tablename__ = "digital_twins"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    
    # Core Quantitative Scores (0-100)
    career_readiness_score = db.Column(db.Integer, default=0, nullable=False)
    interview_readiness = db.Column(db.Integer, default=0, nullable=False)
    technical_strength = db.Column(db.Integer, default=0, nullable=False)
    communication_strength = db.Column(db.Integer, default=0, nullable=False)
    skill_strength = db.Column(db.Integer, default=0, nullable=False)
    target_role = db.Column(db.String(100), default="Software Engineer", nullable=False)
    
    # Structured JSON fields
    job_compatibility_json = db.Column(db.Text, nullable=True)
    skill_gaps_json = db.Column(db.Text, nullable=True)
    strengths_json = db.Column(db.Text, nullable=True)
    weaknesses_json = db.Column(db.Text, nullable=True)
    recommendations_json = db.Column(db.Text, nullable=True)
    profile_summary_json = db.Column(db.Text, nullable=True)
    predictions_json = db.Column(db.Text, nullable=True)
    
    last_synced_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def get_job_compatibility(self) -> dict:
        return json.loads(self.job_compatibility_json) if self.job_compatibility_json else {}

    def set_job_compatibility(self, data: dict) -> None:
        self.job_compatibility_json = json.dumps(data)

    def get_skill_gaps(self) -> list:
        return json.loads(self.skill_gaps_json) if self.skill_gaps_json else []

    def set_skill_gaps(self, data: list) -> None:
        self.skill_gaps_json = json.dumps(data)

    def get_strengths(self) -> list:
        return json.loads(self.strengths_json) if self.strengths_json else []

    def set_strengths(self, data: list) -> None:
        self.strengths_json = json.dumps(data)

    def get_weaknesses(self) -> list:
        return json.loads(self.weaknesses_json) if self.weaknesses_json else []

    def set_weaknesses(self, data: list) -> None:
        self.weaknesses_json = json.dumps(data)

    def get_recommendations(self) -> list:
        return json.loads(self.recommendations_json) if self.recommendations_json else []

    def set_recommendations(self, data: list) -> None:
        self.recommendations_json = json.dumps(data)

    def get_profile_summary(self) -> dict:
        return json.loads(self.profile_summary_json) if self.profile_summary_json else {}

    def set_profile_summary(self, data: dict) -> None:
        self.profile_summary_json = json.dumps(data)

    def get_predictions(self) -> dict:
        return json.loads(self.predictions_json) if self.predictions_json else {}

    def set_predictions(self, data: dict) -> None:
        self.predictions_json = json.dumps(data)

    def to_dict(self) -> dict:
        """Serializes digital twin state to structured dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "target_role": self.target_role,
            "scores": {
                "career_readiness_score": self.career_readiness_score,
                "interview_readiness": self.interview_readiness,
                "technical_strength": self.technical_strength,
                "communication_strength": self.communication_strength,
                "skill_strength": self.skill_strength
            },
            "job_compatibility": self.get_job_compatibility(),
            "skill_gaps": self.get_skill_gaps(),
            "strengths": self.get_strengths(),
            "weaknesses": self.get_weaknesses(),
            "recommendations": self.get_recommendations(),
            "predictions": self.get_predictions(),
            "profile_summary": self.get_profile_summary(),
            "last_synced_at": self.last_synced_at.isoformat() if self.last_synced_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self) -> str:
        return f"<DigitalTwin id={self.id} user_id={self.user_id} readiness={self.career_readiness_score}>"
