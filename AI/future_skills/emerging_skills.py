from typing import Dict, Any, List


class EmergingSkillsEngine:
    """Identifies high-growth emerging technology clusters and provides fast-track learning blueprints."""

    BREAKTHROUGH_SKILLS = [
        {
            "cluster": "Generative AI & Agentic Systems",
            "skills": ["LangGraph", "LlamaIndex", "vLLM", "DSPy", "ChromaDB/Pinecone"],
            "growth_rate": "+180%",
            "learning_difficulty": "Medium",
            "time_to_master": "3-4 Weeks",
            "best_first_project": "Build an Autonomous Documentation Research Agent with Vector Memory"
        },
        {
            "cluster": "Modern Systems & Runtimes",
            "skills": ["Rust", "WebAssembly (Wasm)", "eBPF", "Zig"],
            "growth_rate": "+90%",
            "learning_difficulty": "Hard",
            "time_to_master": "6-8 Weeks",
            "best_first_project": "Build a High-Speed In-Memory Cache in Rust with Wasm Plugins"
        },
        {
            "cluster": "Cloud Native & Platform Engineering",
            "skills": ["ArgoCD", "Crossplane", "OpenTelemetry", "Cilium"],
            "growth_rate": "+85%",
            "learning_difficulty": "Medium-Hard",
            "time_to_master": "4-6 Weeks",
            "best_first_project": "Deploy a GitOps Managed Multi-Service Kubernetes Platform with Distributed Tracing"
        }
    ]

    def get_emerging_skills_catalog(self) -> List[Dict[str, Any]]:
        """Returns the full catalog of high-velocity emerging skills clusters."""
        return self.BREAKTHROUGH_SKILLS

    def recommend_for_candidate(self, candidate_skills: List[str]) -> List[Dict[str, Any]]:
        """Recommends specific emerging skill clusters tailored to candidate baseline."""
        norm = {s.lower().strip() for s in candidate_skills}
        recommendations = []

        for cluster in self.BREAKTHROUGH_SKILLS:
            existing = [s for s in cluster["skills"] if any(s.lower() in cs or cs in s.lower() for cs in norm)]
            missing = [s for s in cluster["skills"] if s not in existing]

            recommendations.append({
                "cluster": cluster["cluster"],
                "growth_rate": cluster["growth_rate"],
                "learning_difficulty": cluster["learning_difficulty"],
                "time_to_master": cluster["time_to_master"],
                "skills_to_learn": missing,
                "already_acquired": existing,
                "recommended_project": cluster["best_first_project"]
            })

        return recommendations
