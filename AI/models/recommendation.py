class ResumeRecommender:
    """Generates AI recommendations, missing skill detection, courses, and interview topics."""

    TRENDING_TECH = [
        "Docker", "Kubernetes", "TypeScript", "Next.js", "FastAPI",
        "React Native", "GraphQL", "AWS", "PyTorch", "TailwindCSS"
    ]

    COURSE_RECOMMENDATIONS = [
        {"title": "Grokking System Design Architecture", "provider": "Educative / Coursera", "level": "Intermediate to Advanced"},
        {"title": "Docker & Kubernetes: The Practical Guide", "provider": "Udemy", "level": "Intermediate"},
        {"title": "Full Stack Web Development with React & FastAPI", "provider": "Udemy / YouTube", "level": "Beginner to Intermediate"},
        {"title": "AWS Certified Solutions Architect Associate", "provider": "AWS Training / Stephane Maarek", "level": "Intermediate"}
    ]

    INTERVIEW_PREP_TOPICS = [
        "Data Structures & Algorithms (Trees, Graphs, Dynamic Programming)",
        "System Design (Load Balancing, Caching, Database Sharding)",
        "Object-Oriented Design & Clean Code Principles",
        "Behavioral STAR Technique (Situation, Task, Action, Result)",
        "RESTful API & Microservices Architecture"
    ]

    def generate_recommendations(self, parsed_data: dict) -> dict:
        """Generates domain skill gaps, course suggestions, and interview topics."""
        existing_skills = [s.lower() for s in parsed_data.get("technical_skills", [])]

        # Identify missing trending technologies
        missing_skills = [
            tech for tech in self.TRENDING_TECH
            if tech.lower() not in existing_skills
        ]

        improvements = [
            "Quantify bullet points with metrics (e.g., 'Reduced API latency by 40%').",
            "Keep formatting clean with consistent font sizes and 1-inch margins.",
            "Add a concise 2-sentence executive summary emphasizing your specialization.",
            "Highlight modern CI/CD pipeline and cloud deployment experience."
        ]

        return {
            "missing_skills": missing_skills[:6],
            "trending_technologies": self.TRENDING_TECH[:6],
            "recommended_courses": self.COURSE_RECOMMENDATIONS,
            "interview_prep_topics": self.INTERVIEW_PREP_TOPICS,
            "resume_improvements": improvements
        }
