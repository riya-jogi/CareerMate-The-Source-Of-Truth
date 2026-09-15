# step-18

Absolutely. **Step 17 is now finalized** and we can move to **Step 18 — Job Description Ingestion & Analysis**.

# **✅ Step 17 — FINALIZED**

The following decisions are now locked for V1:

| Area | Final Decision |
| ----- | ----- |
| Career Profile | ✅ Trusted career source of truth |
| Experiences | ✅ |
| Projects | ✅ |
| Education | ✅ |
| Certifications | ✅ |
| Skills | ✅ Normalized |
| Career Claims | ✅ Core feature |
| Evidence | ✅ Candidate-provided evidence |
| Claim ↔ Evidence | ✅ Many-to-many |
| Experience Type | ✅ Professional / Personal / Academic / Learning |
| Claim Status | ✅ Evidence-backed / Candidate-confirmed / Self-declared / Needs clarification / Unsupported |
| AI extraction | ✅ Proposal only |
| Candidate review | ✅ Mandatory |
| Candidate edit | ✅ |
| Candidate reject | ✅ |
| AI direct DB modification | ❌ |
| Independent verification | ❌ V1 |
| Employer verification | ❌ V1 |
| Resume as source of truth | ❌ |
| Career Profile as source of truth | ✅ |
| Generic soft-delete | ❌ |
| Full event sourcing | ❌ |
| Audit trail | ✅ |
| AI operation history | ✅ |

The final trust boundary is:

Resume  
   ↓  
AI Extraction  
   ↓  
Extraction Proposal  
   ↓  
Candidate Review  
   ├── Confirm  
   ├── Edit  
   └── Reject  
   ↓  
Career Profile  
   ↓  
Career Claims  
   ↓  
Evidence  
   ↓  
TRUSTED CAREER KNOWLEDGE BASE

This is now the foundation for everything that follows.

---

# **🚀 Step 18 — Job Description Ingestion & Analysis**

Now we turn our attention to the **other side of the matching problem**.

We have:

                Candidate Side  
                       │  
                       ▼  
              Career Knowledge Base

Now we need:

                   Job Side  
                       │  
                       ▼  
                  Job Description  
                       │  
                       ▼  
                Job Requirements

Eventually:

Career Knowledge Base  
          \+  
    Job Requirements  
          ↓  
     Matching Engine  
          ↓  
      Gap Analysis  
          ↓  
 Resume Optimization  
---

# **18.1 What exactly are we trying to solve?**

A raw JD is just unstructured text.

For example:

> We are looking for a Python Backend Developer with 3+ years of experience. Strong experience with Django and FastAPI is required. Knowledge of PostgreSQL and Docker is preferred. Experience with AWS is a plus.

A human can understand this.

Our system needs to convert it into structured information.

Something like:

{  
  "title": "Python Backend Developer",  
  "requirements": \[  
    {  
      "skill": "Python",  
      "type": "REQUIRED",  
      "minimum\_experience": 3  
    },  
    {  
      "skill": "Django",  
      "type": "REQUIRED"  
    },  
    {  
      "skill": "FastAPI",  
      "type": "REQUIRED"  
    },  
    {  
      "skill": "PostgreSQL",  
      "type": "PREFERRED"  
    },  
    {  
      "skill": "Docker",  
      "type": "PREFERRED"  
    },  
    {  
      "skill": "AWS",  
      "type": "CONTEXTUAL"  
    }  
  \]  
}

This structured representation becomes the input for our matching engine.

---

# **18.2 V1 Job input**

For V1, I recommend we **do not scrape job websites**.

The candidate will provide the JD directly.

Supported input:

### **Option 1 — Paste JD**

Paste your job description here...

### **Option 2 — Upload a JD file**

Potentially PDF/DOCX later.

But I recommend starting with:

> **Plain text JD input as the primary V1 path.**

Why?

Because it removes unnecessary complexity.

We don't need:

* website scraping  
* LinkedIn integrations  
* job portal APIs  
* browser automation  
* anti-bot handling

Our core product question is:

> Can we accurately analyze a JD and compare it with the candidate's trusted profile?

---

# **18.3 Job entity**

We need a `jobs` table.

Conceptually:

jobs  
\----  
id  
user\_id  
title  
company\_name  
location  
employment\_type  
source  
raw\_description  
created\_at  
updated\_at

Important:

`raw_description` should always be preserved.

Why?

Because the structured analysis can change, but the original JD should remain available.

---

# **18.4 Why preserve the original JD?**

Suppose the AI extracts:

Python → REQUIRED

Later we discover that was wrong.

We need to inspect the original text.

Therefore:

Raw JD  
  ↓  
AI Analysis  
  ↓  
Structured Requirements

The raw JD remains the source material.

This is similar to our resume architecture.

---

# **18.5 JD analysis pipeline**

Our finalized pipeline should be:

Candidate enters JD  
        ↓  
Validate input  
        ↓  
Store raw JD  
        ↓  
Clean / normalize text  
        ↓  
LLM analysis  
        ↓  
Structured JSON  
        ↓  
Pydantic validation  
        ↓  
Business validation  
        ↓  
Job Requirements  
        ↓  
Candidate review

I recommend **candidate review here as well**.

Why?

Because JD interpretation can be ambiguous.

For example:

> Experience with cloud technologies is preferred.

The AI may interpret:

AWS  
Azure  
GCP

But the JD didn't explicitly require all three.

We shouldn't silently create:

> AWS required.

Instead, we should preserve the distinction between:

* explicit requirement  
* inferred concept  
* contextual information

---

# **18.6 Requirement types**

We already finalized:

REQUIRED  
PREFERRED  
CONTEXTUAL

### **REQUIRED**

The employer explicitly requires it.

Example:

> “3+ years of Python experience.”

type \= REQUIRED

### **PREFERRED**

The employer says it is preferred/desirable.

Example:

> “Experience with Docker is preferred.”

type \= PREFERRED

### **CONTEXTUAL**

Useful information that isn't necessarily a qualification.

Example:

> “You will work with a team using AWS.”

That doesn't necessarily mean:

> AWS experience required.

Therefore:

type \= CONTEXTUAL  
---

# **18.7 Requirement categories**

I recommend that each requirement also have a category.

SKILL  
EXPERIENCE  
EDUCATION  
CERTIFICATION  
RESPONSIBILITY  
DOMAIN  
LOCATION  
LANGUAGE  
OTHER

Example:

> Python

category \= SKILL

> 3+ years backend development

category \= EXPERIENCE

> Bachelor's degree in Computer Science

category \= EDUCATION

> AWS Certified Developer

category \= CERTIFICATION

> Design REST APIs

category \= RESPONSIBILITY

This makes matching much more powerful later.

---

# **18.8 A requirement should contain more than just a skill**

Don't design:

job\_requirements  
\----------------  
skill\_name  
required

That is too simplistic.

Consider:

> “3+ years of professional Python backend development.”

We need to capture:

skill \= Python  
domain \= Backend Development  
minimum\_years \= 3  
experience\_type \= PROFESSIONAL  
requirement\_type \= REQUIRED

Therefore a conceptual requirement becomes:

JobRequirement  
│  
├── requirement\_text  
├── category  
├── requirement\_type  
├── normalized\_skill  
├── experience\_type  
├── minimum\_years  
├── maximum\_years  
├── context  
└── source/evidence  
---

# **18.9 Example: complex requirement**

JD:

> “Candidates should have at least 3 years of professional experience building REST APIs using Python and Django.”

Our system should understand:

Requirement  
────────────────────────────  
Text:  
3+ years of professional experience  
building REST APIs using Python and Django.

Category:  
EXPERIENCE

Type:  
REQUIRED

Skills:  
Python  
Django  
REST API

Minimum experience:  
3 years

Experience type:  
PROFESSIONAL

Context:  
Backend API development

Notice that this is **not three independent requirements**.

That's important.

The relationship between the concepts matters.

---

# **18.10 Explicit vs inferred information**

This is another important trust issue.

Suppose JD says:

> “Experience with Django REST Framework.”

The system can normalize:

Django REST Framework  
→ DRF

That's safe.

But:

> Django REST Framework → Django \+ Python \+ REST \+ PostgreSQL

is not necessarily an explicit requirement.

We can use normalized/semantic relationships during matching, but we shouldn't rewrite the original requirement as though the employer explicitly stated those things.

So we should distinguish:

Explicit:  
Django REST Framework

from:

Normalized:  
DRF

Related concepts:  
Django  
REST APIs  
Python

This distinction will become extremely important for accurate matching.

---

# **18.11 Requirement normalization**

We need normalization because employers write the same thing differently.

Examples:

Python  
Python 3  
Python programming  
Python development

Potential canonical concept:

Python

Similarly:

Django REST Framework  
DRF  
Django REST

could map to:

Django REST Framework

But normalization must be conservative.

We should never assume:

Django  
\=  
Django REST Framework

or:

AWS  
\=  
Azure

Semantic similarity helps retrieve candidates, but rules decide whether a requirement is actually satisfied.

---

# **18.12 LLM responsibility**

The LLM is responsible for understanding language.

It can:

* identify requirements  
* classify required/preferred/contextual  
* identify skills  
* identify experience requirements  
* identify education requirements  
* identify certifications  
* identify responsibilities  
* identify domain/context  
* normalize terminology  
* identify relationships between requirements  
* detect ambiguity

But the LLM does **not** make the final candidate qualification decision.

---

# **18.13 Example of what NOT to do**

JD:

> “Experience with Python is preferred.”

LLM shouldn't directly produce:

candidate\_qualifies \= true

That's not its responsibility.

It produces:

{  
    "skill": "Python",  
    "requirement\_type": "PREFERRED"  
}

Then the matching engine looks at:

Candidate Career Claims  
\+  
Python experience  
\+  
Evidence  
\+  
Experience type  
\+  
Dates

and decides the match.

---

# **18.14 Pydantic schema**

Conceptually:

class JobRequirement(BaseModel):  
    requirement\_text: str  
    category: RequirementCategory  
    requirement\_type: RequirementType

    normalized\_skill: str | None \= None

    minimum\_years: float | None \= None  
    maximum\_years: float | None \= None

    experience\_type: ExperienceType | None \= None

    context: str | None \= None

And:

class JobAnalysisResult(BaseModel):  
    title: str | None  
    company\_name: str | None  
    summary: str | None  
    requirements: list\[JobRequirement\]

Again:

> Schema validity ≠ factual correctness.

Business validation comes afterward.

---

# **18.15 Job requirement evidence**

We should preserve where a requirement came from in the JD.

For example:

Requirement:  
3+ years Python backend experience

Source:

JD text:  
"Candidates must have at least 3 years..."

This helps explain the result to the candidate.

Later the UI can say:

> **Why is Python marked as required?**

And show:

> “Candidates must have at least 3 years of Python backend experience.”

This transparency is one of our differentiators.

---

# **18.16 Job embeddings**

After requirements are structured, we can create embeddings.

Job Requirement  
       ↓  
Embedding  
       ↓  
pgvector

We already finalized:

Model:  
BAAI/bge-small-en-v1.5

Dimensions:  
384

Similarity:  
Cosine

Database:  
PostgreSQL \+ pgvector

So:

job\_requirement\_embeddings  
\--------------------------  
id  
job\_requirement\_id  
embedding  
model  
dimension  
created\_at

Likewise our candidate claims can have embeddings.

---

# **18.17 Why embeddings are not enough**

Suppose:

JD:

> 5+ years professional Python experience.

Candidate:

> Python — 2 years professional experience.

Embedding similarity:

VERY HIGH

But qualification:

NOT QUALIFIED FOR EXPERIENCE THRESHOLD

Therefore:

Embedding  
    ↓  
"These things are semantically related."

Rules:

"Does the candidate actually satisfy the requirement?"

This preserves our principle:

