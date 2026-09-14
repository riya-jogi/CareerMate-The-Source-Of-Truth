# step 14-15

# **Step 14 — Backend Project Structure & Implementation Plan**

## **14.1 Objective**

We need a backend structure that is:

* easy to understand while developing  
* suitable for a 1-person/learning project  
* production-oriented  
* modular without becoming over-engineered  
* easy to test  
* provider-independent  
* ready for future Redis/workers  
* compatible with our V1 architecture

We will therefore use a **modular monolith with clear layers**.

---

# **14.2 Final Backend Architecture**

The backend will follow:

                   ┌─────────────────────┐  
                    │      Frontend       │  
                    │ React \+ TypeScript  │  
                    └──────────┬──────────┘  
                               │ HTTP  
                               ↓  
                    ┌─────────────────────┐  
                    │     API Layer       │  
                    │      FastAPI        │  
                    └──────────┬──────────┘  
                               ↓  
                    ┌─────────────────────┐  
                    │ Application Services│  
                    │  Business Workflows │  
                    └──────────┬──────────┘  
                               ↓  
             ┌─────────────────┼─────────────────┐  
             ↓                 ↓                 ↓  
       ┌───────────┐    ┌──────────────┐   ┌────────────┐  
       │Repository │    │  AI Service  │   │ Validators │  
       │   Layer   │    │              │   │            │  
       └─────┬─────┘    └──────┬───────┘   └────────────┘  
             │                 │  
             ↓                 ↓  
      PostgreSQL          LLM / Embeddings  
       \+ pgvector

The important separation is:

> **API knows HTTP. Services know business logic. Repositories know persistence. AI knows models. Validators know rules.**

---

# **14.3 Recommended Folder Structure**

I recommend slightly refining the structure from our earlier conceptual version:

backend/  
│  
├── app/  
│   │  
│   ├── main.py  
│   │  
│   ├── core/  
│   │   ├── config.py  
│   │   ├── security.py  
│   │   ├── database.py  
│   │   ├── exceptions.py  
│   │   └── logging.py  
│   │  
│   ├── api/  
│   │   ├── deps.py  
│   │   │  
│   │   └── v1/  
│   │       ├── router.py  
│   │       │  
│   │       ├── auth.py  
│   │       ├── profile.py  
│   │       ├── claims.py  
│   │       ├── resumes.py  
│   │       ├── jobs.py  
│   │       ├── matching.py  
│   │       ├── optimization.py  
│   │       └── resume\_generation.py  
│   │  
│   ├── models/  
│   │   ├── user.py  
│   │   ├── career\_profile.py  
│   │   ├── experience.py  
│   │   ├── project.py  
│   │   ├── education.py  
│   │   ├── certification.py  
│   │   ├── skill.py  
│   │   ├── candidate\_skill.py  
│   │   ├── career\_claim.py  
│   │   ├── evidence.py  
│   │   ├── job.py  
│   │   ├── job\_requirement.py  
│   │   ├── candidate\_job\_match.py  
│   │   ├── match\_detail.py  
│   │   ├── resume.py  
│   │   ├── resume\_version.py  
│   │   ├── resume\_change.py  
│   │   ├── approval.py  
│   │   └── ai\_operation.py  
│   │  
│   ├── schemas/  
│   │   ├── auth.py  
│   │   ├── profile.py  
│   │   ├── claims.py  
│   │   ├── resumes.py  
│   │   ├── jobs.py  
│   │   ├── matching.py  
│   │   ├── optimization.py  
│   │   └── common.py  
│   │  
│   ├── repositories/  
│   │   ├── user.py  
│   │   ├── profile.py  
│   │   ├── claim.py  
│   │   ├── resume.py  
│   │   ├── job.py  
│   │   ├── match.py  
│   │   └── ai\_operation.py  
│   │  
│   ├── services/  
│   │   ├── auth\_service.py  
│   │   ├── profile\_service.py  
│   │   ├── claim\_service.py  
│   │   ├── resume\_service.py  
│   │   ├── job\_service.py  
│   │   ├── jd\_analysis\_service.py  
│   │   ├── matching\_service.py  
│   │   ├── gap\_analysis\_service.py  
│   │   ├── optimization\_service.py  
│   │   ├── claim\_validation\_service.py  
│   │   └── resume\_generation\_service.py  
│   │  
│   ├── ai/  
│   │   ├── interfaces/  
│   │   │   ├── llm.py  
│   │   │   └── embeddings.py  
│   │   │  
│   │   ├── providers/  
│   │   │   ├── ollama.py  
│   │   │   ├── gemini.py  
│   │   │   └── local\_embeddings.py  
│   │   │  
│   │   ├── prompts/  
│   │   │   ├── resume\_extraction.py  
│   │   │   ├── jd\_analysis.py  
│   │   │   ├── optimization.py  
│   │   │   └── claim\_validation.py  
│   │   │  
│   │   └── schemas/  
│   │       ├── resume\_extraction.py  
│   │       ├── jd\_analysis.py  
│   │       ├── optimization.py  
│   │       └── validation.py  
│   │  
│   ├── validators/  
│   │   ├── claim\_validator.py  
│   │   ├── date\_validator.py  
│   │   ├── experience\_validator.py  
│   │   └── resume\_validator.py  
│   │  
│   ├── storage/  
│   │   ├── interface.py  
│   │   └── local.py  
│   │  
│   └── utils/  
│       ├── dates.py  
│       ├── hashing.py  
│       └── text.py  
│  
├── migrations/  
│  
├── tests/  
│   ├── unit/  
│   ├── integration/  
│   ├── ai/  
│   └── e2e/  
│  
├── .env  
├── .env.example  
├── .gitignore  
├── requirements.txt  
├── alembic.ini  
└── README.md  
---

# **14.4 Why This Structure?**

We don't want this:

routes/  
    auth.py  
    profile.py

everything\_else.py

because eventually all the business logic ends up inside API routes.

Instead:

API  
 ↓  
Service  
 ↓  
Repository  
 ↓  
Database

For AI:

Service  
 ↓  
AI interface  
 ↓  
Provider  
 ↓  
Ollama/Gemini

This gives us clean boundaries.

---

# **14.5 `api/`**

This is our HTTP layer.

Example:

@router.post("/jobs/{job\_id}/analyze")  
async def analyze\_job(  
    job\_id: UUID,  
    current\_user: User \= Depends(get\_current\_user),  
):  
    return await jd\_analysis\_service.analyze(  
        job\_id=job\_id,  
        user\_id=current\_user.id,  
    )

The route should **not** contain:

\# Don't do this inside route  
llm.generate(...)  
db.execute(...)  
calculate\_score(...)  
validate\_claim(...)

Instead:

Route  
 ↓  
Service  
 ↓  
AI / Repository / Validator  
---

# **14.6 `schemas/`**

Schemas define what enters and leaves the API.

For example:

class RegisterRequest(BaseModel):  
    email: EmailStr  
    password: str

and:

class UserResponse(BaseModel):  
    id: UUID  
    email: EmailStr

Schemas are not the same thing as database models.

### **Database model**

Represents:

> How data is stored.

### **Pydantic schema**

Represents:

> What the API accepts/returns.

This distinction is important.

---

# **14.7 `models/`**

These will contain our SQLAlchemy database models.

Example:

User  
CareerProfile  
Experience  
Project  
Education  
Certification  
Skill  
CandidateSkill  
CareerClaim  
Evidence  
ClaimEvidence  
Job  
JobRequirement  
CandidateJobMatch  
MatchDetail  
Resume  
ResumeVersion  
ResumeChange  
Approval  
AIOperation

We'll implement these systematically rather than creating everything at once.

---

# **14.8 `repositories/`**

Repositories isolate database operations.

For example:

class UserRepository:

    async def get\_by\_email(self, email):  
        ...

    async def get\_by\_id(self, user\_id):  
        ...

    async def create(self, user):  
        ...

The service doesn't need to know how SQLAlchemy queries work.

Example:

AuthService  
    ↓  
UserRepository  
    ↓  
SQLAlchemy  
    ↓  
PostgreSQL  
---

# **14.9 `services/`**

This is where the **actual product logic lives**.

Examples:

### **AuthService**

register  
login  
get\_current\_user

### **ProfileService**

create\_profile  
update\_profile  
get\_profile

### **JDAnalysisService**

analyze\_job  
normalize\_requirements  
persist\_requirements

### **MatchingService**

match\_candidate\_to\_job  
retrieve\_relevant\_claims  
calculate\_requirement\_match  
calculate\_alignment\_score

### **OptimizationService**

select\_relevant\_claims  
generate\_resume\_changes  
validate\_proposals

This layer is the heart of the application.

---

# **14.10 `ai/`**

This is deliberately isolated.

ai/  
├── interfaces/  
├── providers/  
├── prompts/  
└── schemas/

For example:

OptimizationService  
       ↓  
LLMProvider  
       ↓  
OllamaProvider  
       ↓  
Ollama

Later:

OptimizationService  
       ↓  
LLMProvider  
       ↓  
GeminiProvider  
       ↓  
