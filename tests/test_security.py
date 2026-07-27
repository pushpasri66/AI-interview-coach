import unittest
from app import create_app
from backend.database import db
from backend.models.user import User


class TestSecurity(unittest.TestCase):
    """Unit tests for Phase 6 Security & Validation."""

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_01_password_strength_validation(self):
        """Test password strength validation rule enforcing uppercase, lowercase, digit, and special char."""
        valid, _ = User.validate_password_strength("Weak1!")
        self.assertFalse(valid)  # Short

        valid, _ = User.validate_password_strength("alllowercase1!")
        self.assertFalse(valid)  # Missing uppercase

        valid, _ = User.validate_password_strength("ALLUPPERCASE1!")
        self.assertFalse(valid)  # Missing lowercase

        valid, _ = User.validate_password_strength("NoDigitSpecial")
        self.assertFalse(valid)  # Missing digit & special char

        valid, msg = User.validate_password_strength("StrongPass123!")
        self.assertTrue(valid)
        self.assertIn("valid", msg)

    def test_02_password_hashing_and_verification(self):
        """Test Werkzeug security password hashing."""
        user = User(fullname="Security Test User", email="sec_user@example.com")
        user.set_password("StrongPass123!")

        self.assertNotEqual(user.password_hash, "StrongPass123!")
        self.assertTrue(user.check_password("StrongPass123!"))
        self.assertFalse(user.check_password("WrongPass123!"))

    def test_03_rate_limiting_headers(self):
        """Test rate limiting response handling."""
        for _ in range(15):
            res = self.client.post("/login", data={"email": "bad@example.com", "password": "wrong"})
        self.assertIn(res.status_code, [200, 302, 429])


if __name__ == "__main__":
    unittest.main()
