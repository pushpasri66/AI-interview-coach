import os
import unittest
import io
from app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.interview import Interview, Question, Answer
from AI.models.question_generator import QuestionGenerator
from AI.models.answer_evaluator import AnswerEvaluator
from backend.services.speech_service import SpeechService
from backend.services.coding_service import CodingService
from backend.services.interview_report_service import InterviewReportService


class TestInterviewEngine(unittest.TestCase):
    """Unit tests for Phase 3 AI Interview Engine & Mock Interview Platform."""

    def setUp(self):
        self.app = create_app("development")
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.client = self.app.test_client()

        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create test user
        self.user = User.query.filter_by(email="interview_tester@example.com").first()
        if not self.user:
            self.user = User(fullname="Interview Tester", email="interview_tester@example.com")
            self.user.set_password("Password123!")
            db.session.add(self.user)
            db.session.commit()

        # Login client
        self.client.post("/login", data={
            "email": "interview_tester@example.com",
            "password": "Password123!"
        })

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_01_question_generator(self):
        """Test question generation for different interview types."""
        generator = QuestionGenerator()

        hr_q = generator.generate_questions("hr", count=5)
        self.assertEqual(len(hr_q), 5)
        self.assertIn("question_text", hr_q[0])

        tech_q = generator.generate_questions("technical", category="python", count=3)
        self.assertEqual(len(tech_q), 3)

        comp_q = generator.generate_questions("company", company_name="Google", count=3)
        self.assertEqual(len(comp_q), 3)

    def test_02_answer_evaluator(self):
        """Test multi-metric answer evaluation AI."""
        evaluator = AnswerEvaluator()
        question_text = "What is a Random Forest algorithm and how does it work?"
        expected_answer = "Random Forest is an ensemble learning method constructing multiple decision trees during training and outputting the mode of the classes."
        user_answer = "Random Forest builds multiple decision trees using bagging to produce high accuracy algorithms."

        eval_res = evaluator.evaluate_answer(question_text, expected_answer, user_answer)

        self.assertGreaterEqual(eval_res["overall_score"], 50)
        self.assertIn("technical_score", eval_res)
        self.assertIn("communication_score", eval_res)
        self.assertIsNotNone(eval_res["feedback"])

    def test_03_coding_service_execution(self):
        """Test safe Python code execution service."""
        coding_svc = CodingService()
        code = "def add(a, b):\n    return a + b\nprint('Result:', add(5, 7))"

        res = coding_svc.execute_python_code(code)
        self.assertTrue(res["success"])
        self.assertIn("Result: 12", res["output"])

    def test_04_interview_session_creation_and_answer(self):
        """Test creating an interview session via HTTP endpoints."""
        gen_resp = self.client.post("/interview/generate", data={
            "interview_type": "hr",
            "difficulty": "medium"
        }, follow_redirects=True)

        self.assertEqual(gen_resp.status_code, 200)

        interview_obj = Interview.query.filter_by(user_id=self.user.id).order_by(Interview.id.desc()).first()
        self.assertIsNotNone(interview_obj)
        self.assertEqual(interview_obj.interview_type, "hr")

        questions = Question.query.filter_by(interview_id=interview_obj.id).all()
        self.assertGreater(len(questions), 0)

        # Submit answer
        ans_resp = self.client.post("/interview/answer", json={
            "interview_id": interview_obj.id,
            "question_id": questions[0].id,
            "user_answer": "I am a dedicated software engineer with strong technical problem solving skills."
        })

        self.assertEqual(ans_resp.status_code, 200)
        json_data = ans_resp.get_json()
        self.assertTrue(json_data["success"])
        self.assertGreater(json_data["score"], 0)

    def test_05_interview_pdf_report_service(self):
        """Test PDF interview report generation."""
        interview_obj = Interview(
            user_id=self.user.id,
            interview_type="technical",
            category="python",
            difficulty="medium",
            total_questions=2,
            score=88,
            status="completed"
        )
        db.session.add(interview_obj)
        db.session.commit()

        q = Question(
            interview_id=interview_obj.id,
            question_text="Explain Python GIL.",
            category="Python",
            expected_answer="Global Interpreter Lock"
        )
        db.session.add(q)
        db.session.commit()

        ans = Answer(
            question_id=q.id,
            interview_id=interview_obj.id,
            user_answer="GIL restricts multi-threaded CPython execution.",
            answer_score=85,
            feedback="Good concise explanation."
        )
        db.session.add(ans)
        db.session.commit()

        report_svc = InterviewReportService()
        report_path = report_svc.generate_pdf_report(self.user.fullname, interview_obj, [q], {q.id: ans})

        self.assertTrue(report_path.startswith("reports/interview_reports/"))
        abs_path = os.path.abspath(os.path.join(self.app.root_path, report_path))
        self.assertTrue(os.path.exists(abs_path))


if __name__ == "__main__":
    unittest.main()