Gemini

No changes to `OptimizationService`.

---

# **14.11 AI schemas**

These are especially important.

For example:

class ExtractedSkill(BaseModel):  
    name: str  
    experience\_type: ExperienceType  
    confidence: float

and:

class ResumeExtractionResult(BaseModel):  
    experiences: list\[ExtractedExperience\]  
    projects: list\[ExtractedProject\]  
    education: list\[ExtractedEducation\]  
    certifications: list\[ExtractedCertification\]  
    skills: list\[ExtractedSkill\]  
    claims: list\[ExtractedClaim\]

The LLM must produce something compatible with this contract.

---

# **14.12 `validators/`**

This is one of the most important directories in the project.

Because:

> **AI does not get the final say.**

Example:

LLM proposes:  
"Architected scalable Python systems"  
             ↓  
Claim Validator  
             ↓  
Career Profile says:  
"Developed Python APIs"  
             ↓  
BLOCK

Validators check:

* dates  
* duration  
* experience type  
* claim support  
* claim strength  
* unsupported skills  
* unsupported achievements  
* contextual changes

---

# **14.13 `storage/`**

V1:

StorageProvider  
      ↓  
LocalStorageProvider  
      ↓  
./storage/

Future:

StorageProvider  
      ↓  
R2StorageProvider  
      ↓  
Cloudflare R2

Again, the service doesn't change.

---

# **14.14 Configuration**

We'll centralize configuration.

class Settings(BaseSettings):  
    app\_name: str  
    environment: str

    database\_url: str

    llm\_provider: str  
    llm\_fallback\_provider: str | None

    ollama\_base\_url: str  
    ollama\_model: str

    gemini\_api\_key: str | None  
    gemini\_model: str | None

    embedding\_provider: str  
    embedding\_model: str

    storage\_provider: str

    queue\_provider: str

Then:

settings \= Settings()

No hard-coded:

OLLAMA\_URL \= "http://localhost:11434"

inside business code.

---

# **14.15 Environment**

`.env.example`:

APP\_NAME=Candidate ATS  
ENVIRONMENT=development

DATABASE\_URL=postgresql+asyncpg://postgres:password@localhost:5432/candidate\_ats

LLM\_PROVIDER=ollama  
LLM\_FALLBACK\_PROVIDER=

OLLAMA\_BASE\_URL=http://localhost:11434  
OLLAMA\_MODEL=

GEMINI\_API\_KEY=  
GEMINI\_MODEL=

EMBEDDING\_PROVIDER=local  
EMBEDDING\_MODEL=

STORAGE\_PROVIDER=local

QUEUE\_PROVIDER=direct  
REDIS\_URL=

Actual `.env`:

DO NOT COMMIT TO GIT  
---

# **14.16 Dependency Injection**

FastAPI dependencies will be used for things such as:

get\_db()  
get\_current\_user()  
get\_llm\_provider()  
get\_embedding\_provider()  
get\_storage\_provider()

For example:

@router.get("/profile")  
async def get\_profile(  
    current\_user \= Depends(get\_current\_user),  
    profile\_service \= Depends(get\_profile\_service),  
):  
    return await profile\_service.get\_profile(current\_user.id)

This will also make testing easier because we can inject mocks/fakes.

---

# **14.17 Error Handling**

We will create application-level exceptions.

For example:

class AppException(Exception):  
    code: str  
    message: str

Then:

ResourceNotFound  
AuthenticationError  
AuthorizationError  
ValidationError  
LLMUnavailableError  
LLMOutputError  
UnsupportedClaimError  
ResumeGenerationError

FastAPI exception handlers convert them into consistent responses.

Example:

{  
  "success": false,  
  "error": {  
    "code": "LLM\_UNAVAILABLE",  
    "message": "The configured AI provider is currently unavailable."  
  }  
}

Not:

{  
  "error": "500 Internal Server Error"  
}  
---

# **14.18 API Response Convention**

For V1, we'll keep responses simple and consistent.

Success:

{  
  "data": {}  
}

Error:

{  
  "error": {  
    "code": "SOME\_ERROR",  
    "message": "Human-readable message"  
  }  
}

For paginated endpoints, we'll later use:

{  
  "data": \[\],  
  "pagination": {  
    "page": 1,  
    "page\_size": 20,  
    "total": 100  
  }  
}

Exact pagination strategy can be finalized when implementing the relevant module.

---

# **14.19 Authentication Boundary**

Authentication will be implemented as its own module.

Auth  
 ├── register  
 ├── login  
 ├── current user  
 └── authorization

The important ownership rule is:

Authenticated User  
       ↓  
user\_id  
       ↓  
Resource ownership check  
       ↓  
Allowed / Forbidden

For example:

GET /jobs/123

must verify:

job.user\_id \== current\_user.id

before returning it.

---

# **14.20 Database Migration Strategy**

We will use **Alembic**.

Not:

manually create tables

and not:

Base.metadata.create\_all()

as our production schema strategy.

Development flow:

SQLAlchemy Model  
       ↓  
Alembic Migration  
       ↓  
PostgreSQL

Example:

alembic revision \--autogenerate \-m "create users table"

then:

alembic upgrade head

This gives us controlled schema evolution.

---

# **14.21 Testing Structure**

tests/  
├── unit/  
│   ├── test\_auth.py  
│   ├── test\_claim\_validation.py  
│   ├── test\_matching.py  
│   └── test\_dates.py  
│  
├── integration/  
│   ├── test\_auth\_api.py  
│   ├── test\_profile\_api.py  
│   └── test\_job\_api.py  
│  
├── ai/  
│   ├── test\_resume\_extraction.py  
│   ├── test\_jd\_analysis.py  
│   ├── test\_optimization.py  
│   └── test\_validation.py  
│  
└── e2e/  
    └── test\_complete\_workflow.py

We should **not wait until the entire application is finished before testing**.

Each module gets tests as it is implemented.

---

# **14.22 Implementation Order**

This is the implementation sequence I recommend:

Phase 1  
│  
├── Project setup  
├── FastAPI application  
├── Configuration  
├── PostgreSQL connection  
├── Alembic  
└── Base infrastructure

Phase 2  
│  
├── User model  
├── Authentication  
├── JWT/session handling  
├── Current user  
└── Authorization

Phase 3  
│  
├── Career Profile  
├── Experiences  
├── Projects  
├── Education  
├── Certifications  
└── Skills

Phase 4  
│  
├── Resume upload  
├── Local storage  
├── Resume text extraction  
└── AI extraction

Phase 5  
│  
├── Career Claims  
├── Evidence  
├── Candidate confirmation  
└── Trust/status system

Phase 6  
│  
├── Job creation  
├── JD storage  
├── JD analysis  
└── Job requirements

Phase 7  
│  
├── Embeddings  
├── Exact matching  
├── Normalized matching  
├── Semantic retrieval  
├── Match engine  
└── Gap analysis

Phase 8  
│  
├── Resume optimization  
├── Change tracking  
├── Claim validation  
└── Candidate approval

Phase 9  
│  
├── Resume versioning  
├── PDF/DOCX generation  
└── Final alignment analysis

Phase 10  
│  
├── Frontend integration  
├── E2E testing  
├── Security hardening  
└── Local V1 completion  
---

# **14.23 What We Should NOT Build Yet**

To avoid scope creep, we will **not** start with:

❌ Redis  
❌ Celery  
❌ Kafka  
❌ Microservices  
❌ Kubernetes  
❌ Cloud deployment  
❌ R2  
❌ Auto-apply  
❌ Job scraping  
❌ Custom ML model  
❌ Fine-tuning  
❌ Complex agent architecture

We first make the core product work locally.

---

# **14.24 V1 Backend Dependency Flow**

The dependency direction should look like:

API  
 ↓  
Services  
 ↓  
Repositories  
 ↓  
Database

Services  
 ↓  
AI Interfaces  
 ↓  
AI Providers

Services  
 ↓  
Validators

Services  
 ↓  
Storage Interface  
 ↓  
Storage Provider

Avoid:

Repository → Service  
Service → API  
Model → Ollama  
Database Model → Gemini

That would create tight coupling.

---

# **14.25 Step 14 Completion Criteria**

Step 14 is complete when we have:

* Backend architecture defined  
* Folder structure defined  
* API/service/repository separation defined  
* AI provider boundary defined  
* Storage boundary defined  
* Configuration strategy defined  
* Authentication boundary defined  
* Error strategy defined  
* Migration strategy defined  
* Testing structure defined  
* Implementation sequence defined  
* V1 scope protection defined

### **One item remains intentionally open**

**Exact authentication implementation** — JWT access/refresh token details, expiry, password hashing library, cookie-vs-header strategy, etc. — will be finalized when we implement the authentication module because those choices should be made together with the frontend login/dashboard flow.

---

# **Next: Step 15 — Database Models & Migrations**

Now that the backend structure is fixed, the logical next step is to turn our conceptual database design into the **actual PostgreSQL schema**.

We'll go through it in this order:

Step 15  
   ↓  
Database architecture  
   ↓  
