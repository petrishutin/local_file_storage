"""Util to hash incoming passwords with secret key"""

from hashlib import sha1

from app.settings import config


def hash_password(password: str) -> str:
    return sha1(f"{config.SECRET_KEY}{password}".encode('utf-8')).hexdigest()
