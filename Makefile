
.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo ""
	@echo "build		build Docker images"
	@echo "up		start Docker containers"
	@echo "down		stop Docker containers"
	@echo "bash		Bash shell inside bitcoind container"
	@echo "attach		Attach to bitcoind stdout"
	@echo "clean		delete stopped containers and dangling images"
	@echo ""

.PHONY: build
build:
	docker build . -t bitcoin-monitor
	@echo "All built 🏛"

.PHONY: bash
bash:
	@echo "Dropping into bash inside bitcoind container."
	@docker ps | grep bitcoind | cut -d' ' -f1 | xargs -o -I % docker exec -it % bash

.PHONY: attach
attach:
	@echo "Attaching to bitcoind stdout, ctrl-c to detach."
	@docker ps | grep bitcoind | cut -d' ' -f1 | xargs -o docker attach

.PHONY: up
up:
	docker run -t -d bitcoin-monitor

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

