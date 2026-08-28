import json
from datetime import datetime
from backend.database import db


class JobApplicationPackage(db.Model):
    """Database model storing tailored job applications, cover letters, tailored resumes, and application answers."""

    __tablename__ = "job_applications"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    company_name = db.Column(db.String(100), nullable=False)
    target_role = db.Column(db.String(100), nullable=False)
    job_description_snippet = db.Column(db.Text, nullable=True)
    
    # Quantitative Scores (0-100)
    job_match_score = db.Column(db.Integer, default=0, nullable=False)
    application_readiness = db.Column(db.Integer, default=0, nullable=False)
    keyword_coverage_pct = db.Column(db.Integer, default=0, nullable=False)
    
    cover_letter = db.Column(db.Text, nullable=False)
    
    # JSON structured payloads
    tailored_resume_json = db.Column(db.Text, nullable=True)
    ats_keywords_json = db.Column(db.Text, nullable=True)
    application_answers_json = db.Column(db.Text, nullable=True)
    interview_questions_json = db.Column(db.Text, nullable=True)
    missing_skills_json = db.Column(db.Text, nullable=True)
    improvement_suggestions_json = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def get_tailored_resume(self) -> dict:
        return json.loads(self.tailored_resume_json) if self.tailored_resume_json else {}

    def set_tailored_resume(self, data: dict) -> None:
        self.tailored_resume_json = json.dumps(data)

    def get_ats_keywords(self) -> dict:
        return json.loads(self.ats_keywords_json) if self.ats_keywords_json else {}

    def set_ats_keywords(self, data: dict) -> None:
        self.ats_keywords_json = json.dumps(data)

    def get_application_answers(self) -> list:
        return json.loads(self.application_answers_json) if self.application_answers_json else []

    def set_application_answers(self, data: list) -> None:
        self.application_answers_json = json.dumps(data)

    def get_interview_questions(self) -> list:
        return json.loads(self.interview_questions_json) if self.interview_questions_json else []

    def set_interview_questions(self, data: list) -> None:
        self.interview_questions_json = json.dumps(data)

    def get_missing_skills(self) -> list:
        return json.loads(self.missing_skills_json) if self.missing_skills_json else []

    def set_missing_skills(self, data: list) -> None:
        self.missing_skills_json = json.dumps(data)

    def get_improvement_suggestions(self) -> list:
        return json.loads(self.improvement_suggestions_json) if self.improvement_suggestions_json else []

    def set_improvement_suggestions(self, data: list) -> None:
        self.improvement_suggestions_json = json.dumps(data)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "company_name": self.company_name,
            "target_role": self.target_role,
            "job_match_score": self.job_match_score,
            "application_readiness": self.application_readiness,
            "keyword_coverage_pct": self.keyword_coverage_pct,
            "cover_letter": self.cover_letter,
            "tailored_resume": self.get_tailored_resume(),
            "ats_keywords": self.get_ats_keywords(),
            "application_answers": self.get_application_answers(),
            "interview_questions": self.get_interview_questions(),
            "missing_skills": self.get_missing_skills(),
            "improvement_suggestions": self.get_improvement_suggestions(),
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self) -> str:
        return f"<JobApplicationPackage id={self.id} user_id={self.user_id} company='{self.company_name}' role='{self.target_role}'>"
