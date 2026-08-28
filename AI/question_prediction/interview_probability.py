from typing import Dict, Any, List


class ProbabilityScorer:
    """Calculates interview question probability scores based on candidate profile evidence and market factors."""

    def compute_probability(
        self,
        category: str,
        has_direct_project: bool = False,
        has_resume_mention: bool = False,
        is_known_skill_gap: bool = False,
        is_company_core_theme: bool = False,
        role_importance: str = "High"
    ) -> int:
        """Calculates 0-100% probability based on multi-factor evidentiary weighting."""
        base_score = 65

        if has_direct_project:
            base_score += 24  # High likelihood of project deep dive
        elif has_resume_mention:
            base_score += 18

        if is_company_core_theme:
            base_score += 15

        if is_known_skill_gap:
            base_score += 10  # Interviewers probe candidate weaker areas

        if role_importance == "Critical":
            base_score += 8
        elif role_importance == "High":
            base_score += 4

        # Category normalization
        if category in ["Project", "Technical", "Company-specific"]:
            base_score += 3

        return min(98, max(45, base_score))
