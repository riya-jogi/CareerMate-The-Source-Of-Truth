I would **define the LLM boundaries first**, because otherwise Step 7 becomes a list of AI technologies without knowing what each one is actually responsible for.

And this is also where we can make your product meaningfully different from **"just prompt ChatGPT better."**

# **Step 7 — AI/ML Components & Decision Architecture**

Let's start with the most important principle.

## **7.0 The Golden Architecture Rule**

> **The LLM can make suggestions and interpretations. It cannot be the final authority on candidate truth, permissions, or application decisions.**

Think of the system as having two brains:

### **🧠 AI/LLM**

Good at:

* Understanding language  
* Extracting information  
* Understanding context  
* Rephrasing  
* Semantic comparison  
* Ranking  
* Generating explanations

### **⚙️ Deterministic application logic**

Good at:

* Rules  
* Validation  
* Permissions  
* Calculations  
* Evidence status  
* Versioning  
* Candidate approval  
* Blocking unsupported claims

So:

                 SYSTEM  
                     │  
          ┌──────────┴──────────┐  
          │                     │  
          ▼                     ▼  
       AI/LLM              RULE ENGINE  
          │                     │  
   "What might this       "What is allowed?"  
      mean?"                    │  
          │                     │  
          └──────────┬──────────┘  
                     ▼  
                FINAL RESULT  
---

# **7.1 What should NEVER be decided solely by the LLM?**

This is our first boundary.

## **❌ Candidate truth**

LLM should never decide:

> "This candidate knows Kubernetes."

It can **detect a mention** of Kubernetes.

But whether Kubernetes is an approved candidate claim should come from the profile/evidence/confirmation system.

---

## **❌ Experience duration**

If the candidate has:

> Jan 2025 – Jun 2026

the system should calculate the duration.

Don't ask the LLM:

> "How many years of experience does this candidate have?"

Use deterministic date calculations.

---

## **❌ Employment dates**

Never allow the LLM to modify:

> Jan 2024 – Dec 2025

into:

> 2023 – Present

---

## **❌ Candidate approval**

The LLM cannot decide:

> "The candidate probably agrees with this change."

Only the candidate can approve.

---

## **❌ Whether unsupported information can enter the final resume**

This should be a system-level rule.

---

## **❌ Application submission**

The LLM should never independently decide:

> "This looks good, submit the application."

Submission should happen only according to explicit user/system authorization.

---

# **7.2 What SHOULD use an LLM?**

LLMs are extremely useful where the problem involves **understanding natural language**.

### **JD understanding**

Given:

> "Looking for an experienced backend engineer with strong Python skills and hands-on experience building RESTful APIs using FastAPI."

LLM can extract:

Role: Backend Engineer

Skills:  
Python  
FastAPI  
REST APIs

Experience:  
Experienced backend engineer

Responsibility:  
API development

This is an excellent LLM use case.

---

# **7.3 Resume information extraction**

Given:

> "Developed backend services using Python and FastAPI and optimized PostgreSQL queries."

LLM can identify:

* Python  
* FastAPI  
* PostgreSQL  
* Backend development  
* Database optimization

But the extracted information should go through validation.

Resume  
  ↓  
LLM extraction  
  ↓  
Structured claims  
  ↓  
Validation  
  ↓  
Candidate confirmation  
  ↓  
Profile  
---

# **7.4 Semantic Matching**

This is another important AI component.

Suppose JD says:

> "Develop RESTful web services."

Candidate says:

> "Built REST APIs."

A simple keyword system might see:

RESTful ≠ REST

But semantically they're very close.

AI/embeddings can identify that relationship.

Similarly:

> "Postgres"

and:

> "PostgreSQL"

should match.

---

# **7.5 But semantic similarity has a boundary**

This is extremely important.

Suppose:

> JD: Kubernetes

Candidate:

> Docker

An embedding model might determine:

> Docker and Kubernetes are related.

But that **doesn't mean the candidate has Kubernetes experience**.

Therefore:

Semantic similarity  
       ≠  
Candidate qualification

This distinction should be explicitly built into our system.

