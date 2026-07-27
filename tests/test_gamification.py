import unittest
from app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.gamification import Gamification


class TestGamificationAndLeaderboard(unittest.TestCase):
    """Unit tests for Phase 7 Gamification & Leaderboard System."""

    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create test user
        self.user = User(fullname="Gamification Tester", email="game_tester@example.com")
        self.user.set_password("StrongPass123!")
        db.session.add(self.user)
        db.session.commit()

        # Login client
        self.client.post("/login", data={"email": "game_tester@example.com", "password": "StrongPass123!"})

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_01_gamification_model_points_and_level(self):
        """Test points addition and automatic level scaling."""
        game = Gamification(user_id=self.user.id, points=150, level=1)
        game.add_points(200)

        self.assertEqual(game.points, 350)
        self.assertEqual(game.level, 3)

    def test_02_leaderboard_route(self):
        """Test /leaderboard HTTP route."""
        res = self.client.get("/leaderboard/")
        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
