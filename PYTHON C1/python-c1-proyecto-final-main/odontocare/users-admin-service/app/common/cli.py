from flask import Flask
from ..extensions import db

def register_cli(app: Flask):
    @app.cli.command("init-db")
    def init_db():
        """Create database tables."""
        # Import models so SQLAlchemy knows them
        from .. import models  # noqa: F401

        db.create_all()
        print("✅ Database tables created")
