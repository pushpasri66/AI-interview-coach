"""
Company model for the AI Interview Coach platform.

Stores company profiles used in target-company mock interviews
and the recruiter portal.
"""
from datetime import datetime
from backend.database import db


class Company(db.Model):
    """Represents a company profile for targeted interview preparation."""

    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False, unique=True, index=True)
    industry = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    website = db.Column(db.String(255), nullable=True)
    logo_url = db.Column(db.String(255), nullable=True)
    headquarters = db.Column(db.String(150), nullable=True)
    employee_count = db.Column(db.String(50), nullable=True)  # e.g. "1000-5000"

    # Interview-specific metadata
    interview_difficulty = db.Column(db.String(20), nullable=True, default="medium")
    known_question_topics = db.Column(db.Text, nullable=True)  # JSON list stored as text
    glassdoor_rating = db.Column(db.Float, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self) -> dict:
        """Return a JSON-serialisable dict representation."""
        return {
            "id": self.id,
            "name": self.name,
            "industry": self.industry,
            "description": self.description,
            "website": self.website,
            "logo_url": self.logo_url,
            "headquarters": self.headquarters,
            "employee_count": self.employee_count,
            "interview_difficulty": self.interview_difficulty,
            "glassdoor_rating": self.glassdoor_rating,
        }

    def __repr__(self) -> str:
        return f"<Company id={self.id} name={self.name!r}>"
