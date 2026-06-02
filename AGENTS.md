# AGENTS.md

This file contains context for AI coding agents working on the `pyfastapi` project.

## Project Overview

`pyfastapi` is a sample backend API built with **FastAPI**, **SQLAlchemy 2.x**, and **Alembic**. It demonstrates a layered architecture with CRUD endpoints for three related entities: `Person`, `Country`, and `Continent`. The project uses **SQLite** as its database and is intended as a reference implementation for building structured FastAPI applications.

A detailed architectural review is available in `architecture.md` at the repository root. It documents structural gaps, scalability concerns, and a prioritized refactoring roadmap.

## Technology Stack

- **Language**: Python 3.12+ (pinned to `3.12.12` in `.python-version`)
- **Framework**: FastAPI 0.109.x
- **ORM**: SQLAlchemy 2.0.25+
- **Migrations**: Alembic 1.13+
- **Database**: SQLite (file-based, `sql_app.db` for dev, `sql_app_test.db` for tests)
- **Pagination**: `fastapi-pagination` (LimitOffsetPage)
- **Settings**: `pydantic-settings` (pulled transitively via `fastapi[all]`)
- **Functional utilities**: `toolz` (used for currying in repository query builders)
- **Package Manager**: `uv` (lockfile `uv.lock` is present; CI uses `uv sync`)
- **Build backend**: `hatchling`
- **Task Runner**: `poethepoet` (`poe`)
- **Testing**: `pytest`, `faker`, `coverage`
- **Linting**: `flake8`, `mypy` (strict mode)

## Project Structure

```
pyfastapi/
  main.py              # FastAPI app factory, lifespan (startup/shutdown), router registration, pagination setup
  __init__.py          # Exports `app`
  controllers/         # FastAPI APIRouters (HTTP layer)
    person.py
    country.py
    continent.py
  services/            # Business logic and orchestration layer
    person.py
    country.py
    continent.py
  repositories/        # Data access layer
    base.py            # BaseRepository, extract_sort, extract_query helpers
    person.py
    country.py
    continent.py
  models/              # SQLAlchemy declarative models
    base.py            # DeclarativeBase
    person.py
    country.py
    continent.py
  schemas/             # Pydantic models for request/response validation
    base.py            # BaseEnum with MetaEnum
    person.py
    country.py
    continent.py
  libs/
    db.py              # SQLAlchemy engine (lazy), SessionLocal, get_db dependency
    exceptions.py      # DomainError and entity-specific NotFound errors
  utils/
    config.py          # Pydantic Settings, uses ENVIRONMENT env var for .env.test
    logging.py         # Uvicorn log formatter customization

tests/
  conftest.py          # pytest fixtures: init_db (alembic upgrade/downgrade per test), db_session, client, faker locale/seed
  test_main.py         # Basic health check test
  api_tests/           # Integration tests using TestClient
    test_persons.py
    test_countries.py
    test_continents.py
    test_e2e.py        # End-to-end cross-entity flow tests
    util_pagination_helper.py
  unit_tests/
    repositories/test_base.py  # Unit tests for extract_sort and extract_query SQL generation
    services/                  # Unit tests for service layer (mocked repos)
      test_person_service.py
      test_country_service.py
      test_continent_service.py

alembic/
  versions/            # Migration scripts including seed data
  env.py               # Alembic environment, reads DB_HOST from Settings

run.py                 # Application entrypoint: loads config, configures logs, runs uvicorn
architecture.md        # Staff-engineer architectural review and refactoring roadmap
```

## Data Model

```
person
  id (PK)
  last_name
  first_name
  country_code (FK -> countries.code)

country
  code (PK)
  name
  phone
  symbol
  capital
  currency
  continent_code (FK -> continents.code)
  alpha_3

continent
  code (PK)
  name
```

Relationships:
- `Person` → `Country` (many-to-one)
- `Country` → `Continent` (many-to-one)

## Architecture

The code follows a layered architecture:

