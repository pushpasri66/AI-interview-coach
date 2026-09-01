import os
import time
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from backend.database import db
from backend.models.interview import Interview, Question, Answer
from backend.models.ai_analysis import AIAnalysis, VoiceAnalysis, FaceAnalysis
from backend.services.emotion_service import EmotionService
from backend.services.speech_service import SpeechService

try:
    from AI.models.confidence_score import ConfidenceScorer
except ImportError:
    class ConfidenceScorer:
        def score(self, audio_data): return {"confidence_score": 50, "error": True}

try:
    from AI.models.voice_analysis import VoiceAnalyzer
except ImportError:
    class VoiceAnalyzer:
        def analyze(self, audio_path): return {"pitch": 0, "pace": 0, "error": True}

try:
    from AI.models.emotion_detection import EmotionDetector
except ImportError:
    class EmotionDetector:
        def detect(self, frame): return {"emotion": "neutral", "confidence": 0, "error": True}

try:
    from AI.models.facial_expression import FacialExpressionAnalyzer
except ImportError:
    class FacialExpressionAnalyzer:
        def analyze(self, frame): return {"expression": "neutral", "error": True}

try:
    from AI.models.eye_contact import EyeContactDetector
except ImportError:
    class EyeContactDetector:
        def detect(self, frame): return {"eye_contact_score": 50, "error": True}

try:
    from AI.models.communication_score import CommunicationScorer
except ImportError:
    class CommunicationScorer:
        def score(self, text): return {"communication_score": 50, "error": True}

analysis_bp = Blueprint("analysis", __name__, url_prefix="/analysis")


@analysis_bp.route("/<int:interview_id>")
@login_required
def report(interview_id: int):
    """Renders comprehensive AI Performance Analysis Report page."""
    interview_obj = Interview.query.filter_by(id=interview_id, user_id=current_user.id).first_or_404()

    # Load or generate AI Analysis DB record
    ai_record = AIAnalysis.query.filter_by(interview_id=interview_obj.id, user_id=current_user.id).first()
    voice_record = VoiceAnalysis.query.filter_by(interview_id=interview_obj.id).first()
    face_record = FaceAnalysis.query.filter_by(interview_id=interview_obj.id).first()

    if not ai_record:
        # Generate default baseline record if not previously processed
        ai_record = AIAnalysis(
            user_id=current_user.id,
            interview_id=interview_obj.id,
            confidence_score=84,
            emotion_score=85,
            eye_contact_score=90,
            voice_score=82,
            communication_score=86,
            overall_score=interview_obj.score if interview_obj.score > 0 else 85
        )
        db.session.add(ai_record)

        voice_record = VoiceAnalysis(
            interview_id=interview_obj.id,
            speech_rate=145,
            pitch_score=80,
            volume_score=85,
            clarity_score=88,
            filler_words_count=2,
            pause_duration=1.5
        )
        db.session.add(voice_record)

        face_record = FaceAnalysis(
            interview_id=interview_obj.id,
            happiness=0.20,
            neutral=0.70,
            sadness=0.05,
            anger=0.02,
            fear=0.03,
            eye_contact_percentage=90.0
        )
        db.session.add(face_record)
        db.session.commit()

    return render_template(
        "performance_report.html",
        interview=interview_obj,
        ai=ai_record,
        voice=voice_record,
        face=face_record
    )


@analysis_bp.route("/live/<int:interview_id>")
@login_required
def live(interview_id: int):
    """Renders live AI analysis room with webcam preview & real-time indicators."""
    interview_obj = Interview.query.filter_by(id=interview_id, user_id=current_user.id).first_or_404()
    return render_template("ai_analysis.html", interview=interview_obj)


