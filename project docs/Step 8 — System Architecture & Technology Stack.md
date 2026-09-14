Now we're moving from **product design → technical design**.

# **Step 8 — System Architecture & Technology Stack**

Before choosing technologies, let's establish one principle:

> **We should build the simplest architecture that can reliably enforce our product's core rule: AI can suggest, but the system validates and the candidate controls the final result.**

For your project, I would recommend a **modular monolith** for the MVP rather than microservices.

---

# **8.1 High-Level Architecture**

The system can look like this:

                        ┌───────────────────┐  
                         │     Candidate     │  
                         └─────────┬─────────┘  
                                   │  
                                   ▼  
                         ┌───────────────────┐  
                         │     Frontend      │  
                         │      React        │  
                         └─────────┬─────────┘  
                                   │ REST API  
                                   ▼  
┌─────────────────────────────────────────────────────────────┐  
│                    BACKEND APPLICATION                      │  
│                                                             │  
│  Auth  │ Profile │ Resume │ JD │ Matching │ Optimization   │  
│                                                             │  
│              ┌──────────────────────────┐                   │  
│              │     AI Orchestration     │                   │  
│              └────────────┬─────────────┘                   │  
└───────────────────────────┼─────────────────────────────────┘  
                            │  
             ┌──────────────┼───────────────┐  
             ▼              ▼               ▼  
        PostgreSQL      Object Storage    AI/LLM  
             │              │               │  
             │              │          ┌────┴────┐  
             │              │          │         │  
             ▼              ▼          ▼         ▼  
         pgvector        Resume      LLM      Embeddings  
                         files

Let's break this down.

---

# **8.2 Frontend**

I'd recommend:

### **React \+ TypeScript**

Why?

Because the product will have quite a few interactive screens:

* Career profile  
* Resume upload  
* JD analysis  
* Match dashboard  
* Change comparison  
* Approval workflow  
* Resume preview

TypeScript will also help keep the frontend/backend data contracts cleaner.

Potential stack:

React  
TypeScript  
Vite  
Tailwind CSS

You don't need something overly complicated.

---

# **8.3 Backend**

For your project, I'd recommend:

### **Python \+ FastAPI**

This fits particularly well because our system has substantial AI/ML work.

Backend responsibilities:

Authentication  
Profile management  
Resume processing  
JD processing  
AI orchestration  
Matching  
Validation  
Resume generation  
Application management

FastAPI also gives you:

* REST APIs  
* Request validation  
* Async support  
* Automatic OpenAPI documentation  
* Good Python AI ecosystem integration

---

# **8.4 Database**

I'd choose:

# **PostgreSQL**

And I would use **pgvector** as an extension.

This gives us:

### **Normal relational data**

users  
candidate\_profiles  
experiences  
projects  
skills  
education  
certifications  
job\_descriptions  
job\_requirements  
resume\_versions  
resume\_changes  
applications

plus:

### **Vector data**

candidate evidence embeddings  
JD requirement embeddings  
skill embeddings

So we don't need a separate vector database initially.

---

# **8.5 Why PostgreSQL \+ pgvector?**

This is particularly appropriate for your project.

We need relationships such as:

Candidate  
  ↓  
Experience  
  ↓  
Skill  
  ↓  
Evidence  
  ↓  
Job Requirement  
  ↓  
Match

That's naturally relational.

Then we also need semantic search:

> "Find candidate experience relevant to this requirement."

That's where pgvector helps.

So we get:

> **Relational database \+ vector search in one system.**

---

# **8.6 Why not SQLite?**

You previously asked about SQLite for your document Q\&A project, and here the situation is different.

For this product, I'd choose PostgreSQL from the beginning because we have:

* Multiple related entities  
* Concurrent users  
* Structured career data  
* Job/application relationships  
* Vector search  
* Potential background processing  
* Future scaling

SQLite could work for a prototype, but PostgreSQL is a better fit for a real-world architecture.

---

# **8.7 File Storage**

Resumes and documents shouldn't be stored directly inside PostgreSQL.

Use object storage.

For example:

### **Cloudflare R2**

or:

### **AWS S3**

The flow becomes:

Candidate uploads PDF  
        ↓  
Backend  
        ↓  
Object Storage  
        ↓  
file\_key stored in PostgreSQL

Database stores:

