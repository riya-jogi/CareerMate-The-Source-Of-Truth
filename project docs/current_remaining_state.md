




# Review Scope

I reviewed all ten Markdown files in `project docs`:

- `CareerMate-About product step 1 to 4.md`
- `Truth layer step 5.md`
- `Step 6_ Core Features & Requirements.md`
- `AI_ML Components & Decision Architecture step 7.md`
- `Step 8 — System Architecture & Technology Stack.md`
- `Step 9 — Database & Data Model.md`
- `Step 10 to 13 End to end system tech workflow.md`
- `Step 14 to 17.md`
- `implementation_plan.md`
- `technology choices free vs cost.md`

No files were changed.

## Executive Status

The repository is currently:

> **Module 1 complete: authentication, session security, profile anchor, health checks, and dashboard shell.**

The documented ATS product itself is **not yet implemented**. Resume ingestion, career claims, evidence, job analysis, matching, optimization, truth validation, approval, and resume generation remain pending.

The existing code is substantially ahead of the original `implementation_plan.md`, which incorrectly states that no backend, frontend, migrations, or Docker configuration exist.

# 1. Implemented Functionality

## Backend

Implemented:

- FastAPI application factory and lifecycle handling in `main.py`
- API versioning under `/api/v1`
- Health endpoints
- Global validation and application-error handlers
- Database connectivity checks
- CORS configuration
- Dashboard aggregation service
- Authentication service

Implemented routes:

| Endpoint | Status |
|---|---|
| `GET /` | ✅ Completed |
| `GET /health` | ✅ Completed |
| `GET /api/v1/health` | ✅ Completed |
| `POST /api/v1/auth/register` | ✅ Completed |
| `POST /api/v1/auth/login` | ✅ Completed |
| `POST /api/v1/auth/refresh` | ✅ Completed |
| `POST /api/v1/auth/logout` | ✅ Completed |
| `GET /api/v1/auth/me` | ✅ Completed |
| `GET /api/v1/dashboard/summary` | ✅ Completed |

The route registry is in `router.py`.

## Database

Implemented tables:

### `users`

Implemented in `user.py`:

- UUID primary key
- Unique email
- Bcrypt password hash
- Full name
- Active status
- Verification flag
- Created/updated timestamps
- Last login timestamp

### `career_profiles`

Implemented in `profile.py`:

- UUID primary key
- One-to-one relationship with user
- Headline
- Summary
- Phone
- Location
- LinkedIn
- GitHub
- Portfolio
- Cascading user deletion

### `refresh_tokens`

Implemented in `refresh_token.py`:

- UUID primary key
- SHA-256 token hash
- Expiry
- Revocation state
- Device metadata
- IP address
- User ownership

Migrations exist in:

- `ef2f3115aa8b_create_initial_user_and_profile_tables.py`
- `79246caf0c9b_create_refresh_tokens_table.py`
- `fa9ac77da9fd_add_last_login_at_to_users.py`

The `vector` extension is enabled by migration, but no vector columns or vector queries exist yet.

## Authentication and Security

Implemented in `security.py` and `deps.py`:

- Bcrypt password hashing
- Password-strength validation
- Case-normalized emails
- Generic invalid-credential responses
- Short-lived JWT access tokens
- JWT subject linked to user UUID
- JWT type validation
- JWT expiry validation
- HttpOnly refresh-token cookie
- SHA-256 refresh-token storage
- Refresh-token rotation
- Revoked-token replay detection
- Automatic invalidation of all sessions after token reuse
- Explicit logout
- Logout-all-devices support
- Active-account enforcement
- Backend authentication dependency
- Backend resource ownership foundation

Not implemented:

- Email verification
- Password reset
- MFA
- Account recovery
- Login throttling/rate limiting
- Security event audit log
- Full profile authorization layer for future resources

## Frontend

Implemented:

- React + TypeScript + Vite
- React Router
- Public and protected route guards
- Sign-in screen
- Sign-up screen
- Automatic login after registration
- In-memory access-token storage
- HttpOnly refresh-cookie flow
- Automatic refresh after `401`
- Logout
- Dashboard page
- Dashboard API integration
- Profile-completeness display
- Security/session display
- Responsive application layout

Relevant files:

- `App.tsx`
- `AuthContext.tsx`
- `client.ts`
- `Dashboard.tsx`

