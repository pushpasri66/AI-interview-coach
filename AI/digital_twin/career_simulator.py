from typing import Dict, Any, List


class CareerSimulator:
    """Simulates hypothetical career trajectories, skill acquisition scenarios, and interview practice curves."""

    def simulate_skill_acquisition(self, current_readiness: int, current_skills: List[str], acquired_skills: List[str]) -> Dict[str, Any]:
        """Projects score growth when candidate acquires specific high-impact skills."""
        unique_new = [s for s in acquired_skills if s.lower() not in [cs.lower() for cs in current_skills]]
        skill_boost = len(unique_new) * 4
        projected_readiness = min(98, current_readiness + skill_boost)

        return {
            "acquired_skills": unique_new,
            "previous_readiness": current_readiness,
            "projected_readiness": projected_readiness,
            "readiness_gain": projected_readiness - current_readiness,
            "status": "High Growth Potential" if skill_boost >= 8 else "Moderate Growth"
        }

    def simulate_interview_practice_curve(self, current_interview_readiness: int, additional_sessions: int) -> Dict[str, Any]:
        """Projects interview readiness score progression given additional practice sessions."""
        gain = int(min(25, additional_sessions * 3.5))
        projected = min(99, current_interview_readiness + gain)

        return {
            "additional_sessions": additional_sessions,
            "current_score": current_interview_readiness,
            "projected_score": projected,
            "confidence_boost_pct": min(30, additional_sessions * 5)
        }

    def simulate_milestone_trajectory(self, base_readiness: int, target_role: str = "Software Engineer") -> Dict[str, Any]:
        """Generates 1, 3, 6, and 12-month career progression milestones."""
        return {
            "target_role": target_role,
            "baseline_readiness": base_readiness,
            "milestones": [
                {
                    "timeline": "Month 1",
                    "focus": "Core fundamentals and resume keyword optimization",
                    "projected_readiness": min(95, base_readiness + 5)
                },
                {
                    "timeline": "Month 3",
                    "focus": "Mock interview sprint & system design mastery",
                    "projected_readiness": min(97, base_readiness + 12)
                },
                {
                    "timeline": "Month 6",
                    "focus": "High-impact portfolio projects & live peer coding",
                    "projected_readiness": min(99, base_readiness + 18)
                },
                {
                    "timeline": "Month 12",
                    "focus": "Senior-level readiness & cross-functional leadership",
                    "projected_readiness": min(100, base_readiness + 25)
                }
            ]
        }