> **Embeddings retrieve; rules decide.**

---

# **18.18 Job analysis status**

Just like resume extraction:

PENDING  
PROCESSING  
COMPLETED  
FAILED

Errors:

JD\_EMPTY  
JD\_TOO\_LONG  
LLM\_UNAVAILABLE  
LLM\_TIMEOUT  
LLM\_INVALID\_OUTPUT  
LLM\_SCHEMA\_ERROR  
JD\_ANALYSIS\_FAILED

We should also preserve AI operation history.

ai\_operations  
operation\_type \= JD\_ANALYSIS  
---

# **18.19 API design**

I recommend:

### **Create Job**

POST /api/v1/jobs

Input:

{  
  "title": "Python Backend Developer",  
  "company\_name": "ABC Technologies",  
  "location": "Ahmedabad",  
  "raw\_description": "..."  
}

### **List Jobs**

GET /api/v1/jobs

### **Get Job**

GET /api/v1/jobs/{id}

### **Analyze JD**

POST /api/v1/jobs/{id}/analyze

### **Get requirements**

GET /api/v1/jobs/{id}/requirements

Later:

PUT /api/v1/jobs/{id}  
DELETE /api/v1/jobs/{id}  
---

# **18.20 Frontend workflow**

I envision:

Dashboard  
   ↓  
"Analyze a Job"  
   ↓  
┌─────────────────────────────┐  
│ Job Title                   │  
│ \[Python Backend Developer\]  │  
│                             │  
│ Company                     │  
│ \[ABC Technologies\]         │  
│                             │  
│ Job Description             │  
│ ┌─────────────────────────┐ │  
│ │ Paste JD here...        │ │  
│ │                         │ │  
│ └─────────────────────────┘ │  
│                             │  
│        \[Analyze Job\]        │  
└─────────────────────────────┘

Then:

Analyzing Job...

Then:

Job Analysis  
────────────────────────────

Python                 REQUIRED  
Django                 REQUIRED  
FastAPI                REQUIRED  
PostgreSQL             PREFERRED  
Docker                 PREFERRED  
AWS                    CONTEXTUAL  
---

# **18.21 Candidate review**

We can show:

### **Required**

✓ Python  
✓ Django  
✓ FastAPI

### **Preferred**

○ PostgreSQL  
○ Docker

### **Contextual**

i AWS

And allow:

\[View source\]  
\[Edit classification\]

This is especially useful when AI is uncertain.

---

# **18.22 Important UX principle**

Don't tell the candidate:

> **“This job requires AWS.”**

if the JD only says:

> “Our infrastructure runs on AWS.”

Instead:

> **“AWS was identified as contextual information, not an explicit requirement.”**

That is much more trustworthy.

---

# **18.23 Job analysis architecture**

Final architecture:

React  
  │  
  ▼  
Job API  
  │  
  ▼  
Job Service  
  │  
  ├── JD Text Cleaner  
  │  
  ├── JD Analysis Service  
  │       │  
  │       ▼  
  │   LLMProvider  
  │       │  
  │       ▼  
  │   Structured JSON  
  │       │  
  │       ▼  
  │   Pydantic  
  │       │  
  │       ▼  
  │   Business Validator  
  │  
  ├── Requirement Service  
  │  
  └── Embedding Service  
           │  
           ▼  
       pgvector  
---

# **18.24 Suggested backend structure**

Add:

app/  
├── services/  
│   ├── job\_service.py  
│   ├── jd\_analysis\_service.py  
│   └── requirement\_service.py  
│  
├── ai/  
│   ├── prompts/  
│   │   └── jd\_analysis.py  
│   │  
│   └── schemas/  
│       └── jd\_analysis.py  
│  
├── validators/  
│   └── job\_requirement\_validator.py  
│  
└── api/  
    └── v1/  
        └── jobs.py

Later we can separate matching:

matching\_service.py

but **don't mix matching into JD analysis**.

That's an important boundary.

---

# **18.25 JD Analysis vs Matching**

These are two completely different operations.

### **JD Analysis**

Answers:

> **“What does this employer appear to be asking for?”**

### **Matching**

Answers:

> **“How well does this candidate satisfy those requirements?”**

Therefore:

JD  
 ↓  
JD Analysis  
 ↓  
Requirements

and separately:

Requirements  
\+  
Career Knowledge Base  
 ↓  
Matching

Do not combine them.

---

# **18.26 What about Job Alignment Score?**

Not yet.

We already decided that the final score/weights are still something we need to design carefully.

Step 18 should produce **clean requirements**.

Step 19 can then focus on:

> **Candidate ↔ Job Matching Engine**

where we determine:

* exact matching  
* normalized matching  
* semantic matching  
* experience matching  
* evidence  
* experience type  
* requirement weights  
* partial matches  
* gaps  
* overall Job Alignment Score

That is where the actual scoring formula should be finalized.

---

# **18.27 Step 18 V1 boundaries**

### **Included**

✅ Paste JD  
✅ Store raw JD  
✅ Job metadata  
✅ LLM analysis  
✅ Structured extraction  
✅ Pydantic validation  
✅ Required/preferred/contextual classification  
✅ Requirement categories  
✅ Skill normalization  
✅ Experience requirements  
✅ Education requirements  
✅ Certification requirements  
✅ Responsibility extraction  
✅ Requirement evidence/source text  
✅ Candidate review  
✅ Embeddings  
✅ AI audit trail

### **Not included**

❌ Job website scraping  
❌ LinkedIn integration  
❌ Job portal integrations  
❌ Automatic job discovery  
❌ Auto-apply  
❌ Candidate matching inside the JD parser  
❌ ATS score guarantee  
❌ External employer verification

---

# **18.28 One important decision I recommend**

I strongly recommend that we **do not let the LLM produce a single "JD score."**

For example:

JD Score: 87%

is misleading at this stage.

Instead, the LLM produces structured facts:

Python → REQUIRED  
Django → REQUIRED  
FastAPI → REQUIRED  
Docker → PREFERRED  
AWS → CONTEXTUAL

Then our deterministic matching engine calculates the candidate's alignment later.

This gives us:

> **Explainable matching instead of an arbitrary AI score.**

---

# **18.29 Final Step 18 pipeline**

                JOB DESCRIPTION  
                       │  
                       ▼  
                Input Validation  
                       │  
                       ▼  
                  Store Raw JD  
                       │  
                       ▼  
                Text Normalization  
                       │  
                       ▼  
                   LLM Analysis  
                       │  
                       ▼  
              Structured JSON Output  
                       │  
                       ▼  
               Pydantic Validation  
                       │  
                       ▼  
              Business Validation  
                       │  
                       ▼  
               Job Requirements  
                       │  
                       ▼  
               Candidate Review  
                       │  
                       ▼  
              Normalize Requirements  
                       │  
                       ▼  
                   Embeddings  
                       │  
                       ▼  
                READY FOR MATCHING

## **Step 18 key principle**

> **The LLM interprets the employer's language. It does not decide whether the candidate is qualified.**

And the architecture remains:

> **LLM understands → Pydantic structures → rules validate → candidate reviews → matching engine decides.**

---

### **Where we go next**

Once we finalize Step 18, **Step 19 will be the Matching Engine**, which is arguably the technical heart of the project:

Career Claims  
      \+  
Job Requirements  
      ↓  
Exact Matching  
      \+  
Normalized Matching  
      \+  
Semantic Matching  
      \+  
Experience Validation  
      \+  
Evidence Validation  
      \+  
Requirement Importance  
      ↓  
STRONG MATCH  
PARTIAL MATCH  
GAP  
UNKNOWN  
      ↓  
Job Alignment Score  
      ↓  
Gap Analysis

**Step 18 is now ready for finalization; the next step is Step 19 — Candidate–Job Matching Engine & Gap Analysis.**

# Step-19

Great. **Step 18 is finalized.** Now we move into one of the most important technical components of the entire project.

# **Step 19 — Candidate–Job Matching Engine & Gap Analysis**

This is where our two previously finalized systems finally meet:

                   CAREER SIDE

                        │

                        ▼

              Trusted Career Profile

                        │

                  Career Claims

                        │

                    Evidence

                        │

                        │

                        ▼

                  MATCHING ENGINE

                        ▲

                        │

                        │

                 Job Requirements

                        │

                        ▼

                    JOB SIDE

The goal is **not** simply:

> “Does the candidate have the keyword?”

The real question is:

> **“Does the candidate have sufficient, relevant, evidence-backed experience to satisfy this specific job requirement?”**

---

# **19.1 What the matching engine must solve**

Consider this JD:

> Python Backend Developer with 3+ years of professional Python experience. Strong Django and FastAPI experience required. Docker and PostgreSQL preferred.

Candidate:

Python

Professional

2.5 years

Django

Professional

2 years

FastAPI

Professional

1.5 years

Docker

Personal project

PostgreSQL

Professional

2 years

A simple keyword matcher might say:

Python ✓

Django ✓

FastAPI ✓

Docker ✓

PostgreSQL ✓

95% match

That would be **wrong**.

Our system should understand:

Python      → PARTIAL

Django      → STRONG/PARTIAL depending requirement

FastAPI     → STRONG/PARTIAL

Docker      → PARTIAL because personal

PostgreSQL  → STRONG/PARTIAL

And explain *why*.

---

# **19.2 Matching architecture**

Our finalized architecture should be:

Job Requirement

       │

       ├── Exact Matching

       │

       ├── Normalized Matching

       │

       └── Semantic Retrieval

                 │

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

       Requirement Evaluation

                 │

                 ▼

          Match Decision

The critical principle remains:

> **Embeddings retrieve. Rules decide.**

---

# **19.3 Three levels of matching**

We should use three complementary techniques.

## **Level 1 — Exact matching**

Example:

JD: Python

Candidate: Python

→ Exact match.

Fast and highly reliable.

---

## **Level 2 — Normalized matching**

Example:

JD: Django REST Framework

Candidate: DRF

Our normalization layer recognizes:

DRF

Django REST

Django REST Framework

as the same canonical concept where appropriate.

→ Normalized match.

---

## **Level 3 — Semantic matching**

Example:

JD:

"RESTful API development"

Candidate:

"Developed backend APIs using FastAPI."

There may not be an exact string match, but semantically they're related.

Embedding retrieval can identify the candidate claim.

→ Semantic candidate.

But this does **not** automatically mean qualified.

Rules still evaluate it.

---

# **19.4 Why semantic similarity alone is dangerous**

Suppose:

JD:

> “5+ years of professional Python experience.”

Candidate:

> “Completed a Python course and built a personal project.”

Semantic similarity:

HIGH

Qualification:

NO

Therefore:

Embedding similarity

       ≠

Qualification

This is one of the most important rules in our system.

---

# **19.5 Match types**

We already agreed on four:

STRONG\_MATCH

PARTIAL\_MATCH

GAP

UNKNOWN

Let's define them precisely.

### **STRONG\_MATCH**

Candidate has sufficiently relevant experience and evidence to satisfy the requirement.

Example:

JD:

2+ years professional Python

Candidate:

3 years professional Python

Evidence-backed

→ STRONG\_MATCH

---

### **PARTIAL\_MATCH**

Candidate has relevant capability, but doesn't fully satisfy the requirement.

Example:

JD:

3+ years professional Python

Candidate:

2 years professional Python

→ PARTIAL\_MATCH

Another example:

JD:

3 years professional Kubernetes

Candidate:

1 year personal Kubernetes project

→ PARTIAL\_MATCH or GAP depending on requirement strictness.

---

### **GAP**

There is insufficient relevant candidate information.

Example:

JD:

Professional Kubernetes experience required

Candidate:

No Kubernetes claim

→ GAP

---

### **UNKNOWN**

The candidate may have the capability, but our trusted data isn't sufficient to determine it.

Example:

JD:

Experience with Terraform

