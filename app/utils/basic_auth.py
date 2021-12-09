"""This module provides Basic Auth dependency for end points"""


from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.utils.hash_pass import hash_password
from app.credentials_storge import auth_storage

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