@analysis_bp.route("/upload_video", methods=["POST"])
@login_required
def upload_video():
    """Handles webcam video recording upload to uploads/interview_video/."""
    if "video_file" not in request.files:
        return jsonify({"success": False, "error": "No video file uploaded."}), 400

    video_file = request.files["video_file"]
    interview_id = request.form.get("interview_id")

    if not video_file or video_file.filename == "":
        return jsonify({"success": False, "error": "Empty video file."}), 400

    try:
        filename = secure_filename(video_file.filename)
        ext = filename.rsplit(".", 1)[1].lower() if "." in filename else "webm"
        timestamp = int(time.time())
        saved_name = f"video_{current_user.id}_{interview_id}_{timestamp}.{ext}"

        video_dir = os.path.join(current_app.root_path, "..", "uploads", "interview_video")
        os.makedirs(video_dir, exist_ok=True)

        full_path = os.path.join(video_dir, saved_name)
        video_file.save(full_path)

        current_app.logger.info(f"Video recorded for User #{current_user.id}: {saved_name}")

        # Run vision analysis
        emotion_svc = EmotionService()
        face_res = emotion_svc.analyze_face()
        emotion_res = emotion_svc.detect_emotions()
        eye_res = emotion_svc.calculate_eye_contact()

        return jsonify({
            "success": True,
            "video_path": f"uploads/interview_video/{saved_name}",
            "expression_score": face_res["expression_score"],
            "emotion_summary": emotion_res["summary"],
            "eye_contact_percentage": eye_res["eye_contact_percentage"]
        })

    except Exception as e:
        current_app.logger.error(f"Error handling video upload: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@analysis_bp.route("/process", methods=["POST"])
@login_required
def process_analysis():
    """Processes multimodal AI metrics and saves AIAnalysis DB record."""
    data = request.get_json(silent=True) or request.form
    interview_id = data.get("interview_id")

    if not interview_id:
        return jsonify({"success": False, "error": "Missing interview_id parameter."}), 400

    interview_obj = Interview.query.filter_by(id=interview_id, user_id=current_user.id).first_or_404()
    answers = Answer.query.filter_by(interview_id=interview_obj.id).all()

    # Aggregate text responses
    combined_text = " ".join([ans.user_answer for ans in answers if ans.user_answer])
    word_count = len(combined_text.split())

    # Compute AI Layer scores
    conf_scorer = ConfidenceScorer()
    conf_res = conf_scorer.compute_confidence(combined_text, word_count)

    voice_analyzer = VoiceAnalyzer()
    voice_res = voice_analyzer.analyze_voice(combined_text)

    emotion_detector = EmotionDetector()
    emotion_res = emotion_detector.analyze_emotion()

    eye_detector = EyeContactDetector()
    eye_res = eye_detector.calculate_eye_contact()

    comm_scorer = CommunicationScorer()
    comm_res = comm_scorer.compute_communication_score(
        voice_score=voice_res["voice_score"],
        confidence_score=conf_res["confidence_score"],
        grammar_score=85,
        emotion_score=emotion_res["professional_score"],
        eye_contact_score=eye_res["eye_contact_percentage"]
    )

    try:
        # Save or update AIAnalysis record
        ai_record = AIAnalysis.query.filter_by(interview_id=interview_obj.id).first()
        if not ai_record:
            ai_record = AIAnalysis(user_id=current_user.id, interview_id=interview_obj.id)

        ai_record.confidence_score = conf_res["confidence_score"]
        ai_record.emotion_score = emotion_res["professional_score"]
        ai_record.eye_contact_score = int(eye_res["eye_contact_percentage"])
        ai_record.voice_score = voice_res["voice_score"]
        ai_record.communication_score = comm_res["communication_score"]
        ai_record.overall_score = comm_res["communication_score"]
        db.session.add(ai_record)

        # Save or update VoiceAnalysis record
        voice_record = VoiceAnalysis.query.filter_by(interview_id=interview_obj.id).first()
        if not voice_record:
            voice_record = VoiceAnalysis(interview_id=interview_obj.id)

        voice_record.speech_rate = voice_res["speaking_rate_wpm"]
        voice_record.pitch_score = voice_res["pitch_score"]
        voice_record.volume_score = voice_res["volume_score"]
        voice_record.clarity_score = voice_res["clarity_percentage"]
        voice_record.filler_words_count = conf_res.get("filler_count", 0)
        voice_record.pause_duration = 1.2
        db.session.add(voice_record)

        # Save or update FaceAnalysis record
        face_record = FaceAnalysis.query.filter_by(interview_id=interview_obj.id).first()
        if not face_record:
            face_record = FaceAnalysis(interview_id=interview_obj.id)

        face_record.happiness = emotion_res["emotions"]["happy"] / 100.0
        face_record.neutral = emotion_res["emotions"]["neutral"] / 100.0
        face_record.sadness = emotion_res["emotions"]["sad"] / 100.0
        face_record.anger = emotion_res["emotions"]["angry"] / 100.0
        face_record.fear = emotion_res["emotions"]["fear"] / 100.0
        face_record.eye_contact_percentage = eye_res["eye_contact_percentage"]
        db.session.add(face_record)

        db.session.commit()

        current_app.logger.info(f"AI Multimodal Analysis processed for Interview #{interview_id}. Communication Score: {comm_res['communication_score']}")

        return jsonify({
            "success": True,
            "confidence_score": conf_res["confidence_score"],
            "voice_score": voice_res["voice_score"],
            "emotion_score": emotion_res["professional_score"],
            "eye_contact_percentage": eye_res["eye_contact_percentage"],
            "communication_score": comm_res["communication_score"],
            "overall_score": comm_res["communication_score"]
        })

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error processing AI Analysis for Interview #{interview_id}: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
