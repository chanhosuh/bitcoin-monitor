
.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo ""
	@echo "build		build Docker images"
	@echo "up		start Docker containers"
	@echo "down		stop Docker containers"
	@echo "clean		delete stopped containers and dangling images"
	@echo ""

.PHONY: build
build:
	docker build . -t bitcoin-monitor
	@echo "All built 🏛"

.PHONY: bash
bash:
	docker run -it bitcoin-monitor /bin/bash

.PHONY: up
up:
	docker run -d bitcoin-monitor

.PHONY: down
down:
	docker ps | grep bitcoin-monitor | cut -d' ' -f1 | xargs docker stop

.PHONY: clean
clean:
	@echo "Deleting exited containers..."
	docker ps -a -q -f status=exited | xargs docker rm -v
	@echo "Deleting dangling images..."
	docker images -q -f dangling=true | xargs docker rmi
	@echo "All clean 🛀"

