import unittest
import jwt
import datetime
from app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.skill import Skill
from backend.models.future_skill import FutureSkillDemand

from AI.future_skills.skill_demand_predictor import SkillDemandPredictor
from AI.future_skills.trend_analyzer import TrendAnalyzer
from AI.future_skills.emerging_skills import EmergingSkillsEngine


class TestFutureSkills(unittest.TestCase):
    """Unit tests for Phase 9 Step 2: Future Skill Intelligence."""

    @classmethod
    def setUpClass(cls):
        cls.app = create_app("testing")
        cls.app.config["TESTING"] = True
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        cls.app.config["SECRET_KEY"] = "future-skills-secret-key-445566"
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
            fullname="Sam Taylor",
            email=f"sam_{datetime.datetime.utcnow().timestamp()}@example.com"
        )
        self.user.set_password("FutureSkillPass2026!")
        db.session.add(self.user)
        db.session.commit()

        skills = [
            Skill(user_id=self.user.id, skill_name="Python", skill_level="Advanced"),
            Skill(user_id=self.user.id, skill_name="Kubernetes", skill_level="Intermediate"),
            Skill(user_id=self.user.id, skill_name="FastAPI", skill_level="Intermediate")
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

    # --- 1. Database Model & Seed Tests ---
    def test_01_future_skill_model_and_seeding(self):
        """Test FutureSkillDemand model fields, to_dict, and automated database seeding."""
        predictor = SkillDemandPredictor()
        predictor.seed_and_sync_database()

        count = FutureSkillDemand.query.count()
        self.assertGreaterEqual(count, 10)

        item = FutureSkillDemand.query.filter_by(skill_name="RAG & Vector Databases").first()
        self.assertIsNotNone(item)
        self.assertEqual(item.category, "AI & Machine Learning")
        self.assertGreater(item.demand_3yr, item.current_demand)
        self.assertEqual(item.importance, "Critical")

        item_dict = item.to_dict()
        self.assertIn("demand_forecast", item_dict)
        self.assertIn("1_year", item_dict["demand_forecast"])
        self.assertIn("2_year", item_dict["demand_forecast"])
        self.assertIn("3_year", item_dict["demand_forecast"])
        self.assertIn("growth_percentage", item_dict)

    # --- 2. 1-Year, 2-Year, 3-Year Prediction Engine ---
    def test_02_future_skills_prediction_engine(self):
        """Test SkillDemandPredictor maps candidate skills against 1-3 year demand horizons."""
        predictor = SkillDemandPredictor()
        result = predictor.predict_future_skills_for_candidate(
            candidate_skills=["Python", "FastAPI"],
            target_role="AI Engineer"
        )

        self.assertIn("forecast_horizons", result)
        self.assertEqual(len(result["forecast_horizons"]), 3)
        self.assertIn("candidate_future_ready_skills", result)
        self.assertIn("recommended_future_skills", result)
        self.assertGreater(len(result["recommended_future_skills"]), 0)

        top_rec = result["recommended_future_skills"][0]
        self.assertIn("demand_1yr", top_rec)
        self.assertIn("demand_2yr", top_rec)
        self.assertIn("demand_3yr", top_rec)
        self.assertIn("growth_percentage", top_rec)
        self.assertIn("importance", top_rec)
        self.assertIn("learning_priority", top_rec)

    # --- 3. Trend Analyzer & Emerging Clusters ---
    def test_03_trend_analyzer(self):
        """Test TrendAnalyzer profile trend alignment and macro drivers."""
        analyzer = TrendAnalyzer()
        res = analyzer.analyze_profile_trends(skills=["Python", "FastAPI", "Kubernetes"])

        self.assertIn("overall_future_alignment_index", res)
        self.assertIn("alignment_status", res)
        self.assertIn("trends", res)
        self.assertGreater(len(res["trends"]), 0)

    def test_04_emerging_skills_engine(self):
        """Test EmergingSkillsEngine breakthrough clusters and projects."""
        engine = EmergingSkillsEngine()
        catalog = engine.get_emerging_skills_catalog()
        self.assertGreaterEqual(len(catalog), 3)

        recs = engine.recommend_for_candidate(["Python", "Rust"])
        self.assertGreaterEqual(len(recs), 3)
        self.assertIn("cluster", recs[0])
        self.assertIn("skills_to_learn", recs[0])
        self.assertIn("recommended_project", recs[0])

    # --- 4. API Endpoints ---
    def test_05_api_future_skills_unauthenticated(self):
        """Test GET /api/career/future-skills without auth returns 401."""
        response = self.client.get("/api/career/future-skills")
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertFalse(data["success"])

    def test_06_api_future_skills_authenticated(self):
        """Test GET /api/career/future-skills with valid JWT returns 200 with 1-3yr forecasts."""
        token = self.generate_token(self.user.id)
        response = self.client.get(
            "/api/career/future-skills",
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertIn("future_skills", data)
        self.assertIn("trend_intelligence", data)
        self.assertIn("emerging_breakthrough_tracks", data)


if __name__ == "__main__":
    unittest.main()