SQLAlchemy Base  
   ↓  
Users  
   ↓  
Career Profile  
   ↓  
Experience / Projects / Education  
   ↓  
Skills  
   ↓  
Career Claims  
   ↓  
Evidence  
   ↓  
Jobs / Requirements  
   ↓  
Matching  
   ↓  
Resumes / Versions / Changes  
   ↓  
Approvals  
   ↓  
AI Operations  
   ↓  
pgvector  
   ↓  
Relationships \+ constraints  
   ↓  
Indexes  
   ↓  
Alembic migrations  
   ↓  
Database testing

**I recommend we do Step 15 before writing the authentication code**, because the authentication module depends directly on the finalized `users` model and database/migration foundation.

ok lets do that

Great. Let’s start **Step 15 — Database Models & Migrations**.

This is where we convert our conceptual database design into the **actual V1 PostgreSQL architecture**. We’ll finalize the schema before implementing authentication and the rest of the backend.

# **Step 15 — Database Models & Migrations**

## **15.1 Objective**

Our database needs to support the complete V1 lifecycle:

User  
 ↓  
Career Profile  
 ↓  
Experiences / Projects / Education / Skills  
 ↓  
Career Claims \+ Evidence  
 ↓  
Job Description  
 ↓  
Job Requirements  
 ↓  
Candidate ↔ Job Matching  
 ↓  
Resume Optimization  
 ↓  
Resume Versions  
 ↓  
Resume Changes  
 ↓  
Candidate Approval  
 ↓  
Final Resume

At the same time, it must support:

* ownership/security  
* immutable resume history  
* AI auditability  
* semantic search  
* future scalability  
* clean migrations  
* provider/model version tracking

---

# **15.2 Database Technology**

### **V1**

PostgreSQL  
    \+  
pgvector  
    \+  
SQLAlchemy  
    \+  
Alembic

### **Why PostgreSQL?**

It gives us:

* strong relational integrity  
* transactions  
* constraints  
* indexing  
* JSON/JSONB support  
* excellent Python/FastAPI ecosystem  
* pgvector support  
* straightforward migration to managed PostgreSQL later

We do **not** need a separate vector database for V1.

---

# **15.3 Database Design Principle**

The most important conceptual distinction is:

Career Profile  
      ↓  
Trusted Candidate Information  
      ↓  
Career Claims  
      ↓  
Resume  
      ↓  
Derived Output

Therefore:

> **The resume is not the source of truth.**

A resume can change for every job.

The underlying Career Profile and approved claims should remain the canonical candidate information.

---

# **15.4 Entity Overview**

Our V1 database contains these major groups.

### **Identity**

users  
career\_profiles

### **Career data**

experiences  
projects  
education  
certifications  
skills  
candidate\_skills

### **Trust/evidence**

career\_claims  
evidence  
claim\_evidence

### **Jobs**

jobs  
job\_requirements

### **Matching**

candidate\_job\_matches  
match\_details

### **Resume**

resume\_files  
resumes  
resume\_versions  
resume\_changes  
approvals

### **AI**

ai\_operations  
career\_claim\_embeddings  
job\_requirement\_embeddings  
---

# **15.5 Entity Relationship Overview**

                        ┌─────────────┐  
                         │    users    │  
                         └──────┬──────┘  
                                │ 1:1  
                                ↓  
                     ┌────────────────────┐  
                     │ career\_profiles    │  
                     └─────────┬──────────┘  
                               │  
             ┌─────────────────┼──────────────────┐  
             ↓                 ↓                  ↓  
       experiences         projects            skills  
             │                 │                  │  
             └──────────┬──────┘                  ↓  
                        ↓                    candidate\_skills  
                  career\_claims  
                        │  
                        ↓  
                    evidence  
                        │  
                  claim\_evidence

users ──────────────── jobs  
                         │  
                         ↓  
                  job\_requirements  
                         │  
                         ↓  
               candidate\_job\_matches  
                         │  
                         ↓  
                   match\_details  
                         │  
                         ↓  
                  career\_claims

career\_profiles  
       │  
       ↓  
    resumes  
       │  
       ↓  
 resume\_versions  
       │  
       ↓  
 resume\_changes  
       │  
       ↓  
   approvals  
---

# **15.6 `users`**

This is our authentication root entity.

### **Fields**

users  
────────────────────────  
id  
email  
password\_hash  
is\_active  
created\_at  
updated\_at  
last\_login\_at

### **Constraints**

id → PRIMARY KEY  
email → UNIQUE  
email → NOT NULL  
password\_hash → NOT NULL

Important:

We store:

password\_hash

never:

password  
---

# **15.7 `career_profiles`**

One user has one primary Career Profile.

career\_profiles  
────────────────────────  
id  
user\_id  
full\_name  
headline  
summary  
phone  
location  
linkedin\_url  
github\_url  
portfolio\_url  
created\_at  
updated\_at

Relationship:

users  
  1  
  │  
  │  
  1  
career\_profiles

Constraint:

user\_id UNIQUE

This ensures:

> one primary profile per user.

---

# **15.8 `experiences`**

Professional/other work experience.

experiences  
────────────────────────  
id  
career\_profile\_id  
company\_name  
job\_title  
location  
employment\_type  
start\_date  
end\_date  
description  
is\_current  
created\_at  
updated\_at

### **Important rule**

Current experience:

end\_date \= NULL

is valid.

Historical experience:

start\_date \<= end\_date

must be enforced.

We should calculate experience duration from:

start\_date  
\+  
end\_date

rather than storing:

"2.5 years"

as the authoritative value.

---

# **15.9 `projects`**

projects  
────────────────────────  
id  
career\_profile\_id  
name  
description  
role  
start\_date  
end\_date  
project\_url  
created\_at  
updated\_at

Projects are particularly important because:

Professional experience  
≠  
Personal project

Our system must preserve this distinction.

---

# **15.10 `education`**

education  
────────────────────────  
id  
career\_profile\_id  
institution  
degree  
field\_of\_study  
start\_date  
end\_date  
grade  
description  
created\_at  
updated\_at  
---

# **15.11 `certifications`**

certifications  
────────────────────────  
id  
career\_profile\_id  
name  
issuing\_organization  
issue\_date  
expiry\_date  
credential\_id  
credential\_url  
created\_at  
updated\_at  
---

# **15.12 `skills`**

This is our normalized skill dictionary.

Example:

Python  
Python Backend  
PostgreSQL  
FastAPI  
Docker  
Kubernetes  
React  
AWS

Schema:

skills  
────────────────────────  
id  
name  
normalized\_name  
category  
created\_at  
updated\_at

We can later have aliases:

Postgres  
PostgreSQL  
Postgre SQL

mapped to:

PostgreSQL

The exact normalization dictionary can evolve.

---

# **15.13 `candidate_skills`**

This connects a candidate to a skill.

candidate\_skills  
────────────────────────  
id  
career\_profile\_id  
skill\_id  
experience\_type  
proficiency  
years\_used  
first\_used  
last\_used  
status  
created\_at  
updated\_at

Unique constraint:

(career\_profile\_id, skill\_id)

But there is an important architectural point:

### **`years_used` should not become our ultimate source of truth.**

Where possible:

experience dates  
\+  
career claims

should be used to calculate actual experience.

`years_used` can be treated as a candidate/profile-level supporting value rather than the sole authoritative calculation.

---

# **15.14 `career_claims`**

This is one of our most important tables.

career\_claims  
────────────────────────  
id  
career\_profile\_id  
claim\_type  
claim\_text  
experience\_type  
status  
confidence  
start\_date  
end\_date  
experience\_id  
project\_id  
skill\_id  
created\_at  
updated\_at

Example:

> Developed REST APIs using Python at Company A from 2024–2026.

This claim can connect to:

skill → Python  
experience → Company A role  
---

# **15.15 Claim Status**

We finalized these statuses conceptually:

EVIDENCE\_BACKED  
CANDIDATE\_CONFIRMED  
SELF\_DECLARED  
NEEDS\_CLARIFICATION  
UNSUPPORTED

Important distinction:

### **Evidence-backed**

Means:

> Candidate provided supporting evidence.

It does **not** mean:

> Independently verified by an employer.

### **Candidate-confirmed**

Means:

> Candidate explicitly approved/confirmed the claim.

---

# **15.16 Experience Type**

Use:

PROFESSIONAL  
PERSONAL  
ACADEMIC  
LEARNING

This is essential for matching.

Example:

Python  
Professional  
3 years

is fundamentally different from:

Python  
Learning  
3 years  
---

# **15.17 `evidence`**

Evidence represents candidate-provided support.

evidence  
────────────────────────  
id  
career\_profile\_id  
evidence\_type  
title  
description  
file\_id  
external\_url  
source\_text  
created\_at  
updated\_at

Potential evidence:

resume  
project documentation  
certificate  
portfolio  
candidate-provided document  
external reference

External verification is **not V1**.

---

# **15.18 `claim_evidence`**

Many-to-many relationship:

career\_claims  
       ↕  
claim\_evidence  
       ↕  
