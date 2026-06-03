FROM python:3.12.12-slim-bookworm

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1

# Install uv
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copy dependency manifests first for layer caching
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Copy source and install the project itself
COPY . .
RUN uv sync --frozen --no-dev

# For demo purposes, always run migrations then start the app
ENTRYPOINT ["/bin/sh", "-c", "uv run --no-sync alembic upgrade head && uv run --no-sync python -m run"]
