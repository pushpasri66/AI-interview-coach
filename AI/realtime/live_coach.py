from AI.realtime.stress_detector import StressDetector
from AI.realtime.confidence_predictor import ConfidencePredictor
from AI.realtime.answer_improver import AnswerImprover


class LiveCoach:
    """Real-time live interview assistant orchestrating stress detection, confidence prediction, and answer suggestions."""

    def __init__(self):
        self.stress_detector = StressDetector()
        self.confidence_predictor = ConfidencePredictor()
        self.answer_improver = AnswerImprover()

    def process_live_feed(self, question: str, answer: str, speech_rate: float = 145.0, eye_contact: float = 88.0) -> dict:
        """Processes live audio/video metrics and generates real-time coaching feedback."""
        stress = self.stress_detector.detect_stress_level(speech_rate, eye_contact_pct=eye_contact)
        confidence = self.confidence_predictor.predict_confidence(stress["stress_percentage"], 85, int(eye_contact))
        improvement = self.answer_improver.improve_answer(question, answer)

        return {
            "stress": stress,
            "confidence": confidence,
            "answer_suggestion": improvement,
            "status": "active"
        }