evidence  
claim\_evidence  
────────────────────────  
claim\_id  
evidence\_id  
relationship\_type  
created\_at

Primary key:

(claim\_id, evidence\_id)  
---

# **15.19 `jobs`**

jobs  
────────────────────────  
id  
user\_id  
title  
company\_name  
description  
source  
location  
created\_at  
updated\_at

The candidate owns the saved job.

V1 initially focuses on:

> JD pasted into the application.

No scraping/integrations yet.

---

# **15.20 `job_requirements`**

The LLM transforms the raw JD into structured requirements.

job\_requirements  
────────────────────────  
id  
job\_id  
requirement\_text  
requirement\_type  
importance  
skill\_id  
minimum\_years  
experience\_type  
created\_at  
updated\_at

Example:

requirement\_text:  
3+ years of Python backend development

requirement\_type:  
REQUIRED

importance:  
1.0

skill:  
Python

minimum\_years:  
3

experience\_type:  
PROFESSIONAL  
---

# **15.21 Requirement Type**

V1:

REQUIRED  
PREFERRED  
CONTEXTUAL

This matters because:

Required Python

should have greater impact than:

Nice-to-have Docker  
---

# **15.22 `candidate_job_matches`**

This stores the overall result.

candidate\_job\_matches  
────────────────────────  
id  
career\_profile\_id  
job\_id  
overall\_score  
skill\_score  
experience\_score  
education\_score  
keyword\_score  
semantic\_score  
status  
created\_at  
updated\_at

### **Important terminology**

We will call this:

> **Job Alignment Score**

not:

> ATS Score

because there is no universal ATS algorithm.

---

# **15.23 `match_details`**

Per requirement:

match\_details  
────────────────────────  
id  
match\_id  
job\_requirement\_id  
career\_claim\_id  
match\_type  
score  
explanation  
created\_at

Example:

Requirement:  
3+ years professional Python

Claim:  
2.4 years professional Python

Result:  
PARTIAL\_MATCH

Score:  
0.80

Explanation:  
Candidate has relevant professional Python experience,  
but the available experience is below the stated 3-year minimum.  
---

# **15.24 Match Types**

STRONG\_MATCH  
PARTIAL\_MATCH  
GAP  
UNKNOWN

### **Why UNKNOWN?**

Because:

> absence of evidence is not always evidence of absence.

For example, if the candidate hasn't provided enough information to determine whether they have a skill, we should not automatically call it a GAP.

---

# **15.25 Resume Architecture**

Resume storage has multiple layers.

resume\_files  
      ↓  
resumes  
      ↓  
resume\_versions  
      ↓  
resume\_changes  
      ↓  
approvals

This gives us traceability.

---

# **15.26 `resume_files`**

Represents uploaded physical files.

resume\_files  
────────────────────────  
id  
user\_id  
original\_filename  
storage\_key  
mime\_type  
file\_size  
checksum  
created\_at

The actual file content is stored by:

StorageProvider

not inside PostgreSQL.

---

# **15.27 `resumes`**

Represents a logical resume.

resumes  
────────────────────────  
id  
career\_profile\_id  
resume\_file\_id  
name  
resume\_type  
created\_at  
updated\_at  
---

# **15.28 `resume_versions`**

Every meaningful resume state should be preserved.

resume\_versions  
────────────────────────  
id  
resume\_id  
version\_number  
content\_snapshot  
source  
status  
created\_at

### **Critical rule**

`content_snapshot` is immutable.

Suppose:

Version 1

is generated for Job A.

Later we generate:

Version 2

for Job B.

Version 1 must not magically change.

This gives us historical reproducibility.

---

# **15.29 `resume_changes`**

This is our explainability layer.

resume\_changes  
────────────────────────  
id  
resume\_version\_id  
change\_type  
original\_text  
proposed\_text  
reason  
career\_claim\_id  
validation\_status  
created\_at  
updated\_at

Example:

Original:  
Worked on APIs.

Proposed:  
Developed REST APIs using Python.

Reason:  
Better alignment with the job's Python backend requirement.

Claim:  
claim\_123

Validation:  
PASS  
---

# **15.30 `approvals`**

Candidate decision:

approvals  
────────────────────────  
id  
resume\_change\_id  
decision  
edited\_text  
decided\_at

Possible decisions:

APPROVED  
REJECTED  
EDITED

This creates:

AI proposal  
     ↓  
Candidate decision  
     ↓  
Approved resume  
---

# **15.31 `ai_operations`**

Every meaningful AI operation can be audited.

ai\_operations  
────────────────────────  
id  
user\_id  
job\_id  
resume\_id  
operation\_type  
provider  
model  
prompt\_version  
input\_hash  
output\_json  
status  
error\_code  
created\_at

This allows us to answer:

> Which model produced this?

> Which prompt version was used?

> What happened when the operation failed?

> Can we reproduce/debug the operation?

---

# **15.32 Vector Tables**

We'll initially use pgvector for:

career\_claim\_embeddings  
job\_requirement\_embeddings

Conceptually:

career\_claim\_embeddings  
────────────────────────  
id  
career\_claim\_id  
embedding  
embedding\_model  
embedding\_dimension  
created\_at

and:

job\_requirement\_embeddings  
────────────────────────  
id  
job\_requirement\_id  
embedding  
embedding\_model  
embedding\_dimension  
created\_at

The exact vector dimension must match the selected embedding model.

Therefore:

> **Embedding model selection must happen before the final migration containing the vector dimension.**

We should avoid hardcoding a random dimension now.

---

# **15.33 Why Not Store Everything as JSON?**

We could technically put the entire profile into:

candidate\_profile JSONB

but that would make important operations difficult:

Find candidates with Python  
Calculate professional experience  
Link evidence  
Track claims  
Match requirements  
Maintain relational integrity

Therefore we use:

> **Relational data for core facts \+ JSONB only where flexible AI/audit payloads make sense.**

Good JSONB candidate:

ai\_operations.output\_json

Bad candidate:

entire candidate career history  
---

# **15.34 Indexing Strategy**

Important indexes will include:

users.email  
career\_profiles.user\_id  
experiences.career\_profile\_id  
projects.career\_profile\_id  
candidate\_skills.career\_profile\_id  
career\_claims.career\_profile\_id  
evidence.career\_profile\_id  
jobs.user\_id  
job\_requirements.job\_id  
candidate\_job\_matches.(career\_profile\_id, job\_id)  
resume\_files.user\_id  
resumes.career\_profile\_id  
resume\_versions.resume\_id  
resume\_changes.resume\_version\_id  
ai\_operations.user\_id

Vector indexes will be added after embedding model/dimension decisions.

---

# **15.35 Cascading Rules**

We need to be careful with deletion.

For example:

User  
 ↓  
Career Profile  
 ↓  
Claims

If a user permanently deletes their account, dependent personal data may need cascading deletion.

But we should **not casually cascade everything** where historical/audit requirements matter.

For V1, we'll explicitly define deletion behavior during implementation.

This is:

> **TO BE FINALIZED**

rather than making assumptions now.

---

# **15.36 SQLAlchemy Model Strategy**

We'll use SQLAlchemy 2.x-style models.

Conceptually:

class User(Base):  
    \_\_tablename\_\_ \= "users"

    id: Mapped\[UUID\] \= mapped\_column(...)  
    email: Mapped\[str\] \= mapped\_column(  
        String,  
        unique=True,  
        index=True,  
        nullable=False,  
    )  
    password\_hash: Mapped\[str\] \= mapped\_column(...)

Relationships will use SQLAlchemy relationships rather than manually duplicating relationship logic.

---

# **15.37 UUIDs vs Integer IDs**

For this project, I recommend:

> **UUID primary keys.**

Why?

* safer to expose publicly  
* avoids predictable sequential IDs  
* easier future distributed architecture  
* good fit for externally visible resource identifiers

Example:

job\_id:  
550e8400-e29b-41d4-a716-446655440000

instead of:

job\_id:  
123

This is now the recommended V1 choice.

---

# **15.38 Timestamps**

Use UTC timestamps at the database/application boundary.

Standard fields:

created\_at  
updated\_at

Additional timestamps where meaningful:

last\_login\_at  
decided\_at

The frontend converts them to the user's local timezone.

---

# **15.39 Soft Delete**

We should **not add `deleted_at` to every table automatically**.

That is over-engineering for V1.

Only entities that genuinely require recoverability/history should receive special deletion treatment.

This remains a future refinement unless required by a specific workflow.

---

# **15.40 Migration Strategy**

Use:

Alembic

Flow:

Modify SQLAlchemy model  
          ↓  
Alembic revision  
          ↓  
Review migration  
          ↓  
Run migration  
          ↓  
PostgreSQL

Never blindly rely on:

Base.metadata.create\_all()

as the application's schema evolution mechanism.

---

# **15.41 Initial Migration Strategy**

Rather than creating one enormous migration, we'll use logical migration stages.

### **Migration 001**

users  
career\_profiles

### **Migration 002**

experiences  
projects  
education  
certifications  
skills  
candidate\_skills

