import unittest
from AI.mentor.mentor_engine import MentorEngine
from AI.mentor.career_planner import CareerPlanner
from AI.mentor.learning_advisor import LearningAdvisor
from AI.mentor.growth_tracker import GrowthTracker


class TestMentorSystem(unittest.TestCase):
    """Unit tests for Phase 8 AI Career Mentor System."""

    def test_01_mentor_engine(self):
        """Test mentor engine advisory generation."""
        engine = MentorEngine()
        res = engine.advise_candidate("Alice", "AI Engineer")
        self.assertIn("Alice", res["advice"])
        self.assertEqual(res["status"], "success")

    def test_02_career_planner(self):
        """Test 6 & 12 month career planning."""
        planner = CareerPlanner()
        plan6 = planner.generate_career_plan("AI Engineer", 6)
        self.assertEqual(len(plan6["timeline"]), 3)

        plan12 = planner.generate_career_plan("AI Engineer", 12)
        self.assertEqual(len(plan12["timeline"]), 5)

    def test_03_learning_advisor_and_growth_tracker(self):
        """Test learning resources advisor and growth tracker."""
        advisor = LearningAdvisor()
        res = advisor.recommend_learning_resources("AI Engineer")
        self.assertIn("courses", res)

        tracker = GrowthTracker()
        growth = tracker.calculate_growth_trend([70, 75, 88])
        self.assertGreater(growth["growth_percentage"], 0)


if __name__ == "__main__":
    unittest.main()
