# step 10

Absolutely. Let's move to **Step 10 — Complete System Workflow & API/Data Flow**.

This step will connect everything we've designed so far into one realistic end-to-end flow. I recommend we do this **before coding the database**, because it will reveal exactly which APIs, tables, background operations, and AI modules we actually need.

# **Step 10 — End-to-End System Workflow**

Our system should follow this overall lifecycle:

                   ┌───────────────────┐  
                    │      User         │  
                    └─────────┬─────────┘  
                              │  
                              ▼  
                    ┌───────────────────┐  
                    │   Create Account  │  
                    └─────────┬─────────┘  
                              │  
                              ▼  
                    ┌───────────────────┐  
                    │ Career Profile    │  
                    │                   │  
                    │ Experience        │  
                    │ Skills            │  
                    │ Projects          │  
                    │ Education         │  
                    │ Certifications    │  
                    │ Claims \+ Evidence │  
                    └─────────┬─────────┘  
                              │  
                              ▼  
                    ┌───────────────────┐  
                    │ Add Job           │  
                    │ Description       │  
                    └─────────┬─────────┘  
                              │  
                              ▼  
                    ┌───────────────────┐  
                    │ JD Analysis        │  
                    └─────────┬─────────┘  
                              │  
                              ▼  
                    ┌───────────────────┐  
                    │ Candidate ↔ Job   │  
                    │ Matching          │  
                    └─────────┬─────────┘  
                              │  
                              ▼  
                    ┌───────────────────┐  
                    │ Gap Analysis      │  
                    └─────────┬─────────┘  
                              │  
                              ▼  
                    ┌───────────────────┐  
                    │ Resume            │  
                    │ Optimization      │  
                    └─────────┬─────────┘  
                              │  
                              ▼  
                    ┌───────────────────┐  
                    │ Truth Validation  │  
                    └─────────┬─────────┘  
                              │  
                              ▼  
                    ┌───────────────────┐  
                    │ Candidate Review  │  
                    │ & Approval        │  
                    └─────────┬─────────┘  
                              │  
                              ▼  
                    ┌───────────────────┐  
                    │ Final Resume      │  
                    │ PDF / DOCX        │  
                    └───────────────────┘

Now let's break this down.

---

# **10.1 Stage 1 — Account Creation**

The user creates an account.

### **Frontend**

POST /api/v1/auth/register

Request:

{  
  "email": "candidate@example.com",  
  "password": "\*\*\*\*\*\*\*\*"  
}

Backend:

FastAPI  
   ↓  
Validate  
   ↓  
Hash password  
   ↓  
Create User  
   ↓  
Create CareerProfile

We should not store plaintext passwords.

---

# **10.2 Stage 2 — Career Profile Setup**

The candidate sees:

┌─────────────────────────────────────┐  
│       Build Your Career Profile     │  
├─────────────────────────────────────┤  
│                                     │  
│ Full Name                           │  
│ \[\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\]      │  
│                                     │  
│ Professional Headline               │  
│ \[\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\]      │  
│                                     │  
│ Experience                           │  
│ \[+ Add Experience\]                  │  
│                                     │  
│ Skills                              │  
│ \[+ Add Skills\]                      │  
│                                     │  
│ Projects                            │  
│ \[+ Add Project\]                     │  
│                                     │  
│ Education                           │  
│ \[+ Add Education\]                   │  
│                                     │  
│             \[Save Profile\]          │  
└─────────────────────────────────────┘

But manually entering everything is annoying.

So we support:

> **Import Existing Resume**

---

# **10.3 Stage 3 — Resume Upload**

User uploads:

resume.pdf

Frontend:

POST /api/v1/resumes/upload

Backend:

FastAPI  
   │  
   ├── Validate file  
   ├── Check size/type  
   └── Save file

For our current MVP:

StorageProvider  
       ↓  
Local Storage

Later:

StorageProvider  
       ↓  
Cloudflare R2

The database stores metadata, not the entire file.

For example:

ResumeFile  
\----------  
id  
user\_id  
filename  
storage\_key  
mime\_type  
size  
created\_at  
---

# **10.4 Stage 4 — Resume Parsing**

Now we need to understand the uploaded resume.

Pipeline:

resume.pdf  
    ↓  
PDF Parser  
    ↓  
Extracted Text  
    ↓  
LLM  
    ↓  
Structured Profile Proposal

The LLM might return:

{  
  "name": "Riya Jogi",  
  "skills": \[  
    "Python",  
    "FastAPI",  
    "PostgreSQL"  
  \],  
  "experiences": \[\],  
  "projects": \[\],  
  "education": \[\]  
}

But remember:

### **This is NOT yet trusted data.**

It's an AI proposal.

---

# **10.5 Stage 5 — Candidate Review**

This is one of the most important screens.

The UI should show:

┌──────────────────────────────────────┐  
│ Review Imported Information          │  
├──────────────────────────────────────┤  
│                                      │  
│ ✓ Python                             │  
│   Source: Resume                     │  
│                                      │  
│ ✓ FastAPI                            │  
│   Source: Resume                     │  
│                                      │  
│ ? Kubernetes                         │  
│   Source: Resume                     │  
│   \[Confirm\] \[Edit\] \[Reject\]          │  
│                                      │  
│ Experience                           │  
│                                      │  
│ ABC Technologies                    │  
│ Python Backend Developer             │  
│ Jan 2024 \- Present                   │  
│                                      │  
│ \[Edit\] \[Confirm\]                     │  
│                                      │  
│         \[Save Career Profile\]        │  
└──────────────────────────────────────┘

Candidate can:

Confirm  
Edit  
Reject  
Add

Only after this do we establish trusted profile information.

---

# **10.6 Stage 6 — Build Career Knowledge Base**

Once confirmed:

Candidate  
    ↓  
Career Profile  
    ↓  
Claims  
    ↓  
Evidence  
    ↓  
Skills  
    ↓  
Projects  
    ↓  
Experience

At this point the system has its:

> **Single Source of Truth**

This is the foundation for everything that follows.

---

# **10.7 Stage 7 — Add a Job**

For MVP, keep this extremely simple.

User sees:

┌─────────────────────────────────────┐  
│ Add a Job                           │  
├─────────────────────────────────────┤  
│ Job Title                           │  
│ \[Python Backend Developer\_\_\_\_\_\_\_\]   │  
│                                     │  
│ Company                             │  
│ \[ABC Technologies\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\]   │  
│                                     │  
│ Job Description                     │  
│ ┌─────────────────────────────────┐ │  
│ │ Paste job description here...   │ │  
│ │                                 │ │  
│ └─────────────────────────────────┘ │  
│                                     │  
│          \[Analyze Job\]              │  
└─────────────────────────────────────┘

API:

POST /api/v1/jobs

Initially, **paste JD** is enough.

Don't build scraping/LinkedIn/Indeed integrations yet.

---

# **10.8 Stage 8 — JD Analysis**

Now the AI gets the JD.

Job Description  
       ↓  
JD Analyzer  
       ↓  
Structured Job Profile

Example output:

{  
  "title": "Python Backend Developer",  
  "requirements": \[  
    {  
      "skill": "Python",  
      "importance": "required",  
      "minimum\_years": 3  
    },  
    {  
      "skill": "FastAPI",  
      "importance": "required"  
    },  
    {  
      "skill": "Docker",  
      "importance": "preferred"  
    }  
  \]  
}

The LLM is useful here because JD language is messy.

For example:

"Experience developing RESTful APIs with Python"

should be understood as related to:

Python  
REST APIs  
Backend Development  
---

# **10.9 Stage 9 — Normalize Requirements**

Before matching, we normalize.

For example:

Postgres  
PostgreSQL  
PostgreSQL DB

→

PostgreSQL

Similarly:

REST API  
RESTful API  
REST APIs

→

REST API

This can be done using a combination of:

* skill dictionary  
* aliases  
* deterministic normalization  
* embeddings  
* LLM interpretation where needed

We shouldn't ask the LLM to decide everything.

---

# **10.10 Stage 10 — Candidate ↔ Job Matching**

Now:

Career Profile  
      \+  
Job Requirements  
      ↓  
Matching Engine

The matcher evaluates:

Exact match  
Normalized match  
Semantic match  
Experience  
Experience type  
Evidence  
Requirement importance

Example:

Python  
────────────────  
Required: 3+ years  
Candidate: 2.5 years professional

→ Partial Match

FastAPI:

Required  
Candidate: 2 years professional

→ Strong Match

Kubernetes:

Preferred  
Candidate: personal project

→ Partial Match  
---

# **10.11 Stage 11 — Match Score**

We can produce an overall score.

For example:

┌─────────────────────────────┐  
│ Job Alignment               │  
│                             │  
│          82%                │  
│                             │  
│ Skills          88%         │  
│ Experience      76%         │  
│ Education       100%        │  
│ Keywords        84%         │  
│                             │  
└─────────────────────────────┘

But remember:

> This is **our alignment score**, not a guaranteed ATS score.

We should explain how the score was calculated.

---

# **10.12 Stage 12 — Gap Analysis**

This should be a major user-facing feature.

Example:

Your Match

🟢 Strong Matches  
   Python  
   FastAPI  
   PostgreSQL

🟡 Partial Matches  
   Docker  
   AWS

🔴 Gaps  
   Kubernetes