### **Migration 003**

career\_claims  
evidence  
claim\_evidence

### **Migration 004**

jobs  
job\_requirements

### **Migration 005**

candidate\_job\_matches  
match\_details

### **Migration 006**

resume\_files  
resumes  
resume\_versions  
resume\_changes  
approvals

### **Migration 007**

ai\_operations

### **Migration 008**

vector tables \+ pgvector indexes

This makes debugging much easier.

---

# **15.42 Important Database Rules**

These are now **non-negotiable**:

### **Rule 1**

Career Profile \> Resume

The profile/claims remain the source of truth.

### **Rule 2**

Dates are authoritative for experience duration.

### **Rule 3**

Experience type must never be silently changed.

### **Rule 4**

AI proposals cannot directly update trusted claims.

### **Rule 5**

Approved resume versions remain historically immutable.

### **Rule 6**

Candidate ownership must be enforced.

### **Rule 7**

Evidence relationships must be traceable.

### **Rule 8**

AI operations should be auditable.

### **Rule 9**

Vector similarity cannot override business rules.

### **Rule 10**

Schema migrations must be version-controlled.

---

# **15.43 Database → Application Flow**

Example:

JD  
 ↓  
LLM  
 ↓  
JobRequirement  
 ↓  
Embedding  
 ↓  
pgvector  
 ↓  
Relevant CareerClaims  
 ↓  
MatchingService  
 ↓  
MatchDetails  
 ↓  
JobAlignmentScore

And:

Resume  
 ↓  
Extraction  
 ↓  
Candidate review  
 ↓  
CareerClaim  
 ↓  
Evidence  
 ↓  
Trusted profile  
---

# **15.44 Step 15 Completion Criteria**

Before moving forward, our database foundation should satisfy:

* PostgreSQL selected  
* pgvector selected  
* SQLAlchemy selected  
* Alembic selected  
* Core entities defined  
* Relationships defined  
* Ownership model defined  
* Career Claims/Evidence model defined  
* Matching model defined  
* Resume versioning defined  
* Approval workflow persistence defined  
* AI audit model defined  
* Vector storage defined conceptually  
* Index strategy defined  
* UUID strategy selected  
* Timestamp strategy selected  
* Migration strategy defined  
* V1 database boundaries defined

### **Still TO BE FINALIZED during implementation**

1. Exact PostgreSQL version  
2. Exact SQLAlchemy version  
3. Exact pgvector/extension setup  
4. Exact embedding model and vector dimension  
5. Exact enum implementation strategy  
6. Deletion/cascade policy  
7. Exact database indexes after query profiling  
8. Production connection pooling configuration

# step 16

Yes. And for **this particular project**, I would actually change our thinking slightly.

If our priority order is:

1. **Extraction accuracy**  
2. **Structured-output reliability**  
3. **No hallucination / no invented candidate information**  
4. **Consistent results**  
5. **Good reasoning over resume text**  
6. Cost  
7. Local/offline capability

then **Ollama should not automatically be our primary LLM**.

Ollama is excellent as an infrastructure/runtime option, but the *model running through Ollama* is what determines extraction quality. And for a system where incorrect extraction can contaminate a candidate's Career Profile, we should optimize for reliability first.

### **My recommendation**

For V1, I would use:

> **Primary LLM: Gemini API**  
> **Optional local LLM: Ollama**  
> **Architecture: Provider abstraction so either can be swapped without changing business logic.**

Gemini has first-class structured-output support with JSON Schema/Pydantic, and Google's documentation explicitly positions structured outputs for data extraction. It also explicitly warns that schema compliance does **not** guarantee semantic correctness—which fits our architecture perfectly because we still run our own validators afterward. ([Google AI for Developers](https://ai.google.dev/gemini-api/docs/get-started?utm_source=chatgpt.com))

So our architecture becomes:

                   ┌─────────────────────┐  
                    │ Resume / JD / Claims │  
                    └──────────┬──────────┘  
                               │  
                               ▼  
                    ┌─────────────────────┐  
                    │    LLMProvider      │  
                    │     Interface       │  
                    └──────────┬──────────┘  
                               │  
                 ┌─────────────┴─────────────┐  
                 │                           │  
                 ▼                           ▼  
        ┌────────────────┐          ┌────────────────┐  
        │ Gemini Provider│          │ Ollama Provider│  
        │   PRIMARY      │          │    OPTIONAL    │  
        └────────────────┘          └────────────────┘  
                 │                           │  
                 └─────────────┬─────────────┘  
                               ▼  
                    ┌─────────────────────┐  
                    │ Structured JSON     │  
                    │ Pydantic Validation │  
                    └──────────┬──────────┘  
                               ▼  
                    ┌─────────────────────┐  
                    │ Business Validation │  
                    │ Truth Validation    │  
                    └──────────┬──────────┘  
                               ▼  
                    ┌─────────────────────┐  
                    │ Candidate Review   │  
                    └─────────────────────┘

## **Why I prefer Gemini for our V1**

The important thing isn't simply "Gemini is smarter."

It's that we can explicitly tell the model:

Return exactly this schema.  
Do not add fields.  
Do not infer facts.  
Do not invent dates.  
Do not infer professional experience.  
Do not convert learning into professional experience.  
If information is ambiguous, return null / NEEDS\_CLARIFICATION.

And then provide a Pydantic schema.

For example:

class ExperienceExtraction(BaseModel):  
    company: str | None  
    role: str | None  
    start\_date: date | None  
    end\_date: date | None  
    responsibilities: list\[str\]  
    technologies: list\[str\]  
    experience\_type: ExperienceType

Gemini's structured-output mechanism can accept a JSON schema generated from Pydantic and return schema-conforming JSON. ([Google AI for Developers](https://ai.google.dev/gemini-api/docs/get-started?utm_source=chatgpt.com))

But there's a **very important point**:

> Structured output does NOT mean truthful output.

For example, Gemini could correctly return:

{  
  "company": "ABC Technologies",  
  "role": "Backend Developer",  
  "start\_date": "2022-01-01",  
  "end\_date": "2025-01-01",  
  "technologies": \["Python", "FastAPI", "Kubernetes"\]  
}

The JSON may be perfectly valid.

But perhaps the resume never actually said Kubernetes.

Therefore:

LLM structured output  
        ↓  
Pydantic validation  
        ↓  
Semantic/factual validation  
        ↓  
Candidate review  
        ↓  
Trusted Career Profile

That distinction is **fundamental to our project**.

Google's own documentation makes essentially the same distinction: structured output guarantees schema-conforming output, but application-side validation is still required for semantically incorrect results. ([Google AI for Developers](https://ai.google.dev/gemini-api/docs/structured-output?authuser=14&hl=en&utm_source=chatgpt.com))

---

# **What about OpenAI?**

There is another strong option:

> **OpenAI API**

For pure quality/reliability, I would absolutely include it in our evaluation.

So I would not lock ourselves into:

Gemini vs Ollama

Instead, benchmark:

Gemini  
OpenAI  
Ollama \+ selected local model

on **our actual resume extraction task**.

That's much more meaningful than generic benchmark scores.

For example, we can take 10–20 realistic resumes and test:

### **Test 1 — Basic extraction**

Can it correctly identify:

* name  
* email  
* phone  
* location  
* summary  
* companies  
* job titles  
* dates  
* projects  
* education  
* certifications  
* skills?

### **Test 2 — Difficult resume**

Two-column resume:

Experience       Skills  
Company A        Python  
Company B        FastAPI  
Project X        PostgreSQL

Which model correctly associates information?

### **Test 3 — Ambiguous experience**

Resume:

> "Built a personal Kubernetes cluster to learn container orchestration."

Bad extraction:

experience\_type \= PROFESSIONAL  
skill \= Kubernetes

Correct:

experience\_type \= PERSONAL  
skill \= Kubernetes

### **Test 4 — Learning vs professional**

Resume:

> "Completed a course on AWS."

We must NOT get:

AWS professional experience

### **Test 5 — Missing dates**

Resume:

> Backend Developer — ABC Technologies

No dates.

Model should return:

{  
    "start\_date": null,  
    "end\_date": null  
}

rather than guessing.

### **Test 6 — Structured-output failure**

Give intentionally difficult text and see:

* Does JSON remain valid?  
* Does schema remain valid?  
* Does the model invent values?  
* Does it omit uncertain values?  
* Does it return unexpected fields?

### **Test 7 — Claim extraction**

This is especially important for us.

Resume:

> Developed REST APIs using Python and FastAPI for an internal project.

We want:

Claim:  
Developed REST APIs using Python and FastAPI.

Experience type:  
PROFESSIONAL / PERSONAL / UNKNOWN

Evidence:  
Resume

Source:  
Resume section / text span

Not:

> Architected scalable microservices infrastructure.

That would be an **AI-created strengthening**, which our system must prevent.

---

# **I would actually make the architecture provider-neutral**

Instead of:

LLM\_PROVIDER=ollama

being deeply embedded throughout the application, keep:

LLM\_PROVIDER=gemini

and:

LLM\_FALLBACK\_PROVIDER=ollama

