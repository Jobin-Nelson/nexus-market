# Agent AI Coding Assistant Guidelines

This document provides system-specific context, conventions, and operational procedures for agentic coding tools (such as Claude, Cursor, Copilot, etc.) working on the `nexus-market` application codebase. Please reference these instructions when modifying, writing, or debugging code.

## 1. Project Overview & Architecture
- **Language/Framework:** Python 3.14+, Django 6.0+, Django Rest Framework (DRF)
- **Package Manager:** `uv`
- **Task Runner:** `just`
- **Containerization:** `docker compose` (local development via `docker-compose.local.yaml`)
- **Database:** PostgreSQL (managed via docker)

## 2. Environment & Tooling Commands

### Dependencies
- The project environment is locked by `uv.lock` and described in `app/pyproject.toml`.
- Install/Sync dependencies: `uv sync`
- Manage packages: `uv add <package>` or `uv remove <package>`

### Running the Application Locally
- Start local environment (Postgres + Django app container): `just up`
- Stop local environment: `just down`
- Rebuild app image: `just restart`
- The primary Django app container is named `django_app_local`.

### Database & Migrations
- **Generate Migrations:** When changing models, run `uv run manage.py makemigrations` locally (in the `app/` folder) before starting the server.
- **Apply Migrations:** `docker exec -it django_app_local uv run manage.py migrate`
- **Wipe Database & Reseed:** `just remigrate` (This clears the DB volume, deletes all local migration files, runs `makemigrations`, and repopulates the database).
- **Interactive Shell:** Connect to DB using `just attach-psql` or `just attach-lazysql`.

### Linting & Formatting
- **Tooling:** We rely on `ruff` for code linting and formatting.
- Format codebase: `uvx ruff format .` (or `ruff format .` if installed)
- Lint codebase: `uvx ruff check .` (or `ruff check .` if installed)

## 3. Testing Strategies & Commands

The project uses Django's built-in `unittest` test runner. It does **not** use `pytest` by default.

### General Testing Rules
- Always run tests to ensure your changes didn't break existing functionality.
- Write unit tests whenever creating a new feature or fixing a bug.
- Test files reside in the `<app>/tests.py` file or within a `<app>/tests/` directory.
- Execute test commands using Docker to ensure tests interact correctly with the containerized Postgres database.

### Running Tests
- **Run all tests in the project:**
  ```bash
  docker exec -it django_app_local uv run manage.py test
  ```
- **Run tests for a specific app (e.g., `core`):**
  ```bash
  docker exec -it django_app_local uv run manage.py test core
  ```
- **Run a single test case (Test Class):**
  ```bash
  docker exec -it django_app_local uv run manage.py test core.tests.MyModelTest
  ```
- **Run a specific single test method:**
  ```bash
  docker exec -it django_app_local uv run manage.py test core.tests.MyModelTest.test_creation_logic
  ```

## 4. Code Style & Engineering Guidelines

### 4.1 Django Structure & Organization
- Use the standard Django architecture. The core application logic resides in `app/core/` and global configurations in `app/config/`.
- Keep business logic in `models.py` (via custom methods) or specific `services.py` modules. Avoid "fat views" heavily overloaded with logic.
- Rely on explicit model configurations. Do not bypass the Django ORM via raw SQL strings unless absolute performance demands it.

### 4.2 Naming Conventions
- **Files/Modules:** `snake_case.py` (e.g., `models.py`, `views.py`).
- **Classes (Models, Views, Serializers):** `PascalCase` (e.g., `DigitalProduct`, `PhysicalProductViewSet`).
- **Functions, Variables, Methods:** `snake_case` (e.g., `get_user_profile`, `is_active`).
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `MAX_RETRIES`).
- **API URLs:** `snake_case` namespaces, generally pluralized endpoints (e.g., `/api/physicalproducts/`).

### 4.3 Models & ORM
- Model definitions should cleanly represent real-world entities. 
- **Tree Structures:** When working with hierarchical models (e.g., Categories), use `MPTTModel` since `django-mptt` is explicitly installed.
- **String Representations:** Always provide descriptive `__str__` methods for all Django Models for sane Admin rendering.
- **User Relations:** Always use `django.contrib.auth.models.AbstractUser` or `get_user_model()` instead of direct hard-coded relationships to `auth.User`.

### 4.4 APIs & Views
- **REST APIs:** Use Django Rest Framework (DRF) generic viewsets (`viewsets.ModelViewSet`, `generics.*`) or class-based views. Use `routers.DefaultRouter()` inside `urls.py`.
- **Validation:** Do not reinvent validation inside API views; write robust DRF `serializers.ModelSerializer` to handle data validation logic, filtering, and model updates.
- **Template Views:** Standard function-based views (in `core/views.py` like `def index(request):`) are acceptable specifically for standard template rendering logic.
- **Error Handling:** Fail gracefully.
  - Raise DRF `ValidationError` inside serializers or APIs to automatically yield `400 Bad Request`.
  - Use Django's `get_object_or_404()` to fetch model records rather than a raw `.get()` inside view logic, yielding a cleaner 404 response.

### 4.5 Types & Signatures
- Python type hinting (`-> return_type`) is not strictly enforced in legacy or standard Django definitions (like simple `views.py` functions).
- For new helper services or decoupled business logic, include meaningful type hints to improve developer experience (e.g., `def calculate_price(amount: int, multiplier: float) -> int:`).
- You do not need explicit types for Model fields, as Django self-documents them natively.

### 4.6 Imports & Formatting
- **Imports Sorting:** Ensure imports are organized cleanly (alphabetical within their block). Use `isort` via `ruff format`.
  1. Python Standard Library (e.g., `import os`, `import uuid`)
  2. Third-party/Django Packages (e.g., `from django.shortcuts...`, `from rest_framework...`)
  3. Local Application Imports (e.g., `from core.models import Vendor`)
- **No Wildcards:** Never use `from module import *`.
- **Absolute Imports:** Rely on absolute paths (`from core.models import User`) for local files instead of relative pointers if crossing directories.

### 4.7 Security & Environment Variables
- **Secrets Management:** Never hardcode secrets in source files.
- `dotenv` is installed. All secrets, DB keys, and environment toggles should reside in `.env.local` or `.env.prod`.
- `config/settings.py` safely unpacks these using `os.getenv`.
- Never commit actual `.env` files into source control. If you add a new environment variable, document it inside `.env.example`.
