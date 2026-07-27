from datetime import datetime
from backend.database import db


class AIAnalysis(db.Model):
    """Database model storing overall AI multimodal analysis metrics for an interview."""
    __tablename__ = "ai_analyses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False, index=True)
    confidence_score = db.Column(db.Integer, default=0, nullable=False)
    emotion_score = db.Column(db.Integer, default=0, nullable=False)
    eye_contact_score = db.Column(db.Integer, default=0, nullable=False)
    voice_score = db.Column(db.Integer, default=0, nullable=False)
    communication_score = db.Column(db.Integer, default=0, nullable=False)
    overall_score = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<AIAnalysis id={self.id} interview_id={self.interview_id} overall_score={self.overall_score}>"


class VoiceAnalysis(db.Model):
    """Database model storing detailed audio and voice quality features."""
    __tablename__ = "voice_analyses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False, index=True)
    speech_rate = db.Column(db.Integer, default=140, nullable=False)  # words per minute
    pitch_score = db.Column(db.Integer, default=80, nullable=False)
    volume_score = db.Column(db.Integer, default=85, nullable=False)
    clarity_score = db.Column(db.Integer, default=85, nullable=False)
    filler_words_count = db.Column(db.Integer, default=0, nullable=False)
    pause_duration = db.Column(db.Float, default=0.0, nullable=False)  # total pause seconds

    def __repr__(self) -> str:
        return f"<VoiceAnalysis id={self.id} interview_id={self.interview_id} speech_rate={self.speech_rate}>"


class FaceAnalysis(db.Model):
    """Database model storing facial emotion distribution and eye contact ratios."""
    __tablename__ = "face_analyses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    interview_id = db.Column(db.Integer, db.ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False, index=True)
    happiness = db.Column(db.Float, default=0.20, nullable=False)
    neutral = db.Column(db.Float, default=0.70, nullable=False)
    sadness = db.Column(db.Float, default=0.05, nullable=False)
    anger = db.Column(db.Float, default=0.02, nullable=False)
    fear = db.Column(db.Float, default=0.03, nullable=False)
    eye_contact_percentage = db.Column(db.Float, default=85.0, nullable=False)

    def __repr__(self) -> str:
        return f"<FaceAnalysis id={self.id} interview_id={self.interview_id} eye_contact={self.eye_contact_percentage}%>"
