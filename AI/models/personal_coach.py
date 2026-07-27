class PersonalCoach:
    """Personalized AI Interview Coach generating daily improvement plans and practice milestones."""

    def generate_daily_plan(self, user_name: str, avg_tech_score: int = 75, avg_comm_score: int = 80) -> dict:
        """Generates candidate daily improvement plan."""
        tasks = []

        if avg_tech_score < 80:
            tasks.append("Practice SQL joins & subquery optimization.")
            tasks.append("Revise core Machine Learning algorithms and bias-variance tradeoff.")
        else:
            tasks.append("Practice System Design for high-throughput distributed applications.")

        if avg_comm_score < 85:
            tasks.append("Improve speaking speed to an optimal 140 words/min cadence.")
            tasks.append("Reduce filler word usage ('um', 'uh', 'like').")
        else:
            tasks.append("Maintain high camera engagement & eye contact.")

        tasks.append("Complete 1 AI Mock Interview session.")

        return {
            "candidate_name": user_name,
            "today_plan": tasks[:3],
            "readiness_percentage": min(98, max(50, int((avg_tech_score * 0.6 + avg_comm_score * 0.4)))),
            "summary": f"Today's Plan: 1. {tasks[0]} 2. {tasks[1]} 3. {tasks[2]}"
        }
