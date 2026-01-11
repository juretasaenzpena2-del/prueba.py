from functools import wraps
from flask import request, jsonify, current_app
import jwt


def _json_error(message="Unauthorized", code="UNAUTHORIZED", details=None, status=401):
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


def token_required(fn):
    """
    Exige header:
      Authorization: Bearer <token>
    Si es válido, inyecta `request.user` con claims del token.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return _json_error(
                "Missing or invalid Authorization header",
                code="UNAUTHORIZED",
                status=401,
            )

        token = auth_header.split(" ", 1)[1].strip()
        if not token:
            return _json_error("Token missing", code="UNAUTHORIZED", status=401)

        secret = current_app.config.get("SECRET_KEY")
        if not secret:
            return _json_error("Server misconfigured", code="SERVER_ERROR", status=500)

        try:
            payload = jwt.decode(token, secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return _json_error("Token expired", code="TOKEN_EXPIRED", status=401)
        except jwt.InvalidTokenError:
            return _json_error("Invalid token", code="INVALID_TOKEN", status=401)

        # Guardamos los claims para usarlos en rutas
        request.user = payload  # sub, username, role, etc.
        return fn(*args, **kwargs)

    return wrapper


def require_role(*allowed_roles):
    """
    Uso:
      @token_required
      @require_role("admin")
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            role = getattr(request, "user", {}).get("role")
            if role not in allowed_roles:
                return _json_error(
                    "Forbidden: insufficient permissions",
                    code="FORBIDDEN",
                    status=403,
                    details=[{"allowed_roles": list(allowed_roles), "current_role": role}],
                )
            return fn(*args, **kwargs)
        return wrapper
    return decorator
