from AI.models.emotion_detection import EmotionDetector
from AI.models.facial_expression import FacialExpressionAnalyzer
from AI.models.eye_contact import EyeContactDetector


class EmotionService:
    """Service wrapping computer vision, emotion detection, and eye contact calculations."""

    def __init__(self):
        self.emotion_detector = EmotionDetector()
        self.expression_analyzer = FacialExpressionAnalyzer()
        self.eye_contact_detector = EyeContactDetector()

    def analyze_face(self, frame_bytes: bytes = None) -> dict:
        """Analyzes facial frame image for composure and smile level."""
        return self.expression_analyzer.analyze_expression()

    def detect_emotions(self, frame_bytes: bytes = None) -> dict:
        """Detects emotion percentages (happy, neutral, sad, angry, fear, surprise)."""
        return self.emotion_detector.analyze_emotion(frame_bytes=frame_bytes)

    def calculate_eye_contact(self, total_frames: int = 100, gaze_frames: int = 88) -> dict:
        """Calculates eye contact percentage and engagement level."""
        return self.eye_contact_detector.calculate_eye_contact(total_frames, gaze_frames)
