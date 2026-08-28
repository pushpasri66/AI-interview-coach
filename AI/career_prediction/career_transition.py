from typing import Dict, Any, List
from AI.career_prediction.role_predictor import RolePredictor


class CareerTransitionEngine:
    """Computes cross-domain transition feasibility, skill bridges, and milestone roadmaps."""

    def __init__(self):
        self.role_evaluator = RolePredictor()

    def generate_transition_plan(self, current_role: str, target_role: str, current_skills: List[str]) -> Dict[str, Any]:
        """Calculates transition roadmap between two roles."""
        target_info = self.role_evaluator.ROLES_CATALOG.get(target_role, self.role_evaluator.ROLES_CATALOG["Software Engineer"])
        required = target_info["required_skills"]

        norm_current = {s.lower().strip() for s in current_skills}
        overlap = [req for req in required if any(req.lower() in cs or cs in req.lower() for cs in norm_current)]
        gaps = [req for req in required if not any(req.lower() in cs or cs in req.lower() for cs in norm_current)]

        overlap_pct = int((len(overlap) / max(1, len(required))) * 100)

        if overlap_pct >= 60:
            feasibility = "High (Direct Progression)"
            duration_months = 2
        elif overlap_pct >= 35:
            feasibility = "Moderate (Strategic Upskilling)"
            duration_months = 4
        else:
            feasibility = "Pivot Required (Comprehensive Re-skilling)"
            duration_months = 6

        roadmap = [
            {
                "phase": "Phase 1: Fundamental Bridge",
                "timeline": f"Weeks 1-{max(2, duration_months * 2)}",
                "focus": f"Master initial high-priority gaps: {', '.join(gaps[:2]) if gaps else 'Core Concepts'}",
                "deliverables": "Theory, guided tutorials, and coding problem sets."
            },
            {
                "phase": "Phase 2: Project & System Mastery",
                "timeline": f"Weeks {max(3, duration_months * 2 + 1)}-{duration_months * 3}",
                "focus": f"Build: {target_info['recommended_projects'][0]}",
                "deliverables": "Production-grade GitHub repo with architecture documentation."
            },
            {
                "phase": "Phase 3: Certification & Mock Interviews",
                "timeline": f"Weeks {duration_months * 3 + 1}-{duration_months * 4}",
                "focus": f"Target Certification: {target_info['certifications'][0]}",
                "deliverables": "5+ Domain mock interviews and tailored resume updates."
            }
        ]

        return {
            "from_role": current_role,
            "to_role": target_role,
            "skill_overlap_percentage": overlap_pct,
            "transferable_skills": overlap,
            "skills_to_acquire": gaps,
            "transition_feasibility": feasibility,
            "estimated_duration_months": duration_months,
            "recommended_certifications": target_info["certifications"],
            "roadmap": roadmap
        }
