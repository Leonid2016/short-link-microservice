from flask import g
from psycopg_pool import ConnectionPool

_pool = None


def init_pool(database_url: str):
    global _pool
    if not database_url:
        raise RuntimeError('DATABASE_URL is not set')
    if _pool is None:
        _pool = ConnectionPool(conninfo=database_url, min_size=1, max_size=5, open=True)


def get_conn():
    if 'db_conn' not in g:
        g.db_conn = _pool.getconn()
    return g.db_conn


def close_conn(_exc=None):
    conn = g.pop('db_conn', None)
    if conn is not None:
        _pool.putconn(conn)
