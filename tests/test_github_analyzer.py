import unittest
import jwt
import datetime
from app import create_app
from backend.database import db
from backend.models.user import User
from backend.models.github_profile import GitHubAnalysis

from AI.github.project_quality import ProjectQualityEvaluator
from AI.github.contribution_analyzer import ContributionAnalyzer
from AI.github.repository_analyzer import RepositoryAnalyzer
from AI.github.github_analyzer import GitHubAIAnalyzer


class TestGitHubAnalyzer(unittest.TestCase):
    """Unit tests for Phase 9 Step 4: GitHub AI Profile Analyzer."""

    @classmethod
    def setUpClass(cls):
        cls.app = create_app("testing")
        cls.app.config["TESTING"] = True
        cls.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        cls.app.config["SECRET_KEY"] = "github-secret-key-778899"
        cls.app.config["WTF_CSRF_ENABLED"] = False
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.drop_all()

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.session.rollback()
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

        self.user = User(
            fullname="Taylor Smith",
            email=f"taylor_{datetime.datetime.utcnow().timestamp()}@example.com"
        )
        self.user.set_password("GitHubPass2026!")
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()
        self.app_context.pop()

    def generate_token(self, user_id: int) -> str:
        payload = {
            "user_id": user_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            "iat": datetime.datetime.utcnow()
        }
        return jwt.encode(payload, self.app.config["SECRET_KEY"], algorithm="HS256")

    # --- 1. Project Quality Evaluator Tests ---
    def test_01_project_quality_evaluator(self):
        """Test ProjectQualityEvaluator README structure analysis and repo complexity scoring."""
        evaluator = ProjectQualityEvaluator()
        
        sample_readme = """
        # Scalable Microservices Platform
        [![Build Passing](https://shields.io/badge/build-passing)]
        ## Installation
        ```bash
        pip install -r requirements.txt
        ```
        ## Usage
        Run the application with `python app.py`.
        ## Architecture
        Microservice architecture connecting FastAPI, Redis, and PostgreSQL.
        """
        readme_res = evaluator.evaluate_readme(sample_readme)
        self.assertGreaterEqual(readme_res["score"], 80)
        self.assertTrue(readme_res["has_title"])
        self.assertTrue(readme_res["has_installation"])
        self.assertTrue(readme_res["has_usage"])
        self.assertTrue(readme_res["has_badges"])
        self.assertTrue(readme_res["has_architecture"])

        repo_info = {"size": 2500, "stargazers_count": 12, "forks_count": 3, "description": "Backend engine", "language": "Python"}
        complexity = evaluator.evaluate_repository_complexity(repo_info)
        self.assertGreaterEqual(complexity, 70)

    # --- 2. Contribution Analyzer Tests ---
    def test_02_contribution_analyzer(self):
        """Test ContributionAnalyzer activity score and open-source contribution metrics."""
        analyzer = ContributionAnalyzer()
        res = analyzer.evaluate_activity_and_contributions(
            public_repos_count=10,
            total_stars=25,
            total_forks=8,
            recent_updates_count=4
        )

        self.assertIn("coding_activity_score", res)
        self.assertGreaterEqual(res["coding_activity_score"], 70)
        self.assertIn("commit_activity_level", res)
        self.assertIn("opensource_contribution_score", res)
        self.assertGreaterEqual(res["opensource_contribution_score"], 60)

    # --- 3. Repository Analyzer Tests ---
    def test_03_repository_analyzer(self):
        """Test RepositoryAnalyzer language breakdown, project diversity, and repo ranking."""
        analyzer = RepositoryAnalyzer()
        repos = [
            {"name": "ai-model-runner", "language": "Python", "stargazers_count": 10, "forks_count": 2, "size": 3000, "description": "AI ML model inference API"},
            {"name": "react-web-portal", "language": "TypeScript", "stargazers_count": 5, "forks_count": 1, "size": 1500, "description": "React frontend web app"},
            {"name": "k8s-infra", "language": "HCL", "stargazers_count": 2, "forks_count": 0, "size": 600, "description": "Kubernetes and terraform cloud scripts"}
        ]

        analysis = analyzer.analyze_repositories(repos)
        self.assertIn("language_distribution", analysis)
        self.assertIn("Python", analysis["language_distribution"])
        self.assertIn("TypeScript", analysis["language_distribution"])
        self.assertGreaterEqual(analysis["project_diversity_score"], 60)
        self.assertEqual(len(analysis["top_repositories"]), 3)

    # --- 4. Master GitHubAIAnalyzer Tests ---
    def test_04_master_github_analyzer_metrics_and_persistence(self):
        """Test GitHubAIAnalyzer calculates all 10 metrics, generates insights, and persists to DB."""
        analyzer = GitHubAIAnalyzer()
        result = analyzer.analyze_profile(username="octocat", user_id=self.user.id, persist=True)

        self.assertEqual(result["github_username"], "octocat")
        self.assertIn("scores", result)
        scores = result["scores"]

        # Verify all 10 core metrics
        self.assertIn("overall_score", scores)
        self.assertIn("coding_activity_score", scores)
        self.assertIn("repository_quality_score", scores)
        self.assertIn("project_complexity_score", scores)
        self.assertIn("readme_quality_score", scores)
        self.assertIn("documentation_quality_score", scores)
        self.assertIn("project_diversity_score", scores)
        self.assertIn("opensource_contribution_score", scores)
        self.assertIn("language_distribution", result)
        self.assertIn("commit_activity", result)

        # Verify qualitative sections
        self.assertIsInstance(result["strengths"], list)
        self.assertIsInstance(result["weaknesses"], list)
        self.assertIsInstance(result["recommended_improvements"], list)
        self.assertIsInstance(result["skills_demonstrated"], list)
        self.assertIn("career_relevance", result)
        self.assertIn("role_fit_scores", result["career_relevance"])

        # Check DB record
        db_record = GitHubAnalysis.query.filter_by(github_username="octocat").first()
        self.assertIsNotNone(db_record)
        self.assertEqual(db_record.overall_score, scores["overall_score"])
        self.assertGreater(len(db_record.get_languages()), 0)

    # --- 5. API Endpoints ---
    def test_05_api_github_analyze_missing_param(self):
        """Test GET /api/github/analyze without username returns 400."""
        response = self.client.get("/api/github/analyze")
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data["success"])
        self.assertIn("Missing required 'username' parameter", data["error"])

    def test_06_api_github_analyze_success(self):
        """Test GET /api/github/analyze with query parameter returns 200 structured analysis."""
        token = self.generate_token(self.user.id)
        response = self.client.get(
            "/api/github/analyze?username=octocat",
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertIn("github_analysis", data)
        self.assertIn("scores", data["github_analysis"])
        self.assertIn("language_distribution", data["github_analysis"])
        self.assertIn("career_relevance", data["github_analysis"])


if __name__ == "__main__":
    unittest.main()
