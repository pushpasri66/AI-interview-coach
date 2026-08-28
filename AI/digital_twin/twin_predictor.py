from typing import Dict, Any


class TwinPredictor:
    """Predicts interview success probability, hiring offer likelihood, and role readiness tier."""

    def predict_interview_success_probability(self, readiness: int, interview_readiness: int) -> Dict[str, Any]:
        """Predicts probability of clearing various recruitment rounds."""
        screening_prob = min(99, int(readiness * 0.6 + interview_readiness * 0.4 + 5))
        tech_round_prob = min(98, int(readiness * 0.7 + interview_readiness * 0.3))
        final_round_prob = min(95, int(readiness * 0.5 + interview_readiness * 0.5 - 2))

        return {
            "hr_screening_pass_rate": max(30, screening_prob),
            "technical_round_pass_rate": max(25, tech_round_prob),
            "final_offer_round_pass_rate": max(20, final_round_prob),
            "confidence_band": "High" if readiness >= 80 else ("Moderate" if readiness >= 65 else "Developing")
        }

    def predict_offer_likelihood(self, career_readiness: int, target_compatibility: int) -> Dict[str, Any]:
        """Computes overall job offer likelihood index."""
        combined = int(career_readiness * 0.55 + target_compatibility * 0.45)
        
        if combined >= 85:
            likelihood = "High (85%+)"
            tier = "Tier-1 Tech Companies & Top Startups"
        elif combined >= 70:
            likelihood = "Moderate-High (70-84%)"
            tier = "Mid-to-Large Enterprises & High-Growth Startups"
        else:
            likelihood = "Emerging (50-69%)"
            tier = "Junior/Associate Roles with Mentorship"

        return {
            "index_score": combined,
            "offer_likelihood": likelihood,
            "recommended_company_tier": tier
        }

    def predict_role_seniority_fit(self, readiness_score: int, tech_strength: int) -> Dict[str, Any]:
        """Estimates candidate level fit based on current digital twin metrics."""
        score = (readiness_score + tech_strength) / 2

        if score >= 88:
            level = "Senior / Lead Level"
            experience_band = "4-7+ Years Equivalent"
        elif score >= 75:
            level = "Mid-Level Professional"
            experience_band = "2-4 Years Equivalent"
        else:
            level = "Associate / Junior Developer"
            experience_band = "0-2 Years Equivalent"

        return {
            "recommended_seniority": level,
            "market_experience_band": experience_band,
            "competitive_percentile": min(99, int(score * 1.05))
        }

    def generate_all_predictions(self, readiness: int, interview_readiness: int, tech_strength: int, target_compatibility: int) -> Dict[str, Any]:
        """Generates unified predictive package for the digital twin."""
        return {
            "interview_probabilities": self.predict_interview_success_probability(readiness, interview_readiness),
            "offer_likelihood": self.predict_offer_likelihood(readiness, target_compatibility),
            "seniority_fit": self.predict_role_seniority_fit(readiness, tech_strength)
        }
