/**
 * AI Interview Coach - Global Client JavaScript
 */

document.addEventListener("DOMContentLoaded", () => {
    // 1. Mobile Navigation Toggle
    const navToggle = document.getElementById("navToggle");
    const navLinks = document.getElementById("navLinks");

    if (navToggle && navLinks) {
        navToggle.addEventListener("click", () => {
            navLinks.classList.toggle("show");
        });
    }

    // 2. Auto-Dismiss Flash Messages after 4 Seconds
    const flashAlerts = document.querySelectorAll(".flash-messages-container .alert");
    flashAlerts.forEach((alert) => {
        setTimeout(() => {
            alert.style.transition = "opacity 0.5s ease-out, transform 0.5s ease-out";
            alert.style.opacity = "0";
            alert.style.transform = "translateY(-10px)";
            setTimeout(() => alert.remove(), 500);
        }, 4000);
    });

    // 3. Form Loading Button Animation on Submit for Auth Forms
    const authForms = document.querySelectorAll("#loginForm, #registerForm");
    authForms.forEach((form) => {
        form.addEventListener("submit", function () {
            const submitBtn = this.querySelector(".btn-submit");
            if (submitBtn && this.checkValidity()) {
                const btnText = submitBtn.querySelector(".btn-text");
                const btnSpinner = submitBtn.querySelector(".btn-spinner");

                if (btnText && btnSpinner) {
                    btnText.classList.add("hidden");
                    btnSpinner.classList.remove("hidden");
                }
                submitBtn.disabled = true;
            }
        });
    });

    // 4. Drag & Drop File Upload Logic (Resume Upload)
    initDragAndDropUpload();

    // 5. Animated Circular ATS Score Counter
    initCircularATSProgress();
});

/**
 * Toggles visibility of a password input field.
 * @param {string} inputId - ID of the password input field.
 * @param {HTMLElement} btn - Toggle button element.
 */
function togglePasswordVisibility(inputId, btn) {
    const input = document.getElementById(inputId);
    if (!input) return;

    const icon = btn.querySelector("i");
    if (input.type === "password") {
        input.type = "text";
        if (icon) {
            icon.classList.remove("fa-eye");
            icon.classList.add("fa-eye-slash");
        }
    } else {
        input.type = "password";
        if (icon) {
            icon.classList.remove("fa-eye-slash");
            icon.classList.add("fa-eye");
        }
    }
}

/**
 * Initializes Drag and Drop file upload zone and file preview.
 */
function initDragAndDropUpload() {
    const dropZone = document.getElementById("dropZone");
    const fileInput = document.getElementById("resumeFileInput");
    const previewCard = document.getElementById("filePreviewCard");
    const fileNameText = document.getElementById("selectedFileName");
    const fileSizeText = document.getElementById("selectedFileSize");
    const btnRemoveFile = document.getElementById("btnRemoveFile");
    const btnSubmit = document.getElementById("btnAnalyzeSubmit");
    const fileTypeIcon = document.getElementById("fileTypeIcon");
    const uploadForm = document.getElementById("resumeUploadForm");

    if (!dropZone || !fileInput) return;

    // Click to open file dialog
    dropZone.addEventListener("click", () => fileInput.click());

    // Drag events
    ["dragenter", "dragover"].forEach((eventName) => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.add("dragover");
        });
    });

    ["dragleave", "drop"].forEach((eventName) => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.remove("dragover");
        });
    });

    // Handle dropped files
    dropZone.addEventListener("drop", (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelection(files[0]);
        }
    });

    // Handle file selection via browse
    fileInput.addEventListener("change", (e) => {
        if (e.target.files.length > 0) {
            handleFileSelection(e.target.files[0]);
        }
    });

    // Remove selected file
    if (btnRemoveFile) {
        btnRemoveFile.addEventListener("click", (e) => {
            e.stopPropagation();
            fileInput.value = "";
            previewCard.classList.add("hidden");
            dropZone.classList.remove("hidden");
            btnSubmit.disabled = true;
        });
    }

    function handleFileSelection(file) {
        const name = file.name;
        const ext = name.split(".").pop().lowerCase || name.split(".").pop().toLowerCase();
        const sizeMB = (file.size / (1024 * 1024)).toFixed(2);

        if (ext !== "pdf" && ext !== "docx") {
            alert("Only PDF and DOCX file formats are allowed.");
            fileInput.value = "";
            return;
        }

        if (file.size > 5 * 1024 * 1024) {
            alert("File size exceeds 5 MB. Please select a smaller file.");
            fileInput.value = "";
            return;
        }

        fileNameText.textContent = name;
        fileSizeText.textContent = `${sizeMB} MB`;

        if (ext === "pdf") {
            fileTypeIcon.className = "fa-solid fa-file-pdf text-rose";
        } else {
            fileTypeIcon.className = "fa-solid fa-file-word text-blue";
        }

        previewCard.classList.remove("hidden");
        btnSubmit.disabled = false;
    }

    // Handle Form Submit & Progress Simulation
    if (uploadForm) {
        uploadForm.addEventListener("submit", function () {
            const progressContainer = document.getElementById("uploadProgressContainer");
            const progressBarFill = document.getElementById("progressBarFill");
            const progressPercentage = document.getElementById("progressPercentage");
            const btnText = btnSubmit.querySelector(".btn-text");
            const btnSpinner = btnSubmit.querySelector(".btn-spinner");

            if (progressContainer && progressBarFill && progressPercentage) {
                progressContainer.classList.remove("hidden");
                let progress = 0;
                const interval = setInterval(() => {
                    progress += Math.floor(Math.random() * 12) + 5;
                    if (progress > 92) {
                        progress = 92;
                        clearInterval(interval);
                    }
                    progressBarFill.style.width = `${progress}%`;
                    progressPercentage.textContent = `${progress}%`;
                }, 250);
            }

            if (btnText && btnSpinner) {
                btnText.classList.add("hidden");
                btnSpinner.classList.remove("hidden");
            }
            btnSubmit.disabled = true;
        });
    }
}

/**
 * Animates the circular ATS score progress meter on progress.html.
 */
function initCircularATSProgress() {
    const circle = document.getElementById("atsProgressCircle");
    const scoreText = document.getElementById("atsScoreText");

    if (!circle || !scoreText) return;

    const targetScore = parseInt(circle.getAttribute("data-score") || "0", 10);
    const scoreColor = circle.getAttribute("data-color") || "#6366f1";

    let currentScore = 0;
    const duration = 1200; // ms
    const stepTime = Math.max(15, Math.floor(duration / (targetScore || 1)));

    const timer = setInterval(() => {
        currentScore++;
        if (currentScore >= targetScore) {
            currentScore = targetScore;
            clearInterval(timer);
        }

        scoreText.textContent = currentScore;
        const deg = (currentScore / 100) * 360;
        circle.style.background = `conic-gradient(${scoreColor} ${deg}deg, #334155 ${deg}deg)`;
    }, stepTime);
}