or potentially:

LLM\_PROVIDER=openai  
LLM\_FALLBACK\_PROVIDER=gemini

Then:

class LLMProvider(ABC):

    @abstractmethod  
    async def generate\_structured(  
        self,  
        prompt: str,  
        schema: type\[BaseModel\],  
    ) \-\> BaseModel:  
        ...

Implementation:

LLMProvider  
   │  
   ├── GeminiProvider  
   │  
   ├── OpenAIProvider  
   │  
   └── OllamaProvider

Your business logic doesn't care which one is underneath.

---

# **One important correction to our previous fallback idea**

I **would not automatically use Ollama as a fallback for Gemini for every failure.**

For example:

Gemini  
   ↓  
invalid business result  
   ↓  
Ollama

❌ No.

That could actually make the system worse.

Instead:

### **Infrastructure failure**

Gemini  
   ↓  
timeout / unavailable  
   ↓  
Ollama

Potentially yes.

### **Schema failure**

Gemini  
   ↓  
invalid JSON/schema  
   ↓  
retry / controlled recovery

Potentially yes.

### **Truth/business validation failure**

Gemini  
   ↓  
claim says 5 years  
but evidence says 2 years  
   ↓  
BLOCK

❌ Do NOT send to Ollama just because we don't like the answer.

The problem isn't the provider.

The problem is the **candidate information**.

---

# **What about cost?**

This is where Ollama remains very valuable.

### **Development**

We could run:

Ollama  
\+  
local embedding model  
\+  
PostgreSQL  
\+  
pgvector  
\+  
FastAPI  
\+  
React

for essentially zero API cost.

That makes Ollama useful for:

* development  
* prompt development  
* testing  
* experimenting  
* offline development  
* regression testing

### **Production-quality extraction**

We could use:

Gemini / OpenAI

for the actual high-value operations.

For example:

Resume extraction       → Gemini  
JD analysis             → Gemini  
Claim interpretation    → Gemini  
Resume optimization     → Gemini  
Claim validation        → Gemini \+ rules  
Embeddings              → local BGE

This gives us a very strong hybrid.

---

# **And I would NOT use an LLM for everything**

This is probably the most important architecture decision.

For example:

### **LLM**

"3+ years Python backend development"

understands:

skill \= Python  
domain \= backend  
minimum\_experience \= 3 years  
experience\_type \= professional

### **Python rules**

Then calculate:

Candidate Python professional experience:  
2.4 years

Therefore:

Required: 3 years  
Candidate: 2.4 years

Result:  
PARTIAL\_MATCH

The LLM should **not** decide that mathematically.

Similarly:

Resume:  
Jan 2023 → Dec 2024

Python calculates:

\~2 years

not the LLM.

This is how we get reliable results.

---

# **My proposed V1 AI stack**

I would now change our Step 16 architecture to:

| Component | V1 decision |
| ----- | ----- |
| Primary LLM | **Gemini API** |
| Local LLM | **Ollama** |
| OpenAI | Optional provider for benchmarking/production choice |
| Embeddings | **BAAI/bge-small-en-v1.5** |
| Embedding dimensions | **384** |
| Structured output | **JSON Schema \+ Pydantic** |
| Business validation | Python |
| Truth validation | Python \+ LLM |
| Candidate confirmation | Required |
| LLM direct DB write | Never |
| LLM decides truth | Never |
| OCR | Future |
| Redis | No |
| Queue | No |

And I'd make one further distinction:

### **High-risk operations**

Use the strongest available provider/model:

Career Claim extraction  
Career Claim validation  
JD requirement interpretation  
Resume optimization  
Final resume validation

### **Lower-risk operations**

Potentially local:

basic extraction  
normalization  
section detection  
text classification  
development/testing  
---

# **But should we immediately choose Gemini?**

**Not yet.**

I think the technically correct next step is to **benchmark Gemini vs OpenAI vs Ollama using our actual Step 16 extraction schema**.

Not generic LLM benchmarks.

We create a small evaluation set:

10–20 resumes

including:

* simple resume  
* complex resume  
* two-column resume  
* fresher resume  
* experienced developer  
* projects-heavy resume  
* missing dates  
* ambiguous experience  
* multiple technologies  
* learning/certification-heavy resume  
* deliberately difficult formatting

Then measure:

                   Gemini   OpenAI   Ollama  
\------------------------------------------------  
Schema validity       100%      ?        ?  
Field accuracy         ?        ?        ?  
Date accuracy          ?        ?        ?  
Skill accuracy         ?        ?        ?  
Experience type        ?        ?        ?  
Hallucination rate     ?        ?        ?  
Missing-value handling ?        ?        ?  
Claim accuracy         ?        ?        ?  
Latency                ?        ?        ?  
Cost                   ?        ?        ?

Then we select the winner **based on our product's requirements**, not marketing or generic benchmarks.

## **My current expectation**

If we prioritize **quality \+ structured extraction reliability** over zero API cost:

**Gemini / OpenAI \> a small local Ollama model**

is the direction I would expect.

If we prioritize **zero cost \+ privacy \+ offline development**:

**Ollama wins.**

Therefore, the best architecture for *our* project isn't choosing one and throwing the others away.

It is:

> **Provider abstraction \+ Gemini as the likely production-quality primary \+ Ollama as the local development/testing provider \+ optional OpenAI provider.**

And because our **Career Claims system, deterministic validators, candidate approval, and immutable evidence trail** sit between the LLM and the trusted database, even a strong LLM never gets to silently become the source of truth.

That is the architecture I would recommend for an ATS product where **accuracy is more important than simply having an AI feature**.

# step 17

Absolutely. Let's move ahead.

### **Step 17 — Career Profile \+ Career Claims & Evidence**

This is the next critical step because it turns the **resume extraction output into the trusted Career Knowledge Base** that everything else—JD matching, gap analysis, optimization, and final resume generation—will depend on.

Our flow is now:

Resume  
  ↓  
Extraction  
  ↓  
Candidate Review  
  ↓  
Career Profile  
  ↓  
Career Claims  
  ↓  
Evidence  
  ↓  
Trusted Career Knowledge Base  
  ↓  
JD Matching  
  ↓  
Resume Optimization

For Step 17, I suggest we finalize these areas **before writing code**:

1. Career Profile structure  
2. Experience / Project / Education / Certification data model  
3. Skills and normalized skills  
4. Career Claims model  
5. Evidence model  
6. Claim ↔ Evidence relationships  
7. Claim statuses and trust rules  
8. Candidate confirmation/edit/rejection workflow  
9. What AI can and cannot change  
10. Backend APIs  
11. Database relationships and constraints  
12. Frontend Career Profile UI  
13. Claim review UI  
14. Validation rules  
15. Audit/history requirements  
16. Exact implementation structure  
17. Test cases  
18. Final Step 17 decisions

The key principle we'll preserve throughout:

> **The Career Profile is the candidate's trusted source of truth. The resume is only one source of evidence.**

And:

> **AI proposes → validation checks → candidate confirms → trusted data is saved.**

Let's start Step 17 from the **data model and trust model**, because those decisions will determine both the backend schema and frontend UI.

Great. Let's move forward with **Step 17 — Career Profile \+ Career Claims & Evidence**.

This is one of the most important parts of the entire ATS because it becomes the **trusted source of truth** for every future AI operation.

# **Step 17 — Career Profile \+ Career Claims & Evidence**

## **17.1 What are we building?**

After the candidate uploads a resume and reviews the AI extraction, we need to convert the approved information into a structured career database.

For example, instead of storing only:

> “Backend Developer with 2.5 years of Python experience...”

we store structured information:

Candidate  
│  
├── Personal Information  
│  
├── Professional Experience  
│   ├── Company A  
│   │   ├── Backend Developer  
│   │   ├── Jan 2024 → Present  
│   │   ├── Python  
│   │   ├── FastAPI  
│   │   └── PostgreSQL  
│   │  
│   └── Company B  
│  
├── Projects  
│   ├── AI Document Assistant  
│   └── ATS Platform  
│  
├── Education  
│  
├── Certifications  
│  
├── Skills  
│  
└── Career Claims  
    ├── Python backend development  
    ├── FastAPI API development  
    ├── PostgreSQL  
    └── AI/ML project experience

The **Career Claims** layer is what makes our system different from a normal resume builder.

---

# **17.2 Career Profile vs Career Claims**

These should **not** be the same thing.

### **Career Profile**

Contains structured career information.

For example:

Experience:  
Company: ABC Technologies  
Role: Backend Developer  
Start: 2024-01  
End: Present

### **Career Claim**

Represents a factual statement that the system may use when matching or generating a resume.

For example:

> “Developed backend APIs using Python and FastAPI at ABC Technologies.”

The distinction is important because one experience can support many claims.

Experience  
     │  
     ├── Claim: Python backend development  
     ├── Claim: FastAPI API development  
     ├── Claim: PostgreSQL usage  
     └── Claim: REST API development  
---

# **17.3 Final Career Profile structure**

I recommend this structure:

