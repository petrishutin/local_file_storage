from fastapi import FastAPI, APIRouter

app = FastAPI(title="File storage")
crud = APIRouter(tags=['File CRUD'])


@crud.get('/read')
async def read_file():
    return "read"


@crud.post('/create')
async def create_file():
    return "created"


@crud.put('/update')
async def update_file():
    return "updated"


@crud.delete('/delete')
async def delete_file():
    return "deleted"


app.include_router(crud)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
