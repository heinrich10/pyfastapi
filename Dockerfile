FROM python:3.12.1-slim-bullseye

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry:
    POETRY_VERSION=1.7.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PATH="$PATH:/root/.local/bin"

WORKDIR /app

# install poetry
RUN pip install pipx
RUN pipx install "poetry==$POETRY_VERSION"
RUN pipx ensurepath

# install dependencies
COPY ./ ./
RUN poetry install --no-dev --no-root --no-interaction --no-ansi

# copy and run program
CMD [ "poetry", "run", "python", "-m", "run" ]