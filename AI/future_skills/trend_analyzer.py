from typing import Dict, Any, List


class TrendAnalyzer:
    """Analyzes market trends, technology obsolescence risk, and emerging industry paradigms."""

    MACRO_TRENDS = [
        {
            "trend_name": "Autonomous Agentic AI Integration",
            "impact_scope": "Global / Universal",
            "velocity": "Accelerating (+120% YoY)",
            "impact_summary": "Shift from static chatbots to autonomous multi-agent systems that plan, invoke tools, and code.",
            "core_driver_skills": ["LangChain/LangGraph", "Vector Databases", "Prompt Engineering", "API Tool Calling"]
        },
        {
            "trend_name": "Cloud-Native Platform Engineering",
            "impact_scope": "Enterprise Systems",
            "velocity": "High Growth (+85% YoY)",
            "impact_summary": "Consolidation of developer experience into internal developer platforms over raw cloud configs.",
            "core_driver_skills": ["Kubernetes", "Backstage", "Terraform", "eBPF"]
        },
        {
            "trend_name": "AI-Driven Cybersecurity & Zero-Trust",
            "impact_scope": "Critical Infrastructure",
            "velocity": "High Growth (+95% YoY)",
            "impact_summary": "Defending against AI-generated exploits and automated security perimeter verification.",
            "core_driver_skills": ["AI Threat Modeling", "Zero-Trust IAM", "OWASP LLM Security", "SIEM"]
        }
    ]

    def analyze_profile_trends(self, skills: List[str]) -> Dict[str, Any]:
        """Evaluates how candidate skills align with current macro tech trends."""
        norm_skills = {s.lower().strip() for s in skills}
        
        aligned_trends = []
        for trend in self.MACRO_TRENDS:
            drivers = trend["core_driver_skills"]
            matches = [d for d in drivers if any(d.lower() in s or s in d.lower() for s in norm_skills)]
            alignment_score = int((len(matches) / max(1, len(drivers))) * 100)

            aligned_trends.append({
                "trend_name": trend["trend_name"],
                "velocity": trend["velocity"],
                "alignment_score": alignment_score,
                "matched_skills": matches,
                "missing_driver_skills": [d for d in drivers if d not in matches],
                "impact_summary": trend["impact_summary"]
            })

        overall_future_alignment = int(sum(t["alignment_score"] for t in aligned_trends) / len(aligned_trends)) if aligned_trends else 50

        return {
            "overall_future_alignment_index": overall_future_alignment,
            "alignment_status": "Highly Future-Proof" if overall_future_alignment >= 70 else ("Moderately Aligned" if overall_future_alignment >= 40 else "Needs Modernization"),
            "trends": aligned_trends
        }
