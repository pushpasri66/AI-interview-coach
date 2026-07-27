import os
import time
from werkzeug.utils import secure_filename


class RecordingService:
    """Service managing complete interview session video/audio recording persistence and retrieval."""

    def __init__(self):
        self.base_uploads = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "uploads"))
        self.rec_dir = os.path.join(self.base_uploads, "recordings")
        self.audio_dir = os.path.join(self.base_uploads, "interview_audio")
        self.video_dir = os.path.join(self.base_uploads, "interview_video")

        for d in [self.rec_dir, self.audio_dir, self.video_dir]:
            os.makedirs(d, exist_ok=True)

    def save_session_recording(self, user_id: int, interview_id: int, file_obj, media_type: str = "video") -> str:
        """Saves session media recording to uploads directory."""
        if not file_obj or file_obj.filename == "":
            raise ValueError("No media file provided.")

        filename = secure_filename(file_obj.filename)
        ext = filename.rsplit(".", 1)[1].lower() if "." in filename else ("webm" if media_type == "video" else "wav")
        timestamp = int(time.time())
        saved_name = f"{media_type}_{user_id}_{interview_id}_{timestamp}.{ext}"

        target_dir = self.video_dir if media_type == "video" else self.audio_dir
        full_path = os.path.join(target_dir, saved_name)
        file_obj.save(full_path)

        return f"uploads/{'interview_video' if media_type == 'video' else 'interview_audio'}/{saved_name}"

    def list_user_recordings(self, user_id: int) -> list:
        """Lists recorded media files for candidate."""
        recordings = []
        for fn in os.listdir(self.video_dir):
            if fn.startswith(f"video_{user_id}_"):
                recordings.append({"type": "video", "filename": fn, "path": f"uploads/interview_video/{fn}"})
        for fn in os.listdir(self.audio_dir):
            if fn.startswith(f"audio_{user_id}_"):
                recordings.append({"type": "audio", "filename": fn, "path": f"uploads/interview_audio/{fn}"})
        return recordings
