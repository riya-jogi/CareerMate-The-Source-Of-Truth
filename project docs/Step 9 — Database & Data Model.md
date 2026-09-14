Great. Now we move to **Step 9 — Database & Data Model Design**.

This is one of the most important steps because our entire product revolves around one principle:

> **The candidate's verified career information is the source of truth, and every AI-generated resume statement must be traceable back to that source.**

So we should **not design the database like a normal resume builder** where we simply store `resume_text`.

We need to model the candidate's career information as structured data.

---

# **Step 9 — Database & Data Model**

## **9.1 First, understand the fundamental relationship**

Our system isn't really:

Resume → Job Description → New Resume

It is:

                ┌───────────────┐  
                 │ Career Profile│  
                 │ Source of Truth│  
                 └───────┬───────┘  
                         │  
              ┌──────────┼──────────┐  
              ▼          ▼          ▼  
           Resume      Skills     Projects  
           Evidence    Experience Education  
              │  
              ▼  
        ┌──────────────┐  
        │ Job Description│  
        └───────┬──────┘  
                │  
                ▼  
        Job Requirements  
                │  
                ▼  
        Candidate ↔ Job  
          Matching  
                │  
                ▼  
        Gap Analysis  
                │  
                ▼  
        Resume Optimization  
                │  
                ▼  
        Truth Validation  
                │  
                ▼  
        Candidate Approval  
                │  
                ▼  
        Job-specific Resume

That is the database model we're trying to support.

---

# **9.2 Main entities**

For the MVP, I recommend these core entities:

User  
  │  
  └── CareerProfile  
          │  
          ├── CareerClaim  
          ├── Experience  
          ├── Project  
          ├── Skill  
          ├── Education  
          ├── Certification  
          └── Evidence

Job  
  │  
  └── JobRequirement

CandidateJobMatch

Resume  
  │  
  └── ResumeVersion  
          │  
          └── ResumeChange

Optimization  
  │  
  └── Approval

Let's understand each one.

---

# **9.3 `User`**

This is simply the account.

User  
\----  
id  
email  
password\_hash  
created\_at  
updated\_at

Example:

id: 101  
email: candidate@example.com

We should **not** put the entire resume inside this table.

---

# **9.4 `CareerProfile`**

This represents the candidate's overall professional identity.

CareerProfile  
\-------------  
id  
user\_id  
full\_name  
headline  
summary  
location  
phone  
email  
linkedin\_url  
github\_url  
portfolio\_url  
created\_at  
updated\_at

Example:

Full Name:  
Riya Jogi

Headline:  
Backend Developer | Python | FastAPI | AI/ML

Location:  
India

But there's an important distinction.

The profile itself contains high-level information.

The detailed facts should live in structured entities.

---

# **9.5 `Experience`**

This represents employment history.

Experience  
\----------  
id  
career\_profile\_id  
company\_name  
job\_title  
start\_date  
end\_date  
is\_current  
employment\_type  
description

Example:

Company:  
ABC Technologies

Role:  
Python Backend Developer

Start:  
2024-01

End:  
2026-03

But here's where our product becomes different.

We shouldn't rely only on:

description \= "Worked on Python backend..."

because the AI needs to know **what specific claims are supported**.

That leads us to our most important entity.

---

# **9.6 `CareerClaim` ⭐**

This is the heart of the system.

A claim represents something the candidate says is true about their career.

For example:

> "Used Python to develop REST APIs."

or:

> "Worked with PostgreSQL for backend applications."

or:

> "Built an AI-powered document Q\&A project."

Instead of storing only:

python \= true

we store:

CareerClaim  
\------------  
id  
career\_profile\_id

claim\_type  
claim\_text

experience\_type

status  
confidence

start\_date  
end\_date

source  
source\_id

created\_at  
updated\_at  
---

# **9.7 Why `CareerClaim` is so important**

Consider this candidate information:

Python

That's almost useless for our system.

Instead:

Claim:  
Used Python to develop backend APIs.

Context:  
Professional employment

Experience:  
2 years

Evidence:  
Resume \+ candidate confirmation

Status:  
Candidate-confirmed

Now the AI has context.

Another example:

Claim:  
Used Kubernetes.

Context:  
Personal project

Evidence:  
GitHub project

Status:  
Evidence-backed

The system knows this is **not automatically equivalent to professional Kubernetes experience**.

This distinction is critical.

---

# **9.8 Claim status**

