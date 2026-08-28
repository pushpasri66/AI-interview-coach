import unittest
import jwt
import datetime
from app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.skill import Skill
from backend.models.career import CareerPlan
from backend.models.career_prediction import CareerPathPrediction

from AI.career_prediction.role_predictor import RolePredictor
from AI.career_prediction.career_path_predictor import CareerPathPredictor
from AI.career_prediction.career_transition import CareerTransitionEngine
from AI.career_prediction.future_role_predictor import FutureRolePredictor


class TestCareerPrediction(unittest.TestCase):
    """Unit tests for Phase 9 Step 2: Predictive Career Path Intelligence."""

    @classmethod
    def setUpClass(cls):
        cls.app = create_app("testing")
        cls.app.config["TESTING"] = True
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        cls.app.config["SECRET_KEY"] = "career-secret-key-998877"
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
            fullname="Jordan Lee",
            email=f"jordan_{datetime.datetime.utcnow().timestamp()}@example.com"
        )
        self.user.set_password("SecurePass2026!")
        db.session.add(self.user)
        db.session.commit()

        skills = [
            Skill(user_id=self.user.id, skill_name="Python", skill_level="Advanced"),
            Skill(user_id=self.user.id, skill_name="Machine Learning", skill_level="Intermediate"),
            Skill(user_id=self.user.id, skill_name="SQL", skill_level="Advanced"),
            Skill(user_id=self.user.id, skill_name="Deep Learning", skill_level="Intermediate"),
            Skill(user_id=self.user.id, skill_name="PyTorch", skill_level="Intermediate"),
            Skill(user_id=self.user.id, skill_name="Docker", skill_level="Intermediate")
        ]
        db.session.add_all(skills)

        plan = CareerPlan(
            user_id=self.user.id,
            target_role="AI Engineer",
            duration_months=6
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

    # --- 1. RolePredictor Tests Across 9 Roles ---
    def test_01_role_predictor_all_9_roles(self):
        """Test RolePredictor calculates match %, skills, projects, certs, prep time, and growth for all 9 roles."""
        predictor = RolePredictor()
        candidate_skills = {"Python", "SQL", "Machine Learning", "PyTorch", "Docker"}
        candidate_scores = {"technical_strength": 85, "interview_readiness": 80}

        expected_roles = [
            "AI Engineer",
            "Machine Learning Engineer",
            "Data Scientist",
            "Data Analyst",
            "Software Engineer",
            "Full Stack Developer",
            "Cloud Engineer",
            "DevOps Engineer",
            "Cybersecurity Engineer"
        ]

        self.assertEqual(len(predictor.ROLES_CATALOG), 9)

        for role_name in expected_roles:
            eval_res = predictor.evaluate_role(role_name, candidate_skills, candidate_scores)
            self.assertEqual(eval_res["role"], role_name)
            self.assertIn("match_percentage", eval_res)
            self.assertGreaterEqual(eval_res["match_percentage"], 30)
            self.assertLessEqual(eval_res["match_percentage"], 100)
            self.assertIsInstance(eval_res["existing_skills"], list)
            self.assertIsInstance(eval_res["missing_skills"], list)
            self.assertGreater(len(eval_res["recommended_projects"]), 0)
            self.assertGreater(len(eval_res["certifications"]), 0)
            self.assertIn("preparation_time", eval_res)
            self.assertIn("career_growth_level", eval_res)

    # --- 2. CareerPathPredictor & Database Persistence ---
    def test_02_career_path_predictor(self):
        """Test CareerPathPredictor rankings, primary role selection, and DB persistence."""
        predictor = CareerPathPredictor()
        predictions = predictor.predict_for_user(self.user.id, persist=True)

        self.assertIn("primary_role", predictions)
        self.assertIn("primary_match_percentage", predictions)
        self.assertIn("top_paths", predictions)
        self.assertEqual(len(predictions["all_roles"]), 9)
        self.assertIn("competitiveness", predictions)

        # Check DB record
        record = CareerPathPrediction.query.filter_by(user_id=self.user.id).first()
        self.assertIsNotNone(record)
        self.assertEqual(record.primary_role, predictions["primary_role"])
        self.assertEqual(len(record.get_predicted_roles()), 9)
        self.assertIn("competitiveness", record.get_future_readiness())

    # --- 3. Career Transition & Future Roles ---
    def test_03_career_transition_engine(self):
        """Test CareerTransitionEngine cross-domain transition plan."""
        engine = CareerTransitionEngine()
        plan = engine.generate_transition_plan(
            current_role="Software Engineer",
            target_role="AI Engineer",
            current_skills=["Python", "SQL", "Git", "Data Structures"]
        )

        self.assertEqual(plan["from_role"], "Software Engineer")
        self.assertEqual(plan["to_role"], "AI Engineer")
        self.assertIn("skill_overlap_percentage", plan)
        self.assertIn("transition_feasibility", plan)
        self.assertGreaterEqual(len(plan["roadmap"]), 3)

    def test_04_future_role_predictor(self):
        """Test FutureRolePredictor emerging 1-3 year outlooks."""
        predictor = FutureRolePredictor()
        emerging = predictor.predict_emerging_roles(
            current_skills=["Python", "PyTorch", "Docker"],
            current_role="AI Engineer"
        )
        self.assertGreaterEqual(len(emerging), 3)
        self.assertIn("role_title", emerging[0])
        self.assertIn("demand_growth", emerging[0])
        self.assertIn("key_technologies", emerging[0])

    # --- 4. API Endpoints ---
    def test_05_api_career_paths_unauthenticated(self):
        """Test GET /api/career/paths without auth returns 401."""
        response = self.client.get("/api/career/paths")
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertFalse(data["success"])

    def test_06_api_career_paths_authenticated(self):
        """Test GET /api/career/paths with valid JWT returns 200 with full predictions."""
        token = self.generate_token(self.user.id)
        response = self.client.get(
            "/api/career/paths",
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertIn("career_paths", data)
        self.assertEqual(len(data["career_paths"]["all_roles"]), 9)
        self.assertIn("active_transition_plan", data)
        self.assertIn("emerging_roles_outlook", data)

    def test_07_api_skill_gaps_authenticated(self):
        """Test GET /api/career/skill-gaps with valid JWT returns 200."""
        token = self.generate_token(self.user.id)
        response = self.client.get(
            "/api/career/skill-gaps?role=DevOps%20Engineer",
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["target_role"], "DevOps Engineer")
        self.assertIn("skill_gaps", data)
        self.assertIn("digital_twin_scores", data)


if __name__ == "__main__":
    unittest.main()
