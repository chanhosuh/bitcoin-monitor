
.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo ""
	@echo "build		build Docker images"
	@echo "up		start Docker containers"
	@echo "down		stop Docker containers"
	@echo "logs		Re-attach to logging output"
	@echo "bash		Bash shell inside bitcoind container"
	@echo "clean		delete stopped containers and dangling images"
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

