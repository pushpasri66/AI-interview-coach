from typing import Dict, Any, List, Optional
from datetime import datetime

from backend.database import db
from backend.models.daily_task import DailyPlan
from backend.models.user import User
from AI.digital_twin.candidate_profile import CandidateProfile
from AI.digital_twin.digital_twin_engine import DigitalTwinEngine
from AI.daily_planner.task_generator import TaskGenerator
from AI.daily_planner.progress_optimizer import ProgressOptimizer
from AI.explainable.score_explainer import ScoreExplainer


class DailyPlanEngine:
    """Master engine generating, managing, and tracking personalized daily career plans with Explainable AI."""

    def __init__(self):
        self.task_generator = TaskGenerator()
        self.optimizer = ProgressOptimizer()
        self.score_explainer = ScoreExplainer()
        self.twin_engine = DigitalTwinEngine()

    def get_or_create_daily_plan(
        self,
        user_id: int,
        plan_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """Retrieves existing daily plan for date or synthesizes a fresh personalized plan."""
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"User #{user_id} does not exist.")

        today_str = plan_date or datetime.utcnow().strftime("%Y-%m-%d")
        plan_record = DailyPlan.query.filter_by(user_id=user_id, plan_date=today_str).first()

        profile_builder = CandidateProfile(user_id)
        snapshot = profile_builder.build_snapshot()
        target_role = snapshot.get("target_role", "Software Engineer")
        target_company = "Tech Enterprise"

        if not plan_record:
            tasks = self.task_generator.generate_daily_tasks(
                candidate_snapshot=snapshot,
                target_role=target_role,
                target_company=target_company
            )

            plan_record = DailyPlan(
                user_id=user_id,
                plan_date=today_str
            )
            plan_record.set_tasks(tasks)
            db.session.add(plan_record)
            db.session.commit()

        # Generate Explainable AI breakdown for today's plan
        twin_data = self.twin_engine.get_digital_twin_state(user_id, auto_sync=False)
        level_map = {"beginner": 65, "intermediate": 80, "advanced": 92, "expert": 98}
        skill_scores = {
            s.get("skill_name", "Skill"): s.get("proficiency_score", level_map.get(s.get("skill_level", "intermediate").lower(), 80))
            for s in snapshot.get("skills", [])
        }
        if not skill_scores:
            skill_scores = {"Python": 92, "Problem Solving": 85, "System Design": 70, "Communication": 78}

        missing_skills = [g["skill"] for g in twin_data.get("skill_gaps", [])]
        if not missing_skills:
            missing_skills = ["Docker", "Cloud Deployment"]

        explainable_analysis = self.score_explainer.explain_career_match_score(
            score_value=twin_data.get("scores", {}).get("career_readiness_score", 82),
            target_role=target_role,
            skill_scores=skill_scores,
            missing_skills=missing_skills,
            interview_scores={"average_score": twin_data.get("scores", {}).get("interview_readiness", 75)}
        )

        schedule_opt = self.optimizer.optimize_daily_schedule(plan_record.get_tasks())

        return {
            "id": plan_record.id,
            "user_id": user_id,
            "candidate_name": user.fullname,
            "plan_date": today_str,
            "target_role": target_role,
            "metrics": schedule_opt,
            "tasks": plan_record.get_tasks(),
            "explainable_ai": explainable_analysis,
            "created_at": plan_record.created_at.isoformat() if plan_record.created_at else None
        }

    def complete_task(
        self,
        user_id: int,
        task_id: str,
        completed: bool = True
    ) -> Dict[str, Any]:
        """Marks a daily task complete, recalculates progress, and updates the candidate's Digital Twin."""
        today_str = datetime.utcnow().strftime("%Y-%m-%d")
        plan_record = DailyPlan.query.filter_by(user_id=user_id, plan_date=today_str).first()

        if not plan_record:
            # Create today's plan first
            self.get_or_create_daily_plan(user_id, today_str)
            plan_record = DailyPlan.query.filter_by(user_id=user_id, plan_date=today_str).first()

        success = plan_record.mark_task_status(task_id=task_id, completed=completed)
        db.session.commit()

        # Update candidate Digital Twin with learning activity
        twin_update = self.twin_engine.sync_user_twin(user_id, trigger_event="daily_task_completed")

        schedule_opt = self.optimizer.optimize_daily_schedule(plan_record.get_tasks())

        return {
            "success": success,
            "task_id": task_id,
            "completed": completed,
            "daily_plan": {
                "id": plan_record.id,
                "plan_date": plan_record.plan_date,
                "metrics": schedule_opt,
                "tasks": plan_record.get_tasks()
            },
            "digital_twin_synced": True,
            "updated_readiness_score": twin_update.career_readiness_score
        }

