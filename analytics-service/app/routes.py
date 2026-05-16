import requests
from flask import Blueprint, current_app, jsonify, request
from .models import get_stats, insert_click
from flask import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
bp = Blueprint('analytics', __name__)


@bp.get('/health')
def health():
    return {'status': 'ok', 'service': 'analytics'}


@bp.post('/internal/clicks')
def internal_clicks():
    data = request.get_json(silent=True) or {}
    link_id = data.get('link_id')
    code = data.get('code')
    if not link_id or not code:
        return jsonify({'error': 'link_id and code required'}), 400
    insert_click(int(link_id), str(code), data.get('ip_hash'), data.get('user_agent'), data.get('referer'))
    return jsonify({'ok': True})


@bp.get('/links/<code>/stats')
def link_stats(code: str):
    resp = requests.get(f"{current_app.config['LINKS_INTERNAL_URL'].rstrip('/')}/internal/links/by-code/{code}", timeout=3)
    if resp.status_code != 200:
        return jsonify({'error': 'Not found'}), 404
    link = resp.json()
    stats = get_stats(int(link['id']))
    return jsonify({'link': {
        'id': int(link['id']),
        'code': link['code'],
        'original_url': link['original_url'],
        'created_at': link['created_at'],
        'is_active': link['is_active'],
        'expires_at': link['expires_at'],
    }, **stats})


@bp.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)