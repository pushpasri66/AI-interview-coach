import random


class QuestionGenerator:
    """AI engine generating tailored interview questions and expected answers."""

    HR_QUESTION_BANK = [
        {
            "question_text": "Tell me about yourself and summarize your professional background.",
            "category": "Introduction",
            "expected_answer": "Candidate should summarize career trajectory, key technical strengths, relevant achievements, and enthusiasm for the position using concise storytelling."
        },
        {
            "question_text": "What are your greatest professional strengths and your biggest weakness?",
            "category": "Self-Assessment",
            "expected_answer": "Candidate should state 2-3 genuine strengths with examples and a real weakness along with actionable steps taken to overcome it."
        },
        {
            "question_text": "Describe a situation where you demonstrated leadership or took initiative in a team project.",
            "category": "Leadership",
            "expected_answer": "Candidate should use the STAR method (Situation, Task, Action, Result) showcasing proactive problem-solving and team collaboration."
        },
        {
            "question_text": "How do you handle workplace conflicts or disagreements on technical decisions?",
            "category": "Teamwork",
            "expected_answer": "Candidate should emphasize active listening, data-driven discussions, mutual respect, and focusing on project goals."
        },
        {
            "question_text": "Where do you see yourself professionally in 3 to 5 years?",
            "category": "Career Goals",
            "expected_answer": "Candidate should express commitment to skill progression, technical leadership, mastering emerging technologies, and contributing value to the organization."
        }
    ]

    TECHNICAL_QUESTION_BANK = {
        "python": [
            {
                "question_text": "Explain the difference between deep copy and shallow copy in Python, and how decorators work.",
                "category": "Python",
                "expected_answer": "Shallow copy constructs a new object and populates it with references to child objects. Deep copy recursively copies all nested objects. Decorators wrap functions to extend functionality dynamically using higher-order functions."
            },
            {
                "question_text": "How does memory management and garbage collection work in Python?",
                "category": "Python",
                "expected_answer": "Python uses reference counting as its primary mechanism alongside a generational garbage collector to detect and resolve reference cycles."
            }
        ],
        "java": [
            {
                "question_text": "Explain the principles of OOPs in Java and the difference between Method Overloading and Method Overriding.",
                "category": "Java",
                "expected_answer": "OOPs principles: Encapsulation, Inheritance, Polymorphism, Abstraction. Overloading is compile-time polymorphism in the same class. Overriding is runtime polymorphism in a child subclass."
            }
        ],
        "ai_ml": [
            {
                "question_text": "Explain the difference between Supervised, Unsupervised, and Reinforcement Learning, and how Random Forest works.",
                "category": "AI/ML",
                "expected_answer": "Supervised uses labeled data, Unsupervised finds unlabeled patterns, Reinforcement learns via rewards/penalties. Random Forest builds an ensemble of decision trees using bagging and majority voting."
            },
            {
                "question_text": "What is the Bias-Variance tradeoff, and how do you prevent overfitting in deep neural networks?",
                "category": "AI/ML",
                "expected_answer": "Bias is error from erroneous assumptions; Variance is error from sensitivity to fluctuations. Overfitting is prevented using Dropout, L1/L2 regularization, early stopping, and data augmentation."
            }
        ],
        "dsa": [
            {
                "question_text": "Explain the time and space complexity of QuickSort, MergeSort, and Binary Search.",
                "category": "Data Structures",
                "expected_answer": "MergeSort is O(N log N) worst-case time, O(N) space. QuickSort is O(N log N) average, O(N^2) worst-case time. Binary Search is O(log N) time on sorted arrays."
            }
        ],
        "dbms": [
            {
                "question_text": "What are ACID properties in DBMS and how do indexing and normalization improve performance?",
                "category": "DBMS",
                "expected_answer": "ACID: Atomicity, Consistency, Isolation, Durability. Indexing creates B-Trees to speed retrieval. Normalization reduces data redundancy across normal forms."
            }
        ],
        "sql": [
            {
                "question_text": "Explain the difference between INNER JOIN, LEFT JOIN, and GROUP BY with HAVING clause.",
                "category": "SQL",
                "expected_answer": "INNER JOIN matches rows present in both tables. LEFT JOIN retains all rows from left table. GROUP BY aggregates rows; HAVING filters aggregated groups after grouping."
            }
        ],
        "cn": [
            {
                "question_text": "Explain the 7 layers of the OSI Model and the main differences between TCP and UDP protocols.",
                "category": "Computer Networks",
                "expected_answer": "OSI Layers: Physical, Data Link, Network, Transport, Session, Presentation, Application. TCP is connection-oriented, reliable with handshakes; UDP is connectionless, fast, and unacknowledged."
            }
        ],
        "os": [
            {
                "question_text": "What is Deadlock, what are its 4 necessary conditions, and how does Paging differ from Segmentation?",
                "category": "Operating Systems",
                "expected_answer": "Deadlock conditions: Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait. Paging divides memory into fixed-size pages; Segmentation divides memory into logical variable-length segments."
            }
        ]
    }

    CODING_QUESTION_BANK = [
        {
            "question_text": "Write a function `two_sum(nums, target)` that returns indices of two numbers that add up to target.",
            "category": "Coding",
            "difficulty": "easy",
            "expected_answer": "def two_sum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        diff = target - num\n        if diff in seen:\n            return [seen[diff], i]\n        seen[num] = i\n    return []"
        },
        {
            "question_text": "Write a function `is_palindrome(s)` to determine if a string is a valid palindrome ignoring non-alphanumeric characters.",
            "category": "Coding",
            "difficulty": "easy",
            "expected_answer": "def is_palindrome(s):\n    cleaned = ''.join(c.lower() for c in s if c.isalnum())\n    return cleaned == cleaned[::-1]"
        },
        {
            "question_text": "Write a function `max_subarray(nums)` implementing Kadane's algorithm to find maximum contiguous subarray sum.",
            "category": "Coding",
            "difficulty": "medium",
            "expected_answer": "def max_subarray(nums):\n    max_so_far = current = nums[0]\n    for num in nums[1:]:\n        current = max(num, current + num)\n        max_so_far = max(max_so_far, current)\n    return max_so_far"
        }
    ]

    COMPANY_QUESTION_BANK = {
        "google": [
            {
                "question_text": "Google Interview: How would you design a distributed web crawler that scales to billions of web pages?",
                "category": "Google System Design",
                "expected_answer": "Discuss URL Frontier queue, DNS resolution caching, HTML fetcher workers, duplicate elimination using Bloom filters, and storing index in Bigtable."
            },
            {
                "question_text": "Google Interview: Explain Google's MapReduce architecture and how data locality optimizes distributed computation.",
                "category": "Google Architecture",
                "expected_answer": "Map phase processes key-value pairs, Shuffle/Sort groups keys, Reduce aggregates. Data locality schedules map tasks on nodes holding GFS chunks."
            }
        ],
        "amazon": [
            {
                "question_text": "Amazon Leadership Principle: Describe a time you demonstrated 'Customer Obsession' and 'Ownership'.",
                "category": "Amazon LP",
                "expected_answer": "Candidate should detail taking initiative beyond immediate scope to solve a critical customer pain point using quantifiable metrics."
            },
            {
                "question_text": "Amazon Technical: Design Amazon's flash sale checkout system handling 100,000 requests per second.",
                "category": "Amazon System Design",
                "expected_answer": "Discuss API Gateway, Redis inventory decrement with atomic Lua scripts, asynchronous SQS queues, and DynamoDB for order persistence."
            }
        ],
        "microsoft": [
            {
                "question_text": "Microsoft Interview: How does Azure Blob Storage ensure high availability, replication, and disaster recovery?",
                "category": "Microsoft Azure",
                "expected_answer": "Discuss LRS (Locally Redundant), ZRS (Zone-Redundant), and GRS (Geo-Redundant) replication models across data centers."
            }
        ],
        "tcs": [
            {
                "question_text": "TCS Technical: Explain SDLC phases, Agile methodologies, and how you manage client release deliverables.",
                "category": "TCS Process",
                "expected_answer": "Detail Requirements, Design, Development, Testing, Deployment, Maintenance, and Sprint ceremonies in Scrum."
            }
        ]
    }

    def generate_questions(self, interview_type: str, category: str = None, company_name: str = None, difficulty: str = "medium", resume_data: dict = None, count: int = 5) -> list:
        """Generates a list of question dicts based on parameters."""
        questions = []

        if interview_type == "hr":
            questions = random.sample(self.HR_QUESTION_BANK, min(count, len(self.HR_QUESTION_BANK)))

        elif interview_type == "technical":
            cat_key = (category or "python").lower()
            pool = self.TECHNICAL_QUESTION_BANK.get(cat_key, self.TECHNICAL_QUESTION_BANK["python"])
            # If pool is small, combine with general DSA/DBMS
            if len(pool) < count:
                pool = pool + self.TECHNICAL_QUESTION_BANK["dsa"] + self.TECHNICAL_QUESTION_BANK["dbms"]
            questions = random.sample(pool, min(count, len(pool)))

        elif interview_type == "coding":
            questions = random.sample(self.CODING_QUESTION_BANK, min(count, len(self.CODING_QUESTION_BANK)))

        elif interview_type == "company":
            comp_key = (company_name or "google").lower()
            pool = self.COMPANY_QUESTION_BANK.get(comp_key, self.COMPANY_QUESTION_BANK["google"])
            if len(pool) < count:
                pool = pool + self.HR_QUESTION_BANK[:3]
            questions = pool[:count]

        elif interview_type == "resume":
            skills = (resume_data.get("technical_skills", []) if resume_data else []) or ["Python", "SQL", "Web Development"]
            for skill in skills[:count]:
                questions.append({
                    "question_text": f"Based on your resume, you listed expertise in {skill}. Can you describe a project where you applied {skill} to solve a complex problem?",
                    "category": f"Resume - {skill}",
                    "expected_answer": f"Candidate should detail practical implementation of {skill}, system architecture, challenges overcome, and measurable outcome."
                })
            while len(questions) < count:
                questions.append(self.HR_QUESTION_BANK[len(questions) % len(self.HR_QUESTION_BANK)])

        else:
            questions = random.sample(self.HR_QUESTION_BANK, min(count, len(self.HR_QUESTION_BANK)))

        # Format items
        formatted = []
        for item in questions[:count]:
            formatted.append({
                "question_text": item["question_text"],
                "category": item.get("category", interview_type.upper()),
                "difficulty": difficulty,
                "expected_answer": item.get("expected_answer", "Constructive technical explanation with domain examples.")
            })

        return formatted
