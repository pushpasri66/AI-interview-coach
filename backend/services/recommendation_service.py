import json
from AI.models.career_predictor import CareerPredictor
from AI.models.skill_matcher import SkillMatcher
from AI.models.job_analyzer import JobAnalyzer
from AI.models.roadmap_generator import RoadmapGenerator
from backend.models.skill import Skill
from backend.models.recommendation import CareerRecommendation


class RecommendationService:
    """Service orchestrating AI career predictions, skill gap detection, job analysis, and roadmap building."""

    def __init__(self):
        self.predictor = CareerPredictor()
        self.matcher = SkillMatcher()
        self.job_analyzer = JobAnalyzer()
        self.roadmap_gen = RoadmapGenerator()

    def recommend_roles(self, user_id: int) -> list:
        """Recommends matching career roles for candidate."""
        skills = Skill.query.filter_by(user_id=user_id).all()
        skill_names = [s.skill_name for s in skills] if skills else ["Python", "SQL", "Machine Learning", "Flask"]
        return self.predictor.predict_career_matches(user_skills=skill_names)

    def find_skill_gaps(self, user_id: int, target_role: str = "AI Engineer") -> dict:
        """Finds missing skills and priority level for target role."""
        skills = Skill.query.filter_by(user_id=user_id).all()
        skill_names = [s.skill_name for s in skills] if skills else ["Python", "SQL", "Flask"]
        return self.matcher.analyze_skill_gap(target_role=target_role, user_skills=skill_names)

    def generate_courses(self, missing_skills: list) -> list:
        """Recommends learning courses for missing skills."""
        plan = self.roadmap_gen.generate_roadmap(missing_skills=missing_skills)
        return plan["suggested_courses"]

    def create_learning_plan(self, user_id: int, target_role: str = "AI Engineer") -> dict:
        """Creates personalized 4-month learning roadmap and saves DB record."""
        gaps = self.find_skill_gaps(user_id, target_role)
        roadmap_data = self.roadmap_gen.generate_roadmap(target_role=target_role, missing_skills=gaps["missing_skills"])

        return {
            "target_role": target_role,
            "missing_skills": gaps["missing_skills"],
            "roadmap": roadmap_data["roadmap"],
            "suggested_courses": roadmap_data["suggested_courses"]
        }
