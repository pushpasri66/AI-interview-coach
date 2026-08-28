import unittest
import jwt
import datetime
from app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.skill import Skill
from backend.models.career import CareerPlan
from backend.models.job_application import JobApplicationPackage

from AI.job_application.cover_letter_generator import CoverLetterGenerator
from AI.job_application.application_answer_generator import ApplicationAnswerGenerator
from AI.job_application.resume_tailor import ResumeTailor
from AI.job_application.application_engine import JobApplicationEngine


class TestJobApplication(unittest.TestCase):
    """Unit tests for Phase 9 Step 5: AI Job Application Assistant."""

    @classmethod
    def setUpClass(cls):
        cls.app = create_app("testing")
        cls.app.config["TESTING"] = True
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        cls.app.config["SECRET_KEY"] = "job-app-secret-key-334455"
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
            fullname="Casey Miller",
            email=f"casey_{datetime.datetime.utcnow().timestamp()}@example.com"
        )
        self.user.set_password("AppPass2026!")
        db.session.add(self.user)
        db.session.commit()

        skills = [
            Skill(user_id=self.user.id, skill_name="Python", skill_level="Advanced"),
            Skill(user_id=self.user.id, skill_name="SQL", skill_level="Advanced"),
            Skill(user_id=self.user.id, skill_name="Docker", skill_level="Intermediate"),
            Skill(user_id=self.user.id, skill_name="FastAPI", skill_level="Intermediate")
        ]
        db.session.add_all(skills)

        plan = CareerPlan(
            user_id=self.user.id,
            target_role="Full Stack Developer",
            duration_months=6,
            projects_to_build="Distributed Async Task Queue,Collaborative Kanban Board"
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

    # --- 1. Cover Letter Generator Tests ---
    def test_01_cover_letter_generator(self):
        """Test CoverLetterGenerator generates structured, personalized cover letters."""
        gen = CoverLetterGenerator()
        letter = gen.generate_cover_letter(
            candidate_name="Casey Miller",
            candidate_email="casey@example.com",
            company_name="Stripe",
            target_role="Backend Engineer",
            key_skills=["Python", "SQL", "Docker"],
            top_project="Distributed Async Task Queue"
        )

        self.assertIn("Stripe", letter)
        self.assertIn("Backend Engineer", letter)
        self.assertIn("Distributed Async Task Queue", letter)
        self.assertIn("Casey Miller", letter)

    # --- 2. Application Answer Generator Tests ---
    def test_02_application_answer_generator(self):
        """Test ApplicationAnswerGenerator produces tailored answers for screening questions."""
        gen = ApplicationAnswerGenerator()
        answers = gen.generate_screening_answers(
            company_name="Netflix",
            target_role="Senior Software Engineer",
            skills=["Python", "FastAPI"],
            top_project="High-Throughput Video Pipeline"
        )

        self.assertGreaterEqual(len(answers), 4)
        for a in answers:
            self.assertIn("question", a)
            self.assertIn("category", a)
            self.assertIn("answer", a)
            self.assertIn("key_talking_points", a)

    # --- 3. Resume Tailor & ATS Matching Tests ---
    def test_03_resume_tailor_and_ats_matching(self):
        """Test ResumeTailor ATS keyword matching, match score, and improvement tips."""
        tailor = ResumeTailor()
        jd = "Looking for a Python developer proficient in SQL, Docker, Redis, and Microservices."
        res = tailor.tailor_resume_content(
            candidate_name="Casey Miller",
            target_role="Software Engineer",
            company_name="Uber",
            candidate_skills=["Python", "SQL", "Docker", "FastAPI"],
            job_description=jd,
            existing_projects=["Distributed Task Worker"]
        )

        self.assertIn("tailored_summary", res)
        self.assertIn("tailored_bullet_points", res)
        self.assertIn("ats_keywords", res)
        self.assertGreater(res["job_match_score"], 50)
        self.assertGreater(res["application_readiness"], 50)
        self.assertIn("keyword_coverage_percentage", res["ats_keywords"])
        self.assertIsInstance(res["improvement_suggestions"], list)

    # --- 4. Master JobApplicationEngine Tests ---
    def test_04_master_application_engine_and_db_persistence(self):
        """Test JobApplicationEngine generates complete package and persists to DB."""
        engine = JobApplicationEngine()
        package = engine.generate_application_package(
            user_id=self.user.id,
            company_name="Datadog",
            target_role="Cloud Infrastructure Engineer",
            job_description="Seeking Cloud Engineer experienced in Docker, Python, and CI/CD.",
            persist=True
        )

        self.assertEqual(package["company_name"], "Datadog")
        self.assertEqual(package["target_role"], "Cloud Infrastructure Engineer")
        self.assertIn("scores", package)
        self.assertIn("cover_letter", package)
        self.assertIn("tailored_resume", package)
        self.assertIn("application_answers", package)
        self.assertIn("interview_questions", package)

        # Check DB record
        record = JobApplicationPackage.query.filter_by(user_id=self.user.id).first()
        self.assertIsNotNone(record)
        self.assertEqual(record.company_name, "Datadog")
        self.assertGreater(record.job_match_score, 0)
        self.assertIn("summary", record.get_tailored_resume())

        # Check history retrieval
        history = engine.get_application_history(self.user.id)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["company_name"], "Datadog")

    # --- 5. API Endpoints Tests ---
    def test_05_api_job_application_unauthenticated(self):
        """Test POST and GET /api/career/job-application without auth return 401."""
        res_post = self.client.post("/api/career/job-application", json={})
        self.assertEqual(res_post.status_code, 401)

        res_get = self.client.get("/api/career/job-application/history")
        self.assertEqual(res_get.status_code, 401)

    def test_06_api_job_application_validation(self):
        """Test POST /api/career/job-application with missing parameters returns 400."""
        token = self.generate_token(self.user.id)
        headers = {"Authorization": f"Bearer {token}"}

        res = self.client.post("/api/career/job-application", json={"company_name": "Google"}, headers=headers)
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertFalse(data["success"])
        self.assertIn("Missing required", data["error"])

    def test_07_api_job_application_post_and_history_success(self):
        """Test POST and GET /api/career/job-application with valid JWT token."""
        token = self.generate_token(self.user.id)
        headers = {"Authorization": f"Bearer {token}"}

        payload = {
            "company_name": "Snowflake",
            "target_role": "Data Systems Engineer",
            "job_description": "Proficiency in Python, SQL, Cloud Architecture, and Performance Optimization."
        }

        # 1. POST creation
        res_post = self.client.post("/api/career/job-application", json=payload, headers=headers)
        self.assertEqual(res_post.status_code, 201)
        data_post = res_post.get_json()
        self.assertTrue(data_post["success"])
        self.assertIn("job_application_package", data_post)
        self.assertEqual(data_post["job_application_package"]["company_name"], "Snowflake")

        # 2. GET history
        res_get = self.client.get("/api/career/job-application/history", headers=headers)
        self.assertEqual(res_get.status_code, 200)
        data_get = res_get.get_json()
        self.assertTrue(data_get["success"])
        self.assertEqual(data_get["total_applications"], 1)
        self.assertEqual(data_get["applications"][0]["company_name"], "Snowflake")


if __name__ == "__main__":
    unittest.main()
