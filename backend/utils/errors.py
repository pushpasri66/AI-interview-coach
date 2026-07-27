from flask import render_template, jsonify, request


def register_error_handlers(app):
    """Registers application-wide HTTP error handlers for 403, 404, 500, and 429."""

    @app.errorhandler(403)
    def forbidden_error(e):
        if request.is_json:
            return jsonify({"error": "Forbidden", "message": "You do not have permission to access this resource."}), 403
        return render_template("403.html"), 403

    @app.errorhandler(404)
    def not_found_error(e):
        if request.is_json:
            return jsonify({"error": "Not Found", "message": "The requested URL was not found on the server."}), 404
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(e):
        app.logger.error(f"Internal server error: {str(e)}")
        if request.is_json:
            return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred."}), 500
        return render_template("500.html"), 500

    @app.errorhandler(429)
    def rate_limit_error(e):
        app.logger.warning(f"Rate limit exceeded by IP: {request.remote_addr}")
        if request.is_json:
            return jsonify({"error": "Rate Limit Exceeded", "message": "Too many requests. Please try again later."}), 429
        return render_template("500.html", message="Too many requests. Rate limit exceeded."), 429