Frontend routes for profile, resumes, jobs, matching, optimization, and settings currently render `PlaceholderPage.tsx`.

## Configuration

Implemented in `config.py`:

- Environment-based settings
- PostgreSQL URL
- Connection-pool configuration
- JWT configuration
- Access/refresh expiry configuration
- Cookie configuration
- CORS configuration
- Production validation for JWT secret and secure cookies

Infrastructure currently exists in `docker-compose.yml`:

- PostgreSQL with pgvector image
- Persistent PostgreSQL volume
- Health check

Not configured:

- Ollama
- Gemini/OpenAI adapters
- Embedding provider
- Object storage
- MinIO
- Redis
- Celery
- Worker process
- Monitoring
- Production deployment

## Testing

Backend tests cover:

- Registration
- Duplicate registration
- Password validation
- Login
- Invalid credentials
- JWT expiry
- Inactive users
- Refresh rotation
- Refresh-token replay
- Logout
- Logout-all-devices
- `/auth/me`
- Dashboard
- Database relationships
- Health endpoints
- Configuration
- Error handling
- End-to-end Module 1 flow

The main integration test is `test_module_1_complete_flow.py`.

Frontend has no automated test suite.

Validation results:

- Frontend build: ✅ Passed
- Frontend lint: ⚠️ Passed with warnings
- Backend tests: ⚠️ Could not collect because `psycopg` is missing from the active Python environment

The backend requirements correctly declare `psycopg`, but the current interpreter environment is incomplete.

# 2. Current Development Step

The repository is currently at:

> **Step 14 implementation outcome: Module 1 authentication and dashboard foundation.**

Completed in this module:

- User registration
- Automatic career-profile anchor creation
- Login
- JWT access token
- Refresh-token persistence
- Refresh rotation
- Logout
- Current-user endpoint
- Dashboard summary
- Initial database migrations
- Frontend auth flow
- Protected application shell

Currently in progress:

- Transition from authentication foundation to **Module 2: Career Profile and Evidence**
- Replacing placeholder application routes with real profile functionality
- Expanding the database from three tables into the documented career data model

Remaining before the core ATS workflow can begin:

1. Profile CRUD
2. Experience, project, education, certification, and skill models
3. Career claims and evidence
4. Resume upload and extraction
5. Candidate review/confirmation
6. Job and JD analysis
7. Matching and gap analysis
8. Resume optimization
9. Truth validation
10. Candidate approval
11. Resume generation

Primary dependency: the source-of-truth data model must be implemented before AI optimization.

# 3. Complete Pending Work Checklist

## Backend

- [ ] Profile CRUD service and router
- [ ] Experiences
- [ ] Projects
- [ ] Education
- [ ] Certifications
- [ ] Skills
- [ ] Candidate-skill relationships
- [ ] Career claims
- [ ] Evidence
- [ ] Claim/evidence relationships
- [ ] Resume file metadata
- [ ] Resume upload handling
- [ ] PDF/DOCX parsing
- [ ] Extraction proposal workflow
- [ ] Jobs
- [ ] Job requirements
- [ ] Matching engine
- [ ] Gap analysis
- [ ] Resume optimization
- [ ] Claim validation
- [ ] Change tracking
- [ ] Candidate approvals
- [ ] Resume rendering
- [ ] Final alignment analysis
- [ ] Application tracking

## Frontend

- [ ] Editable career profile
- [ ] Experience/project/education/certification forms
- [ ] Skills and claim management
- [ ] Evidence management
- [ ] Resume upload
- [ ] Extraction review screen
- [ ] Claim confirmation/edit/reject workflow
- [ ] Job-description input
- [ ] JD requirement display
- [ ] Match and gap dashboard
- [ ] Resume optimization review
- [ ] Diff/change review
- [ ] Approve/reject/edit controls
- [ ] Resume preview
- [ ] Download flow
- [ ] Version history
- [ ] Application tracking
- [ ] Frontend automated tests

## Database

