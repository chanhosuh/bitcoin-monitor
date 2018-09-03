
.DEFAULT_GOAL := help

TODAY := $(shell date -u +%Y%m%d)

.PHONY: help
help:
	@echo ""
	@echo "OPERATE:"
	@echo "up                Start containers"
	@echo "down              Stop containers"
	@echo "restart           Stop then start containers"
	@echo "build             Build images"
	@echo "rebuild           Stop, build, then start containers"
	@echo ""
	@echo "DEBUGGING:"
	@echo "logs              Re-attach to all logging output"
	@echo "log               Re-attach to specified container log"
	@echo "bash              Bash inside a container (default=django)"
	@echo "ipython           Interactive console inside django container"
	@echo "status            Blockchain status info from bitcoind"
	@echo ""
	@echo "TEST:"
	@echo "test              Execute tests on running containers"
	@echo "coverage          Run test coverage analysis and generate html report"
	@echo "lint              Linting checks through flake8"
	@echo ""
	@echo "DATA:"
	@echo "nuke_db           Delete Postgres and Redis data"
	@echo "clear_redis       Delete all the keys in Redis"
	@echo ""
	@echo "MAINTENANCE:"
	@echo "clean		     Delete stopped containers and dangling images"
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
	    -rpcuser=user \
	    -rpcpassword=password \
	    getblockchaininfo\
	"

.PHONY: nuke_db
nuke_db:
	@read -r -p "WARNING: this will delete all data from Postgres and Redis (ctrl-c to exit / any other key to continue)." input
	@make down
	@docker-compose rm --force --stop -v redis
	@docker-compose rm --force --stop -v db
	@docker volume rm loanstreet-rebuild_db-data
	@echo "Postgres and Redis data deleted 💣"

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

.PHONY: lint
lint:
	@echo "flake8 django"
	@if ! flake8 django; then \
	    echo "flake8: \033[00;31mFAILED\033[0m checks" ;\
	    exit 1 ;\
	fi
	@echo "flake8 passed 🥇"

.PHONY: coverage
coverage:
	-docker-compose exec django coverage run manage.py test
	docker-compose exec django coverage report
	docker-compose exec django coverage html
	@echo "test coverage report complete 📊"
	@docker cp "$(shell docker ps | grep 'loanstreet-rebuild_django' | cut -d ' ' -f1)":/code/htmlcov /tmp
	@python -m webbrowser "file:///tmp/htmlcov/index.html"
