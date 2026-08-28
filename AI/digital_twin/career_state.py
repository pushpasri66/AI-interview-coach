from typing import Dict, Any, List


class CareerState:
    """Calculates multi-dimensional career health, scores, skill gaps, and strengths."""

    ROLE_BENCHMARKS = {
        "Software Engineer": {
            "core_skills": ["Python", "Data Structures", "Algorithms", "SQL", "Git", "System Design"],
            "tech_weight": 0.40,
            "comm_weight": 0.25,
            "interview_weight": 0.35
        },
        "Full Stack Developer": {
            "core_skills": ["JavaScript", "React", "Node.js", "Python", "SQL", "HTML/CSS", "REST APIs"],
            "tech_weight": 0.45,
            "comm_weight": 0.20,
            "interview_weight": 0.35
        },
        "AI / ML Engineer": {
            "core_skills": ["Python", "Machine Learning", "Deep Learning", "TensorFlow/PyTorch", "SQL", "Data Analysis"],
            "tech_weight": 0.50,
            "comm_weight": 0.20,
            "interview_weight": 0.30
        },
        "DevOps / Cloud Engineer": {
            "core_skills": ["Docker", "Kubernetes", "AWS/Cloud", "CI/CD", "Linux", "Terraform", "Python"],
            "tech_weight": 0.45,
            "comm_weight": 0.20,
            "interview_weight": 0.35
        },
        "Data Scientist": {
            "core_skills": ["Python", "SQL", "Statistics", "Pandas/NumPy", "Data Visualization", "Machine Learning"],
            "tech_weight": 0.45,
            "comm_weight": 0.25,
            "interview_weight": 0.30
        }
    }

    def __init__(self, profile_data: Dict[str, Any]):
        self.profile = profile_data
        self.target_role = profile_data.get("target_role", "Software Engineer")
        if self.target_role not in self.ROLE_BENCHMARKS:
            self.target_role = "Software Engineer"

    def compute_skill_strength(self) -> int:
        """Calculates skill proficiency strength score (0-100)."""
        skills = self.profile.get("skills", [])
        if not skills:
            return 65

        level_weights = {
            "beginner": 50,
            "intermediate": 75,
            "advanced": 90,
            "expert": 100
        }
        scores = []
        for s in skills:
            lvl = str(s.get("skill_level", "intermediate")).lower()
            scores.append(level_weights.get(lvl, 75))

        base_score = sum(scores) / len(scores) if scores else 70
        # Boost based on skill count breadth
        breadth_boost = min(15, len(skills) * 2)
        final_score = int(min(100, max(40, base_score * 0.85 + breadth_boost)))
        return final_score

    def compute_technical_strength(self) -> int:
        """Computes technical performance across coding, skill depth, and technical interviews."""
        interview_perf = self.profile.get("interview_performance", {})
        avg_tech_interview = interview_perf.get("avg_technical_score", 78)
        skill_str = self.compute_skill_strength()
        ats_score = self.profile.get("resume", {}).get("ats_score", 75)

        tech_score = int(avg_tech_interview * 0.45 + skill_str * 0.35 + ats_score * 0.20)
        return min(100, max(30, tech_score))

    def compute_communication_strength(self) -> int:
        """Computes candidate communication, confidence, and speech fluency score."""
        interview_perf = self.profile.get("interview_performance", {})
        avg_comm = interview_perf.get("avg_communication_score", 80)
        avg_conf = interview_perf.get("avg_confidence", 82)
        avg_eye = interview_perf.get("avg_eye_contact", 85)

        comm_score = int(avg_comm * 0.45 + avg_conf * 0.35 + avg_eye * 0.20)
        return min(100, max(35, comm_score))

    def compute_interview_readiness(self) -> int:
        """Computes overall interview readiness based on completed sessions and past results."""
        interview_perf = self.profile.get("interview_performance", {})
        completed = interview_perf.get("completed_interviews", 0)
        avg_overall = interview_perf.get("avg_overall_score", 75)

        # Experience factor based on simulation counts
        volume_multiplier = min(1.15, 0.85 + (completed * 0.05))
        readiness = int(avg_overall * volume_multiplier)
        return min(100, max(40, readiness))

    def compute_career_readiness_score(self) -> int:
        """Computes composite career readiness score across technical, communication, and ATS indicators."""
        tech_score = self.compute_technical_strength()
        comm_score = self.compute_communication_strength()
        interview_readiness = self.compute_interview_readiness()
        skill_strength = self.compute_skill_strength()
        ats_score = self.profile.get("resume", {}).get("ats_score", 75)

        composite = int(
            tech_score * 0.30 +
            comm_score * 0.25 +
            interview_readiness * 0.25 +
            skill_strength * 0.10 +
            ats_score * 0.10
        )
        return min(100, max(35, composite))

    def compute_job_compatibility(self) -> Dict[str, int]:
        """Evaluates compatibility percentages across top industry roles."""
        user_skills = {str(s.get("skill_name", "")).lower() for s in self.profile.get("skills", [])}
        tech_score = self.compute_technical_strength()
        interview_score = self.compute_interview_readiness()

        compatibilities = {}
        for role, data in self.ROLE_BENCHMARKS.items():
            req_skills = data["core_skills"]
            matched_count = sum(1 for req in req_skills if any(req.lower() in us or us in req.lower() for us in user_skills))
            skill_match_ratio = matched_count / max(1, len(req_skills))

            role_compat = int((skill_match_ratio * 100) * 0.50 + tech_score * 0.30 + interview_score * 0.20)
            compatibilities[role] = min(98, max(45, role_compat))

        return compatibilities

    def find_skill_gaps(self) -> List[Dict[str, Any]]:
        """Identifies missing benchmark skills for target role with improvement roadmaps."""
        user_skills = {str(s.get("skill_name", "")).lower() for s in self.profile.get("skills", [])}
        role_data = self.ROLE_BENCHMARKS.get(self.target_role, self.ROLE_BENCHMARKS["Software Engineer"])
        required_skills = role_data["core_skills"]

        gaps = []
        for req in required_skills:
            has_skill = any(req.lower() in us or us in req.lower() for us in user_skills)
            if not has_skill:
                gaps.append({
                    "skill": req,
                    "target_role": self.target_role,
                    "importance": "High" if req in required_skills[:3] else "Medium",
                    "learning_timeline": "2-3 Weeks",
                    "action": f"Practice hands-on projects and mock interview questions targeting {req}."
                })

        return gaps

    def extract_strengths_and_weaknesses(self) -> tuple[List[str], List[str]]:
        """Extracts high-level strengths and weaknesses."""
        tech = self.compute_technical_strength()
        comm = self.compute_communication_strength()
        interview = self.compute_interview_readiness()
        skills = self.profile.get("skills", [])

        strengths = []
        weaknesses = []

        if tech >= 80:
            strengths.append("High technical proficiency and problem solving ability.")
        else:
            weaknesses.append("Need deeper practice on core data structures and architectural design.")

        if comm >= 80:
            strengths.append("Clear verbal communication, confidence, and articulation.")
        else:
            weaknesses.append("Work on minimizing filler words and enhancing structured responses.")

        if interview >= 80:
            strengths.append("Consistent interview performance with high success probability.")
        else:
            weaknesses.append("Increase mock interview volume to build pressure resilience.")

        if len(skills) >= 5:
            strengths.append(f"Diverse technical skill stack across {len(skills)} competencies.")
        else:
            weaknesses.append("Expand skill portfolio with modern in-demand frameworks.")

        return strengths, weaknesses

    def generate_recommendations(self) -> List[str]:
        """Generates actionable next steps for candidate career advancement."""
        gaps = self.find_skill_gaps()
        readiness = self.compute_career_readiness_score()

        recs = []
        if gaps:
            top_gap = gaps[0]["skill"]
            recs.append(f"Prioritize mastering {top_gap} to increase job compatibility for {self.target_role}.")
        
        if readiness < 80:
            recs.append("Complete at least 2 more mock technical interview sessions this week.")
        else:
            recs.append("You are in a prime readiness zone. Start applying for target tier-1 job openings.")

        recs.append(f"Optimize your resume keywords specifically tailored to '{self.target_role}'.")
        return recs

    def evaluate_state(self) -> Dict[str, Any]:
        """Produces full career state evaluation."""
        strengths, weaknesses = self.extract_strengths_and_weaknesses()
        return {
            "career_readiness_score": self.compute_career_readiness_score(),
            "interview_readiness": self.compute_interview_readiness(),
            "technical_strength": self.compute_technical_strength(),
            "communication_strength": self.compute_communication_strength(),
            "skill_strength": self.compute_skill_strength(),
            "target_role": self.target_role,
            "job_compatibility": self.compute_job_compatibility(),
            "skill_gaps": self.find_skill_gaps(),
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": self.generate_recommendations()
        }
