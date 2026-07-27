class DebuggingAssistant:
    """AI Debugging Assistant providing intelligent fix hints and error diagnosis."""

    def diagnose_error(self, code_str: str, error_message: str = None) -> dict:
        """Diagnoses runtime or syntax errors in candidate code."""
        err = error_message or ""

        if "IndentationError" in err or "indent" in err.lower():
            hint = "Check Python indentation consistency. Ensure 4 spaces per block level."
        elif "IndexError" in err or "out of range" in err.lower():
            hint = "Array index out of bounds. Verify loop termination condition and array length."
        elif "KeyError" in err:
            hint = "Dictionary key missing. Use dict.get(key, default) or check key existence before accessing."
        else:
            hint = "Verify object initialization, check variable scope, and validate boundary edge cases."

        return {
            "error_diagnosis": err if err else "Potential edge case vulnerability detected.",
            "debugging_hint": hint,
            "fix_recommended": True
        }