⚪ Needs Clarification  
   CI/CD

And the system explains why.

For example:

> **Kubernetes — Gap**  
> Your profile contains a personal learning project involving Kubernetes, but no evidence of professional Kubernetes experience was found.

That's much more useful than simply saying:

> Kubernetes ❌

---

# **10.13 Stage 13 — Resume Optimization**

Now the user clicks:

\[Optimize Resume\]

The optimizer receives:

Career Profile  
\+  
Relevant Career Claims  
\+  
Job Requirements  
\+  
Gap Analysis  
\+  
Existing Resume

Then:

Optimizer  
   ↓  
Proposed Resume Changes

For example:

### **Original**

> Developed backend applications.

### **Proposed**

> Developed Python-based REST APIs using FastAPI for backend applications.

And the system records:

Why:  
The job emphasizes Python, REST APIs and FastAPI.

Evidence:  
Career Claim \#123

Risk:  
Low

Candidate decision:  
Pending  
---

# **10.14 Stage 14 — Truth Validation**

This happens **before the candidate receives the final resume**.

Generated resume:

"Designed and deployed scalable Kubernetes  
microservices on AWS."

Validator checks:

Kubernetes?  
→ Personal project only

AWS?  
→ Learning only

Designed?  
→ No supporting claim

Deployed?  
→ No supporting claim

Scalable?  
→ No supporting evidence

Result:

❌ BLOCKED

The system tells the optimizer:

> This statement contains unsupported claims.

It must be revised.

---

# **10.15 Stage 15 — Change Review**

After validation, candidate sees:

┌─────────────────────────────────────────────┐  
│ Review Changes                              │  
├─────────────────────────────────────────────┤  
│                                             │  
│ ORIGINAL                                    │  
│ Developed backend applications.              │  
│                                             │  
│              ↓                              │  
│                                             │  
│ PROPOSED                                    │  
│ Developed Python REST APIs using FastAPI.   │  
│                                             │  
│ WHY                                         │  
│ Better alignment with the JD.               │  
│                                             │  
│ EVIDENCE                                    │  
│ Career Claim \#123                            │  
│                                             │  
│ \[Reject\]             \[Approve\]              │  
└─────────────────────────────────────────────┘

This is where your product's **candidate control** becomes visible.

---

# **10.16 Stage 16 — Candidate Approval**

Candidate approves.

Database records:

ResumeChange  
    ↓  
Approved

If candidate rejects:

ResumeChange  
    ↓  
Rejected

If candidate edits:

ResumeChange  
    ↓  
Edited

We retain this history.

---

# **10.17 Stage 17 — Final Resume Generation**

Only after approval:

Approved structured content  
          ↓  
Resume Renderer  
          ↓  
PDF / DOCX

Important:

### **LLM should not be responsible for final document formatting.**

Instead:

Structured Resume Data  
        ↓  
Deterministic Template  
        ↓  
PDF/DOCX

This gives us consistent formatting.

---

# **10.18 Stage 18 — Final Job Alignment Analysis**

Before download:

Final Resume  
      \+  
Job Description  
      ↓  
Final Analysis

Example:

Job Alignment: 91%

Required Skills:     95%  
Preferred Skills:    82%  
Experience:          88%  
Keyword Coverage:    93%  
Education:          100%

Potential Issues:  
• Python experience requirement is 3+ years;  
  profile supports approximately 2.5 years.

This is much more honest than:

> "ATS Score: 91 — You'll pass ATS."

---

# **10.19 Complete API flow**

Now let's translate everything into APIs.

### **Authentication**

POST   /api/v1/auth/register  
POST   /api/v1/auth/login  
GET    /api/v1/auth/me

### **Career Profile**

GET    /api/v1/profile  
PUT    /api/v1/profile

GET    /api/v1/profile/claims  
POST   /api/v1/profile/claims  
PUT    /api/v1/profile/claims/{id}  
DELETE /api/v1/profile/claims/{id}

### **Resume**

POST   /api/v1/resumes/upload  
GET    /api/v1/resumes  
GET    /api/v1/resumes/{id}

### **Resume extraction**

POST /api/v1/resumes/{id}/extract  
GET  /api/v1/resumes/{id}/extraction

### **Jobs**

POST /api/v1/jobs  
GET  /api/v1/jobs  
GET  /api/v1/jobs/{id}

### **JD Analysis**

POST /api/v1/jobs/{id}/analyze  
GET  /api/v1/jobs/{id}/requirements

### **Matching**

POST /api/v1/jobs/{id}/match  
GET  /api/v1/jobs/{id}/match

### **Optimization**

POST /api/v1/jobs/{id}/optimize  
GET  /api/v1/jobs/{id}/optimization

### **Changes**

GET  /api/v1/optimizations/{id}/changes

POST /api/v1/changes/{id}/approve  
POST /api/v1/changes/{id}/reject  
POST /api/v1/changes/{id}/edit

### **Final resume**

POST /api/v1/jobs/{id}/resume/generate  
GET  /api/v1/jobs/{id}/resume  
---

# **10.20 One important improvement**

I would **not** make every AI operation a separate public endpoint forever.

For example:

/analyze  
/match  
/optimize  
/validate  
/generate

are useful conceptually, but internally we should have an orchestration layer.

Something like:

Application Service  
       │  
       ├── JDAnalyzer  
       ├── Matcher  
       ├── GapAnalyzer  
       ├── Optimizer  
       ├── ClaimValidator  
       └── ResumeGenerator

This gives us a clean separation between:

API Layer  
    ↓  
Application/Business Layer  
    ↓  
AI/Infrastructure Layer  
---

# **10.21 Current MVP execution model**

Since we removed Redis for now, the workflow can be synchronous where practical:

POST /jobs/{id}/analyze  
        ↓  
FastAPI  
        ↓  
JD Analyzer  
        ↓  
Ollama  
        ↓  
Validation  
        ↓  
Database  
        ↓  
Response

If later this becomes too slow:

POST /jobs/{id}/analyze  
        ↓  
Create processing job  
        ↓  
Queue  
        ↓  
Worker  
        ↓  
JD Analyzer  
        ↓  
Ollama/Cloud LLM

Our business logic doesn't need to change.

---

# **10.22 Error handling**

This needs to be designed now.

Imagine Ollama isn't running.

We shouldn't return:

500 Internal Server Error

with no useful explanation.

Instead:

{  
  "error": {  
    "code": "LLM\_UNAVAILABLE",  
    "message": "The configured AI provider is currently unavailable."  
  }  
}

The frontend can then show:

⚠ AI service unavailable

Ollama is not running.

Please start Ollama and try again.

Similarly:

FILE\_UNSUPPORTED  
JD\_EMPTY  
CLAIM\_UNSUPPORTED  
VALIDATION\_FAILED  
RESUME\_GENERATION\_FAILED

should have meaningful error codes.

---

# **10.23 One more important concept — Processing Status**

Even without Redis, we should have a status field for long-running operations.

For example:

ProcessingStatus  
\----------------  
PENDING  
PROCESSING  
COMPLETED  
FAILED

So:

Job Analysis  
     │  
     ├── PENDING  
     ├── PROCESSING  
     ├── COMPLETED  
     └── FAILED

Why?

Because when we introduce a queue later, these same states become useful.

We won't need to redesign the data model.

---

# **10.24 Complete real-world example**

Let's put everything together.

Candidate uploads:

Resume.pdf

System extracts:

Python  
FastAPI  
PostgreSQL  
Docker  
AI Project

Candidate confirms:

Python → Professional  
FastAPI → Professional  
PostgreSQL → Professional  
Docker → Professional  
AI Project → Personal

Candidate adds JD:

Python Backend Engineer

3+ years Python  
FastAPI  
PostgreSQL  
Docker  
AWS  
Kubernetes

System analyzes:

Required:  
Python  
FastAPI  
PostgreSQL

Preferred:  
Docker  
AWS  
Kubernetes

Matching:

Python       🟡 2.5 vs 3+ years  
FastAPI      🟢 Strong  
PostgreSQL   🟢 Strong  
Docker       🟢 Strong  
AWS          🔴/🟡 depends on evidence  
Kubernetes   🟡 Personal

Optimizer proposes:

Original:  
Worked on backend applications.

New:  
Developed Python-based REST APIs using FastAPI  
and PostgreSQL.

Evidence:

Python claim  
FastAPI claim  
PostgreSQL claim

Validator:

✅ All claims supported

Candidate:

Approve

Final generator:

Resume\_Version\_3.pdf

Final analysis:

Job Alignment: 87%

And the system tells the candidate:

> "Your profile aligns strongly with the core backend requirements. The main gap is the requested 3+ years of Python experience; your available evidence supports approximately 2.5 years."

**That is the product.**

---

# **10.25 Our architecture is now coming together**

We now have:

            ┌─────────────────────┐  
             │       React         │  
             └──────────┬──────────┘  
                        │  
                        ▼  
             ┌─────────────────────┐  
             │      FastAPI        │  
             └──────────┬──────────┘  
                        │  
                        ▼  
             ┌─────────────────────┐  
             │ Application Services│  
             └──────────┬──────────┘  
                        │  
       ┌────────────────┼────────────────┐  
       ▼                ▼                ▼  
 Career Services   Job Services    Resume Services  
       │                │                │  
       └────────────────┼────────────────┘  
                        ▼  
                 AI Orchestrator  
                        │  
          ┌─────────────┼─────────────┐  
          ▼             ▼             ▼  
        LLM         Embeddings     Validators  
          │  
     ┌────┴────┐  
     ▼         ▼  
  Ollama    Cloud LLM

