"""
Grammar analysis service for the AI Interview Coach platform.

Provides heuristic grammar and fluency scoring for candidate interview
answers without requiring an external API. Scores vocabulary diversity,
sentence structure, filler-word usage, and answer coherence.
"""
import re


# ──────────────────────────────────────────────
# Filler words / weak language patterns
# ──────────────────────────────────────────────

FILLER_WORDS = {
    "um", "uh", "like", "you know", "sort of", "kind of", "basically",
    "literally", "actually", "right", "so", "well", "i mean", "i guess",
}

WEAK_PHRASES = {
    "i think maybe", "i'm not sure", "i don't know", "possibly",
    "might be", "could be", "i was just",
}


# ──────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────

class GrammarService:
    """Heuristic grammar and fluency analyser for spoken/written interview answers."""

    @staticmethod
    def analyse(text: str) -> dict:
        """
        Analyse *text* for grammar quality and fluency.

        Returns a dict with:
        - ``grammar_score`` (0–100)
        - ``fluency_score`` (0–100)
        - ``filler_count`` — number of filler-word occurrences
        - ``weak_phrase_count`` — number of weak-language occurrences
        - ``vocabulary_diversity`` — unique word ratio (0.0–1.0)
        - ``avg_sentence_length`` — mean word count per sentence
        - ``feedback`` — list of improvement suggestions
        """
        if not text or not text.strip():
            return {
                "grammar_score": 0,
                "fluency_score": 0,
                "filler_count": 0,
                "weak_phrase_count": 0,
                "vocabulary_diversity": 0.0,
                "avg_sentence_length": 0.0,
                "feedback": ["No text provided for analysis."],
            }

        text_lower = text.lower()
        words = re.findall(r"\b\w+\b", text_lower)
        sentences = re.split(r"[.!?]+", text)
        sentences = [s.strip() for s in sentences if s.strip()]

        # Filler word count
        filler_count = sum(
            text_lower.count(fw) for fw in FILLER_WORDS
        )

        # Weak phrase count
        weak_count = sum(
            text_lower.count(wp) for wp in WEAK_PHRASES
        )

        # Vocabulary diversity (type-token ratio)
        vocab_diversity = len(set(words)) / len(words) if words else 0.0

        # Average sentence length
        word_counts = [len(re.findall(r"\b\w+\b", s)) for s in sentences]
        avg_sentence_length = sum(word_counts) / len(word_counts) if word_counts else 0.0

        # ── Score calculation ──────────────────
        # Fluency (penalise filler words and weak phrases)
        fluency_deduction = min(40, (filler_count * 3) + (weak_count * 5))
        fluency_score = max(0, 100 - fluency_deduction)

        # Grammar (reward vocabulary diversity and sentence variety)
        diversity_score = min(60, int(vocab_diversity * 80))
        length_score = 40 if 10 <= avg_sentence_length <= 25 else 20
        grammar_score = min(100, diversity_score + length_score)

        # ── Feedback ──────────────────────────
        feedback = []
        if filler_count > 3:
            feedback.append(
                f"You used {filler_count} filler word(s) (e.g. 'um', 'like', 'basically'). "
                "Practice pausing instead of using fillers."
            )
        if weak_count > 1:
            feedback.append(
                "Avoid tentative phrases like 'I'm not sure' or 'I think maybe'. "
                "Speak with confidence."
            )
        if vocab_diversity < 0.4:
            feedback.append(
                "Expand your vocabulary — try to vary your word choices for a more impactful answer."
            )
        if avg_sentence_length > 30:
            feedback.append(
                "Your sentences are quite long. Break complex ideas into shorter, clearer statements."
            )
        if avg_sentence_length < 5 and sentences:
            feedback.append(
                "Your answers are very brief. Aim for 2–3 detailed sentences per point."
            )
        if not feedback:
            feedback.append("Great fluency and vocabulary — keep it up!")

        return {
            "grammar_score": grammar_score,
            "fluency_score": fluency_score,
            "filler_count": filler_count,
            "weak_phrase_count": weak_count,
            "vocabulary_diversity": round(vocab_diversity, 3),
            "avg_sentence_length": round(avg_sentence_length, 1),
            "feedback": feedback,
        }

    @staticmethod
    def score_text(text: str) -> int:
        """
        Convenience wrapper — return a single composite grammar/fluency score (0–100).
        """
        result = GrammarService.analyse(text)
        return round((result["grammar_score"] + result["fluency_score"]) / 2)
