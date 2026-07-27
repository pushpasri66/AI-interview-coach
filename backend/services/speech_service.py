import os
import time
from werkzeug.utils import secure_filename
from AI.models.voice_analysis import VoiceAnalyzer
from AI.models.confidence_score import ConfidenceScorer


class SpeechService:
    """Service handling audio uploads to uploads/interview_audio/, transcript analysis, and voice quality feature extraction."""

    ALLOWED_AUDIO_EXTENSIONS = {"wav", "mp3", "webm", "ogg", "m4a"}

    def __init__(self):
        self.voice_analyzer = VoiceAnalyzer()
        self.confidence_scorer = ConfidenceScorer()

    def save_audio_file(self, user_id: int, interview_id: int, question_id: int, file_obj) -> str:
        """Saves uploaded audio recording file to uploads/interview_audio/."""
        if not file_obj or file_obj.filename == "":
            raise ValueError("No audio file provided.")

        filename = secure_filename(file_obj.filename)
        ext = filename.rsplit(".", 1)[1].lower() if "." in filename else "webm"

        if ext not in self.ALLOWED_AUDIO_EXTENSIONS:
            ext = "webm"

        timestamp = int(time.time())
        saved_name = f"audio_{user_id}_{interview_id}_{question_id}_{timestamp}.{ext}"

        audio_dir = os.path.join(os.path.dirname(__file__), "..", "..", "uploads", "interview_audio")
        os.makedirs(audio_dir, exist_ok=True)

        full_path = os.path.join(audio_dir, saved_name)
        file_obj.save(full_path)

        rel_path = f"uploads/interview_audio/{saved_name}"
        return rel_path

    def process_speech_transcript(self, transcript_text: str, audio_file_path: str = None) -> str:
        """Processes and cleans speech-to-text transcript."""
        if transcript_text and transcript_text.strip():
            return transcript_text.strip()
        return "Audio response recorded successfully."

    def extract_voice_metrics(self, transcript_text: str, duration_sec: float = 45.0) -> dict:
        """Extracts voice quality, speech rate, filler words count, pause duration, and pitch metrics."""
        cleaned_text = transcript_text.lower() if transcript_text else ""
        words = cleaned_text.split()
        word_count = len(words)

        # Count filler words ("um", "uh", "like", "you know", "basically")
        filler_words_list = ["um", "uh", "like", "you know", "basically", "actually"]
        filler_count = sum(cleaned_text.count(w) for w in filler_words_list)

        # Estimate pause duration (sec)
        pause_duration = round(max(0.0, (duration_sec - (word_count / 2.5))), 1)

        voice_res = self.voice_analyzer.analyze_voice(transcript_text, duration_sec)
        conf_res = self.confidence_scorer.compute_confidence(transcript_text, word_count, duration_sec, filler_count, pause_duration)

        return {
            "speech_rate": voice_res["speaking_rate_wpm"],
            "pitch_score": voice_res["pitch_score"],
            "volume_score": voice_res["volume_score"],
            "clarity_score": voice_res["clarity_percentage"],
            "filler_words_count": filler_count,
            "pause_duration": pause_duration,
            "voice_score": voice_res["voice_score"],
            "confidence_score": conf_res["confidence_score"]
        }
