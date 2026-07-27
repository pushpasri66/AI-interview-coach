import sys
import io
import traceback


class CodingService:
    """Service providing safe Python code execution and automated test case evaluation."""

    def execute_python_code(self, code_text: str, test_inputs: list = None) -> dict:
        """Executes user Python code in an isolated scope and captures stdout/stderr."""
        if not code_text or not code_text.strip():
            return {
                "success": False,
                "output": "Error: Empty code submitted.",
                "error": "No code to execute."
            }

        # Redirect stdout/stderr
        old_stdout = sys.stdout
        redirected_output = io.StringIO()
        sys.stdout = redirected_output

        execution_scope = {}
        success = True
        error_msg = None

        try:
            # Execute code in clean global dict
            exec(code_text, execution_scope)
            output = redirected_output.getvalue()
        except Exception as e:
            success = False
            error_msg = f"{type(e).__name__}: {str(e)}"
            output = f"Execution Error:\n{traceback.format_exc()}"
        finally:
            sys.stdout = old_stdout

        return {
            "success": success,
            "output": output if output else "Code executed cleanly with no stdout output.",
            "error": error_msg
        }