---

# **7.6 Resume rewriting**

This is probably where the LLM gets the most visibility.

Suppose candidate says:

> "Made backend APIs with Python."

LLM can propose:

> "Developed REST APIs using Python."

But before accepting:

Proposed statement  
        ↓  
What claims does it contain?  
        ↓  
Python ✓  
REST API ?  
        ↓  
Does candidate evidence support REST API?  
        ↓  
YES → allowed  
NO  → reject / ask candidate

So even generated text gets validated.

---

# **7.7 The LLM should produce structured output**

This is another architectural rule.

We shouldn't simply ask:

> "Analyze this JD."

and get a huge paragraph.

We should ask it to produce structured information.

Conceptually:

{  
  "job\_title": "Python Backend Developer",  
  "required\_skills": \[  
    "Python",  
    "FastAPI",  
    "PostgreSQL"  
  \],  
  "preferred\_skills": \[  
    "AWS",  
    "Docker"  
  \],  
  "experience": {  
    "minimum\_years": 2  
  }  
}

Then our backend can validate and process this.

This makes the LLM much easier to control.

---

# **7.8 LLM output should never directly modify the database**

This is another strong rule.

Bad architecture:

JD  
 ↓  
LLM  
 ↓  
UPDATE candidate\_profile

No.

Better:

JD  
 ↓  
LLM  
 ↓  
Proposed structured result  
 ↓  
Validation  
 ↓  
Business rules  
 ↓  
Database

Same thing for resume generation.

---

# **7.9 Proposed AI/ML architecture**

Now let's identify our components.

## **Component 1 — Document Parser**

Input:

* Resume PDF/DOCX  
* JD text

Purpose:

> Extract usable text and structure.

This doesn't necessarily need an LLM.

---

# **7.10 Component 2 — JD Analyzer**

**LLM**

Responsibilities:

* Identify job title  
* Extract requirements  
* Identify skills  
* Identify responsibilities  
* Identify qualifications  
* Identify experience requirements  
* Separate required vs preferred  
* Understand contextual requirements

Output:

> Structured Job Profile

---

# **7.11 Component 3 — Resume/Profile Extractor**

**LLM \+ parsing**

Input:

> Existing resume

Output:

> Structured candidate claims

Example:

Experience  
 └── ABC Technologies  
      ├── Python  
      ├── FastAPI  
      └── PostgreSQL

Then candidate confirms/corrects.

---

# **7.12 Component 4 — Skill Normalization**

Suppose candidate has:

> Postgres

JD says:

> PostgreSQL

System should map them to a canonical skill:

Postgres  
    ↓  
PostgreSQL

This could combine:

* Skill taxonomy  
* Exact matching  
* Synonym mapping  
* Embeddings  
* LLM when ambiguous

We don't need an LLM for every simple synonym.

---

# **7.13 Component 5 — Candidate-JD Matching Engine**

This should probably be **hybrid**, not purely LLM.

It can combine:

### **Exact matching**

Python ↔ Python

### **Normalized matching**

Postgres ↔ PostgreSQL

### **Semantic matching**

RESTful API ↔ REST API

### **Evidence**

Does candidate actually have supporting evidence?

### **Requirement importance**

Required \> Preferred

### **Experience**

3 years required  
vs  
1.5 years candidate

This gives us a much more reliable match.

---

# **7.14 Component 6 — Gap Analyzer**

This can use a combination of:

* Rules  
* Structured matching  
* LLM explanation

For example:

Requirement:  
Kubernetes

Candidate:  
No supporting evidence

Result:  
Missing

No LLM is needed to decide that.

The LLM might help explain:

> "Kubernetes is listed as a preferred infrastructure skill, but your profile currently contains no supporting experience."

---

# **7.15 Component 7 — Resume Optimizer**

This is primarily an **LLM generation task**.

Input:

Candidate Profile  
\+  
Relevant Evidence  
\+  
Job Requirements  
\+  
Optimization Rules

Output:

> Proposed resume content.

But here's the critical part:

### **The LLM should NOT receive unrestricted permission to use the entire world of knowledge.**

