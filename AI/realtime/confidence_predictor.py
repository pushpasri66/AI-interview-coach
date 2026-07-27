class ConfidencePredictor:
    """Predicts overall candidate confidence percentage in real-time."""

    def predict_confidence(self, stress_pct: int = 20, clarity_score: int = 85, eye_contact_pct: int = 90) -> dict:
        """Calculates confidence percentage."""
        conf = int((clarity_score * 0.4) + (eye_contact_pct * 0.4) + ((100 - stress_pct) * 0.2))
        return {
            "confidence_percentage": min(99, max(30, conf)),
            "rating": "High Confidence" if conf >= 80 else "Moderate Confidence"
        }