And infrastructure:

                ┌─────────────┐  
                 │ PostgreSQL  │  
                 │ \+ pgvector  │  
                 └─────────────┘

                 ┌─────────────┐  
                 │    Local    │  
                 │   Storage   │  
                 └─────────────┘

                 ┌─────────────┐  
                 │   Ollama    │  
                 └─────────────┘

No Redis currently.

---

# **Step 10 conclusion**

At this point, we have answered:

* **What happens when a user enters the system?**  
* **How does a resume become structured data?**  
* **How does AI extraction become trusted information?**  
* **How is a JD analyzed?**  
* **How are candidate and job requirements matched?**  
* **How are gaps identified?**  
* **How does AI optimize the resume?**  
* **How do we prevent hallucinated claims?**  
* **How does candidate approval work?**  
* **How is the final resume generated?**  
* **How can we later introduce a queue without redesigning everything?**

The next step should be **Step 11 — Detailed Database Schema / ER Diagram**, where we turn the conceptual entities from Step 9 into actual PostgreSQL tables, relationships, primary keys, foreign keys, indexes, constraints, and the pgvector design.

That is where we'll decide things like:

users  
career\_profiles  
career\_claims  
evidence  
skills  
candidate\_skills  
experiences  
projects  
jobs  
job\_requirements  
match\_details  
resume\_versions  
resume\_changes  
approvals

and determine **exactly which fields each table should contain and why**.

# step 11

Great. Let's move to **Step 11 — Detailed Database Schema & ER Design**.

This is where we convert the conceptual model from Step 9 into an actual PostgreSQL design.

The goal is **not** to create as many tables as possible. The goal is to create a schema that is:

* normalized enough to avoid duplicated/conflicting data,  
* simple enough for your MVP,  
* safe for AI-generated content,  
* traceable back to evidence,  
* compatible with `pgvector`,  
* and easy to extend later.

---

# **Step 11 — Database Schema & ER Design**

## **11.1 First: the complete relationship**

The high-level ER structure should look like this:

┌─────────────┐  
│    users    │  
└──────┬──────┘  
       │ 1:1  
       ▼  
┌──────────────────┐  
│ career\_profiles  │  
└──────┬───────────┘  
       │  
       ├──────────────┬───────────────┬──────────────┐  
       │              │               │              │  
       ▼              ▼               ▼              ▼  
 experiences       projects        education      certifications  
       │              │  
       └──────┬───────┘  
              ▼  
       ┌──────────────┐  
       │career\_claims │◄──────────────┐  
       └──────┬───────┘               │  
              │                       │  
              ▼                       │  
         ┌──────────┐                 │  
         │ evidence │─────────────────┘  
         └──────────┘

career\_profiles  
       │  
       ▼  
candidate\_skills  
       │  
       ▼  
     skills

users  
  │  
  ▼  
 jobs  
  │  
  ▼  
job\_requirements  
  │  
  ▼  
candidate\_job\_matches  
  │  
  ▼  
match\_details  
  │  
  ├──────────────► career\_claims  
  │  
  └──────────────► job\_requirements

career\_profiles  
       │  
       ▼  
    resumes  
       │  
       ▼  
 resume\_versions  
       │  
       ▼  
 resume\_changes  
       │  
       ▼  
   approvals

Now let's define the tables.

---

# **11.2 `users`**

This is the authentication/account table.

users  
────────────────────────────  
id                  PK  
email               UNIQUE  
password\_hash  
is\_active  
created\_at  
updated\_at

Example:

id: 1  
email: riya@example.com  
password\_hash: $argon2...  
is\_active: true

### **Important**

Don't store:

password

Store only a secure password hash.

For FastAPI/Python, we'll later use a proper password hashing library such as Argon2/bcrypt rather than implementing hashing ourselves.

---

# **11.3 `career_profiles`**

One user has one primary career profile for the MVP.

career\_profiles  
────────────────────────────  
id                  PK  
user\_id             FK → users.id UNIQUE

full\_name  
headline  
summary

phone  
email

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

Why separate this from `users`?

Because authentication information and professional information are different concerns.

---

# **11.4 `experiences`**

experiences  
────────────────────────────  
id                  PK  
career\_profile\_id   FK

company\_name  
job\_title

employment\_type

start\_date  
end\_date  
is\_current

description

created\_at  
updated\_at

Example:

ABC Technologies  
Python Backend Developer

2024-01-01  
2026-06-30

Professional

### **Important date rule**

Don't store experience duration as:

2.5 years

Store dates.

Then calculate duration when required.

Why?

Because:

start\_date \= 2024-01  
end\_date \= 2026-06

can produce different calculations depending on the current date and context.

---

# **11.5 `projects`**

projects  
────────────────────────────  
id                  PK  
career\_profile\_id   FK

name  
description

project\_type

start\_date  
end\_date

repository\_url  
project\_url

created\_at  
updated\_at

`project_type`:

professional  
personal  
academic  
learning

This is important because:

> A personal project demonstrating Kubernetes is not the same as two years of professional Kubernetes experience.

---

# **11.6 `education`**

education  
────────────────────────────  
id                  PK  
career\_profile\_id   FK

institution  
degree  
field\_of\_study

start\_date  
end\_date

grade

created\_at  
updated\_at  
---

# **11.7 `certifications`**

certifications  
────────────────────────────  
id                  PK  
career\_profile\_id   FK

name  
issuer

issue\_date  
expiry\_date

credential\_id  
credential\_url

created\_at  
updated\_at  
---

# **11.8 `skills`**

This is our canonical skill dictionary.

skills  
────────────────────────────  
id                  PK

name  
canonical\_name  
category

created\_at

Example:

id | name       | canonical\_name  
\--------------------------------  
1  | Python     | Python  
2  | Postgres   | PostgreSQL  
3  | PostgreSQL | PostgreSQL  
4  | FastAPI    | FastAPI

However, I'd make one refinement.

We probably don't need multiple rows for aliases initially.

Instead, later we can introduce:

skill\_aliases

For MVP, a simpler approach can be:

skills  
\----------------  
id  
canonical\_name  
category

and maintain aliases in application configuration or a separate table once the vocabulary grows.

---

# **11.9 `candidate_skills`**

This represents the candidate's relationship with a skill.

candidate\_skills  
────────────────────────────  
id                  PK

career\_profile\_id   FK  
skill\_id            FK

experience\_type

proficiency

years\_used

first\_used  
last\_used

status

created\_at  
updated\_at

Example:

Candidate: 1  
Skill: Python

Experience type:  
Professional

Years used:  
2.5

Status:  
candidate\_confirmed

Another:

Skill:  
Kubernetes

Experience type:  
Personal

Years:  
0.5

Status:  
evidence\_backed  
---

# **11.10 `career_claims` ⭐**

This is the most important table.

I'd structure it approximately as:

career\_claims  
────────────────────────────────  
id                      PK

career\_profile\_id       FK

claim\_type

claim\_text

experience\_type

status  
confidence

start\_date  
end\_date

experience\_id           FK nullable  
project\_id              FK nullable  
skill\_id                FK nullable

created\_at  
updated\_at

Potential `claim_type`:

skill  
responsibility  
achievement  
experience  
project  
education  
certification

Example:

claim\_text:  
"Developed REST APIs using FastAPI."

experience\_type:  
professional

status:  
candidate\_confirmed

experience\_id:  
15

skill\_id:  
8  
---

# **11.11 Why do we link claims to Experience/Project?**

Because we want to answer:

> **Where did this claim happen?**

For example:

Career Claim  
     │  
     ▼  
"Developed FastAPI APIs"  
     │  
     ▼  
Experience \#15  
     │  
     ▼  
ABC Technologies

Or:

Career Claim  
     │  
     ▼  
"Built document Q\&A system"  
     │  
     ▼  
Project \#7  
     │  
     ▼  
Personal AI Project

This gives the system context.

---

# **11.12 One potential problem with nullable foreign keys**

You might notice:

experience\_id nullable  
project\_id nullable

That's intentional for the MVP.

A claim could be:

"Completed M.Sc. in Information Technology."

which may not belong to an experience or project.

Later, if we want a more sophisticated polymorphic evidence model, we can improve this.

Don't over-engineer it now.

---

# **11.13 `evidence`**

Now the evidence table.

evidence  
────────────────────────────  
id                  PK

career\_profile\_id   FK

evidence\_type

title  
description

file\_id  
external\_url

source\_text

created\_at  
updated\_at

Possible types:

resume  
project\_document  
github  
portfolio  
certificate  
work\_sample  
candidate\_confirmation  
other  
---

# **11.14 Connecting Claims and Evidence**

Here's an important improvement.

Don't make:

career\_claims.evidence\_id

because a claim can have **multiple evidence sources**.

Instead use a junction table:

claim\_evidence  
────────────────────────────  
claim\_id            FK  
evidence\_id         FK

relationship\_type

created\_at

PRIMARY KEY (claim\_id, evidence\_id)

Example:

Claim:  
"Built FastAPI backend"

Evidence:  
Resume.pdf  
GitHub repository  
Project documentation  
Candidate confirmation

