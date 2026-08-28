import unittest
import jwt
import datetime
from app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.skill import Skill
from backend.models.career_simulation import CareerSimulation

from AI.simulator.scenario_engine import ScenarioEngine
from AI.simulator.outcome_predictor import OutcomePredictor
from AI.simulator.career_simulator import AICareerSimulator


class TestCareerSimulator(unittest.TestCase):
    """Unit tests for Phase 9 Step 7: AI Career Simulation Engine."""

    @classmethod
    def setUpClass(cls):
        cls.app = create_app("testing")
        cls.app.config["TESTING"] = True
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        cls.app.config["SECRET_KEY"] = "sim-secret-key-998877"
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
            fullname="Jordan Reed",
            email=f"jordan_{datetime.datetime.utcnow().timestamp()}@example.com"
        )
        self.user.set_password("SimulatorPass2026!")
        db.session.add(self.user)
        db.session.commit()

        skills = [
            Skill(user_id=self.user.id, skill_name="Python", skill_level="Advanced"),
            Skill(user_id=self.user.id, skill_name="SQL", skill_level="Intermediate")
        ]
        db.session.add_all(skills)
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

    # --- 1. Scenario Engine Tests ---
    def test_01_scenario_engine_inference(self):
        """Test ScenarioEngine infers correct scenario types for various user inputs."""
        engine = ScenarioEngine()
        self.assertEqual(engine.infer_scenario_type("Learn AWS + Docker"), "learn_skill")
        self.assertEqual(engine.infer_scenario_type("Earn AWS Certified Solutions Architect"), "certification")
        self.assertEqual(engine.infer_scenario_type("Build Fullstack Microservice Pipeline"), "build_project")
        self.assertEqual(engine.infer_scenario_type("Improve Mock Interview Communication"), "improve_interview")
        self.assertEqual(engine.infer_scenario_type("Pivot role to AI Engineer"), "change_role")
        self.assertEqual(engine.infer_scenario_type("Submit 20 job applications to FAANG"), "apply_jobs")

    # --- 2. Outcome Predictor Tests ---
    def test_02_outcome_predictor_calculations(self):
        """Test OutcomePredictor projects positive readiness, job match, and salary growth deltas."""
        predictor = OutcomePredictor()
        outcomes = predictor.predict_outcome(
            scenario_type="learn_skill",
            scenario_title="Learn AWS + Docker",
            target_role="Cloud Engineer",
            base_readiness=78,
            base_job_match=70,
            base_interview_readiness=72
        )

        self.assertEqual(outcomes["current_readiness"], 78)
        self.assertEqual(outcomes["predicted_readiness"], 86)
        self.assertEqual(outcomes["readiness_delta"], 8)
        self.assertGreater(outcomes["job_match_delta"], 0)
        self.assertGreater(outcomes["salary_growth_pct"], 0)
        self.assertIn("Build", outcomes["recommended_next_step"])

    # --- 3. Master AICareerSimulator Tests ---
    def test_03_master_career_simulator_and_db_persistence(self):
        """Test AICareerSimulator executes simulation, projects all metrics, and saves to DB."""
        simulator = AICareerSimulator()
        sim_res = simulator.run_simulation(
            user_id=self.user.id,
            scenario_title="Complete Certified Kubernetes Administrator (CKA)",
            target_role="DevOps Engineer",
            persist=True
        )

        self.assertEqual(sim_res["target_role"], "DevOps Engineer")
        self.assertEqual(sim_res["scenario_type"], "certification")
        self.assertIn("impact_comparison", sim_res)
        
        comp = sim_res["impact_comparison"]
        self.assertIn("career_readiness", comp)
        self.assertIn("job_match", comp)
        self.assertIn("salary_potential", comp)
        self.assertIn("interview_readiness", comp)
        self.assertIn("recommended_next_step", sim_res)

        # Check DB record
        db_rec = CareerSimulation.query.filter_by(user_id=self.user.id).first()
        self.assertIsNotNone(db_rec)
        self.assertEqual(db_rec.scenario_title, "Complete Certified Kubernetes Administrator (CKA)")
        self.assertGreater(db_rec.readiness_delta, 0)

        # Check history retrieval
        history = simulator.get_simulation_history(self.user.id)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["scenario_title"], "Complete Certified Kubernetes Administrator (CKA)")

    # --- 4. API Endpoints ---
    def test_04_api_simulate_unauthenticated(self):
        """Test POST /api/career/simulate and GET /api/career/simulations return 401 unauthenticated."""
        res_post = self.client.post("/api/career/simulate", json={})
        self.assertEqual(res_post.status_code, 401)

        res_get = self.client.get("/api/career/simulations")
        self.assertEqual(res_get.status_code, 401)

    def test_05_api_simulate_validation(self):
        """Test POST /api/career/simulate with empty scenario returns 400."""
        token = self.generate_token(self.user.id)
        headers = {"Authorization": f"Bearer {token}"}

        res = self.client.post("/api/career/simulate", json={}, headers=headers)
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertFalse(data["success"])
        self.assertIn("Missing required", data["error"])

    def test_06_api_simulate_post_and_history_success(self):
        """Test POST /api/career/simulate and GET /api/career/simulations with valid JWT."""
        token = self.generate_token(self.user.id)
        headers = {"Authorization": f"Bearer {token}"}

        payload = {
            "scenario_title": "Learn PyTorch + Deep Learning Vision Pipelines",
            "target_role": "AI Engineer"
        }

        # 1. POST simulation
        res_post = self.client.post("/api/career/simulate", json=payload, headers=headers)
        self.assertEqual(res_post.status_code, 201)
        data_post = res_post.get_json()
        self.assertTrue(data_post["success"])
        self.assertIn("simulation", data_post)
        self.assertEqual(data_post["simulation"]["target_role"], "AI Engineer")

        # 2. GET history
        res_get = self.client.get("/api/career/simulations", headers=headers)
        self.assertEqual(res_get.status_code, 200)
        data_get = res_get.get_json()
        self.assertTrue(data_get["success"])
        self.assertEqual(data_get["total_simulations"], 1)
        self.assertEqual(data_get["simulations"][0]["target_role"], "AI Engineer")


if __name__ == "__main__":
    unittest.main()
