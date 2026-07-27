import unittest
from AI.code_review.code_analyzer import CodeAnalyzer
from AI.code_review.complexity_checker import ComplexityChecker
from AI.code_review.optimization_engine import OptimizationEngine
from AI.code_review.debugging_assistant import DebuggingAssistant


class TestCodingAIPlatform2(unittest.TestCase):
    """Unit tests for Phase 8 AI Coding Interview Platform 2.0."""

    def test_01_code_analyzer_and_complexity(self):
        """Test multi-language code quality analysis and Big-O complexity checker."""
        analyzer = CodeAnalyzer()
        res = analyzer.analyze_code_quality("def two_sum(nums, target):\n    for i in nums:\n        for j in nums:\n            pass")
        self.assertGreater(res["quality_score"], 50)

        comp = ComplexityChecker()
        c_res = comp.analyze_complexity("for i in range(n):\n    for j in range(n):\n        print(i)")
        self.assertEqual(c_res["time_complexity"], "O(N^2)")

    def test_02_optimization_and_debugging(self):
        """Test optimization engine and AI debugging assistant."""
        opt = OptimizationEngine()
        opt_res = opt.suggest_optimization("def foo(): pass", "python")
        self.assertIn("def solution", opt_res["optimized_code"])

        dbg = DebuggingAssistant()
        diag = dbg.diagnose_error("code", "IndentationError: unexpected indent")
        self.assertIn("IndentationError", diag["error_diagnosis"])


if __name__ == "__main__":
    unittest.main()
