

.PHONY: run down build

run:
	docker-compose up

down:
	docker-compose down

build:
	docker-compose up --build
