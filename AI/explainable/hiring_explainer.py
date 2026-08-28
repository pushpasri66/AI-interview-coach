from typing import Dict, Any, List


class HiringExplainer:
    """Explains recruiter hiring probability, screening pass rates, and seniority readiness."""

    def explain_hiring_probability(
        self,
        probability_score: int,
        target_role: str,
        target_company: str,
        strengths: List[str],
        blockers: List[str]
    ) -> Dict[str, Any]:
        """Provides explainable breakdown of recruiter hiring decision factors."""
        why_decision = (
            f"Recruiter screening match of {probability_score}% for {target_company} ({target_role}) "
            f"reflects candidate's verified {', '.join(strengths[:2]) if strengths else 'technical background'}. "
            f"{'Key gating criteria: ' + ', '.join(blockers[:2]) if blockers else 'No severe blockers identified.'}"
        )

        return {
            "hiring_probability": probability_score,
            "target_role": target_role,
            "target_company": target_company,
            "why_decision": why_decision,
            "hiring_strengths": strengths,
            "candidate_blockers": blockers,
            "key_hiring_indicators": [
                "Technical Screening Pass Likelihood: " + ("High (85%+)" if probability_score >= 80 else "Moderate (65%)"),
                "Resume ATS Alignment: " + ("Strong" if probability_score >= 75 else "Needs Keyword Optimization"),
                "Behavioral Competency: " + ("Consistent" if probability_score >= 70 else "Needs Practice")
            ]
        }