resume\_id  
candidate\_id  
file\_key  
filename  
file\_type  
created\_at

rather than the entire PDF binary.

---

# **8.8 Document Processing**

We need to process:

### **Resume**

PDF / DOCX

### **Job Description**

Initially:

Plain text

Later:

PDF / URL

The pipeline:

Document  
   ↓  
Parser  
   ↓  
Extracted Text  
   ↓  
Structure Detection  
   ↓  
LLM Extraction  
   ↓  
Candidate Claims

For PDFs, we can use appropriate Python libraries depending on whether the document is text-based or scanned.

For DOCX, Python's document-processing ecosystem is sufficient.

For scanned resumes, OCR can be added later.

---

# **8.9 AI/LLM Layer**

I'd create an internal service/module:

### **`AI Orchestrator`**

It handles calls to the LLM rather than scattering LLM calls throughout the application.

For example:

ai/  
├── jd\_analyzer.py  
├── resume\_extractor.py  
├── skill\_normalizer.py  
├── matcher.py  
├── resume\_optimizer.py  
├── change\_explainer.py  
└── claim\_validator.py

This keeps AI functionality organized.

---

# **8.10 LLM**

For the MVP, don't hard-code the entire product around one provider if you can avoid it.

Create an abstraction:

LLMProvider  
    │  
    ├── OpenAI  
    ├── Anthropic  
    └── Local model

Then your application calls:

generate\_structured\_output(...)

rather than:

openai\_specific\_function(...)

everywhere.

This gives you flexibility later.

---

# **8.11 Structured LLM Outputs**

This is important.

For JD analysis, the LLM shouldn't return:

> "This is a backend job requiring Python..."

We want structured output.

Something like:

{  
  "job\_title": "Python Backend Developer",  
  "experience": {  
    "minimum\_years": 2  
  },  
  "required\_skills": \[  
    "Python",  
    "FastAPI",  
    "PostgreSQL"  
  \],  
  "preferred\_skills": \[  
    "AWS",  
    "Docker"  
  \]  
}

The backend validates that structure before using it.

---

# **8.12 Embedding Model**

We need embeddings for semantic matching.

Conceptually:

JD requirement  
     ↓  
Embedding  
     ↓  
Vector

Candidate evidence  
     ↓  
Embedding  
     ↓  
Vector

       ↓

Similarity  
       ↓

Potential Match

The embedding model can initially be provided through your chosen AI provider or a suitable open-source model.

We don't need to train our own embedding model.

---

# **8.13 Matching Engine**

I would **not** let the LLM directly output:

> Match \= 87%.

Instead, build a hybrid matching engine.

For example:

                Requirement  
                      │  
       ┌──────────────┼──────────────┐  
       ▼              ▼              ▼  
   Exact Match    Normalized      Semantic  
                    Match           Match  
       │              │              │  
       └──────────────┼──────────────┘  
                      ▼  
                 Evidence Check  
                      │  
                      ▼  
                Experience Check  
                      │  
                      ▼  
                Requirement Type  
                Required/Preferred  
                      │  
                      ▼  
                  Final Match

This makes the result more explainable.

---

# **8.14 Example Matching Logic**

Suppose:

**JD:**

> FastAPI — Required

Candidate:

> FastAPI — evidence-backed

We might get:

Exact match       \= yes  
Evidence          \= strong  
Requirement       \= required  
Experience        \= relevant

Result:  
Strong Match

Now:

**JD:**

> Kubernetes — Required

Candidate:

> Docker — evidence-backed

Semantic similarity might be high.

But:

Candidate Kubernetes evidence \= none

Result:  
Missing

This is why **semantic similarity alone cannot determine qualification.**

---

# **8.15 Truth/Validation Engine**

This should be a separate backend component.

Potential flow:

LLM-generated resume  
        ↓  
Claim extraction  
        ↓  
Candidate claim lookup  
        ↓  
Evidence verification  
        ↓  
Rule evaluation  
        ↓  
Allowed / Blocked

For every generated claim:

claim\_id  
claim\_text  
source\_evidence  
confidence  
status

This creates auditability.

---

# **8.16 Example**

LLM generates:

> "Developed scalable REST APIs using FastAPI."

System extracts claims:

Python?       → Yes  
REST API?     → Yes  
FastAPI?      → Yes  
Scalable?     → ?

