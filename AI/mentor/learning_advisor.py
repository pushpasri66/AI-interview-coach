class LearningAdvisor:
    """Recommends courses, books, practice platforms, and AI tools."""

    def recommend_learning_resources(self, target_role: str = "AI Engineer") -> dict:
        """Returns curated learning resources."""
        return {
            "courses": [
                {"title": "Deep Learning Specialization", "platform": "Coursera"},
                {"title": "Docker & Kubernetes: The Practical Guide", "platform": "Udemy"}
            ],
            "books": [
                "Designing Data-Intensive Applications by Martin Kleppmann",
                "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow"
            ],
            "practice_platforms": ["LeetCode", "HackerRank", "Kaggle"],
            "ai_tools": ["GitHub Copilot", "ChatGPT Plus", "LangChain"]
        }