So:

                ┌─────────────┐  
                 │ CareerClaim │  
                 └──────┬──────┘  
                        │  
                        │ M:N  
                        │  
                 ┌──────▼──────┐  
                 │ClaimEvidence│  
                 └──────┬──────┘  
                        │  
                        ▼  
                 ┌─────────────┐  
                 │   Evidence  │  
                 └─────────────┘

This is much more flexible.

---

# **11.15 Resume files**

We should separate the physical file from resume metadata.

Conceptually:

resume\_files  
────────────────────────────  
id  
career\_profile\_id

filename  
storage\_key  
mime\_type  
file\_size

source\_type

created\_at

`source_type` might be:

uploaded\_original  
generated

The actual PDF/DOCX lives in:

Local Storage

today and:

R2

later.

The database only stores the reference.

---

# **11.16 `resumes`**

This represents a resume entity.

resumes  
────────────────────────────  
id  
career\_profile\_id  
original\_file\_id

name

created\_at  
updated\_at

For example:

Master Resume

The original uploaded file remains unchanged.

---

# **11.17 `resume_versions`**

Every generated version gets its own record.

resume\_versions  
────────────────────────────  
id

resume\_id  
job\_id nullable

version\_number

status

file\_id nullable

content\_snapshot

created\_at

Possible status:

draft  
pending\_review  
approved  
final  
rejected

Example:

Resume  
   │  
   ├── Version 1 → Python Backend Job  
   ├── Version 2 → AI Engineer Job  
   └── Version 3 → FastAPI Developer Job  
---

# **11.18 Why `content_snapshot`?**

This is important.

Suppose the candidate's Career Profile changes later.

We don't want old resumes to magically change.

Therefore:

Resume Version 1  
      ↓  
Snapshot of approved content at that time

The version becomes immutable after finalization.

The Career Profile can continue evolving independently.

---

# **11.19 `jobs`**

jobs  
────────────────────────────  
id  
user\_id

title  
company\_name

description

location  
employment\_type

source  
source\_url

created\_at  
updated\_at

For MVP:

source \= manual  
source\_url \= NULL

Later:

source \= linkedin  
source \= company\_site  
source \= indeed

But don't implement those integrations yet.

---

# **11.20 `job_requirements`**

The JD analyzer converts raw JD text into these records.

job\_requirements  
────────────────────────────  
id

job\_id

requirement\_text

requirement\_type  
importance

skill\_id nullable

minimum\_years nullable

experience\_type nullable

created\_at  
updated\_at

Example:

Requirement:  
3+ years Python development

Type:  
skill

Importance:  
required

Skill:  
Python

Minimum years:  
3  
---

# **11.21 Store the LLM's raw response?**

Yes — but carefully.

For AI operations, I recommend storing the **structured result** and optionally the raw response for debugging/audit.

For example:

ai\_operations  
────────────────────────────  
id

user\_id  
job\_id nullable  
resume\_id nullable

operation\_type

provider  
model

input\_hash

output\_json

status

error\_code

created\_at

Examples:

jd\_analysis  
resume\_extraction  
matching  
optimization  
claim\_validation

Why?

Because while developing, you'll constantly ask:

> "Why did the AI produce this result?"

Having the operation metadata is extremely useful.

But we should **not blindly store sensitive prompts/responses forever** in production. We'll define retention/privacy rules later.

---

# **11.22 `candidate_job_matches`**

candidate\_job\_matches  
────────────────────────────  
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

Example:

overall \= 86  
skills \= 91  
experience \= 78  
education \= 100  
keywords \= 88  
semantic \= 84  
---

# **11.23 `match_details`**

This provides explainability.

match\_details  
────────────────────────────  
id

match\_id

job\_requirement\_id  
career\_claim\_id nullable

match\_type

score

explanation

created\_at

`match_type`:

strong  
partial  
gap  
unknown

Example:

Requirement:  
Python 3+ years

Claim:  
Python professional 2.5 years

Result:  
partial

Score:  
0.75  
---

# **11.24 `resume_changes`**

This is our audit trail.

resume\_changes  
────────────────────────────  
id

resume\_version\_id

change\_type

original\_text  
proposed\_text

reason

career\_claim\_id nullable

validation\_status

created\_at  
updated\_at

Example:

Original:  
Worked on backend applications.

Proposed:  
Developed Python REST APIs using FastAPI.

Reason:  
Improves alignment with required Python/FastAPI  
experience in the job description.

Career Claim:  
123

Validation:  
passed  
---

# **11.25 `approvals`**

approvals  
────────────────────────────  
id

resume\_change\_id

decision

edited\_text nullable

decided\_at

Decision:

approved  
rejected  
edited

This creates a clean audit trail.

---

# **11.26 Where does pgvector fit?**

Now the interesting part.

We don't need embeddings for everything.

We should use them where semantic search actually helps.

Potential vector-bearing entities:

career\_claims  
job\_requirements  
projects  
experiences

For MVP, I'd start with:

career\_claims.embedding  
job\_requirements.embedding

For example:

career\_claims  
────────────────────────────  
id  
claim\_text  
embedding vector(...)

and:

job\_requirements  
────────────────────────────  
id  
requirement\_text  
embedding vector(...)

Then:

JD Requirement  
     ↓  
Embedding  
     ↓  
Vector similarity  
     ↓  
Candidate Claims  
---

# **11.27 But don't let embeddings determine truth**

This is extremely important.

Suppose:

Job:  
"Experience architecting distributed systems."

Candidate:  
"Built a small REST API project."

Semantic similarity might be reasonably high.

That does **not** mean:

Architected distributed systems \= TRUE

Embeddings tell us:

> "These pieces of text are semantically related."

They do not tell us:

> "The candidate satisfies this qualification."

Therefore:

Embedding  
     ↓  
Candidate retrieval  
     ↓  
Deterministic/business rules  
     ↓  
Evidence/context  
     ↓  
Match decision

Not:

Embedding similarity \> 0.7  
       ↓  
Qualified  
---

# **11.28 Vector metadata**

Because we discussed provider switching earlier, we should store:

embedding\_model  
embedding\_dimension

For example:

career\_claim\_embeddings  
\-----------------------  
claim\_id  
embedding  
model\_name  
dimension  
created\_at

We could also put these directly on the claim table for MVP.

I prefer keeping embedding information separate if we anticipate multiple embedding versions.

---

# **11.29 Final MVP schema**

Putting everything together:

AUTH  
────────────────  
users

CAREER  
────────────────  
career\_profiles  
experiences  
projects  
education  
certifications  
skills  
candidate\_skills  
career\_claims  
evidence  
claim\_evidence

JOBS  
────────────────  
jobs  
job\_requirements

MATCHING  
────────────────  
candidate\_job\_matches  
match\_details

RESUMES  
────────────────  
resume\_files  
resumes  
resume\_versions  
resume\_changes  
approvals

AI / AUDIT  
────────────────  
ai\_operations

VECTOR  
────────────────  
career\_claim\_embeddings  
job\_requirement\_embeddings

That's a solid starting architecture.

---

# **11.30 But I want to avoid one mistake**

It might be tempting to immediately create all these tables.

**Don't.**

For our implementation, we'll build incrementally.

### **Phase A**

users  
career\_profiles  
experiences  
projects  
education  
certifications  
skills  
candidate\_skills  
career\_claims  
evidence  
claim\_evidence

### **Phase B**

jobs  
job\_requirements

### **Phase C**

candidate\_job\_matches  
match\_details

### **Phase D**

resumes  
resume\_versions  
resume\_changes  
approvals

### **Phase E**

embeddings  
ai\_operations

This lets us test each part before adding the next.

---

# **11.31 Important database constraints**

We should enforce some rules at the database/application level.

For example:

### **One profile per user**

career\_profiles.user\_id UNIQUE

### **Candidate skill shouldn't duplicate**

UNIQUE(career\_profile\_id, skill\_id)

### **Claim/evidence relationship shouldn't duplicate**

PRIMARY KEY(claim\_id, evidence\_id)

### **Dates**

We should ensure:

end\_date \>= start\_date

where applicable.

### **Experience**

If:

is\_current \= true

then:

end\_date \= NULL

These rules prevent bad data before AI even gets involved.

---

# **11.32 Indexes**

We don't need hundreds of indexes.

Start with indexes around common lookups:

users.email

career\_profiles.user\_id

career\_claims.career\_profile\_id

candidate\_skills.career\_profile\_id

experiences.career\_profile\_id

projects.career\_profile\_id

jobs.user\_id

job\_requirements.job\_id

candidate\_job\_matches.job\_id

resume\_versions.resume\_id

For vector search, we'll add an appropriate pgvector index once we know the embedding model/dimension.

---

# **11.33 One architectural improvement I'd make**

There's an important distinction between:

Career Claim

and:

Candidate Skill

They shouldn't be treated as the same thing.

For example:

CandidateSkill:  
Python

is a **normalized capability**.

But:

CareerClaim:  
"Developed Python REST APIs for payment processing."

is a **specific factual statement**.

So:

Candidate Skill  
       │  
       ▼  
Python  
       │  
       ├── Claim: developed REST APIs  
       ├── Claim: wrote background jobs  
       └── Claim: implemented authentication

This gives us both broad matching and precise evidence.

---

