import datetime
from typing import Dict, Any, Optional

from backend.database import db
from backend.models.digital_twin import DigitalTwin
from backend.models.user import User
from AI.digital_twin.candidate_profile import CandidateProfile
from AI.digital_twin.career_state import CareerState
from AI.digital_twin.career_simulator import CareerSimulator
from AI.digital_twin.twin_predictor import TwinPredictor


class DigitalTwinEngine:
    """Master AI engine orchestrating Career Digital Twin construction, synchronization, and predictions."""

    def __init__(self):
        self.simulator = CareerSimulator()
        self.predictor = TwinPredictor()

    def build_digital_twin(self, user_id: int) -> Dict[str, Any]:
        """Generates dynamic in-memory AI career digital twin representation."""
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"User #{user_id} does not exist.")

        # Step 1: Aggregate multi-pillar profile
        profile_builder = CandidateProfile(user_id)
        snapshot = profile_builder.build_snapshot()

        # Step 2: Compute multi-dimensional career state
        state_evaluator = CareerState(snapshot)
        career_state = state_evaluator.evaluate_state()

        # Step 3: Run predictions & trajectory modeling
        compat_dict = career_state["job_compatibility"]
        target_role = career_state["target_role"]
        target_compat = compat_dict.get(target_role, 75)

        predictions = self.predictor.generate_all_predictions(
            readiness=career_state["career_readiness_score"],
            interview_readiness=career_state["interview_readiness"],
            tech_strength=career_state["technical_strength"],
            target_compatibility=target_compat
        )

        simulated_trajectory = self.simulator.simulate_milestone_trajectory(
            base_readiness=career_state["career_readiness_score"],
            target_role=target_role
        )

        return {
            "user_id": user_id,
            "candidate_name": user.fullname,
            "email": user.email,
            "target_role": target_role,
            "scores": {
                "career_readiness_score": career_state["career_readiness_score"],
                "interview_readiness": career_state["interview_readiness"],
                "technical_strength": career_state["technical_strength"],
                "communication_strength": career_state["communication_strength"],
                "skill_strength": career_state["skill_strength"]
            },
            "job_compatibility": career_state["job_compatibility"],
            "skill_gaps": career_state["skill_gaps"],
            "strengths": career_state["strengths"],
            "weaknesses": career_state["weaknesses"],
            "recommendations": career_state["recommendations"],
            "predictions": predictions,
            "trajectory": simulated_trajectory,
            "profile_snapshot": snapshot,
            "synced_at": datetime.datetime.utcnow().isoformat()
        }

    def sync_user_twin(self, user_id: int, trigger_event: str = "general") -> DigitalTwin:
        """Computes and synchronizes Digital Twin in the database."""
        twin_data = self.build_digital_twin(user_id)

        twin_rec = DigitalTwin.query.filter_by(user_id=user_id).first()
        if not twin_rec:
            twin_rec = DigitalTwin(user_id=user_id)
            db.session.add(twin_rec)

        twin_rec.target_role = twin_data["target_role"]
        twin_rec.career_readiness_score = twin_data["scores"]["career_readiness_score"]
        twin_rec.interview_readiness = twin_data["scores"]["interview_readiness"]
        twin_rec.technical_strength = twin_data["scores"]["technical_strength"]
        twin_rec.communication_strength = twin_data["scores"]["communication_strength"]
        twin_rec.skill_strength = twin_data["scores"]["skill_strength"]

        twin_rec.set_job_compatibility(twin_data["job_compatibility"])
        twin_rec.set_skill_gaps(twin_data["skill_gaps"])
        twin_rec.set_strengths(twin_data["strengths"])
        twin_rec.set_weaknesses(twin_data["weaknesses"])
        twin_rec.set_recommendations(twin_data["recommendations"])
        twin_rec.set_predictions(twin_data["predictions"])
        twin_rec.set_profile_summary(twin_data["profile_snapshot"])
        twin_rec.last_synced_at = datetime.datetime.utcnow()

        db.session.commit()
        return twin_rec

    def get_digital_twin_state(self, user_id: int, auto_sync: bool = True) -> Dict[str, Any]:
        """Fetches stored Digital Twin or builds fresh snapshot."""
        if auto_sync:
            twin_rec = self.sync_user_twin(user_id, trigger_event="fetch")
            return twin_rec.to_dict()

        twin_rec = DigitalTwin.query.filter_by(user_id=user_id).first()
        if not twin_rec:
            twin_rec = self.sync_user_twin(user_id, trigger_event="initial")

        return twin_rec.to_dict()
