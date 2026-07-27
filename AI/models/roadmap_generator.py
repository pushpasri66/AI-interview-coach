class RoadmapGenerator:
    """Generates personalized 4-month learning roadmaps and course recommendations."""

    def generate_roadmap(self, target_role: str = "AI Engineer", missing_skills: list = None) -> dict:
        """Builds a month-by-month structured learning plan."""
        skills = missing_skills if missing_skills else ["Deep Learning", "TensorFlow", "MLOps", "Docker", "Kubernetes", "Cloud"]

        roadmap = {
            "Month 1": {
                "title": "Foundations & Core Technical Mastery",
                "focus": [skills[0] if len(skills) > 0 else "Advanced Python", "SQL & Database Optimization"],
                "action": "Complete core syntax drills, master data manipulation with pandas, and solve 20 algorithmic challenges."
            },
            "Month 2": {
                "title": "Domain Frameworks & Deep Learning",
                "focus": [skills[1] if len(skills) > 1 else "Deep Learning", skills[2] if len(skills) > 2 else "TensorFlow"],
                "action": "Build end-to-end predictive models, tune neural network hyperparameters, and train image/text classifiers."
            },
            "Month 3": {
                "title": "MLOps & Cloud Infrastructure",
                "focus": [skills[3] if len(skills) > 3 else "MLOps", skills[4] if len(skills) > 4 else "Docker & Kubernetes"],
                "action": "Containerize machine learning microservices with Docker, deploy FastAPI containers, and set up CI/CD pipelines."
            },
            "Month 4": {
                "title": "Production Deployment & Mock Interviews",
                "focus": ["Production Cloud Deployment", "System Design & Mock Interviews"],
                "action": "Deploy production applications to cloud (AWS/Azure), practice mock technical interviews, and publish GitHub portfolio."
            }
        }

        courses = [
            {"title": "Complete AI & Machine Learning Masterclass", "platform": "Coursera / Udemy", "duration": "4 Weeks"},
            {"title": "Production MLOps & Docker Microservices", "platform": "edX / DeepLearning.AI", "duration": "3 Weeks"},
            {"title": "Advanced Data Structures & Algorithms", "platform": "LeetCode / HackerRank", "duration": "4 Weeks"}
        ]

        return {
            "target_role": target_role,
            "roadmap": roadmap,
            "suggested_courses": courses
        }
