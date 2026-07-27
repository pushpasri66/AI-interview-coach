class StressDetector:
    """Detects candidate nervousness and stress levels using voice, speech speed, and facial expressions."""

    def detect_stress_level(self, speech_rate_wpm: float = 160.0, pitch_variation: float = 4.0, eye_contact_pct: float = 85.0) -> dict:
        """Computes stress level percentage and nervousness indicator."""
        # High speech speed (>170 wpm) or low pitch variation (<3) indicates stress
        stress_val = 15.0
        if speech_rate_wpm > 170.0:
            stress_val += 25.0
        if eye_contact_pct < 65.0:
            stress_val += 20.0
        if pitch_variation < 3.0:
            stress_val += 15.0

        stress_score = min(95, int(stress_val))
        is_stressed = stress_score > 45

        return {
            "stress_percentage": stress_score,
            "is_stressed": is_stressed,
            "status": "High Stress / Nervousness" if is_stressed else "Calm & Composed"
        }