Now suppose candidate evidence only supports:

> Built REST APIs using FastAPI.

The word **"scalable"** might not be supported.

The system can either:

* remove it,  
* downgrade the wording,  
* or ask the candidate.

So the final sentence might become:

> **"Developed REST APIs using FastAPI."**

This is exactly the kind of control we want.

---

# **8.17 Resume Generation**

Once content is approved:

Approved Resume Data  
        ↓  
Template Engine  
        ↓  
PDF / DOCX

The LLM should **not** be responsible for formatting the final PDF.

It generates/optimizes the content.

A deterministic document-generation layer creates the actual document.

---

# **8.18 Resume Templates**

Initially:

### **Template 1**

ATS-friendly professional.

### **Template 2**

Simple modern.

That's enough.

We don't need 20 templates.

---

# **8.19 Background Jobs**

Some tasks may take time:

* PDF parsing  
* OCR  
* Resume extraction  
* Embedding generation  
* JD analysis  
* Resume generation

We shouldn't necessarily make the user wait on a single HTTP request.

Eventually:

Frontend  
   ↓  
POST /resume/upload  
   ↓  
Backend  
   ↓  
Job Queue  
   ↓  
Worker  
   ↓  
Process  
   ↓  
Database  
   ↓  
Frontend receives status

For MVP, we could initially keep some operations synchronous and introduce a queue when needed.

If we use one, options include:

* Celery \+ Redis  
* RQ \+ Redis  
* Dramatiq  
* A lightweight task system

I'd probably use **Celery \+ Redis** if we want to demonstrate production-style backend architecture.

But don't add it everywhere from day one.

---

# **8.20 Redis**

Redis can eventually serve multiple purposes:

### **Background job broker**

API → Redis → Worker

### **Caching**

For example:

> Same JD analyzed repeatedly?

Cache where appropriate.

### **Rate limiting**

Prevent abuse of expensive AI endpoints.

But Redis isn't mandatory for the first local prototype.

---

# **8.21 API Structure**

I'd organize the backend roughly like:

/api/v1

/auth  
  POST /register  
  POST /login

/profile  
  GET /  
  PUT /  
  POST /experience  
  POST /projects  
  POST /skills

/resumes  
  POST /upload  
  GET /  
  GET /{id}

/jobs  
  POST /  
  GET /{id}  
  POST /{id}/analyze

/matches  
  POST /job/{id}  
  GET /job/{id}

/optimization  
  POST /job/{id}/generate  
  GET /{id}/changes  
  POST /{id}/approve  
  POST /{id}/reject

/resume  
  POST /generate  
  GET /{id}/download

We can refine this once we design the database.

---

# **8.22 Security Architecture**

Because we're dealing with resumes and personal career information:

User  
 ↓  
Authentication  
 ↓  
Authorization  
 ↓  
Candidate-owned resources

A user should only be able to access:

> **their own profile, resumes, jobs, and applications.**

We should enforce ownership checks at the backend—not just hide things in the frontend.

---

# **8.23 Data Flow for the Main Use Case**

Let's trace one complete request.

### **Candidate uploads resume**

React  
  ↓  
FastAPI  
  ↓  
Object Storage  
  ↓  
Resume Processing  
  ↓  
Text Extraction  
  ↓  
LLM  
  ↓  
Structured Candidate Claims  
  ↓  
Validation  
  ↓  
Candidate Review  
  ↓  
PostgreSQL  
---

### **Candidate submits JD**

React  
  ↓  
FastAPI  
  ↓  
JD Analyzer  
  ↓  
LLM  
  ↓  
Structured Job Profile  
  ↓  
PostgreSQL  
---

### **Candidate asks for optimization**

JD  
 \+  
Career Profile  
 \+  
Evidence  
        ↓  
Matching Engine  
        ↓  
Relevant Evidence  
        ↓  
LLM  
        ↓  
Proposed Resume  
        ↓  
Claim Validator  
        ↓  
Change List  
        ↓  
Candidate Approval  
        ↓  
Final Resume  
---

# **8.24 The Most Important Boundary**

Our architecture should make this impossible:

JD  
 ↓  
LLM  
 ↓  
Directly modify Candidate Profile

Instead:

JD  
 ↓  
LLM  
 ↓  
Proposal  
 ↓  