1. **Controllers** (`controllers/`): FastAPI routers handling HTTP requests/responses. They depend on services via FastAPI's `Depends()`.
2. **Services** (`services/`): Business logic layer. Orchestrates repositories and enforces domain rules. They depend on repositories and the DB session via `Depends()`.
3. **Repositories** (`repositories/`): Encapsulate SQLAlchemy query logic. All inherit from `BaseRepository`, which receives a `Session` via dependency injection. Helper functions `extract_sort` and `extract_query` (curried with `toolz`) build dynamic `SELECT` statements.
4. **Models** (`models/`): SQLAlchemy 2.0 mapped classes using `Mapped` and `mapped_column`.
5. **Schemas** (`schemas/`): Pydantic v2 models. `model_config = {"from_attributes": True}` is used for ORM mode.
6. **Libs** (`libs/`): Database connectivity, session management, and custom exception definitions.

### Dependency Injection

- `get_db()` yields a SQLAlchemy `Session` per request.
- Services and Repositories accept `db: Annotated[Session, Depends(get_db)]` where needed in their constructors.
- Controllers depend on services via `Annotated[SomeService, Depends()]`.
- Services depend on repositories via `Annotated[SomeRepository, Depends()]`.

### Pagination

List endpoints return `LimitOffsetPage[T]` from `fastapi-pagination`. Pagination is added globally via `add_pagination(app)` in `main.py`.

### Logging Initialization

`init_logger()` is called inside the FastAPI `lifespan` context manager at application startup (defined in `pyfastapi/main.py`). This configures a colored `ColourizedFormatter` on the root logger. `run.py` later customizes the uvicorn log config via `configure_log()`. The engine is disposed on shutdown via `get_engine().dispose()`.

## Build and Run Commands

### Local Development

The project uses `uv` for dependency management. A virtual environment (`.venv`) is already present in the repository.

```bash
# Install dependencies
uv sync --locked --all-extras --dev

# Run the application
uv run python run.py
```

The API will be available at `http://localhost:5000`. OpenAPI docs are at `/docs`.

> **Note**: The `README.md` and `Dockerfile` reference `poetry`, but the active package manager in CI and the presence of `uv.lock` indicate `uv` is the current standard. The Dockerfile also references `poetry.lock`, which does not exist in the repo.

### Environment Files

- `.env` — Development configuration (default DB: `sqlite:///./sql_app.db`, port 5000).
- `.env.test` — Test configuration (DB: `sqlite:///./sql_app_test.db`).
- `pyfastapi/utils/config.py` loads `.env.test` when the `ENVIRONMENT` env var is set to `test`, otherwise it loads `.env`. The `tests/conftest.py` unconditionally sets `ENVIRONMENT=test` so tests are always hermetic.
- `pyfastapi/libs/db.py` creates the engine lazily via `get_engine()` on first use.

### Database Migrations

```bash
# Run migrations (creates schema and seed data)
alembic upgrade head

# Downgrade
alembic downgrade base
```

Migrations are not run automatically in local development; you must execute `alembic upgrade head` before seed data is available.

## Testing Instructions

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run poe coverage        # Equivalent to: coverage run -m pytest && coverage report && coverage xml -o coverage.xml
```

### Test Strategy

- **Integration tests** (`tests/api_tests/`): Use `TestClient` against the full FastAPI app. The `init_db` fixture (function-scoped) runs `alembic upgrade head` before each test and `alembic downgrade base` after, ensuring a clean seeded database.
- **End-to-end tests** (`tests/api_tests/test_e2e.py`): Cross-entity flow tests exercising full request/response cycles.
- **Service unit tests** (`tests/unit_tests/services/`): Test service logic in isolation by mocking repositories and the database session.
- **Repository unit tests** (`tests/unit_tests/repositories/`): Test repository helper functions in isolation without a real database (e.g., asserting generated SQL strings).
- **Fixtures**:
  - `init_db`: Resets the database per test function via full Alembic up/down migrations. This guarantees perfect isolation but scales linearly with test count; see `architecture.md` for rationale on keeping this strategy.
  - `db_session`: Yields a properly managed SQLAlchemy `Session` with guaranteed `close()` cleanup.
  - `client`: Session-scoped `TestClient(app)` used as a context manager (triggers lifespan events).
  - `add_50_records`, `add_juan_dela_cruz`: Add specific data for pagination/filter tests.
  - Faker is configured with `faker_session_locale = ["en_US"]` and `faker_seed = 12345`.

> **Integration test hygiene**: Tests that perform write operations (POST, PUT) query the database after the API call to verify persistence, not just the HTTP response.

### Seed Data

The Alembic migration `2b65d99108d5_seed_data.py` inserts:
- 7 continents
- 252 countries
- 13 persons

Tests assert against these exact counts, so modifying seed data will break tests.

## Code Style Guidelines

Lint tasks are defined in `pyproject.toml` under `[tool.poe.tasks]`.

```bash
# Run flake8
uv run poe flake8

