from typing import Dict, Any, List, Optional
from backend.database import db
from backend.models.future_skill import FutureSkillDemand


class SkillDemandPredictor:
    """Predicts 1-year, 2-year, and 3-year industry skill demand trajectories and learning priorities."""

    DEFAULT_SKILL_FORECASTS = [
        # AI & Machine Learning
        {
            "skill_name": "RAG & Vector Databases",
            "category": "AI & Machine Learning",
            "current_demand": 82,
            "demand_1yr": 92,
            "demand_2yr": 96,
            "demand_3yr": 98,
            "growth_percentage": 19.5,
            "importance": "Critical",
            "learning_priority": "Immediate",
            "market_drivers": "Enterprise LLM adoption; proprietary data integration; semantic search dominance"
        },
        {
            "skill_name": "Autonomous Agentic Frameworks",
            "category": "AI & Machine Learning",
            "current_demand": 74,
            "demand_1yr": 88,
            "demand_2yr": 95,
            "demand_3yr": 99,
            "growth_percentage": 33.8,
            "importance": "Critical",
            "learning_priority": "Immediate",
            "market_drivers": "Automated developer tooling; agentic workflows; multi-step task resolution"
        },
        {
            "skill_name": "MLOps & LLMOps",
            "category": "AI & Machine Learning",
            "current_demand": 78,
            "demand_1yr": 86,
            "demand_2yr": 93,
            "demand_3yr": 97,
            "growth_percentage": 24.4,
            "importance": "Critical",
            "learning_priority": "Immediate",
            "market_drivers": "Production model drift monitoring; fine-tuning orchestration; GPU cost optimization"
        },
        {
            "skill_name": "PyTorch & Deep Learning",
            "category": "AI & Machine Learning",
            "current_demand": 85,
            "demand_1yr": 89,
            "demand_2yr": 94,
            "demand_3yr": 96,
            "growth_percentage": 12.9,
            "importance": "High",
            "learning_priority": "Immediate",
            "market_drivers": "Foundation model customization; research-to-production transfer"
        },
        # Cloud & DevOps
        {
            "skill_name": "Kubernetes & Cloud Orchestration",
            "category": "Cloud & DevOps",
            "current_demand": 88,
            "demand_1yr": 91,
            "demand_2yr": 94,
            "demand_3yr": 96,
            "growth_percentage": 9.1,
            "importance": "Critical",
            "learning_priority": "Immediate",
            "market_drivers": "Microservices standard; hybrid multi-cloud elasticity; containerized workloads"
        },
        {
            "skill_name": "Infrastructure as Code (Terraform)",
            "category": "Cloud & DevOps",
            "current_demand": 82,
            "demand_1yr": 87,
            "demand_2yr": 92,
            "demand_3yr": 95,
            "growth_percentage": 15.8,
            "importance": "High",
            "learning_priority": "Medium-term",
            "market_drivers": "Cloud compliance automation; multi-region provisioning reproducibility"
        },
        {
            "skill_name": "eBPF & Observability",
            "category": "Cloud & DevOps",
            "current_demand": 65,
            "demand_1yr": 76,
            "demand_2yr": 86,
            "demand_3yr": 92,
            "growth_percentage": 41.5,
            "importance": "High",
            "learning_priority": "Medium-term",
            "market_drivers": "Kernel-level security; zero-overhead tracing; modern network routing"
        },
        # Software Engineering & Backend
        {
            "skill_name": "Python",
            "category": "Software Engineering",
            "current_demand": 92,
            "demand_1yr": 94,
            "demand_2yr": 96,
            "demand_3yr": 98,
            "growth_percentage": 6.5,
            "importance": "Critical",
            "learning_priority": "Immediate",
            "market_drivers": "Universal language for AI/ML, backend APIs, data engineering, and automation"
        },
        {
            "skill_name": "Rust for High Performance",
            "category": "Software Engineering",
            "current_demand": 70,
            "demand_1yr": 80,
            "demand_2yr": 89,
            "demand_3yr": 95,
            "growth_percentage": 35.7,
            "importance": "High",
            "learning_priority": "Medium-term",
            "market_drivers": "Memory safety without garbage collection; AI inference runtimes; WebAssembly"
        },
        {
            "skill_name": "FastAPI & Async Microservices",
            "category": "Software Engineering",
            "current_demand": 80,
            "demand_1yr": 86,
            "demand_2yr": 91,
            "demand_3yr": 94,
            "growth_percentage": 17.5,
            "importance": "High",
            "learning_priority": "Immediate",
            "market_drivers": "High-throughput asynchronous IO; seamless OpenAPI specs for AI endpoints"
        },
        # Cybersecurity
        {
            "skill_name": "AI Application Security & OWASP LLM",
            "category": "Cybersecurity",
            "current_demand": 68,
            "demand_1yr": 82,
            "demand_2yr": 91,
            "demand_3yr": 97,
            "growth_percentage": 42.6,
            "importance": "Critical",
            "learning_priority": "Immediate",
            "market_drivers": "Prompt injection defenses; automated agent sandboxing; enterprise compliance"
        },
        {
            "skill_name": "Zero-Trust Architecture",
            "category": "Cybersecurity",
            "current_demand": 79,
            "demand_1yr": 85,
            "demand_2yr": 91,
            "demand_3yr": 95,
            "growth_percentage": 20.2,
            "importance": "High",
            "learning_priority": "Medium-term",
            "market_drivers": "Identity-first security boundaries; distributed cloud-native perimeter defense"
        }
    ]

    def seed_and_sync_database(self) -> None:
        """Ensures all future skill forecasts exist in the database."""
        for item in self.DEFAULT_SKILL_FORECASTS:
            existing = FutureSkillDemand.query.filter_by(skill_name=item["skill_name"]).first()
            if not existing:
                record = FutureSkillDemand(
                    skill_name=item["skill_name"],
                    category=item["category"],
                    current_demand=item["current_demand"],
                    demand_1yr=item["demand_1yr"],
                    demand_2yr=item["demand_2yr"],
                    demand_3yr=item["demand_3yr"],
                    growth_percentage=item["growth_percentage"],
                    importance=item["importance"],
                    learning_priority=item["learning_priority"],
                    market_drivers=item["market_drivers"]
                )
                db.session.add(record)
        db.session.commit()

    def get_forecasts_for_category(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieves formatted skill demand forecasts filtered optionally by category."""
        self.seed_and_sync_database()

        query = FutureSkillDemand.query
        if category:
            query = query.filter(FutureSkillDemand.category.ilike(f"%{category}%"))

        records = query.order_by(FutureSkillDemand.growth_percentage.desc()).all()
        return [r.to_dict() for r in records]

    def predict_future_skills_for_candidate(self, candidate_skills: List[str], target_role: str = "Software Engineer") -> Dict[str, Any]:
        """Maps candidate current skills to future skill trajectories and highlights missing high-growth skills."""
        self.seed_and_sync_database()
        all_forecasts = self.get_forecasts_for_category()

        norm_candidate = {s.lower().strip() for s in candidate_skills}

        candidate_future_strengths = []
        high_priority_recommendations = []

        for f in all_forecasts:
            s_name = f["skill_name"]
            is_owned = any(s_name.lower() in cs or cs in s_name.lower() for cs in norm_candidate)
            
            item_data = {
                "skill_name": s_name,
                "category": f["category"],
                "current_demand": f["current_demand"],
                "demand_1yr": f["demand_forecast"]["1_year"],
                "demand_2yr": f["demand_forecast"]["2_year"],
                "demand_3yr": f["demand_forecast"]["3_year"],
                "growth_percentage": f["growth_percentage"],
                "importance": f["importance"],
                "learning_priority": f["learning_priority"]
            }

            if is_owned:
                candidate_future_strengths.append(item_data)
            else:
                high_priority_recommendations.append(item_data)

        # Sort recommendations by growth percentage
        high_priority_recommendations.sort(key=lambda x: x["growth_percentage"], reverse=True)

        return {
            "target_role": target_role,
            "forecast_horizons": ["1 Year", "2 Years", "3 Years"],
            "total_forecasted_skills": len(all_forecasts),
            "candidate_future_ready_skills": candidate_future_strengths,
            "recommended_future_skills": high_priority_recommendations,
            "all_forecasts": all_forecasts
        }