Validation  
 ↓  
Candidate  
 ↓  
Approval  
 ↓  
Database

The **candidate profile should never be silently mutated by the LLM.**

---

# **8.25 Proposed Technology Stack**

Here's the stack I'd recommend for your project:

| Layer | Technology |
| ----- | ----- |
| Frontend | React \+ TypeScript |
| Styling | Tailwind CSS |
| Backend | Python \+ FastAPI |
| Database | PostgreSQL |
| Vector Search | pgvector |
| Cache/Queue | Redis |
| Background Jobs | Celery |
| LLM | API-based LLM provider |
| Embeddings | Embedding model |
| File Storage | Cloudflare R2 / S3 |
| PDF parsing | Python PDF tooling |
| DOCX parsing | python-docx |
| Resume generation | HTML/CSS → PDF or document generation |
| Authentication | JWT/session-based auth |
| Deployment | Docker |
| Reverse proxy | Nginx/Caddy later |
| Testing | Pytest \+ frontend testing framework |

---

# **8.26 But don't build all of this immediately**

This is important.

The architecture above is our **target architecture**, not necessarily our **Day 1 implementation**.

For your first working version:

React  
  ↓  
FastAPI  
  ↓  
PostgreSQL \+ pgvector  
  ↓  
LLM  
  ↓  
Resume Generator

That's enough.

Then introduce:

R2  
Redis  
Celery  
Monitoring  
Caching

as the project matures.

---

# **8.27 Suggested Project Structure**

A possible backend structure:

backend/  
│  
├── app/  
│   ├── main.py  
│   │  
│   ├── api/  
│   │   └── v1/  
│   │       ├── auth.py  
│   │       ├── profile.py  
│   │       ├── resumes.py  
│   │       ├── jobs.py  
│   │       ├── matching.py  
│   │       └── optimization.py  
│   │  
│   ├── models/  
│   │   ├── user.py  
│   │   ├── profile.py  
│   │   ├── experience.py  
│   │   ├── project.py  
│   │   ├── skill.py  
│   │   ├── evidence.py  
│   │   ├── job.py  
│   │   └── resume.py  
│   │  
│   ├── schemas/  
│   │  
│   ├── services/  
│   │   ├── resume\_parser.py  
│   │   ├── jd\_analyzer.py  
│   │   ├── matcher.py  
│   │   ├── optimizer.py  
│   │   ├── validator.py  
│   │   └── resume\_generator.py  
│   │  
│   ├── ai/  
│   │   ├── llm.py  
│   │   ├── embeddings.py  
│   │   └── prompts/  
│   │  
│   ├── rules/  
│   │   ├── claim\_rules.py  
│   │   ├── experience\_rules.py  
│   │   └── validation\_rules.py  
│   │  
│   └── db/  
│  
├── tests/  
│  
├── Dockerfile  
└── requirements.txt

The frontend would have its own feature-based structure.

---

# **8.28 One Architecture Decision I Strongly Recommend**

Don't make this:

FastAPI  
   │  
   ├── OpenAI call  
   ├── OpenAI call  
   ├── OpenAI call  
   ├── OpenAI call  
   └── OpenAI call

scattered throughout the code.

Instead:

Business Service  
       ↓  
AI Orchestrator  
       ↓  
LLM Provider

That lets us:

* log AI requests/results safely,  
* validate outputs,  
* swap models,  
* test components,  
* control costs,  
* add retries,  
* enforce schemas,  
* eventually use local models.

---

# **8.29 Our Architecture in One Diagram**

                        ┌──────────────┐  
                         │   CANDIDATE  │  
                         └──────┬───────┘  
                                │  
                                ▼  
                       ┌─────────────────┐  
                       │ React Frontend  │  
                       └────────┬────────┘  
                                │  
                             REST API  
                                │  
                                ▼  
┌───────────────────────────────────────────────────────────┐  
│                     FASTAPI BACKEND                       │  
│                                                           │  
│  Auth │ Profile │ Resume │ JD │ Match │ Optimize │ Apply │  
│                                                           │  
│                   AI ORCHESTRATOR                        │  
│                         │                                 │  
│            ┌────────────┼────────────┐                    │  
│            ▼            ▼            ▼                    │  
│          LLM        Embeddings    Validation              │  
│            │            │            │                    │  
│            └────────────┼────────────┘                    │  
│                         │                                 │  
│                    Business Rules                        │  
└─────────────┬───────────┼──────────────┬──────────────────┘  
              │           │              │  
              ▼           ▼              ▼  
       PostgreSQL      pgvector       Redis  
              │  
              ▼  
       Candidate Data  
       Evidence  
       Jobs  
       Matches  
       Changes  
       Versions

              │  
              ▼  
        Object Storage  
        Resume / Documents  
