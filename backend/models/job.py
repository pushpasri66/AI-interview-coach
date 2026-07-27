from datetime import datetime
from backend.database import db


class JobPosting(db.Model):
    """Database model for storing job vacancies and corporate requirements."""

    __tablename__ = "job_postings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), default="Remote")
    required_skills = db.Column(db.Text, nullable=False)
    salary_range = db.Column(db.String(50), default="$90,000 - $140,000")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<JobPosting id={self.id} title={self.title} company={self.company}>"
