# ANSI escape codes
BOLD := \033[1m
RESET := \033[0m
REVERSE := \033[7m
RED := \033[0;31m

.DEFAULT_GOAL := help

include ../docker-bitcoin/bitcoind/bitcoin.conf

SHELL := bash

.PHONY: help
help:
	@echo ""
	@echo "OPERATE:"
	@echo "build                    Build images"
	@echo "up                       Start all containers"
	@echo "down                     Stop all containers"
	@echo "restart                  Stop then start containers"
	@echo "rebuild                  Stop, build, then start containers"
	@echo ""
	@echo "DEBUGGING:"
	@echo "logs                     Re-attach to running container logs"
	@echo "log                      Re-attach to specified running container log"
	@echo "ps                       List running container info"
	@echo "bash                     Bash inside a container (default=django)"
	@echo "ipython                  Interactive console inside django container"
	@echo "status                   Blockchain status info from bitcoind"
	@echo ""
	@echo "TEST:"
	@echo "test                     Run python unit tests"
	@echo "coverage                 Run test coverage report"
	@echo "lint                     Linting checks through flake8 and pylint"
	@echo "flake8                   Lint using flake8"
	@echo "pylint                   Lint using pylint"
	@echo ""
	@echo "DATA:"
	@echo "nuke_db                  Delete Postgres data"
	@echo "nuke_blockchain          Delete blockchain data"
	@echo "clear_redis              Delete all the keys in Redis"
	@echo ""
	@echo "MAINTENANCE:"
	@echo "clean                    Remove dangling images and exited containers"
	@echo "requirements             Generate requirements.txt from requirements_base.txt"
	@echo "hooks                    Install Git hooks"
	@echo "clear_logs               Truncate Docker logs"
	@echo ""
	@echo "APPLICATION:"
	@echo "process_blockchain       Run 'process_blockchain' Django management command"
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
	@if test -z $(name); then\
	    echo "bash in django container:";\
	    docker-compose exec django bash;\
	else\
	    echo "bash in $(name) container:";\
	    docker-compose exec $(name) bash;\
	fi

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
	    --rpcuser=$(rpcuser) \
	    --rpcpassword=$(rpcpassword) \
	    getblockchaininfo\
	"

.PHONY: nuke_blockchain
nuke_blockchain:
	@read -r -p "WARNING: this will delete all blockchain data (ctrl-c to exit / any other key to continue)." input
	@make down
	@docker-compose rm --force --stop -v bitcoind
	@docker volume rm bitcoin-monitor_bitcoin-data
	@echo "Bitcoin blockchain deleted 💣"

.PHONY: nuke_db
nuke_db:
	@read -r -p "WARNING: this will delete all data from Postgres (ctrl-c to exit / any other key to continue)." input
	@make down
	@docker-compose rm --force --stop -v db
	@docker volume rm bitcoin-monitor_db-data
	@echo "Postgres data deleted 💣"

.PHONY: clear_redis
clear_redis:
	@read -r -p "WARNING: this will clear all Redis data (ctrl-C to exit / any other key to continue)." input
	@docker-compose rm --force --stop -v redis
	@docker-compose up -d redis

.PHONY: test
test:
	docker-compose up -d
	@echo "Starting django tests..."
	docker-compose exec django  sh -c "manage.py test --noinput"
	@echo "Tests passed 🏁"

.PHONY: coverage
coverage:
	-docker-compose exec django coverage run manage.py test
	docker-compose exec django coverage report
	docker-compose exec django coverage html
	@echo "test coverage report complete 📊"
	@docker cp "$(shell docker ps | grep 'loanstreet-rebuild_django' | cut -d ' ' -f1)":/code/htmlcov /tmp
	@python -m webbrowser "file:///tmp/htmlcov/index.html"

# https://stackoverflow.com/a/51866793/1175053
.PHONY: clear_logs
clear_logs:
	docker run -it --rm --privileged --pid=host alpine:latest nsenter -t 1 -m -u -n -i -- sh -c 'truncate -s0 /var/lib/docker/containers/*/*-json.log'

.PHONY: lint
lint:
	@echo ""
	@echo "make flake8 => make pylint"
	@echo ""
	@make flake8
	@echo ""
	@make pylint
	@echo ""
	@echo "Linting checks passed 🏆"

.PHONY: flake8
flake8:
	@echo "$(REVERSE)Running$(RESET) $(BOLD)flake8$(RESET)..."
	@if ! flake8 ; then \
	    echo "$(BOLD)flake8$(RESET): $(RED)FAILED$(RESET) checks" ;\
	    exit 1 ;\
	fi
	@echo "flake8 passed 🍄"

.PHONY: pylint
pylint:
	@echo "$(REVERSE)Running$(RESET) $(BOLD)pylint$(RESET)..."
	@echo ""
	@travis/check_pylint_score.py
	@echo ""
	@echo "pylint passed ⚙️"

.PHONY: hooks
hooks:
	@echo "Installing git hooks..."
	cp ./hooks/{commit-msg,pre-commit*} .git/hooks/
	@echo "Hooks installed"

.PHONY: requirements
requirements:
	@if [ -z ${VIRTUAL_ENV} ]; then \
    	    echo "Must be in virtual environment first"; \
    	    exit 1; \
	fi
	@echo "Generating requirements.txt from core dependencies in requirements_base.txt ..."
	pip install virtualenvwrapper && \
	source virtualenvwrapper.sh && \
	wipeenv && \
    	pip install -r django/requirements_base.txt && \
    	echo '# generated via "make requirements"' > django/requirements.txt && \
    	pip freeze -r django/requirements_base.txt >> django/requirements.txt
	@echo "requirements.txt has been updated 🍉"

.PHONY: ps
ps:
	docker-compose ps

.PHONY: process_blockchain
process_blockchain:
	docker-compose exec --detach django bash -c "manage.py process_blockchain"

