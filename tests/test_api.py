import unittest
from app import create_app
from backend.database import db
from backend.models.user import User


class TestAPIEndpoints(unittest.TestCase):
    """Unit tests for Phase 6 API Endpoint Responses."""

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_01_public_routes(self):
        """Test public GET routes (Landing page, About page, Login page)."""
        res_home = self.client.get("/")
        self.assertEqual(res_home.status_code, 200)

        res_about = self.client.get("/about")
        self.assertEqual(res_about.status_code, 200)

        res_login = self.client.get("/login")
        self.assertEqual(res_login.status_code, 200)

    def test_02_404_error_handler(self):
        """Test custom 404 error handler."""
        res = self.client.get("/non_existent_route_xyz")
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
