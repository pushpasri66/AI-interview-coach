class AnswerImprover:
    """Suggests instant answer improvements and technical refinements."""

    def improve_answer(self, question: str, candidate_answer: str) -> dict:
        """Returns refined STAR-formatted answer suggestion."""
        ans = candidate_answer.strip() if candidate_answer else ""

        improved = (
            f"Stronger response: 'In my previous project addressing {question[:30]}..., I utilized {ans[:40]}... "
            "which improved system throughput by 35% and reduced latency to under 100ms.'"
        )

        return {
            "original_answer": candidate_answer,
            "improved_suggestion": improved,
            "key_addition": "Quantified performance metrics and architectural rationale."
        }
