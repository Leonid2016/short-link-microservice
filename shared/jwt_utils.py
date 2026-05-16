import os
import jwt
from flask import request, jsonify
from functools import wraps

ALGO = 'HS256'


def jwt_secret() -> str:
    return os.getenv('JWT_SECRET', 'dev-secret')


def make_token(user_id: int, role: str, email: str) -> str:
    return jwt.encode({"user_id": user_id, "role": role, "email": email}, jwt_secret(), algorithm=ALGO)


def read_token():
    header = request.headers.get('Authorization', '')
    if not header.startswith('Bearer '):
        return None
    token = header[7:].strip()
    try:
        return jwt.decode(token, jwt_secret(), algorithms=[ALGO])
    except Exception:
        return None


def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        payload = read_token()
        if not payload:
            return jsonify({"error": "Unauthorized"}), 401
        request.user = payload
        return fn(*args, **kwargs)
    return wrapper


def require_admin(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        payload = read_token()
        if not payload:
            return jsonify({"error": "Unauthorized"}), 401
        if payload.get('role') != 'admin':
            return jsonify({"error": "Forbidden"}), 403
        request.user = payload
        return fn(*args, **kwargs)
    return wrapper
