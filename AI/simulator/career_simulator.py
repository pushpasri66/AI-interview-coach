from typing import Dict, Any, List, Optional
from datetime import datetime

from backend.database import db
from backend.models.career_simulation import CareerSimulation
from backend.models.user import User
from AI.digital_twin.digital_twin_engine import DigitalTwinEngine
from AI.simulator.scenario_engine import ScenarioEngine
from AI.simulator.outcome_predictor import OutcomePredictor


class AICareerSimulator:
    """Master simulator predicting the career and market impact of prospective learning, projects, certs, and role transitions."""

    def __init__(self):
        self.scenario_engine = ScenarioEngine()
        self.outcome_predictor = OutcomePredictor()
        self.twin_engine = DigitalTwinEngine()

    def run_simulation(
        self,
        user_id: int,
        scenario_title: str,
        scenario_type: str = "",
        target_role: Optional[str] = None,
        persist: bool = True
    ) -> Dict[str, Any]:
        """Executes a hypothetical career experiment and projects impact across all core metrics."""
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"User #{user_id} does not exist.")

        # 1. Fetch current baseline state from candidate Digital Twin
        twin_data = self.twin_engine.get_digital_twin_state(user_id=user_id, auto_sync=False)
        scores = twin_data.get("scores", {})
        base_readiness = scores.get("career_readiness_score", 75)
        base_interview = scores.get("interview_readiness", 70)
        
        role = target_role or twin_data.get("target_role", "Software Engineer")
        compat_dict = twin_data.get("job_compatibility", {})
        base_job_match = compat_dict.get(role, 72)

        # 2. Determine scenario type
        inferred_type = self.scenario_engine.infer_scenario_type(scenario_title, scenario_type)

        # 3. Predict outcome & quantitative deltas
        outcomes = self.outcome_predictor.predict_outcome(
            scenario_type=inferred_type,
            scenario_title=scenario_title,
            target_role=role,
            base_readiness=base_readiness,
            base_job_match=base_job_match,
            base_interview_readiness=base_interview
        )

        sim_dict = {
            "user_id": user_id,
            "scenario_type": inferred_type,
            "scenario_title": scenario_title,
            "target_role": role,
            "impact_comparison": {
                "career_readiness": {
                    "current": outcomes["current_readiness"],
                    "predicted": outcomes["predicted_readiness"],
                    "delta": outcomes["readiness_delta"],
                    "delta_display": f"+{outcomes['readiness_delta']}%"
                },
                "job_match": {
                    "current": outcomes["current_job_match"],
                    "predicted": outcomes["predicted_job_match"],
                    "delta": outcomes["job_match_delta"],
                    "delta_display": f"+{outcomes['job_match_delta']}%"
                },
                "interview_readiness": {
                    "current": outcomes["current_interview_readiness"],
                    "predicted": outcomes["predicted_interview_readiness"],
                    "delta": outcomes["predicted_interview_readiness"] - outcomes["current_interview_readiness"],
                    "delta_display": f"+{outcomes['predicted_interview_readiness'] - outcomes['current_interview_readiness']}%"
                },
                "salary_potential": {
                    "current": outcomes["current_salary_est"],
                    "predicted": outcomes["predicted_salary_est"],
                    "growth_percentage": outcomes["salary_growth_pct"],
                    "growth_display": f"+{outcomes['salary_growth_pct']}%"
                }
            },
            "recommended_next_step": outcomes["recommended_next_step"],
            "created_at": datetime.utcnow().isoformat()
        }

        if persist:
            record = CareerSimulation(
                user_id=user_id,
                scenario_type=inferred_type,
                scenario_title=scenario_title,
                target_role=role,
                current_readiness=outcomes["current_readiness"],
                predicted_readiness=outcomes["predicted_readiness"],
                readiness_delta=outcomes["readiness_delta"],
                current_job_match=outcomes["current_job_match"],
                predicted_job_match=outcomes["predicted_job_match"],
                job_match_delta=outcomes["job_match_delta"],
                current_interview_readiness=outcomes["current_interview_readiness"],
                predicted_interview_readiness=outcomes["predicted_interview_readiness"],
                current_salary_est=outcomes["current_salary_est"],
                predicted_salary_est=outcomes["predicted_salary_est"],
                salary_growth_pct=outcomes["salary_growth_pct"],
                recommended_next_step=outcomes["recommended_next_step"]
            )
            record.set_details(sim_dict["impact_comparison"])
            db.session.add(record)
            db.session.commit()
            sim_dict["id"] = record.id

        return sim_dict

    def get_simulation_history(self, user_id: int) -> List[Dict[str, Any]]:
        """Retrieves past simulated scenarios for candidate."""
        records = CareerSimulation.query.filter_by(user_id=user_id).order_by(CareerSimulation.created_at.desc()).all()
        return [r.to_dict() for r in records]
