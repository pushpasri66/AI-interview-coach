from typing import Dict, Any, List, Optional
from backend.database import db
from backend.models.question_prediction import InterviewPrediction
from backend.models.user import User
from AI.digital_twin.candidate_profile import CandidateProfile
from AI.digital_twin.career_state import CareerState
from AI.question_prediction.resume_question_engine import ResumeQuestionEngine
from AI.question_prediction.job_description_question_engine import JobDescriptionQuestionEngine
from AI.question_prediction.interview_probability import ProbabilityScorer


class QuestionPredictor:
    """Master prediction engine generating likely interview questions across 7 comprehensive categories."""

    def __init__(self):
        self.resume_engine = ResumeQuestionEngine()
        self.jd_engine = JobDescriptionQuestionEngine()
        self.scorer = ProbabilityScorer()

    def predict_questions(
        self,
        candidate_profile: Dict[str, Any],
        target_role: Optional[str] = None,
        target_company: Optional[str] = None,
        job_description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generates comprehensive predicted question set with probability scores and rationale."""
        role = target_role or candidate_profile.get("target_role", "Software Engineer")
        company = target_company or "Tech Enterprise"
        skills = [s.get("skill_name", "") for s in candidate_profile.get("skills", [])]
        projects = candidate_profile.get("career_goals", {}).get("projects_to_build", [])

        # 1. Gather Resume & Project Questions (Project, Technical)
        resume_questions = self.resume_engine.generate_from_resume_and_projects(
            resume_data=candidate_profile.get("resume", {}),
            skills=skills,
            projects=projects
        )

        # 2. Gather Company, JD, System Design, Coding, HR, Behavioral Questions
        jd_questions = self.jd_engine.generate_company_and_jd_questions(
            target_company=company,
            target_role=role,
            job_description=job_description or ""
        )

        # 3. Add Weakness / Skill Gap Probing Questions
        state_evaluator = CareerState(candidate_profile)
        gaps = state_evaluator.find_skill_gaps()
        gap_questions = []
        if gaps:
            top_gap = gaps[0]["skill"]
            prob = self.scorer.compute_probability(category="Technical", is_known_skill_gap=True, role_importance="High")
            gap_questions.append({
                "question": f"How do you evaluate and implement {top_gap} when architecting systems for {role} roles?",
                "probability_score": prob,
                "difficulty": "Hard",
                "category": "Technical",
                "reason": f"Identified as a critical skill gap for {role} in candidate Digital Twin.",
                "expected_focus_areas": [f"Core mechanics of {top_gap}", "Real-world trade-offs", "Best practices"]
            })

        # Combine all questions and ensure no duplicates
        combined_questions = resume_questions + jd_questions + gap_questions
        seen_texts = set()
        unique_questions = []

        for q in combined_questions:
            txt = q["question"].strip()
            if txt not in seen_texts:
                seen_texts.add(txt)
                unique_questions.append(q)

        # Sort by probability score descending
        unique_questions.sort(key=lambda x: x["probability_score"], reverse=True)

        # Compute category breakdown
        breakdown = {}
        for q in unique_questions:
            cat = q["category"]
            breakdown[cat] = breakdown.get(cat, 0) + 1

        highest_prob = unique_questions[0]["probability_score"] if unique_questions else 0

        return {
            "target_role": role,
            "target_company": company,
            "total_predicted_questions": len(unique_questions),
            "highest_probability": highest_prob,
            "category_breakdown": breakdown,
            "predictions": unique_questions
        }

    def predict_and_persist_for_user(
        self,
        user_id: int,
        target_role: Optional[str] = None,
        target_company: Optional[str] = None,
        job_description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generates predictions from user database profile and persists results to database."""
        profile_builder = CandidateProfile(user_id)
        snapshot = profile_builder.build_snapshot()

        result = self.predict_questions(
            candidate_profile=snapshot,
            target_role=target_role,
            target_company=target_company,
            job_description=job_description
        )

        prediction_rec = InterviewPrediction(
            user_id=user_id,
            target_role=result["target_role"],
            target_company=result["target_company"],
            job_description_snippet=job_description[:500] if job_description else None,
            total_predicted_questions=result["total_predicted_questions"],
            highest_probability=result["highest_probability"]
        )
        prediction_rec.set_predictions(result["predictions"])
        prediction_rec.set_category_breakdown(result["category_breakdown"])

        db.session.add(prediction_rec)
        db.session.commit()

        return result
