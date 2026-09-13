# Project Inspection & Module 1 Implementation Plan: User Authentication & Dashboard

## Executive Summary

The project **CareerMate-The-Source-Of-Truth** is an AI-powered, candidate-controlled ATS and resume optimization platform.
Its core architectural tenet is:
> **The candidate's verified career information is the source of truth.** AI-generated resume content must never become the source of truth, and every generated claim must be traceable to candidate evidence. The LLM proposes; deterministic rules validate; the candidate decides.

---

## 1. Project Inspection Findings

### 1.1 Complete Existing Project Structure
The workspace at `d:\CareerMate-The-Source-Of-Truth` is an initialized Git repository with:
- `.git/` (Branch `main`, initial commit `d0b7e0b` by riya-jogi)
- `.gitignore` (Standard Python/Node/IDE ignore rules)
- `AI_Candidate_ATS_Resume_Optimization_Master_Reference.docx` (430-paragraph master reference specifying architecture, requirements, entity models, API surface, and roadmap through Step 11)
- `AIp1-mindmap.png` (Mindmap Phase 1: Workflow, trust architecture, data models)
- `AIp2-mindmap.png` (Mindmap Phase 2: Requirements, matching, truth validator, roadmap)

**Current Codebase State:**
There is **no existing backend or frontend code, no Docker configuration, and no database models or migrations** committed yet. The repository contains architectural blueprints and specifications, making this the foundational implementation stage.

### 1.2 System Environment & Tooling Audit
- **Python**: Python 3.14.7 (Default) and Python 3.13 (via `py -V:3.13`).
  - *Recommendation*: Use Python 3.13 or 3.14 for the virtual environment (`.venv`), ensuring all required packages (SQLAlchemy, FastAPI, Pydantic v2, Passlib/Bcrypt, PyJWT, psycopg/asyncpg) have compatible wheels.
- **Node.js**: v22.18.0 & npm 10.9.3 (Ready for Vite + React + TypeScript + Tailwind CSS).
- **PostgreSQL**: PostgreSQL 18.6 is installed and currently running as an active Windows service (`postgresql-x64-18`) on default port 5432.
- **Docker**: Docker CLI is currently not in PATH or not installed on this system.
  - *Strategy*: We will provide a standard `docker-compose.yml` for containerized setups (with PostgreSQL + pgvector), while natively supporting the local running PostgreSQL 18 service via `.env`.
- **Ollama**: Installed (v0.34.0) with model `qwen2:7b` present locally (for future AI extraction and matching modules).

---

## 2. Architecture & Design Alignment

### 2.1 Backend Architecture (FastAPI Modular Monolith)
The backend will be structured under `backend/` as follows:
```
backend/
├── app/
│   ├── api/
│   │   ├── deps.py             # Dependency injection: get_db, get_current_user
│   │   └── v1/
│   │       ├── router.py       # Aggregator for v1 routers
│   │       ├── auth.py         # /register, /login, /me
│   │       ├── dashboard.py    # /summary
│   │       └── profile.py      # /profile (source of truth profile)
│   ├── core/
│   │   ├── config.py           # Pydantic Settings (.env configuration)
│   │   └── security.py         # Password hashing (bcrypt) & JWT handling
│   ├── db/
│   │   ├── base.py             # Base declarative class importing all models
│   │   └── session.py          # SQLAlchemy engine & sessionmaker
│   ├── models/
│   │   ├── user.py             # User model
│   │   └── profile.py          # CareerProfile model (1-to-1 with User)
│   ├── schemas/
│   │   ├── auth.py             # UserRegister, UserLogin, Token, TokenPayload
│   │   ├── user.py             # UserRead, UserUpdate
│   │   ├── profile.py          # CareerProfileRead, CareerProfileUpdate
│   │   └── dashboard.py        # DashboardSummary response schema
│   ├── services/
│   │   ├── auth_service.py     # Auth business logic
│   │   ├── user_service.py     # User lifecycle & automatic profile creation
│   │   └── dashboard_service.py# Dashboard statistics aggregation
│   └── main.py                 # FastAPI application factory & CORS setup
├── alembic/                    # Database migrations
│   ├── env.py
│   └── versions/
├── requirements.txt
└── .env.example
```

