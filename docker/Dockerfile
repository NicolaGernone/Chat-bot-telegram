FROM python:3.12-alpine

ARG POETRY_HOME=/opt/poetry
ENV PATH="${PATH}:${POETRY_HOME}/bin" \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    APP_DIR=/opt/rocket_bot

ENV PYTHONPATH="${PYTHONPATH}:/opt/rocket_bot"

WORKDIR ${APP_DIR}

COPY poetry.lock pyproject.toml ${APP_DIR}/

RUN apk add --no-cache curl && \
    curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} python3 - && \
    poetry install --no-interaction --no-root

    COPY . ${APP_DIR}/

EXPOSE 5050

CMD ["poetry", "run", "python", "bot/rocket_launch_bot.py"]
