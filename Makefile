PROJECT_NAME=bot
DOCKER_COMPOSE=docker-compose
POETRY_RUN=poetry run
TEST_DIR=tests
LOG_DIR=logs
PYTEST_OPTS=--maxfail=1 --disable-warnings

build:
	$(DOCKER_COMPOSE) build

up: build
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

logs:
	$(DOCKER_COMPOSE) logs -f

run-local:
	$(POETRY_RUN) python bot/rocket_launch_bot.py

install:
	poetry install

update:
	poetry update

test: logs-directory
	$(DOCKER_COMPOSE) run --rm $(PROJECT_NAME) pytest tests

lint:
	$(DOCKER_COMPOSE) run --rm $(PROJECT_NAME) flake8 bot/$(TEST_DIR)

logs-directory:
	@mkdir -p $(LOG_DIR)

clean:
	$(DOCKER_COMPOSE) down -v
	rm -rf $(LOG_DIR)
	@echo "Cleaned up Docker containers and logs."

help:
	@echo "Available commands:"
	@echo "  make build           Build the Docker containers"
	@echo "  make up              Start the Docker containers"
	@echo "  make down            Stop the Docker containers"
	@echo "  make logs            Follow the logs of the Docker containers"
	@echo "  make run-local       Run the bot locally"
	@echo "  make install         Install dependencies with Poetry"
	@echo "  make update          Update dependencies with Poetry"
	@echo "  make test            Create logs directory and run tests with pytest in Docker"
	@echo "  make lint            Run flake8 linter in Docker"
	@echo "  make clean           Stop containers, remove volumes and logs"
	@echo "  make help            Show this help message"

.PHONY: build up down logs run-local install update test lint clean logs-directory help
