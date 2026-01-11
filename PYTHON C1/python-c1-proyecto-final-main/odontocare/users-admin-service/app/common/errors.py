from flask import jsonify

class APIError(Exception):
    def __init__(self, message, status_code=400, code="API_ERROR", details=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
        self.details = details or []

def register_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(err: APIError):
        return jsonify({
            "success": False,
            "error": {
                "code": err.code,
                "message": err.message,
                "details": err.details
            }
        }), err.status_code

    @app.errorhandler(404)
    def handle_404(_):
        return jsonify({
            "success": False,
            "error": {
                "code": "NOT_FOUND",
                "message": "Resource not found",
                "details": []
            }
        }), 404

    @app.errorhandler(405)
    def handle_405(_):
        return jsonify({
            "success": False,
            "error": {
                "code": "METHOD_NOT_ALLOWED",
                "message": "Method not allowed",
                "details": []
            }
        }), 405

    @app.errorhandler(500)
    def handle_500(_):
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Internal server error",
                "details": []
            }
        }), 500
