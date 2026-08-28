from typing import Dict, Any, List
from backend.models.user import User
from backend.models.resume import Resume, ResumeAnalysis
from backend.models.skill import Skill
from backend.models.certificate import Certificate
from backend.models.career import CareerPlan
from backend.models.interview import Interview, Answer
from backend.models.ai_analysis import AIAnalysis
from backend.models.analytics import PerformanceAnalytics


class CandidateProfile:
    """Aggregates candidate resume, skills, certifications, interview scores, and career goals into a unified profile."""

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.user = User.query.get(user_id)

    def extract_skills_data(self) -> List[Dict[str, Any]]:
        """Collects candidate skills from database and resumes."""
        skills = Skill.query.filter_by(user_id=self.user_id).all()
        skill_list = []
        for s in skills:
            skill_list.append({
                "skill_name": s.skill_name,
                "skill_level": s.skill_level or "Intermediate",
                "source": s.source or "Profile"
            })

        # Augment with resume skills if available
        latest_resume = Resume.query.filter_by(user_id=self.user_id, is_active=True).order_by(Resume.upload_date.desc()).first()
        if latest_resume:
            analysis = ResumeAnalysis.query.filter_by(resume_id=latest_resume.id).first()
            if analysis:
                parsed = analysis.get_parsed_data()
                resume_skills = parsed.get("skills", [])
                existing_names = {s["skill_name"].lower() for s in skill_list}
                for r_skill in resume_skills:
                    if isinstance(r_skill, str) and r_skill.lower() not in existing_names:
                        skill_list.append({
                            "skill_name": r_skill,
                            "skill_level": "Intermediate",
                            "source": "Resume"
                        })
                        existing_names.add(r_skill.lower())

        return skill_list

    def extract_certifications_data(self) -> List[Dict[str, Any]]:
        """Collects verified certificates."""
        certs = Certificate.query.filter_by(user_id=self.user_id).all()
        return [{
            "id": c.id,
            "title": c.title,
            "certificate_id": c.certificate_id,
            "issue_date": c.issue_date.strftime("%Y-%m-%d") if c.issue_date else None
        } for c in certs]

    def extract_career_goals(self) -> Dict[str, Any]:
        """Collects active career plans and target roles."""
        plan = CareerPlan.query.filter_by(user_id=self.user_id).order_by(CareerPlan.created_at.desc()).first()
        if plan:
            return {
                "target_role": plan.target_role,
                "duration_months": plan.duration_months,
                "skills_to_learn": plan.skills_to_learn.split(",") if plan.skills_to_learn else [],
                "projects_to_build": plan.projects_to_build.split(",") if plan.projects_to_build else []
            }
        return {
            "target_role": "Software Engineer",
            "duration_months": 6,
            "skills_to_learn": ["System Design", "Cloud Architecture"],
            "projects_to_build": ["Scalable Microservices Application"]
        }

    def extract_interview_performance(self) -> Dict[str, Any]:
        """Calculates historical interview, coding, and communication metrics."""
        interviews = Interview.query.filter_by(user_id=self.user_id).all()
        answers = Answer.query.join(Interview).filter(Interview.user_id == self.user_id).all()
        
        completed_interviews = [i for i in interviews if i.status == "completed"]
        coding_interviews = [i for i in completed_interviews if i.interview_type == "coding"]
        technical_interviews = [i for i in completed_interviews if i.interview_type in ["technical", "coding"]]
        hr_interviews = [i for i in completed_interviews if i.interview_type == "hr"]

        avg_overall = int(sum(i.score for i in completed_interviews) / len(completed_interviews)) if completed_interviews else 75
        avg_tech_score = int(sum(a.technical_score for a in answers if a.technical_score) / max(1, len(answers))) if answers else 78
        avg_comm_score = int(sum(a.communication_score for a in answers if a.communication_score) / max(1, len(answers))) if answers else 80

        # AI Multimodal analysis
        ai_analyses = AIAnalysis.query.filter_by(user_id=self.user_id).all()
        avg_confidence = int(sum(a.confidence_score for a in ai_analyses) / len(ai_analyses)) if ai_analyses else 82
        avg_eye_contact = int(sum(a.eye_contact_score for a in ai_analyses) / len(ai_analyses)) if ai_analyses else 85

        return {
            "total_interviews": len(interviews),
            "completed_interviews": len(completed_interviews),
            "coding_interviews_count": len(coding_interviews),
            "avg_overall_score": avg_overall,
            "avg_technical_score": avg_tech_score,
            "avg_communication_score": avg_comm_score,
            "avg_confidence": avg_confidence,
            "avg_eye_contact": avg_eye_contact
        }

    def extract_resume_profile(self) -> Dict[str, Any]:
        """Collects candidate latest resume parsing info and ATS score."""
        latest_resume = Resume.query.filter_by(user_id=self.user_id, is_active=True).order_by(Resume.upload_date.desc()).first()
        if not latest_resume:
            return {
                "has_resume": False,
                "ats_score": 70,
                "parsed_data": {},
                "strengths": ["Clear structure"],
                "weaknesses": ["Upload resume for personalized feedback"]
            }
        
        analysis = ResumeAnalysis.query.filter_by(resume_id=latest_resume.id).first()
        ats_score = analysis.ats_score if analysis else 72
        parsed_data = analysis.get_parsed_data() if analysis else {}
        strengths = analysis.get_strengths() if analysis else ["Relevant technical background"]
        weaknesses = analysis.get_weaknesses() if analysis else ["Add more quantifiable impact"]

        return {
            "has_resume": True,
            "resume_id": latest_resume.id,
            "filename": latest_resume.original_filename,
            "ats_score": ats_score,
            "parsed_data": parsed_data,
            "strengths": strengths,
            "weaknesses": weaknesses
        }

    def build_snapshot(self) -> Dict[str, Any]:
        """Builds a comprehensive profile snapshot combining all career pillars."""
        goals = self.extract_career_goals()
        skills = self.extract_skills_data()
        certs = self.extract_certifications_data()
        interviews = self.extract_interview_performance()
        resume_info = self.extract_resume_profile()

        fullname = self.user.fullname if self.user else "Candidate"
        email = self.user.email if self.user else ""

        return {
            "user_id": self.user_id,
            "fullname": fullname,
            "email": email,
            "target_role": goals["target_role"],
            "career_goals": goals,
            "skills": skills,
            "certifications": certs,
            "interview_performance": interviews,
            "resume": resume_info
        }
