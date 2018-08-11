
.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo ""
	@echo "OPERATE:"
	@echo "up		Start Docker containers"
	@echo "down		Stop Docker containers"
	@echo "restart		Stop then start Docker containers"
	@echo "build		Build Docker images"
	@echo "rebuild		Stop, build, then start Docker containers"
	@echo ""
	@echo "DEBUGGING:"
	@echo "logs		Re-attach to logging output"
	@echo "bash		Bash shell inside bitcoind container"
	@echo "ipython		Interactive console inside django container"
	@echo "status	        Blockchain status info from bitcoind"
	@echo ""
	@echo "MAINTENANCE:"
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

.PHONY: log
log:
	@if test -z $(name); then\
	    echo "";\
	    echo "Please enter a container name as argument.";\
	    echo "";\
	    echo " e.g. 'make log name=bitcoind'";\
	    echo "";\
	    echo "or use 'make logs' to attach to all container logs.";\
	    echo "";\
	    echo "Available container names are:";\
	    echo "  bitcoind";\
	    echo "  django";\
	    echo "  db";\
	else\
	  docker-compose logs -f $(name);\
	fi

.PHONY: bash
bash:
	@echo "Dropping into bash inside bitcoind container."
	@docker-compose exec bitcoind bash

.PHONY: ipython
ipython:
	docker-compose exec django /code/manage.py shell_plus --ipython

.PHONY: clean
clean:
	@echo "Deleting exited containers..."
	docker ps -a -q -f status=exited | xargs docker rm -v
	@echo "Deleting dangling images..."
	docker images -q -f dangling=true | xargs docker rmi
	@echo "All clean 🛀"

.PHONY: status
status:
	@docker-compose exec bitcoind bash -c "\
	    bitcoin-cli \
	    -rpcuser=user \
	    -rpcpassword=password \
	    getblockchaininfo\
	"