Candidate:

Resume says "cloud technologies"

We shouldn't invent:

> Terraform experience.

→ UNKNOWN

This is better than falsely saying GAP.

---

# **19.6 Match result needs an explanation**

Don't just store:

match\_type \= PARTIAL\_MATCH

We should store an explanation.

Example:

> “Candidate has 2 years of professional Python experience against the required 3 years.”

Or:

> “Candidate has Kubernetes experience in a personal project, but the job requires professional Kubernetes experience.”

This is essential for the UI.

---

# **19.7 Match detail model**

Our existing conceptual model:

candidate\_job\_matches

\---------------------

id

career\_profile\_id

job\_id

overall\_score

created\_at

updated\_at

And:

match\_details

\-------------

id

candidate\_job\_match\_id

job\_requirement\_id

match\_type

score

explanation

matched\_claim\_id

We should potentially allow multiple matched claims:

matched\_claim\_ids

but relationally it is cleaner to introduce a relationship table later if needed.

For V1, one primary matched claim plus explanation can work, but **multiple claims may contribute to one requirement**, especially experience requirements.

I recommend:

match\_detail\_claims

\-------------------

match\_detail\_id

claim\_id

with a composite primary key.

This makes the model robust without much complexity.

---

# **19.8 Requirement evaluation**

Let's take:

> “3+ years professional Python backend development.”

The engine evaluates:

### **Skill**

Python

### **Context**

Backend development

### **Experience type**

Professional

### **Minimum duration**

3 years

### **Candidate**

Python

Professional

2.5 years

Backend

Evidence-backed

Then:

Skill → MATCH

Context → MATCH

Experience type → MATCH

Evidence → MATCH

Years → PARTIAL

Overall:

PARTIAL\_MATCH

That's much more meaningful than keyword matching.

---

# **19.9 Experience duration calculation**

We must calculate experience from dates.

Example:

2023-01 → 2025-06

Python determines the duration.

We should **not trust**:

"2.5 years"

written by the candidate or generated by an LLM.

The calculation comes from:

start\_date

end\_date

and business rules.

---

# **19.10 Overlapping experience**

This is important.

Suppose:

Company A:

Jan 2023 → Dec 2024

Company B:

Jan 2024 → Dec 2025

You cannot simply add:

2 years \+ 2 years \= 4 years

because 2024 overlaps.

The engine needs to merge overlapping professional periods when calculating total experience for a skill.

Conceptually:

Company A  ███████████████

Company B        ███████████████

                  ↓

Combined     ███████████████████

This prevents inflated experience.

---

# **19.11 Skill-specific experience**

We also shouldn't assume:

> Candidate worked at a company for 3 years → 3 years of Python.

Instead, claims must establish the relationship.

Example:

Experience:

ABC Technologies

2023 → 2026

Claims:

Python

FastAPI

PostgreSQL

We can calculate relevant duration based on the supported claims and their associated experience.

If Python only appears in a project from 2025:

Python professional experience

≠

Entire employment duration

This is critical.

---

# **19.12 Experience type affects matching**

Example JD:

> “3 years professional AWS experience.”

Candidate:

AWS

PERSONAL

2 years

Result:

NOT STRONG\_MATCH

Candidate:

AWS

PROFESSIONAL

3.5 years

Result:

STRONG\_MATCH

Candidate:

AWS

LEARNING

1 year

Result:

GAP / PARTIAL

The exact result depends on requirement strictness, but it can never become a full professional match automatically.

---

# **19.13 Evidence affects confidence**

Suppose:

Candidate claim:

Python

Status:

SELF\_DECLARED

versus:

Candidate claim:

Python backend development

Status:

EVIDENCE\_BACKED

The second should produce a stronger match.

But we must avoid saying:

> “Self-declared means false.”

It simply means:

> “Our evidence confidence is lower.”

---

# **19.14 Claim status and matching**

Suggested behavior:

| Claim status | Matching treatment |
| ----- | ----- |
| Candidate-confirmed | Strongest candidate-owned signal |
| Evidence-backed | Strong |
| Self-declared | Lower confidence |
| Needs clarification | Do not use as confirmed qualification |
| Unsupported | Do not use |

Again:

> Candidate-confirmed does not mean independently verified.

---

# **19.15 Requirement importance**

We need weighting.

A required requirement should matter more than a preferred one.

For example:

Required:

Python

Django

FastAPI

Preferred:

Docker

PostgreSQL

Missing Python should hurt the alignment more than missing Docker.

Conceptually:

REQUIRED     → high weight

PREFERRED    → medium weight

CONTEXTUAL   → low/no qualification weight

But I recommend we **do not finalize exact numeric weights yet** until we design the full scoring model.

---

# **19.16 Responsibilities**

Not everything is a skill.

JD:

> “Design and implement REST APIs.”

Candidate:

> “Developed REST APIs using FastAPI.”

This may be semantically related.

The system can produce:

RESPONSIBILITY\_MATCH

but shouldn't pretend:

> Candidate has explicitly claimed "designed APIs."

because "developed" and "designed" are not necessarily equivalent in responsibility strength.

This connects directly to our earlier **claim-strength hierarchy**.

---

# **19.17 Claim strength**

We previously established the risk spectrum:

Exposure

Learning

Used

Implemented

Developed

Designed

Led

Architected

Expert

The matching engine must consider this.

Example:

JD:

> “Architect scalable distributed systems.”

Candidate:

> “Used Python to develop APIs.”

Semantic similarity may exist.

But:

Developed

≠

Architected

Therefore:

NOT STRONG\_MATCH

This protects the candidate from AI exaggeration.

---

# **19.18 Match scoring**

We need two separate concepts.

### **Requirement-level score**

How well does the candidate satisfy one requirement?

Example:

Python:

92

### **Overall Job Alignment Score**

How well does the candidate align with the entire job?

Example:

Job Alignment Score

78/100

But the score must be **our deterministic calculation**, not an LLM-generated number.

---

# **19.19 Proposed scoring dimensions**

The final model can evaluate:

Skill relevance

Experience type

Experience duration

Context relevance

Evidence status

Requirement importance

Semantic similarity

Exact/normalized match

Claim strength

Conceptually:

Requirement Score

        │

        ├── Skill Match

        ├── Context Match

        ├── Experience Match

        ├── Evidence

        └── Claim Strength

Then:

Overall Job Alignment

        │

        ├── Required requirements

        ├── Preferred requirements

        └── Contextual information

---

# **19.20 Don't let score hide critical gaps**

This is extremely important.

Suppose:

Required Python       ✓

Required Django       ✓

Required FastAPI      ✓

Required 5yr exp      ✗

Preferred Docker      ✓

Preferred PostgreSQL  ✓

A weighted average might still produce:

82%

That could mislead the candidate.

Therefore the UI should always display:

### **Job Alignment**

82/100

### **Critical gaps**

⚠ Required experience threshold not met

The candidate should never interpret 82 as:

> “I definitely qualify.”

---

# **19.21 Gap analysis**

Gap analysis should be generated from match results.

Example:

Job Requirements

────────────────────────────

✓ Python

✓ Django

⚠ FastAPI — 1.5 years vs 2 years required

✕ Kubernetes — no relevant experience

✓ PostgreSQL

Then summarize:

### **Strong matches**

Python

Django

PostgreSQL

### **Partial matches**

FastAPI

### **Gaps**

Kubernetes

### **Unknown**

Terraform

---

# **19.22 Gap categories**

We should distinguish:

SKILL\_GAP

EXPERIENCE\_GAP

DURATION\_GAP

CONTEXT\_GAP

EVIDENCE\_GAP

EDUCATION\_GAP

CERTIFICATION\_GAP

Example:

> Candidate has Python but only 1 year; JD requires 3 years.

That's:

DURATION\_GAP

Candidate has Kubernetes personal project but JD requires professional:

EXPERIENCE\_TYPE\_GAP

Candidate may know Terraform but hasn't documented it:

EVIDENCE\_GAP / UNKNOWN

This gives much better career guidance.

---

# **19.23 What should the system tell the candidate?**

Not:

> “You don't have Kubernetes.”

Instead:

> **“Kubernetes is required, but your Career Profile currently does not contain a professional Kubernetes claim supported by evidence.”**

That's much more accurate.

Maybe the candidate actually has the experience but forgot to add it.

This is where our system provides real value.

---

# **19.24 Candidate can resolve unknowns**

Example:

Terraform

Status: UNKNOWN

We found related cloud/infrastructure experience,

but couldn't determine whether you have Terraform experience.

\[Add Career Claim\]

\[Mark as not applicable\]

Candidate can then update the Career Profile.

This creates a useful loop:

JD Analysis

   ↓

Matching

   ↓

Unknown

   ↓

Candidate adds information

   ↓

Matching again

---

# **19.25 Matching API**

We already planned:

POST /api/v1/jobs/{id}/match

This starts matching.

Then:

GET /api/v1/jobs/{id}/match

returns the latest result.

Response concept:

{

  "data": {

    "overall\_score": 78,

    "summary": "...",

    "strong\_matches": \[\],

    "partial\_matches": \[\],

    "gaps": \[\],

    "unknowns": \[\],

    "critical\_gaps": \[\]

  }

}

---

# **19.26 Matching should be reproducible**

This is very important.

Given the same:

Career Profile version

\+

Job Requirements version

\+

Matching algorithm version

we should get the same result.

Therefore we should store:

matching\_algorithm\_version

For example:

matching-v1

If we later change scoring:

matching-v2

we can distinguish results.

This is excellent for debugging and future experimentation.

---

# **19.27 Match history**

We don't necessarily need to preserve every matching calculation forever in V1.

But when a candidate reruns matching after changing their profile, we should know which data produced the result.

At minimum:

candidate\_job\_matches

\---------------------

career\_profile\_id

job\_id

algorithm\_version

overall\_score

created\_at

updated\_at

And details.

---

# **19.28 Embedding generation**

For each:

Career Claim

we can generate:

embedding vector(384)

And for:

Job Requirement

also:

embedding vector(384)

Then pgvector retrieves relevant claims.

Example:

JD requirement:

"REST API development"

       ↓ embedding

Candidate claims

       ↓

Python backend API development

FastAPI REST APIs

Django REST Framework

Top relevant claims are retrieved.

Then deterministic rules evaluate them.

---

# **19.29 Retrieval threshold**

We should not assume every retrieved claim is relevant.

Example:

similarity \= 0.89

looks high, but similarity scores depend on model/domain.

So we should eventually calibrate a threshold using our test dataset.

For V1:

> Use embeddings for candidate retrieval, then let the rule engine determine whether the retrieved claim is sufficiently relevant.

Don't hard-code a magical universal threshold without evaluation.

---

# **19.30 Matching engine architecture**

This is the architecture I recommend:

                   Job Requirement

                          │

                          ▼

                 Requirement Analyzer

                          │

            ┌─────────────┼─────────────┐

            ▼             ▼             ▼

         Exact       Normalized      Semantic

        Matching       Matching       Retrieval

            │             │             │

            └─────────────┼─────────────┘

                          ▼

                    Candidate Claims

                          │

                          ▼

                 Evidence Evaluation

                          │

                          ▼

              Experience Type Check

                          │

                          ▼

                Duration Calculation

                          │

                          ▼

                  Claim Strength

                          │

                          ▼

                  Rule Evaluation

                          │

                          ▼

                Match Classification

                          │

            ┌─────────────┼─────────────┐

            ▼             ▼             ▼

         STRONG        PARTIAL        GAP

                          │

                          └── UNKNOWN

---

# **19.31 Backend structure**

Add:

app/

├── matching/

│   ├── engine.py

│   ├── exact\_matcher.py

│   ├── normalized\_matcher.py

│   ├── semantic\_matcher.py

│   ├── experience\_evaluator.py

│   ├── evidence\_evaluator.py

