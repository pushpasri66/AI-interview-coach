import unittest
from app import create_app
from backend.database import db
from backend.models.user import User


class TestGroupDiscussion(unittest.TestCase):
    """Unit tests for Phase 8 AI Mock Group Discussion Platform."""

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create test user
        self.user = User(fullname="GD Tester", email="gd_tester@example.com")
        self.user.set_password("StrongPass123!")
        db.session.add(self.user)
        db.session.commit()

        # Login
        self.client.post("/login", data={"email": "gd_tester@example.com", "password": "StrongPass123!"})

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_01_group_discussion_routes(self):
        """Test GET /group-discussion and POST /group-discussion/start."""
        res_get = self.client.get("/group-discussion/")
        self.assertEqual(res_get.status_code, 200)

        res_start = self.client.post("/group-discussion/start", json={
            "topic": "Impact of Artificial Intelligence on Future Employment"
        })
        self.assertEqual(res_start.status_code, 200)
        json_data = res_start.get_json()
        self.assertTrue(json_data["success"])
        self.assertIn("scores", json_data)


if __name__ == "__main__":
    unittest.main()
