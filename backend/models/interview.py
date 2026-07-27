from datetime import datetime
from backend.database import db


class Interview(db.Model):
    """Database model storing candidate interview sessions."""
    __tablename__ = "interviews"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    interview_type = db.Column(db.String(50), nullable=False)  # 'hr', 'technical', 'coding', 'company', 'resume'
    company_name = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(50), nullable=True)
    difficulty = db.Column(db.String(20), default="medium", nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    total_questions = db.Column(db.Integer, default=5, nullable=False)
    score = db.Column(db.Integer, default=0, nullable=False)
    status = db.Column(db.String(20), default="in_progress", nullable=False)  # 'in_progress', 'completed'
    report_path = db.Column(db.String(500), nullable=True)

    # Relationships
    questions = db.relationship("Question", backref="interview", cascade="all, delete-orphan", lazy=True)
    answers = db.relationship("Answer", backref="interview", cascade="all, delete-orphan", lazy=True)

    def __repr__(self) -> str:
        return f"<Interview id={self.id} type='{self.interview_type}' score={self.score}>"


class Question(db.Model):
    """Database model for questions generated during an interview session."""
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False, index=True)
    question_text = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=True)
    difficulty = db.Column(db.String(20), default="medium", nullable=False)
    expected_answer = db.Column(db.Text, nullable=True)

    # Relationships
    answers = db.relationship("Answer", backref="question", cascade="all, delete-orphan", lazy=True)

    def __repr__(self) -> str:
        return f"<Question id={self.id} interview_id={self.interview_id}>"


class Answer(db.Model):
    """Database model for candidate responses and AI evaluation scores."""
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False, index=True)
    user_answer = db.Column(db.Text, nullable=False)
    code_language = db.Column(db.String(20), nullable=True)
    answer_score = db.Column(db.Integer, default=0, nullable=False)
    technical_score = db.Column(db.Integer, default=0, nullable=False)
    communication_score = db.Column(db.Integer, default=0, nullable=False)
    relevance_score = db.Column(db.Integer, default=0, nullable=False)
    feedback = db.Column(db.Text, nullable=True)
    strengths = db.Column(db.Text, nullable=True)
    improvements = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Answer id={self.id} question_id={self.question_id} score={self.answer_score}>"