- [ ] Experiences
- [ ] Projects
- [ ] Education
- [ ] Certifications
- [ ] Skills
- [ ] Candidate skills
- [ ] Career claims
- [ ] Evidence
- [ ] Claim evidence junction
- [ ] Resume files
- [ ] Resumes
- [ ] Resume versions
- [ ] Resume changes
- [ ] Approvals
- [ ] Jobs
- [ ] Job requirements
- [ ] Candidate-job matches
- [ ] Match details
- [ ] AI operations
- [ ] Embedding records
- [ ] Vector indexes
- [ ] Check constraints
- [ ] Ownership indexes
- [ ] Deletion policy

## APIs

- [ ] `GET /profile`
- [ ] `PUT /profile`
- [ ] Career-data CRUD endpoints
- [ ] Claim CRUD endpoints
- [ ] Evidence endpoints
- [ ] Resume upload endpoint
- [ ] Resume extraction endpoint
- [ ] Extraction-review endpoints
- [ ] Job CRUD endpoints
- [ ] JD analysis endpoint
- [ ] Requirements endpoint
- [ ] Matching endpoint
- [ ] Gap-analysis endpoint
- [ ] Optimization endpoint
- [ ] Change-review endpoints
- [ ] Approval endpoints
- [ ] Resume-generation endpoint
- [ ] Download endpoint
- [ ] Version-history endpoint
- [ ] Application endpoints

## Authentication and Security

- [ ] Email verification
- [ ] Password reset
- [ ] Rate limiting
- [ ] Secure production secret provisioning
- [ ] File type and size validation
- [ ] Malware scanning strategy
- [ ] Private object-storage access
- [ ] Prompt/data-retention policy
- [ ] AI-provider privacy controls
- [ ] Security audit logging
- [ ] Account deletion workflow
- [ ] Data export workflow
- [ ] CSRF review if cookie-authenticated APIs expand

## AI/LLM

- [ ] `LLMProvider` interface
- [ ] Ollama provider
- [ ] Gemini provider
- [ ] Optional OpenAI provider
- [ ] Structured Pydantic AI schemas
- [ ] JD analyzer
- [ ] Resume extractor
- [ ] Claim extractor
- [ ] Skill normalization
- [ ] Resume optimizer
- [ ] Change explanation
- [ ] Claim validator
- [ ] Prompt versioning
- [ ] AI-operation logging
- [ ] Provider fallback rules
- [ ] Model benchmark dataset
- [ ] Hallucination/regression evaluation

## Storage

- [ ] Storage interface
- [ ] Local filesystem provider
- [ ] File checksum handling
- [ ] Private file retrieval
- [ ] MinIO provider
- [ ] R2/S3 provider
- [ ] Retention/deletion behavior
- [ ] Maximum file-size policy

## Infrastructure and Configuration

- [ ] `.env.example`
- [ ] Remove default production credentials
- [ ] Configure local PostgreSQL startup documentation
- [ ] Optional pgvector verification
- [ ] AI provider configuration
- [ ] Storage-provider configuration
- [ ] Embedding-provider configuration
- [ ] Production CORS configuration
- [ ] Structured logging
- [ ] Health/readiness checks
- [ ] Error monitoring
- [ ] Backup strategy
- [ ] Database migration runbook

## Testing

- [ ] Profile tests
- [ ] Career entity tests
- [ ] Claims/evidence tests
- [ ] File-upload tests
- [ ] Parser tests
- [ ] AI-schema tests
- [ ] JD-analysis tests
- [ ] Matching tests
- [ ] Truth-validator adversarial tests
- [ ] Approval tests
- [ ] Resume-rendering tests
- [ ] Ownership/isolation tests
- [ ] Security tests
- [ ] Frontend component tests
- [ ] Frontend route tests
- [ ] Browser E2E tests
- [ ] Performance tests
- [ ] Provider-contract tests

## Deployment

- [ ] Backend Dockerfile
- [ ] Frontend production build
- [ ] Reverse proxy
- [ ] Managed PostgreSQL
- [ ] Object storage
- [ ] Secrets management
- [ ] TLS
- [ ] Database backups
- [ ] CI/CD
- [ ] Monitoring
- [ ] Queue/worker architecture
- [ ] Deployment rollback process

## Documentation

- [ ] Correct stale implementation plan
- [ ] Local setup guide
- [ ] Environment variable reference
- [ ] API documentation
- [ ] Database migration guide
- [ ] AI-provider guide
- [ ] Storage-provider guide
- [ ] Truth-layer rules
- [ ] Privacy/data-retention policy
- [ ] Security model
- [ ] User workflow documentation
- [ ] Deployment runbook

