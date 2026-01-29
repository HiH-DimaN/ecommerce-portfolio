# AGENTS.md — case-2-education

## Project Overview

AI-автоматизация онлайн-школы английского: FastAPI backend + Vue.js frontend + PostgreSQL.

```
case-2-education/
├── backend/          # Python 3.12, FastAPI, SQLAlchemy async
├── frontend/         # Vue 3, TypeScript, Vite, TailwindCSS
├── docker/           # Docker Compose (local dev)
├── ARCHITECTURE.md   # Full architecture & API design
├── DATABASE.md       # DB schema reference
└── PRD.md            # Product requirements
```

## Build / Lint / Test Commands

### Backend (working directory: `backend/`)

```bash
pip install -e ".[dev]"

# Dev server
granian --interface asgi --reload app.main:app

# Lint & type-check
ruff check .
ruff format --check .
mypy app

# Format
ruff format .

# Test — all
pytest -v

# Test — single file
pytest tests/test_chat.py -v

# Test — single test function
pytest tests/test_chat.py::test_send_message -v

# Test — with coverage
pytest --cov=app --cov-report=html

# Database
alembic upgrade head                          # apply migrations
alembic revision --autogenerate -m "desc"     # generate migration
python -m app.db.seed                         # seed demo data
```

### Frontend (working directory: `frontend/`)

```bash
npm install
npm run dev           # Vite dev server
npm run build         # production build
npm run lint          # ESLint
npm run type-check    # vue-tsc
npm run format        # Prettier
```

### Docker (working directory: `docker/`)

```bash
docker compose up -d                    # start all services
docker compose down                     # stop
docker compose logs -f backend          # logs
```

## Code Style — Python

### Tooling
- **Ruff** — linter + formatter, line-length 100, target py312
- **mypy** — strict mode, disallow_untyped_defs
- Rule sets: E, W, F, I, B, C4, UP, ARG, SIM
- Ignored: E501, B008, B904

### Imports (Ruff isort, first-party = `app`)
```python
import uuid
from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDMixin
```

### Types
- `str | None` not `Optional[str]`; `list[str]` not `List[str]` (Python 3.12)
- `Mapped[T]` for SQLAlchemy columns, never raw `Column()`
- Pydantic v2 field types directly
- Settings via `pydantic_settings.BaseSettings` in `app/config.py`

### Naming
- Classes: `PascalCase` — `StudentProgress`, `ChatMessage`
- Functions: `snake_case` — `get_ai_response`, `validate_init_data`
- Constants: `UPPER_SNAKE` — `SYSTEM_PROMPT`, `MAX_HISTORY`
- Enums: `class StudentStatus(str, Enum)` with UPPER values
- DB tables: `snake_case` plural — `students`, `chat_messages`
- Files: `snake_case` matching primary class — `student.py` → `Student`

### SQLAlchemy Patterns
- Declarative base + mixins: `class Model(Base, UUIDMixin, TimestampMixin)`
- UUID primary keys via `UUIDMixin`, timestamps via `TimestampMixin`
- Async only: `AsyncSession`, `asyncpg` driver
- Relationships: `Mapped["Foo"]` with string forward refs

### Error Handling
- Never bare `except:` — always specific exceptions
- FastAPI: `raise HTTPException(status_code=..., detail=...)`
- Service layer: return `None` on failure, caller decides
- Logging: `logger.error(...)`, never `print()`

### Configuration
- All env vars in `app/config.py` (`pydantic_settings.BaseSettings`)
- Access: `settings.DATABASE_URL` (module-level singleton)
- Secrets never hardcoded — env vars with safe dev defaults

### Auth
- Telegram Mini App `initData` → HMAC-SHA256 validation
- JWT via `python-jose` — payload: `sub` (telegram_id), `role`

## Code Style — Frontend (Vue / TypeScript)

- Vue 3 Composition API: `<script setup lang="ts">`
- TypeScript strict mode
- TailwindCSS utility classes
- Pinia for state management
- Axios with auth interceptor (`api/client.ts`)
- Lucide Vue for icons
- Chart.js for data visualization

## Git Conventions

- Branch: `main` (direct push)
- Commits: imperative English — `Add student dashboard API`
- No secrets in commits — `.env` files only

## Database & Migrations

- PostgreSQL 16 + pgvector extension
- Alembic async migrations in `app/db/migrations/versions/`
- Naming: `001_initial.py`, `002_add_xyz.py`
- Always include reversible `downgrade()`
- Directus (port 8055) as admin panel for DB browsing

## Docker Services (local dev)

| Service | Image | Port |
|---------|-------|------|
| Backend | Dockerfile (Granian) | 8000 |
| Frontend | Dockerfile (Nginx) | 3000 |
| PostgreSQL | pgvector/pgvector:pg16 | 5432 |
| Redis | redis:7-alpine | 6379 |
| Directus | directus/directus:11 | 8055 |
| MinIO | minio/minio | 9000, 9001 |

## Key Files

| Purpose | Path |
|---------|------|
| App config | `backend/app/config.py` |
| DB session | `backend/app/db/session.py` |
| All models | `backend/app/models/__init__.py` |
| Base + mixins | `backend/app/models/base.py` |
| Migrations | `backend/app/db/migrations/versions/` |
| Seed data | `backend/app/db/seed.py` |
| Ruff/mypy/pytest config | `backend/pyproject.toml` |
| Architecture | `ARCHITECTURE.md` |
| PRD | `PRD.md` |
| DB schema | `ARCHITECTURE.md` (section 2) |
