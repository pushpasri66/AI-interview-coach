/**
 * AI Interview Coach - Interview Room Manager & Dynamic Flow Engine
 */

let questionTimerInterval = null;
let totalTimerInterval = null;
let questionTimeRemaining = 120; // 120 seconds per question
let totalSecondsElapsed = 0;
let currentQIndex = 0;

document.addEventListener("DOMContentLoaded", () => {
    initInterviewRoom();
});

function initInterviewRoom() {
    if (!window.INTERVIEW_DATA || !window.INTERVIEW_DATA.questions || window.INTERVIEW_DATA.questions.length === 0) {
        return;
    }

    startTotalTimer();
    startQuestionTimer();

    const answerForm = document.getElementById("answerForm");
    const btnSubmit = document.getElementById("btnSubmitAnswer");
    const btnNext = document.getElementById("btnNextQuestion");

    if (answerForm) {
        answerForm.addEventListener("submit", (e) => {
            e.preventDefault();
            submitCurrentAnswer();
        });
    }

    if (btnNext) {
        btnNext.addEventListener("click", () => {
            loadNextQuestion();
        });
    }
}

/**
 * Starts question countdown timer (120s).
 */
function startQuestionTimer() {
    clearInterval(questionTimerInterval);
    questionTimeRemaining = 120;
    updateQuestionTimerDisplay();

    questionTimerInterval = setInterval(() => {
        questionTimeRemaining--;
        updateQuestionTimerDisplay();

        if (questionTimeRemaining <= 0) {
            clearInterval(questionTimerInterval);
            // Auto submit answer on timeout
            submitCurrentAnswer(true);
        }
    }, 1000);
}

function updateQuestionTimerDisplay() {
    const display = document.getElementById("questionTimer");
    if (!display) return;

    const mins = Math.floor(questionTimeRemaining / 60);
    const secs = questionTimeRemaining % 60;
    display.textContent = `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
}

/**
 * Starts total interview duration counter.
 */
function startTotalTimer() {
    clearInterval(totalTimerInterval);
    totalSecondsElapsed = 0;

    totalTimerInterval = setInterval(() => {
        totalSecondsElapsed++;
        const display = document.getElementById("totalTimer");
        if (display) {
            const mins = Math.floor(totalSecondsElapsed / 60);
            const secs = totalSecondsElapsed % 60;
            display.textContent = `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
        }
    }, 1000);
}

/**
 * Submits candidate answer via AJAX to /interview/answer.
 */
function submitCurrentAnswer(isTimeout = false) {
    const interviewId = document.getElementById("interviewId").value;
    const currentQId = document.getElementById("currentQuestionId").value;
    const answerText = document.getElementById("userAnswerText").value;
    const btnSubmit = document.getElementById("btnSubmitAnswer");
    const btnNext = document.getElementById("btnNextQuestion");
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;

    if (btnSubmit) {
        const btnText = btnSubmit.querySelector(".btn-text");
        const btnSpinner = btnSubmit.querySelector(".btn-spinner");
        if (btnText && btnSpinner) {
            btnText.classList.add("hidden");
            btnSpinner.classList.remove("hidden");
        }
        btnSubmit.disabled = true;
    }

    const payload = {
        interview_id: parseInt(interviewId, 10),
        question_id: parseInt(currentQId, 10),
        user_answer: isTimeout && !answerText.trim() ? "[Time Expired - No Answer Submitted]" : answerText
    };

    fetch("/interview/answer", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify(payload)
    })
    .then((res) => res.json())
    .then((data) => {
        if (btnSubmit) {
            const btnText = btnSubmit.querySelector(".btn-text");
            const btnSpinner = btnSubmit.querySelector(".btn-spinner");
            if (btnText && btnSpinner) {
                btnText.classList.remove("hidden");
                btnSpinner.classList.add("hidden");
            }
            btnSubmit.disabled = false;
        }

        if (data.success) {
            updateLiveFeedbackDisplay(data);
            if (btnNext) btnNext.classList.remove("hidden");
        } else {
            alert(`Error: ${data.error || "Failed to submit answer."}`);
        }
    })
    .catch((err) => {
        console.error("Answer submission error:", err);
        if (btnSubmit) btnSubmit.disabled = false;
    });
}

/**
 * Updates Real-Time AI Feedback Sidebar in interview_room.html.
 */
window.updateLiveFeedbackDisplay = function (data) {
    const placeholder = document.getElementById("feedbackPlaceholder");
    const liveContent = document.getElementById("feedbackLiveContent");
    const liveScoreValue = document.getElementById("liveScoreValue");
    const liveTechScore = document.getElementById("liveTechScore");
    const liveRelevanceScore = document.getElementById("liveRelevanceScore");
    const liveCommScore = document.getElementById("liveCommScore");
    const liveFeedbackText = document.getElementById("liveFeedbackText");
    const liveStrengthsText = document.getElementById("liveStrengthsText");
    const liveImprovementsText = document.getElementById("liveImprovementsText");

    if (placeholder) placeholder.classList.add("hidden");
    if (liveContent) liveContent.classList.remove("hidden");

    if (liveScoreValue) liveScoreValue.textContent = data.score || 0;
    if (liveTechScore) liveTechScore.textContent = `${data.technical_score || 0}%`;
    if (liveRelevanceScore) liveRelevanceScore.textContent = `${data.relevance_score || 0}%`;
    if (liveCommScore) liveCommScore.textContent = `${data.communication_score || 0}%`;

    if (liveFeedbackText) liveFeedbackText.textContent = data.feedback || "";
    if (liveStrengthsText) liveStrengthsText.textContent = data.strengths || "";
    if (liveImprovementsText) liveImprovementsText.textContent = data.improvements || "";
};

/**
 * Loads the next question in the session.
 */
function loadNextQuestion() {
    const questions = window.INTERVIEW_DATA.questions;
    currentQIndex++;

    if (currentQIndex >= questions.length) {
        // Redirect to complete interview
        const interviewId = document.getElementById("interviewId").value;
        window.location.href = `/interview/complete/${interviewId}`;
        return;
    }

    const q = questions[currentQIndex];
    document.getElementById("currentQuestionId").value = q.id;
    document.getElementById("currentQuestionIndex").value = currentQIndex;
    document.getElementById("questionCategoryBadge").textContent = q.category || "General";
    document.getElementById("questionTextDisplay").textContent = q.text;
    document.getElementById("userAnswerText").value = "";

    // Reset feedback sidebar
    const placeholder = document.getElementById("feedbackPlaceholder");
    const liveContent = document.getElementById("feedbackLiveContent");
    const btnNext = document.getElementById("btnNextQuestion");

    if (placeholder) placeholder.classList.remove("hidden");
    if (liveContent) liveContent.classList.add("hidden");
    if (btnNext) btnNext.classList.add("hidden");

    // Update Progress Bar
    const progressText = document.getElementById("questionProgressText");
    const progressFill = document.getElementById("progressFill");
    if (progressText) progressText.textContent = `Question ${currentQIndex + 1} of ${questions.length}`;
    if (progressFill) progressFill.style.width = `${((currentQIndex + 1) / questions.length) * 100}%`;

    // Restart Question Timer
    startQuestionTimer();
}