---

# **8.30 The Architecture's Core Philosophy**

If you remember only one diagram from this project, make it this:

                ┌──────────────┐  
                 │     LLM      │  
                 │              │  
                 │  Understand  │  
                 │  Extract     │  
                 │  Suggest     │  
                 │  Rewrite     │  
                 └──────┬───────┘  
                        │  
                     Proposal  
                        │  
                        ▼  
              ┌───────────────────┐  
              │   RULE ENGINE     │  
              │                   │  
              │ Evidence          │  
              │ Permissions       │  
              │ Validation        │  
              │ Calculations      │  
              └─────────┬─────────┘  
                        │  
                 Allowed / Blocked  
                        │  
                        ▼  
              ┌───────────────────┐  
              │     CANDIDATE     │  
              │                   │  
              │ Approve / Edit /  │  
              │ Reject            │  
              └─────────┬─────────┘  
                        │  
                        ▼  
                 FINAL RESUME

### **LLM proposes.**

### **Rules validate.**

### **Candidate decides.**

That is the architectural principle that differentiates your product from simply putting a better prompt in ChatGPT.

---

## **What we've now established**

We have gone from the original idea to a fairly concrete architecture:

**Product**

→ Verified Career Profile

**Data**

→ Candidate claims \+ evidence

**AI**

→ JD analysis \+ extraction \+ semantic matching \+ rewriting

**ML**

→ Embeddings initially; custom ML only if justified by data

**Rules**

→ Truth validation \+ permissions \+ experience calculations

**Human**

→ Confirmation \+ approval

**Backend**

→ FastAPI

**Database**

→ PostgreSQL \+ pgvector

**Frontend**

→ React \+ TypeScript

**Storage**

→ R2/S3

**Deployment**

→ Docker

Absolutely. Let’s move to **Step 8.5 — Provider Abstraction & Configuration Design**.

This step is important because you specifically want:

> **₹0-cost local development now → cloud/paid production later, without rewriting the core application.**

### **Step 8.5: Provider-Independent Architecture**

We should make the application think in terms of **capabilities**, not vendors.

For example, your business logic should say:

Generate structured JD analysis  
        ↓  
       LLM

not:

Generate structured JD analysis  
        ↓  
       Gemini

That means we define an internal interface:

LLMProvider  
 ├── OllamaProvider  
 ├── GeminiProvider  
 └── OpenAIProvider

Similarly:

StorageProvider  
 ├── LocalStorageProvider  
 ├── MinIOStorageProvider  
 └── R2StorageProvider

and:

EmbeddingProvider  
 ├── LocalEmbeddingProvider  
 └── CloudEmbeddingProvider  
---

# **1\. Overall design**

Your application will look like this:

                   ┌──────────────────┐  
                    │    Frontend      │  
                    │ React \+ TypeScript│  
                    └────────┬─────────┘  
                             │  
                             ▼  
                    ┌──────────────────┐  
                    │     FastAPI      │  
                    │    API Layer     │  
                    └────────┬─────────┘  
                             │  
                             ▼  
                 ┌───────────────────────┐  
                 │    Business Logic     │  
                 │                       │  
                 │ JD Analyzer            │  
                 │ Matcher                │  
                 │ Resume Optimizer       │  
                 │ Claim Validator        │  
                 │ Resume Generator       │  
                 └───────────┬───────────┘  
                             │  
              ┌──────────────┼──────────────┐  
              ▼              ▼              ▼  
        ┌──────────┐   ┌───────────┐  ┌──────────┐  
        │   LLM    │   │ Embeddings│  │ Storage  │  
        │ Provider │   │ Provider  │  │ Provider │  
        └────┬─────┘   └─────┬─────┘  └────┬─────┘  
             │               │              │  
       ┌─────┼─────┐         │        ┌─────┼─────┐  
       ▼     ▼     ▼         ▼        ▼     ▼     ▼  
    Ollama Gemini OpenAI   Local    Local  MinIO   R2

