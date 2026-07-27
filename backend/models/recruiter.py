from datetime import datetime
from backend.database import db


class Recruiter(db.Model):
    """Database model for recruiter accounts and job hiring requirements."""

    __tablename__ = "recruiters"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recruiter_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    company_name = db.Column(db.String(100), nullable=False)
    job_role = db.Column(db.String(100), nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Recruiter id={self.id} company={self.company_name} role={self.job_role}>"