CareerProfile  
│  
├── Basic Information  
│  
├── Experiences  
│  
├── Projects  
│  
├── Education  
│  
├── Certifications  
│  
├── Skills  
│  
└── Career Claims  
       │  
       └── Evidence

Database-wise:

users  
  │  
  └── career\_profiles  
         │  
         ├── experiences  
         ├── projects  
         ├── education  
         ├── certifications  
         ├── candidate\_skills  
         │  
         └── career\_claims  
                  │  
                  └── claim\_evidence  
                           │  
                           └── evidence  
---

# **17.4 Personal Information**

We should keep personal information relatively simple.

career\_profiles  
\----------------  
id  
user\_id  
headline  
summary  
location  
linkedin\_url  
github\_url  
portfolio\_url  
created\_at  
updated\_at

Email and authentication information should remain under `users`.

For example:

users  
\-----  
id  
email  
password\_hash  
created\_at  
updated\_at

Don't duplicate authentication information inside Career Profile.

---

# **17.5 Experience**

experiences  
\-----------  
id  
career\_profile\_id  
company\_name  
job\_title  
employment\_type  
location  
start\_date  
end\_date  
is\_current  
description  
created\_at  
updated\_at

### **Important**

We should **not** store:

experience\_duration \= "2.5 years"

Instead:

start\_date \= 2024-01-01  
end\_date \= NULL  
is\_current \= true

Then Python calculates duration.

This prevents inconsistencies.

---

# **17.6 Experience Type**

This becomes particularly important for our AI validation.

Use:

PROFESSIONAL  
PERSONAL  
ACADEMIC  
LEARNING

Example:

| Activity | Type |
| ----- | ----- |
| Backend Developer at company | PROFESSIONAL |
| Personal Kubernetes project | PERSONAL |
| University project | ACADEMIC |
| Udemy AWS course | LEARNING |

This prevents a major ATS problem:

> Turning something the candidate learned into something the candidate professionally did.

---

# **17.7 Projects**

projects  
\--------  
id  
career\_profile\_id  
name  
description  
role  
start\_date  
end\_date  
url  
created\_at  
updated\_at

Projects should also have technologies/skills associated with them.

For example:

AI Document Q\&A  
│  
├── Python  
├── FastAPI  
├── PostgreSQL  
├── pgvector  
└── LLM

But again:

> Project usage does NOT automatically become professional experience.

---

# **17.8 Education**

education  
\---------  
id  
career\_profile\_id  
institution  
degree  
field\_of\_study  
start\_date  
end\_date  
grade  
description  
created\_at  
updated\_at

We shouldn't force every candidate to provide every field.

For example:

grade \= NULL

is perfectly valid.

---

# **17.9 Certifications**

certifications  
\--------------  
id  
career\_profile\_id  
name  
issuing\_organization  
issue\_date  
expiration\_date  
credential\_id  
credential\_url  
description  
created\_at  
updated\_at

Again, don't allow the AI to invent certification information.

---

# **17.10 Skills**

Skills require a little more thought.

Instead of storing:

candidate\_skills  
\----------------  
skill\_name

we should normalize skills.

For example:

Python  
python  
PYTHON  
Python 3

should map to the same canonical skill where appropriate.

So:

skills  
\------  
id  
name  
normalized\_name  
category

and:

candidate\_skills  
\----------------  
id  
career\_profile\_id  
skill\_id  
proficiency  
years\_of\_experience

However, there's an important rule:

### **`years_of_experience` should not be manually trusted.**

If we eventually calculate it from Career Claims/Experiences, that's preferable.

So for V1, we can keep the field nullable or omit it until we have a robust calculation model.

---

# **17.11 Career Claims**

This is the heart of Step 17\.

A claim should contain something like:

career\_claims  
\-------------  
id  
career\_profile\_id  
claim\_text  
experience\_type  
status  
skill\_id  
experience\_id  
project\_id  
start\_date  
end\_date  
created\_at  
updated\_at

Example:

Claim:  
"Developed REST APIs using Python and FastAPI."

Experience Type:  
PROFESSIONAL

Status:  
EVIDENCE\_BACKED

Related Skill:  
Python

Related Experience:  
ABC Technologies

Evidence:  
Resume.pdf  
---

# **17.12 Claim Status**

We finalized the following statuses earlier:

EVIDENCE\_BACKED  
CANDIDATE\_CONFIRMED  
SELF\_DECLARED  
NEEDS\_CLARIFICATION  
UNSUPPORTED

But these statuses need precise meanings.

### **EVIDENCE\_BACKED**

There is candidate-provided supporting evidence.

Important:

> This does NOT mean employer-verified.

It means:

> “There is supporting material supplied by the candidate.”

---

### **CANDIDATE\_CONFIRMED**

The candidate explicitly reviewed and confirmed the claim.

Example:

AI extracted:

"Used Kubernetes professionally."

Candidate:  
✓ Yes, this is correct.

Now the claim can become candidate-confirmed.

---

### **SELF\_DECLARED**

Candidate says something is true, but supporting evidence/context isn't sufficient.

Example:

> “I'm familiar with Terraform.”

No supporting project or experience.

---

### **NEEDS\_CLARIFICATION**

The system cannot safely determine the truth.

Example:

> “Worked with AWS.”

But there is no context.

We shouldn't guess whether this means:

* professional experience  
* personal project  
* course  
* certification  
* learning

---

### **UNSUPPORTED**

There is no evidence supporting the claim.

Such claims should **not be used for automatic resume generation**.

---

# **17.13 Evidence**

Evidence is separate from the claim.

evidence  
\--------  
id  
career\_profile\_id  
source\_type  
source\_reference  
content  
content\_hash  
created\_at

Possible source types:

RESUME  
CANDIDATE\_INPUT  
PROJECT\_DESCRIPTION  
EXPERIENCE\_DESCRIPTION  
CERTIFICATION  
OTHER

For V1, we primarily care about:

RESUME  
CANDIDATE\_INPUT  
---

# **17.14 Claim ↔ Evidence**

One claim may have multiple pieces of evidence.

Example:

Claim:  
Python backend development

        │  
        ├── Resume  
        ├── Project description  
        └── Candidate confirmation

Therefore:

claim\_evidence  
\-------------  
claim\_id  
evidence\_id

with:

PRIMARY KEY (claim\_id, evidence\_id)

This was already part of our finalized database design.

---

# **17.15 Very important: evidence isn't proof of truth**

We need to be extremely careful with terminology.

If the candidate uploads a resume saying:

> “Led a team of 10 developers.”

that resume is evidence that:

> **The candidate claims they led 10 developers.**

It is not independent verification that they actually did.

Therefore our UI should say:

> **Candidate-provided evidence**

rather than:

> **Verified by employer**

unless we eventually integrate an external verification system.

---

# **17.16 Candidate review workflow**

Now let's connect Step 16 and Step 17\.

Resume Upload  
      ↓  
Text Extraction  
      ↓  
AI Extraction  
      ↓  
Extraction Proposal  
      ↓  
Candidate Review  
      ↓  
Approved Information  
      ↓  
Career Profile  
      ↓  
Career Claims  
      ↓  
Evidence

The critical boundary is:

AI Output  
   ❌  
   │  
   │ cannot directly become trusted data  
   ▼  
Candidate Review  
   │  
   ├── Confirm  
   ├── Edit  
   └── Reject  
   ▼  
Trusted Career Profile  
---

# **17.17 Example**

Suppose the resume says:

> Backend Developer — XYZ Technologies  
> Jan 2024 – Present  
> Developed REST APIs using Python and FastAPI.

AI extracts:

{  
  "company": "XYZ Technologies",  
  "role": "Backend Developer",  
  "start\_date": "2024-01-01",  
  "end\_date": null,  
  "experience\_type": "PROFESSIONAL",  
  "technologies": \[  
    "Python",  
    "FastAPI"  
  \]  
}

Candidate clicks:

**Confirm**

Then we create:

Experience  
\-----------  
XYZ Technologies  
Backend Developer  
2024-01 → Present  
PROFESSIONAL

And claims:

Claim 1  
\-------  
Developed REST APIs using Python.  
Claim 2  
\-------  
Developed REST APIs using FastAPI.

Evidence:

Evidence  
\--------  
Source: Resume

Relationships:

Experience  
    │  
    ├──── Claim 1  
    │        │  
    │        └── Resume Evidence  
    │  
    └──── Claim 2  
             │  
             └── Resume Evidence  
---

# **17.18 What happens if the candidate edits it?**

Suppose AI says:

> “Developed REST APIs using Python and FastAPI.”

Candidate changes it to:

> “Developed backend APIs using Python.”

We should **store the candidate-approved version**, not silently overwrite the AI extraction history.

The audit trail should show:

AI proposal:  
Developed REST APIs using Python and FastAPI.

Candidate action:  
EDITED

Final claim:  
Developed backend APIs using Python.

This becomes valuable later when debugging AI behavior.

---

# **17.19 What happens when candidate rejects something?**

Example:

AI extracts:

> Kubernetes

Candidate says:

> ❌ I only studied Kubernetes. I never used it.

