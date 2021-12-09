from time import time

from fastapi import APIRouter, UploadFile, File, Depends

from hashlib import sha1

from app.utils.basic_auth import check_basic_auth

file_router = APIRouter(tags=['File CRUD'])


@file_router.get('/download/{file_hash}')
async def read_file(file_hash: str, auth: bool = Depends(check_basic_auth)):  # noqa
    return "downloading"


@file_router.post('/upload', response_model=str)
async def upload_file(uploaded_file: UploadFile = File(...), auth: bool = Depends(check_basic_auth)):  # noqa
    hash_name = sha1(f"{time()}{uploaded_file.filename}".encode('utf-8')).hexdigest()
    return hash_name


@file_router.put('/update/{file_hash}')
async def update_file(auth: bool = Depends(check_basic_auth)):
    return "updated"


@file_router.delete('/delete')
async def delete_file(auth: bool = Depends(check_basic_auth)):
    return "deleted"
