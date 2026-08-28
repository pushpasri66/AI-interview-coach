from typing import Dict, Any, List
from AI.question_prediction.interview_probability import ProbabilityScorer


class ResumeQuestionEngine:
    """Generates high-probability interview questions grounded in candidate resume details and project claims."""

    def __init__(self):
        self.scorer = ProbabilityScorer()

    def generate_from_resume_and_projects(
        self,
        resume_data: Dict[str, Any],
        skills: List[str],
        projects: List[str]
    ) -> List[Dict[str, Any]]:
        """Extracts Project and Technical questions directly tailored to candidate profile."""
        predicted = []
        skills_lower = [s.lower() for s in skills]

        # 1. Project-grounded questions
        for proj in projects:
            proj_lower = proj.lower()
            if any(k in proj_lower for k in ["ml", "cnn", "image", "vision", "classification", "deep learning"]):
                prob = self.scorer.compute_probability(category="Project", has_direct_project=True, has_resume_mention=True)
                predicted.append({
                    "question": f"Explain the CNN/Deep Learning architecture used in your '{proj}' project and how you addressed overfitting.",
                    "probability_score": prob,
                    "difficulty": "Hard",
                    "category": "Project",
                    "reason": f"Candidate highlights '{proj}' involving Machine Learning/Vision in their portfolio.",
                    "expected_focus_areas": ["Model architecture choices", "Loss functions", "Hyperparameter tuning", "Validation metrics"]
                })
            elif any(k in proj_lower for k in ["api", "microservice", "fastapi", "flask", "backend", "distributed"]):
                prob = self.scorer.compute_probability(category="Project", has_direct_project=True, has_resume_mention=True)
                predicted.append({
                    "question": f"How did you design the API endpoints and manage data consistency in '{proj}' under high concurrency?",
                    "probability_score": prob,
                    "difficulty": "Medium",
                    "category": "Project",
                    "reason": f"Candidate has a backend project '{proj}' emphasizing scalable API architecture.",
                    "expected_focus_areas": ["Database indexing", "Caching strategy", "Error handling", "Load handling"]
                })
            elif any(k in proj_lower for k in ["react", "frontend", "fullstack", "web", "collaborative"]):
                prob = self.scorer.compute_probability(category="Project", has_direct_project=True, has_resume_mention=True)
                predicted.append({
                    "question": f"In '{proj}', how did you optimize frontend state management and reduce client-side render latency?",
                    "probability_score": prob,
                    "difficulty": "Medium",
                    "category": "Project",
                    "reason": f"Candidate developed interactive web interface '{proj}'.",
                    "expected_focus_areas": ["State management", "Virtual DOM / component re-renders", "Bundle optimization"]
                })

        # If no specific projects matched, provide general resume project question
        if not predicted and projects:
            prob = self.scorer.compute_probability(category="Project", has_direct_project=True)
            predicted.append({
                "question": f"Walk me through the technical architecture of your project '{projects[0]}' and your primary individual contributions.",
                "probability_score": prob,
                "difficulty": "Medium",
                "category": "Project",
                "reason": "Top featured project on candidate profile.",
                "expected_focus_areas": ["System architecture", "Tech stack tradeoffs", "Key engineering challenges"]
            })

        # 2. Key Skill Deep-Dive Technical Questions
        if "python" in skills_lower:
            prob = self.scorer.compute_probability(category="Technical", has_resume_mention=True, role_importance="Critical")
            predicted.append({
                "question": "How does Python handle memory management and the Global Interpreter Lock (GIL) in multi-threaded environments?",
                "probability_score": prob,
                "difficulty": "Medium",
                "category": "Technical",
                "reason": "Python is listed as a primary language on candidate resume.",
                "expected_focus_areas": ["Reference counting", "Generative garbage collection", "Multiprocessing vs asyncio"]
            })

        if "docker" in skills_lower or "kubernetes" in skills_lower:
            prob = self.scorer.compute_probability(category="Technical", has_resume_mention=True, role_importance="High")
            predicted.append({
                "question": "Explain container isolation mechanisms (cgroups, namespaces) and how you optimize Docker container image layers.",
                "probability_score": prob,
                "difficulty": "Medium",
                "category": "Technical",
                "reason": "Containerization skills (Docker/Kubernetes) are prominent on candidate profile.",
                "expected_focus_areas": ["Multi-stage builds", "Security non-root users", "Kernel namespaces"]
            })

        if "sql" in skills_lower:
            prob = self.scorer.compute_probability(category="Technical", has_resume_mention=True)
            predicted.append({
                "question": "Explain database indexing strategies, B-Trees, and how you investigate a slow-running SQL query.",
                "probability_score": prob,
                "difficulty": "Medium",
                "category": "Technical",
                "reason": "Relational database/SQL experience cited in resume.",
                "expected_focus_areas": ["EXPLAIN ANALYZE", "Clustered vs non-clustered index", "Query execution plans"]
            })

        return predicted