│   ├── claim\_strength\_evaluator.py

│   ├── requirement\_evaluator.py

│   └── score\_calculator.py

│

├── services/

│   ├── matching\_service.py

│   └── gap\_analysis\_service.py

│

└── api/

    └── v1/

        └── matching.py

The important thing is that these are **pure business components** wherever possible.

---

# **19.32 Matching flow in code architecture**

API

 ↓

MatchingService

 ↓

Load Job Requirements

 ↓

Load Candidate Claims

 ↓

Semantic Retrieval

 ↓

RequirementEvaluator

 ↓

ExperienceEvaluator

 ↓

EvidenceEvaluator

 ↓

MatchClassifier

 ↓

ScoreCalculator

 ↓

GapAnalysisService

 ↓

Persist result

---

# **19.33 What the LLM does here**

The LLM can still assist with interpretation.

For example:

"Experience building scalable RESTful backend services"

could be interpreted as:

Domain:

Backend

Responsibility:

API/service development

Concepts:

REST APIs

Scalability

But the LLM should **not** return:

candidate\_score \= 92

The deterministic engine calculates the result.

---

# **19.34 Matching example end-to-end**

JD:

> Python Backend Developer  
> 3+ years professional Python experience  
> Django required  
> FastAPI preferred  
> Docker preferred

Candidate:

Python

Professional

2.5 years

Evidence-backed

Django

Professional

3 years

Evidence-backed

FastAPI

Professional

1 year

Evidence-backed

Docker

Personal project

6 months

Candidate-confirmed

Result:

Python

→ PARTIAL

Reason: 2.5 vs 3 years

Django

→ STRONG\_MATCH

FastAPI

→ PARTIAL/STRONG depending requirement

Docker

→ PARTIAL

Reason: personal rather than professional

Overall:

Job Alignment Score

≈ strong but not complete

And:

Critical gap:

Python professional experience threshold

This is exactly the type of result we want.

---

# **19.35 What makes this different from an ATS?**

Traditional ATS systems often emphasize:

keyword found?

Our system emphasizes:

keyword

\+

meaning

\+

context

\+

experience type

\+

duration

\+

evidence

\+

claim strength

So the candidate isn't told:

> “You need to add Kubernetes.”

They're told:

> “Kubernetes is required. Your profile currently shows Kubernetes only in a personal project, while the JD asks for professional experience.”

That's much more actionable and truthful.

---

# **19.36 V1 boundaries**

### **Included**

✅ Exact matching  
✅ Normalized matching  
✅ Semantic retrieval  
✅ Evidence-aware matching  
✅ Experience-aware matching  
✅ Experience type  
✅ Duration calculation  
✅ Claim strength  
✅ Required/preferred weighting  
✅ Strong/Partial/Gap/Unknown  
✅ Explainable results  
✅ Gap analysis  
✅ Critical gap detection  
✅ Job Alignment Score  
✅ Algorithm versioning  
✅ Match audit data

### **Not included**

❌ Machine-learning-trained ranking model  
❌ User outcome prediction  
❌ Hiring probability prediction  
❌ “Guaranteed ATS score”  
❌ Automatic application  
❌ Employer-side ranking  
❌ External verification  
❌ Custom fine-tuned matching model

---

# **19.37 Final architecture principle**

We now have a very clean AI architecture:

               LLM

                 │

        Understand language

                 │

                 ▼

       Structured representation

                 │

                 ▼

            Embeddings

                 │

           Retrieve candidates

                 │

                 ▼

        Deterministic Rules

                 │

      ┌──────────┼──────────┐

      ▼          ▼          ▼

    Dates      Evidence    Context

      │          │          │

      └──────────┼──────────┘

                 ▼

          Match Decision

                 │

                 ▼

          Gap Analysis

### **The golden rule for Step 19:**

> **Semantic similarity tells us what might be relevant. Evidence, experience, dates, context, and deterministic rules tell us whether it actually qualifies.**

---

## **Step 19 — Decisions to finalize**

Before we lock this step, there are **four things I deliberately don't want to guess**:

1. **Exact Job Alignment Score formula and weights**  
2. **Exact semantic similarity thresholds**  
3. **How much a preferred requirement can influence the final score**  
4. **Exact rules for converting requirement-level scores into the overall score**

Those should be finalized using examples/test cases rather than arbitrary numbers.

Once those are locked, Step 19 becomes completely implementable.

**After that, Step 20 should be Resume Optimization \+ Change Tracking \+ Truth Validation**—where the matching results are finally used to customize the candidate's resume without allowing the AI to fabricate anything.

Yes. Let's finalize the four remaining decisions properly rather than leaving them ambiguous.

I recommend we make these **V1 defaults**, while keeping the thresholds and weights configurable so we can tune them after testing real resumes/JDs.

# **Step 19 — Final Matching & Scoring Decisions**

## **1\. Final Job Alignment Score formula**

We should **not** calculate one giant average across every requirement.

Instead, divide requirements into:

* **Required**  
* **Preferred**  
* **Contextual**

Contextual requirements do **not** contribute to qualification score.

### **Final weighting**

| Requirement type | Contribution |
| ----- | ----- |
| Required | **70%** |
| Preferred | **30%** |
| Contextual | **0%** |

If a JD contains no preferred requirements, the required requirements are normalized to **100%**.

### **Requirement-level score**

| Match | Score |
| ----- | ----- |
| STRONG\_MATCH | **100** |
| PARTIAL\_MATCH | **50** |
| GAP | **0** |
| UNKNOWN | **Not scored** |

I intentionally don't give `UNKNOWN` a 50 or 0\.

Why?

Because:

> **Unknown ≠ Gap.**

If the candidate hasn't provided enough information, we shouldn't tell them they definitely lack the skill.

---

## **2\. Exact overall formula**

Let:

Required Score \=  
weighted average of known required requirement scores

Preferred Score \=  
weighted average of known preferred requirement scores

Then:

Job Alignment Score \=  
(Required Score × 0.70)  
\+  
(Preferred Score × 0.30)

If there are no preferred requirements:

Job Alignment Score \= Required Score

### **Example**

Suppose:

Required:  
Python       STRONG     100  
Django       STRONG     100  
FastAPI      PARTIAL     50  
Docker       GAP          0

Preferred:  
PostgreSQL   STRONG     100  
AWS          PARTIAL     50

Required:

(100 \+ 100 \+ 50 \+ 0\) / 4  
\= 62.5

Preferred:

(100 \+ 50\) / 2  
\= 75

Overall:

62.5 × 0.70  
\+  
75 × 0.30

\= 66.25

So:

> **Job Alignment Score \= 66.3 / 100**

But we don't stop there.

The UI must also say:

> ⚠️ 1 required requirement is currently a gap.

This prevents the score from hiding important deficiencies.

---

# **3\. Unknown handling**

This is important enough to finalize separately.

Suppose the JD says:

> Terraform experience required.

Candidate profile says:

> Cloud infrastructure experience.

We cannot determine whether they know Terraform.

Therefore:

Terraform → UNKNOWN

It should **not** become:

GAP

and it should not artificially increase the score.

### **But there's a problem**

If we simply exclude UNKNOWN requirements, a candidate could appear to have an excellent score despite having many unknowns.

So we'll introduce another metric:

## **Profile Coverage**

Profile Coverage \=  
known requirements / total requirements

Example:

10 requirements  
7 evaluated  
3 unknown

Coverage \= 70%

The UI can therefore say:

Job Alignment        84/100  
Profile Coverage      70%

This is much more honest than pretending the 84 is fully reliable.

---

# **4\. Required UNKNOWN rule**

There's one more safeguard.

If a **critical required requirement** is UNKNOWN, the system should flag the result:

status \= INCOMPLETE

Example:

Job Alignment: 84/100  
Profile Coverage: 70%

⚠ Analysis incomplete

Required requirement:  
Terraform experience

Status:  
UNKNOWN

The candidate can then add information to their Career Profile and rerun matching.

---

# **5\. Semantic similarity thresholds**

This one needs careful handling.

I don't want us to pretend that:

> cosine similarity ≥ 0.80 always means a match.

That is not universally true.

The exact threshold depends on:

* embedding model  
* text length  
* domain  
* wording  
* candidate claim structure  
* JD language

We have already finalized:

BAAI/bge-small-en-v1.5  
384 dimensions  
cosine similarity

So for V1, we'll use **configurable initial thresholds**.

### **Initial V1 thresholds**

≥ 0.80  
→ HIGH semantic relevance

0.68 – 0.79  
→ MODERATE semantic relevance

\< 0.68  
→ LOW semantic relevance

But these do **not directly determine STRONG/PARTIAL/GAP**.

They determine retrieval/relevance.

That's an important distinction.

---

# **6\. Semantic matching pipeline**

For example:

JD:  
RESTful API development

Candidate claims:

A: Developed REST APIs using FastAPI  
similarity \= 0.87

B: Built backend services using Django  
similarity \= 0.76

C: Completed Python course  
similarity \= 0.54

Retrieval:

A → HIGH  
B → MODERATE  
C → LOW

Then business rules evaluate them.

So:

0.87 similarity

doesn't automatically mean:

STRONG\_MATCH

because we still need:

experience type  
duration  
evidence  
claim strength  
context  
---

# **7\. Exact/normalized matching takes precedence**

Our matching priority will be:

1\. Exact match  
2\. Normalized match  
3\. Semantic retrieval  
4\. Business-rule evaluation

For example:

JD:  
Django REST Framework

Candidate:  
DRF

If our canonical skill mapping says:

DRF → Django REST Framework

that's a normalized match.

We don't need semantic similarity to prove something we already know.

---

# **8\. Semantic thresholds are configurable**

We'll put them in configuration rather than hard-code them throughout the application.

For example:

SEMANTIC\_HIGH\_THRESHOLD=0.80  
SEMANTIC\_MEDIUM\_THRESHOLD=0.68

Later, after testing 100+ real-world JDs/resumes, we can change:

0.80 → 0.82

without rewriting the matching engine.

This is particularly important because we shouldn't consider these numbers scientifically final until we've evaluated them on our own data.

---

# **9\. Preferred requirement influence**

We now officially set:

Required \= 70%  
Preferred \= 30%  
Contextual \= 0%

Therefore preferred requirements **can improve the candidate's score**, but they can never compensate equally for missing required qualifications.

Example:

Required:  
Python      GAP  
Django      GAP

Preferred:  
Docker      STRONG  
AWS         STRONG  
PostgreSQL  STRONG

The candidate should **not** receive a high score merely because they have the preferred skills.

Required qualifications remain dominant.

---

# **10\. Critical required gaps**

We should add a special concept:

> **Critical Gap**

A critical gap is a required requirement where the candidate clearly does not satisfy an essential condition.

Examples:

JD:  
3+ years professional Python

Candidate:  
1 year professional Python

→ Critical duration gap.

Or:

JD:  
Professional Kubernetes experience required

Candidate:  
No professional Kubernetes experience

→ Critical experience gap.

The exact score may still be mathematically calculated, but the UI must prominently surface the critical gap.

---

# **11\. Should one critical gap automatically make the candidate score 0?**

**No.**

This is an important decision.

If a job has:

10 requirements

and the candidate misses:

1 required requirement

they shouldn't automatically receive:

0/100

The score should represent **overall alignment**, while critical gaps separately communicate important blockers.

Therefore:

Score ≠ Qualification decision  
---

# **12\. Final result object**

Our matching engine should ultimately produce something like:

{  
  "overall\_score": 72.5,  
  "profile\_coverage": 90.0,  
  "analysis\_status": "COMPLETE\_WITH\_GAPS",

  "required": {  
    "score": 65.0,  
    "strong": 4,  
    "partial": 1,  
    "gaps": 1,  
    "unknown": 0  
  },

  "preferred": {  
    "score": 90.0,  
    "strong": 3,  
    "partial": 1,  
    "gaps": 0,  
    "unknown": 0  
  },

  "critical\_gaps": \[  
    "Required professional experience threshold not met"  
  \]  
}

