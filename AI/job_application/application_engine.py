from typing import Dict, Any, List, Optional
from datetime import datetime

from backend.database import db
from backend.models.job_application import JobApplicationPackage
from backend.models.user import User
from AI.digital_twin.candidate_profile import CandidateProfile
from AI.job_application.cover_letter_generator import CoverLetterGenerator
from AI.job_application.application_answer_generator import ApplicationAnswerGenerator
from AI.job_application.resume_tailor import ResumeTailor
from AI.question_prediction.question_predictor import QuestionPredictor


class JobApplicationEngine:
    """Master AI engine generating job-specific tailored application packages, cover letters, and ATS optimizations."""

    def __init__(self):
        self.cover_letter_gen = CoverLetterGenerator()
        self.answer_gen = ApplicationAnswerGenerator()
        self.resume_tailor = ResumeTailor()
        self.question_predictor = QuestionPredictor()

    def generate_application_package(
        self,
        user_id: int,
        company_name: str,
        target_role: str,
        job_description: str = "",
        persist: bool = True
    ) -> Dict[str, Any]:
        """Generates a complete, tailored job application bundle."""
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"User #{user_id} does not exist.")

        # 1. Gather profile snapshot
        profile_builder = CandidateProfile(user_id)
        snapshot = profile_builder.build_snapshot()
        candidate_skills = [s["skill_name"] for s in snapshot.get("skills", [])]
        projects = snapshot.get("career_goals", {}).get("projects_to_build", [])
        top_project = projects[0] if projects else "Scalable Microservices Application"

        # 2. Tailor Resume & Calculate ATS Match
        tailored_res = self.resume_tailor.tailor_resume_content(
            candidate_name=user.fullname,
            target_role=target_role,
            company_name=company_name,
            candidate_skills=candidate_skills,
            job_description=job_description,
            existing_projects=projects
        )

        # 3. Generate Cover Letter
        cover_letter_text = self.cover_letter_gen.generate_cover_letter(
            candidate_name=user.fullname,
            candidate_email=user.email,
            company_name=company_name,
            target_role=target_role,
            key_skills=candidate_skills,
            top_project=top_project,
            job_description=job_description
        )

        # 4. Generate Application Answers
        app_answers = self.answer_gen.generate_screening_answers(
            company_name=company_name,
            target_role=target_role,
            skills=candidate_skills,
            top_project=top_project
        )

        # 5. Generate Target Job Interview Preparation Questions
        predicted_q_res = self.question_predictor.predict_questions(
            candidate_profile=snapshot,
            target_role=target_role,
            target_company=company_name,
            job_description=job_description
        )
        interview_questions = predicted_q_res.get("predictions", [])[:5]

        package_dict = {
            "user_id": user.id,
            "candidate_name": user.fullname,
            "company_name": company_name,
            "target_role": target_role,
            "scores": {
                "job_match_score": tailored_res["job_match_score"],
                "application_readiness": tailored_res["application_readiness"],
                "keyword_coverage_pct": tailored_res["ats_keywords"]["keyword_coverage_percentage"]
            },
            "cover_letter": cover_letter_text,
            "tailored_resume": {
                "summary": tailored_res["tailored_summary"],
                "bullet_points": tailored_res["tailored_bullet_points"],
                "highlighted_skills": tailored_res["highlighted_skills"]
            },
            "ats_keywords": tailored_res["ats_keywords"],
            "application_answers": app_answers,
            "interview_questions": interview_questions,
            "missing_skills": tailored_res["missing_skills"],
            "improvement_suggestions": tailored_res["improvement_suggestions"],
            "generated_at": datetime.utcnow().isoformat()
        }

        if persist:
            record = JobApplicationPackage(
                user_id=user.id,
                company_name=company_name,
                target_role=target_role,
                job_description_snippet=job_description[:500] if job_description else None,
                job_match_score=tailored_res["job_match_score"],
                application_readiness=tailored_res["application_readiness"],
                keyword_coverage_pct=tailored_res["ats_keywords"]["keyword_coverage_percentage"],
                cover_letter=cover_letter_text
            )
            record.set_tailored_resume(package_dict["tailored_resume"])
            record.set_ats_keywords(package_dict["ats_keywords"])
            record.set_application_answers(package_dict["application_answers"])
            record.set_interview_questions(package_dict["interview_questions"])
            record.set_missing_skills(package_dict["missing_skills"])
            record.set_improvement_suggestions(package_dict["improvement_suggestions"])

            db.session.add(record)
            db.session.commit()
            package_dict["id"] = record.id

        return package_dict

    def get_application_history(self, user_id: int) -> List[Dict[str, Any]]:
        """Retrieves past generated job application packages for candidate."""
        records = JobApplicationPackage.query.filter_by(user_id=user_id).order_by(JobApplicationPackage.created_at.desc()).all()
        return [r.to_dict() for r in records]