We previously decided not to use simply:

verified \= true/false

Instead:

Evidence-backed  
Candidate-confirmed  
Self-declared  
Needs clarification  
Unsupported

For example:

| Claim | Status |
| ----- | ----- |
| Python backend development | 🟢 Evidence-backed |
| FastAPI | 🔵 Candidate-confirmed |
| Kubernetes | 🟡 Self-declared |
| AWS Lambda | ⚪ Needs clarification |
| Kubernetes professional experience | 🔴 Unsupported |

This allows the validator to make intelligent decisions.

---

# **9.9 `Evidence`**

Now we need to answer:

> **Why do we believe this claim?**

That's the job of the Evidence entity.

Evidence  
\--------  
id  
career\_profile\_id

evidence\_type  
title  
description

file\_id  
external\_url

created\_at

Possible evidence:

Resume  
GitHub repository  
Portfolio  
Certificate  
Project document  
Candidate confirmation  
Work sample

For example:

Evidence  
\--------  
type: GitHub  
title: AI Document Q\&A project  
url: github.com/...

Then:

CareerClaim  
     │  
     ▼  
Evidence

So the system can answer:

> "Where did this resume statement come from?"

---

# **9.10 `Skill`**

We should also have normalized skills.

Skill  
\-----  
id  
name  
category  
canonical\_name

Example:

Python  
FastAPI  
PostgreSQL  
Docker  
AWS  
TensorFlow  
PyTorch

But we shouldn't only store strings.

We need normalization.

For example:

Postgres  
PostgreSQL  
PostgreSQL DB

should map to:

Canonical Skill:  
PostgreSQL

This becomes extremely useful during JD matching.

---

# **9.11 Candidate ↔ Skill**

A candidate's relationship with a skill needs additional information.

So conceptually:

CandidateSkill  
\--------------  
career\_profile\_id  
skill\_id

experience\_type  
proficiency  
years\_used

first\_used  
last\_used

status  
evidence

Example:

Python  
\------------------------  
Experience: Professional  
Years: 2.5  
Proficiency: Strong  
Status: Evidence-backed

Versus:

Kubernetes  
\------------------------  
Experience: Personal  
Years: 0.5  
Proficiency: Basic  
Status: Self-declared

This prevents the system from treating both equally.

---

# **9.12 `Project`**

Projects deserve their own entity.

Project  
\-------  
id  
career\_profile\_id

name  
description

project\_type  
start\_date  
end\_date

url  
repository\_url

Project type:

Professional  
Personal  
Academic  
Learning

Example:

Project:  
AI-Powered Document Q\&A

Type:  
Personal

Technologies:  
Python  
FastAPI  
PostgreSQL  
pgvector  
Ollama

This project may be highly relevant to an AI/ML backend JD even if it isn't professional experience.

Our matching engine should know that distinction.

---

# **9.13 Education**

Education  
\---------  
id  
career\_profile\_id

institution  
degree  
field\_of\_study  
start\_date  
end\_date  
grade

Example:

M.Sc.  
Information Technology  
XYZ University  
---

# **9.14 Certification**

Certification  
\-------------  
id  
career\_profile\_id

name  
issuer  
issue\_date  
expiry\_date  
credential\_id  
credential\_url

Again, certifications can contribute to JD matching.

---

# **9.15 Now the Job side**

The candidate side isn't enough.

We need to represent the job.

---

## **`Job`**

Job  
\---  
id  
user\_id

company\_name  
job\_title  
job\_description

location  
employment\_type

source  
source\_url

created\_at

For MVP, the candidate can simply paste:

Job Description

Later we can support:

URL  
PDF  
LinkedIn  
Indeed  
etc.

But we don't need that complexity now.

---

# **9.16 `JobRequirement` ⭐**

The JD analyzer will convert the raw JD into structured requirements.

For example:

JobRequirement  
\--------------  
id  
job\_id

requirement\_text

requirement\_type  
importance

skill\_id

minimum\_years

experience\_type

Example:

Requirement:  
3+ years Python experience

Type:  
Skill

Importance:  
Required

Skill:  
Python

Minimum years:  
3

Another:

Requirement:  
Experience with Docker

Importance:  
Preferred

Another:

Requirement:  
Build REST APIs

Importance:  
Required  
---

# **9.17 Requirement classification**

The AI should classify requirements into:

Required  
Preferred  
Contextual

Potentially later:

