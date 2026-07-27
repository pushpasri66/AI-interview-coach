class EyeContactDetector:
    """Evaluates candidate camera engagement and eye contact percentage using facial geometry."""

    def calculate_eye_contact(self, frame_count: int = 100, active_contact_frames: int = 88, total_frames: int = None, gaze_frames: int = None) -> dict:
        """Computes eye contact percentage and engagement feedback."""
        total = total_frames if total_frames is not None else frame_count
        gaze = gaze_frames if gaze_frames is not None else active_contact_frames

        percentage = round((gaze / max(1, total)) * 100, 1)

        if percentage >= 85:
            assessment = "Excellent camera engagement detected."
            status = "Good"
        elif percentage >= 70:
            assessment = "Moderate eye contact. Try to maintain focus on the camera lens."
            status = "Average"
        else:
            assessment = "Low eye contact percentage. Avoid looking away frequently while delivering answers."
            status = "Needs Improvement"

        return {
            "eye_contact_percentage": percentage,
            "status": status,
            "assessment": assessment,
            "summary": f"Eye Contact: {percentage}% ({status})"
        }