This gives the frontend much more useful information than:

{  
    "score": 72.5  
}  
---

# **13\. Final classification rules**

Let's make the requirement-level classification deterministic.

### **STRONG\_MATCH**

Candidate satisfies the important conditions:

Skill/context relevant  
\+  
Correct experience type  
\+  
Sufficient duration where required  
\+  
Acceptable evidence  
\+  
No significant claim-strength mismatch

### **PARTIAL\_MATCH**

Relevant capability exists, but one or more conditions aren't fully satisfied.

Examples:

2 years vs 3 years

or:

Personal experience vs professional requirement

or:

Developed APIs vs JD asks for architecture

### **GAP**

Candidate profile provides sufficient information to determine that the requirement is not met.

Example:

JD:  
Professional Kubernetes

Candidate:  
No Kubernetes experience

### **UNKNOWN**

There isn't enough trusted information to determine whether the candidate satisfies it.

Example:

JD:  
Terraform

Candidate:  
Infrastructure experience  
---

# **14\. Final matching hierarchy**

This is now our definitive decision pipeline:

                 JOB REQUIREMENT  
                         │  
                         ▼  
                ┌─────────────────┐  
                │ Exact Matching  │  
                └────────┬────────┘  
                         │  
                    no exact match  
                         │  
                         ▼  
                ┌─────────────────┐  
                │ Normalization   │  
                └────────┬────────┘  
                         │  
                    no clear match  
                         │  
                         ▼  
                ┌─────────────────┐  
                │ Vector Search   │  
                │ BGE 384         │  
                └────────┬────────┘  
                         │  
                         ▼  
                  Candidate Claims  
                         │  
                         ▼  
              ┌─────────────────────┐  
              │ Context Evaluation  │  
              ├─────────────────────┤  
              │ Experience Type     │  
              │ Duration            │  
              │ Evidence            │  
              │ Claim Strength      │  
              └──────────┬──────────┘  
                         │  
                         ▼  
                 Business Rules  
                         │  
                         ▼  
          ┌──────────────┼──────────────┐  
          ▼              ▼              ▼  
       STRONG         PARTIAL          GAP  
                         │  
                         └────── UNKNOWN  
---

# **15\. Final Job Alignment calculation**

The complete V1 formula is therefore:

Required Score  
    \=  
average score of known required requirements

Preferred Score  
    \=  
average score of known preferred requirements

Job Alignment Score  
    \=  
(Required Score × 0.70)  
\+  
(Preferred Score × 0.30)

where:

STRONG  \= 100  
PARTIAL \= 50  
GAP     \= 0  
UNKNOWN \= excluded

and:

Profile Coverage  
\=  
evaluated requirements  
/  
total requirements  
× 100

Contextual requirements:

weight \= 0

Critical gaps are surfaced separately and **never hidden by the overall score**.

---

# **16\. One more protection: score confidence**

I recommend we expose:

> **Profile Coverage**

rather than creating a fake "AI confidence score."

For example:

### **Case A**

Alignment: 82  
Coverage: 100%

High-quality comparison.

### **Case B**

Alignment: 82  
Coverage: 55%

The candidate should understand:

> “The 82 score is based on only 55% of the requirements because several requirements couldn't be evaluated.”

That's far more transparent.

---

# **17\. Final Step 19 decisions**

So we can now officially lock all four previously open items:

| Decision | Final V1 |
| ----- | ----- |
| Required weight | **70%** |
| Preferred weight | **30%** |
| Contextual weight | **0%** |
| STRONG score | **100** |
| PARTIAL score | **50** |
| GAP score | **0** |
| UNKNOWN | **Excluded from score** |
| Unknown visibility | **Profile Coverage** |
| Critical unknown | **Analysis marked incomplete** |
| Initial semantic high threshold | **0.80** |
| Initial semantic medium threshold | **0.68** |
| Similarity decides qualification? | **No** |
| Exact match precedence | **Yes** |
| Normalized match precedence | **Yes** |
| Embeddings | **Retrieval only** |
| Dates | **Deterministic** |
| Experience calculation | **Deterministic** |
| Evidence evaluation | **Deterministic rules** |
| Claim-strength evaluation | **Rules \+ AI interpretation where necessary** |
| Critical gaps | **Always surfaced separately** |
| Score \= qualification guarantee? | **No** |
| ATS guarantee | **No** |
| Algorithm version | **Yes (`matching-v1`)** |
| Thresholds configurable | **Yes** |

### **One terminology decision**

I want us to consistently call this:

> **Job Alignment Score**

—not **ATS Score**.

Because our system is measuring how well the candidate's **trusted career information aligns with a specific job**, not claiming to reproduce some universal ATS algorithm.

---

## **✅ Step 19 is now fully finalized**

Our core product logic is now:

              CANDIDATE  
                   │  
          Career Knowledge Base  
                   │  
                   │  
                   ▼  
             MATCHING ENGINE  
                   ▲  
                   │  
                   │  
             Job Requirements  
                   │  
                  JOB

And:

> **LLM understands. Embeddings retrieve. Rules evaluate. Evidence supports. Dates calculate. Candidate decides.**

This gives us a solid, explainable foundation rather than a black-box "AI score."

### **Next: Step 20**

We can now move to the part where this intelligence becomes useful to the candidate:

**Step 20 — AI Resume Optimization \+ Change Tracking \+ Truth Validation \+ Candidate Approval**

That step will answer:

> **Given the candidate's trusted Career Profile and this specific Job Description, how do we create the best possible job-specific resume without inventing or exaggerating anything?**

# Step-20

Absolutely. **Step 20 is the point where our product starts delivering its main value**: taking the candidate's trusted career information and a specific job's requirements, then producing a tailored resume **without allowing AI to fabricate anything**.

# **Step 20 — AI Resume Optimization, Change Tracking & Truth Validation**

Our complete pipeline is now:

                   CAREER KNOWLEDGE BASE  
                             │  
                             │  
                    ┌────────▼────────┐  
                    │  Job Requirements│  
                    └────────┬────────┘  
                             │  
                             ▼  
                      MATCHING ENGINE  
                             │  
                             ▼  
                        GAP ANALYSIS  
                             │  
                             ▼  
                   RESUME OPTIMIZATION  
                             │  
                             ▼  
                    PROPOSED CHANGES  
                             │  
                             ▼  
                    TRUTH VALIDATION  
                             │  
                   ┌─────────┼─────────┐  
                   ▼         ▼         ▼  
                 PASS     WARNING     BLOCK  
                             │  
                             ▼  
                     CANDIDATE REVIEW  
                             │  
                    ┌────────┼────────┐  
                    ▼        ▼        ▼  
                 APPROVE    EDIT     REJECT  
                             │  
                             ▼  
                      RESUME VERSION  
                             │  
                             ▼  
                       FINAL RESUME

The most important rule remains:

> **AI can optimize presentation, but it cannot upgrade the candidate's reality.**

---

# **20.1 What exactly is Resume Optimization?**

We are **not** asking the LLM:

> "Create the best resume for this job."

That is too dangerous.

Instead, we give it controlled inputs:

Career Profile  
\+  
Approved Career Claims  
\+  
Evidence  
\+  
Job Requirements  
\+  
Match Results  
\+  
Existing Resume

and ask:

> **"Identify and propose truthful changes that make the candidate's existing information more relevant to this specific job."**

This difference is fundamental.

---

# **20.2 What optimization is allowed?**

The AI can:

### **Reorder**

If Python and FastAPI are highly relevant:

Before:  
Skills:  
HTML  
CSS  
Python  
FastAPI  
PostgreSQL

Potential proposal:

Skills:  
Python  
FastAPI  
PostgreSQL  
HTML  
CSS  
---

### **Rewrite wording**

Original:

> Worked on APIs using Python.

Proposal:

> Developed backend APIs using Python.

If supported by the underlying claim/evidence, this can be safe.

---

### **Prioritize relevant experience**

If the JD emphasizes:

Python  
FastAPI  
PostgreSQL

the system can bring relevant experience/projects higher in the resume.

---

### **Condense irrelevant information**

For example, if the candidate has:

> Basic HTML/CSS knowledge

and the target is a Python backend role, it can be moved lower or condensed.

---

### **Normalize terminology**

Candidate:

> Django Rest Framework

JD:

> Django REST Framework

The system can use the standardized terminology.

---

# **20.3 What optimization is NOT allowed to do**

The optimizer cannot:

❌ Add a skill the candidate doesn't have  
❌ Increase experience duration  
❌ Change employment dates  
❌ Invent responsibilities  
❌ Invent achievements  
❌ Invent metrics  
❌ Invent certifications  
❌ Invent projects  
❌ Convert learning into professional experience  
❌ Convert personal projects into professional experience  
❌ Upgrade "used" → "architected" without evidence  
❌ Claim leadership without evidence  
❌ Claim expertise without evidence

Example:

Candidate:

> Developed REST APIs using FastAPI.

JD:

> Architect scalable distributed systems.

The optimizer must **not** write:

> Architected scalable distributed systems using FastAPI.

Instead it might retain:

> Developed REST APIs using FastAPI.

and perhaps identify:

> ⚠️ Architecture experience is not supported by the Career Profile.

---

# **20.4 Optimization is proposal generation**

The LLM should never directly produce the final trusted resume.

Instead:

LLM  
 ↓  
Optimization Proposal  
 ↓  
Pydantic  
 ↓  
Truth Validator  
 ↓  
Candidate Review  
 ↓  
Approved Changes  
 ↓  
Resume Version

This is the same architecture we've used throughout the project.

---

# **20.5 Optimization proposal structure**

We should have a structured response.

For example:

{  
  "changes": \[  
    {  
      "section": "SUMMARY",  
      "change\_type": "REWRITE",  
      "original": "...",  
      "proposed": "...",  
      "reason": "Better highlights Python backend experience relevant to the job.",  
      "supporting\_claim\_ids": \["claim-123"\],  
      "risk\_level": "LOW"  
    }  
  \]  
}

This is far better than asking the LLM to return a complete resume immediately.

---

# **20.6 Change types**

Let's define the V1 change types:

ADD  
REMOVE  
REWRITE  
REORDER  
CONDENSE  
NORMALIZE

### **ADD**

Example:

> Add FastAPI to the skills section.

But only if it already exists in the trusted Career Profile.

---

### **REMOVE**

Example:

> Remove irrelevant technology from the prominent skills list.

This does **not** delete it from Career Profile.

Very important.

It only removes it from this resume version.

---

### **REWRITE**

Change wording while preserving factual meaning.

---

### **REORDER**

Change the position of:

* skills  
* experience  
* projects  
* bullets  
* sections

---

### **CONDENSE**

Shorten low-relevance content.

---

### **NORMALIZE**

Change terminology to a canonical form.

---

# **20.7 Every change needs a reason**

This is one of our differentiators.

Don't show:

> "AI changed this."

Show:

> **"Moved FastAPI higher because it is a required skill in the target job and is supported by your professional experience."**

For example:

CHANGE \#12

Before:  
Worked on APIs using Python.

After:  
Developed backend APIs using Python.

Why:  
Improves alignment with the job's backend API  
requirement while preserving the original claim.

Evidence:  
ABC Technologies experience

This makes the system explainable.

---

# **20.8 Every factual change needs supporting claims**

Suppose the optimizer proposes:

> Developed REST APIs using FastAPI.

The validator asks:

Which Career Claim supports this?

If no claim supports it:

BLOCK

If there is a claim:

"Developed APIs using FastAPI."

then continue validation.

This creates a powerful rule:

> **Every factual statement in an optimized resume must trace back to trusted Career Knowledge Base information.**

---

