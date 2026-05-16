from .db import get_conn


def init_schema():
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS links (
                id BIGSERIAL PRIMARY KEY,
                code TEXT NOT NULL UNIQUE,
                original_url TEXT NOT NULL,
                title TEXT NULL,
                expires_at TIMESTAMPTZ NULL,
                is_active BOOLEAN NOT NULL DEFAULT TRUE,
                owner_user_id BIGINT NULL,
                owner_email_snapshot TEXT NULL,
                is_guest BOOLEAN NOT NULL DEFAULT FALSE,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            '''
        )
        cur.execute('CREATE INDEX IF NOT EXISTS idx_links_owner_user_id ON links(owner_user_id)')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_links_created_at ON links(created_at DESC)')
    conn.commit()


def insert_link(code: str, original_url: str, title=None, expires_at=None, owner_user_id=None, owner_email_snapshot=None, is_guest=False) -> int:
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(
            '''
            INSERT INTO links (code, original_url, title, expires_at, owner_user_id, owner_email_snapshot, is_guest)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            RETURNING id
            ''',
            (code, original_url, title, expires_at, owner_user_id, owner_email_snapshot, is_guest),
        )
        row_id = cur.fetchone()[0]
    conn.commit()
    return int(row_id)


def find_link_by_code(code: str):
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(
            '''
            SELECT id, code, original_url, is_active, expires_at, title, owner_user_id, owner_email_snapshot, is_guest, created_at
            FROM links WHERE code=%s
            ''',
            (code,),
        )
        row = cur.fetchone()
    if not row:
        return None
    return {
        'id': int(row[0]),
        'code': row[1],
        'original_url': row[2],
        'is_active': bool(row[3]),
        'expires_at': row[4].isoformat() if row[4] else None,
        'title': row[5],
        'owner_user_id': int(row[6]) if row[6] is not None else None,
        'owner_email_snapshot': row[7],
        'is_guest': bool(row[8]),
        'created_at': row[9].isoformat() if row[9] else None,
    }


def set_link_active(code: str, is_active: bool) -> bool:
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute('UPDATE links SET is_active=%s WHERE code=%s', (is_active, code))
        updated = cur.rowcount
    conn.commit()
    return updated > 0


def find_existing_link(original_url: str, owner_user_id=None, owner_email_snapshot=None, is_guest=False):
    conn = get_conn()
    sql = '''
        SELECT id, code, original_url, created_at, is_active, title, expires_at, owner_user_id, owner_email_snapshot, is_guest
        FROM links
        WHERE original_url=%s
          AND is_active=TRUE
          AND (expires_at IS NULL OR expires_at > NOW())
    '''
    params = [original_url]
    if is_guest:
        sql += ' AND is_guest=TRUE'
    else:
        sql += ' AND owner_user_id=%s'
        params.append(owner_user_id)
    sql += ' ORDER BY created_at DESC LIMIT 1'
    with conn.cursor() as cur:
        cur.execute(sql, params)
        row = cur.fetchone()
    if not row:
        return None
    return {
        'id': int(row[0]),
        'code': row[1],
        'original_url': row[2],
        'created_at': row[3].isoformat() if row[3] else None,
        'is_active': bool(row[4]),
        'title': row[5],
        'expires_at': row[6].isoformat() if row[6] else None,
        'owner_user_id': int(row[7]) if row[7] is not None else None,
        'owner_email_snapshot': row[8],
        'is_guest': bool(row[9]),
    }


def list_links(limit=200, owner_user_id=None, q=None, owner_email=None, created_from=None, created_to=None):
    conn = get_conn()
    sql = '''
        SELECT id, code, original_url, created_at, is_active, title, expires_at, owner_email_snapshot, is_guest, owner_user_id
        FROM links WHERE 1=1
    '''
    params = []
    if owner_user_id is not None:
        sql += ' AND owner_user_id=%s'
        params.append(owner_user_id)
    if q:
        sql += ' AND (code ILIKE %s OR original_url ILIKE %s OR COALESCE(title,\'\') ILIKE %s)'
        params.extend([f'%{q}%', f'%{q}%', f'%{q}%'])
    if owner_email:
        sql += ' AND COALESCE(owner_email_snapshot, \'\') ILIKE %s'
        params.append(f'%{owner_email}%')
    if created_from:
        sql += ' AND created_at >= %s'
        params.append(created_from)
    if created_to:
        sql += ' AND created_at <= %s'
        params.append(created_to)
    sql += ' ORDER BY created_at DESC LIMIT %s'
    params.append(limit)
    with conn.cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()
    return [
        {
            'id': int(r[0]),
            'code': r[1],
            'original_url': r[2],
            'created_at': r[3].isoformat() if r[3] else None,
            'is_active': bool(r[4]),
            'title': r[5],
            'expires_at': r[6].isoformat() if r[6] else None,
            'user_email': r[7],
            'is_guest': bool(r[8]),
            'owner_user_id': int(r[9]) if r[9] is not None else None,
        }
        for r in rows
    ]
