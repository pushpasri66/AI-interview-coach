"""
Core AI Service for the AI Interview Coach platform.

Provides rule-based and heuristic AI capabilities for interview question
generation, answer scoring, feedback synthesis, and career recommendations.
All logic runs locally with no external API dependency by default; swap out
``_call_llm`` to plug in OpenAI, Gemini, or any other LLM backend.
"""
import re
import os
import random
from datetime import datetime
from flask import current_app


# ──────────────────────────────────────────────
# Question banks (rule-based fallback)
# ──────────────────────────────────────────────

_HR_QUESTIONS = [
    "Tell me about yourself.",
    "Why do you want to work at this company?",
    "Where do you see yourself in 5 years?",
    "What are your greatest strengths and weaknesses?",
    "Describe a challenging situation you faced and how you resolved it.",
    "Why are you leaving your current role?",
    "How do you handle pressure and tight deadlines?",
    "Tell me about a time you worked effectively in a team.",
]

_TECHNICAL_QUESTIONS = [
    "Explain the difference between a stack and a queue.",
    "What is the time complexity of binary search?",
    "Describe the SOLID principles of software design.",
    "What is the difference between REST and GraphQL?",
    "Explain how a hash table works internally.",
    "What is the CAP theorem in distributed systems?",
    "Describe your experience with CI/CD pipelines.",
    "What is the difference between SQL and NoSQL databases?",
]

_BEHAVIORAL_QUESTIONS = [
    "Give an example of a goal you reached and how you achieved it.",
    "Describe a time you had a conflict with a team member. How did you handle it?",
    "Tell me about a time you showed leadership.",
    "Give an example of when you had to learn something quickly.",
    "Describe a time you failed and what you learned from it.",
]


class AIService:
    """
    Centralized AI service providing question generation, answer scoring,
    and feedback synthesis for the AI Interview Coach platform.
    """

    # ──────────────────────────────────────────
    # Question generation
    # ──────────────────────────────────────────

    @staticmethod
    def generate_questions(
        interview_type: str = "hr",
        difficulty: str = "medium",
        count: int = 5,
        role: str = "",
    ) -> list[dict]:
        """
        Generate interview questions for the given *interview_type* and *difficulty*.

        Returns a list of question dicts with keys: ``question``, ``type``, ``difficulty``.
        """
        bank = {
            "hr": _HR_QUESTIONS,
            "behavioral": _BEHAVIORAL_QUESTIONS,
            "technical": _TECHNICAL_QUESTIONS,
        }.get(interview_type.lower(), _HR_QUESTIONS)

        selected = random.sample(bank, min(count, len(bank)))
        return [
            {
                "question": q,
                "type": interview_type,
                "difficulty": difficulty,
                "order": idx + 1,
            }
            for idx, q in enumerate(selected)
        ]

    # ──────────────────────────────────────────
    # Answer scoring
    # ──────────────────────────────────────────

    @staticmethod
    def score_answer(question: str, answer: str) -> dict:
        """
        Score a candidate's *answer* to a *question* using heuristic analysis.

        Returns a dict with keys: ``score`` (0-100), ``feedback``, ``keywords_found``.
        """
        if not answer or not answer.strip():
            return {
                "score": 0,
                "feedback": "No answer provided.",
                "keywords_found": [],
                "word_count": 0,
            }

        words = answer.lower().split()
        word_count = len(words)

        # Base score on answer length (up to 60 points)
        length_score = min(60, word_count * 2)

        # Bonus points for structure keywords (up to 40 points)
        structure_keywords = [
            "because", "therefore", "however", "for example", "specifically",
            "result", "achieved", "improved", "led", "managed", "implemented",
            "problem", "solution", "team", "success", "challenge",
        ]
        found = [kw for kw in structure_keywords if kw in answer.lower()]
        keyword_score = min(40, len(found) * 5)

        score = min(100, length_score + keyword_score)

        # Generate feedback
        feedback_parts = []
        if word_count < 30:
            feedback_parts.append("Try to provide a more detailed answer with specific examples.")
        if not found:
            feedback_parts.append("Use structured language — explain cause, action, and result.")
        if score >= 80:
            feedback_parts.append("Excellent answer with strong structure and detail.")
        elif score >= 60:
            feedback_parts.append("Good answer. Adding more concrete examples would strengthen it.")
        else:
            feedback_parts.append("Consider the STAR method: Situation, Task, Action, Result.")

        return {
            "score": round(score),
            "feedback": " ".join(feedback_parts) if feedback_parts else "Good answer.",
            "keywords_found": found,
            "word_count": word_count,
        }

    # ──────────────────────────────────────────
    # Overall interview feedback
    # ──────────────────────────────────────────

    @staticmethod
    def generate_interview_feedback(answers: list[dict]) -> dict:
        """
        Aggregate per-answer scores and generate overall interview feedback.

        *answers* should be a list of dicts with ``score`` and ``feedback`` keys.
        Returns a dict with ``overall_score``, ``grade``, ``summary``, ``improvements``.
        """
        if not answers:
            return {
                "overall_score": 0,
                "grade": "F",
                "summary": "No answers recorded.",
                "improvements": [],
            }

        scores = [a.get("score", 0) for a in answers]
        overall = round(sum(scores) / len(scores))

        grade_map = [(90, "A+"), (80, "A"), (70, "B"), (60, "C"), (50, "D")]
        grade = next((g for threshold, g in grade_map if overall >= threshold), "F")

        summary = (
            f"You completed {len(answers)} question(s) with an overall score of {overall}/100."
        )

        improvements = []
        if overall < 60:
            improvements.append("Practice the STAR method for behavioral questions.")
            improvements.append("Work on providing more structured, detailed answers.")
        if overall < 80:
            improvements.append("Use specific numbers and outcomes to quantify your impact.")
        if overall >= 80:
            improvements.append("Polish your answers with industry-specific terminology.")

        return {
            "overall_score": overall,
            "grade": grade,
            "summary": summary,
            "improvements": improvements,
        }

    # ──────────────────────────────────────────
    # LLM integration hook (plug-in ready)
    # ──────────────────────────────────────────

    @staticmethod
    def _call_llm(prompt: str) -> str:
        """
        Placeholder for LLM API calls.

        Replace this method to integrate with OpenAI, Google Gemini, Anthropic Claude,
        or any other provider. Currently returns an empty string (disabled).
        """
        api_key = os.getenv("AI_API_KEY", "")
        if not api_key or api_key == "replace-with-your-ai-api-key":
            current_app.logger.debug("AI_API_KEY not configured — LLM calls are disabled.")
            return ""
        # TODO: Implement actual LLM API call here
        return ""
