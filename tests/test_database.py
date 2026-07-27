import unittest
from app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.resume import Resume
from backend.models.interview import Interview


class TestDatabaseConnection(unittest.TestCase):
    """Unit tests for Phase 6 Database Pooling and Relationships."""

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_01_user_relationships(self):
        """Test cascade relationships between User, Resume, and Interview models."""
        user = User(fullname="Database Tester", email="db_tester@example.com")
        user.set_password("StrongPass123!")
        db.session.add(user)
        db.session.commit()

        resume = Resume(user_id=user.id, filename="test_res.pdf", original_filename="test_res.pdf", file_path="uploads/test_res.pdf", file_type="pdf", file_size=1024)
        db.session.add(resume)

        interview = Interview(user_id=user.id, interview_type="hr", difficulty="medium")
        db.session.add(interview)
        db.session.commit()

        fetched_user = User.query.filter_by(email="db_tester@example.com").first()
        self.assertEqual(len(fetched_user.resumes), 1)
        self.assertEqual(len(fetched_user.interviews), 1)


if __name__ == "__main__":
    unittest.main()
