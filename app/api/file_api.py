import os
from time import time
from hashlib import sha1

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.basic_auth import check_basic_auth
from app.db.database import SessionLocal
from app.db.db_utils import select_file_data, insert_file_data
from app.db.models import FileMetaData
from app.settings import config
from app.service_logger import logger

file_router = APIRouter(tags=['File CRUD'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@file_router.get('/download/{file_hash}')
async def read_file(file_hash: str, db: Session = Depends(get_db), auth: bool = Depends(check_basic_auth)):  # noqa
    file_meta: FileMetaData = select_file_data(db, hash_name=file_hash)
    if not file_meta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'file {file_hash} not found')
    bucket = file_hash[:2]
    return FileResponse(
        f'{config.BASE_DIR}/storage/{bucket}/{file_hash}.{file_meta.extension}',
        filename=f"{file_hash}.{file_meta.extension}"
    )


@file_router.post('/upload', response_model=str)
async def upload_file(
        uploaded_file: UploadFile = File(...),
        db: Session = Depends(get_db),
        auth: bool = Depends(check_basic_auth)  # noqa
):
    split_file_name = uploaded_file.filename.rsplit('.')
    extension = split_file_name[1] if len(split_file_name) > 1 else None
    if not extension:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='file name must have extension')
    file_hash = sha1(f"{time()}{uploaded_file.filename}".encode('utf-8')).hexdigest()
    bucket = file_hash[:2]
    try:
        insert_file_data(db, file_hash, extension, bucket)
    except Exception as e:
        logger.log(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='can not save file')
    file_data: bytes = uploaded_file.file.read()
    os.makedirs(f'{config.BASE_DIR}/storage/{bucket}', exist_ok=True)
    with open(f'{config.BASE_DIR}/storage/{bucket}/{file_hash}.{extension}', 'wb') as f:
        f.write(file_data)
    return file_hash


@file_router.put('/update/{file_hash}')
async def update_file(auth: bool = Depends(check_basic_auth)):
    return "updated"


@file_router.delete('/delete')
async def delete_file(auth: bool = Depends(check_basic_auth)):
    return "deleted"
