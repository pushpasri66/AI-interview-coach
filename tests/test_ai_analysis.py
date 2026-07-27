import os
import unittest
from app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.interview import Interview
from backend.models.ai_analysis import AIAnalysis, VoiceAnalysis, FaceAnalysis

from AI.models.confidence_score import ConfidenceScorer
from AI.models.voice_analysis import VoiceAnalyzer
from AI.models.emotion_detection import EmotionDetector
from AI.models.facial_expression import FacialExpressionAnalyzer
from AI.models.eye_contact import EyeContactDetector
from AI.models.communication_score import CommunicationScorer


class TestAIAnalysisEngine(unittest.TestCase):
    """Unit tests for Phase 4 Advanced AI Interview Analysis Engine."""

    def setUp(self):
        self.app = create_app("development")
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.client = self.app.test_client()

        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create test user
        self.user = User.query.filter_by(email="ai_tester@example.com").first()
        if not self.user:
            self.user = User(fullname="AI Analysis Tester", email="ai_tester@example.com")
            self.user.set_password("Password123!")
            db.session.add(self.user)
            db.session.commit()

        # Login client
        self.client.post("/login", data={
            "email": "ai_tester@example.com",
            "password": "Password123!"
        })

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_01_confidence_scorer(self):
        """Test confidence level score calculation and feedback."""
        scorer = ConfidenceScorer()
        sample_text = "I am confident in building scalable distributed microservices with Python and FastAPI."
        res = scorer.compute_confidence(sample_text, word_count=12, duration_sec=6.0)

        self.assertGreaterEqual(res["confidence_score"], 50)
        self.assertIn("strengths", res)
        self.assertIn("improvements", res)

    def test_02_voice_analyzer(self):
        """Test voice quality, pitch, volume, and clarity evaluation."""
        analyzer = VoiceAnalyzer()
        sample_text = "Optimized PostgreSQL database query indexing."
        res = analyzer.analyze_voice(sample_text, audio_duration_sec=5.0)

        self.assertGreaterEqual(res["voice_score"], 60)
        self.assertIn("clarity_percentage", res)
        self.assertEqual(res["volume_status"], "Good")

    def test_03_emotion_detector_and_facial_expression(self):
        """Test emotion distribution breakdown and composure analysis."""
        detector = EmotionDetector()
        emo_res = detector.analyze_emotion()

        self.assertGreaterEqual(emo_res["professional_score"], 70)
        self.assertIn("neutral", emo_res["emotions"])

        expr_analyzer = FacialExpressionAnalyzer()
        expr_res = expr_analyzer.analyze_expression()
        self.assertGreaterEqual(expr_res["expression_score"], 70)

    def test_04_eye_contact_detector(self):
        """Test eye contact percentage calculation."""
        detector = EyeContactDetector()
        eye_res = detector.calculate_eye_contact(total_frames=100, gaze_frames=90)

        self.assertEqual(eye_res["eye_contact_percentage"], 90.0)
        self.assertEqual(eye_res["status"], "Good")

    def test_05_communication_scorer(self):
        """Test weighted communication score formula: Voice 25% + Conf 25% + Gram 20% + Emo 15% + Eye 15%."""
        scorer = CommunicationScorer()
        res = scorer.compute_communication_score(
            voice_score=80,
            confidence_score=80,
            grammar_score=80,
            emotion_score=80,
            eye_contact_score=80.0
        )

        self.assertEqual(res["communication_score"], 80)

    def test_06_analysis_process_route(self):
        """Test processing analysis API route for an interview session."""
        interview_obj = Interview(
            user_id=self.user.id,
            interview_type="hr",
            difficulty="medium",
            total_questions=1,
            score=85,
            status="completed"
        )
        db.session.add(interview_obj)
        db.session.commit()

        response = self.client.post("/analysis/process", json={
            "interview_id": interview_obj.id
        })

        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertTrue(json_data["success"])
        self.assertGreaterEqual(json_data["communication_score"], 50)

        # Check DB
        ai_rec = AIAnalysis.query.filter_by(interview_id=interview_obj.id).first()
        self.assertIsNotNone(ai_rec)
        self.assertGreaterEqual(ai_rec.communication_score, 50)


if __name__ == "__main__":
    unittest.main()
