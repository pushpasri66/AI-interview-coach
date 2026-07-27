import os
import unittest
from backend.services.resume_builder import ResumeBuilderService


class TestResumeBuilder2(unittest.TestCase):
    """Unit tests for Phase 8 AI Resume Builder & Optimizer 2.0."""

    def test_01_content_generation_and_exporters(self):
        """Test resume content generation and PDF/DOCX file exporters."""
        builder = ResumeBuilderService()
        content = builder.generate_resume_content("Bob Developer", "ai_engineer", ["Python", "Flask", "Docker"])

        self.assertEqual(content["fullname"], "Bob Developer")
        self.assertIn("Python", content["summary"])

        docx_path = builder.generate_docx_resume(content, user_id=99)
        self.assertTrue(docx_path.endswith(".docx"))

        pdf_path = builder.generate_pdf_resume(content, user_id=99)
        self.assertTrue(pdf_path.endswith(".pdf"))


if __name__ == "__main__":
    unittest.main()