This is the architecture I would recommend for your project.

---

# **2\. LLM abstraction**

Create something conceptually like:

class LLMProvider:

    def generate(self, prompt):  
        pass

    def generate\_structured(self, prompt, schema):  
        pass

Then:

OllamaProvider  
GeminiProvider  
OpenAIProvider

all implement the same interface.

Your JD analyzer doesn't care which one is being used.

For example:

class JDAnalyzer:

    def \_\_init\_\_(self, llm: LLMProvider):  
        self.llm \= llm

    def analyze(self, job\_description):  
        return self.llm.generate\_structured(...)

So today:

JDAnalyzer  
     ↓  
Ollama

Later:

JDAnalyzer  
     ↓  
Gemini

or:

JDAnalyzer  
     ↓  
OpenAI

The `JDAnalyzer` doesn't change.

---

# **3\. Configuration controls the provider**

Instead of hardcoding:

if provider \== "ollama":  
    ...  
elif provider \== "gemini":  
    ...

everywhere, centralize configuration.

For development:

LLM\_PROVIDER=ollama

OLLAMA\_BASE\_URL=http://localhost:11434  
OLLAMA\_MODEL=\<local-model\>

For cloud:

LLM\_PROVIDER=gemini

GEMINI\_API\_KEY=\<api-key\>  
GEMINI\_MODEL=\<model\>

Or:

LLM\_PROVIDER=openai

OPENAI\_API\_KEY=\<api-key\>  
OPENAI\_MODEL=\<model\>

Your application starts with whichever provider is configured.

---

# **4\. Even better: fallback provider**

We can support:

LLM\_PROVIDER=ollama  
LLM\_FALLBACK\_PROVIDER=gemini

Then:

             Request  
                 │  
                 ▼  
              Ollama  
                 │  
          ┌──────┴──────┐  
          │             │  
       success        failure  
          │             │  
          ▼             ▼  
        result        Gemini

But there is an important rule:

### **Fallback should NOT hide business validation errors.**

For example:

Ollama unavailable  
       ↓  
Use Gemini

Good.

But:

Generated resume contains unsupported claim  
       ↓  
Use Gemini

❌ Not good.

That should go through your validation system.

---

# **5\. Storage abstraction**

The same principle applies to files.

Your candidate might upload:

resume.pdf  
resume.docx  
certificate.pdf  
portfolio.pdf

The application shouldn't care whether they're stored locally or in R2.

Define:

class StorageProvider:

    def upload(self, file):  
        pass

    def download(self, key):  
        pass

    def delete(self, key):  
        pass

    def get\_url(self, key):  
        pass

Then:

StorageProvider  
       │  
       ├── LocalStorage  
       ├── MinIO  
       └── R2

### **Development**

STORAGE\_PROVIDER=local

Files:

./storage/  
    resumes/  
    documents/  
    generated/

### **Production**

STORAGE\_PROVIDER=r2

Your business code remains unchanged.

R2 is particularly suitable later because it provides an S3-compatible API and currently has a free monthly allowance for storage and operations, with free egress.

---

# **6\. Embedding abstraction**

This one is slightly more important than it initially looks.

You'll use embeddings for things such as:

Candidate skill  
       ↓  
Embedding

Job requirement  
       ↓  
Embedding

        ↓

Semantic similarity

Define:

class EmbeddingProvider:

    def embed(self, text):  
        pass

    def embed\_batch(self, texts):  
        pass

Then:

EmbeddingProvider  
       │  
       ├── LocalEmbeddingProvider  
       └── CloudEmbeddingProvider

One important design decision:

### **Store embedding metadata.**

For example:

embedding\_model  
embedding\_dimension  
created\_at

Why?

Suppose you initially use:

Model A

and later switch to:

Model B

You generally need to regenerate the stored vectors because the vector space/model may differ.

So don't make embeddings an invisible database detail.

---

# **7\. Database**

For your MVP:

PostgreSQL  
\+  
pgvector

Run it locally using Docker.

For example:

localhost  
   │  
   ▼  
PostgreSQL  
   │  
   ├── Candidate data  
   ├── Career claims  
   ├── Jobs  
   ├── Matches  
   ├── Resume versions  
   └── Embeddings

