from flask import Flask, jsonify
from .config import Config
from .common.errors import register_error_handlers
from .extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Extensions
    db.init_app(app)

    # Blueprints
    from .auth import auth_bp
    from .admin import admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    # CLI
    from .common.cli import register_cli
    register_cli(app)

    # Errors JSON
    register_error_handlers(app)

    @app.get("/health")
    def root_health():
        return jsonify(
            {"success": True, "data": {"service": "users-admin-service"}, "message": "OK"}
        ), 200

    return app
