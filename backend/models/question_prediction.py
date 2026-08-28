import json
from datetime import datetime
from backend.database import db


class InterviewPrediction(db.Model):
    """Database model storing AI-predicted interview questions with probability scores and rationale."""

    __tablename__ = "interview_predictions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    target_role = db.Column(db.String(100), default="Software Engineer", nullable=False)
    target_company = db.Column(db.String(100), nullable=True)
    job_description_snippet = db.Column(db.Text, nullable=True)
    
    total_predicted_questions = db.Column(db.Integer, default=0, nullable=False)
    highest_probability = db.Column(db.Integer, default=0, nullable=False)
    
    predictions_json = db.Column(db.Text, nullable=False)
    category_breakdown_json = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def get_predictions(self) -> list:
        return json.loads(self.predictions_json) if self.predictions_json else []

    def set_predictions(self, data: list) -> None:
        self.predictions_json = json.dumps(data)

    def get_category_breakdown(self) -> dict:
        return json.loads(self.category_breakdown_json) if self.category_breakdown_json else {}

    def set_category_breakdown(self, data: dict) -> None:
        self.category_breakdown_json = json.dumps(data)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "target_role": self.target_role,
            "target_company": self.target_company,
            "total_predicted_questions": self.total_predicted_questions,
            "highest_probability": self.highest_probability,
            "predictions": self.get_predictions(),
            "category_breakdown": self.get_category_breakdown(),
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self) -> str:
        return f"<InterviewPrediction id={self.id} user_id={self.user_id} role='{self.target_role}' count={self.total_predicted_questions}>"
