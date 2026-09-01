"""
Grammar checker model for the AI module.

Wraps the backend GrammarService to provide a consistent AI-layer
interface for grammar and fluency analysis, matching the pattern
used by other AI/ submodules.
"""
import sys
import os

# Allow imports from the project root when run directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from backend.services.grammar_service import GrammarService  # noqa: E402


class GrammarChecker:
    """
    AI-layer wrapper around GrammarService.

    Provides a clean interface for the AI pipeline to score answer
    grammar and fluency without coupling to Flask's application context.
    """

    def __init__(self):
        self._service = GrammarService()

    def check(self, text: str) -> dict:
        """
        Analyse *text* and return a grammar/fluency report.

        Returns:
            dict with keys: ``grammar_score``, ``fluency_score``,
            ``filler_count``, ``weak_phrase_count``,
            ``vocabulary_diversity``, ``avg_sentence_length``, ``feedback``.
        """
        return GrammarService.analyse(text)

    def score(self, text: str) -> int:
        """Return a single composite grammar score (0–100) for *text*."""
        return GrammarService.score_text(text)

    def is_fluent(self, text: str, threshold: int = 60) -> bool:
        """Return True if the composite grammar score meets *threshold*."""
        return self.score(text) >= threshold

    def batch_check(self, texts: list[str]) -> list[dict]:
        """
        Analyse a list of answer texts and return a report for each.

        Useful for scoring all answers in an interview session at once.
        """
        return [GrammarService.analyse(t) for t in texts]

    def batch_score(self, texts: list[str]) -> list[int]:
        """Return composite grammar scores for each text in *texts*."""
        return [GrammarService.score_text(t) for t in texts]

    def average_score(self, texts: list[str]) -> float:
        """Return the mean grammar score across all *texts*."""
        scores = self.batch_score(texts)
        if not scores:
            return 0.0
        return round(sum(scores) / len(scores), 1)