# **11.34 The resulting data flow**

Now the database supports our complete product:

                    USER  
                      │  
                      ▼  
               CAREER PROFILE  
                      │  
          ┌───────────┼───────────┐  
          ▼           ▼           ▼  
       Skills      Experience   Projects  
          │           │           │  
          └───────────┼───────────┘  
                      ▼  
                CAREER CLAIMS  
                      │  
                      ▼  
                   EVIDENCE  
                      │  
                      │  
                      ▼  
                    JOB  
                      │  
                      ▼  
              JOB REQUIREMENTS  
                      │  
                      ▼  
              MATCHING ENGINE  
                      │  
                      ▼  
               GAP ANALYSIS  
                      │  
                      ▼  
             RESUME OPTIMIZER  
                      │  
                      ▼  
               RESUME CHANGES  
                      │  
                      ▼  
               TRUTH VALIDATOR  
                      │  
                      ▼  
               CANDIDATE APPROVAL  
                      │  
                      ▼  
              RESUME VERSION  
                      │  
                      ▼  
                  PDF/DOCX

This is the database architecture I would recommend for the project at this stage.

---

## **One decision I would not make yet**

We should **not lock the exact embedding model and vector dimension yet**.

That belongs in the next AI/ML design step because we need to decide:

* which embedding model we'll use locally,  
* whether Ollama can handle it,  
* whether we'll use a separate local embedding model,  
* what vector dimension it produces,  
* how semantic similarity will be calculated,  
* when to use exact matching vs embeddings,  
* and how the final match score will be calculated.

# step 12

Great. Let's continue with **Step 12 — AI/ML Pipeline & Matching Engine Design**.

This is the point where we define **how the intelligence of the product actually works**.

The most important architectural decision here is:

> **We will not build an "LLM does everything" system.**

> We will build a **hybrid AI system** where the LLM understands language, embeddings find semantic relationships, and deterministic Python/business rules make the final decisions.

---

# **Step 12 — AI/ML Pipeline & Matching Engine**

## **12.1 The AI architecture**

Our overall intelligence pipeline will be:

                ┌─────────────────┐  
                 │ Candidate Data  │  
                 └────────┬────────┘  
                          │  
                          ▼  
                 ┌─────────────────┐  
                 │ Career Claims   │  
                 │ \+ Evidence      │  
                 └────────┬────────┘  
                          │  
                          │  
                          │  
                 ┌────────▼────────┐  
                 │ Job Description  │  
                 └────────┬────────┘  
                          │  
                          ▼  
                 ┌─────────────────┐  
                 │   JD Analyzer   │  
                 │      LLM        │  
                 └────────┬────────┘  
                          │  
                          ▼  
                 ┌─────────────────┐  
                 │ Requirements    │  
                 │ Normalization   │  
                 └────────┬────────┘  
                          │  
                          ▼  
          ┌───────────────┴────────────────┐  
          │                                │  
          ▼                                ▼  
   Exact Matching                   Semantic Matching  
          │                                │  
          │                           Embeddings  
          │                                │  
          └───────────────┬────────────────┘  
                          ▼  
                 ┌─────────────────┐  
                 │ Matching Engine │  
                 │  Business Rules │  
                 └────────┬────────┘  
                          │  
                          ▼  
                 ┌─────────────────┐  
                 │  Gap Analysis   │  
                 └────────┬────────┘  
                          │  
                          ▼  
                 ┌─────────────────┐  
                 │ Resume Optimizer│  
                 │      LLM        │  
                 └────────┬────────┘  
                          │  
                          ▼  
                 ┌─────────────────┐  
                 │ Claim Validator │  
                 │ Rules \+ LLM     │  
                 └────────┬────────┘  
                          │  
                          ▼  
                 ┌─────────────────┐  
                 │ Candidate Review│  
                 └─────────────────┘  
---

# **12.2 Divide AI responsibilities into three categories**

This will make the architecture much easier to understand.

## **A. LLM**

Use the LLM for tasks involving **language understanding and generation**.

LLM  
├── Resume extraction  
├── JD interpretation  
├── Requirement classification  
├── Semantic interpretation  
├── Resume rewriting  
├── Change explanation  
└── Claim extraction  
---

## **B. Embeddings**

Use embeddings for **semantic retrieval and similarity**.

Embeddings  
├── Similar skills  
├── Similar responsibilities  
├── Related technologies  
├── Relevant career claims  
└── Requirement ↔ claim retrieval  
---

## **C. Deterministic Python logic**

Use normal application code for **truth and decisions**.

Python Rules  
├── Dates  
├── Years of experience  
├── Experience type  
├── Evidence status  
├── Candidate approval  
├── Score calculation  
├── Unsupported claims  
├── Versioning  
└── Permissions

This separation is extremely important.

---

# **12.3 AI Module 1 — Resume/Profile Extraction**

Input:

resume.pdf

Pipeline:

PDF/DOCX  
   ↓  
Document Parser  
   ↓  
Extracted Text  
   ↓  
LLM  
   ↓  
Structured JSON  
   ↓  
Schema Validation  
   ↓  
Candidate Review

Example:

{  
  "experiences": \[  
    {  
      "company": "ABC Technologies",  
      "role": "Python Backend Developer",  
      "start\_date": "2024-01",  
      "end\_date": null  
    }  
  \],  
  "skills": \[  
    "Python",  
    "FastAPI",  
    "PostgreSQL"  
  \]  
}

### **Important**

The LLM's response is:

PROPOSAL

not:

TRUTH

The candidate reviews it before trusted profile data is established.

---

# **12.4 AI Module 2 — JD Analyzer**

Input:

Job Description

The LLM needs to understand more than keywords.

For example:

> "Looking for a backend developer with strong Python experience who has built REST APIs using FastAPI and has experience deploying containerized applications."

We want:

{  
  "requirements": \[  
    {  
      "skill": "Python",  
      "type": "skill",  
      "importance": "required"  
    },  
    {  
      "skill": "REST API",  
      "type": "skill",  
      "importance": "required"  
    },  
    {  
      "skill": "FastAPI",  
      "type": "skill",  
      "importance": "required"  
    },  
    {  
      "skill": "Docker",  
      "type": "skill",  
      "importance": "preferred"  
    }  
  \]  
}  
---

# **12.5 Requirement classification**

Every requirement should ideally be classified.

### **Required**

The employer explicitly expects it.

### **Preferred**

Useful but not necessarily mandatory.

### **Contextual**

Relevant background that helps but isn't a direct skill requirement.

Potentially later:

### **Disqualifier**

Something that could make the candidate ineligible.

For example:

Work authorization required

This shouldn't be treated like a normal skill.

---

# **12.6 Requirement categories**

We should also classify requirements by category.

For example:

Skill  
Experience  
Education  
Certification  
Responsibility  
Domain  
Location  
Work authorization  
Employment type

So:

> "3+ years Python"

becomes:

category \= experience  
skill \= Python  
minimum\_years \= 3  
importance \= required

Whereas:

> "Bachelor's degree in Computer Science"

becomes:

category \= education  
degree \= Bachelor's  
field \= Computer Science  
importance \= required

This makes matching much more reliable.

---

# **12.7 AI Module 3 — Skill Normalization**

This is where we combine deterministic mapping and AI.

Suppose the JD contains:

Postgres

Candidate profile contains:

PostgreSQL

We should normalize:

Postgres  
     ↓  
PostgreSQL

Similarly:

RESTful API  
REST API  
REST APIs  
REST-based APIs

can map to:

REST API  
---

# **12.8 Do not use embeddings for everything**

A common mistake would be:

JD  
 ↓  
Embedding  
 ↓  
Resume  
 ↓  
Similarity  
 ↓  
Score

and call that an ATS/matching engine.

That's too simplistic.

Instead:

                 Requirement  
                       │  
        ┌──────────────┼───────────────┐  
        ▼              ▼               ▼  
      Exact        Normalized       Semantic  
      Match           Match          Match  
        │              │               │  
        └──────────────┼───────────────┘  
                       ▼  
                Candidate Claims  
                       │  
        ┌──────────────┼───────────────┐  
        ▼              ▼               ▼  
   Experience      Evidence        Context  
        │              │               │  
        └──────────────┼───────────────┘  
                       ▼  
                 Final Decision  
---

# **12.9 Exact matching**

Example:

JD:  
Python

Candidate:  
Python

Easy.

match \= exact

Highest confidence.

---

# **12.10 Normalized matching**

Example:

JD:  
Postgres

Candidate:  
PostgreSQL

Our canonical skill dictionary says:

Postgres → PostgreSQL

Therefore:

match \= normalized

Again, high confidence.

---

# **12.11 Semantic matching**

Now consider:

JD:  
"Experience building RESTful APIs"

Candidate claim:

"Developed backend APIs using FastAPI."

These aren't exact strings.

But they're semantically related.

Embeddings can help us retrieve this claim.

Then the business logic evaluates:

Does the claim actually satisfy the requirement?

This distinction is critical.

---

# **12.12 Retrieval vs Decision**

Think of embeddings as a **candidate finder**.

Example:

Requirement:  
Build RESTful APIs  
       ↓  
Embedding  
       ↓  
Find top 10 related career claims  
       ↓  
Claim 1  
Claim 2  
Claim 3  
...  
       ↓  
Business rules  
       ↓  
Determine actual match

