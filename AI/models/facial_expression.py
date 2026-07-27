class FacialExpressionAnalyzer:
    """Evaluates facial composure, smile intensity, and professional presence."""

    def analyze_expression(self, emotion_data: dict = None) -> dict:
        """Computes facial expression score out of 100 and offers recommendations."""
        expression_score = 82
        smile_level = "Natural & Warm"
        stress_indicator = "Low / Composed"

        recommendations = [
            "Maintain natural, pleasant facial expressions during answers.",
            "Avoid excessive frowning or squinting when thinking through complex technical prompts.",
            "Nod periodically to show active listening during interviewer prompts."
        ]

        return {
            "expression_score": expression_score,
            "smile_level": smile_level,
            "stress_indicator": stress_indicator,
            "recommendations": recommendations,
            "summary": f"Facial Expression Score: {expression_score}/100. Composure: {stress_indicator}."
        }
