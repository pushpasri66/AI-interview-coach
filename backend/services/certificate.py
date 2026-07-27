import uuid
from datetime import datetime
from backend.database import db
from backend.models.certificate import Certificate


class CertificateService:
    """Blockchain-style digital credential verification service generating unique Certificate IDs and verification URLs."""

    def issue_certificate(self, user_id: int, title: str = "Certified AI Interview Mastery") -> Certificate:
        """Issues a new verifiable digital certificate."""
        cert_id = f"CERT-AIC-{uuid.uuid4().hex[:10].upper()}"
        verify_url = f"/verify_certificate/{cert_id}"

        cert = Certificate(
            user_id=user_id,
            certificate_id=cert_id,
            title=title,
            verification_url=verify_url
        )
        db.session.add(cert)
        db.session.commit()
        return cert

    def verify_certificate(self, certificate_id: str) -> dict:
        """Verifies digital certificate status against database."""
        cert = Certificate.query.filter_by(certificate_id=certificate_id).first()
        if not cert:
            return {"valid": False, "error": "Invalid or non-existent Certificate ID."}

        return {
            "valid": True,
            "certificate_id": cert.certificate_id,
            "title": cert.title,
            "user_id": cert.user_id,
            "issue_date": cert.issue_date.strftime("%B %d, %Y"),
            "verification_url": cert.verification_url
        }
