from typing import Dict, Any, List


class FutureRolePredictor:
    """Predicts next-generation emerging roles and industry transformation trends."""

    EMERGING_ROLES = [
        {
            "role_title": "Agentic AI Systems Architect",
            "evolution_from": ["AI Engineer", "Software Engineer"],
            "horizon_years": 1,
            "demand_growth": "+140%",
            "key_technologies": ["Multi-Agent Frameworks", "LangChain/LangGraph", "Vector Databases", "Function Calling"],
            "summary": "Designs autonomous, multi-agent workflows and real-time LLM tool execution pipelines."
        },
        {
            "role_title": "MLOps & AI Infrastructure Engineer",
            "evolution_from": ["DevOps Engineer", "Machine Learning Engineer"],
            "horizon_years": 2,
            "demand_growth": "+95%",
            "key_technologies": ["Kubeflow", "MLflow", "Triton Inference Server", "Ray", "vLLM"],
            "summary": "Operates high-performance GPU clusters, model quantization, and distributed AI deployments."
        },
        {
            "role_title": "AI Security & Alignment Specialist",
            "evolution_from": ["Cybersecurity Engineer", "AI Engineer"],
            "horizon_years": 2,
            "demand_growth": "+120%",
            "key_technologies": ["Prompt Injection Defense", "Model Red Teaming", "Differential Privacy", "OWASP LLM Top 10"],
            "summary": "Guards AI models and inference pipelines against adversarial attacks, jailbreaks, and compliance breaches."
        },
        {
            "role_title": "Cloud-Native Platform Engineer",
            "evolution_from": ["Cloud Engineer", "DevOps Engineer"],
            "horizon_years": 3,
            "demand_growth": "+80%",
            "key_technologies": ["Internal Developer Platforms (IDP)", "Backstage", "Crossplane", "eBPF", "Terraform"],
            "summary": "Builds frictionless self-service developer infrastructure platforms in hybrid multi-cloud environments."
        }
    ]

    def predict_emerging_roles(self, current_skills: List[str], current_role: str = "Software Engineer") -> List[Dict[str, Any]]:
        """Matches candidate profile against upcoming 1-3 year high-growth emerging roles."""
        norm_skills = {s.lower().strip() for s in current_skills}
        results = []

        for er in self.EMERGING_ROLES:
            techs = er["key_technologies"]
            matched_techs = [t for t in techs if any(t.lower() in s or s in t.lower() for s in norm_skills)]
            relevance = 60 + (len(matched_techs) * 10)
            if current_role in er["evolution_from"]:
                relevance += 15

            results.append({
                "role_title": er["role_title"],
                "evolution_from": er["evolution_from"],
                "horizon": f"{er['horizon_years']} Year Outlook",
                "demand_growth": er["demand_growth"],
                "relevance_score": min(98, relevance),
                "key_technologies": er["key_technologies"],
                "summary": er["summary"]
            })

        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results
