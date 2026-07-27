class ConversationMemory:
    """Manages conversational history and context windows for dynamic AI interview follow-ups."""

    def __init__(self):
        self._history = []

    def add_exchange(self, question: str, candidate_answer: str, ai_feedback: str = None) -> None:
        """Appends a Q&A exchange to conversation memory."""
        self._history.append({
            "question": question,
            "answer": candidate_answer,
            "feedback": ai_feedback
        })

    def get_history(self) -> list:
        """Returns complete conversation history."""
        return self._history

    def get_last_exchange(self) -> dict:
        """Returns last Q&A exchange."""
        return self._history[-1] if self._history else None

    def clear(self) -> None:
        """Clears memory history."""
        self._history.clear()
