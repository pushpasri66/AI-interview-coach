import json
from datetime import datetime
from backend.database import db


class CareerSimulation(db.Model):
    """Database model storing candidate career simulation experiments, projected impacts, and outcomes."""

    __tablename__ = "career_simulations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    scenario_type = db.Column(db.String(50), nullable=False)  # learn_skill, certification, build_project, improve_interview, change_role, apply_jobs
    scenario_title = db.Column(db.String(255), nullable=False)
    target_role = db.Column(db.String(100), default="Software Engineer", nullable=False)
    
    # Quantitative comparison
    current_readiness = db.Column(db.Integer, default=0, nullable=False)
    predicted_readiness = db.Column(db.Integer, default=0, nullable=False)
    readiness_delta = db.Column(db.Integer, default=0, nullable=False)
    
    current_job_match = db.Column(db.Integer, default=0, nullable=False)
    predicted_job_match = db.Column(db.Integer, default=0, nullable=False)
    job_match_delta = db.Column(db.Integer, default=0, nullable=False)
    
    current_interview_readiness = db.Column(db.Integer, default=0, nullable=False)
    predicted_interview_readiness = db.Column(db.Integer, default=0, nullable=False)
    
    current_salary_est = db.Column(db.String(50), nullable=True)
    predicted_salary_est = db.Column(db.String(50), nullable=True)
    salary_growth_pct = db.Column(db.Integer, default=0, nullable=False)
    
    recommended_next_step = db.Column(db.Text, nullable=False)
    simulation_details_json = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def get_details(self) -> dict:
        return json.loads(self.simulation_details_json) if self.simulation_details_json else {}

    def set_details(self, data: dict) -> None:
        self.simulation_details_json = json.dumps(data)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "scenario_type": self.scenario_type,
            "scenario_title": self.scenario_title,
            "target_role": self.target_role,
            "impact_comparison": {
                "career_readiness": {
                    "current": self.current_readiness,
                    "predicted": self.predicted_readiness,
                    "delta": self.readiness_delta,
                    "delta_display": f"+{self.readiness_delta}%" if self.readiness_delta >= 0 else f"{self.readiness_delta}%"
                },
                "job_match": {
                    "current": self.current_job_match,
                    "predicted": self.predicted_job_match,
                    "delta": self.job_match_delta,
                    "delta_display": f"+{self.job_match_delta}%" if self.job_match_delta >= 0 else f"{self.job_match_delta}%"
                },
                "interview_readiness": {
                    "current": self.current_interview_readiness,
                    "predicted": self.predicted_interview_readiness,
                    "delta": self.predicted_interview_readiness - self.current_interview_readiness
                },
                "salary_potential": {
                    "current": self.current_salary_est,
                    "predicted": self.predicted_salary_est,
                    "growth_percentage": self.salary_growth_pct,
                    "growth_display": f"+{self.salary_growth_pct}%"
                }
            },
            "recommended_next_step": self.recommended_next_step,
            "details": self.get_details(),
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self) -> str:
        return f"<CareerSimulation id={self.id} user_id={self.user_id} scenario='{self.scenario_title}' delta=+{self.readiness_delta}%>"
