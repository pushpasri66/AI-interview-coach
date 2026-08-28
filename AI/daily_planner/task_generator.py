import uuid
from typing import Dict, Any, List


class TaskGenerator:
    """Generates personalized daily career development tasks tailored to skill gaps, goals, and interview data."""

    def generate_daily_tasks(
        self,
        candidate_snapshot: Dict[str, Any],
        target_role: str = "Software Engineer",
        target_company: str = "Tech Enterprise"
    ) -> List[Dict[str, Any]]:
        """Generates 4-5 focused daily action items balancing coding, concepts, mock practice, and career assets."""
        tasks = []

        skills = [s.get("skill_name", "") for s in candidate_snapshot.get("skills", [])]
        skills_lower = [s.lower() for s in skills]

        # 1. Skill Gap Tasks (High Priority)
        # Determine missing or gap skills
        if "docker" not in skills_lower and "kubernetes" not in skills_lower:
            tasks.append({
                "id": str(uuid.uuid4())[:8],
                "title": f"Learn Docker Containerization Fundamentals for {target_role}",
                "duration_minutes": 45,
                "category": "Skill Building",
                "priority": "High",
                "digital_twin_skill_impact": "Docker",
                "instructions": "Study Dockerfile layers, multi-stage builds, and container networking.",
                "completed": False,
                "completed_at": None
            })
        elif "aws" not in skills_lower and "cloud" not in skills_lower:
            tasks.append({
                "id": str(uuid.uuid4())[:8],
                "title": f"Master Cloud Computing Basics (AWS S3, EC2, Lambda)",
                "duration_minutes": 45,
                "category": "Skill Building",
                "priority": "High",
                "digital_twin_skill_impact": "AWS",
                "instructions": "Review serverless architecture and IAM security policies.",
                "completed": False,
                "completed_at": None
            })

        # 2. Coding Challenge Task
        primary_lang = skills[0] if skills else "Python"
        tasks.append({
            "id": str(uuid.uuid4())[:8],
            "title": f"Solve 2 {primary_lang} Algorithmic Coding Problems",
            "duration_minutes": 30,
            "category": "Coding Practice",
            "priority": "High",
            "digital_twin_skill_impact": "Problem Solving",
            "instructions": "Focus on Two-Pointers, Sliding Window, or Hash Map complexity optimization.",
            "completed": False,
            "completed_at": None
        })

        # 3. Domain Question Practice
        if "ai" in target_role.lower() or "machine learning" in target_role.lower() or "data" in target_role.lower():
            tasks.append({
                "id": str(uuid.uuid4())[:8],
                "title": "Practice Machine Learning & Deep Learning Core Questions",
                "duration_minutes": 30,
                "category": "Domain Mastery",
                "priority": "Medium",
                "digital_twin_skill_impact": "Machine Learning",
                "instructions": "Review bias-variance tradeoff, gradient descent variants, and evaluation metrics.",
                "completed": False,
                "completed_at": None
            })
        else:
            tasks.append({
                "id": str(uuid.uuid4())[:8],
                "title": "Review System Design & Microservice Patterns",
                "duration_minutes": 30,
                "category": "System Design",
                "priority": "Medium",
                "digital_twin_skill_impact": "System Architecture",
                "instructions": "Study caching strategies (Redis), message queues (Kafka), and database sharding.",
                "completed": False,
                "completed_at": None
            })

        # 4. Resume & Career Asset Optimization
        tasks.append({
            "id": str(uuid.uuid4())[:8],
            "title": f"Tailor Resume Bullet Points for {target_company} {target_role}",
            "duration_minutes": 20,
            "category": "Resume Optimization",
            "priority": "Medium",
            "digital_twin_skill_impact": "Career Presentation",
            "instructions": "Add quantifiable impact metrics (latency reductions, uptime %s) to your top project.",
            "completed": False,
            "completed_at": None
        })

        # 5. HR & Behavioral Mock Practice
        tasks.append({
            "id": str(uuid.uuid4())[:8],
            "title": "Complete 15-Minute HR & Behavioral Mock Session",
            "duration_minutes": 15,
            "category": "Behavioral / HR",
            "priority": "Medium",
            "digital_twin_skill_impact": "Communication",
            "instructions": "Record responses to 'Why this company?' and 'Overcoming technical challenges' using STAR format.",
            "completed": False,
            "completed_at": None
        })

        return tasks
