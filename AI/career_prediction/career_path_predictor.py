from typing import Dict, Any, List, Optional
from backend.database import db
from backend.models.career_prediction import CareerPathPrediction
from backend.models.user import User
from AI.digital_twin.candidate_profile import CandidateProfile
from AI.career_prediction.role_predictor import RolePredictor


class CareerPathPredictor:
    """Evaluates and ranks career path suitability across 9 key tech roles."""

    def __init__(self):
        self.role_evaluator = RolePredictor()

    def predict_paths_for_candidate(self, candidate_skills: List[str], candidate_scores: Dict[str, Any]) -> Dict[str, Any]:
        """Runs role compatibility predictions across all 9 catalog roles."""
        skills_set = set(candidate_skills)
        all_evaluations = []

        for role_name in self.role_evaluator.ROLES_CATALOG.keys():
            res = self.role_evaluator.evaluate_role(
                role_name=role_name,
                candidate_skills=skills_set,
                candidate_scores=candidate_scores
            )
            all_evaluations.append(res)

        # Sort descending by match percentage
        all_evaluations.sort(key=lambda x: x["match_percentage"], reverse=True)

        primary_role = all_evaluations[0]["role"]
        primary_match = all_evaluations[0]["match_percentage"]
        top_paths = all_evaluations[:3]

        # Determine competitiveness tier
        if primary_match >= 85:
            competitiveness = "Tier-1 Ready (Highly Competitive)"
        elif primary_match >= 70:
            competitiveness = "Strong Industry Contender"
        else:
            competitiveness = "Developing Skill Base"

        return {
            "primary_role": primary_role,
            "primary_match_percentage": primary_match,
            "competitiveness": competitiveness,
            "top_paths": top_paths,
            "all_roles": all_evaluations,
            "evaluated_roles_count": len(all_evaluations)
        }

    def predict_for_user(self, user_id: int, persist: bool = True) -> Dict[str, Any]:
        """Gathers user profile and calculates persistent career path predictions."""
        profile_builder = CandidateProfile(user_id)
        snapshot = profile_builder.build_snapshot()

        skills_list = [s.get("skill_name", "") for s in snapshot.get("skills", [])]
        scores_data = {
            "technical_strength": snapshot.get("interview_performance", {}).get("avg_technical_score", 78),
            "interview_readiness": snapshot.get("interview_performance", {}).get("avg_overall_score", 75)
        }

        predictions = self.predict_paths_for_candidate(skills_list, scores_data)

        if persist:
            pred_rec = CareerPathPrediction.query.filter_by(user_id=user_id).first()
            if not pred_rec:
                pred_rec = CareerPathPrediction(user_id=user_id)
                db.session.add(pred_rec)

            pred_rec.primary_role = predictions["primary_role"]
            pred_rec.primary_match_pct = predictions["primary_match_percentage"]
            pred_rec.set_predicted_roles(predictions["all_roles"])
            pred_rec.set_future_readiness({
                "competitiveness": predictions["competitiveness"],
                "top_paths": [p["role"] for p in predictions["top_paths"]]
            })
            db.session.commit()

        return predictions
