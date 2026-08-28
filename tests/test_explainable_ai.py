import unittest
from AI.explainable.score_explainer import ScoreExplainer
from AI.explainable.recommendation_explainer import RecommendationExplainer
from AI.explainable.hiring_explainer import HiringExplainer


class TestExplainableAI(unittest.TestCase):
    """Unit tests for Phase 9 Step 6: Explainable AI Engine."""

    def setUp(self):
        self.score_explainer = ScoreExplainer()
        self.rec_explainer = RecommendationExplainer()
        self.hiring_explainer = HiringExplainer()

    def test_01_career_match_score_explanation(self):
        """Test ScoreExplainer breaks down career match scores into positive/negative factors and actions."""
        skill_scores = {
            "Python": 95,
            "Machine Learning": 90,
            "SQL": 72,
            "Communication": 84,
            "AWS": 45
        }
        missing = ["Docker", "Kubernetes"]

        explanation = self.score_explainer.explain_career_match_score(
            score_value=87,
            target_role="AI Engineer",
            skill_scores=skill_scores,
            missing_skills=missing,
            interview_scores={"average_score": 82}
        )

        self.assertEqual(explanation["score_value"], 87)
        self.assertIn("why_generated", explanation)
        self.assertIn("sub_score_breakdown", explanation)
        self.assertIn("positive_factors", explanation)
        self.assertIn("negative_factors", explanation)
        self.assertIn("missing_skills", explanation)
        self.assertIn("improvement_actions", explanation)

        # Check positive factors contains strong skills
        pos_text = " ".join(explanation["positive_factors"])
        self.assertIn("Python", pos_text)

        # Check negative factors contains missing skills
        neg_text = " ".join(explanation["negative_factors"])
        self.assertIn("Docker", neg_text)

    def test_02_project_and_cert_recommendation_explanation(self):
        """Test RecommendationExplainer provides transparent reasons for learning recommendations."""
        proj_exp = self.rec_explainer.explain_project_recommendation(
            project_title="CNN Image Classifier",
            target_role="AI Engineer",
            target_skill="PyTorch",
            candidate_current_skills=["Python", "SQL"]
        )
        self.assertEqual(proj_exp["item_type"], "Project Recommendation")
        self.assertIn("PyTorch", proj_exp["why_recommended"])
        self.assertIn("expected_score_impact", proj_exp)

        cert_exp = self.rec_explainer.explain_certification_recommendation(
            cert_name="AWS Certified Machine Learning - Specialty",
            target_role="Machine Learning Engineer"
        )
        self.assertEqual(cert_exp["item_type"], "Certification Recommendation")
        self.assertIn("Machine Learning Engineer", cert_exp["why_recommended"])

    def test_03_hiring_decision_explainer(self):
        """Test HiringExplainer explains recruiter screening decision and readiness."""
        hiring_exp = self.hiring_explainer.explain_hiring_probability(
            probability_score=85,
            target_role="Senior Software Engineer",
            target_company="Google",
            strengths=["Distributed Systems", "Clean Architecture", "Algorithmic Speed"],
            blockers=["Limited Kubernetes production experience"]
        )

        self.assertEqual(hiring_exp["hiring_probability"], 85)
        self.assertIn("why_decision", hiring_exp)
        self.assertIn("Google", hiring_exp["why_decision"])
        self.assertIn("key_hiring_indicators", hiring_exp)
        self.assertGreater(len(hiring_exp["key_hiring_indicators"]), 0)


if __name__ == "__main__":
    unittest.main()