So:

> **Embeddings retrieve candidates; rules decide the result.**

---

# **12.13 Experience matching**

This is where our system becomes significantly better than a keyword matcher.

JD:

Python — 3+ years

Candidate:

Python  
Professional  
2.5 years

Result:

PARTIAL

Not:

MATCH

And definitely not:

3 years  
---

# **12.14 Experience type matching**

Suppose:

JD:  
3 years professional Kubernetes experience

Candidate:

Kubernetes  
Personal project  
1 year

The system should say:

GAP / PARTIAL

depending on the scoring policy.

It must not count personal project time as professional experience.

---

# **12.15 Evidence-aware matching**

Suppose:

Candidate:  
AWS

but status:

Self-declared

The matcher should be more cautious than:

AWS  
Evidence-backed  
Professional  
2 years

We can incorporate evidence status into the confidence of the match.

For example:

Evidence-backed professional  
      ↓  
High confidence

Candidate-confirmed  
      ↓  
High confidence

Self-declared  
      ↓  
Medium confidence

Needs clarification  
      ↓  
Low confidence

Unsupported  
      ↓  
No match

The exact numerical weights are **TO FINALIZE**.

---

# **12.16 Match result model**

Each requirement should produce:

MatchResult  
───────────  
requirement\_id  
candidate\_claim\_id  
match\_type  
confidence  
score  
reason

For example:

{  
  "requirement": "Python 3+ years",  
  "candidate\_claim": "Python backend development",  
  "match\_type": "partial",  
  "confidence": 0.92,  
  "score": 0.75,  
  "reason": "Candidate has approximately 2.5 years of professional Python experience against the requested 3+ years."  
}  
---

# **12.17 Match types**

Let's establish these as our initial vocabulary:

STRONG\_MATCH  
PARTIAL\_MATCH  
GAP  
UNKNOWN

### **Strong Match**

Evidence strongly supports the requirement.

### **Partial Match**

Candidate has relevant experience but does not fully satisfy the requirement.

### **Gap**

No relevant supported evidence.

### **Unknown**

There may be relevant information, but the system needs clarification.

---

# **12.18 Overall Job Alignment Score**

Now we need to combine individual requirements.

Suppose:

Required:  
Python        0.75  
FastAPI       1.00  
PostgreSQL    1.00

Preferred:  
Docker        1.00  
AWS           0.50  
Kubernetes    0.25

We shouldn't simply average them.

Missing a required requirement should matter more than missing a preferred one.

Conceptually:

Required requirements  
        ↓  
High weight

Preferred requirements  
        ↓  
Lower weight

So:

Overall Score \=  
weighted requirement coverage

But we should **not finalize the exact formula yet**.

We'll benchmark and test it using sample JDs.

---

# **12.19 Important: Score ≠ qualification**

Suppose:

Job Alignment \= 87%

That does **not** mean:

> "You qualify."

It means:

> "Based on the available candidate information and the selected matching methodology, the candidate's profile is strongly aligned with the analyzed job requirements."

This wording matters.

---

# **12.20 Gap Analysis Engine**

After matching:

Match Results  
      ↓  
Gap Analyzer

Produces:

Strong Matches  
Partial Matches  
Gaps  
Unknowns

Example:

🟢 Python  
🟢 FastAPI  
🟢 PostgreSQL

🟡 Docker  
🟡 AWS

🔴 Kubernetes

⚪ CI/CD

The candidate should also see **why**.

---

# **12.21 Resume Optimization Engine**

Now we have:

Career Profile  
\+  
Relevant Claims  
\+  
Job Requirements  
\+  
Match Results  
\+  
Gap Analysis

The optimizer should answer:

> "How can I present the candidate's existing experience more effectively for this specific job?"

It should not answer:

> "How can I make the candidate look qualified?"

That distinction should remain central.

---

# **12.22 What the optimizer is allowed to do**

### **Reorder**

Move relevant experience higher.

### **Rewrite**

Improve wording while preserving meaning.

### **Prioritize**

Put relevant skills/projects before less relevant ones.

### **Condense**

Reduce irrelevant information.

### **Normalize**

Use standard terminology.

### **Improve keywords**

Use JD terminology **when the candidate genuinely has the corresponding experience**.

---

# **12.23 What the optimizer cannot do**

It cannot:

Add skill  
Increase years  
Invent responsibility  
Invent achievement  
Invent project  
Invent certification  
Change dates  
Convert learning into professional experience  
Convert personal project into professional experience

For example:

Candidate:

> "Completed a Kubernetes course."

Optimizer cannot produce:

> "Managed Kubernetes production clusters."

❌

---

# **12.24 Prompt architecture**

We should not create one enormous prompt.

Instead, separate prompts by task:

prompts/  
├── resume\_extraction.py  
├── jd\_analysis.py  
├── skill\_normalization.py  
├── resume\_optimization.py  
├── change\_explanation.py  
└── claim\_extraction.py

Each prompt has:

System instructions  
Input schema  
Output schema  
Rules  
Examples where useful  
---

# **12.25 Structured outputs**

We should strongly prefer structured output.

Instead of:

The candidate seems to be a good match because...

the JD analyzer should return structured data:

{  
  "requirements": \[...\]  
}

Then Python validates it.

Pipeline:

LLM  
 ↓  
JSON  
 ↓  
Pydantic validation  
 ↓  
Business validation  
 ↓  
Database

This reduces unpredictable behavior.

---

# **12.26 LLM should not directly modify the database**

Never:

LLM  
 ↓  
UPDATE career\_claims

Instead:

LLM  
 ↓  
Proposal  
 ↓  
Schema validation  
 ↓  
Business rules  
 ↓  
Candidate review  
 ↓  
Database

This should be a **non-negotiable architecture rule**.

---

# **12.27 Claim Validator**

This is probably our most important AI safety component.

Input:

Generated Resume

First:

Generated Resume  
       ↓  
Claim Extraction

Suppose it extracts:

Claim 1:  
Developed Python APIs.

Claim 2:  
Designed microservices.

Claim 3:  
Managed AWS infrastructure.

Then:

Claim 1 → Career Claim exists → PASS  
Claim 2 → No supporting claim → BLOCK  
Claim 3 → Only learning evidence → BLOCK  
---

# **12.28 Claim validation isn't just keyword checking**

Suppose the profile contains:

> "Worked on Docker deployment."

Generated resume says:

> "Architected container orchestration infrastructure using Docker."

Keyword matching sees:

Docker ✓

but that's not enough.

The validator needs to compare **factual strength and meaning**.

This is where we can use an LLM as a secondary semantic validator, but the final enforcement remains a business rule.

---

# **12.29 Claim validation levels**

We can define:

PASS  
WARNING  
BLOCK

### **PASS**

Generated claim is supported.

### **WARNING**

Claim is probably supported but has ambiguity or needs candidate review.

### **BLOCK**

No evidence or clear overstatement.

For example:

"Developed APIs using Python."  
→ PASS

"Designed APIs using Python."  
→ WARNING

"Architected distributed systems using Python."  
→ BLOCK

Exact thresholds will be finalized later.

---

# **12.30 AI Provider Strategy**

We already decided:

### **Development**

Ollama

### **Cloud fallback**

Gemini

### **Production**

Benchmark:  
Gemini  
OpenAI  
Potentially other providers

The application sees:

LLMProvider

not a specific vendor.

---

# **12.31 Model selection by task**

We don't necessarily need one model for everything.

For example:

Task                         Model class  
────────────────────────────────────────────  
JD classification             Smaller/fast model  
Skill extraction              Smaller/fast model  
Resume extraction             Medium model  
Resume rewriting              Stronger model  
Claim validation              Strong model  
Complex matching explanation  Strong model

This can reduce cost later.

However, **we should not optimize model-per-task prematurely**.

For MVP:

> Start with one capable local model and benchmark it.

Then specialize only where useful.

---

# **12.32 Embedding architecture**

We'll create:

EmbeddingProvider

with:

embed(text)  
embed\_batch(texts)

Candidate claims:

"Developed REST APIs using FastAPI"

→ vector

Job requirement:

"Experience building RESTful APIs with FastAPI"

→ vector

Then pgvector retrieves similar claims.

---

# **12.33 What should be embedded?**

For MVP:

### **Definitely**

Career Claims  
Job Requirements

### **Potentially later**

Projects  
Experience descriptions  
Skills  
Resume sections

But we should avoid embedding every possible field without a reason.

---

# **12.34 Matching architecture**

Our actual matching engine can look like:

                Job Requirement  
                       │  
                       ▼  
             ┌──────────────────┐  
             │ Normalize skill  │  
             └────────┬─────────┘  
                      │  
          ┌───────────┴───────────┐  
          ▼                       ▼  
     Exact Match             Vector Search  
          │                       │  
          └───────────┬───────────┘  
                      ▼  
              Candidate Claims  
                      │  
                      ▼  
             Evidence Evaluation  
                      │  
                      ▼  
             Experience Evaluation  
                      │  
                      ▼  
             Requirement Weight  
                      │  
                      ▼  
               Match Result  
---

# **12.35 Example: Complete matching decision**

JD:

> "3+ years of Python backend development."

Candidate:

Claim:  
Developed backend APIs using Python.

Experience:  
Professional

Duration:  
2.5 years

Evidence:  
Resume \+ candidate confirmation

