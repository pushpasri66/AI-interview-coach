class LinkedInAnalyzer:
    """Evaluates LinkedIn profile completeness, headline impact, and keyword density."""

    def analyze_profile_text(self, profile_text: str) -> dict:
        """Analyzes profile headline and text."""
        txt = profile_text.lower() if profile_text else ""
        word_count = len(txt.split())

        has_skills = any(w in txt for w in ["python", "machine learning", "developer", "engineer", "data"])
        has_headline = "headline" in txt or word_count > 10

        headline_score = 85 if has_headline else 60
        summary_score = 90 if word_count > 50 else 70

        return {
            "headline_score": headline_score,
            "summary_score": summary_score,
            "overall_score": int((headline_score + summary_score) / 2),
            "word_count": word_count,
            "has_keywords": has_skills
        }