## Future Enhancements

- [ ] Multiple resume templates
- [ ] Resume version history UI
- [ ] Application tracker
- [ ] Cover letters
- [ ] Job URL parsing
- [ ] Job discovery
- [ ] Interview preparation
- [ ] External verification
- [ ] Auto-apply
- [ ] Custom ML ranking
- [ ] OCR
- [ ] Multi-language support
- [ ] Team/recruiter accounts

# 4. Step-by-Step Implementation Plan

## Step 0: Reconcile Contracts and Infrastructure

**Objective:** Establish one implementable contract before adding product modules.

**Requirements:** Resolve documented inconsistencies and make local development reproducible.

**Files/components:** Update configuration documentation, `.env.example`, API conventions, and migration conventions.

**Backend:** Confirm synchronous processing for V1; keep service boundaries queue-ready.

**Frontend:** Confirm API response/error shapes and route names.

**Database:** Confirm UUIDs, UTC timestamps, ownership, enums, and cascade rules.

**API:** Freeze `/api/v1/profile`, `/resumes`, `/jobs`, `/matching`, `/optimization` contracts.

**AI/ML:** Confirm provider interfaces without selecting a permanent vendor.

**Configuration:** Add explicit provider, storage, embedding, and environment settings.

**Security:** Remove reliance on default secrets and database credentials.

**Testing:** Add startup/configuration checks.

**Expected result:** One authoritative technical contract.

**Completion criteria:** Documentation and code agree on names, IDs, statuses, and ownership.

**Dependencies:** None.

## Step 1: Career Profile and Structured Career Data

**Objective:** Implement the persistent source of truth.

**Requirements:** Career profile, experience, projects, education, certifications, skills.

**Files/components:** New models, schemas, services, routers, migrations, frontend profile pages.

**Backend:** Add CRUD services with ownership checks and date validation.

**Frontend:** Replace `/app/profile` placeholder with editable profile and career-data forms.

**Database:** Add `experiences`, `projects`, `education`, `certifications`, `skills`, and `candidate_skills`.

**API:** Add profile and career-entity CRUD endpoints.

**AI/ML:** None yet; manual data must work first.

**Configuration:** No new external service required.

**Security:** Every query must filter by authenticated user/profile ownership.

**Testing:** CRUD, validation, ownership isolation, date constraints, duplicate skills.

**Expected result:** A candidate can build a structured career profile without AI.

**Completion criteria:** Profile data persists and can be edited safely from the frontend.

**Dependencies:** Step 0 and current authentication.

## Step 2: Claims, Evidence, and Trust Rules

**Objective:** Build the truth layer.

**Requirements:** Evidence statuses, claims, source traceability, candidate confirmation.

**Files/components:** Claim/evidence models, schemas, validators, services, routes, review components.

**Backend:** Implement claim lifecycle and deterministic status transitions.

**Frontend:** Add claim/evidence review, confirm, edit, reject, and clarification actions.

**Database:** Add `career_claims`, `evidence`, and `claim_evidence`.

**API:** Add claim/evidence CRUD and confirmation endpoints.

**AI/ML:** No trusted mutation by AI; extraction proposals remain pending.

**Configuration:** Add status/enum configuration only if needed.

**Security:** Evidence must be private and profile-owned.

**Testing:** Unsupported claims, status transitions, evidence linking, unauthorized access.

**Expected result:** The system can distinguish evidence-backed, candidate-confirmed, self-declared, clarification, and unsupported claims.

**Completion criteria:** No claim can become trusted without evidence or explicit candidate action.

**Dependencies:** Step 1.

## Step 3: Resume Upload and Candidate Review

**Objective:** Import resumes as proposals, never as automatic truth.

**Requirements:** PDF/DOCX upload, parsing, extraction, candidate review.

**Files/components:** Resume models, storage interface, local provider, parsers, extraction schemas, upload/review pages.

**Backend:** Validate files, store metadata, extract text, persist extraction proposals.

**Frontend:** Replace `/app/resumes` placeholder with upload and review screens.

**Database:** Add `resume_files`, `resumes`, extraction/proposal status fields, and AI-operation metadata.

**API:** Add upload, extraction, extraction-status, and proposal-review endpoints.

**AI/ML:** Implement structured resume extraction through `LLMProvider`.

