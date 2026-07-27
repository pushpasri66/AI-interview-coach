class CommunicationScorer:
    """Computes composite Communication Score using weighted multimodal metrics."""

    def compute_communication_score(self, voice_score: int, confidence_score: int, grammar_score: int, emotion_score: int, eye_contact_score: float) -> dict:
        """Applies exact weighted formula: Voice 25% + Confidence 25% + Grammar 20% + Emotion 15% + Eye Contact 15%."""
        
        v_contrib = voice_score * 0.25
        c_contrib = confidence_score * 0.25
        g_contrib = grammar_score * 0.20
        e_contrib = emotion_score * 0.15
        ec_contrib = eye_contact_score * 0.15

        comm_score = min(100, max(0, int(v_contrib + c_contrib + g_contrib + e_contrib + ec_contrib)))

        if comm_score >= 80:
            grade = "Superior Communication & Presence"
        elif comm_score >= 65:
            grade = "Effective Communication"
        else:
            grade = "Needs Practice"

        return {
            "communication_score": comm_score,
            "grade": grade,
            "breakdown": {
                "voice_contribution": round(v_contrib, 1),
                "confidence_contribution": round(c_contrib, 1),
                "grammar_contribution": round(g_contrib, 1),
                "emotion_contribution": round(e_contrib, 1),
                "eye_contact_contribution": round(ec_contrib, 1)
            },
            "summary": f"Communication Score: {comm_score}/100 ({grade})"
        }
