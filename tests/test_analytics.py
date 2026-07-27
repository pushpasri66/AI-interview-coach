import unittest
from app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.skill import Skill
from backend.models.recommendation import CareerRecommendation
from backend.models.achievement import Achievement

from AI.models.career_predictor import CareerPredictor
from AI.models.skill_matcher import SkillMatcher
from AI.models.job_analyzer import JobAnalyzer
from AI.models.roadmap_generator import RoadmapGenerator
from backend.services.analytics_service import AnalyticsService
from backend.services.recommendation_service import RecommendationService


class TestPhase5AnalyticsAndCareer(unittest.TestCase):
    """Unit tests for Phase 5 AI Analytics Dashboard & Career Recommendation System."""

    def setUp(self):
        self.app = create_app("development")
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.client = self.app.test_client()

        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create test user
        self.user = User.query.filter_by(email="analytics_tester@example.com").first()
        if not self.user:
            self.user = User(fullname="Analytics Tester", email="analytics_tester@example.com")
            self.user.set_password("Password123!")
            db.session.add(self.user)
            db.session.commit()

        # Login client
        self.client.post("/login", data={
            "email": "analytics_tester@example.com",
            "password": "Password123!"
        })

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_01_career_predictor(self):
        """Test AI career role match prediction."""
        predictor = CareerPredictor()
        skills = ["Python", "Machine Learning", "Data Analysis", "SQL"]
        matches = predictor.predict_career_matches(user_skills=skills, avg_tech_score=85)

        self.assertGreater(len(matches), 0)
        self.assertIn("role", matches[0])
        self.assertGreaterEqual(matches[0]["match_percentage"], 50)

    def test_02_skill_matcher(self):
        """Test skill gap detection and priority assignment."""
        matcher = SkillMatcher()
        gaps = matcher.analyze_skill_gap("AI Engineer", ["Python", "Flask"])

        self.assertIn("missing_skills", gaps)
        self.assertIn("priority", gaps)
        self.assertIn("TensorFlow", gaps["missing_skills"])

    def test_03_job_analyzer(self):
        """Test job description keyword extraction and compatibility scoring."""
        analyzer = JobAnalyzer()
        jd_text = "Looking for a Senior Python Backend Developer with strong SQL, Flask, PostgreSQL, Docker, and REST API experience."
        user_skills = ["Python", "Flask", "SQL"]

        res = analyzer.analyze_job_description(jd_text, user_skills)
        self.assertGreaterEqual(res["match_score"], 40)
        self.assertIn("Docker", res["missing_skills"])

    def test_04_roadmap_generator(self):
        """Test 4-month learning roadmap generation."""
        generator = RoadmapGenerator()
        plan = generator.generate_roadmap("Machine Learning Engineer", ["Deep Learning", "MLOps"])

        self.assertIn("roadmap", plan)
        self.assertIn("Month 1", plan["roadmap"])
        self.assertIn("suggested_courses", plan)

    def test_05_analytics_service(self):
        """Test statistics and growth report generation."""
        svc = AnalyticsService()
        stats = svc.generate_statistics(self.user.id)
        growth = svc.generate_growth_report(self.user.id)

        self.assertIn("avg_score", stats)
        self.assertIn("progress", growth)

    def test_06_career_routes(self):
        """Test HTTP routes for career dashboard, skill-gap, and roadmap."""
        resp = self.client.get("/career/dashboard")
        self.assertEqual(resp.status_code, 200)

        resp2 = self.client.get("/career/skill-gap?role=AI+Engineer")
        self.assertEqual(resp2.status_code, 200)

        resp3 = self.client.get("/career/roadmap?role=AI+Engineer")
        self.assertEqual(resp3.status_code, 200)

    def test_07_analytics_routes(self):
        """Test HTTP routes for analytics dashboard and progress API."""
        resp = self.client.get("/analytics/dashboard")
        self.assertEqual(resp.status_code, 200)

        resp2 = self.client.get("/analytics/progress")
        self.assertEqual(resp2.status_code, 200)
        self.assertTrue(resp2.get_json()["success"])


if __name__ == "__main__":
    unittest.main()