**Configuration:** Add local storage path, file limits, parser settings, provider settings.

**Security:** Validate MIME type, extension, size, path safety, and private access.

**Testing:** PDF/DOCX parsing, malformed files, unsupported files, extraction schema validation.

**Expected result:** A resume becomes a reviewable structured proposal.

**Completion criteria:** Candidate can confirm, edit, or reject every extracted item.

**Dependencies:** Steps 1 and 2.

## Step 4: Jobs and JD Analysis

**Objective:** Convert pasted job descriptions into structured requirements.

**Requirements:** Job creation, required/preferred classification, normalization.

**Files/components:** Job models, requirement models, analyzer service, job pages.

**Backend:** Store raw JD, invoke analyzer, validate structured results, persist requirements.

**Frontend:** Replace `/app/jobs` placeholder with job-entry and analysis views.

**Database:** Add `jobs` and `job_requirements`.

**API:** Add job CRUD, analyze, requirements, and status endpoints.

**AI/ML:** Implement JD extraction, requirement classification, skill normalization.

**Configuration:** Add LLM provider/model and prompt-version settings.

**Security:** Jobs must be accessible only to their owner.

**Testing:** Empty JD, malformed AI output, required/preferred cases, experience extraction.

**Expected result:** A pasted JD becomes structured, explainable requirements.

**Completion criteria:** Requirements are persisted with category, importance, skill, and experience fields.

**Dependencies:** Step 0; normalized skills from Step 1.

## Step 5: Matching and Gap Analysis

**Objective:** Compare supported candidate claims with job requirements.

**Requirements:** Exact, normalized, semantic, evidence-aware matching.

**Files/components:** Matching service, scoring rules, match schemas, matching page.

**Backend:** Implement deterministic matching, experience calculations, gap classification, explanations.

**Frontend:** Replace `/app/matching` placeholder with score breakdown, matches, partials, gaps, and unknowns.

**Database:** Add `candidate_job_matches` and `match_details`.

**API:** Add match creation, retrieval, and gap-analysis endpoints.

**AI/ML:** Add embeddings only for retrieval; never let similarity authorize truth.

**Configuration:** Add embedding provider/model/dimension configuration.

**Security:** Match data must be job/profile-owned.

**Testing:** Alias matching, semantic retrieval, professional-vs-personal experience, missing evidence, score weighting.

**Expected result:** Candidates see why they match or fail each requirement.

**Completion criteria:** Every requirement receives a match type, score, explanation, and supporting claim where applicable.

**Dependencies:** Steps 1, 2, and 4.

## Step 6: Resume Optimization, Validation, and Approval

**Objective:** Generate safe job-specific content and require explicit approval.

**Requirements:** Resume rewriting, change tracking, truth validation, approve/edit/reject.

**Files/components:** Optimizer, validator, change models, approval routes, review UI.

**Backend:** Select allowed claims, generate proposals, extract generated claims, block unsupported statements.

**Frontend:** Replace `/app/optimization` placeholder with side-by-side review and decision controls.

**Database:** Add `resume_versions`, `resume_changes`, `approvals`.

**API:** Add optimize, changes, approve, reject, edit, and validation endpoints.

**AI/ML:** LLM generates wording only from an allow-listed fact set.

**Configuration:** Add prompt versions, retry limits, validation thresholds.

**Security:** Candidate approval must be explicit and auditable.

**Testing:** Fabricated skills, inflated dates, invented responsibilities, unsupported adjectives, approval state transitions.

**Expected result:** Every final resume statement is traceable to approved candidate information.

**Completion criteria:** Unsupported claims are blocked before approval or generation.

**Dependencies:** Steps 2, 4, and 5.

## Step 7: Deterministic Resume Generation and Alignment

**Objective:** Produce immutable final PDF/DOCX outputs.

**Requirements:** Templates, final generation, downloads, alignment analysis, version history.

**Files/components:** Renderer, templates, file provider, preview/download UI.

**Backend:** Render approved structured content; store immutable snapshots and file metadata.

**Frontend:** Add preview, download, version list, and final alignment results.

**Database:** Add immutable content snapshots and generated-file references.

**API:** Add generate, download, version-history, and final-analysis endpoints.

**AI/ML:** Optional semantic coverage explanation; rendering remains deterministic.