# **20.9 Claim traceability**

We should be able to trace:

Final Resume Sentence  
        ↓  
Resume Change  
        ↓  
Career Claim  
        ↓  
Evidence  
        ↓  
Original Source

For example:

"Developed REST APIs using FastAPI"  
             ↓  
Change \#18  
             ↓  
Claim \#42  
             ↓  
Experience \#5  
             ↓  
Resume Evidence

This is a major differentiator.

---

# **20.10 Truth Validation**

After optimization:

Generated Resume  
       ↓  
Extract factual claims  
       ↓  
Compare against Career Knowledge Base  
       ↓  
Validate

The validator checks:

### **Skills**

Is the skill supported?

### **Dates**

Are dates unchanged?

### **Experience duration**

Was experience inflated?

### **Experience type**

Did personal experience become professional?

### **Responsibilities**

Did wording become stronger than the source?

### **Certifications**

Is the certification real in the profile?

### **Projects**

Does the project exist?

### **Metrics**

Are metrics supported?

### **Education**

Are degree/institution details accurate?

---

# **20.11 Validation statuses**

We finalized:

PASS  
WARNING  
BLOCK  
NEEDS\_CLARIFICATION

### **PASS**

No meaningful factual concern.

---

### **WARNING**

Potential issue requiring candidate review.

Example:

Original:

> Worked on API development.

Generated:

> Developed API services.

Probably okay, but the validator may flag a wording-strength change.

---

### **BLOCK**

Clearly unsupported.

Example:

Candidate has:

> Python — 2 years

Generated:

> 5 years of Python experience.

→ BLOCK.

---

### **NEEDS\_CLARIFICATION**

The system cannot determine whether the statement is supported.

Example:

> Managed cloud infrastructure.

Career Profile only says:

> Worked with AWS.

→ NEEDS\_CLARIFICATION.

---

# **20.12 Claim strengthening detection**

This is one of the most important validators.

Suppose source claim:

> Used Python.

Generated:

> Developed backend applications using Python.

Potentially acceptable depending on evidence.

But:

> Architected highly scalable distributed systems using Python.

is much stronger.

Our validator should detect this.

We already have the risk spectrum:

Exposure  
   ↓  
Learning  
   ↓  
Used  
   ↓  
Implemented  
   ↓  
Developed  
   ↓  
Designed  
   ↓  
Led  
   ↓  
Architected  
   ↓  
Expert

This is a **risk model**, not an absolute linguistic hierarchy.

If generated wording moves substantially upward without supporting evidence:

BLOCK / NEEDS\_CLARIFICATION  
---

# **20.13 Metrics require special treatment**

This is a very common AI hallucination problem.

Candidate:

> Improved API performance.

AI generates:

> Improved API performance by 40%.

❌ BLOCK.

Unless we have evidence for the 40%.

Likewise:

> Worked on a team.

AI must not generate:

> Led a team of 10 developers.

❌ BLOCK.

---

# **20.14 Dates are deterministic**

LLM:

Jan 2024 – Present

Our database:

start\_date \= 2024-01-01  
end\_date \= NULL

The optimizer cannot alter this.

The validator compares generated dates with trusted dates.

Trusted:  
2024 → Present

Generated:  
2023 → Present

Result:  
BLOCK  
---

# **20.15 Experience duration**

Same rule.

Trusted:

Python professional experience \= 2.5 years

Generated:

> 3+ years of Python experience.

→ BLOCK.

The LLM doesn't get to calculate or modify the candidate's experience duration.

---

# **20.16 Experience type protection**

Candidate:

Kubernetes  
PERSONAL

Generated:

> Professional Kubernetes experience.

→ BLOCK.

This is exactly the type of issue our product is designed to prevent.

---

# **20.17 Resume change database**

We already have:

resume\_changes  
\----------------  
id  
resume\_version\_id  
change\_type  
section  
original\_content  
proposed\_content  
reason  
risk\_level  
created\_at

We should extend it with traceability:

primary\_claim\_id

And potentially a relationship table:

resume\_change\_claims  
\--------------------  
change\_id  
claim\_id

This supports multiple claims.

---

# **20.18 Candidate approval**

Every AI-proposed change should have an approval state.

We already have `approvals`.

Conceptually:

approval  
\--------  
id  
resume\_change\_id  
decision  
candidate\_comment  
created\_at

Decision:

APPROVED  
REJECTED  
EDITED  
---

# **20.19 Candidate review UI**

This should feel like a **Git diff for resumes**.

Example:

────────────────────────────────────────────  
SUMMARY  
────────────────────────────────────────────

BEFORE

Backend developer with experience in Python,  
Django and FastAPI.

AI PROPOSAL

Backend developer with professional experience  
building Python APIs using Django and FastAPI.

WHY?

Highlights technologies relevant to this job.

SUPPORTED BY

✓ Python claim  
✓ Django claim  
✓ FastAPI claim

        \[Approve\] \[Edit\] \[Reject\]  
────────────────────────────────────────────

This is much better than silently replacing the resume.

---

# **20.20 Change risk**

I recommend three V1 risk levels:

LOW  
MEDIUM  
HIGH

### **LOW**

Formatting/reordering/normalization.

### **MEDIUM**

Wording changes that could slightly alter interpretation.

### **HIGH**

Changes involving:

* responsibilities  
* leadership  
* architecture  
* metrics  
* years  
* certifications  
* experience type

High-risk changes should receive stronger validation.

---

# **20.21 Optimization strategy**

We should optimize in stages.

### **Stage 1 — Selection**

Determine:

> Which existing candidate information is relevant?

### **Stage 2 — Prioritization**

Determine:

> What should appear more prominently?

### **Stage 3 — Wording**

Determine:

> How can it be expressed clearly and truthfully?

### **Stage 4 — Validation**

Determine:

> Did we accidentally strengthen or invent anything?

This is safer than generating a complete resume in one LLM call.

---

# **20.22 Optimization prompt architecture**

Our prompt should contain:

SYSTEM RULES  
\+  
JOB REQUIREMENTS  
\+  
MATCH RESULTS  
\+  
CAREER CLAIMS  
\+  
EVIDENCE  
\+  
CURRENT RESUME  
\+  
OUTPUT SCHEMA

The system instruction should explicitly say:

> You may only use factual information contained in the supplied Career Claims and approved Career Profile. Do not invent, infer, strengthen, or fabricate candidate facts.

And:

> When a requested job requirement is not supported, do not add it to the resume. Instead, identify it as a gap.

---

# **20.23 Don't ask the LLM to "beat the ATS"**

Avoid prompts such as:

> "Make this resume score 95% on ATS."

That encourages keyword stuffing and potentially fabricated content.

Instead:

> "Optimize the candidate's resume for relevance to this job while preserving factual accuracy and the candidate's approved experience."

This aligns the AI with our product philosophy.

---

# **20.24 Keyword optimization**

Keyword optimization is still useful.

Example JD:

> Django REST Framework

Candidate:

> DRF

We can write:

> Django REST Framework (DRF)

if the candidate's claim supports it.

This improves terminology alignment without inventing anything.

But:

JD:

> Kubernetes

Candidate:

> No Kubernetes claim.

We cannot add:

> Kubernetes

just to improve keyword matching.

---

# **20.25 Gap-aware optimization**

Suppose the JD requires:

Python ✓  
Django ✓  
FastAPI ✓  
Kubernetes ✕

The resume optimizer should:

Highlight:  
Python  
Django  
FastAPI

but should **not**:

Add:  
Kubernetes

Instead:

> Kubernetes remains a gap and has not been added to the resume.

This protects the candidate.

---

# **20.26 What if the candidate actually has the missing skill?**

The candidate can return to Career Profile:

Add Career Claim  
       ↓  
Provide context  
       ↓  
Provide evidence  
       ↓  
Candidate confirms  
       ↓  
Matching reruns  
       ↓  
Resume optimization reruns

This creates a powerful feedback loop.

---

# **20.27 Resume versioning**

We already finalized:

> Resume versions are immutable.

So:

Resume  
│  
├── Version 1 — Original  
│  
├── Version 2 — Python Backend Job  
│  
├── Version 3 — AI Engineer Job  
│  
└── Version 4 — FastAPI Developer Job

Each version contains a snapshot.

---

# **20.28 Resume version**

Conceptually:

resume\_versions  
\---------------  
id  
resume\_id  
version\_number  
content\_snapshot  
source\_version\_id  
job\_id  
created\_at

The `content_snapshot` should be immutable.

If the candidate edits Version 2:

> Don't modify Version 2\.

Create:

Version 3

This preserves history.

---

# **20.29 Why versioning matters**

Candidate may want to return to:

> “The resume I used for Company X.”

We should be able to reproduce it.

Also:

Job  
 ↓  
Matching result  
 ↓  
Optimization  
 ↓  
Changes  
 ↓  
Approved resume version

can be linked together.

---

# **20.30 Final resume generation**

Only after:

Optimization  
 ↓  
Validation  
 ↓  
Candidate approval

do we generate the final document.

Possible outputs:

* PDF  
* DOCX

The exact rendering implementation can be finalized separately, but conceptually:

Approved Resume JSON  
        ↓  
Resume Renderer  
        ↓  
DOCX / PDF

The renderer should **not contain AI logic**.

---

# **20.31 API design**

We already planned:

POST /api/v1/jobs/{id}/optimize

Returns an optimization proposal.

Then:

GET /api/v1/jobs/{id}/optimization

Gets the current proposal.

Changes:

GET /api/v1/optimizations/{id}/changes

Approval:

POST /api/v1/changes/{id}/approve  
POST /api/v1/changes/{id}/reject  
POST /api/v1/changes/{id}/edit

Final resume:

POST /api/v1/jobs/{id}/resume/generate  
GET  /api/v1/jobs/{id}/resume  
---

# **20.32 Important API behavior**

`POST /optimize` should **not automatically create a final resume version**.

It creates:

Optimization Proposal

Then:

Candidate Review

Then:

Approved Changes

Then:

Resume Version

This separation protects our trust model.

---

# **20.33 Complete Step 20 architecture**

                CAREER KNOWLEDGE BASE  
                         │  
                         │  
                  JOB REQUIREMENTS  
                         │  
                         ▼  
                  MATCHING RESULTS  
                         │  
                         ▼  
                 OPTIMIZATION SERVICE  
                         │  
                         ▼  
                     LLMProvider  
                         │  
                         ▼  
                Structured Proposal  
                         │  
                         ▼  
                   Pydantic Schema  
                         │  
                         ▼  
                 Truth Validator  
                         │  
            ┌────────────┼────────────┐  
            ▼            ▼            ▼  
          PASS        WARNING        BLOCK  
            │            │  
            └──────┬─────┘  
                   ▼  
             Candidate Review  
                   │  
          ┌────────┼─────────┐  
          ▼        ▼         ▼  
       Approve    Edit     Reject  
          │        │  
          └────┬───┘  
               ▼  
        Approved Changes  
               │  
               ▼  
       Immutable Resume Version  
               │  
               ▼  
          PDF / DOCX  
---

# **20.34 Backend structure**

I'd add:

app/  
├── optimization/  
│   ├── optimizer.py  
│   ├── change\_detector.py  
│   ├── claim\_mapper.py  
│   └── risk\_evaluator.py  
│  
├── validation/  
│   ├── resume\_validator.py  
│   ├── factual\_validator.py  
│   ├── date\_validator.py  
│   ├── experience\_validator.py  
│   ├── claim\_strength\_validator.py  
│   └── metric\_validator.py  
│  
├── services/  
│   ├── optimization\_service.py  
│   ├── approval\_service.py  
│   └── resume\_version\_service.py  
│  
└── api/  
    └── v1/  
        ├── optimization.py  
        └── resume\_generation.py  
---

# **20.35 Final V1 data flow**

