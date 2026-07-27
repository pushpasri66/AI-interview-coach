import json
from datetime import datetime
from backend.database import db


class Resume(db.Model):
    """Database model for candidate uploaded resumes."""
    __tablename__ = "resumes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    file_type = db.Column(db.String(10), nullable=False)  # 'pdf' or 'docx'
    upload_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Relationships
    analyses = db.relationship("ResumeAnalysis", backref="resume", cascade="all, delete-orphan", lazy=True)

    def __repr__(self) -> str:
        return f"<Resume id={self.id} user_id={self.user_id} filename='{self.filename}'>"


class ResumeAnalysis(db.Model):
    """Database model storing ATS evaluation, parsed structured data, feedback, and report path."""
    __tablename__ = "resume_analyses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resume_id = db.Column(db.Integer, db.ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    ats_score = db.Column(db.Integer, nullable=False, default=0)
    extracted_text = db.Column(db.Text, nullable=True)
    
    # JSON-encoded text fields for structured storage
    parsed_json_data = db.Column(db.Text, nullable=True)
    strengths_json_data = db.Column(db.Text, nullable=True)
    weaknesses_json_data = db.Column(db.Text, nullable=True)
    suggestions_json_data = db.Column(db.Text, nullable=True)
    recommendations_json_data = db.Column(db.Text, nullable=True)
    
    report_path = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Helper getters and setters for JSON fields
    def get_parsed_data(self) -> dict:
        return json.loads(self.parsed_json_data) if self.parsed_json_data else {}

    def set_parsed_data(self, data: dict) -> None:
        self.parsed_json_data = json.dumps(data)

    def get_strengths(self) -> list:
        return json.loads(self.strengths_json_data) if self.strengths_json_data else []

    def set_strengths(self, data: list) -> None:
        self.strengths_json_data = json.dumps(data)

    def get_weaknesses(self) -> list:
        return json.loads(self.weaknesses_json_data) if self.weaknesses_json_data else []

    def set_weaknesses(self, data: list) -> None:
        self.weaknesses_json_data = json.dumps(data)

    def get_suggestions(self) -> list:
        return json.loads(self.suggestions_json_data) if self.suggestions_json_data else []

    def set_suggestions(self, data: list) -> None:
        self.suggestions_json_data = json.dumps(data)

    def get_recommendations(self) -> dict:
        return json.loads(self.recommendations_json_data) if self.recommendations_json_data else {}

    def set_recommendations(self, data: dict) -> None:
        self.recommendations_json_data = json.dumps(data)

    def __repr__(self) -> str:
        return f"<ResumeAnalysis id={self.id} resume_id={self.resume_id} ats_score={self.ats_score}>"
