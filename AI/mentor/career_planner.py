class CareerPlanner:
    """Generates structured 6-month and 12-month career advancement plans."""

    def generate_career_plan(self, target_role: str = "AI Engineer", duration_months: int = 6) -> dict:
        """Generates 6-month or 12-month career development plan."""
        skills = ["Deep Learning", "MLOps", "Docker", "Kubernetes", "PostgreSQL Optimization"]
        projects = ["Distributed Web Crawler", "Real-Time Emotion Analyzer", "High-Throughput Microservice API"]
        certs = ["AWS Certified Machine Learning - Specialty", "TensorFlow Developer Certificate"]
        timeline = [
            "Months 1-2: Core technical fundamentals & algorithm practice",
            "Months 3-4: Build production portfolio projects & containerization",
            "Months 5-6: System design, mock interviews & corporate applications"
        ]

        if duration_months == 12:
            timeline.extend([
                "Months 7-9: Advanced distributed systems & cloud architecture",
                "Months 10-12: Leadership, technical blogging & senior role interviewing"
            ])

        return {
            "target_role": target_role,
            "duration_months": duration_months,
            "skills_to_learn": skills,
            "projects_to_build": projects,
            "certifications": certs,
            "timeline": timeline
        }
