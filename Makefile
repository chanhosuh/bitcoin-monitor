
.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo ""
	@echo "build		Build Docker images"
	@echo "up		Start Docker containers"
	@echo "down		Stop Docker containers"
	@echo "restart		Stop then start Docker containers"
	@echo "rebuild		Stop, build, then start Docker containers"
	@echo "logs		Re-attach to logging output"
	@echo "bash		Bash shell inside bitcoind container"
	@echo "clean		Delete stopped containers and dangling images"
	@echo ""

.PHONY: build
build:
	docker-compose build
	@echo "All built 🏛"

.PHONY: up
up:
	docker-compose up -d
	@make logs

.PHONY: down
down:
	docker-compose stop

.PHONY: restart
restart:
	@echo "make down ==> make up"
	@make down
	@make up

.PHONY: rebuild
rebuild:
	@echo "make down ==> make build ==> make up"
	@make down
	@make build
	@make up

.PHONY: logs
logs:
	docker-compose logs -f

.PHONY: bash
bash:
	@echo "Dropping into bash inside bitcoind container."
	@docker-compose exec bitcoind bash

.PHONY: clean
clean:
	@echo "Deleting exited containers..."
	docker ps -a -q -f status=exited | xargs docker rm -v
	@echo "Deleting dangling images..."
	docker images -q -f dangling=true | xargs docker rmi
	@echo "All clean 🛀"

