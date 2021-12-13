# Local_file_storage

Local_file_storage provides file CRUD API. Files are stored in container locale storage.

_Basic auth are required (by default USER=admin PASSWORD=admin)_

###Tech
- FastAPI
- SQLAlchemy + SQLite

### Useful links
- Explore API at http://localhost:8000/docs
- Explore docs at http://localhost:8000/redoc

### Useful commands

- run service locally in docker container: `make run`
- run as a daemon (release terminal after app start): `run_daemon`
- run tests: `make tests`
- remove container: `make remove`
