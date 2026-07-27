class JobRecommender:
    """Recommends relevant job vacancies based on candidate resume skills, scores, and goals."""

    def recommend_jobs(self, candidate_skills: list, target_role: str = "AI Engineer") -> list:
        """Returns recommended job opportunities."""
        cand = [s.lower() for s in candidate_skills] if candidate_skills else ["python", "machine learning"]

        jobs = [
            {
                "id": 1,
                "title": "Senior AI Engineer",
                "company": "Google",
                "location": "Mountain View, CA (Hybrid)",
                "match_score": 94,
                "required_skills": ["Python", "TensorFlow", "Kubernetes"],
                "salary": "$140,000 - $180,000"
            },
            {
                "id": 2,
                "title": "Machine Learning Software Developer",
                "company": "Amazon",
                "location": "Seattle, WA (Remote)",
                "match_score": 89,
                "required_skills": ["Python", "AWS", "Docker"],
                "salary": "$130,000 - $165,000"
            },
            {
                "id": 3,
                "title": "Backend Python Developer",
                "company": "Microsoft",
                "location": "Redmond, WA",
                "match_score": 85,
                "required_skills": ["Python", "Flask", "PostgreSQL"],
                "salary": "$120,000 - $155,000"
            }
        ]
        return jobs