Disqualifier

For example:

Python — Required  
FastAPI — Required  
Docker — Preferred  
Kubernetes — Preferred  
Bachelor's degree — Required  
Healthcare experience — Contextual

This is important for our matching score.

Missing a preferred skill shouldn't hurt as much as missing a required one.

---

# **9.18 Candidate ↔ Job Matching**

Now we can create:

CandidateJobMatch  
\-----------------  
id  
career\_profile\_id  
job\_id

overall\_score

skill\_score  
experience\_score  
education\_score  
keyword\_score  
semantic\_score

created\_at

But I don't want this table to simply store:

score \= 82

We need the **reason behind the score**.

---

# **9.19 Match details**

We should have something like:

MatchDetail  
\-----------  
id  
match\_id

job\_requirement\_id  
candidate\_claim\_id

match\_type  
score

explanation

Example:

Requirement:  
Python 3+ years

Candidate:  
Python 2.5 years professional

Match:  
Partial

Score:  
0.75

Explanation:  
Candidate has strong professional Python experience,  
but the available evidence indicates approximately 2.5 years  
against the requested 3+ years.

This is much more valuable than:

Match \= 75%  
---

# **9.20 Gap Analysis**

From these match details we can derive:

Strong Match  
Partial Match  
Gap  
Unknown

For example:

Python       🟢 Strong  
FastAPI      🟢 Strong  
PostgreSQL   🟢 Strong  
Docker       🟡 Partial  
Kubernetes   🔴 Gap  
AWS          ⚪ Unknown

The system can then tell the candidate:

> "You are a strong match for Python, FastAPI and PostgreSQL. Docker is partially aligned, while Kubernetes is currently unsupported by your career evidence."

That's the kind of intelligence our product should provide.

---

# **9.21 Resume**

Now we get to the interesting part.

We should **not overwrite the candidate's original resume**.

Instead:

Resume  
  │  
  ├── Original  
  │  
  ├── Version 1  
  ├── Version 2  
  └── Version 3

So:

Resume  
\------  
id  
career\_profile\_id  
original\_file\_id  
created\_at

And:

ResumeVersion  
\-------------  
id  
resume\_id  
job\_id

version\_number

content  
status

created\_at  
---

# **9.22 Why job-specific versions matter**

Suppose the candidate applies to:

Company A — Python Backend Developer

We generate:

Resume Version 1

Then:

Company B — AI Engineer

We generate:

Resume Version 2

The Career Profile remains unchanged.

That's critical.

Career Profile  
      │  
      ├── Job A → Resume V1  
      │  
      ├── Job B → Resume V2  
      │  
      └── Job C → Resume V3

We're generating different **representations of the same truth**.

---

# **9.23 `ResumeChange`**

This supports one of our major differentiators:

> **Show the candidate exactly what AI changed.**

Store:

ResumeChange  
\------------  
id  
resume\_version\_id

change\_type

original\_text  
new\_text

reason

source\_claim\_id

status

Example:

Original:  
Developed backend applications.

New:  
Developed Python-based REST APIs using FastAPI.

Reason:  
The job description emphasizes Python and REST API  
development, and the candidate profile contains  
evidence supporting both.

Source:  
Career Claim \#123

Status:  
Approved

That's powerful.

The candidate can see:

AI proposed this  
       ↓  
Here is why  
       ↓  
Here is the evidence  
       ↓  
Approve / Reject  
---

# **9.24 Approval**

We need explicit candidate control.

Approval  
\--------  
id  
resume\_version\_id  
change\_id

decision  
decided\_at

Decision:

Approved  
Rejected  
Edited

This gives us an audit trail.

---

# **9.25 Truth validation**

Before finalizing a resume:

Generated Resume  
       ↓  
Extract claims  
       ↓  
Compare against Career Profile  
       ↓  
Validate evidence  
       ↓  
Check unsupported claims  
       ↓  
PASS / BLOCK

For example:

Generated statement:

"Designed and deployed Kubernetes clusters."

Validator:

❌ BLOCK

Reason:  
No supporting career claim or evidence.

Whereas:

"Developed REST APIs using FastAPI."

Validator:

✅ PASS

Supporting claim:  
CareerClaim \#123  
---

# **9.26 Very important database relationship**

