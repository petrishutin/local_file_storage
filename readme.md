_DISCLAIMER: This is a test task to create local storage application in a single container with Python3 PL. So, I know that it is bad idea to make file storage on high-level PL. I know that it is better to use production grade relational DB like Postgres with async engine to get higher performance. But that was a task_


# Local_file_storage

Local_file_storage provides file CRUD API. Files are stored in container locale storage.

_Basic auth are required (by default STORAGE_USER=admin PASSWORD=admin)_

###Tech
- FastAPI
- SQLAlchemy + SQLite

### Useful links
- Explore API at http://localhost:8000/docs
- Explore docs at http://localhost:8000/redoc

### Useful commands
if you want to start app with another user login/password or any other settings use env variables (see the list in app/settings.py)

- run service locally in docker container: `make run`
- run tests: `make tests`
- remove container: `make remove`