### 2.2 Frontend Architecture (React + TypeScript + Vite + Tailwind CSS)
The frontend will be structured under `frontend/` as follows:
```
frontend/
├── src/
│   ├── api/
│   │   ├── client.ts           # Axios / Fetch client with Bearer token interceptor
│   │   └── auth.ts             # Auth & Dashboard API service calls
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Navbar.tsx      # Top bar with candidate status & user menu
│   │   │   ├── Sidebar.tsx     # Navigation (Dashboard, Career Profile, Resumes, Jobs)
│   │   │   └── Layout.tsx      # Main authenticated app layout wrapper
│   │   ├── common/
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Badge.tsx
│   │   │   └── SourceOfTruthBadge.tsx  # Highlights verified source-of-truth status
│   │   └── dashboard/
│   │       ├── StatCard.tsx            # Key metrics (claims count, verified stats)
│   │       ├── ProfileProgressCard.tsx # Career profile completion progress
│   │       └── QuickActionsCard.tsx    # Direct jump to Resume Upload or JD Match
│   ├── context/
│   │   └── AuthContext.tsx     # Auth state provider (login, logout, user info)
│   ├── pages/
│   │   ├── Login.tsx           # Login view with validation
│   │   ├── Register.tsx        # Registration view with validation
│   │   ├── Dashboard.tsx       # Core candidate dashboard
│   │   └── Profile.tsx         # Career Profile preview & basic editing
│   ├── types/
│   │   └── index.ts            # TypeScript interfaces matching backend schemas
│   ├── App.tsx                 # React Router with PublicRoute and ProtectedRoute
│   ├── index.css               # Tailwind CSS & custom design tokens
│   └── main.tsx
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

---

## 3. Database Specification for Module 1

Aligned with the Master Reference Section 11 & 12:

### `users` Table
- `id`: UUID (Primary Key, default uuid4)
- `email`: VARCHAR(255), Unique, Indexed, Not Null
- `hashed_password`: VARCHAR(255), Not Null
- `full_name`: VARCHAR(255), Not Null
- `is_active`: BOOLEAN, Default True
- `is_verified`: BOOLEAN, Default False
- `created_at`: TIMESTAMP WITH TIME ZONE, Default UTC NOW
- `updated_at`: TIMESTAMP WITH TIME ZONE, Default UTC NOW

### `career_profiles` Table (Candidate's Source of Truth)
- `id`: UUID (Primary Key, default uuid4)
- `user_id`: UUID, Unique, Foreign Key -> `users.id` (ON DELETE CASCADE)
- `headline`: VARCHAR(255), Nullable (e.g. "Full Stack Engineer | Python & React")
- `summary`: TEXT, Nullable
- `phone`: VARCHAR(50), Nullable
- `location`: VARCHAR(100), Nullable
- `linkedin_url`: VARCHAR(255), Nullable
- `github_url`: VARCHAR(255), Nullable
- `portfolio_url`: VARCHAR(255), Nullable
- `created_at`: TIMESTAMP WITH TIME ZONE, Default UTC NOW
- `updated_at`: TIMESTAMP WITH TIME ZONE, Default UTC NOW

*Note: In accordance with Rule 1 of the Master Reference, when a user registers, their initial empty `career_profile` record is created automatically so their career profile is always the anchor for future claims, experiences, and resumes.*

---

## 4. API Endpoints for Module 1

| Method | Path | Description | Access |
|---|---|---|---|
| `POST` | `/api/v1/auth/register` | Register new user + automatically create Career Profile | Public |
| `POST` | `/api/v1/auth/login` | Authenticate with email & password, return JWT token | Public |
| `GET` | `/api/v1/auth/me` | Fetch authenticated user profile & verification status | Protected |
| `GET` | `/api/v1/dashboard/summary`| Metrics: profile completion, claims count, resumes, jobs | Protected |
| `GET` | `/api/v1/profile` | Get the authenticated user's Career Profile | Protected |
| `PUT` | `/api/v1/profile` | Update basic Career Profile details | Protected |

---

## 5. Potential Conflicts & Mitigations

1. **Docker Availability on Host**:
   - *Conflict*: The user requested Docker for local infrastructure, but Docker is not currently available in the Windows environment PATH.
   - *Mitigation*: We will create a robust `docker-compose.yml` for containerized environments, and simultaneously configure the application so it can connect directly to the locally running PostgreSQL 18 service on port 5432 with `.env` settings (`DATABASE_URL`).

2. **Python 3.14 Compatibility with Older C-Extension Wheels**:
   - *Conflict*: Python 3.14 is very new, and binary wheels for certain libraries (`asyncpg`, `bcrypt`) might need compilation or specific versions.
   - *Mitigation*: We will use modern pure-Python or pre-compiled packages (`pyjwt[crypto]`, standard `bcrypt` / `argon2-cffi`, `psycopg3` or `psycopg2-binary`, `SQLAlchemy 2.0+`), or create the virtual environment targeting Python 3.13 if Python 3.14 encounters missing binary wheels.

3. **Source of Truth Principle Integrity**:
   - *Conflict*: Risk of conflating auth user account data with career profile data.
   - *Mitigation*: We will strictly separate `users` (credentials, auth, status) and `career_profiles` (career data, anchor for claims & evidence), linked by a 1-to-1 relationship with unique `user_id`.

---

## 6. Implementation Steps for Module 1

### Phase 1: Backend Foundation & Database
1. Initialize `backend/` structure, create `pyproject.toml` / `requirements.txt` with FastAPI, Uvicorn, SQLAlchemy 2.0, Alembic, Pydantic v2, PyJWT, Passlib/Bcrypt, Psycopg.
2. Create Python virtual environment and install dependencies.
3. Configure `app/core/config.py` with Pydantic `BaseSettings` reading from `.env`.
4. Configure database connection in `app/db/session.py` with retry logic and connection testing.
5. Create SQLAlchemy models for `User` and `CareerProfile`.
6. Set up Alembic and run the initial migration to create `users` and `career_profiles` tables.
7. Implement security helpers in `app/core/security.py` (password hashing, verification, JWT generation and validation).
8. Implement `auth_service`, `user_service`, and `dashboard_service`.
9. Create FastAPI dependency `get_current_user` in `app/api/deps.py`.
10. Build API routes for auth (`register`, `login`, `me`), `dashboard/summary`, and `profile`.
11. Test backend endpoints with automated test scripts.

### Phase 2: Frontend Foundation & UI
1. Scaffold frontend using Vite with React and TypeScript in `frontend/`.
2. Install and configure Tailwind CSS, Lucide icons, Axios, and React Router.
3. Build cohesive, modern design system in `src/index.css` (dark/light theme with slate/indigo palette, glowing status badges, card styling).
4. Create TypeScript interfaces and Axios client with token interceptors.
5. Build `AuthContext` for persistent session management.
6. Build pages:
   - `Register.tsx`: Modern registration card with real-time validation.
   - `Login.tsx`: Clean login card with error handling and redirect to dashboard.
   - `Dashboard.tsx`: High-impact candidate dashboard featuring:
     - Header with "Source of Truth" status indicator.
     - Profile completion progress card.
     - Metric cards (Career Claims, Verified Evidence, Resumes, Target Jobs).
     - Quick Action cards ("Import Resume", "Add Career Claim", "Analyze Job Description").
   - `Profile.tsx`: Basic profile editor for headline, summary, and links.
7. Wrap protected routes with navigation layout (`Navbar`, `Sidebar`).

### Phase 3: Verification & Polish
1. Run end-to-end user registration and login flow.
2. Verify token storage, route protection, and logout.
3. Verify database state in PostgreSQL.
4. Document startup instructions in `README.md`.

---

## Verification Plan

### Automated Tests
- Backend test script verifying:
  - User registration (`POST /api/v1/auth/register`)
  - Duplicate registration rejection (409 Conflict)
  - User login (`POST /api/v1/auth/login`) with JWT token response
  - Authenticated user retrieval (`GET /api/v1/auth/me`)
  - Dashboard summary retrieval (`GET /api/v1/dashboard/summary`)
  - Profile update (`PUT /api/v1/profile`)

### Manual Verification
- Browser testing of frontend:
  - Registration form -> successful account creation.
  - Automatic transition to Dashboard.
  - Dashboard visual verification (metrics, cards, responsive layout).
  - Logout and session clearance.
  - Login form -> dashboard redirect.
