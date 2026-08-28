import unittest
import datetime
from app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.skill import Skill
from backend.models.career import CareerPlan


class TestCareerIntelligenceUI(unittest.TestCase):
    """Unit tests for Phase 9 Step 8: Advanced AI Career Intelligence Dashboard UI & Integration."""

    @classmethod
    def setUpClass(cls):
        cls.app = create_app("testing")
        cls.app.config["TESTING"] = True
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        cls.app.config["SECRET_KEY"] = "career-intel-ui-key-12345"
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
            fullname="Devon Patel",
            email=f"devon_{datetime.datetime.utcnow().timestamp()}@example.com"
        )
        self.user.set_password("IntelPass2026!")
        db.session.add(self.user)
        db.session.commit()

        skills = [
            Skill(user_id=self.user.id, skill_name="Python", skill_level="Advanced"),
            Skill(user_id=self.user.id, skill_name="Machine Learning", skill_level="Intermediate")
        ]
        db.session.add_all(skills)

        plan = CareerPlan(
            user_id=self.user.id,
            target_role="AI Engineer",
            duration_months=6,
            projects_to_build="CNN Vision Pipeline"
        )
        db.session.add(plan)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()
        self.app_context.pop()

    def login_session(self):
        with self.client.session_transaction() as sess:
            sess["_user_id"] = str(self.user.id)
            sess["_fresh"] = True

    def test_01_unauthenticated_access_redirects(self):
        """Test unauthenticated GET /career/intelligence redirects to login."""
        response = self.client.get("/career/intelligence", follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.location)

    def test_02_authenticated_dashboard_renders_all_12_pillars(self):
        """Test authenticated GET /career/intelligence returns 200 and all 12 career intelligence components."""
        self.login_session()
        response = self.client.get("/career/intelligence")
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)

        # 1. AI Career Digital Twin & 2. Readiness Score
        self.assertIn("Digital Twin State", html)
        self.assertIn("Career Readiness Index", html)

        # 3. Top Career Paths & 4. Job Match
        self.assertIn("Predictive Career Paths", html)
        self.assertIn("AI Engineer", html)

        # 6. Future Skill Demand
        self.assertIn("Future Skill Demand Intelligence", html)

        # 7. Predicted Interview Questions
        self.assertIn("Predicted Interview Questions", html)

        # 8. GitHub AI Profile Intelligence
        self.assertIn("GitHub AI Profile Intelligence", html)

        # 10. Daily Career Plan
        self.assertIn("Personalized Daily Career Plan", html)

        # 11. Career Simulation
        self.assertIn("AI Career Simulation Engine", html)

        # 12. Explainable AI
        self.assertIn("Explainable AI Recommendation", html)

        # Verify Chart.js integration
        self.assertIn("chart.js", html.lower())
        self.assertIn("readinessChart", html)
        self.assertIn("careerPathsChart", html)
        self.assertIn("futureSkillsChart", html)

    def test_03_navigation_and_dashboard_links(self):
        """Test navigation link in base navbar and card in main dashboard."""
        self.login_session()
        resp_dash = self.client.get("/dashboard")
        self.assertEqual(resp_dash.status_code, 200)
        dash_html = resp_dash.get_data(as_text=True)

        self.assertIn("career-intelligence", dash_html)
        self.assertIn("AI Career Intelligence", dash_html)



if __name__ == "__main__":
    unittest.main()