**Configuration:** Add output format, template, storage, and rendering settings.

**Security:** Generated files remain private and access-controlled.

**Testing:** PDF text extraction, deterministic output, snapshot immutability, download authorization.

**Expected result:** Candidate receives a job-specific, traceable resume.

**Completion criteria:** Approved resume can be regenerated reproducibly without changing historical versions.

**Dependencies:** Step 6.

## Step 8: Production Hardening and Deployment

**Objective:** Make Version 1 deployable and operable.

**Requirements:** Security, reliability, storage, monitoring, deployment.

**Files/components:** Dockerfiles, CI/CD, deployment manifests, monitoring, documentation.

**Backend:** Add readiness checks, structured logging, rate limiting, cleanup jobs, and production error handling.

**Frontend:** Add production API configuration and browser E2E coverage.

**Database:** Add backup strategy, indexes, migration verification, and connection-pool tuning.

**API:** Document OpenAPI contracts and operational error codes.

**AI/ML:** Add provider benchmarks, cost controls, fallback policy, and regression suite.

**Configuration:** Production secrets, secure cookies, CORS, managed database, R2/S3.

**Security:** TLS, secret management, file privacy, retention, deletion, audit review.

**Testing:** Full end-to-end workflow, isolation tests, load tests, deployment smoke tests.

**Expected result:** Version 1 is reproducible, secure, observable, and deployable.

**Completion criteria:** All core workflow tests pass in a production-like environment.

**Dependencies:** Steps 1–7.

# 5. Requirement-to-Implementation Mapping

| Requirement | Implementation | Status | Remaining Work |
|---|---|---|---|
| Candidate account | Auth routes and auth service | ✅ Completed | Email verification/reset |
| Secure passwords | Bcrypt in `security.py` | ✅ Completed | Rate limiting and breach policy |
| JWT authentication | Access JWT and dependencies | ✅ Completed | Broader authorization testing |
| Refresh sessions | Rotating hashed refresh tokens | ✅ Completed | Cleanup and security audit logging |
| Career profile anchor | `CareerProfile` model created on registration | ✅ Completed | Full profile CRUD |
| Profile information | Basic profile columns exist | 🟡 Partially Completed | Frontend/API editing |
| Experiences | Documented model, absent in code | 🔴 Not Started | Step 1 |
| Projects | Documented model, absent in code | 🔴 Not Started | Step 1 |
| Education | Documented model, absent in code | 🔴 Not Started | Step 1 |
| Certifications | Documented model, absent in code | 🔴 Not Started | Step 1 |
| Skills | Documented model, absent in code | 🔴 Not Started | Step 1 |
| Career claims | Documented truth-layer design only | 🔴 Not Started | Step 2 |
| Evidence | Documented truth-layer design only | 🔴 Not Started | Step 2 |
| Resume upload | Placeholder frontend only | 🔴 Not Started | Step 3 |
| Resume extraction | No parser or AI integration | 🔴 Not Started | Step 3 |
| Candidate review | Not implemented | 🔴 Not Started | Step 3 |
| JD input | Placeholder frontend only | 🔴 Not Started | Step 4 |
| JD analysis | No analyzer/provider | 🔴 Not Started | Step 4 |
| Required/preferred requirements | Documented only | 🔴 Not Started | Step 4 |
| Skill normalization | Documented only | 🔴 Not Started | Steps 1 and 4 |
| Candidate-job matching | Placeholder frontend only | 🔴 Not Started | Step 5 |
| Gap analysis | Documented only | 🔴 Not Started | Step 5 |
| Semantic matching | pgvector extension only | 🟡 Partially Completed | Embeddings and retrieval |
| Resume optimization | Placeholder frontend only | 🔴 Not Started | Step 6 |
| Truth validation | Design principle only | 🔴 Not Started | Step 6 |
| Change tracking | No models/routes | 🔴 Not Started | Step 6 |
| Candidate approval | No models/routes | 🔴 Not Started | Step 6 |
| Resume generation | No renderer/storage | 🔴 Not Started | Step 7 |
| Resume versioning | No implementation | 🔴 Not Started | Step 7 |
| Application tracking | Dashboard placeholder only | ⏸️ Deferred | Post-V1 |
| AI abstraction | Not implemented | 🔴 Not Started | Step 3/4 |
| Ollama | Not configured | 🔴 Not Started | Provider integration |
| Gemini/OpenAI | Not configured | 🔴 Not Started | Provider integration |
| Local storage | Not implemented | 🔴 Not Started | Step 3 |
| R2/S3 | Not implemented | ⏸️ Deferred | Production |
| Redis/queue | Intentionally excluded | ⏸️ Deferred | Production scale |
| PostgreSQL | Configured and migrated | ✅ Completed | Production database |
| pgvector | Extension enabled | 🟡 Partially Completed | Vector schema/search |
| Docker | PostgreSQL compose service exists | 🟡 Partially Completed | Full application deployment |
| Backend tests | Module 1 tests exist | ✅ Completed | Tests for all future modules |
| Frontend tests | None | 🔴 Not Started | Add component/E2E tests |
| Documentation | Architecture is extensive | 🟡 Partially Completed | Update stale implementation plan |

