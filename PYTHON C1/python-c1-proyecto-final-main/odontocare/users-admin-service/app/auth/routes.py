from flask import request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta, timezone

from . import auth_bp
from ..extensions import db
from ..models import User


def _json_ok(data=None, message="OK", status=200):
    return jsonify({"success": True, "data": data or {}, "message": message}), status


def _json_error(message="Bad request", code="BAD_REQUEST", details=None, status=400):
    return (
        jsonify(
            {
                "success": False,
                "error": {
                    "code": code,
                    "message": message,
                    "details": details or [],
                },
            }
        ),
        status,
    )


def _make_token(user: User) -> str:
    secret = current_app.config.get("SECRET_KEY")
    if not secret:
        # Esto no debería pasar si config está bien
        raise RuntimeError("SECRET_KEY is not configured")

    payload = {
        "sub": str(user.id),
        "username": user.username,
        "role": user.role,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=8),
    }
    return jwt.encode(payload, secret, algorithm="HS256")


@auth_bp.get("/health")
def auth_health():
    return _json_ok(
        data={"service": "users-admin-service", "module": "auth"},
        message="OK",
        status=200,
    )


@auth_bp.post("/register")
def register():
    """
    Body JSON:
    {
      "username": "admin",
      "password": "1234",
      "role": "admin"   // opcional
    }
    """
    payload = request.get_json(silent=True) or {}
    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""
    role = (payload.get("role") or "admin").strip() or "admin"

    if not username:
        return _json_error("username is required", code="VALIDATION_ERROR", status=400)
    if not password or len(password) < 4:
        return _json_error(
            "password must be at least 4 characters",
            code="VALIDATION_ERROR",
            status=400,
        )

    # ¿existe?
    existing = User.query.filter_by(username=username).first()
    if existing:
        return _json_error("username already exists", code="CONFLICT", status=409)

    password_hash = generate_password_hash(password)  # pbkdf2:sha256 por defecto
    user = User(username=username, password_hash=password_hash, role=role)

    db.session.add(user)
    db.session.commit()

    return _json_ok(data={"user": user.to_dict()}, message="User registered", status=201)


@auth_bp.post("/login")
def login():
    """
    Body JSON:
    {
      "username": "admin",
      "password": "1234"
    }
    """
    payload = request.get_json(silent=True) or {}
    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""

    if not username or not password:
        return _json_error(
            "username and password are required",
            code="VALIDATION_ERROR",
            status=400,
        )

    user = User.query.filter_by(username=username).first()
    if not user:
        return _json_error("invalid credentials", code="UNAUTHORIZED", status=401)

    if not check_password_hash(user.password_hash, password):
        return _json_error("invalid credentials", code="UNAUTHORIZED", status=401)

    token = _make_token(user)

    return _json_ok(
        data={"access_token": token, "token_type": "Bearer", "user": user.to_dict()},
        message="Login successful",
        status=200,
    )
