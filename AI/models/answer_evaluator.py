import re


class AnswerEvaluator:
    """Evaluates candidate answers against expected criteria and computes multi-metric AI scores."""

    TECHNICAL_KEYWORDS = [
        "algorithm", "architecture", "database", "latency", "performance", "optimization",
        "scale", "security", "framework", "concurrency", "asynchronous", "deployment",
        "complexity", "interface", "refactoring", "component", "testing", "pipeline",
        "forest", "tree", "bagging", "ensemble", "accuracy", "model", "data", "training"
    ]

    def evaluate_answer(self, question_text: str, expected_answer: str, user_answer: str, difficulty: str = "medium") -> dict:
        """Evaluates answer correctness, relevance, communication quality, and technical depth."""
        if not user_answer or not user_answer.strip():
            return {
                "overall_score": 0,
                "technical_score": 0,
                "communication_score": 0,
                "relevance_score": 0,
                "feedback": "No answer provided.",
                "strengths": "N/A",
                "improvements": "Please provide a complete verbal or written response to the question."
            }

        cleaned_user = user_answer.strip()
        word_count = len(cleaned_user.split())

        # 1. Technical Depth Score (0-100)
        expected_words = set(re.findall(r"\w+", expected_answer.lower()))
        user_words = set(re.findall(r"\w+", cleaned_user.lower()))
        
        common_words = expected_words.intersection(user_words)
        overlap_ratio = len(common_words) / max(1, len(expected_words))
        tech_kw_count = sum(1 for kw in self.TECHNICAL_KEYWORDS if kw in cleaned_user.lower())
        
        raw_tech_score = int(overlap_ratio * 60 + min(40, tech_kw_count * 10))
        technical_score = min(100, max(40, raw_tech_score))

        # 2. Relevance Score (0-100)
        q_words = set(re.findall(r"\w+", question_text.lower()))
        q_match = len(q_words.intersection(user_words)) / max(1, len(q_words))
        relevance_score = min(100, max(50, int(q_match * 70 + 40)))

        # 3. Communication Quality Score (0-100)
        if word_count >= 30:
            comm_score = 90
        elif word_count >= 12:
            comm_score = 80
        elif word_count >= 5:
            comm_score = 65
        else:
            comm_score = 45

        communication_score = comm_score

        # 4. Overall Weighted Score
        overall_score = min(100, int(technical_score * 0.50 + relevance_score * 0.30 + communication_score * 0.20))

        # Build Feedback
        strengths = []
        improvements = []

        if technical_score >= 70:
            strengths.append("Demonstrated solid technical understanding of core principles.")
        else:
            improvements.append("Elaborate further on architectural details and implementation mechanics.")

        if communication_score >= 75:
            strengths.append("Clear and well-structured answer explanation.")
        else:
            improvements.append("Provide a more detailed response using concrete real-world examples or STAR format.")

        if relevance_score >= 65:
            strengths.append("Directly addressed the core question prompt.")

        feedback_summary = f"Overall score: {overall_score}/100. Technical depth: {technical_score}%, Relevance: {relevance_score}%, Communication: {communication_score}%."

        return {
            "overall_score": overall_score,
            "technical_score": technical_score,
            "communication_score": communication_score,
            "relevance_score": relevance_score,
            "feedback": feedback_summary,
            "strengths": " ".join(strengths) if strengths else "Good effort answering the prompt.",
            "improvements": " ".join(improvements) if improvements else "Focus on continuous practice and adding metric results."
        }