It should receive the **candidate facts it is allowed to use**.

Conceptually:

LLM Context

ALLOWED FACTS  
├── Python  
├── FastAPI  
├── PostgreSQL  
├── Docker  
├── Project X  
└── Company A experience

DO NOT CLAIM  
├── Kubernetes  
├── 5 years experience  
└── AWS production experience

This is much safer than merely saying:

> "Don't hallucinate."

---

# **7.16 Component 8 — Claim Validator**

This could become one of the most important components of the project.

After generating the resume:

Generated Resume  
       ↓  
Extract claims  
       ↓  
Compare against Candidate Profile  
       ↓  
Evidence check  
       ↓  
Allowed?

For example:

### **Generated claim**

> "Designed microservices architecture."

System searches candidate evidence.

No supporting claim.

Result:

### **❌ BLOCKED**

The candidate never sees this in the final resume unless they explicitly add/confirm appropriate evidence.

---

# **7.17 Component 9 — Change Explanation Engine**

For each change:

Original  
    ↓  
New  
    ↓  
Why?  
    ↓  
Evidence

LLM can generate the explanation, but the underlying evidence should come from our system.

For example:

> **Why was FastAPI highlighted?**

Because:

> FastAPI appears in the candidate's verified project experience and is a required skill in the JD.

---

# **7.18 Component 10 — ATS/Resume Compatibility Analyzer**

This should mostly be **deterministic \+ rule-based**.

Things like:

* Is text extractable?  
* Are standard headings used?  
* Are contact details detectable?  
* Are important sections present?  
* Are required keywords represented?  
* Are there suspicious formatting patterns?  
* Are dates consistent?

LLM can assist with semantic coverage, but shouldn't be responsible for everything.

---

# **7.19 Component 11 — Resume Generator**

Once the candidate approves the content:

Approved structured content  
        ↓  
Template  
        ↓  
Resume document

The actual document rendering doesn't need an LLM.

This should be deterministic.

---

# **7.20 Our AI/ML architecture**

So conceptually:

                        INPUTS  
                           │  
              ┌────────────┴────────────┐  
              │                         │  
          RESUME                    JOB DESCRIPTION  
              │                         │  
              ▼                         ▼  
       Document Parser             JD Analyzer  
              │                         │  
              ▼                         ▼  
       Profile Extractor          Job Profile  
              │                         │  
              ▼                         │  
        Candidate Claims              │  
              │                         │  
              └──────────┬──────────────┘  
                         ▼  
                  Matching Engine  
                         │  
              ┌──────────┼──────────┐  
              ▼          ▼          ▼  
           Matches      Gaps      Evidence  
              │          │          │  
              └──────────┼──────────┘  
                         ▼  
                  Resume Optimizer  
                         │  
                         ▼  
                  Proposed Resume  
                         │  
                         ▼  
                  Claim Validator  
                         │  
                   ┌─────┴─────┐  
                   ▼           ▼  
                Allowed      Blocked  
                   │  
                   ▼  
              Change Tracker  
                   │  
                   ▼  
            Candidate Approval  
                   │  
                   ▼  
             Resume Generator  
                   │  
                   ▼  
              Final Resume  
---

# **7.21 Where embeddings/vector search fit**

This is something people often get wrong.

We **do not need a vector database just because this is an AI project.**

We need embeddings where semantic retrieval is useful.

For example, the candidate might have:

**50 projects \+ 10 years of experience \+ hundreds of claims.**

When a JD arrives, we want to retrieve:

> "Which pieces of this candidate's experience are most relevant to this job?"

Embeddings can help retrieve candidate evidence.

For example:

JD:  
"Build RESTful APIs using Python"

             ↓ embedding

Candidate Evidence

Project A → 0.91 similarity  
Project B → 0.84  
Project C → 0.42  
Project D → 0.18

Then the system can inspect the top relevant evidence.

But similarity doesn't authorize a claim.

That's the distinction again:

> **Vector search finds relevant evidence. Rules determine whether that evidence can support a claim.**

---

# **7.22 Do we need fine-tuning?**