The full product flow is now becoming very clear:

                   USER  
                     │  
                     ▼  
                  RESUME  
                     │  
                     ▼  
               EXTRACTION  
                     │  
                     ▼  
             CANDIDATE REVIEW  
                     │  
                     ▼  
          CAREER KNOWLEDGE BASE  
                     │  
                     │  
                     │  
                  JOB JD  
                     │  
                     ▼  
               JD ANALYSIS  
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
            CHANGE PROPOSALS  
                     │  
                     ▼  
             TRUTH VALIDATION  
                     │  
                     ▼  
             CANDIDATE APPROVAL  
                     │  
                     ▼  
            IMMUTABLE VERSION  
                     │  
                     ▼  
                 FINAL RESUME  
---

# **20.36 Final Step 20 decisions**

| Area | V1 Decision |
| ----- | ----- |
| AI resume optimization | ✅ |
| Optimization from trusted claims | ✅ |
| Job-specific optimization | ✅ |
| AI-generated proposal | ✅ |
| Structured output | ✅ |
| Pydantic validation | ✅ |
| Claim traceability | ✅ |
| Evidence traceability | ✅ |
| Change tracking | ✅ |
| Change explanation | ✅ |
| Candidate approval | **Mandatory** |
| Candidate edit | ✅ |
| Candidate reject | ✅ |
| Truth validation | **Mandatory** |
| Claim-strength validation | ✅ |
| Date validation | ✅ |
| Experience validation | ✅ |
| Metric validation | ✅ |
| Experience-type validation | ✅ |
| Unsupported claim blocking | ✅ |
| Risk levels | Low / Medium / High |
| Resume versioning | ✅ |
| Immutable versions | ✅ |
| PDF generation | ✅ |
| DOCX generation | ✅ |
| Keyword optimization | ✅, only when truthful |
| Keyword stuffing | ❌ |
| Fabrication | ❌ |
| Experience inflation | ❌ |
| AI direct DB write | ❌ |
| "ATS score guarantee" | ❌ |

---

## **The final principle for Step 20**

> **The optimizer can change how the candidate's truth is presented, but never what the candidate's truth is.**

And our complete safety chain becomes:

TRUSTED CLAIM  
     ↓  
EVIDENCE  
     ↓  
JOB RELEVANCE  
     ↓  
AI PROPOSAL  
     ↓  
FACTUAL VALIDATION  
     ↓  
CANDIDATE APPROVAL  
     ↓  
FINAL RESUME

This is what makes the product fundamentally different from simply asking ChatGPT to "tailor my resume."

### **Step 20 is ready to be finalized.**

After this, the next logical step is **Step 21 — Resume Generation, Templates, ATS-safe formatting, PDF/DOCX rendering, and final Resume Quality Validation**, where we'll design exactly how the approved content becomes the actual downloadable resume.

# step-21

Absolutely. **Step 20 is finalized.** Now we move to **Step 21 — Resume Generation, Templates, ATS-Safe Formatting & Final Quality Validation**.

This step is about turning our **approved, validated resume content** into an actual professional resume file.

The important distinction is:

> **Step 20 decides what the resume should say. Step 21 decides how that approved content is rendered and delivered.**

---

# **Step 21 — Resume Generation & Final Resume Quality**

## **21.1 Where we are now**

Our complete pipeline is:

Resume Upload  
      ↓  
Resume Extraction  
      ↓  
Career Profile  
      ↓  
Career Claims \+ Evidence  
      ↓  
Job Description  
      ↓  
JD Analysis  
      ↓  
Job Requirements  
      ↓  
Matching Engine  
      ↓  
Gap Analysis  
      ↓  
Resume Optimization  
      ↓  
Change Proposals  
      ↓  
Truth Validation  
      ↓  
Candidate Approval  
      ↓  
        ★ STEP 21 ★  
   Resume Generation  
      ↓  
ATS-Safe Rendering  
      ↓  
Final Quality Validation  
      ↓  
PDF / DOCX  
---

# **21.2 First important decision: separate content from presentation**

We should **never store the final resume as only HTML/PDF/DOCX**.

Instead, create a structured **Resume Document Model**.

For example:

ResumeDocument  
│  
├── Header  
│   ├── Name  
│   ├── Headline  
│   ├── Email  
│   ├── Phone  
│   ├── Location  
│   └── Links  
│  
├── Summary  
│  
├── Skills  
│  
├── Experience  
│   ├── Experience 1  
│   │   ├── Company  
│   │   ├── Role  
│   │   ├── Dates  
│   │   └── Bullets  
│   │  
│   └── Experience 2  
│  
├── Projects  
│  
├── Education  
│  
└── Certifications

This becomes the **canonical resume representation**.

Then:

ResumeDocument  
      │  
      ├── DOCX Renderer  
      │  
      └── PDF Renderer

This is important because later we can add:

ResumeDocument  
      │  
      ├── DOCX  
      ├── PDF  
      └── HTML Preview

without changing the optimization engine.

---

# **21.3 Resume content schema**

I recommend a structured model such as:

class ResumeDocument(BaseModel):  
    header: ResumeHeader  
    summary: str | None  
    skills: list\[ResumeSkillGroup\]  
    experiences: list\[ResumeExperience\]  
    projects: list\[ResumeProject\]  
    education: list\[ResumeEducation\]  
    certifications: list\[ResumeCertification\]

For example:

class ResumeExperience(BaseModel):  
    experience\_id: UUID  
    company\_name: str  
    job\_title: str  
    location: str | None  
    start\_date: date  
    end\_date: date | None  
    bullets: list\[ResumeBullet\]

And importantly:

class ResumeBullet(BaseModel):  
    text: str  
    claim\_ids: list\[UUID\]

That gives every factual bullet traceability.

---

# **21.4 Why claim IDs inside resume content?**

Suppose the final resume says:

> Developed REST APIs using FastAPI and Python.

Internally we know:

Resume Bullet  
     ↓  
Claim \#102  
     ↓  
Experience \#14  
     ↓  
Evidence \#27

The user doesn't need to see UUIDs, but our backend can.

This allows us to validate the final resume after rendering.

---

# **21.5 Resume templates**

We should **not create dozens of templates in V1**.

Start with approximately:

### **Template 1 — Professional ATS**

Simple single-column resume.

### **Template 2 — Modern ATS**

Still single-column, slightly stronger visual hierarchy.

### **Template 3 — Compact ATS**

For candidates with more experience/content.

The actual number can remain configurable, but **3 templates are enough for V1**.

---

# **21.6 What makes a template ATS-safe?**

We should prioritize:

### **Good**

* standard section headings  
* normal text  
* single-column layout  
* readable fonts  
* consistent headings  
* normal bullet points  
* conventional date formats  
* clear hierarchy  
* selectable text  
* standard document structure

### **Avoid**

* tables for primary layout  
* text boxes  
* floating elements  
* excessive graphics  
* decorative icons containing important information  
* images containing text  
* skill bars  
* star ratings  
* progress meters  
* multi-column layouts for V1  
* headers/footers containing critical information

This is important:

> **We should not claim that any resume is universally "ATS-proof."**

Different ATS systems parse documents differently.

We should instead say:

> **ATS-friendly / ATS-aware formatting.**

---

# **21.7 Single-column should be our default**

For V1:

┌───────────────────────────────────┐  
│ Name                              │  
│ Backend Developer                 │  
│ email | phone | location | links │  
├───────────────────────────────────┤  
│ SUMMARY                           │  
├───────────────────────────────────┤  
│ SKILLS                            │  
├───────────────────────────────────┤  
│ EXPERIENCE                        │  
├───────────────────────────────────┤  
│ PROJECTS                          │  
├───────────────────────────────────┤  
│ EDUCATION                         │  
├───────────────────────────────────┤  
│ CERTIFICATIONS                    │  
└───────────────────────────────────┘

This is easier for parsers and easier for us to validate.

---

# **21.8 Standard section names**

Use predictable headings:

SUMMARY  
SKILLS  
EXPERIENCE  
PROJECTS  
EDUCATION  
CERTIFICATIONS

Avoid:

> “My Professional Journey”

when we want maximum machine readability.

The AI can optimize content, but the renderer should maintain standardized section semantics.

---

# **21.9 Ordering sections**

Default order for a technical candidate:

1\. Header  
2\. Professional Summary  
3\. Skills  
4\. Professional Experience  
5\. Projects  
6\. Education  
7\. Certifications

But we can allow the optimization engine to change ordering based on the candidate/job.

For example, a fresher may benefit from:

Header  
Summary  
Skills  
Projects  
Education  
Certifications

This decision should be part of the **resume structure**, not hard-coded into the PDF renderer.

---

# **21.10 Dates**

Use deterministic date formatting.

For example:

Jan 2024 – Present  
Jun 2022 – Dec 2023

Never allow the LLM to format dates inconsistently.

The renderer receives:

start\_date  
end\_date  
is\_current

and formats them.

---

# **21.11 Contact information**

The header can contain:

Name  
Professional headline  
Email  
Phone  
Location  
LinkedIn  
GitHub  
Portfolio

But only information existing in the trusted Career Profile should be used.

No AI-generated URLs.

No invented contact information.

---

# **21.12 Links**

Links should be validated.

For example:

linkedin.com/in/...  
github.com/...

We should verify basic URL structure.

We don't need external verification in V1.

The important thing is preventing malformed/generated links.

---

# **21.13 Resume length**

We should not blindly enforce:

> "Every resume must be exactly one page."

That's bad product design.

Instead:

### **Entry-level / junior**

Prefer:

> 1 page

### **Experienced candidates**

Allow:

> 1–2 pages

But the system should detect excessive content.

Example:

Resume length:  
3 pages

Recommendation:  
Consider condensing lower-relevance content.

Not:

> Automatically delete information.

The candidate decides.

---

# **21.14 Content density**

We should validate:

* extremely long bullets  
* huge paragraphs  
* excessive number of bullets  
* repeated information  
* redundant skills  
* duplicate projects  
* excessive whitespace  
* orphan headings  
* awkward page breaks

This is separate from factual validation.

---

# **21.15 Final Resume Quality Validator**

After generating the structured document:

ResumeDocument  
      ↓  
Content Validation  
      ↓  
Factual Validation  
      ↓  
ATS Structure Validation  
      ↓  
Formatting Validation  
      ↓  
Rendering  
      ↓  
Rendered File Validation

We should have **two validation stages**.

### **Stage A — Before rendering**

Check the structured content.

### **Stage B — After rendering**

Check the actual PDF/DOCX.

---

# **21.16 Stage A validation**

Check:

### **Factual**

✓ claims supported  
✓ dates correct  
✓ experience types correct  
✓ skills supported  
✓ certifications supported

### **Structural**

✓ valid sections  
✓ no missing required content  
✓ no duplicate experience  
✓ valid dates

### **Content**

✓ no unsupported claims  
✓ no unsupported metrics  
✓ no excessive repetition  
---

# **21.17 Stage B validation**

After generating PDF:

We should extract text from the PDF again.

Generated PDF  
      ↓  
PyMuPDF  
      ↓  
Extracted text  
      ↓  
Compare against ResumeDocument

Why?

Because rendering bugs can occur.

For example:

* missing text  
* broken page  
* overlapping content  
* text not selectable  
* unexpected characters

This gives us a useful integrity check.

---

# **21.18 PDF text extraction**

Since we already selected **PyMuPDF** for resume parsing, we can also use it for basic PDF validation.

For example:

Generated PDF  
      ↓  
PyMuPDF text extraction  
      ↓  
Expected content comparison

We don't need another PDF parser for V1.

---

# **21.19 DOCX validation**

For DOCX:

Generated DOCX  
      ↓  
python-docx  
      ↓  
Extract paragraphs  
      ↓  
Compare with ResumeDocument

Again, this ensures the generated file actually contains what we intended.

---

# **21.20 Rendering architecture**