Process:

Semantic similarity  
        ↓  
High

Skill match  
        ↓  
Python ✓

Experience type  
        ↓  
Professional ✓

Years  
        ↓  
2.5 \< 3

Evidence  
        ↓  
Strong

Final:  
PARTIAL MATCH

This is exactly the behavior we want.

---

# **12.36 Example: semantic false positive**

JD:

> "Experience designing distributed systems."

Candidate:

> "Built a Python REST API for a college project."

Embedding similarity might be:

0.72

But:

Professional? No  
Distributed systems evidence? No  
Design/architecture evidence? No

Therefore:

❌ GAP / insufficient evidence

This example demonstrates why **embeddings cannot be our final judge**.

---

# **12.37 AI/ML pipeline summary**

Our final intelligence architecture becomes:

                RESUME  
                    │  
                    ▼  
             Resume Parser  
                    │  
                    ▼  
             LLM Extraction  
                    │  
                    ▼  
           Candidate Proposal  
                    │  
                    ▼  
           Candidate Approval  
                    │  
                    ▼  
        ┌──────────────────────┐  
        │   Career Knowledge   │  
        │        Base          │  
        └──────────┬───────────┘  
                   │  
                   │  
                   ▼  
                 JOB JD  
                   │  
                   ▼  
              JD Analyzer  
                   │  
                   ▼  
        Structured Requirements  
                   │  
                   ▼  
             Normalization  
                   │  
                   ▼  
          ┌────────┴─────────┐  
          ▼                  ▼  
       Exact             Embedding  
       Match              Search  
          │                  │  
          └────────┬─────────┘  
                   ▼  
             Match Engine  
                   │  
          ┌────────┴─────────┐  
          ▼                  ▼  
     Strong/Partial      Gaps/Unknown  
          │                  │  
          └────────┬─────────┘  
                   ▼  
             Resume Optimizer  
                   │  
                   ▼  
            Proposed Changes  
                   │  
                   ▼  
            Claim Validator  
                   │  
             ┌─────┴─────┐  
             ▼           ▼  
           PASS        BLOCK  
             │  
             ▼  
       Candidate Approval  
             │  
             ▼  
        Final Resume  
---

# **12.38 What is decided vs what isn't**

### **✅ DECIDED**

* Hybrid AI architecture.  
* LLM for language understanding/generation.  
* Embeddings for semantic retrieval.  
* Deterministic logic for truth/business decisions.  
* Structured LLM outputs.  
* LLM cannot directly modify trusted data.  
* Exact \+ normalized \+ semantic matching.  
* Evidence and experience context affect matching.  
* Claim validation occurs before final resume.  
* Unsupported claims must be blocked/clarified.  
* Job Alignment Score instead of universal "ATS pass score".  
* Start with one local Ollama model for MVP and benchmark it.

### **🟡 TO FINALIZE**

* Exact embedding model.  
* Exact vector dimension.  
* Exact LLM model for Ollama.  
* Exact matching weights.  
* Exact Job Alignment Score formula.  
* Confidence thresholds.  
* Claim-strength taxonomy/thresholds.  
* Whether an LLM or rules should handle particular edge cases.  
* Evaluation dataset and benchmark methodology.

### **🔵 FUTURE**

* Model-per-task routing.  
* Fine-tuning.  
* Learning-to-rank matching.  
* Candidate-specific recommendation models.  
* Automated evaluation pipelines.  
* Production model routing based on cost/latency.  
* More advanced evidence graph reasoning.

---

# **12.39 One major recommendation before we continue**

I **do not recommend training a custom ML model yet**.

For your project, the first version should be:

LLM  
\+  
Embeddings  
\+  
Rules  
\+  
PostgreSQL/pgvector

rather than:

Train custom NLP model  
\+  
Train classifier  
\+  
Fine-tune LLM  
\+  
Train ranking model

Why?

Because you currently don't have the most valuable training data:

Thousands of real JDs  
\+  
Candidate profiles  
\+  
Human-approved matches  
\+  
Human-approved resume changes  
\+  
Successful/unsuccessful application outcomes

Once the product collects enough high-quality labeled data, custom ML becomes much more interesting.

---

# **12.40 The most important mental model**

Think of the AI system as four layers:

┌──────────────────────────────────┐  
│ Layer 4 — Generation             │  
│ "How should we present this?"    │  
│            LLM                   │  
├──────────────────────────────────┤  
│ Layer 3 — Interpretation         │  
│ "What does this requirement mean?"│  
│            LLM                   │  
├──────────────────────────────────┤  
│ Layer 2 — Retrieval              │  
│ "What candidate information is    │  
│  potentially relevant?"          │  
│            Embeddings            │  
├──────────────────────────────────┤  
│ Layer 1 — Truth & Rules          │  
│ "Is the candidate actually        │  
│  allowed to claim this?"         │  
│            Python/DB             │  
└──────────────────────────────────┘

**Layer 1 is the authority.**

That is the key architectural idea behind the whole project.

---

## **Next Step — Step 13**

Now that we know **what the AI should do**, the next step should be:

### **Step 13 — LLM Contracts, Prompt Architecture & Structured Output Schemas**

We'll define the actual contracts between our application and the LLM:

Resume Extraction → JSON schema  
JD Analysis        → JSON schema  
Skill Normalization→ JSON schema  
Resume Optimization→ JSON schema  
Claim Extraction   → JSON schema  
Claim Validation   → JSON schema  
Change Explanation → JSON schema

We'll also design:

* system vs user prompts,  
* what information each prompt receives,  
* what information it must never receive,  
* structured output validation,  
* retries,  
* hallucination controls,  
* prompt versioning,  
* model/provider differences,  
* and how the same prompt contract can work with **Ollama today and Gemini/OpenAI later**.

# step 13

Absolutely. We’ll move to **Step 13: LLM Contracts, Prompt Architecture & Structured Output Schemas**.

This is an important step because we need to define **exactly how our backend communicates with the LLM** before we start implementing the AI services.

### **Step 13 — What we’ll design**

We’ll cover:

1. **LLM service architecture**  
   * `LLMProvider`  
   * Ollama implementation  
   * future Gemini/OpenAI implementations  
   * fallback behavior  
2. **Prompt architecture**  
   * system prompts  
   * task prompts  
   * candidate/job context  
   * what information is allowed to reach the LLM  
   * avoiding one giant prompt  
3. **Structured output contracts**  
   * Resume extraction schema  
   * JD analysis schema  
   * requirement schema  
   * matching interpretation schema  
   * resume optimization schema  
   * claim validation schema  
4. **Pydantic models**  
   * LLM output → Pydantic validation  
   * invalid output handling  
   * schema versioning

**AI operation lifecycle**  
Request  
   ↓  
Build Context  
   ↓  
Prompt  
   ↓  
LLM  
   ↓  
Structured JSON  
   ↓  
Pydantic Validation  
   ↓  
Business Rules  
   ↓  
Candidate Review  
   ↓

5. Database  
6. **Prompt safety and truth constraints**  
   * no fabrication  
   * no unsupported skills  
   * no date changes  
   * no experience-type changes  
   * no automatic trusted-data updates  
7. **Model-specific considerations**  
   * local Ollama  
   * cloud fallback  
   * structured output capability  
   * model benchmarking

### **Most important design rule**

We should establish this before coding:

> **The LLM never directly decides what becomes a trusted candidate fact.**

Instead:

LLM  
 ↓  
Proposal  
 ↓  
Schema validation  
 ↓  
Business validation  
 ↓  
Candidate approval  
 ↓  
Trusted Career Profile

And for resume generation:

Career Profile  
      \+  
Job Requirements  
      ↓  
Relevant Claims  
      ↓  
LLM proposes resume changes  
      ↓  
Claim Validator  
      ↓  
PASS / WARNING / BLOCK  
      ↓  
Candidate approval  
      ↓  
Final Resume

So in this step, we'll effectively define the **contract between our application and AI layer**. Once this is finalized, Step 14 can move into the actual **FastAPI backend project structure and implementation plan**.

# finalization

Yes. Let’s **freeze Step 13 for Version 1** and move forward. We’ll treat the following as the V1 contract unless implementation/testing reveals a concrete issue.

# **Step 13 — Finalized for V1**

## **1\. V1 AI architecture**

                   ┌─────────────────────┐  
                    │    FastAPI API      │  
                    └──────────┬──────────┘  
                               ↓  
                    ┌─────────────────────┐  
                    │ Application Service │  
                    └──────────┬──────────┘  
                               ↓  
                    ┌─────────────────────┐  
                    │    AI Service       │  
                    └──────────┬──────────┘  
                               ↓  
              ┌────────────────────────────────┐  
              │       LLMProvider               │  
              │                                │  
              │  Ollama (V1 primary)           │  
              │  Gemini (optional fallback)    │  
              └───────────────┬────────────────┘  
                              ↓  
                     Structured JSON  
                              ↓  
                     Pydantic Validation  
                              ↓  
                     Business Validation  
                              ↓  
                     Database / Candidate

### **V1 providers**

| Component | V1 |
| ----- | ----- |
| Primary LLM | Ollama |
| Cloud fallback | Gemini, optional |
| Embeddings | Local/open-source |
| Database | PostgreSQL \+ pgvector |
| Storage | Local filesystem |
| Queue | None |
| Redis | None |

