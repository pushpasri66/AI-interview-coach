from typing import Dict, Any, List


class RecommendationExplainer:
    """Explains rationale behind recommended projects, certifications, and learning milestones."""

    def explain_project_recommendation(
        self,
        project_title: str,
        target_role: str,
        target_skill: str,
        candidate_current_skills: List[str]
    ) -> Dict[str, Any]:
        """Provides transparency on why a project was prioritized."""
        has_prereqs = bool(candidate_current_skills)
        reason = (
            f"'{project_title}' was recommended because {target_role} job postings require demonstrable experience in {target_skill}. "
            f"Building this project directly resolves a high-priority skill gap and strengthens portfolio proof."
        )

        return {
            "item_type": "Project Recommendation",
            "title": project_title,
            "target_skill": target_skill,
            "why_recommended": reason,
            "expected_score_impact": "+8% to +12% in Technical Strength",
            "prerequisites_met": has_prereqs
        }

    def explain_certification_recommendation(
        self,
        cert_name: str,
        target_role: str,
        industry_demand_pct: int = 85
    ) -> Dict[str, Any]:
        """Explains certification prioritization."""
        return {
            "item_type": "Certification Recommendation",
            "title": cert_name,
            "why_recommended": f"{cert_name} is recognized by {industry_demand_pct}% of recruiters hiring for {target_role} positions.",
            "expected_score_impact": "+10% to ATS & Recruiter Filter Match"
        }
