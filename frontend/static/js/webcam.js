/**
 * AI Interview Coach - WebRTC Camera Stream & Vision Frame Analysis Module
 */

let videoStream = null;

document.addEventListener("DOMContentLoaded", () => {
    initWebcamModule();
});

/**
 * Initializes camera stream controls and frame capture handlers.
 */
function initWebcamModule() {
    const videoElem = document.getElementById("webcamVideo");
    const canvasElem = document.getElementById("webcamCanvas");
    const btnStart = document.getElementById("btnStartCamera");
    const btnStop = document.getElementById("btnStopCamera");
    const btnCapture = document.getElementById("btnCaptureSnapshot");
    const overlay = document.getElementById("webcamOverlay");
    const statusBadge = document.getElementById("cameraStatusBadge");

    if (!videoElem || !btnStart) return;

    btnStart.addEventListener("click", async () => {
        try {
            videoStream = await navigator.mediaDevices.getUserMedia({
                video: { width: { ideal: 640 }, height: { ideal: 480 }, facingMode: "user" },
                audio: false
            });

            videoElem.srcObject = videoStream;
            if (overlay) overlay.classList.add("hidden");
            if (btnStart) btnStart.classList.add("hidden");
            if (btnStop) btnStop.classList.remove("hidden");
            if (btnCapture) btnCapture.disabled = false;
            if (statusBadge) {
                statusBadge.textContent = "Camera Live & Recording";
                statusBadge.className = "badge badge-primary";
            }
        } catch (err) {
            console.error("Camera access error:", err);
            alert("Unable to access webcam. Please check browser permissions.");
        }
    });

    if (btnStop) {
        btnStop.addEventListener("click", () => {
            stopCameraStream();
        });
    }

    if (btnCapture && canvasElem) {
        btnCapture.addEventListener("click", () => {
            captureAndAnalyzeFrame(videoElem, canvasElem);
        });
    }

    function stopCameraStream() {
        if (videoStream) {
            videoStream.getTracks().forEach((track) => track.stop());
            videoStream = null;
        }
        videoElem.srcObject = null;
        if (overlay) overlay.classList.remove("hidden");
        if (btnStart) btnStart.classList.remove("hidden");
        if (btnStop) btnStop.classList.add("hidden");
        if (btnCapture) btnCapture.disabled = true;
        if (statusBadge) {
            statusBadge.textContent = "Camera Off";
            statusBadge.className = "badge badge-outline";
        }
    }

    function captureAndAnalyzeFrame(video, canvas) {
        const ctx = canvas.getContext("2d");
        canvas.width = video.videoWidth || 640;
        canvas.height = video.videoHeight || 480;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob((blob) => {
            if (!blob) return;

            const formData = new FormData();
            formData.append("video_file", blob, "webcam_snapshot.webm");
            formData.append("interview_id", window.ANALYSIS_DATA ? window.ANALYSIS_DATA.interviewId : 1);

            const csrfToken = document.querySelector('input[name="csrf_token"]') ? document.querySelector('input[name="csrf_token"]').value : "";

            fetch("/analysis/upload_video", {
                method: "POST",
                headers: { "X-CSRFToken": csrfToken },
                body: formData
            })
            .then((res) => res.json())
            .then((data) => {
                if (data.success) {
                    // Update live indicators
                    const eyeVal = document.getElementById("liveEyeVal");
                    const eyeFill = document.getElementById("liveEyeFill");
                    if (eyeVal && data.eye_contact_percentage) {
                        eyeVal.textContent = `${data.eye_contact_percentage}%`;
                        if (eyeFill) eyeFill.style.width = `${data.eye_contact_percentage}%`;
                    }
                }
            })
            .catch((err) => console.error("Frame analysis error:", err));
        }, "image/jpeg", 0.8);
    }
}
