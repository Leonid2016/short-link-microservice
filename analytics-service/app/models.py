from .db import get_conn


def init_schema():
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS clicks (
                id BIGSERIAL PRIMARY KEY,
                link_id BIGINT NOT NULL,
                code TEXT NOT NULL,
                ip_hash TEXT NULL,
                user_agent TEXT NULL,
                referer TEXT NULL,
                clicked_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
            '''
        )
        cur.execute('CREATE INDEX IF NOT EXISTS idx_clicks_link_id ON clicks(link_id)')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_clicks_code ON clicks(code)')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_clicks_clicked_at ON clicks(clicked_at DESC)')
    conn.commit()


def insert_click(link_id: int, code: str, ip_hash: str | None, user_agent: str | None, referer: str | None):
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute(
            'INSERT INTO clicks (link_id, code, ip_hash, user_agent, referer) VALUES (%s,%s,%s,%s,%s)',
            (link_id, code, ip_hash, user_agent, referer)
        )
    conn.commit()


def get_stats(link_id: int):
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute('SELECT COUNT(*) FROM clicks WHERE link_id=%s', (link_id,))
        total = int(cur.fetchone()[0])
        cur.execute(
            '''
            SELECT to_char(date_trunc('day', clicked_at), 'YYYY-MM-DD') AS day, COUNT(*)
            FROM clicks
            WHERE link_id=%s AND clicked_at >= NOW() - interval '14 days'
            GROUP BY day
            ORDER BY day
            ''',
            (link_id,),
        )
        by_day = [{'day': r[0], 'count': int(r[1])} for r in cur.fetchall()]
        cur.execute(
            '''
            SELECT COALESCE(NULLIF(referer, ''), '(direct)') AS ref, COUNT(*)
            FROM clicks
            WHERE link_id=%s
            GROUP BY ref
            ORDER BY COUNT(*) DESC
            LIMIT 10
            ''',
            (link_id,),
        )
        top_ref = [{'referer': r[0], 'count': int(r[1])} for r in cur.fetchall()]
        cur.execute(
            '''
            SELECT clicked_at, COALESCE(NULLIF(referer, ''), '(direct)') AS ref, COALESCE(NULLIF(user_agent, ''), '') AS ua
            FROM clicks
            WHERE link_id=%s
            ORDER BY clicked_at DESC
            LIMIT 20
            ''',
            (link_id,),
        )
        last = [{'clicked_at': r[0].isoformat(), 'referer': r[1], 'user_agent': r[2]} for r in cur.fetchall()]
    return {'total_clicks': total, 'by_day': by_day, 'top_referers': top_ref, 'last_clicks': last}
