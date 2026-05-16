from werkzeug.security import generate_password_hash
from .db import get_conn


def init_schema():
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS users (
                id BIGSERIAL PRIMARY KEY,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user',
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            '''
        )
    conn.commit()


def ensure_admin(email: str, password: str):
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute('SELECT id FROM users WHERE email=%s', (email.lower().strip(),))
        if cur.fetchone():
            conn.commit()
            return
        cur.execute(
            'INSERT INTO users (email, password_hash, role) VALUES (%s,%s,%s)',
            (email.lower().strip(), generate_password_hash(password), 'admin')
        )
    conn.commit()


def create_user(email: str, password: str, role: str = 'user') -> int:
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(
            'INSERT INTO users (email, password_hash, role) VALUES (%s,%s,%s) RETURNING id',
            (email.lower().strip(), generate_password_hash(password), role)
        )
        uid = cur.fetchone()[0]
    conn.commit()
    return int(uid)


def find_user_by_email(email: str):
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute('SELECT id, email, password_hash, role, created_at FROM users WHERE email=%s', (email.lower().strip(),))
        row = cur.fetchone()
    if not row:
        return None
    return {
        'id': int(row[0]),
        'email': row[1],
        'password_hash': row[2],
        'role': row[3],
        'created_at': row[4].isoformat() if row[4] else None,
    }


def list_users(q: str | None = None, limit: int = 200):
    conn = get_conn()
    with conn.cursor() as cur:
        if q:
            cur.execute(
                'SELECT id, email, role, created_at FROM users WHERE email ILIKE %s ORDER BY created_at DESC LIMIT %s',
                (f'%{q}%', limit)
            )
        else:
            cur.execute('SELECT id, email, role, created_at FROM users ORDER BY created_at DESC LIMIT %s', (limit,))
        rows = cur.fetchall()
    return [
        {
            'id': int(r[0]),
            'email': r[1],
            'role': r[2],
            'created_at': r[3].isoformat() if r[3] else None,
        }
        for r in rows
    ]
