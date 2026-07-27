import re


class JobAnalyzer:
    """Extracts keywords and required tech skills from job descriptions to compute job compatibility scores."""

    TECH_DICTIONARY = [
        "python", "java", "c++", "sql", "postgresql", "mysql", "mongodb", "flask", "django",
        "fastapi", "html", "css", "javascript", "react", "node.js", "docker", "kubernetes",
        "aws", "azure", "gcp", "machine learning", "deep learning", "nlp", "tensorflow",
        "pytorch", "pandas", "numpy", "scikit-learn", "git", "ci/cd", "rest api", "spark"
    ]

    def analyze_job_description(self, job_description_text: str, user_skills: list) -> dict:
        """Parses job description text and computes job compatibility score."""
        if not job_description_text or not job_description_text.strip():
            return {
                "match_score": 0,
                "matched_skills": [],
                "missing_skills": [],
                "summary": "No job description text provided."
            }

        cleaned_text = job_description_text.lower()
        extracted_jd_skills = set()

        for tech in self.TECH_DICTIONARY:
            if re.search(r"\b" + re.escape(tech) + r"\b", cleaned_text):
                extracted_jd_skills.add(tech.title())

        if not extracted_jd_skills:
            extracted_jd_skills = {"Python", "SQL", "Machine Learning"}

        user_clean = [s.lower().strip() for s in user_skills] if user_skills else ["python", "sql"]

        matched = []
        missing = []

        for req in extracted_jd_skills:
            if any(req.lower() in us or us in req.lower() for us in user_clean):
                matched.append(req)
            else:
                missing.append(req)

        match_score = min(98, max(30, int((len(matched) / max(1, len(extracted_jd_skills))) * 100)))

        return {
            "match_score": match_score,
            "extracted_skills": list(extracted_jd_skills),
            "matched_skills": matched,
            "missing_skills": missing,
            "summary": f"Job Match Score: {match_score}%. Matched: {len(matched)} / {len(extracted_jd_skills)} required skills."
        }