The business layer will **never depend directly on Ollama or Gemini**.

---

# **2\. LLM Provider contract**

We'll use an abstraction similar to:

class LLMProvider(ABC):

    @abstractmethod  
    async def generate(  
        self,  
        system\_prompt: str,  
        user\_prompt: str,  
    ) \-\> str:  
        pass

    @abstractmethod  
    async def generate\_structured(  
        self,  
        system\_prompt: str,  
        user\_prompt: str,  
        response\_schema: type\[BaseModel\],  
    ) \-\> BaseModel:  
        pass

Then:

LLMProvider  
   │  
   ├── OllamaProvider  
   │  
   └── GeminiProvider

Later:

  ├── OpenAIProvider  
   ├── AnthropicProvider  
   └── OtherProvider

No application-service code needs to change.

---

# **3\. Prompt architecture — finalized**

We will **not** create one giant prompt.

Instead, each AI operation gets its own prompt.

prompts/  
│  
├── resume/  
│   └── extraction.py  
│  
├── job/  
│   └── analysis.py  
│  
├── matching/  
│   └── interpretation.py  
│  
├── optimization/  
│   └── resume\_optimization.py  
│  
└── validation/  
    └── claim\_validation.py

Every operation has:

System Instructions  
        \+  
Task Instructions  
        \+  
Structured Context  
        ↓  
       LLM  
        ↓  
 Structured Response

This makes prompts:

* easier to test  
* easier to version  
* easier to debug  
* easier to replace  
* safer  
* easier to benchmark across models

---

# **4\. V1 AI operations**

We will support these AI operations:

### **A. Resume extraction**

Input:

Resume text

Output:

Candidate information  
Experiences  
Projects  
Education  
Certifications  
Skills  
Potential claims

Important:

**Extraction does not automatically make information trusted.**

For example:

Resume says:  
"Built REST APIs using Python"

LLM can extract:

{  
  "claim": "Built REST APIs using Python",  
  "skill": "Python",  
  "experience\_type": "professional"  
}

But the system still needs candidate confirmation/evidence rules.

---

### **B. JD analysis**

Input:

Job Description

Output:

Job title  
Company  
Required skills  
Preferred skills  
Experience requirements  
Education  
Responsibilities  
Keywords  
Other requirements

Each requirement becomes a structured object.

Example:

{  
  "requirement\_text": "3+ years of Python backend development",  
  "requirement\_type": "required",  
  "importance": 1.0,  
  "skill": "Python",  
  "minimum\_years": 3,  
  "experience\_type": "professional"  
}  
---

# **5\. Matching**

Matching is **not purely an LLM task**.

This is critical.

JD Requirement  
       ↓  
Normalization  
       ↓  
Exact Matching  
       ↓  
Semantic Retrieval  
       ↓  
Candidate Claims  
       ↓  
Evidence  
       ↓  
Experience Type  
       ↓  
Years  
       ↓  
Business Rules  
       ↓  
Match Result

LLM can help interpret language.

But Python calculates the actual result.

Example:

Requirement:  
3+ years professional Python

Candidate:  
Python  
Professional  
2.4 years  
Evidence-backed

Result:

PARTIAL\_MATCH

The LLM cannot simply say:

> "The candidate is experienced in Python, therefore STRONG\_MATCH."

---

# **6\. Resume optimization contract**

The optimizer receives:

Candidate Career Profile  
\+  
Relevant Career Claims  
\+  
Job Requirements  
\+  
Match Results  
\+  
Existing Resume

It returns **proposed changes**, not a final trusted truth.

Example:

{  
  "change\_type": "REWRITE",  
  "original\_text": "Worked on APIs",  
  "proposed\_text": "Developed REST APIs using Python",  
  "reason": "Better alignment with the job's Python backend requirement",  
  "career\_claim\_id": "claim\_123"  
}

This is exactly the behavior we want.

---

# **7\. Truth constraints**

Every optimization prompt will contain explicit rules.

The LLM must not:

❌ Add unsupported skills  
❌ Add companies  
❌ Add projects  
❌ Add certifications  
❌ Change dates  
❌ Increase years of experience  
❌ Invent achievements  
❌ Invent metrics  
❌ Convert learning into professional experience  
❌ Convert personal projects into professional experience  
❌ Claim leadership without evidence  
❌ Claim architecture/design responsibility without evidence

It may:

✅ Rephrase  
✅ Reorder  
✅ Condense  
✅ Improve grammar  
✅ Normalize terminology  
✅ Prioritize relevant experience  
✅ Improve keyword alignment  
✅ Select relevant existing claims  
---

# **8\. Claim validation**

This becomes our **final AI safety layer**.

Generated Resume  
       ↓  
Claim Extraction  
       ↓  
Compare against Career Claims  
       ↓  
Evidence Check  
       ↓  
Date Check  
       ↓  
Experience Type Check  
       ↓  
Claim Strength Check  
       ↓  
Validation Result

Possible result:

PASS  
WARNING  
BLOCK  
NEEDS\_CLARIFICATION

Example:

Candidate has:

> "Used Kubernetes for a personal project."

Generated resume says:

> "Managed Kubernetes infrastructure in production."

Validator:

BLOCK

Because:

personal  
      ↓  
professional production

is an unsupported factual transformation.

---

# **9\. Pydantic is mandatory**

We won't trust raw LLM JSON.

LLM  
 ↓  
Raw JSON  
 ↓  
Pydantic  
 ↓  
Valid structured object  
 ↓  
Business rules

For example:

class JobRequirement(BaseModel):  
    requirement\_text: str  
    requirement\_type: RequirementType  
    importance: float  
    skill: str | None \= None  
    minimum\_years: float | None \= None  
    experience\_type: ExperienceType | None \= None

If the model produces:

{  
  "importance": "very important"  
}

when we require a float:

Pydantic validation  
       ↓  
INVALID  
       ↓  
retry / repair / fail

We never blindly insert it into PostgreSQL.

---

# **10\. AI failure handling**

V1 statuses:

PENDING  
PROCESSING  
COMPLETED  
FAILED

Error codes:

LLM\_UNAVAILABLE  
LLM\_TIMEOUT  
LLM\_INVALID\_OUTPUT  
LLM\_SCHEMA\_ERROR  
EMBEDDING\_FAILED  
FILE\_UNSUPPORTED  
EXTRACTION\_FAILED  
JD\_ANALYSIS\_FAILED  
VALIDATION\_FAILED

Fallback behavior:

Ollama  
  ↓  
Unavailable?  
  ↓  
Gemini  
  ↓  
Generate  
  ↓  
Validate

But:

Ollama  
 ↓  
Bad/fabricated result

does **not** mean:

→ Gemini

We don't use another model to hide a business-validation failure.

---

# **11\. Prompt versioning**

This is important for debugging.

Every AI operation should record:

operation\_type  
provider  
model  
prompt\_version  
input\_hash  
output  
status  
created\_at

For example:

operation\_type: JD\_ANALYSIS  
provider: ollama  
model: llama...  
prompt\_version: jd\_analysis\_v1  
status: COMPLETED

Later, if we change the prompt:

jd\_analysis\_v2

we can determine why results changed.

---

# **12\. AI audit trail**

Our `ai_operations` table therefore becomes important.

Conceptually:

AI Operation  
─────────────  
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

This gives us reproducibility and debugging capability.

---

# **13\. Final V1 AI principle**

The architecture is now officially:

> **LLM proposes → Pydantic validates structure → deterministic rules validate facts → candidate approves → database stores trusted information.**

And for matching:

> **Embeddings retrieve → rules decide.**

And for resume generation:

> **Career Profile is the source of truth; resume is a derived artifact.**

These three principles should guide the entire implementation.

---

# **Step 13 Status**

| Decision | V1 Status |
| ----- | ----- |
| LLM abstraction | ✅ Final |
| Ollama primary | ✅ Final |
| Gemini fallback | ✅ Final/Optional |
| Modular prompts | ✅ Final |
| Structured JSON | ✅ Final |
| Pydantic validation | ✅ Final |
| LLM cannot directly update trusted DB | ✅ Final |
| Exact \+ semantic matching | ✅ Final |
| Deterministic truth validation | ✅ Final |
| Claim-strength validation | ✅ Final |
| Candidate approval | ✅ Final |
| Prompt versioning | ✅ Final |
| AI audit trail | ✅ Final |
| Custom ML training | ❌ Not V1 |
| Redis/queue | ❌ Not V1 |
| Microservices | ❌ Not V1 |

---

# **Next: Step 14 — Backend Project Structure**

Now we can finally start designing the **actual codebase**.

We'll define:

backend/  
├── app/  
│   ├── api/  
│   ├── core/  
│   ├── models/  
│   ├── schemas/  
│   ├── services/  
│   ├── repositories/  
│   ├── ai/  
│   ├── prompts/  
│   ├── validators/  
│   ├── storage/  
│   └── main.py  
│  
├── migrations/  
├── tests/  
├── .env  
├── requirements.txt  
└── README.md

Then we'll decide **exactly what belongs in each folder, how the layers communicate, dependency injection, configuration management, authentication boundaries, and the implementation order**.

After that, we'll move from architecture into actual **FastAPI \+ PostgreSQL code**, starting with the first V1 module: **authentication (Sign Up / Sign In / JWT / user / dashboard)**.

