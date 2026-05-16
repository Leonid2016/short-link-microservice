from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse
import requests
from flask import Blueprint, abort, current_app, jsonify, redirect, request
from shared.jwt_utils import read_token, require_admin, require_auth
from .models import find_existing_link, find_link_by_code, insert_link, list_links, set_link_active
from .utils import gen_code, hash_ip
from flask import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
bp = Blueprint('links', __name__)


def is_valid_http_url(url: str) -> bool:
    p = urlparse(url)
    return p.scheme in ('http', 'https') and bool(p.netloc)


def _build_short_url(code: str) -> str:
    return f"{current_app.config['BASE_URL'].rstrip('/')}/s/{code}"


def _send_click_event(link: dict):
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get('User-Agent')
    ref = request.headers.get('Referer')
    try:
        requests.post(
            f"{current_app.config['ANALYTICS_INTERNAL_URL'].rstrip('/')}/internal/clicks",
            json={
                'link_id': link['id'],
                'code': link['code'],
                'ip_hash': hash_ip(ip or ''),
                'user_agent': ua,
                'referer': ref,
            },
            timeout=1.5,
        )
    except Exception:
        pass


@bp.get('/health')
def health():
    return {'status': 'ok', 'service': 'links'}


@bp.post('/links')
def create_link():
    payload = read_token()
    is_guest = payload is None
    owner_user_id = None if is_guest else int(payload['user_id'])
    owner_email = None if is_guest else payload.get('email')

    data = request.get_json(silent=True) or {}
    original_url = (data.get('original_url') or '').strip()
    custom_alias = (data.get('custom_alias') or '').strip()
    expires_at = (data.get('expires_at') or '').strip()
    title = (data.get('title') or '').strip() or None

    if not is_valid_http_url(original_url):
        return jsonify({'error': 'Invalid URL. Use http/https.'}), 400

    if is_guest:
        if custom_alias:
            return jsonify({'error': 'Alias is not available for guest users'}), 400
        expires_dt = datetime.now(timezone.utc) + timedelta(days=30)
    else:
        expires_dt = None
        if expires_at:
            try:
                expires_dt = datetime.fromisoformat(expires_at.replace('Z', '+00:00'))
            except Exception:
                return jsonify({'error': 'expires_at must be ISO datetime, e.g. 2026-01-10T12:00:00Z'}), 400

    if not custom_alias:
        existing = find_existing_link(original_url, owner_user_id=owner_user_id, owner_email_snapshot=owner_email, is_guest=is_guest)
        if existing:
            existing['short_url'] = _build_short_url(existing['code'])
            existing['reused'] = True
            return jsonify(existing), 200

    code = custom_alias or gen_code()
    if find_link_by_code(code):
        return jsonify({'error': 'Alias is already taken.'}), 409

    link_id = insert_link(
        code=code,
        original_url=original_url,
        title=title,
        expires_at=expires_dt,
        owner_user_id=owner_user_id,
        owner_email_snapshot=owner_email,
        is_guest=is_guest,
    )
    return jsonify({
        'id': link_id,
        'code': code,
        'short_url': _build_short_url(code),
        'original_url': original_url,
        'title': title,
        'expires_at': expires_dt.isoformat().replace('+00:00', 'Z') if expires_dt else None,
        'reused': False,
        'is_guest': is_guest,
    }), 201


@bp.get('/links')
@require_auth
def get_links():
    role = request.user['role']
    user_id = int(request.user['user_id'])
    q = request.args.get('q')
    owner_email = request.args.get('user')
    created_from = request.args.get('from')
    created_to = request.args.get('to')
    if role == 'admin':
        items = list_links(limit=200, owner_user_id=None, q=q, owner_email=owner_email, created_from=created_from, created_to=created_to)
    else:
        items = list_links(limit=200, owner_user_id=user_id)
    for it in items:
        it['short_url'] = _build_short_url(it['code'])
    return jsonify({'items': items})


@bp.patch('/links/<code>')
@require_admin
def patch_link(code: str):
    data = request.get_json(silent=True) or {}
    if 'is_active' not in data:
        return jsonify({'error': 'Nothing to update'}), 400
    ok = set_link_active(code, bool(data['is_active']))
    if not ok:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'ok': True})


@bp.get('/internal/links/by-code/<code>')
def internal_link_by_code(code: str):
    link = find_link_by_code(code)
    if not link:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(link)


@bp.get('/s/<code>')
def go(code: str):
    link = find_link_by_code(code)
    if not link or not link['is_active']:
        abort(404)
    exp = link.get('expires_at')
    if exp:
        exp_dt = datetime.fromisoformat(exp.replace('Z', '+00:00'))
        if exp_dt <= datetime.now(timezone.utc):
            abort(404)
    _send_click_event(link)
    return redirect(link['original_url'], code=302)


@bp.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
    
    
