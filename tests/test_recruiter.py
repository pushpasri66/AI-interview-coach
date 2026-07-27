import unittest
from app import create_app
from backend.database import db
from backend.models.user import User


class TestRecruiterPortal(unittest.TestCase):
    """Unit tests for Phase 8 Recruiter & Enterprise Company Portal."""

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create test user
        self.user = User(fullname="Recruiter User", email="recruiter_user@example.com")
        self.user.set_password("StrongPass123!")
        db.session.add(self.user)
        db.session.commit()

        # Login
        self.client.post("/login", data={"email": "recruiter_user@example.com", "password": "StrongPass123!"})

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_01_recruiter_dashboard_and_posting(self):
        """Test recruiter candidate search and job vacancy posting."""
        dash_res = self.client.get("/recruiter/dashboard")
        self.assertEqual(dash_res.status_code, 200)
        self.assertTrue(dash_res.get_json()["success"])

        post_res = self.client.post("/recruiter/post_job", json={
            "company_name": "Google",
            "job_role": "AI Engineer",
            "requirements": "Python, Flask, PyTorch"
        })
        self.assertEqual(post_res.status_code, 200)
        self.assertTrue(post_res.get_json()["success"])


if __name__ == "__main__":
    unittest.main()