The architecture now becomes:

                CAREER PROFILE  
                       │  
          ┌────────────┼────────────┐  
          ▼            ▼            ▼  
       Claims       Projects     Experience  
          │  
          ▼  
       Evidence  
          │  
          ▼  
      Skills  
          │  
          │  
          │  
          ▼  
       JOB  
          │  
          ▼  
   Job Requirements  
          │  
          ▼  
   Candidate ↔ Job Match  
          │  
          ▼  
      Gap Analysis  
          │  
          ▼  
   Resume Optimization  
          │  
          ▼  
     Resume Change  
          │  
          ▼  
       Approval  
          │  
          ▼  
   Truth Validation  
          │  
          ▼  
   Final Resume

This is essentially the **data backbone of the product**.

---

# **9.27 MVP database — don't overbuild it**

Although we have discussed many entities, I don't want you to create 20 tables immediately.

For our first implementation, I would start with roughly:

users  
career\_profiles

experiences  
projects  
skills  
candidate\_skills  
education  
certifications

career\_claims  
evidence

jobs  
job\_requirements

candidate\_job\_matches  
match\_details

resumes  
resume\_versions  
resume\_changes  
approvals

That's enough to build the core product.

Some of these can be simplified initially and normalized further when we actually start coding.

---

# **9.28 One important decision before we freeze the schema**

There is one question we should settle before moving to Step 10:

### **Should `CareerClaim` be the central source of truth, or should the structured entities themselves be the source of truth?**

I recommend:

> **Structured career entities \+ Career Claims \+ Evidence**

rather than making claims completely independent.

Think of it like:

Experience  
   │  
   ├── Claim: "Developed Python APIs"  
   │        │  
   │        └── Evidence  
   │  
   ├── Claim: "Used PostgreSQL"  
   │        │  
   │        └── Evidence  
   │  
   └── Claim: "Worked on authentication system"  
            │  
            └── Evidence

This gives us both:

**structured data** for matching/filtering

and

**claim-level traceability** for AI safety.

---

## **The core design principle**

If you remember only one thing from Step 9, remember this:

> **Never let the generated resume become the source of truth.**

It should always be:

Career Evidence  
      ↓  
Career Profile  
      ↓  
Claims  
      ↓  
Job Matching  
      ↓  
AI Optimization  
      ↓  
Validation  
      ↓  
Approved Resume

**Never:**

Old Resume  
   ↓  
AI  
   ↓  
New Resume  
   ↓  
AI uses New Resume as truth

That second architecture is exactly how information can gradually become exaggerated or fabricated across multiple AI-generated resume versions.

---

### **Next step**

Before we move to Step 10, I suggest we spend one focused discussion on **the exact `CareerClaim + Evidence` model**, because that is the part that will make your product genuinely different from a normal AI resume builder.

We can design exactly:

* what a claim looks like,  
* how evidence is linked,  
* how confidence/status works,  
* how AI proposes a claim,  
* how candidate verifies it,  
* how claims are used by the matcher,  
* and most importantly, **how the system blocks AI from inventing experience**.

Absolutely. This is worth discussing carefully because **Career Claims \+ Evidence is probably the strongest technical foundation/differentiator in your product**.

# **Step 9.5 — Career Claims \+ Evidence Model**

Let's start with the problem we're solving.

A normal AI resume builder might have:

Resume

   ↓

LLM

   ↓

Optimized Resume

Our system should instead have:

Candidate's Career Data

        ↓

     Claims

        ↓

    Evidence

        ↓

   Job Requirements

        ↓

   Allowed Claims

        ↓

    AI Wording

        ↓

   Validation

        ↓

 Approved Resume

The crucial idea is:

> **AI can decide how to say something, but the system decides whether the candidate is allowed to say it.**

---

# **1\. What exactly is a Career Claim?**

A claim is a **specific factual statement about the candidate's background**.

Don't think of it as just a skill.

For example:

### **Weak representation**

Python

FastAPI

PostgreSQL

Docker

This tells us almost nothing about context.

### **Career claims**

"Used Python to develop REST APIs."

"Used FastAPI to build backend services."

"Used PostgreSQL for application data storage."

"Used Docker to containerize backend applications."

Now the system has meaningful facts to work with.

---

# **2\. A claim should contain context**

Suppose someone says:

> "I know Kubernetes."

That's not enough.

We want:

Skill:

Kubernetes

Context:

Personal project

Experience Type:

Personal

Duration:

6 months

Level:

Basic

Evidence:

GitHub repository

Status:

Evidence-backed

Compare that with:

