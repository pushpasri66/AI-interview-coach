import unittest
import os
import jwt
import datetime
from app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.skill import Skill
from backend.models.career import CareerPlan
from backend.services.career_report import CareerReportService


class TestCareerReport(unittest.TestCase):
    """Unit tests for Phase 9 Step 9: AI Career Intelligence Reports & PDF Generation."""

    @classmethod
    def setUpClass(cls):
        cls.app = create_app("testing")
        cls.app.config["TESTING"] = True
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        cls.app.config["SECRET_KEY"] = "report-secret-key-112233"
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
            fullname="Rowan Sterling",
            email=f"rowan_{datetime.datetime.utcnow().timestamp()}@example.com"
        )
        self.user.set_password("ReportPass2026!")
        db.session.add(self.user)
        db.session.commit()

        skills = [
            Skill(user_id=self.user.id, skill_name="Python", skill_level="Advanced"),
            Skill(user_id=self.user.id, skill_name="SQL", skill_level="Intermediate"),
            Skill(user_id=self.user.id, skill_name="Machine Learning", skill_level="Advanced")
        ]
        db.session.add_all(skills)

        plan = CareerPlan(
            user_id=self.user.id,
            target_role="AI Engineer",
            duration_months=6,
            projects_to_build="Distributed Vision Pipeline"
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

    # --- 1. Service Level PDF Generation Tests ---
    def test_01_generate_intelligence_pdf_report(self):
        """Test CareerReportService creates a valid AI Career Intelligence PDF on disk."""
        service = CareerReportService()
        filepath = service.generate_career_pdf(user_id=self.user.id, report_type="intelligence")

        self.assertTrue(os.path.exists(filepath))
        self.assertGreater(os.path.getsize(filepath), 1000)

        with open(filepath, "rb") as f:
            header = f.read(5)
            self.assertEqual(header, b"%PDF-")

    def test_02_generate_all_4_report_types(self):
        """Test CareerReportService generates all 4 requested report types without error."""
        service = CareerReportService()
        types = ["intelligence", "readiness", "skill_gap", "job_application"]

        for r_type in types:
            filepath = service.generate_career_pdf(user_id=self.user.id, report_type=r_type)
            self.assertTrue(os.path.exists(filepath))
            self.assertGreater(os.path.getsize(filepath), 1000)

    # --- 2. API Authorization & Delivery Tests ---
    def test_03_api_report_unauthenticated(self):
        """Test GET /api/career/report without token returns 401."""
        response = self.client.get("/api/career/report")
        self.assertEqual(response.status_code, 401)

    def test_04_api_report_authenticated_success(self):
        """Test GET /api/career/report with valid Bearer token returns application/pdf."""
        token = self.generate_token(self.user.id)
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.get("/api/career/report?type=intelligence", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/pdf")
        self.assertTrue(response.data.startswith(b"%PDF-"))

    def test_05_api_report_download_attachment(self):
        """Test GET /api/career/report?download=true returns attachment Content-Disposition."""
        token = self.generate_token(self.user.id)
        headers = {"Authorization": f"Bearer {token}"}

        response = self.client.get("/api/career/report?type=skill_gap&download=true", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "application/pdf")
        self.assertIn("attachment", response.headers.get("Content-Disposition", ""))


if __name__ == "__main__":
    unittest.main()
