FROM python:3.12-alpine

ARG POETRY_HOME=/opt/poetry

ENV PATH="${PATH}:${POETRY_HOME}/bin"                                                               \
    PYTHONUNBUFFERED=1                                                                              \
    POETRY_VIRTUALENVS_CREATE=false                                                                 \
    APP_DIR=/opt/bot

WORKDIR ${APP_DIR}

COPY poetry.lock                    ${APP_DIR}/poetry.lock
COPY pyproject.toml                 ${APP_DIR}/pyproject.toml
COPY bot/                          ${APP_DIR}/bot/

RUN apk add --update --no-cache                                                                     \
    curl                                                                                            \
    build-base                                                                                      \
    libffi-dev                                                                                      

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} python3 -           && \
    poetry config virtualenvs.create false                                                       && \
    poetry install --no-interaction

EXPOSE 5050

CMD ["poetry", "run", "python", "bot/rocket_launch_bot.py"]
