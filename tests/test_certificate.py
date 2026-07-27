import unittest
from app import create_app
from backend.database import db
from backend.models.user import User
from backend.services.certificate import CertificateService


class TestCertificateService(unittest.TestCase):
    """Unit tests for Phase 8 Blockchain Digital Certificate Verification."""

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.user = User(fullname="Cert Candidate", email="cert_cand@example.com")
        self.user.set_password("StrongPass123!")
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_01_certificate_issuance_and_verification(self):
        """Test digital certificate issuance and verification URL check."""
        svc = CertificateService()
        cert = svc.issue_certificate(self.user.id, "Certified AI Engineer")
        self.assertIn("CERT-AIC-", cert.certificate_id)

        v_res = svc.verify_certificate(cert.certificate_id)
        self.assertTrue(v_res["valid"])
        self.assertEqual(v_res["title"], "Certified AI Engineer")

        invalid_res = svc.verify_certificate("INVALID-CERT-999")
        self.assertFalse(invalid_res["valid"])


if __name__ == "__main__":
    unittest.main()
