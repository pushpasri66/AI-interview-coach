class CareerPredictor:
    """AI Machine Learning predictor mapping candidate skills and interview scores to target job roles."""

    JOB_PROFILES = {
        "Machine Learning Engineer": {
            "required_skills": ["python", "machine learning", "data analysis", "deep learning", "mlops", "docker"],
            "description": "Designs and deploys scalable machine learning models, neural networks, and MLOps pipelines."
        },
        "AI Engineer": {
            "required_skills": ["python", "ai", "machine learning", "nlp", "llm", "tensorflow", "pytorch", "cloud"],
            "description": "Builds intelligent AI systems, natural language processing applications, and generative AI solutions."
        },
        "Data Scientist": {
            "required_skills": ["python", "sql", "statistics", "data analysis", "machine learning", "pandas", "scikit-learn"],
            "description": "Extracts actionable insights from complex data structures using predictive modeling and statistical analysis."
        },
        "Backend Developer": {
            "required_skills": ["python", "flask", "django", "sql", "postgresql", "rest api", "docker", "git"],
            "description": "Architects high-performance server APIs, database queries, and distributed backend applications."
        },
        "Software Developer": {
            "required_skills": ["python", "javascript", "data structures", "algorithms", "git", "sql", "html", "css"],
            "description": "Engineers full-stack web applications, clean software architectures, and automated testing."
        },
        "Data Analyst": {
            "required_skills": ["sql", "python", "excel", "power bi", "tableau", "data analysis", "statistics"],
            "description": "Transforms raw transactional data into business intelligence dashboards and statistical reports."
        }
    }

    def predict_career_matches(self, user_skills: list, avg_tech_score: int = 75) -> list:
        """Computes matching percentage and skill gaps for candidate against target job roles."""
        user_skills_clean = [s.lower().strip() for s in user_skills] if user_skills else ["python", "sql", "machine learning"]

        results = []
        for role_name, profile in self.JOB_PROFILES.items():
            req_skills = profile["required_skills"]
            matched = [s for s in req_skills if any(s in us or us in s for us in user_skills_clean)]
            missing = [s for s in req_skills if s not in matched]

            skill_match_ratio = len(matched) / max(1, len(req_skills))
            score_factor = min(1.0, max(0.5, avg_tech_score / 100.0))
            
            raw_pct = int((skill_match_ratio * 0.70 + score_factor * 0.30) * 100)
            final_match = min(98, max(45, raw_pct))

            results.append({
                "role": role_name,
                "match_percentage": final_match,
                "description": profile["description"],
                "strengths": [m.title() for m in matched[:4]],
                "missing_skills": [m.title() for m in missing]
            })

        # Sort by match percentage descending
        results.sort(key=lambda x: x["match_percentage"], reverse=True)
        return results