Then:

AI proposal  
     ↓  
Candidate rejects  
     ↓  
No trusted Kubernetes professional claim

We may retain the extraction/review history for audit purposes, but it must **not become trusted Career Profile data**.

---

# **17.20 What can AI change?**

### **Allowed**

AI can:

* normalize skill names  
* organize information  
* extract claims  
* associate claims with experiences/projects  
* identify possible evidence  
* suggest categorization  
* detect ambiguity  
* suggest corrections

### **Not allowed**

AI cannot:

* invent skills  
* invent dates  
* increase years  
* invent projects  
* invent responsibilities  
* invent metrics  
* invent certifications  
* turn learning into professional experience  
* turn personal experience into professional experience  
* claim expertise without evidence  
* silently modify trusted information

---

# **17.21 Career Profile editing**

The candidate should always be able to manually edit their profile.

For example:

Career Profile

Personal  
──────────────────  
Name  
Headline  
Location  
Links

Experience  
──────────────────  
\[ABC Technologies\]  
Backend Developer  
Jan 2024 – Present  
\[Edit\]

Projects  
──────────────────  
\[AI Document Assistant\]  
\[Edit\]

Skills  
──────────────────  
Python  
FastAPI  
PostgreSQL  
Docker

Claims  
──────────────────  
✓ Python backend development  
✓ FastAPI API development  
⚠ Kubernetes — Needs clarification  
---

# **17.22 Claim UI**

This should be one of our strongest UX components.

For each claim:

┌─────────────────────────────────────────────┐  
│ Python Backend Development                  │  
│                                             │  
│ "Developed backend APIs using Python."      │  
│                                             │  
│ Experience: ABC Technologies                │  
│ Type: Professional                          │  
│                                             │  
│ Evidence: Resume                            │  
│ Status: Evidence-backed                    │  
│                                             │  
│ \[View Evidence\] \[Edit\] \[Reject\]             │  
└─────────────────────────────────────────────┘

For ambiguous claims:

┌─────────────────────────────────────────────┐  
│ Kubernetes                                  │  
│                                             │  
│ We found Kubernetes mentioned in your       │  
│ resume, but couldn't determine the context. │  
│                                             │  
│ Was this:                                   │  
│                                             │  
│ ○ Professional experience                  │  
│ ○ Personal project                         │  
│ ○ Academic project                         │  
│ ○ Learning / course                        │  
│                                             │  
│ \[Confirm\]                                   │  
└─────────────────────────────────────────────┘

This is much better than allowing the LLM to guess.

---

# **17.23 Backend APIs**

We already have:

GET    /api/v1/profile  
PUT    /api/v1/profile

Now Step 17 should finalize:

GET    /api/v1/profile/claims  
POST   /api/v1/profile/claims  
GET    /api/v1/profile/claims/{id}  
PUT    /api/v1/profile/claims/{id}  
DELETE /api/v1/profile/claims/{id}

Experience:

GET    /api/v1/profile/experiences  
POST   /api/v1/profile/experiences  
PUT    /api/v1/profile/experiences/{id}  
DELETE /api/v1/profile/experiences/{id}

Projects:

GET    /api/v1/profile/projects  
POST   /api/v1/profile/projects  
PUT    /api/v1/profile/projects/{id}  
DELETE /api/v1/profile/projects/{id}

Education:

GET    /api/v1/profile/education  
POST   /api/v1/profile/education  
PUT    /api/v1/profile/education/{id}  
DELETE /api/v1/profile/education/{id}

Certifications:

GET    /api/v1/profile/certifications  
POST   /api/v1/profile/certifications  
PUT    /api/v1/profile/certifications/{id}  
DELETE /api/v1/profile/certifications/{id}

Skills:

GET    /api/v1/profile/skills  
POST   /api/v1/profile/skills  
DELETE /api/v1/profile/skills/{id}

Evidence:

GET /api/v1/profile/claims/{id}/evidence  
---

# **17.24 Authorization**

Every one of these endpoints must enforce:

Authenticated User  
       ↓  
Resource ownership  
       ↓  
Allow / Deny

For example:

User A must never be able to:

GET /api/v1/profile/claims/{user-B-claim-id}

Even if they somehow know the UUID.

The service layer should verify ownership.

---

# **17.25 Validation rules**

We should implement deterministic validation.

### **Date validation**

start\_date \<= end\_date

unless:

is\_current \= true  
end\_date \= NULL

### **Claim validation**

Claim must belong to the candidate's Career Profile.

### **Relationship validation**

If:

claim.experience\_id \= X

then experience X must belong to the same Career Profile.

Same for projects and skills.

### **Evidence validation**

Evidence must belong to the same candidate.

### **Status validation**

An unsupported claim cannot suddenly become:

EVIDENCE\_BACKED

without evidence.

---

# **17.26 Claim state transition**

Let's formalize this.

                ┌──────────────────────┐  
                 │ AI extracted claim   │  
                 └──────────┬───────────┘  
                            ↓  
                   NEEDS\_CLARIFICATION  
                      /     |      \\  
                     /      |       \\  
                    ↓       ↓        ↓  
              Confirm     Edit     Reject  
                 │          │         │  
                 ↓          ↓         ↓  
      CANDIDATE\_CONFIRMED  ...     UNSUPPORTED

Evidence can independently influence:

SELF\_DECLARED  
     ↓  
Evidence added  
     ↓  
EVIDENCE\_BACKED

But candidate confirmation remains important.

---

# **17.27 Do we need versioning?**

Yes, but **not full versioning for every profile field in V1**.

We need audit history around:

* AI extraction  
* candidate approval  
* candidate edit  
* candidate rejection  
* claim changes  
* resume versions

We don't need a complicated event-sourcing architecture.

A simple audit mechanism is enough.

---

# **17.28 AI audit trail**

We already finalized `ai_operations`.

For resume extraction:

ai\_operations  
\-------------  
id  
user\_id  
operation\_type  
provider  
model  
prompt\_version  
input\_hash  
output\_json  
status  
error\_code  
created\_at

Example:

operation\_type:  
RESUME\_EXTRACTION

provider:  
gemini

model:  
\<model\>

prompt\_version:  
resume-extraction-v1

status:  
COMPLETED

This allows us to answer:

> “Why did the system extract Kubernetes?”

We can inspect:

Resume  
  ↓  
AI output  
  ↓  
Candidate action  
  ↓  
Final Career Claim

That's extremely valuable.

---

# **17.29 Career Knowledge Base**

After Step 17, this is what we should have:

              CAREER KNOWLEDGE BASE  
                       │  
        ┌──────────────┼───────────────┐  
        │              │               │  
     Profile       Experiences      Projects  
        │              │               │  
        ├──────────────┼───────────────┤  
        │                              │  
      Skills                         Claims  
                                       │  
                                       │  
                                   Evidence

Then Step 18 can consume this:

Career Knowledge Base  
          \+  
       Job Description  
          ↓  
     JD Analysis  
          ↓  
     Requirements  
          ↓  
       Matching  
          ↓  
      Gap Analysis  
---

# **17.30 Final Step 17 architecture**

React  
  │  
  ▼  
Profile / Claims API  
  │  
  ▼  
Career Profile Service  
  │  
  ├── Experience Service  
  ├── Project Service  
  ├── Skill Service  
  ├── Claim Service  
  └── Evidence Service  
          │  
          ▼  
      Validators  
          │  
          ▼  
    Repositories  
          │  
          ▼  
     PostgreSQL

AI extraction remains separate:

Resume Extraction  
       │  
       ▼  
Extraction Proposal  
       │  
       ▼  
Candidate Review  
       │  
       ▼  
Career Profile Service

This prevents AI from bypassing our business rules.

---

# **17.31 Final V1 decisions for Step 17**

| Decision | V1 |
| ----- | ----- |
| Career Profile | ✅ |
| Experiences | ✅ |
| Projects | ✅ |
| Education | ✅ |
| Certifications | ✅ |
| Skills | ✅ |
| Career Claims | ✅ |
| Evidence | ✅ |
| Claim ↔ Evidence | ✅ |
| Candidate confirmation | ✅ |
| Candidate editing | ✅ |
| Candidate rejection | ✅ |
| Experience type | ✅ |
| Claim status | ✅ |
| Independent verification | ❌ |
| Employer verification | ❌ |
| External verification integrations | ❌ |
| Full event sourcing | ❌ |
| Generic soft delete | ❌ |
| AI direct DB writes | ❌ |
| AI can invent claims | ❌ |
| Resume as evidence | ✅ |
| Resume as source of truth | ❌ |
| Career Profile as source of truth | **✅** |

### **The most important final principle**

> **The resume tells us what the candidate has written. The Career Profile tells us what the candidate has approved. Career Claims tell us what the system can safely reason about. Evidence tells us why a claim exists.**

That gives us the foundation we need for the next major component: **JD ingestion and Job Description analysis**.

Once Step 17 is finalized, the natural next step is **Step 18 — Job Description ingestion, requirement extraction, classification, normalization, and structured Job Requirement design.**

