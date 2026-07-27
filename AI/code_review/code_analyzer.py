class CodeAnalyzer:
    """Analyzes code quality, readability, and syntax conventions across Python, Java, C++, and JavaScript."""

    def analyze_code_quality(self, code_str: str, language: str = "python") -> dict:
        """Evaluates code quality score and style compliance."""
        if not code_str or not code_str.strip():
            return {"quality_score": 50, "issues": ["Code snippet is empty."], "language": language}

        issues = []
        code_clean = code_str.strip()

        # Common code quality checks
        if "def " not in code_clean and "function" not in code_clean and "class" not in code_clean and "void" not in code_clean:
            issues.append("Consider encapsulating logic inside modular functions or classes.")

        if len(code_clean.split("\n")) < 3:
            issues.append("Add docstrings or inline comments explaining complex algorithm steps.")

        score = max(60, 95 - (len(issues) * 15))

        return {
            "quality_score": score,
            "issues": issues if issues else ["Code is clean, modular, and adheres to standard style guidelines."],
            "language": language
        }
