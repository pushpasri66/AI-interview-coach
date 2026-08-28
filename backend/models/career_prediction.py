import json
from datetime import datetime
from backend.database import db


class CareerPathPrediction(db.Model):
    """Database model storing predicted career paths, role compatibility, and transition roadmaps."""

    __tablename__ = "career_path_predictions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    primary_role = db.Column(db.String(100), nullable=False)
    primary_match_pct = db.Column(db.Integer, default=0, nullable=False)
    
    # JSON structured payloads
    predicted_roles_json = db.Column(db.Text, nullable=True)
    transition_roadmap_json = db.Column(db.Text, nullable=True)
    future_readiness_json = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def get_predicted_roles(self) -> list:
        return json.loads(self.predicted_roles_json) if self.predicted_roles_json else []

    def set_predicted_roles(self, data: list) -> None:
        self.predicted_roles_json = json.dumps(data)

    def get_transition_roadmap(self) -> dict:
        return json.loads(self.transition_roadmap_json) if self.transition_roadmap_json else {}

    def set_transition_roadmap(self, data: dict) -> None:
        self.transition_roadmap_json = json.dumps(data)

    def get_future_readiness(self) -> dict:
        return json.loads(self.future_readiness_json) if self.future_readiness_json else {}

    def set_future_readiness(self, data: dict) -> None:
        self.future_readiness_json = json.dumps(data)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "primary_role": self.primary_role,
            "primary_match_pct": self.primary_match_pct,
            "predicted_roles": self.get_predicted_roles(),
            "transition_roadmap": self.get_transition_roadmap(),
            "future_readiness": self.get_future_readiness(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self) -> str:
        return f"<CareerPathPrediction id={self.id} user_id={self.user_id} primary_role='{self.primary_role}'>"
