/**
 * AI Interview Coach - Coding Environment & Code Execution Module
 */

document.addEventListener("DOMContentLoaded", () => {
    initCodingExecution();
});

/**
 * Initializes code runner execution button.
 */
function initCodingExecution() {
    const btnRunCode = document.getElementById("btnRunCode");
    const codeTextarea = document.getElementById("userAnswerText");
    const outputBox = document.getElementById("codeOutputBox");
    const outputText = document.getElementById("codeOutputText");

    if (!btnRunCode || !codeTextarea || !outputBox) return;

    btnRunCode.addEventListener("click", () => {
        const code = codeTextarea.value.trim();
        if (!code) {
            alert("Please enter Python code to execute.");
            return;
        }

        btnRunCode.disabled = true;
        btnRunCode.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Executing...';
        outputBox.classList.remove("hidden");
        if (outputText) outputText.textContent = "Running Python code in sandbox...";

        // Simulate or post answer for evaluation
        const interviewId = document.getElementById("interviewId") ? document.getElementById("interviewId").value : "";
        const currentQuestionId = document.getElementById("currentQuestionId") ? document.getElementById("currentQuestionId").value : "";
        const csrfToken = document.querySelector('input[name="csrf_token"]') ? document.querySelector('input[name="csrf_token"]').value : "";

        fetch("/interview/answer", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                interview_id: interviewId,
                question_id: currentQuestionId,
                user_answer: code,
                code_language: "python"
            })
        })
        .then(res => res.json())
        .then(data => {
            btnRunCode.disabled = false;
            btnRunCode.innerHTML = '<i class="fa-solid fa-play text-success"></i> Run & Test Code';

            if (data.success) {
                if (outputText) {
                    outputText.textContent = (data.code_output || "Code executed cleanly.").trim();
                }
                // Trigger live feedback display update if handler exists
                if (typeof window.updateLiveFeedbackDisplay === "function") {
                    window.updateLiveFeedbackDisplay(data);
                }
            } else {
                if (outputText) outputText.textContent = `Error: ${data.error || "Execution failed."}`;
            }
        })
        .catch(err => {
            btnRunCode.disabled = false;
            btnRunCode.innerHTML = '<i class="fa-solid fa-play text-success"></i> Run & Test Code';
            if (outputText) outputText.textContent = `Execution Error: ${err.message}`;
        });
    });
}
