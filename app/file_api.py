import os
import inspect
from time import time
from hashlib import sha1
from typing import Type

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.basic_auth import check_basic_auth
from app.db import SessionLocal
from app.db import select_file_data, insert_file_meta, delete_file_record, update_file_extension
from app.db import FileMetaData
from app.settings import config
from app.service_logger import logger

file_router = APIRouter(tags=['File CRUD'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def as_form(cls: Type[BaseModel]):
    """
    Adds an as_form class method to decorated models. The as_form class method
    can be used with FastAPI endpoints
    """
    new_params = [
        inspect.Parameter(
            field.alias,
            inspect.Parameter.POSITIONAL_ONLY,
            default=(Form(field.default) if not field.required else Form(...)),
        )
        for field in cls.__fields__.values()
    ]

    async def _as_form(**data):
        return cls(**data)

    sig = inspect.signature(_as_form)
    sig = sig.replace(parameters=new_params)
    _as_form.__signature__ = sig
    setattr(cls, "as_form", _as_form)
    return cls


@file_router.get('/download/{file_hash}')
async def download_file(file_hash: str, db: Session = Depends(get_db), auth: bool = Depends(check_basic_auth)):  # noqa
    file_meta: FileMetaData = select_file_data(db, file_hash=file_hash)
    if not file_meta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'file {file_hash} not found')
    bucket = file_hash[:2]
    return FileResponse(
        f'{config.BASE_DIR}/storage/{bucket}/{file_hash}.{file_meta.extension}',
        filename=f"{file_hash}.{file_meta.extension}"
    )


@file_router.post('/upload', status_code=201, response_model=str)
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
        insert_file_meta(db, file_hash, extension, bucket)
    except Exception as e:
        logger.log(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='can not save file')
    file_data: bytes = uploaded_file.file.read()
    os.makedirs(f'{config.BASE_DIR}/storage/{bucket}', exist_ok=True)
    with open(f'{config.BASE_DIR}/storage/{bucket}/{file_hash}.{extension}', 'wb') as f:
        f.write(file_data)
    return file_hash


@as_form
class UpdateFileForm(BaseModel):
    file_hash: str


@file_router.put('/update/')
async def update_file(
        uploaded_file: UploadFile = File(...),
        file_hash: UpdateFileForm = Depends(UpdateFileForm.as_form),
        db: Session = Depends(get_db),
        auth: bool = Depends(check_basic_auth)  # noqa
):
    file_hash = file_hash.file_hash
    file_meta = select_file_data(db, file_hash)
    if not file_meta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'file {file_hash} not found')
    split_file_name = uploaded_file.filename.rsplit('.')
    new_extension = split_file_name[1] if len(split_file_name) > 1 else None
    if new_extension != file_meta.extension:
        update_file_extension(db, file_hash, new_extension)
    file_data: bytes = uploaded_file.file.read()
    with open(f'{config.BASE_DIR}/storage/{file_meta.bucket}/{file_hash}.{new_extension}', 'wb') as f:
        f.write(file_data)
    return f"file {file_hash} successfully updated"


@file_router.delete('/delete/{file_hash}')
async def delete_file(
        file_hash: str, db: Session = Depends(get_db), auth: bool = Depends(check_basic_auth),  # noqa
):
    file_meta = select_file_data(db, file_hash)
    if not file_meta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'file {file_hash} not found')
    delete_file_record(db, file_hash)
    os.remove(f'{config.BASE_DIR}/storage/{file_meta.bucket}/{file_hash}.{file_meta.extension}')
    return f"file {file_hash} successfully deleted"
