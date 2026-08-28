import unittest
import jwt
import datetime
from app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.skill import Skill
from backend.models.daily_task import DailyPlan

from AI.daily_planner.task_generator import TaskGenerator
from AI.daily_planner.progress_optimizer import ProgressOptimizer
from AI.daily_planner.daily_plan_engine import DailyPlanEngine


class TestDailyPlanner(unittest.TestCase):
    """Unit tests for Phase 9 Step 6: Personalized Daily Career Planner & Digital Twin Integration."""

    @classmethod
    def setUpClass(cls):
        cls.app = create_app("testing")
        cls.app.config["TESTING"] = True
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        cls.app.config["SECRET_KEY"] = "daily-plan-secret-key-114477"
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
            fullname="Alex Jordan",
            email=f"alex_{datetime.datetime.utcnow().timestamp()}@example.com"
        )
        self.user.set_password("DailyPlannerPass2026!")
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

    # --- 1. Task Generator Tests ---
    def test_01_task_generator_creates_balanced_daily_schedule(self):
        """Test TaskGenerator produces tasks across coding, skills, projects, and mock interviews."""
        gen = TaskGenerator()
        snapshot = {
            "skills": [{"skill_name": "Python", "proficiency_score": 90}],
            "career_goals": {"projects_to_build": ["FastAPI Service"]}
        }
        tasks = gen.generate_daily_tasks(snapshot, target_role="AI Engineer", target_company="Google")

        self.assertGreaterEqual(len(tasks), 4)
        categories = {t["category"] for t in tasks}
        self.assertIn("Skill Building", categories)
        self.assertIn("Coding Practice", categories)
        self.assertIn("Resume Optimization", categories)
        self.assertIn("Behavioral / HR", categories)

        for t in tasks:
            self.assertIn("id", t)
            self.assertIn("title", t)
            self.assertIn("duration_minutes", t)
            self.assertIn("digital_twin_skill_impact", t)
            self.assertFalse(t["completed"])

    # --- 2. Progress Optimizer Tests ---
    def test_02_progress_optimizer_metrics(self):
        """Test ProgressOptimizer calculates completion rate, estimated minutes, and momentum rating."""
        optimizer = ProgressOptimizer()
        tasks = [
            {"id": "t1", "duration_minutes": 45, "completed": True},
            {"id": "t2", "duration_minutes": 30, "completed": False},
            {"id": "t3", "duration_minutes": 15, "completed": False}
        ]
        res = optimizer.optimize_daily_schedule(tasks)

        self.assertEqual(res["total_tasks_count"], 3)
        self.assertEqual(res["completed_tasks_count"], 1)
        self.assertEqual(res["total_estimated_minutes"], 90)
        self.assertEqual(res["completed_minutes"], 45)
        self.assertEqual(res["completion_rate_pct"], 33)
        self.assertIn("momentum_rating", res)

    # --- 3. Master DailyPlanEngine Tests ---
    def test_03_master_daily_plan_engine_and_db_persistence(self):
        """Test DailyPlanEngine creates and retrieves daily plans with Explainable AI."""
        engine = DailyPlanEngine()
        plan_data = engine.get_or_create_daily_plan(self.user.id)

        self.assertIn("tasks", plan_data)
        self.assertGreater(len(plan_data["tasks"]), 0)
        self.assertIn("explainable_ai", plan_data)
        self.assertIn("metrics", plan_data)

        # Check DB record
        db_plan = DailyPlan.query.filter_by(user_id=self.user.id).first()
        self.assertIsNotNone(db_plan)
        self.assertGreater(len(db_plan.get_tasks()), 0)

    # --- 4. Task Completion and Digital Twin Synchronization ---
    def test_04_task_completion_syncs_digital_twin(self):
        """Test completing a task updates progress and synchronizes Digital Twin."""
        engine = DailyPlanEngine()
        plan_data = engine.get_or_create_daily_plan(self.user.id)
        task_id = plan_data["tasks"][0]["id"]

        comp_res = engine.complete_task(user_id=self.user.id, task_id=task_id, completed=True)
        self.assertTrue(comp_res["success"])
        self.assertTrue(comp_res["digital_twin_synced"])
        self.assertIn("updated_readiness_score", comp_res)

        # Verify DB updated
        db_plan = DailyPlan.query.filter_by(user_id=self.user.id).first()
        completed_tasks = [t for t in db_plan.get_tasks() if t.get("completed")]
        self.assertEqual(len(completed_tasks), 1)

    # --- 5. API Endpoints ---
    def test_05_api_daily_plan_unauthenticated(self):
        """Test GET /api/career/daily-plan and POST /api/career/daily-plan/complete return 401 unauthenticated."""
        res_get = self.client.get("/api/career/daily-plan")
        self.assertEqual(res_get.status_code, 401)

        res_post = self.client.post("/api/career/daily-plan/complete", json={})
        self.assertEqual(res_post.status_code, 401)

    def test_06_api_daily_plan_authenticated_flow(self):
        """Test GET and POST /api/career/daily-plan with valid JWT."""
        token = self.generate_token(self.user.id)
        headers = {"Authorization": f"Bearer {token}"}

        # 1. GET daily plan
        res_get = self.client.get("/api/career/daily-plan", headers=headers)
        self.assertEqual(res_get.status_code, 200)
        data_get = res_get.get_json()
        self.assertTrue(data_get["success"])
        self.assertIn("daily_plan", data_get)
        tasks = data_get["daily_plan"]["tasks"]
        self.assertGreater(len(tasks), 0)

        # 2. POST complete task
        task_id = tasks[0]["id"]
        res_post = self.client.post(
            "/api/career/daily-plan/complete",
            json={"task_id": task_id, "completed": True},
            headers=headers
        )
        self.assertEqual(res_post.status_code, 200)
        data_post = res_post.get_json()
        self.assertTrue(data_post["success"])
        self.assertTrue(data_post["result"]["digital_twin_synced"])


if __name__ == "__main__":
    unittest.main()