# 6. Gaps and Inconsistencies

## Critical

1. **The documented MVP is not implemented.**  
   The core product workflow stops after authentication and dashboard shell.

2. **Profile CRUD is documented but absent.**  
   The frontend route exists, but `/profile` API routes and service do not.

3. **Dashboard metrics are placeholders.**  
   Claims, evidence, jobs, matches, and optimized-resume counts are hard-coded to zero in `dashboard_service.py`.

4. **The dashboard mislabels evidence as resume upload.**  
   The frontend infers resume upload from `evidence_sources_count`, although evidence and resume tables do not exist.

5. **The truth firewall is not enforced yet.**  
   It exists only as architecture documentation. There is no claim validator, evidence validator, or approval gate.

## High

6. **No resource ownership model beyond users/profile.**  
   Future jobs, files, claims, and resumes must all enforce ownership in backend queries.

7. **No file security pipeline.**  
   Upload validation, private storage, size limits, checksums, and safe retrieval are absent.

8. **No AI provider abstraction.**  
   Ollama/Gemini/OpenAI are described but not implemented.

9. **pgvector is only partially configured.**  
   The extension exists, but no embeddings, dimensions, metadata, or similarity queries exist.

10. **No structured AI output validation.**  
    The planned Pydantic schemas and semantic checks do not exist.

11. **No deterministic experience calculation.**  
    The system cannot currently calculate professional years by skill or experience type.

12. **No immutable resume history.**  
    There are no resume versions, snapshots, changes, or approvals.

## Medium

13. **The original implementation plan is stale.**  
    It says the repository has no code, which conflicts with the current implementation.

14. **Documentation uses inconsistent terminology.**  
    Earlier documents use “verified,” while later documents correctly distinguish evidence-backed, candidate-confirmed, self-declared, needs-clarification, and unsupported.

15. **Documentation and code differ on profile fields.**  
    Some documents place full name/email in `career_profiles`; current code stores full name in `users`.

16. **Documentation describes asynchronous/async patterns, while current code is synchronous.**  
    This is acceptable for low traffic but should be recorded as an intentional V1 decision.

17. **No email verification exists despite `is_verified`.**  
    New users are marked unverified, but current protected routes require only active status.

18. **Default development secrets are present.**  
    Production validation catches them, but deployment documentation must require explicit secret injection.

19. **Backend tests cannot currently run in the active environment.**  
    `psycopg` is declared but missing from the interpreter used by `py -3.13`.

20. **Frontend lint warnings remain.**  
    Warnings concern effect-driven state updates and mixed component/helper exports.

# 7. Recommended Development Order

```text
Current state
  -> Fix environment and documentation drift
  -> Step 1: Career Profile and structured career data
  -> Step 2: Claims, evidence, and trust rules
  -> Step 3: Resume upload, parsing, and candidate review
  -> Step 4: Job storage and JD analysis
  -> Step 5: Matching and gap analysis
  -> Step 6: Resume optimization, truth validation, and approval
  -> Step 7: Deterministic resume generation and versioning
  -> Step 8: Frontend completion and full workflow integration
  -> Version 1 feature complete
  -> Security, regression, browser, and deployment testing
  -> Local production-like deployment
  -> Later: queue/workers, R2/S3, application tracking, auto-apply
```

The immediate next implementation should be **Step 1: Career Profile and structured career data**, beginning with profile CRUD and the core entities that the truth layer depends on.