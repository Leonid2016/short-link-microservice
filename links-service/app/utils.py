import hashlib
import os
import secrets
import string

ALPHABET = string.ascii_letters + string.digits


def gen_code(length: int = 7) -> str:
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))


def hash_ip(ip: str) -> str:
    salt = os.getenv('IP_SALT', 'dev-salt')
    return hashlib.sha256((salt + '|' + (ip or '')).encode('utf-8')).hexdigest()
