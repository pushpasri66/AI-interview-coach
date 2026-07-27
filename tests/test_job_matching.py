import unittest
from AI.job_matching.job_recommender import JobRecommender
from AI.job_matching.skill_gap_predictor import SkillGapPredictor
from AI.job_matching.salary_predictor import SalaryPredictor
from AI.job_matching.company_matcher import CompanyMatcher


class TestJobMatchingEngine(unittest.TestCase):
    """Unit tests for Phase 8 AI Job Matching, Skill Gap, Salary, and Company Matcher."""

    def test_01_job_recommender(self):
        """Test job recommendations."""
        recommender = JobRecommender()
        jobs = recommender.recommend_jobs(["Python", "Flask"])
        self.assertGreater(len(jobs), 0)
        self.assertIn("company", jobs[0])

    def test_02_salary_predictor(self):
        """Test salary prediction calculation."""
        predictor = SalaryPredictor()
        sal = predictor.predict_salary_range(["Python", "AWS"], experience_years=3)
        self.assertGreater(sal["min_salary"], 80000)
        self.assertIn("USD", sal["formatted"])

    def test_03_skill_gap_and_company_matcher(self):
        """Test skill gap predictor and company culture matcher."""
        gap_pred = SkillGapPredictor()
        gap = gap_pred.predict_missing_skills(["Python", "Flask"])
        self.assertIn("missing_skills", gap)

        comp_matcher = CompanyMatcher()
        comps = comp_matcher.match_company_culture(["Python"])
        self.assertEqual(len(comps), 3)


if __name__ == "__main__":
    unittest.main()
