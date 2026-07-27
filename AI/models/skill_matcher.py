class SkillMatcher:
    """Detects existing skills vs missing skill gaps and calculates priority levels."""

    ROLE_REQUIREMENTS = {
        "AI Engineer": ["Python", "Machine Learning", "NLP", "Flask", "TensorFlow", "Kubernetes", "Cloud Deployment", "Docker"],
        "Machine Learning Engineer": ["Python", "Machine Learning", "Data Analysis", "Deep Learning", "MLOps", "Docker", "PyTorch"],
        "Backend Developer": ["Python", "Flask", "SQL", "PostgreSQL", "REST APIs", "Docker", "Git", "Redis"]
    }

    def analyze_skill_gap(self, target_role: str, user_skills: list) -> dict:
        """Analyzes skill coverage against target role requirements."""
        role_key = target_role if target_role in self.ROLE_REQUIREMENTS else "AI Engineer"
        required_list = self.ROLE_REQUIREMENTS.get(role_key, self.ROLE_REQUIREMENTS["AI Engineer"])

        user_clean = [s.lower().strip() for s in user_skills] if user_skills else ["python", "ml", "flask"]

        available = []
        missing = []

        for req in required_list:
            if any(req.lower() in us or us in req.lower() for us in user_clean):
                available.append(req)
            else:
                missing.append(req)

        coverage = len(available) / max(1, len(required_list))
        priority = "High" if coverage < 0.60 else ("Medium" if coverage < 0.85 else "Low")

        return {
            "target_role": role_key,
            "coverage_percentage": int(coverage * 100),
            "available_skills": available,
            "missing_skills": missing,
            "required_skills": required_list,
            "priority": priority
        }
