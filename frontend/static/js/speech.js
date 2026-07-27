/**
 * AI Interview Coach - Speech Recognition & Voice Recording Module
 */

let recognition = null;
let isRecording = false;

document.addEventListener("DOMContentLoaded", () => {
    initSpeechRecognition();
});

/**
 * Initializes Web Speech API recognition engine.
 */
function initSpeechRecognition() {
    const btnMic = document.getElementById("btnMicRecord");
    const micIcon = document.getElementById("micIcon");
    const micText = document.getElementById("micText");
    const answerTextarea = document.getElementById("userAnswerText");

    if (!btnMic || !answerTextarea) return;

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        btnMic.addEventListener("click", () => {
            alert("Speech recognition is not supported in your browser. Please type your response.");
        });
        return;
    }

    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = "en-US";

    recognition.onresult = (event) => {
        let transcript = "";
        for (let i = event.resultIndex; i < event.results.length; i++) {
            transcript += event.results[i][0].transcript;
        }
        if (transcript.strip ? transcript.strip() : transcript) {
            answerTextarea.value = transcript;
        }
    };

    recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        stopRecordingUI();
    };

    recognition.onend = () => {
        if (isRecording) {
            stopRecordingUI();
        }
    };

    btnMic.addEventListener("click", () => {
        if (!isRecording) {
            startRecordingUI();
            try {
                recognition.start();
            } catch (err) {
                console.warn("Recognition start error:", err);
            }
        } else {
            stopRecordingUI();
            try {
                recognition.stop();
            } catch (err) {
                console.warn("Recognition stop error:", err);
            }
        }
    });

    function startRecordingUI() {
        isRecording = true;
        btnMic.classList.add("btn-danger-outline");
        btnMic.classList.remove("btn-outline");
        if (micIcon) micIcon.className = "fa-solid fa-microphone-slash text-rose fa-beat";
        if (micText) micText.textContent = "Listening... (Click to Stop)";
    }

    function stopRecordingUI() {
        isRecording = false;
        btnMic.classList.remove("btn-danger-outline");
        btnMic.classList.add("btn-outline");
        if (micIcon) micIcon.className = "fa-solid fa-microphone text-rose";
        if (micText) micText.textContent = "Speak Answer";
    }
}
