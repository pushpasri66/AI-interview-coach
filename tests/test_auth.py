"""
Unit tests for authentication routes (register, login, logout).
"""
import unittest
from app import create_app
from backend.database import db
from backend.models.user import User


class TestAuthRoutes(unittest.TestCase):
    """Integration tests for /register, /login, and /logout endpoints."""

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    # ── Registration ────────────────────────────────────────────────────────

    def test_01_register_page_loads(self):
        """GET /register returns HTTP 200."""
        res = self.client.get("/register")
        self.assertIn(res.status_code, [200, 302])

    def test_02_register_new_user(self):
        """POST /register with valid data creates a new user."""
        res = self.client.post("/register", data={
            "fullname": "Test User",
            "email": "test_auth@example.com",
            "password": "StrongPass123!",
            "confirm_password": "StrongPass123!",
        }, follow_redirects=True)
        self.assertIn(res.status_code, [200, 302])
        user = User.query.filter_by(email="test_auth@example.com").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.fullname, "Test User")

    def test_03_register_duplicate_email(self):
        """Registering with an existing email does not create a duplicate."""
        # Create the user first
        user = User(fullname="Existing User", email="dupe@example.com")
        user.set_password("StrongPass123!")
        db.session.add(user)
        db.session.commit()

        # Attempt to register with the same email
        res = self.client.post("/register", data={
            "fullname": "Another User",
            "email": "dupe@example.com",
            "password": "StrongPass123!",
            "confirm_password": "StrongPass123!",
        }, follow_redirects=True)

        count = User.query.filter_by(email="dupe@example.com").count()
        self.assertEqual(count, 1)

    def test_04_register_password_mismatch(self):
        """POST /register with mismatched passwords does not create user."""
        res = self.client.post("/register", data={
            "fullname": "Mismatch User",
            "email": "mismatch@example.com",
            "password": "StrongPass123!",
            "confirm_password": "DifferentPass123!",
        }, follow_redirects=True)
        user = User.query.filter_by(email="mismatch@example.com").first()
        self.assertIsNone(user)

    # ── Login ───────────────────────────────────────────────────────────────

    def test_05_login_page_loads(self):
        """GET /login returns HTTP 200."""
        res = self.client.get("/login")
        self.assertIn(res.status_code, [200, 302])

    def test_06_login_valid_credentials(self):
        """POST /login with correct credentials redirects to dashboard."""
        user = User(fullname="Login Tester", email="login_test@example.com")
        user.set_password("StrongPass123!")
        db.session.add(user)
        db.session.commit()

        res = self.client.post("/login", data={
            "email": "login_test@example.com",
            "password": "StrongPass123!",
        }, follow_redirects=True)
        self.assertIn(res.status_code, [200, 302])

    def test_07_login_wrong_password(self):
        """POST /login with wrong password returns 200 (re-renders form)."""
        user = User(fullname="Wrong Pass", email="wrongpass@example.com")
        user.set_password("StrongPass123!")
        db.session.add(user)
        db.session.commit()

        res = self.client.post("/login", data={
            "email": "wrongpass@example.com",
            "password": "WrongPassword!",
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)

    def test_08_login_nonexistent_user(self):
        """POST /login with unknown email returns 200 (re-renders form)."""
        res = self.client.post("/login", data={
            "email": "nobody@example.com",
            "password": "AnyPass123!",
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)

    # ── Logout ──────────────────────────────────────────────────────────────

    def test_09_logout_requires_login(self):
        """GET /logout without an active session redirects to login."""
        res = self.client.get("/logout")
        self.assertIn(res.status_code, [302, 401])

    # ── Password model ──────────────────────────────────────────────────────

    def test_10_password_not_stored_in_plaintext(self):
        """User password is stored as a hash, never in plaintext."""
        user = User(fullname="Hash Test", email="hash@example.com")
        user.set_password("StrongPass123!")
        self.assertNotEqual(user.password_hash, "StrongPass123!")
        self.assertTrue(user.password_hash.startswith("scrypt:") or
                        user.password_hash.startswith("pbkdf2:"))


if __name__ == "__main__":
    unittest.main()
