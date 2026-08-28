import unittest
import jwt
import datetime
from app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.skill import Skill
from backend.models.career import CareerPlan
from backend.models.question_prediction import InterviewPrediction

from AI.question_prediction.question_predictor import QuestionPredictor
from AI.question_prediction.resume_question_engine import ResumeQuestionEngine
from AI.question_prediction.job_description_question_engine import JobDescriptionQuestionEngine
from AI.question_prediction.interview_probability import ProbabilityScorer


class TestQuestionPrediction(unittest.TestCase):
    """Unit tests for Phase 9 Step 3: AI Interview Question Prediction Engine."""

    @classmethod
    def setUpClass(cls):
        cls.app = create_app("testing")
        cls.app.config["TESTING"] = True
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        cls.app.config["SECRET_KEY"] = "question-secret-key-11223344"
        cls.app.config["WTF_CSRF_ENABLED"] = False
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.drop_all()

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.session.rollback()
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

        self.user = User(
            fullname="Morgan Vance",
            email=f"morgan_{datetime.datetime.utcnow().timestamp()}@example.com"
        )
        self.user.set_password("PredictPass2026!")
        db.session.add(self.user)
        db.session.commit()

        skills = [
            Skill(user_id=self.user.id, skill_name="Python", skill_level="Advanced"),
            Skill(user_id=self.user.id, skill_name="Machine Learning", skill_level="Intermediate"),
            Skill(user_id=self.user.id, skill_name="Docker", skill_level="Intermediate"),
            Skill(user_id=self.user.id, skill_name="SQL", skill_level="Advanced")
        ]
        db.session.add_all(skills)

        plan = CareerPlan(
            user_id=self.user.id,
            target_role="AI Engineer",
            duration_months=6,
            projects_to_build="CNN Image Classification Pipeline,Distributed FastAPI Microservice"
        )
        db.session.add(plan)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()
        self.app_context.pop()

    def generate_token(self, user_id: int) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            "iat": datetime.datetime.utcnow()
        }
        return jwt.encode(payload, self.app.config["SECRET_KEY"], algorithm="HS256")

    # --- 1. Probability Scorer Tests ---
    def test_01_probability_scorer_calculation(self):
        """Test probability score calculation based on project claims and evidence."""
        scorer = ProbabilityScorer()
        high_prob = scorer.compute_probability(
            category="Project",
            has_direct_project=True,
            has_resume_mention=True,
            role_importance="Critical"
        )
        self.assertGreaterEqual(high_prob, 90)

        moderate_prob = scorer.compute_probability(
            category="HR",
            role_importance="Medium"
        )
        self.assertGreaterEqual(moderate_prob, 50)
        self.assertLessEqual(moderate_prob, 85)

    # --- 2. Resume and Job Description Engine Tests ---
    def test_02_resume_question_engine(self):
        """Test ResumeQuestionEngine produces project and technical questions grounded in resume."""
        engine = ResumeQuestionEngine()
        questions = engine.generate_from_resume_and_projects(
            resume_data={},
            skills=["Python", "SQL", "Docker"],
            projects=["CNN Image Classification Pipeline"]
        )

        self.assertGreater(len(questions), 0)
        project_q = next((q for q in questions if q["category"] == "Project"), None)
        self.assertIsNotNone(project_q)
        self.assertIn("CNN", project_q["question"])
        self.assertGreaterEqual(project_q["probability_score"], 85)
        self.assertIn("reason", project_q)

    def test_03_job_description_and_company_engine(self):
        """Test JobDescriptionQuestionEngine generates company-specific and behavioral questions."""
        engine = JobDescriptionQuestionEngine()
        questions = engine.generate_company_and_jd_questions(
            target_company="Amazon",
            target_role="AI Engineer"
        )

        categories = {q["category"] for q in questions}
        self.assertIn("Behavioral", categories)
        self.assertIn("System Design", categories)
        self.assertIn("HR", categories)
        self.assertIn("Coding", categories)

    # --- 3. Master Question Predictor (All 7 Categories) ---
    def test_04_master_question_predictor_all_7_categories(self):
        """Test QuestionPredictor produces questions spanning all 7 required categories."""
        predictor = QuestionPredictor()
        result = predictor.predict_and_persist_for_user(
            user_id=self.user.id,
            target_role="AI Engineer",
            target_company="Google"
        )

        self.assertEqual(result["target_role"], "AI Engineer")
        self.assertEqual(result["target_company"], "Google")
        self.assertGreaterEqual(result["total_predicted_questions"], 5)
        self.assertGreaterEqual(result["highest_probability"], 85)

        predictions = result["predictions"]
        for q in predictions:
            self.assertIn("question", q)
            self.assertIn("probability_score", q)
            self.assertIn("difficulty", q)
            self.assertIn("category", q)
            self.assertIn("reason", q)
            self.assertIn("expected_focus_areas", q)

        # Verify DB persistence
        db_record = InterviewPrediction.query.filter_by(user_id=self.user.id).first()
        self.assertIsNotNone(db_record)
        self.assertEqual(db_record.target_role, "AI Engineer")
        self.assertGreater(len(db_record.get_predictions()), 0)

    # --- 4. API Endpoints ---
    def test_05_api_predictions_unauthenticated(self):
        """Test GET and POST /api/career/interview-predictions without auth return 401."""
        res_get = self.client.get("/api/career/interview-predictions")
        self.assertEqual(res_get.status_code, 401)

        res_post = self.client.post("/api/career/interview-predictions", json={})
        self.assertEqual(res_post.status_code, 401)

    def test_06_api_predictions_post_and_get_authenticated(self):
        """Test POST and GET /api/career/interview-predictions with valid JWT."""
        token = self.generate_token(self.user.id)
        headers = {"Authorization": f"Bearer {token}"}

        # Test POST
        payload = {
            "target_role": "Machine Learning Engineer",
            "target_company": "Microsoft",
            "job_description": "Seeking ML Engineer experienced in PyTorch, deep learning, and scalable systems."
        }
        res_post = self.client.post("/api/career/interview-predictions", json=payload, headers=headers)
        self.assertEqual(res_post.status_code, 201)
        data_post = res_post.get_json()
        self.assertTrue(data_post["success"])
        self.assertIn("interview_predictions", data_post)
        self.assertEqual(data_post["interview_predictions"]["target_role"], "Machine Learning Engineer")

        # Test GET
        res_get = self.client.get("/api/career/interview-predictions", headers=headers)
        self.assertEqual(res_get.status_code, 200)
        data_get = res_get.get_json()
        self.assertTrue(data_get["success"])
        self.assertIn("interview_predictions", data_get)
        self.assertGreaterEqual(data_get["interview_predictions"]["total_predicted_questions"], 5)


if __name__ == "__main__":
    unittest.main()
