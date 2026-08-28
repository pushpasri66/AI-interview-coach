from typing import Dict, Any, List
from AI.question_prediction.interview_probability import ProbabilityScorer


class JobDescriptionQuestionEngine:
    """Generates company-specific, system design, behavioral, and JD-targeted interview questions."""

    COMPANY_PATTERNS = {
        "google": {
            "focus": "Algorithmic scale, Clean Code, System scalability",
            "questions": [
                {
                    "question": "How would you design a distributed web crawler capable of handling billions of URLs per day with deduplication?",
                    "category": "System Design",
                    "difficulty": "Hard",
                    "reason": "Google heavily emphasizes large-scale distributed systems and data processing architecture.",
                    "focus_areas": ["Frontier queues", "Bloom filters for deduplication", "Politeness policies", "Fault tolerance"]
                },
                {
                    "question": "Tell me about a time you encountered a severe ambiguity in project requirements. How did you structure your engineering approach?",
                    "category": "Behavioral",
                    "difficulty": "Medium",
                    "reason": "Google assesses 'Googliness' and thriving under ambiguous technical constraints.",
                    "focus_areas": ["Stakeholder alignment", "Iterative prototypes", "Data-driven decisions"]
                }
            ]
        },
        "amazon": {
            "focus": "Leadership Principles (Customer Obsession, Ownership, Bias for Action)",
            "questions": [
                {
                    "question": "Give me an example of a time when you had to make a high-stakes technical tradeoff with incomplete data. (Bias for Action)",
                    "category": "Behavioral",
                    "difficulty": "Medium",
                    "reason": "Amazon behavioral rounds strictly evaluate the 16 Leadership Principles using STAR methodology.",
                    "focus_areas": ["STAR format", "Quantifiable impact", "Two-way vs one-way door decisions"]
                },
                {
                    "question": "Design a high-availability E-Commerce flash sale inventory reservation system preventing overselling.",
                    "category": "System Design",
                    "difficulty": "Hard",
                    "reason": "Amazon technical interviews frequently probe transactional e-commerce consistency and caching.",
                    "focus_areas": ["Redis distributed locking", "Pessimistic vs optimistic locking", "Eventual consistency"]
                }
            ]
        },
        "microsoft": {
            "focus": "Collaborative engineering, Enterprise cloud architecture, Code quality",
            "questions": [
                {
                    "question": "How would you design a collaborative real-time document editing service like Microsoft Office 365?",
                    "category": "System Design",
                    "difficulty": "Hard",
                    "reason": "Microsoft values real-time synchronization, operational transformation (OT/CRDT), and high reliability.",
                    "focus_areas": ["Operational transformation", "WebSockets", "Conflict resolution", "Data partition"]
                },
                {
                    "question": "Describe a situation where you had a strong technical disagreement with a team member. How was it resolved?",
                    "category": "Behavioral",
                    "difficulty": "Medium",
                    "reason": "Microsoft culture values growth mindset and constructive collaboration.",
                    "focus_areas": ["Empathy", "Objective benchmarking", "Consensus building"]
                }
            ]
        },
        "tcs": {
            "focus": "Software lifecycle, enterprise application delivery, core problem solving",
            "questions": [
                {
                    "question": "Explain how you manage technical debt and maintain continuous integration across enterprise client deliverables.",
                    "category": "Company-specific",
                    "difficulty": "Medium",
                    "reason": "TCS Digital/Innovator interviews probe enterprise delivery standards and SDLC maturity.",
                    "focus_areas": ["Agile ceremonies", "Automated regression testing", "Code reviews"]
                }
            ]
        }
    }

    def __init__(self):
        self.scorer = ProbabilityScorer()

    def generate_company_and_jd_questions(
        self,
        target_company: str,
        target_role: str,
        job_description: str = ""
    ) -> List[Dict[str, Any]]:
        """Generates Company-specific, System Design, Coding, Behavioral, and HR questions."""
        questions = []
        company_key = (target_company or "").lower().strip()

        # 1. Company Specific Patterns
        if company_key in self.COMPANY_PATTERNS:
            pattern = self.COMPANY_PATTERNS[company_key]
            for item in pattern["questions"]:
                prob = self.scorer.compute_probability(
                    category=item["category"],
                    is_company_core_theme=True,
                    role_importance="Critical"
                )
                questions.append({
                    "question": item["question"],
                    "probability_score": prob,
                    "difficulty": item["difficulty"],
                    "category": item["category"],
                    "reason": item["reason"],
                    "expected_focus_areas": item["focus_areas"]
                })
        elif target_company:
            prob = self.scorer.compute_probability(category="Company-specific", is_company_core_theme=True)
            questions.append({
                "question": f"Why do you specifically want to join {target_company}, and how does your engineering background fit our mission?",
                "probability_score": prob,
                "difficulty": "Easy",
                "category": "Company-specific",
                "reason": f"Standard company alignment inquiry for {target_company}.",
                "expected_focus_areas": ["Company product knowledge", "Cultural values", "Personal growth alignment"]
            })

        # 2. Universal HR & Cultural Fit
        hr_prob = self.scorer.compute_probability(category="HR", role_importance="High")
        questions.append({
            "question": "Walk me through your professional journey and highlight what motivates you as a software engineer.",
            "probability_score": hr_prob,
            "difficulty": "Easy",
            "category": "HR",
            "reason": "Universal introductory question in 95%+ of recruitment screening rounds.",
            "expected_focus_areas": ["Chronological summary", "Passion for building", "Why target role"]
        })

        # 3. Core Coding Challenge
        coding_prob = self.scorer.compute_probability(category="Coding", role_importance="Critical")
        questions.append({
            "question": "Given an array of integers, find the maximum subarray sum in O(N) time and O(1) space (Kadane's Algorithm).",
            "probability_score": coding_prob,
            "difficulty": "Medium",
            "category": "Coding",
            "reason": "Foundational coding challenge frequently asked to evaluate optimal algorithmic complexity.",
            "expected_focus_areas": ["Time complexity O(N)", "Space complexity O(1)", "Handling negative inputs"]
        })

        # 4. Role-tailored System Design Question if not already added
        has_sys_design = any(q["category"] == "System Design" for q in questions)
        if not has_sys_design:
            sd_prob = self.scorer.compute_probability(category="System Design", role_importance="High")
            questions.append({
                "question": f"How would you architect a scalable, fault-tolerant notification microservice for a {target_role} platform?",
                "probability_score": sd_prob,
                "difficulty": "Hard",
                "category": "System Design",
                "reason": f"System architecture question standard for {target_role} positions.",
                "expected_focus_areas": ["Message queues (Kafka/RabbitMQ)", "Rate limiting", "Push notification providers", "Retries"]
            })

        return questions
