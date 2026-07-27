class ResponseGenerator:
    """Constructs structured AI interviewer responses and follow-up prompts."""

    def format_interviewer_response(self, follow_up_question: str, feedback_comment: str = None) -> dict:
        """Formats response payload for client UI."""
        return {
            "ai_response": follow_up_question,
            "feedback_comment": feedback_comment or "Good response.",
            "status": "ready"
        }