Skill:

Kubernetes

Context:

Professional employment

Experience Type:

Professional

Duration:

2 years

Level:

Advanced

Evidence:

Employment project documentation

Status:

Evidence-backed

These are **not equivalent claims**.

This is why a simple:

kubernetes \= true

database field would be inadequate.

---

# **3\. Proposed CareerClaim structure**

Conceptually:

CareerClaim

────────────────────────

id

career\_profile\_id

claim\_type

claim\_text

subject

skill\_id

context

experience\_type

start\_date

end\_date

proficiency

status

confidence

created\_at

updated\_at

Let's understand these.

### **`claim_type`**

Examples:

skill

responsibility

achievement

project

experience

education

certification

### **`claim_text`**

The human-readable statement:

"Developed REST APIs using FastAPI."

### **`subject`**

What is the claim about?

Python

FastAPI

PostgreSQL

AWS

Machine Learning

This can connect to our normalized `Skill` entity.

---

# **4\. Experience type is extremely important**

We should explicitly distinguish:

Professional

Personal

Academic

Learning

For example:

### **Claim 1**

Python

Professional

2 years

### **Claim 2**

PyTorch

Academic

6 months

### **Claim 3**

Kubernetes

Personal

4 months

### **Claim 4**

AWS

Learning

3 months

Now when a JD says:

> "3 years of professional Python experience"

our matcher can reason correctly.

It should **not** count:

2 years professional

\+

6 months academic

\+

3 months learning

as:

2.75 years professional experience

That's one of the safeguards that separates our system from a generic LLM.

---

# **5\. Evidence**

Now comes the second half.

A claim should ideally have evidence.

For example:

Claim

─────

"Developed REST APIs using FastAPI."

       │

       ▼

Evidence

───────

Resume.pdf

Another:

Claim

─────

"Built AI document Q\&A application."

       │

       ▼

Evidence

───────

GitHub repository

Project documentation

Another:

Claim

─────

"Completed AWS certification."

       │

       ▼

Evidence

───────

AWS certificate

---

# **6\. Evidence should have a source type**

Something like:

EvidenceType

────────────

RESUME

PROJECT\_DOCUMENT

GITHUB

PORTFOLIO

CERTIFICATE

WORK\_SAMPLE

CANDIDATE\_CONFIRMATION

OTHER

This lets us understand where information came from.

For example:

Claim:

Used Docker professionally.

Evidence:

Resume

Status:

Evidence-backed

versus:

Claim:

Used Docker professionally.

Evidence:

Candidate confirmation

Status:

Candidate-confirmed

These should not necessarily have the same trust semantics.

---

# **7\. But there's an important distinction**

We must be careful with the word **verified**.

If the candidate uploads:

resume.pdf

and the resume says:

> "Used AWS for 2 years."

we haven't independently verified that statement.

We've only established:

> **The candidate provided evidence containing this claim.**

Therefore I prefer the status terminology we previously discussed:

### **🟢 Evidence-backed**

Supporting candidate-provided evidence exists.

### **🔵 Candidate-confirmed**

The candidate explicitly confirmed the claim.

### **🟡 Self-declared**

The candidate says it, but supporting evidence/context is insufficient.

### **⚪ Needs clarification**

The system cannot confidently understand the claim.

### **🔴 Unsupported**

The claim has no supporting basis.

This is much more honest than saying:

verified \= true

---

# **8\. What happens when the candidate uploads their resume?**

This is where AI enters.

Suppose their resume says:

> "Developed scalable backend APIs using Python and FastAPI."

The LLM extracts:

Claim 1:

Used Python for backend development.

Claim 2:

Used FastAPI for backend API development.

Claim 3:

Developed backend APIs.

But **the LLM does not automatically make these permanent facts.**

Instead:

Resume

   ↓

LLM extraction

   ↓

Proposed Claims

   ↓

Validation

   ↓

Candidate Review

The UI might show:

We found these claims:

✓ Used Python for backend development

   Source: Resume

✓ Used FastAPI for backend APIs

   Source: Resume

? How long did you use FastAPI?

   \[ 1 year \]

? Was this professional experience?

   \[ Professional ▼ \]

The candidate confirms/corrects them.

Only then do we create the trusted profile state.

---

# **9\. This gives us a very important state transition**

A claim can move through:

Extracted

   ↓

Needs Review

   ↓

Candidate Confirmed

   ↓

Active

Or:

