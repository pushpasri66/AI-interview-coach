"""
Unit tests for the core AI Service module.
"""
import unittest
from app import create_app
from backend.database import db
from backend.services.ai_service import AIService


class TestAIService(unittest.TestCase):
    """Tests for AIService question generation, scoring, and feedback."""

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    # ── Question generation ─────────────────────────────────────────────────

    def test_01_generate_hr_questions(self):
        """generate_questions returns the requested number of HR questions."""
        questions = AIService.generate_questions(interview_type="hr", count=3)
        self.assertIsInstance(questions, list)
        self.assertLessEqual(len(questions), 3)
        for q in questions:
            self.assertIn("question", q)
            self.assertEqual(q["type"], "hr")

    def test_02_generate_technical_questions(self):
        """generate_questions returns technical questions when type='technical'."""
        questions = AIService.generate_questions(interview_type="technical", count=5)
        self.assertIsInstance(questions, list)
        for q in questions:
            self.assertEqual(q["type"], "technical")

    def test_03_generate_behavioral_questions(self):
        """generate_questions returns behavioral questions."""
        questions = AIService.generate_questions(interview_type="behavioral", count=2)
        self.assertIsInstance(questions, list)
        self.assertLessEqual(len(questions), 2)

    def test_04_generate_unknown_type_falls_back_to_hr(self):
        """Unknown interview types fall back to HR question bank."""
        questions = AIService.generate_questions(interview_type="unknown_type", count=2)
        self.assertIsInstance(questions, list)

    # ── Answer scoring ──────────────────────────────────────────────────────

    def test_05_score_empty_answer_returns_zero(self):
        """Empty answers score 0."""
        result = AIService.score_answer("Tell me about yourself.", "")
        self.assertEqual(result["score"], 0)

    def test_06_score_short_answer_low_score(self):
        """Very short answers score lower than detailed answers."""
        short = AIService.score_answer("Tell me about yourself.", "I am a developer.")
        long = AIService.score_answer(
            "Tell me about yourself.",
            "I am a software engineer with 3 years of experience building scalable "
            "web applications. I have led teams, implemented CI/CD pipelines, and "
            "improved system performance by 40%. I am passionate about clean code "
            "and continuous learning. For example, I recently completed a course on "
            "distributed systems to further develop my technical skills.",
        )
        self.assertLess(short["score"], long["score"])

    def test_07_score_answer_returns_required_keys(self):
        """score_answer always returns score, feedback, keywords_found, word_count."""
        result = AIService.score_answer("Why do you want this job?", "Because I am passionate.")
        self.assertIn("score", result)
        self.assertIn("feedback", result)
        self.assertIn("keywords_found", result)
        self.assertIn("word_count", result)

    def test_08_score_is_in_valid_range(self):
        """score_answer always returns a score between 0 and 100."""
        result = AIService.score_answer("Question?", "A" * 500)
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)

    # ── Overall feedback ────────────────────────────────────────────────────

    def test_09_feedback_empty_answers(self):
        """generate_interview_feedback handles empty answer list."""
        result = AIService.generate_interview_feedback([])
        self.assertEqual(result["overall_score"], 0)

    def test_10_feedback_calculates_average(self):
        """generate_interview_feedback correctly averages scores."""
        answers = [{"score": 80}, {"score": 60}, {"score": 70}]
        result = AIService.generate_interview_feedback(answers)
        self.assertEqual(result["overall_score"], 70)

    def test_11_feedback_assigns_grade(self):
        """generate_interview_feedback assigns a letter grade."""
        answers = [{"score": 95}]
        result = AIService.generate_interview_feedback(answers)
        self.assertIn(result["grade"], ["A+", "A", "B", "C", "D", "F"])

    def test_12_feedback_includes_improvements(self):
        """generate_interview_feedback always returns an improvements list."""
        answers = [{"score": 40}]
        result = AIService.generate_interview_feedback(answers)
        self.assertIsInstance(result["improvements"], list)
        self.assertGreater(len(result["improvements"]), 0)


if __name__ == "__main__":
    unittest.main()
