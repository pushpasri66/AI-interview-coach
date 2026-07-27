import os
import unittest
import io
from app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.resume import Resume, ResumeAnalysis
from backend.services.resume_parser import ResumeParser
from AI.models.ats_score import ATSScoreCalculator
from AI.models.resume_analysis import ResumeAnalyzer
from AI.models.recommendation import ResumeRecommender
from backend.services.ats_service import ATSService


class TestResumeAnalyzer(unittest.TestCase):
    """Unit tests for Phase 2 Resume Analyzer & ATS Engine."""

    def setUp(self):
        self.app = create_app("development")
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.client = self.app.test_client()

        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create test user
        self.user = User.query.filter_by(email="resume_tester@example.com").first()
        if not self.user:
            self.user = User(fullname="Resume Tester", email="resume_tester@example.com")
            self.user.set_password("Password123!")
            db.session.add(self.user)
            db.session.commit()

        # Login client
        self.client.post("/login", data={
            "email": "resume_tester@example.com",
            "password": "Password123!"
        })

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_01_resume_parser_structured_data(self):
        """Test resume text extraction and field parsing."""
        sample_resume_text = """
        John Candidate
        john.candidate@example.com | (555) 123-4567 | linkedin.com/in/johncandidate | github.com/johncandidate
        
        SKILLS
        Programming: Python, JavaScript, TypeScript, SQL
        Frameworks: React, Django, Flask, FastAPI
        Tools: Git, Docker, Kubernetes, AWS, PostgreSQL
        Soft Skills: Leadership, Communication, Problem Solving
        
        EXPERIENCE
        Senior Software Engineer - Tech Solutions (2022 - Present)
        • Built scalable microservices using Python, FastAPI, and Docker.
        • Optimized PostgreSQL database queries reducing response time by 40%.
        
        EDUCATION
        B.S. in Computer Science - State University
        
        CERTIFICATIONS
        AWS Certified Solutions Architect
        """
        parser = ResumeParser()
        parsed = parser.parse_resume(sample_resume_text)

        self.assertEqual(parsed["email"], "john.candidate@example.com")
        self.assertIn("Python", parsed["technical_skills"])
        self.assertIn("React", parsed["frameworks"])
        self.assertIn("Docker", parsed["tools"])
        self.assertIn("Leadership", parsed["soft_skills"])

    def test_02_ats_score_calculation(self):
        """Test ATS 100-point score calculator."""
        parsed_data = {
            "name": "John Candidate",
            "email": "john@example.com",
            "phone": "555-123-4567",
            "linkedin": "linkedin.com/in/john",
            "github": "github.com/john",
            "technical_skills": ["Python", "React", "Django", "Docker", "AWS", "SQL"],
            "soft_skills": ["Leadership", "Communication"],
            "experience": ["Software Engineer"],
            "education": ["Computer Science"],
            "projects": ["Web App"],
            "certifications": ["AWS Certified"],
            "word_count": 450
        }
        raw_text = "Built and engineered scalable web applications using Python and React."

        calculator = ATSScoreCalculator()
        score_res = calculator.compute_score(parsed_data, raw_text)

        self.assertGreaterEqual(score_res["overall_score"], 60)
        self.assertIn(score_res["grade"], ["Excellent", "Good", "Needs Improvement"])
        self.assertIn("contact_info", score_res["categories"])

    def test_03_resume_upload_and_db(self):
        """Test uploading a sample resume file."""
        sample_file_content = b"John Tester\ntester@example.com\nPython Developer with React and SQL experience."
        data = {
            "resume_file": (io.BytesIO(sample_file_content), "sample_test_resume.pdf")
        }

        response = self.client.post("/resume/upload", data=data, content_type="multipart/form-data", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check DB
        res_record = Resume.query.filter_by(user_id=self.user.id).order_by(Resume.upload_date.desc()).first()
        self.assertIsNotNone(res_record)
        self.assertEqual(res_record.original_filename, "sample_test_resume.pdf")

        analysis_record = ResumeAnalysis.query.filter_by(resume_id=res_record.id).first()
        self.assertIsNotNone(analysis_record)
        self.assertGreaterEqual(analysis_record.ats_score, 0)

    def test_04_pdf_report_generation(self):
        """Test PDF report generation service."""
        res_record = Resume(
            user_id=self.user.id,
            filename="1_test_file.pdf",
            original_filename="test_file.pdf",
            file_path="uploads/resumes/1_test_file.pdf",
            file_size=1024,
            file_type="pdf"
        )
        db.session.add(res_record)
        db.session.commit()

        analysis_record = ResumeAnalysis(
            resume_id=res_record.id,
            user_id=self.user.id,
            ats_score=85
        )
        analysis_record.set_parsed_data({"name": "Test User", "technical_skills": ["Python", "Flask"]})
        analysis_record.set_strengths(["Strong Skills"])
        analysis_record.set_weaknesses(["Missing Certifications"])
        analysis_record.set_suggestions(["Add Certifications"])
        analysis_record.set_recommendations({"color": "#10b981", "recommended_courses": []})
        db.session.add(analysis_record)
        db.session.commit()

        service = ATSService()
        report_path = service.generate_pdf_report(self.user.fullname, res_record, analysis_record)

        self.assertTrue(report_path.startswith("reports/interview_reports/"))
        abs_path = os.path.abspath(os.path.join(self.app.root_path, report_path))
        self.assertTrue(os.path.exists(abs_path))


if __name__ == "__main__":
    unittest.main()
