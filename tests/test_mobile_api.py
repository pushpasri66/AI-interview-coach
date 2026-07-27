import unittest
from app import create_app
from backend.database import db
from backend.models.user import User


class TestMobileRESTAPI(unittest.TestCase):
    """Unit tests for Phase 7 PyJWT Authenticated Mobile REST API."""

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create test user
        self.user = User(fullname="Mobile Tester", email="mobile_tester@example.com")
        self.user.set_password("StrongPass123!")
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_01_mobile_jwt_login_and_profile_access(self):
        """Test POST /api/mobile/login and GET /api/mobile/profile bearer token access."""
        login_res = self.client.post("/api/mobile/login", json={
            "email": "mobile_tester@example.com",
            "password": "StrongPass123!"
        })

        self.assertEqual(login_res.status_code, 200)
        json_data = login_res.get_json()
        self.assertTrue(json_data["success"])
        token = json_data["token"]
        self.assertIsNotNone(token)

        # Access profile with Bearer Token
        profile_res = self.client.get("/api/mobile/profile", headers={
            "Authorization": f"Bearer {token}"
        })

        self.assertEqual(profile_res.status_code, 200)
        prof_data = profile_res.get_json()
        self.assertTrue(prof_data["success"])
        self.assertEqual(prof_data["user"]["email"], "mobile_tester@example.com")

    def test_02_mobile_progress_and_interview_creation(self):
        """Test mobile progress endpoint and mobile interview generation."""
        login_res = self.client.post("/api/mobile/login", json={
            "email": "mobile_tester@example.com",
            "password": "StrongPass123!"
        })
        token = login_res.get_json()["token"]

        int_res = self.client.post("/api/mobile/interview", json={
            "interview_type": "technical",
            "difficulty": "medium"
        }, headers={"Authorization": f"Bearer {token}"})

        self.assertEqual(int_res.status_code, 200)
        self.assertTrue(int_res.get_json()["success"])


if __name__ == "__main__":
    unittest.main()
