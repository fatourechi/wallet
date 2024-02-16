.PHONY: help build up down clean build-no-cache restart

help:
	@echo "Usage: make <target>"
	@echo "Available targets:"
	@echo "  build           Build Docker images"
	@echo "  up              Start Docker containers"
	@echo "  down            Stop Docker containers"
	@echo "  clean           Remove Docker containers and images"
	@echo "  build-no-cache  Build Docker images without cache"
	@echo "  restart         Restart Docker containers"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

clean:
	docker-compose down --rmi all -v

build-no-cache:
	docker-compose build --no-cache

restart: down up

logs:
	docker-compose logs -f