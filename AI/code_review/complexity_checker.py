class ComplexityChecker:
    """Estimates time and space complexity for candidate code algorithms."""

    def analyze_complexity(self, code_str: str) -> dict:
        """Determines Big-O Time and Space Complexity."""
        c = code_str.lower() if code_str else ""

        # Check nested loops
        loop_count = c.count("for ") + c.count("while ")

        if loop_count >= 2:
            time_comp = "O(N^2)"
            space_comp = "O(1)" if "append" not in c and "new" not in c else "O(N)"
        elif loop_count == 1:
            time_comp = "O(N)"
            space_comp = "O(N)" if ("[" in c or "list" in c or "map" in c) else "O(1)"
        else:
            time_comp = "O(1)"
            space_comp = "O(1)"

        return {
            "time_complexity": time_comp,
            "space_complexity": space_comp,
            "explanation": f"Detected loop structures resulting in estimated {time_comp} runtime complexity."
        }
