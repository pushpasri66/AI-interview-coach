from typing import Dict, Any, List, Optional


class ScoreExplainer:
    """Provides transparent, explainable breakdowns for AI career readiness, match, and twin scores."""

    def explain_career_match_score(
        self,
        score_value: int,
        target_role: str,
        skill_scores: Dict[str, int],
        missing_skills: List[str],
        interview_scores: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Deconstructs the career match score into positive/negative factors and improvement actions."""
        positive_factors = []
        negative_factors = []
        improvement_actions = []

        # 1. Analyze high-performing skills (> 80)
        strong_skills = [s for s, val in skill_scores.items() if val >= 80]
        if strong_skills:
            positive_factors.append(
                f"High mastery demonstrated in core competencies: {', '.join(strong_skills[:3])} (averaging {int(sum(skill_scores[s] for s in strong_skills)/len(strong_skills))}%)"
            )

        # 2. Analyze moderate skills (60-79)
        moderate_skills = [s for s, val in skill_scores.items() if 60 <= val < 80]
        if moderate_skills:
            positive_factors.append(
                f"Foundational proficiency established in: {', '.join(moderate_skills[:2])}"
            )

        # 3. Analyze weak skills (< 60)
        weak_skills = [s for s, val in skill_scores.items() if val < 60]
        if weak_skills:
            negative_factors.append(
                f"Sub-optimal evaluation in {', '.join(weak_skills[:2])}, reducing technical readiness by ~15%."
            )
            for w in weak_skills[:2]:
                improvement_actions.append(f"Dedicate 45 minutes to fundamental tutorials and coding challenges in {w}.")

        # 4. Analyze missing skills
        if missing_skills:
            negative_factors.append(
                f"Absence of critical industry requirements for {target_role}: {', '.join(missing_skills[:3])}."
            )
            for m in missing_skills[:2]:
                improvement_actions.append(f"Build a mini-project integrating {m} to bridge target role gaps.")

        # 5. Analyze interview performance factors
        if interview_scores:
            avg_interview = interview_scores.get("average_score", 70)
            if avg_interview >= 80:
                positive_factors.append(f"Consistent verbal and technical interview performance (Score: {avg_interview}/100).")
            elif avg_interview < 65:
                negative_factors.append(f"Recent mock interview average ({avg_interview}/100) indicates nervousness or incomplete answers.")
                improvement_actions.append("Practice 2 timed AI mock interviews focusing on STAR method responses.")

        if not improvement_actions:
            improvement_actions.append(f"Undertake advanced system design challenges tailored for {target_role}.")

        why_generated = (
            f"Career Match score of {score_value}% for {target_role} reflects strong technical capability in "
            f"{', '.join(strong_skills[:2]) if strong_skills else 'core programming'}, offset by "
            f"{len(missing_skills)} missing prerequisite skill(s) ({', '.join(missing_skills[:2]) if missing_skills else 'advanced architecture'})."
        )

        return {
            "score_name": f"{target_role} Career Match",
            "score_value": score_value,
            "why_generated": why_generated,
            "sub_score_breakdown": skill_scores,
            "positive_factors": positive_factors,
            "negative_factors": negative_factors,
            "missing_skills": missing_skills,
            "improvement_actions": improvement_actions
        }