# Run mypy (strict)
uv run poe mypy

# Run both
uv run poe lint
```

### flake8 Configuration (`.flake8`)

- `max-line-length = 127`
- `max-complexity = 10`
- `inline-quotes = double`
- Excludes: `venv`, `.venv`, `build`, `dist`, `__pycache__`, `.pytest_cache`, `.mypy_cache`, `*.egg-info`

### mypy Configuration (`pyproject.toml`)

- Runs with `--strict`.
- Excludes standard cache/build directories.

## CI / CD

GitHub Actions workflow (`.github/workflows/python-app.yml`):

- **Trigger**: Push and PR to `main`.
- **Runner**: `ubuntu-22.04`.
- **Steps**:
  1. Checkout code.
  2. Set up Python from `.python-version` (3.12.12).
  3. Install `uv` (version 0.9.18).
  4. `uv sync --locked --all-extras --dev`
  5. `uv run poe lint` (flake8 + mypy)
  6. `uv run poe coverage` (pytest with coverage)
  7. On PRs, uploads coverage report via `orgoro/coverage` using `./coverage.xml`.

## Deployment

A `Dockerfile` is provided with a multi-stage build:

1. **Builder stage** (`python:3.12.1-bookworm`): Installs Poetry and project dependencies.
2. **Runtime stage** (`python:3.12.1-slim-bookworm`): Copies the virtual environment and source code.

**Entrypoint**: `alembic upgrade head && python -m run`

> **Note**: The Dockerfile currently uses Poetry for installation and references `poetry.lock`, but the repo only contains `uv.lock`. If switching fully to `uv`, the Dockerfile should be updated accordingly.

## Security Considerations

- The application uses SQLite with local files. No network database credentials are required.
- `check_same_thread=False` is set on the SQLite engine to allow usage across FastAPI's async workers.
- No authentication or authorization layer is implemented; this is a sample/demo project.
- Input validation is handled by Pydantic schemas in controllers.
- Global exception handling is implemented in `main.py` for `DomainError` subclasses, providing clean error responses and preventing internal detail leakage.

## Conventions

- **Imports**: Use `TYPE_CHECKING` guards for model relationship imports to avoid circular imports.
- **String quoting**: Double quotes preferred (enforced by `flake8-quotes`).
- **Sort syntax**: API list endpoints accept a `sort` query parameter. Prefix with `-` for descending (e.g., `-name`), `+` or no prefix for ascending.
- **Filter syntax**: Query parameters on list endpoints are mapped to schema fields. String fields listed in `use_like_list` use `ILIKE` (`%value%`); others use exact equality.
- **Logging**: `init_logger()` must run before the app starts. It configures colored uvicorn-style formatters. Log level is toggled in `utils/logging.py`.
- **Schema naming**: `*Schema` for responses, `*ListSchema` for paginated/list items, `Query*Schema` for filters, `Sort*Enum` for sortable fields.
- **Repository patterns**: `BaseRepository` inherits from `ABC` but defines no abstract methods. Repositories use `flush()` / `execute()`; transaction boundaries (`commit()`) are managed at the Service layer.
- **Trailing slashes**: Collection list endpoints are registered without a trailing slash (e.g., `/persons`, `/countries`, `/continents`). FastAPI's default `redirect_slashes` behavior will redirect the slash variant (`/persons/`) to the canonical path with a `307`.
- **Lifespan**: `pyfastapi/main.py` defines an `asynccontextmanager` lifespan that runs `init_logger()` on startup and `get_engine().dispose()` on shutdown.