Extracted

   ↓

Candidate Rejects

   ↓

Rejected

For example:

AI:

"You have Kubernetes experience."

Candidate:

"No, I only watched a Kubernetes course."

System:

Change claim → Learning

Now the system knows:

Kubernetes

Experience Type \= Learning

rather than incorrectly treating it as professional experience.

---

# **10\. What if AI misunderstands something?**

This will happen.

Suppose the resume says:

> "Worked on deploying applications using Docker."

LLM extracts:

"Managed Docker infrastructure."

That's stronger than the original statement.

Our system should **not silently accept that transformation**.

Instead, claim validation should detect the semantic strengthening.

Conceptually:

Original evidence:

"Worked on deploying applications using Docker."

AI interpretation:

"Managed Docker infrastructure."

        ↓

Semantic comparison

        ↓

Potential overstatement

        ↓

BLOCK / ASK CANDIDATE

This is a very important capability.

---

# **11\. We need a "claim strength" concept**

Not every rewrite is equally risky.

Consider:

### **Original**

> "Developed APIs using Python."

### **Rewrite A**

> "Built APIs using Python."

Almost the same factual strength.

✅ Safe.

---

### **Rewrite B**

> "Designed and developed APIs using Python."

This introduces **designed**.

Potentially okay, but needs evidence.

⚠️ Validate.

---

### **Rewrite C**

> "Architected scalable distributed systems using Python."

This is substantially stronger.

❌ Block unless supported.

This means our validator shouldn't just check:

> "Does Python exist?"

It should also ask:

> **"Did the generated statement increase the strength of the candidate's claim?"**

That's much more sophisticated.

---

# **12\. Claim strength**

We could conceptually represent:

Claim Strength

───────────────

Exposure

Learning

Used

Implemented

Developed

Designed

Led

Architected

Expert

These aren't universally ordered in every context, but they give us a useful risk model.

For example:

Evidence:

"Learned Docker."

AI output:

"Implemented Docker."

Potentially an unsupported escalation.

Whereas:

Evidence:

"Implemented Docker containers for backend deployment."

AI output:

"Containerized backend applications using Docker."

Likely safe.

---

# **13\. The AI should therefore have two responsibilities**

### **Responsibility A — Interpretation**

LLM can understand:

"Worked with Postgres"

and normalize it to:

PostgreSQL

### **Responsibility B — Presentation**

LLM can turn:

"Used Python to create APIs"

into:

"Developed REST APIs using Python."

But it should **not become the authority that decides whether the candidate actually did those things**.

That authority belongs to:

Career Profile

\+

Evidence

\+

Candidate approval

\+

Validation rules

---

# **14\. Now let's apply this to a real JD**

Suppose JD says:

> "3+ years of Python development experience, strong FastAPI knowledge, Docker, AWS, and Kubernetes."

Candidate profile:

Python

Professional

2.5 years

Evidence-backed

FastAPI

Professional

2 years

Candidate-confirmed

Docker

Professional

1 year

Evidence-backed

AWS

Learning

4 months

Self-declared

Kubernetes

Personal

3 months

Evidence-backed

The matcher should produce something like:

| Requirement | Candidate evidence | Result |
| ----- | ----- | ----- |
| Python 3+ years | 2.5 yrs professional | 🟡 Partial |
| FastAPI | 2 yrs professional | 🟢 Strong |
| Docker | 1 yr professional | 🟢 Strong |
| AWS | Learning | 🟡 Partial |
| Kubernetes | Personal project | 🟡 Partial |

Notice what **doesn't** happen.

The system doesn't say:

> "Candidate knows all five technologies."

Instead, it preserves context.

---

# **15\. Now resume optimization**

The JD emphasizes:

Python

FastAPI

Docker

AWS

Kubernetes

The optimizer can prioritize:

Python

FastAPI

Docker

because they're strongly supported.

It could potentially include:

AWS — learning

Kubernetes — personal project

if useful and appropriately labeled.

But it must **not produce**:

> "3+ years of Python, AWS and Kubernetes experience."

because that's false.

---

# **16\. The final validation pipeline**

This is where our architecture becomes really strong.

            Career Profile

                   │

                   ▼

             Job Description

                   │

                   ▼

              Job Matcher

                   │

                   ▼

            Relevant Claims

                   │

                   ▼

           Resume Optimizer

                   │

                   ▼

           Proposed Resume

                   │

                   ▼

          Claim Extraction

                   │

                   ▼

          Claim Validator

                   │

        ┌──────────┴──────────┐

        ▼                     ▼

      Valid                 Invalid

        │                     │

        ▼                     ▼

