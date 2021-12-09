build:
	docker build -t local_file_storage .

run: build
	docker run --network="host" --name local_file_storage -it -p 8000:8000 local_file_storage

run_daemon: build
	docker run --network="host" --name local_file_storage -itd -p 8081:8081 local_file_storage

remove:
	docker rm -v -f local_file_storage