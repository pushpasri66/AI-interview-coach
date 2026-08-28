from typing import Dict, Any, List, Set


class RolePredictor:
    """Predicts role fit and calculates readiness metrics across 9 industry technology roles."""

    ROLES_CATALOG = {
        "AI Engineer": {
            "required_skills": ["Python", "Machine Learning", "Deep Learning", "PyTorch", "TensorFlow", "NLP", "LLM", "APIs"],
            "recommended_projects": [
                "End-to-End LLM RAG Pipeline with Vector Search",
                "Autonomous Multi-Agent AI Task Coordinator",
                "Real-time Computer Vision Inference Microservice"
            ],
            "certifications": ["AWS Certified AI Practitioner", "TensorFlow Developer Certificate", "Google Cloud Professional ML Engineer"],
            "growth_level": "Exponential",
            "base_prep_weeks": 8
        },
        "Machine Learning Engineer": {
            "required_skills": ["Python", "Scikit-Learn", "Machine Learning", "Deep Learning", "SQL", "MLOps", "Docker", "Model Deployment"],
            "recommended_projects": [
                "Predictive Analytics Pipeline with Automated CI/CD Model Retraining",
                "Distributed Recommendation Engine using Feature Stores",
                "High-Throughput FastAPI Model Serving Engine"
            ],
            "certifications": ["AWS Certified Machine Learning - Specialty", "Databricks Certified ML Professional", "Azure AI Engineer Associate"],
            "growth_level": "Exponential",
            "base_prep_weeks": 10
        },
        "Data Scientist": {
            "required_skills": ["Python", "SQL", "Pandas", "NumPy", "Statistics", "Machine Learning", "Data Visualization", "Hypothesis Testing"],
            "recommended_projects": [
                "Customer Churn & Lifetime Value Probabilistic Modeling",
                "Exploratory Market Basket & Segment Analysis Dashboard",
                "A/B Testing Experimentation Framework"
            ],
            "certifications": ["IBM Data Science Professional Certificate", "Google Advanced Data Analytics", "Microsoft Certified: Azure Data Scientist Associate"],
            "growth_level": "Very High",
            "base_prep_weeks": 8
        },
        "Data Analyst": {
            "required_skills": ["SQL", "Excel", "PowerBI", "Tableau", "Python", "Data Cleaning", "Business Intelligence", "Reporting"],
            "recommended_projects": [
                "Executive KPI Business Intelligence Tableau Dashboard",
                "Automated SQL ETL Data Pipeline with Data Quality Validation",
                "Sales & Revenue Growth Cohort Analysis"
            ],
            "certifications": ["Google Data Analytics Certificate", "Microsoft Certified: Power BI Data Analyst", "Tableau Certified Data Analyst"],
            "growth_level": "High",
            "base_prep_weeks": 6
        },
        "Software Engineer": {
            "required_skills": ["Python", "Java", "C++", "Data Structures", "Algorithms", "SQL", "Git", "Object-Oriented Design", "System Design"],
            "recommended_projects": [
                "Distributed Key-Value Store with Concurrency Control",
                "High-Performance URL Shortener & Rate Limiting Engine",
                "Scalable Task Queue Worker System"
            ],
            "certifications": ["AWS Certified Developer - Associate", "Oracle Certified Professional: Java SE", "Meta Back-End Developer Certificate"],
            "growth_level": "High",
            "base_prep_weeks": 6
        },
        "Full Stack Developer": {
            "required_skills": ["JavaScript", "TypeScript", "React", "Node.js", "Python", "HTML/CSS", "REST APIs", "SQL", "MongoDB", "Git"],
            "recommended_projects": [
                "Full-Stack Collaborative Workspace with WebSockets",
                "E-Commerce Platform with Stripe Checkout & Admin Dashboard",
                "SaaS Multi-Tenant Authentication & Subscription System"
            ],
            "certifications": ["Meta Front-End & Back-End Professional Certificate", "AWS Certified Developer", "MongoDB Certified Developer"],
            "growth_level": "Very High",
            "base_prep_weeks": 7
        },
        "Cloud Engineer": {
            "required_skills": ["AWS", "Azure", "GCP", "Linux", "Terraform", "Cloud Architecture", "Docker", "Networking", "IAM", "Python"],
            "recommended_projects": [
                "Multi-Tier High Availability VPC Architecture with Terraform",
                "Serverless Event-Driven Data Ingestion Pipeline",
                "Zero-Trust Cloud Identity & Access Security Matrix"
            ],
            "certifications": ["AWS Certified Solutions Architect - Associate", "Google Cloud Professional Cloud Architect", "Microsoft Certified: Azure Solutions Architect Expert"],
            "growth_level": "Very High",
            "base_prep_weeks": 8
        },
        "DevOps Engineer": {
            "required_skills": ["Docker", "Kubernetes", "CI/CD", "Jenkins", "GitHub Actions", "Terraform", "Linux", "Prometheus", "Grafana", "Python"],
            "recommended_projects": [
                "Production Kubernetes Cluster with GitOps (ArgoCD)",
                "Automated Multi-Stage CI/CD Deployment Pipeline with Security Scanning",
                "Observability Stack with Prometheus, Grafana, and Alertmanager"
            ],
            "certifications": ["Certified Kubernetes Administrator (CKA)", "AWS Certified DevOps Engineer - Professional", "HashiCorp Certified: Terraform Associate"],
            "growth_level": "Very High",
            "base_prep_weeks": 9
        },
        "Cybersecurity Engineer": {
            "required_skills": ["Network Security", "Cryptography", "Penetration Testing", "Linux", "Python", "SIEM", "Vulnerability Assessment", "OWASP", "Firewalls"],
            "recommended_projects": [
                "Automated Vulnerability Scanning & Alerting Bot",
                "Enterprise Security Information and Event Management (SIEM) Lab",
                "Web Application Firewall (WAF) Rule Evaluator"
            ],
            "certifications": ["CompTIA Security+", "Certified Information Systems Security Professional (CISSP)", "Offensive Security Certified Professional (OSCP)"],
            "growth_level": "Exponential",
            "base_prep_weeks": 10
        }
    }

    def evaluate_role(self, role_name: str, candidate_skills: Set[str], candidate_scores: Dict[str, Any]) -> Dict[str, Any]:
        """Calculates detailed metrics for a single role given candidate skills and scores."""
        if role_name not in self.ROLES_CATALOG:
            raise ValueError(f"Role '{role_name}' is not in the catalog.")

        role_info = self.ROLES_CATALOG[role_name]
        required = role_info["required_skills"]

        matched = []
        missing = []

        norm_candidate = {s.lower().strip() for s in candidate_skills}

        for req in required:
            req_lower = req.lower()
            if any(req_lower in cs or cs in req_lower for cs in norm_candidate):
                matched.append(req)
            else:
                missing.append(req)

        skill_ratio = len(matched) / max(1, len(required))
        tech_score = candidate_scores.get("technical_strength", 75)
        interview_score = candidate_scores.get("interview_readiness", 75)

        # Match calculation
        match_pct = int(min(98, max(30, (skill_ratio * 60) + (tech_score * 0.25) + (interview_score * 0.15))))

        # Estimate preparation time
        missing_count = len(missing)
        base_weeks = role_info["base_prep_weeks"]
        if match_pct >= 85:
            prep_time = "2-4 Weeks (Interview Polish)"
        elif match_pct >= 70:
            prep_time = f"{max(3, int(missing_count * 1.5))} - {max(4, missing_count * 2)} Weeks"
        elif match_pct >= 50:
            prep_time = f"{max(2, int(missing_count * 0.8))} - {max(3, missing_count)} Months"
        else:
            prep_time = f"{base_weeks // 2} - {base_weeks} Months"

        return {
            "role": role_name,
            "match_percentage": match_pct,
            "existing_skills": matched,
            "missing_skills": missing,
            "recommended_projects": role_info["recommended_projects"],
            "certifications": role_info["certifications"],
            "preparation_time": prep_time,
            "career_growth_level": role_info["growth_level"]
        }
