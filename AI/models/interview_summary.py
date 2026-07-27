class InterviewSummaryGenerator:
    """Generates structured interview summary reports detailing strengths, weaknesses, and recommended action steps."""

    def generate_summary_report(self, candidate_name: str, interview_type: str, overall_score: int, tech_score: int, comm_score: int) -> dict:
        """Builds comprehensive interview summary report object."""
        strengths = []
        weaknesses = []
        actions = []

        if tech_score >= 80:
            strengths.append("Solid technical depth in Python and core engineering principles.")
        else:
            weaknesses.append("System Design and memory optimization depth.")
            actions.append("Practice system design and database indexing problems.")

        if comm_score >= 80:
            strengths.append("Clear verbal communication and articulate response delivery.")
        else:
            weaknesses.append("Pacing and filler word frequency.")
            actions.append("Pace responses to 140 words/min and reduce filler words.")

        actions.append("Complete 2 mock technical interviews weekly.")

        return {
            "candidate_name": candidate_name,
            "interview_type": interview_type,
            "overall_score": overall_score,
            "strengths": strengths if strengths else ["Good effort answering interview prompts."],
            "weaknesses": weaknesses if weaknesses else ["Minor continuous practice areas."],
            "recommended_actions": actions
        }
