import os
class Config:
    JSON_SORT_KEYS = False
    SECRET_KEY = os.getenv("SECRET_KEY","dev-secret-change-me")
    ENV =os.getenv("FLASK_ENV","production")

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI =os.getenv(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "admin.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False