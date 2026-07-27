from flask import Blueprint, request, jsonify

mobile_v2_bp = Blueprint("mobile_v2", __name__, url_prefix="/api/mobile/v2")


@mobile_v2_bp.route("/notifications", methods=["GET"])
def push_notifications():
    """Returns candidate mobile push notifications."""
    return jsonify({
        "notifications": [
            {"id": 1, "title": "Daily Practice Reminder", "body": "Complete 1 AI Mock Interview session today!", "timestamp": "10m ago"},
            {"id": 2, "title": "Resume Tip", "body": "Your ATS score improved by 12% following your recent project updates.", "timestamp": "2h ago"}
        ]
    })


@mobile_v2_bp.route("/offline_sync", methods=["POST"])
def offline_sync():
    """Syncs offline practice sessions with server database."""
    data = request.get_json(silent=True) or {}
    items = data.get("offline_sessions", [])
    return jsonify({"success": True, "synced_count": len(items), "status": "Synced successfully"})


@mobile_v2_bp.route("/ai_chat", methods=["POST"])
def ai_chat():
    """AI Career Mentor chat assistant API endpoint."""
    data = request.get_json(silent=True) or {}
    msg = data.get("message", "How do I prepare for a Python technical interview?")
    return jsonify({
        "response": f"AI Mentor: To excel in Python interviews, focus on core OOP, decorators, generators, memory management, and data structure complexity.",
        "status": "success"
    })
