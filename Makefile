PROJECT_NAME=rocket_launch_bot
DOCKER_COMPOSE=docker-compose
POETRY_RUN=poetry run

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
