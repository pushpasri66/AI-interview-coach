class DifficultyEngine:
    """Adaptive difficulty engine dynamically adjusting question challenge level based on candidate performance."""

    def determine_next_difficulty(self, current_difficulty: str, last_score: int, avg_score: int = 75) -> str:
        """Determines next question difficulty level."""
        curr = current_difficulty.lower()

        if last_score >= 85 and avg_score >= 80:
            if curr == "easy":
                return "medium"
            elif curr == "medium":
                return "hard"
            else:
                return "hard"
        elif last_score < 50:
            if curr == "hard":
                return "medium"
            elif curr == "medium":
                return "easy"
            else:
                return "easy"
        else:
            return current_difficulty.lower()
