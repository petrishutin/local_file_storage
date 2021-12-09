from fastapi import FastAPI

from app.api.file_api import file_router
from app.api.auth_api import auth_router
from app.db.database import init_db

app = FastAPI(title="File storage")

app.include_router(file_router)
app.include_router(auth_router)


@app.on_event("startup")
async def db_setup_at_startup():
    init_db()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
