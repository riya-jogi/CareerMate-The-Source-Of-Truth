# CareerMate

CareerMate is a full-stack application for AI-assisted career profile management, resume analysis, job matching, and ATS optimization. The platform keeps a verified career source of truth and uses it to power candidate profile management, claims validation, resume uploads, and job-fit analysis.

## Project overview

- Backend: FastAPI + SQLAlchemy + PostgreSQL + Alembic
- Frontend: React + TypeScript + Vite + Tailwind
- Database: PostgreSQL with pgvector support
- Auth: JWT-based authentication with refresh tokens
- Core workflows: user auth, profile management, claims/evidence, resumes, jobs, matching, and candidate optimization

## Repository structure

```text
CareerMate-The-Source-Of-Truth/
├── backend/
│   ├── app/
│   ├── alembic/
│   ├── storage/
│   ├── tests/
│   ├── .env.example
│   ├── requirements.txt
│   ├── alembic.ini
│   └── README.md
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── README.md
├── docker-compose.yml
├── project docs/
├── Backend.md
├── README.md
└── .gitignore
```

## Tech stack

### Backend
- Python 3.11+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic v2
- JWT auth and cookie-based refresh tokens

### Frontend
- React 19
- TypeScript
- Vite
- Tailwind CSS
- React Router

## Prerequisites

Before you begin, make sure you have installed:

- Python 3.11+
- Node.js 18+
- npm or pnpm
- Docker Desktop or Docker Engine
- Git

## Quick start

### 1. Clone the repository

```bash
git clone <repo-url>
cd CareerMate-The-Source-Of-Truth
```

### 2. Start PostgreSQL

```bash
docker compose up -d postgres
```

### 3. Set up the backend

```bash
cd backend
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
```

Then review and adjust environment variables in `backend/.env` as needed.

Start the API:

```bash
# Windows
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API should be available at:

- http://localhost:8000
- Swagger UI: http://localhost:8000/api/v1/docs

### 4. Set up the frontend

```bash
cd ../frontend
npm install
npm run dev
```

The frontend will typically run at:

- http://localhost:5173

## Environment notes

The backend loads settings from `backend/.env` using the config defined in `backend/app/core/config.py`.

Default local development settings assume:

- PostgreSQL at `localhost:5432`
- Database name: `careermate_db`
- Default local credentials: `postgres` / `Postgres@123`
- Frontend origin: `http://localhost:5173`

## Useful commands

### Backend

```bash
cd backend
.\.venv\Scripts\activate
pytest -q
python -m uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
npm run build
npm run lint
```

## Common workflows

- Register and log in as a user
- Create or edit a career profile
- Add verified claims and supporting evidence
- Upload resume files and review extracted content
- Analyze jobs and requirements
- Generate matches and optimization recommendations

## Documentation

- Project docs are stored in the `project docs/` folder.
- Backend architecture notes are in `Backend.md`.
- See the sub-project README files for deeper setup and usage details.

## Status

This project is under active development and is structured for iterative feature expansion.

---

For more detailed backend instructions, see [backend/README.md](backend/README.md).
For more detailed frontend instructions, see [frontend/README.md](frontend/README.md).
