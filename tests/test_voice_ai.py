import unittest
from backend.services.speech_service import SpeechService


class TestVoiceAI(unittest.TestCase):
    """Unit tests for Phase 7 Voice AI and Speech Processing."""

    def test_01_speech_transcript_processing(self):
        """Test transcript processing and voice feature extraction."""
        speech_svc = SpeechService()
        transcript = speech_svc.process_speech_transcript("I implemented a Flask backend with PostgreSQL.")
        self.assertEqual(transcript, "I implemented a Flask backend with PostgreSQL.")

        metrics = speech_svc.extract_voice_metrics("I implemented a Flask backend with PostgreSQL.", duration_sec=10.0)
        self.assertIn("speech_rate", metrics)
        self.assertIn("clarity_score", metrics)


if __name__ == "__main__":
    unittest.main()
