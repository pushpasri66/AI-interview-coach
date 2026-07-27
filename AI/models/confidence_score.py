class ConfidenceScorer:
    """Evaluates candidate confidence level based on speech rate, pauses, filler words, and vocal stability."""

    FILLER_WORDS = ["um", "uh", "like", "you know", "ah", "basically", "actually", "so", "right"]

    def compute_confidence(self, text: str, word_count: int, duration_sec: float = 60.0, filler_count: int = None, pause_sec: float = 0.0) -> dict:
        """Calculates 100-point confidence score and generates feedback."""
        if not text or not text.strip():
            return {
                "confidence_score": 50,
                "strengths": ["Clear attempt at response."],
                "improvements": ["Provide a complete verbal response to demonstrate confidence."]
            }

        cleaned = text.lower()
        
        # Calculate filler words count if not passed directly
        if filler_count is None:
            filler_count = sum(cleaned.count(word) for word in self.FILLER_WORDS)

        # 1. Speech Rate Score (Optimal: 120 - 160 words per minute)
        wpm = (word_count / max(10, duration_sec)) * 60
        if 120 <= wpm <= 160:
            rate_score = 30
        elif 90 <= wpm < 120 or 160 < wpm <= 190:
            rate_score = 22
        else:
            rate_score = 15

        # 2. Filler Word Penalty (Max 35 pts)
        filler_penalty = min(25, filler_count * 4)
        filler_score = max(10, 35 - filler_penalty)

        # 3. Sentence Structure & Length (Max 35 pts)
        if word_count >= 40:
            length_score = 35
        elif word_count >= 20:
            length_score = 25
        else:
            length_score = 15

        total_confidence = min(100, max(30, rate_score + filler_score + length_score))

        strengths = []
        improvements = []

        if rate_score >= 25:
            strengths.append("Excellent, steady speaking pace (optimal cadence).")
        elif wpm < 120:
            improvements.append("Increase speaking pace slightly to convey enthusiasm and readiness.")
        else:
            improvements.append("Slow down your speaking pace slightly to ensure clear articulation.")

        if filler_count <= 2:
            strengths.append("Minimal filler word usage ('um', 'uh', 'like').")
        else:
            improvements.append(f"Reduce filler word frequency ({filler_count} detected); pause silently instead.")

        if word_count >= 30:
            strengths.append("Articulate and comprehensive answer delivery.")

        return {
            "confidence_score": total_confidence,
            "speech_rate_wpm": int(wpm),
            "filler_count": filler_count,
            "strengths": strengths if strengths else ["Good voice delivery."],
            "improvements": improvements if improvements else ["Maintain current confident speaking habits."]
        }
