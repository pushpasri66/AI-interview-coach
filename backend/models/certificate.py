from datetime import datetime
from backend.database import db


class Certificate(db.Model):
    """Database model for verifiable digital certificates with unique credential IDs and verification QR codes."""

    __tablename__ = "certificates"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    certificate_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    verification_url = db.Column(db.String(255), nullable=False)

    def __repr__(self) -> str:
        return f"<Certificate id={self.id} cert_id={self.certificate_id} title={self.title}>"
