# CareerMate Backend

This directory contains the FastAPI backend for the CareerMate platform.

## Overview

The backend is built around a modular monolith structure with clear separation between:

- API routes
- business services
- database models
- schemas
- authentication and security
- storage and resume handling

## Stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic v2
- JWT auth
- pytest

## Project structure

```text
backend/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── alembic/
├── storage/
├── tests/
├── .env.example
├── alembic.ini
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.11+
- PostgreSQL running locally or in Docker
- pip
- virtual environment support

## Setup

From the `backend` folder:

```bash
python -m venv .venv

# Windows
.\.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
```

### Environment configuration

Update `.env` to match your local environment if needed. The default config expects PostgreSQL on `localhost:5432` with the database name `careermate_db`.

Key values include:

- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `ENVIRONMENT`
- `DEBUG`
- `CORS_ORIGINS`

## Database

The project includes Docker Compose support for PostgreSQL. From the project root:

```bash
docker compose up -d postgres
```

This creates the `careermate_db` database and starts a local PostgreSQL container.

## Run the API

```bash
# Windows
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:

- http://localhost:8000
- http://localhost:8000/api/v1/docs

## Tests

```bash
pytest -q
```

Or target specific areas:

```bash
pytest tests/test_auth_login.py -q
pytest tests/test_profile.py -q
```

## Useful endpoints

The app exposes a root metadata endpoint and health check:

- `/`
- `/health`
- `/api/v1/docs`

## Notes

- `app.core.config.Settings` loads environment values from `.env`.
- `app.main.create_app()` registers the API router and global exception handlers.
- Startup validates the database connection and logs connection health.

## Production guidance

For production, update the following before deployment:

- `JWT_SECRET_KEY`
- `ENVIRONMENT=production`
- `COOKIE_SECURE=True`
- database credentials and connection settings
- CORS origins for the real frontend domain