We should create:

app/  
├── resume\_generation/  
│   ├── document\_builder.py  
│   ├── template\_manager.py  
│   ├── docx\_renderer.py  
│   ├── pdf\_renderer.py  
│   └── quality\_validator.py

The flow:

Approved Content  
      ↓  
ResumeDocument  
      ↓  
TemplateManager  
      ↓  
Renderer  
      ↓  
PDF / DOCX  
---

# **21.21 Renderer must never make business decisions**

This is important.

The renderer should not decide:

> "Python is important, so I'll add it."

No.

The renderer only receives approved content.

Optimizer  
    ↓  
Approved ResumeDocument  
    ↓  
Renderer

Therefore:

> **Rendering is deterministic.**

---

# **21.22 Resume generation API**

We already have:

POST /api/v1/jobs/{id}/resume/generate

We should allow:

{  
  "template": "professional\_ats",  
  "format": "pdf"  
}

Potentially:

{  
  "template": "professional\_ats",  
  "format": "docx"  
}

And later:

{  
  "template": "professional\_ats",  
  "format": "pdf",  
  "version\_id": "..."  
}  
---

# **21.23 Important: generate from a specific version**

The final resume must be tied to an immutable version.

Resume Version 7  
      ↓  
Generate PDF

not:

Current Career Profile  
      ↓  
Generate random resume

This ensures reproducibility.

---

# **21.24 File storage**

For V1:

storage/  
└── users/  
    └── {user\_id}/  
        └── resumes/  
            └── {resume\_id}/  
                ├── original/  
                │   └── original.pdf  
                │  
                └── generated/  
                    ├── version-1.pdf  
                    ├── version-2.pdf  
                    └── version-3.docx

Never use the candidate's original filename as the storage path.

---

# **21.25 Resume file metadata**

We already have `resume_files`.

For generated files, we should track:

generated\_resume\_files  
\----------------------  
id  
resume\_version\_id  
format  
storage\_key  
file\_size  
checksum  
created\_at

Or we can extend the existing file abstraction depending on the final database implementation.

The important concept is:

> Every generated file belongs to an immutable Resume Version.

---

# **21.26 Checksum**

Use SHA-256.

For example:

generated PDF  
     ↓  
SHA-256  
     ↓  
checksum

This allows us to detect accidental file corruption or duplication.

---

# **21.27 Template customization**

The candidate should eventually be able to select:

Template  
Font  
Spacing  
Margins  
Section ordering

But V1 should keep customization controlled.

For example:

Template:  
Professional ATS

Font:  
Inter / Arial / Calibri

Spacing:  
Compact / Standard

We should avoid a full Canva-like resume editor.

That's a separate product.

---

# **21.28 Font selection**

For ATS-safe resumes, use standard, highly readable fonts.

Examples:

* Arial  
* Calibri  
* Helvetica  
* Georgia

We can include a small curated set.

The system should not allow arbitrary decorative fonts in V1.

---

# **21.29 Color**

Keep color conservative.

The candidate can select:

Minimal  
Professional  
Modern

But important content should never rely on color.

For example:

> Skill names should remain readable in black-and-white printing.

---

# **21.30 Icons**

Avoid icons for essential contact information.

Instead of:

☎ 123456789  
✉ email@example.com

we can simply use:

123456789 | email@example.com

Icons may be decorative, but ATS compatibility should come first.

---

# **21.31 Resume filename**

We should automatically generate professional filenames.

Example:

Riya\_Jogi\_Python\_Backend\_Developer.pdf

But sanitize it.

No:

Riya\<\>Jogi?.pdf

Filename generation should be deterministic.

---

# **21.32 Final resume metadata**

Each generated resume should know:

Candidate  
Job  
Resume Version  
Template  
Generation timestamp  
Matching algorithm version  
Optimization version

This gives us traceability.

---

# **21.33 Final resume quality score**

I would **not** create another mysterious "AI resume score."

Instead, use quality checks:

ATS Structure       PASS  
Content Integrity   PASS  
Fact Validation     PASS  
Formatting          PASS  
Traceability        PASS

Then:

Resume Quality:  
READY

or:

Resume Quality:  
NEEDS\_REVIEW

This is more meaningful.

---

# **21.34 Final statuses**

For generated resume:

DRAFT  
VALIDATING  
READY  
NEEDS\_REVIEW  
FAILED

For example:

Optimization approved  
       ↓  
Generation  
       ↓  
VALIDATING  
       ↓  
READY

If something goes wrong:

FAILED  
---

# **21.35 What if validation fails?**

Never silently generate the file anyway.

Example:

Resume validator:  
BLOCK

Reason:  
Generated bullet contains unsupported  
"Led a team of 8 developers."

Then:

Resume generation  
       ↓  
BLOCK  
       ↓  
Return to optimization/review

The candidate must resolve it.

---

# **21.36 What if only formatting fails?**

Example:

Content:  
PASS

PDF rendering:  
WARNING

We can regenerate using the same content with the renderer.

That's a technical failure, not an AI/business failure.

---

# **21.37 ATS-safe doesn't mean ATS guarantee**

This needs to be explicit in our product language.

We can say:

> **ATS-friendly formatting**

We should NOT say:

> “Guaranteed to pass every ATS.”

Because different systems have different parsing and ranking algorithms.

Likewise:

> Job Alignment Score ≠ hiring probability.

---

# **21.38 Frontend flow**

The candidate experience should be:

Job Analysis  
      ↓  
Match Results  
      ↓  
Gap Analysis  
      ↓  
Optimize Resume  
      ↓  
Review Changes  
      ↓  
Approve Changes  
      ↓  
Choose Template  
      ↓  
Preview  
      ↓  
Final Validation  
      ↓  
Generate  
      ↓  
Download / Save Version  
---

# **21.39 Resume preview**

Before generation, show a live HTML preview:

┌───────────────────────────────────┐  
│             RIYA JOGI             │  
│       Python Backend Developer    │  
│                                   │  
│ SUMMARY                           │  
│ ...                               │  
│                                   │  
│ SKILLS                            │  
│ Python • Django • FastAPI         │  
│                                   │  
│ EXPERIENCE                        │  
│ ABC Technologies                 │  
│ Backend Developer | 2024–Present │  
│ • Developed ...                   │  
│ • Implemented ...                │  
└───────────────────────────────────┘

The preview should use the same `ResumeDocument` used by the renderer.

That prevents preview/render mismatch.

---

# **21.40 Recommended architecture**

                   Approved Changes  
                           │  
                           ▼  
                   ResumeDocument  
                           │  
              ┌────────────┼────────────┐  
              ▼            ▼            ▼  
          HTML Preview    DOCX         PDF  
              │            │            │  
              └────────────┼────────────┘  
                           ▼  
                  Quality Validation  
                           │  
                  ┌────────┴────────┐  
                  ▼                 ▼  
                READY           NEEDS\_REVIEW  
---

# **21.41 Backend structure**

Add:

app/  
├── resume\_generation/  
│   ├── document\_model.py  
│   ├── document\_builder.py  
│   ├── template\_manager.py  
│   ├── templates/  
│   │   ├── professional\_ats.py  
│   │   ├── modern\_ats.py  
│   │   └── compact\_ats.py  
│   ├── renderers/  
│   │   ├── html\_renderer.py  
│   │   ├── docx\_renderer.py  
│   │   └── pdf\_renderer.py  
│   └── quality\_validator.py  
│  
├── services/  
│   └── resume\_generation\_service.py  
│  
└── api/  
    └── v1/  
        └── resume\_generation.py  
---

# **21.42 Technology choice for rendering**

For DOCX:

> **python-docx**

This fits our Python stack and gives us deterministic document generation.

For PDF, we have two reasonable approaches:

### **Option A**

Generate PDF directly with a PDF library.

### **Option B**

Generate HTML → PDF.

For V1, I recommend we **keep the rendering interface abstract** and test the most reliable implementation on Windows/local development before locking the exact PDF engine.

The business logic should not care.

PDFRenderer  
   │  
   └── implementation can change later

This is consistent with our provider abstraction philosophy.

---

# **21.43 Final quality pipeline**

This is the final version:

            APPROVED RESUME CONTENT  
                       │  
                       ▼  
                 ResumeDocument  
                       │  
                       ▼  
              Content Validation  
                       │  
                       ▼  
              Factual Validation  
                       │  
                       ▼  
             ATS Structure Check  
                       │  
                       ▼  
                  Rendering  
                       │  
              ┌────────┴────────┐  
              ▼                 ▼  
             PDF               DOCX  
              │                 │  
              └────────┬────────┘  
                       ▼  
                File Validation  
                       │  
                       ▼  
               Text Extraction  
                       │  
                       ▼  
             Content Comparison  
                       │  
                       ▼  
              FINAL VALIDATION  
                       │  
                ┌──────┴──────┐  
                ▼             ▼  
              READY      NEEDS\_REVIEW  
---

# **21.44 Final Step 21 decisions**

| Area | V1 Decision |
| ----- | ----- |
| Structured ResumeDocument | ✅ |
| Content/presentation separation | ✅ |
| ATS-friendly formatting | ✅ |
| Single-column default | ✅ |
| Standard headings | ✅ |
| 3 initial templates | ✅ |
| HTML preview | ✅ |
| PDF | ✅ |
| DOCX | ✅ |
| Resume version association | ✅ |
| Immutable versions | ✅ |
| Claim traceability | ✅ |
| Evidence traceability | ✅ |
| Factual validation | ✅ |
| ATS structure validation | ✅ |
| Rendered-file validation | ✅ |
| PDF text extraction validation | ✅ |
| DOCX content validation | ✅ |
| SHA-256 generated-file checksum | ✅ |
| Automatic filename | ✅ |
| 1-page hard requirement | ❌ |
| 1–2 page recommendation | ✅ |
| ATS guarantee | ❌ |
| Universal ATS score | ❌ |
| Canva-style editor | ❌ V1 |
| Complex graphics | ❌ |
| Multi-column default | ❌ |
| Images containing important text | ❌ |
| AI inside renderer | ❌ |

---

# **21.45 The architecture we've built so far**

At this point, our system has a very clean separation:

┌─────────────────────────────────────────────────────┐  
│                    CANDIDATE DATA                   │  
│                                                     │  
│ Career Profile → Claims → Evidence                  │  
└─────────────────────────┬───────────────────────────┘  
                          │  
                          ▼  
┌─────────────────────────────────────────────────────┐  
│                  JOB UNDERSTANDING                  │  
│                                                     │  
│ JD → Requirements → Normalization                   │  
└─────────────────────────┬───────────────────────────┘  
                          │  
                          ▼  
┌─────────────────────────────────────────────────────┐  
│                    MATCHING                         │  
│                                                     │  
│ Exact \+ Normalized \+ Semantic \+ Rules               │  
└─────────────────────────┬───────────────────────────┘  
                          │  
                          ▼  
┌─────────────────────────────────────────────────────┐  
│                  OPTIMIZATION                       │  
│                                                     │  
│ Relevant facts → AI proposals → Change tracking     │  
└─────────────────────────┬───────────────────────────┘  
                          │  
                          ▼  
┌─────────────────────────────────────────────────────┐  
│                   VALIDATION                        │  
│                                                     │  
│ Truth \+ Claims \+ Dates \+ Evidence \+ Strength         │  
└─────────────────────────┬───────────────────────────┘  
                          │  
                          ▼  
┌─────────────────────────────────────────────────────┐  
│                  RESUME GENERATION                  │  
│                                                     │  
│ ResumeDocument → Template → PDF / DOCX              │  
└─────────────────────────┬───────────────────────────┘  
                          │  
                          ▼  
                    FINAL RESUME

The most important boundary is:

> **AI decides how to propose. Business rules decide what is allowed. The candidate decides what is approved. The renderer only renders approved truth.**