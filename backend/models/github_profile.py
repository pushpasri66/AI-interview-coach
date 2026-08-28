import json
from datetime import datetime
from backend.database import db


class GitHubAnalysis(db.Model):
    """Database model storing candidate GitHub profile analysis, scores, and repository metrics."""

    __tablename__ = "github_analyses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    github_username = db.Column(db.String(100), nullable=False, index=True)
    
    # Quantitative Scores (0-100)
    overall_score = db.Column(db.Integer, default=0, nullable=False)
    coding_activity_score = db.Column(db.Integer, default=0, nullable=False)
    repository_quality_score = db.Column(db.Integer, default=0, nullable=False)
    project_complexity_score = db.Column(db.Integer, default=0, nullable=False)
    readme_quality_score = db.Column(db.Integer, default=0, nullable=False)
    documentation_quality_score = db.Column(db.Integer, default=0, nullable=False)
    project_diversity_score = db.Column(db.Integer, default=0, nullable=False)
    opensource_contribution_score = db.Column(db.Integer, default=0, nullable=False)
    
    total_public_repos = db.Column(db.Integer, default=0, nullable=False)
    total_stars = db.Column(db.Integer, default=0, nullable=False)
    total_forks = db.Column(db.Integer, default=0, nullable=False)
    
    # JSON structured payloads
    language_distribution_json = db.Column(db.Text, nullable=True)
    top_repositories_json = db.Column(db.Text, nullable=True)
    strengths_json = db.Column(db.Text, nullable=True)
    weaknesses_json = db.Column(db.Text, nullable=True)
    recommendations_json = db.Column(db.Text, nullable=True)
    skills_demonstrated_json = db.Column(db.Text, nullable=True)
    career_relevance_json = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def get_languages(self) -> dict:
        return json.loads(self.language_distribution_json) if self.language_distribution_json else {}

    def set_languages(self, data: dict) -> None:
        self.language_distribution_json = json.dumps(data)

    def get_top_repositories(self) -> list:
        return json.loads(self.top_repositories_json) if self.top_repositories_json else []

    def set_top_repositories(self, data: list) -> None:
        self.top_repositories_json = json.dumps(data)

    def get_strengths(self) -> list:
        return json.loads(self.strengths_json) if self.strengths_json else []

    def set_strengths(self, data: list) -> None:
        self.strengths_json = json.dumps(data)

    def get_weaknesses(self) -> list:
        return json.loads(self.weaknesses_json) if self.weaknesses_json else []

    def set_weaknesses(self, data: list) -> None:
        self.weaknesses_json = json.dumps(data)

    def get_recommendations(self) -> list:
        return json.loads(self.recommendations_json) if self.recommendations_json else []

    def set_recommendations(self, data: list) -> None:
        self.recommendations_json = json.dumps(data)

    def get_skills_demonstrated(self) -> list:
        return json.loads(self.skills_demonstrated_json) if self.skills_demonstrated_json else []

    def set_skills_demonstrated(self, data: list) -> None:
        self.skills_demonstrated_json = json.dumps(data)

    def get_career_relevance(self) -> dict:
        return json.loads(self.career_relevance_json) if self.career_relevance_json else {}

    def set_career_relevance(self, data: dict) -> None:
        self.career_relevance_json = json.dumps(data)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "github_username": self.github_username,
            "metrics": {
                "overall_score": self.overall_score,
                "coding_activity_score": self.coding_activity_score,
                "repository_quality_score": self.repository_quality_score,
                "project_complexity_score": self.project_complexity_score,
                "readme_quality_score": self.readme_quality_score,
                "documentation_quality_score": self.documentation_quality_score,
                "project_diversity_score": self.project_diversity_score,
                "opensource_contribution_score": self.opensource_contribution_score
            },
            "public_stats": {
                "total_public_repos": self.total_public_repos,
                "total_stars": self.total_stars,
                "total_forks": self.total_forks
            },
            "language_distribution": self.get_languages(),
            "top_repositories": self.get_top_repositories(),
            "strengths": self.get_strengths(),
            "weaknesses": self.get_weaknesses(),
            "recommendations": self.get_recommendations(),
            "skills_demonstrated": self.get_skills_demonstrated(),
            "career_relevance": self.get_career_relevance(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self) -> str:
        return f"<GitHubAnalysis id={self.id} username='{self.github_username}' score={self.overall_score}>"
