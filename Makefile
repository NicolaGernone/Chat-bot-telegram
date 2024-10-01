PROJECT_NAME=rocket_launch_bot
DOCKER_COMPOSE=docker-compose
POETRY_RUN=poetry run
TEST_DIR=tests
LOG_DIR=logs

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

logs:
	$(DOCKER_COMPOSE) logs -f

run-local:
	$(POETRY_RUN) python rocket_launch_bot.py

install:
	poetry install

update:
	poetry update

test: logs-directory
	$(POETRY_RUN) python -m unittest discover $(TEST_DIR)

help:
	@echo "Available commands:"
	@echo "  make build           Build the Docker containers"
	@echo "  make up              Start the Docker containers"
	@echo "  make down            Stop the Docker containers"
	@echo "  make logs            Follow the logs of the Docker containers"
	@echo "  make run-local       Run the bot locally"
	@echo "  make install         Install dependencies with Poetry"
	@echo "  make update          Update dependencies with Poetry"
	@echo "  make test            Create logs directory and run unit tests"
	@echo "  make help            Show this help message"

.PHONY: build up down logs run-local install update test logs-directory help