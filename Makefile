remove:
	docker rm -v -f local_file_storage

build:
	docker build -t local_file_storage .

run: remove build
	docker run --network="host" --name local_file_storage -it -p 8000:8000 -e STORAGE_USER=$(STORAGE_USER) PASSWORD=$(PASSWORD) DB_URL=$(DB_URL) BASE_DIR=$(BASE_DIR) LOG_LEVEL=$(LOG_LEVEL) SECRET_KEY=$(SECRET_KEY) local_file_storage

tests: remove build
	docker run local_file_storage python -m pytest ./tests