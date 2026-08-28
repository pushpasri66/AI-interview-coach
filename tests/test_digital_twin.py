import unittest
import jwt
import datetime
from app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.skill import Skill
from backend.models.career import CareerPlan
from backend.models.certificate import Certificate
from backend.models.interview import Interview, Question, Answer
from backend.models.digital_twin import DigitalTwin

from AI.digital_twin.candidate_profile import CandidateProfile
from AI.digital_twin.career_state import CareerState
from AI.digital_twin.career_simulator import CareerSimulator
from AI.digital_twin.twin_predictor import TwinPredictor
from AI.digital_twin.digital_twin_engine import DigitalTwinEngine


class TestDigitalTwin(unittest.TestCase):
    """Unit tests for Phase 9 Step 1: AI Career Digital Twin."""

    @classmethod
    def setUpClass(cls):
        cls.app = create_app("testing")
        cls.app.config["TESTING"] = True
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        cls.app.config["SECRET_KEY"] = "test-secret-key-12345"
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

        # Clean DB before each test
        db.session.rollback()
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

        # Create test candidate user
        self.user = User(
            fullname="Alex Morgan",
            email=f"alex_{datetime.datetime.utcnow().timestamp()}@example.com"
        )
        self.user.set_password("StrongPass123!")
        db.session.add(self.user)
        db.session.commit()

        # Add Skills
        skills = [
            Skill(user_id=self.user.id, skill_name="Python", skill_level="Advanced", source="Profile"),
            Skill(user_id=self.user.id, skill_name="SQL", skill_level="Intermediate", source="Profile"),
            Skill(user_id=self.user.id, skill_name="Flask", skill_level="Intermediate", source="Profile"),
            Skill(user_id=self.user.id, skill_name="Data Structures", skill_level="Advanced", source="Profile")
        ]
        db.session.add_all(skills)

        # Add Career Plan
        plan = CareerPlan(
            user_id=self.user.id,
            target_role="Software Engineer",
            duration_months=6,
            skills_to_learn="System Design,Docker",
            projects_to_build="Distributed Cache"
        )
        db.session.add(plan)

        # Add Certificate
        cert = Certificate(
            user_id=self.user.id,
            certificate_id=f"CERT-TWIN-{datetime.datetime.utcnow().timestamp()}",
            title="Certified Python Developer",
            verification_url="http://test.com/verify"
        )
        db.session.add(cert)

        # Add Interview & Answer
        interview = Interview(
            user_id=self.user.id,
            interview_type="technical",
            score=85,
            status="completed"
        )
        db.session.add(interview)
        db.session.commit()

        q = Question(
            interview_id=interview.id,
            question_text="Explain Python memory management.",
            expected_answer="Garbage collection and reference counting."
        )
        db.session.add(q)
        db.session.commit()

        ans = Answer(
            question_id=q.id,
            interview_id=interview.id,
            user_answer="Python uses reference counting and a generational garbage collector.",
            answer_score=88,
            technical_score=90,
            communication_score=85,
            relevance_score=90
        )
        db.session.add(ans)
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

    # --- 1. Model & Relationship Tests ---
    def test_01_digital_twin_model_creation(self):
        """Test DigitalTwin SQLAlchemy model instantiation, JSON helpers, and User relation."""
        twin = DigitalTwin(
            user_id=self.user.id,
            career_readiness_score=84,
            interview_readiness=82,
            technical_strength=88,
            communication_strength=80,
            skill_strength=85,
            target_role="Software Engineer"
        )
        twin.set_job_compatibility({"Software Engineer": 90, "Full Stack Developer": 85})
        twin.set_skill_gaps([{"skill": "Docker", "importance": "High"}])
        twin.set_strengths(["Strong algorithmic knowledge"])
        twin.set_weaknesses(["Need deeper CI/CD practice"])
        twin.set_recommendations(["Build a Dockerized web project"])
        
        db.session.add(twin)
        db.session.commit()

        fetched = DigitalTwin.query.filter_by(user_id=self.user.id).first()
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.career_readiness_score, 84)
        self.assertEqual(fetched.get_job_compatibility()["Software Engineer"], 90)
        self.assertEqual(len(fetched.get_skill_gaps()), 1)
        self.assertEqual(fetched.user.id, self.user.id)
        self.assertEqual(self.user.digital_twin.id, fetched.id)

        twin_dict = fetched.to_dict()
        self.assertIn("scores", twin_dict)
        self.assertEqual(twin_dict["scores"]["career_readiness_score"], 84)

    # --- 2. Candidate Profile & Career State Calculations ---
    def test_02_candidate_profile_aggregation(self):
        """Test CandidateProfile aggregation across skills, certifications, and interviews."""
        builder = CandidateProfile(self.user.id)
        snapshot = builder.build_snapshot()

        self.assertEqual(snapshot["user_id"], self.user.id)
        self.assertGreaterEqual(len(snapshot["skills"]), 4)
        self.assertEqual(len(snapshot["certifications"]), 1)
        self.assertEqual(snapshot["interview_performance"]["completed_interviews"], 1)
        self.assertEqual(snapshot["career_goals"]["target_role"], "Software Engineer")

    def test_03_career_state_calculations(self):
        """Test multi-dimensional scores, skill gaps, and strengths calculation."""
        builder = CandidateProfile(self.user.id)
        snapshot = builder.build_snapshot()
        state = CareerState(snapshot)
        eval_res = state.evaluate_state()

        self.assertIn("career_readiness_score", eval_res)
        self.assertGreater(eval_res["career_readiness_score"], 0)
        self.assertGreater(eval_res["technical_strength"], 0)
        self.assertGreater(eval_res["communication_strength"], 0)
        self.assertGreater(eval_res["skill_strength"], 0)
        self.assertIn("Software Engineer", eval_res["job_compatibility"])
        self.assertIsInstance(eval_res["skill_gaps"], list)
        self.assertIsInstance(eval_res["recommendations"], list)

    # --- 3. Simulator & Predictor Tests ---
    def test_04_career_simulator_and_predictor(self):
        """Test CareerSimulator what-if scenarios and TwinPredictor metrics."""
        simulator = CareerSimulator()
        sim_res = simulator.simulate_skill_acquisition(
            current_readiness=75,
            current_skills=["Python", "SQL"],
            acquired_skills=["Docker", "Kubernetes", "AWS"]
        )
        self.assertGreater(sim_res["projected_readiness"], 75)
        self.assertEqual(sim_res["readiness_gain"], 12)

        predictor = TwinPredictor()
        pred_res = predictor.generate_all_predictions(
            readiness=85,
            interview_readiness=82,
            tech_strength=88,
            target_compatibility=90
        )
        self.assertIn("interview_probabilities", pred_res)
        self.assertIn("offer_likelihood", pred_res)
        self.assertIn("seniority_fit", pred_res)
        self.assertGreater(pred_res["interview_probabilities"]["hr_screening_pass_rate"], 50)

    # --- 4. DigitalTwinEngine Tests ---
    def test_05_digital_twin_engine_sync(self):
        """Test DigitalTwinEngine automated synchronization and state retrieval."""
        engine = DigitalTwinEngine()
        twin_rec = engine.sync_user_twin(self.user.id, trigger_event="test")
        self.assertIsNotNone(twin_rec)
        self.assertEqual(twin_rec.user_id, self.user.id)

        twin_data = engine.get_digital_twin_state(self.user.id, auto_sync=False)
        self.assertEqual(twin_data["user_id"], self.user.id)
        self.assertIn("scores", twin_data)
        self.assertIn("predictions", twin_data)

    def test_06_digital_twin_invalid_user(self):
        """Test error handling when building digital twin for non-existent user."""
        engine = DigitalTwinEngine()
        with self.assertRaises(ValueError):
            engine.build_digital_twin(user_id=999999)

    # --- 5. API Authentication, Authorization & Response Tests ---
    def test_07_api_digital_twin_unauthenticated(self):
        """Test GET /api/career/digital-twin without auth returns 401 Unauthorized."""
        response = self.client.get("/api/career/digital-twin")
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertFalse(data["success"])
        self.assertIn("Authentication required", data["error"])

    def test_08_api_digital_twin_invalid_token(self):
        """Test GET /api/career/digital-twin with invalid token returns 401."""
        response = self.client.get(
            "/api/career/digital-twin",
            headers={"Authorization": "Bearer invalid.token.payload"}
        )
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertFalse(data["success"])

    def test_09_api_digital_twin_jwt_success(self):
        """Test GET /api/career/digital-twin with valid Bearer JWT token returns 200 OK."""
        token = self.generate_token(self.user.id)
        response = self.client.get(
            "/api/career/digital-twin",
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["candidate"]["id"], self.user.id)
        self.assertIn("digital_twin", data)
        self.assertIn("scores", data["digital_twin"])
        self.assertIn("job_compatibility", data["digital_twin"])
        self.assertIn("skill_gaps", data["digital_twin"])

    def test_10_api_career_blueprint_endpoint(self):
        """Test GET /career/digital-twin with authenticated session."""
        with self.client.session_transaction() as sess:
            sess["_user_id"] = str(self.user.id)
            sess["_fresh"] = True

        response = self.client.get("/career/digital-twin")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["candidate"]["id"], self.user.id)


if __name__ == "__main__":
    unittest.main()
