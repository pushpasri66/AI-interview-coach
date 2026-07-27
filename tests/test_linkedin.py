import unittest
from AI.linkedin.linkedin_analyzer import LinkedInAnalyzer
from AI.linkedin.profile_optimizer import ProfileOptimizer
from AI.linkedin.networking_advisor import NetworkingAdvisor


class TestLinkedInAnalyzer(unittest.TestCase):
    """Unit tests for Phase 8 AI LinkedIn Profile Analyzer."""

    def test_01_profile_analyzer(self):
        """Test LinkedIn profile text analysis."""
        analyzer = LinkedInAnalyzer()
        res = analyzer.analyze_profile_text("Experienced Python AI Software Engineer specializing in Flask and PyTorch.")
        self.assertGreater(res["overall_score"], 50)

    def test_02_optimizer_and_networking_advisor(self):
        """Test optimization suggestions and networking strategies."""
        opt = ProfileOptimizer()
        suggs = opt.generate_optimizations("AI Engineer")
        self.assertIn("headline_suggestion", suggs)

        net = NetworkingAdvisor()
        net_res = net.recommend_networking_strategies("Google")
        self.assertEqual(net_res["target_company"], "Google")


if __name__ == "__main__":
    unittest.main()