Candidate Review          BLOCK

        │

        ▼

    Approved

        │

        ▼

   Final Resume

This is the system I want us to build.

---

# **17\. One subtle but very important rule**

Suppose the candidate's profile contains:

Python

Professional

2.5 years

The JD asks:

Python

3+ years

The AI should **not try to hide the gap**.

For example, it shouldn't manipulate the dates or write:

> "Extensive Python experience."

just to make the candidate appear qualified.

Instead:

Match:

Partial

Reason:

Candidate has 2.5 years of professional Python

experience against the requested 3+ years.

Our product should help candidates **present themselves better**, not deceive recruiters.

---

# **18\. The "Single Source of Truth" rule**

Let's make this an official architecture rule:

### **Source of truth**

Career Profile \+ Claims \+ Evidence

### **Derived information**

Job Match

Gap Analysis

Resume Suggestions

Resume Versions

ATS/Job Alignment Score

### **Never source of truth**

AI-generated resume

AI-generated explanation

LLM output

Job-specific resume

This prevents a dangerous cycle:

Resume V1

 ↓

AI

 ↓

Resume V2

 ↓

AI

 ↓

Resume V3

 ↓

AI

 ↓

Candidate suddenly has 5 years experience

Instead:

Verified Career Profile

        ↓

    Resume V1

        ↓

    Resume V2

        ↓

    Resume V3

All versions originate from the same truth.

---

# **19\. One more thing: evidence can expire/change**

This is something I'd include in the design now.

Suppose:

Claim:

Currently working at Company X

Later the candidate leaves.

The claim shouldn't disappear because it was true historically.

Instead:

start\_date \= 2024

end\_date \= 2026

Similarly:

AWS Certification

Issue: 2025

Expiry: 2028

So evidence isn't simply:

valid \= true

We need temporal context.

This will become important when matching:

> "Currently working with AWS"

versus:

> "Has previous AWS experience."

---

# **20\. The model we're converging toward**

Conceptually:

┌───────────────────────┐

│     Career Profile    │

└───────────┬───────────┘

            │

            ▼

      ┌─────────────┐

      │ CareerClaim │

      └──────┬──────┘

             │

       ┌─────┴─────┐

       ▼           ▼

    Skill       Evidence

       │           │

       │           ▼

       │      Evidence Source

       │

       ▼

 Experience Context

       │

       ▼

 Professional /

 Personal /

 Academic /

 Learning

Then:

CareerClaim

     │

     ▼

Candidate ↔ Job Matching

     │

     ▼

Relevant Claims

     │

     ▼

Resume Optimization

     │

     ▼

Claim Validation

---

# **21\. The strongest product differentiator**

I think we can now articulate something very important about your product.

A normal AI resume builder says:

> **"Give me your resume and JD, and I'll create a better resume."**

Your product says:

> **"Build your trusted career profile once. For every job, I'll determine what is actually relevant, show you why, and generate a tailored resume using only claims supported by your career evidence."**

That is a **much stronger product proposition**.

And this is also why our earlier discussion about "why wouldn't someone just prompt ChatGPT to ask for approval?" is important.

ChatGPT can be instructed to ask:

> "Do you approve this change?"

But your application can maintain a **persistent structured evidence graph**, enforce claim rules, track every generated claim back to evidence, compare claim strength, maintain versions, and validate the final document before it is allowed to leave the system.

That's a system-level capability, not merely a better prompt.

---

## **I would now freeze these rules**

**Rule 1:** Every meaningful resume claim should have a source.

**Rule 2:** AI extraction creates proposals, not truth.

**Rule 3:** Candidate confirmation can establish a claim as candidate-confirmed, but doesn't mean independently verified.

**Rule 4:** Experience type must be preserved.

**Rule 5:** AI cannot increase the factual strength of a claim without supporting evidence or explicit candidate confirmation.

**Rule 6:** Generated resume content must be validated before finalization.

**Rule 7:** Every important generated statement should be traceable to one or more career claims.

**Rule 8:** Job-specific resumes never become the source of truth.

**Rule 9:** Historical experience must retain its dates/context.

**Rule 10:** When the system is uncertain, **ask rather than assume**.

This gives us a solid foundation.