For the MVP:

### **Probably no.**

We can accomplish a lot using:

* LLM API  
* Structured prompts  
* JSON/schema-constrained outputs  
* Embeddings  
* Skill taxonomy  
* Deterministic rules  
* Validation

Fine-tuning should only be considered later if we collect enough high-quality examples and identify a specific task where it provides measurable improvement.

Don't fine-tune just because:

> "This is an AI/ML project."

---

# **7.23 What about traditional ML?**

We could eventually build ML models for:

### **Resume-job relevance**

Predict likelihood that a candidate profile aligns with a JD.

### **Ranking**

Rank candidate experiences/projects for a specific JD.

### **Classification**

Classify:

* Required vs preferred  
* Skill categories  
* Experience types

But again:

**MVP doesn't need a custom ML model.**

We can start with a hybrid architecture and later introduce ML where data justifies it.

---

# **7.24 The decision hierarchy**

This is perhaps the most important diagram for the whole project:

                   LLM  
                     │  
              Makes a proposal  
                     │  
                     ▼  
              Validation Layer  
                     │  
          ┌──────────┴──────────┐  
          │                     │  
       Evidence             Business Rules  
          │                     │  
          └──────────┬──────────┘  
                     ▼  
               Permission  
                     │  
          ┌──────────┴──────────┐  
          ▼                     ▼  
       Allowed                Blocked  
          │                     │  
          ▼                     ▼  
Candidate Review           Explain why  
          │  
          ▼  
       APPROVAL  
          │  
          ▼  
      Final Output

**The LLM proposes. The system validates. The candidate approves.**

I'd actually make that one of the core principles of the project.

---

# **7.25 What makes this defensible against ChatGPT?**

Now we can return to your earlier concern.

Someone can tell ChatGPT:

> "Don't hallucinate."

But they would still be relying on the LLM to police itself.

Your system instead has:

### **Persistent structured career profile**

* 

### **Evidence-backed claims**

* 

### **Skill normalization**

* 

### **JD requirement model**

* 

### **Hybrid matching**

* 

### **Explicit claim permissions**

* 

### **Post-generation validation**

* 

### **Change/evidence tracking**

* 

### **Candidate approval**

* 

### **Resume/application version history**

That is the difference between:

> **"A prompt that tells AI to behave."**

and:

> **"A system engineered so AI has limited authority."**

That's a much stronger product.

---

# **One more important decision: Should we use one LLM or multiple AI models?**

For the MVP, I recommend **one capable LLM \+ specialized non-LLM components** rather than creating a complicated multi-agent system.

Something like:

            LLM  
              │  
    ┌─────────┼─────────┐  
    ▼         ▼         ▼  
JD Analysis  Extraction  Generation  
              │  
              ▼  
        Embedding Model  
              │  
              ▼  
        Matching / Search  
              │  
              ▼  
        Rule Engine  
              │  
              ▼  
         Validation

Don't introduce:

> Agent 1 → Agent 2 → Agent 3 → Agent 4 → Agent 5

unless there's a real reason.

For this product, **controlled orchestration** is more important than "multi-agent AI."

---

# **So Step 7 gives us this architecture philosophy**

### **LLM is responsible for:**

**Understand → Extract → Interpret → Suggest → Rewrite → Explain**

### **Traditional application logic is responsible for:**

**Store → Calculate → Validate → Authorize → Block → Track → Approve**

### **Embeddings are responsible for:**

**Find semantically relevant information**

### **Candidate is responsible for:**

**Confirm → Correct → Approve**

---

## **And now we are ready for the actual technical architecture.**

The next step should be **Step 8 — System Architecture & Technology Stack**.

There we'll decide, concretely:

* Frontend  
* Backend  
* Database  
* File storage  
* Vector database / pgvector  
* LLM  
* Embedding model  
* Document parsing  
* Resume generation  
* Authentication  
* API structure  
* Background jobs/queues  
* Caching  
* Validation engine  
* How all components communicate

And importantly, we'll design it as a **real-world project you can actually build**, rather than an unnecessarily complicated enterprise architecture.

