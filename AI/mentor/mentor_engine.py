class MentorEngine:
    """AI Career Mentor conversational system providing personalized career guidance."""

    def advise_candidate(self, candidate_name: str, target_role: str, user_goals: str = None) -> dict:
        """Generates candidate career advice response."""
        advice = (
            f"Hello {candidate_name}! To advance toward your target role as an {target_role}, focus on "
            "deepening production MLOps practices, containerizing applications with Docker, and building "
            "scalable database architectures. Maintain a consistent practice cadence of 2 mock interviews per week."
        )
        return {
            "mentor_name": "AI Career Mentor (Dr. Evelyn)",
            "advice": advice,
            "status": "success"
        }