Later:

Local PostgreSQL  
       ↓  
Managed PostgreSQL

Because we're using standard PostgreSQL \+ pgvector, your application architecture doesn't need to change significantly.

---

# **8\. Redis abstraction**

Same idea.

Development:

REDIS\_URL=redis://localhost:6379

Production:

REDIS\_URL=\<managed-redis-url\>

Your application only knows:

Redis

not:

Upstash  
Redis Cloud  
AWS ElastiCache  
---

# **9\. Your complete development stack**

For your **zero-cost development/testing environment**, I'd use:

Frontend  
React \+ TypeScript  
        │  
        ▼  
Backend  
FastAPI  
        │  
        ├──────── PostgreSQL \+ pgvector  
        │  
        ├──────── Redis  
        │  
        ├──────── Ollama  
        │  
        ├──────── Local filesystem  
        │  
        └──────── Local embeddings

Everything runs on your computer.

So there is essentially:

**No API bill.**

The trade-off is that your computer does the work.

---

# **10\. Production stack**

Later, the architecture can become:

React  
  │  
  ▼  
FastAPI  
  │  
  ├── Managed PostgreSQL \+ pgvector  
  │  
  ├── Managed Redis  
  │  
  ├── Cloud LLM  
  │  
  ├── Cloud embeddings  
  │  
  └── Cloudflare R2

The business logic remains the same.

Only configuration/provider implementations change.

---

# **11\. This gives us a very important property**

Imagine we build the application today using:

Ollama  
Local Storage  
Local PostgreSQL  
Local Redis  
Local Embeddings

Six months later you get 10,000 users.

You can move to:

OpenAI/Gemini  
R2  
Managed PostgreSQL  
Managed Redis  
Cloud embeddings

without rewriting:

JD Analyzer  
Matching Engine  
Gap Analyzer  
Resume Optimizer  
Claim Validator  
Change Tracker  
Resume Generator

That's exactly what we want.

---

# **12\. One more architectural rule**

I strongly recommend that we **do not let provider-specific code leak into business logic**.

Bad:

\# optimizer.py

if provider \== "gemini":  
    ...  
elif provider \== "ollama":  
    ...

Good:

\# optimizer.py

result \= self.llm.generate\_structured(  
    prompt,  
    schema  
)

The provider selection happens somewhere else.

This makes your project much easier to maintain.

---

# **13\. Final provider configuration**

I'd structure our configuration roughly like this:

\# Application  
APP\_ENV=development

\# Database  
DATABASE\_URL=postgresql://...

\# Redis  
REDIS\_URL=redis://localhost:6379

\# LLM  
LLM\_PROVIDER=ollama  
LLM\_FALLBACK\_PROVIDER=gemini

\# Ollama  
OLLAMA\_BASE\_URL=http://localhost:11434  
OLLAMA\_MODEL=...

\# Gemini  
GEMINI\_API\_KEY=  
GEMINI\_MODEL=...

\# OpenAI  
OPENAI\_API\_KEY=  
OPENAI\_MODEL=...

\# Embeddings  
EMBEDDING\_PROVIDER=local  
EMBEDDING\_MODEL=...

\# Storage  
STORAGE\_PROVIDER=local

\# R2 \- later  
R2\_ENDPOINT=  
R2\_ACCESS\_KEY=  
R2\_SECRET\_KEY=  
R2\_BUCKET=

And importantly:

### **API keys never go into Git.**

We'll use:

.env  
.env.example

with `.env` in `.gitignore`.

---

# **14\. The architecture decision we're making**

So I would officially lock this in:

| Component | Development | Production |
| ----- | ----- | ----- |
| Frontend | React \+ TS | React \+ TS |
| Backend | FastAPI | FastAPI |
| Database | PostgreSQL \+ pgvector | Managed PostgreSQL \+ pgvector |
| LLM | Ollama | Gemini/OpenAI/etc. |
| LLM fallback | Gemini | Another cloud provider |
| Embeddings | Local | Local/cloud |
| File storage | Local | Cloudflare R2 |
| Cache/queue | Local Redis | Managed Redis |
| Deployment | Docker/local | Docker/cloud |

And the key principle is:

> **Business logic is provider-independent; providers are configuration-dependent.**

This is the foundation that lets us build cheaply now without painting ourselves into a corner.

