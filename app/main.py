import os

from fastapi import FastAPI

from app.file_api import file_router
from app.db import init_db
from app.settings import config

app = FastAPI(title="File storage")

app.include_router(file_router)


@app.on_event("startup")
async def db_setup_at_startup():
    init_db()


@app.on_event("startup")
async def init_storage_at_startup():
    os.makedirs(f'{config.BASE_DIR}/storage/', exist_ok=True)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
