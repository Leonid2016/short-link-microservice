from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from .models import create_user, find_user_by_email, list_users
from shared.jwt_utils import make_token, require_admin, require_auth, read_token
from flask import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
bp = Blueprint('auth', __name__)


@bp.get('/health')
def health():
    return {'status': 'ok', 'service': 'auth'}


@bp.post('/auth/login')
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    u = find_user_by_email(email)
    if not u or not check_password_hash(u['password_hash'], password):
        return jsonify({'error': 'Invalid credentials'}), 401
    token = make_token(u['id'], u['role'], u['email'])
    return jsonify({'token': token, 'role': u['role'], 'email': u['email']})


@bp.post('/auth/register')
def register():
    data = request.get_json(silent=True) or {}
    email = (data.get('email') or '').strip().lower()
    password = data.get('password') or ''
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    if find_user_by_email(email):
        return jsonify({'error': 'User already exists'}), 400
    uid = create_user(email, password, role='user')
    token = make_token(uid, 'user', email)
    return jsonify({'token': token, 'role': 'user', 'email': email})


@bp.get('/auth/me')
@require_auth
def me():
    payload = read_token()
    return jsonify({'user_id': payload['user_id'], 'role': payload['role'], 'email': payload['email']})


@bp.get('/admin/users')
@require_admin
def admin_users():
    q = request.args.get('q')
    return jsonify({'items': list_users(q=q, limit=200)})

@bp.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)