"""
This module provides Basic Auth dependency for endpoints.
Storage lives in memory during runtime, so it makes this app stateful
"""
from hashlib import sha1

from app.settings import config
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials


def hash_password(password: str) -> str:
    return sha1(f"{config.SECRET_KEY}{password}".encode('utf-8')).hexdigest()


security = HTTPBasic()


async def check_basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    stored_pass_hash = auth_storage.get(username)
    if not stored_pass_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not exist",
            headers={"WWW-Authenticate": "Basic"},
        )
    if hash_password(credentials.password) != stored_pass_hash:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True


auth_storage = {config.ADMIN_NAME: hash_password(config.ADMIN_PASSWORD)}
