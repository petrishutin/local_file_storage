from typing import List

from pydantic import BaseModel, validator

from fastapi import APIRouter, Depends, status

from app.basic_auth import check_basic_auth, hash_password
from app.basic_auth import auth_storage

auth_router = APIRouter(tags=['Basic Auth'])


class NewUserSchema(BaseModel):
    username: str
    password1: str
    password2: str

    @validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'Username must be alphanumeric'
        return v

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password1' in values and v != values['password1']:
            raise ValueError('passwords do not match')
        return v


@auth_router.post('/add_user', status_code=status.HTTP_201_CREATED)
async def add_user(new_user: NewUserSchema, auth: bool = Depends(check_basic_auth)):  # noqa
    auth_storage.update({new_user.username: hash_password(new_user.password1)})
    return


@auth_router.get('/get_users', response_model=List[str])
async def get_users(auth: bool = Depends(check_basic_auth)):  # noqa
    return list(auth_storage.keys())
