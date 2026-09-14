**Step 6: Core Features & Requirements**.

This is where we stop saying *"the product should do X"* at a high level and define **exactly what the system must be capable of doing**.

I suggest we divide requirements into:

1. **Functional requirements** — what the system must do  
2. **Business/product rules** — what the system must never do  
3. **Non-functional requirements** — security, reliability, performance, etc.  
4. **MVP vs future features**

---

# **6.1 First: What is our MVP?**

Before listing dozens of features, let's define the MVP boundary.

Our MVP should answer one question:

> **Can we take a candidate's trusted career information and a job description, then produce a relevant, ATS-aware resume without introducing unsupported claims?**

Therefore:

### **MVP**

Career Profile  
      ↓  
Resume Import  
      ↓  
Candidate Verification  
      ↓  
JD Analysis  
      ↓  
Candidate-JD Matching  
      ↓  
Gap Analysis  
      ↓  
Resume Optimization  
      ↓  
Truth Validation  
      ↓  
Change Review  
      ↓  
Final Resume

Everything else can wait.

---

# **6.2 Feature Group 1 — Candidate Account**

### **FR-01 — Account creation**

Candidate can:

* Sign up  
* Log in  
* Log out  
* Reset password

This is standard and not our differentiator.

---

# **6.3 Feature Group 2 — Career Profile**

This is **core**.

### **FR-02 — Create Career Profile**

Candidate can maintain:

### **Personal**

* Name  
* Contact  
* Location  
* LinkedIn  
* GitHub  
* Portfolio

### **Education**

* Degree  
* Institution  
* Field  
* Dates

### **Experience**

* Company  
* Position  
* Dates  
* Responsibilities  
* Achievements  
* Technologies

### **Projects**

* Name  
* Description  
* Role  
* Technologies  
* Results

### **Skills**

* Skill  
* Category  
* Experience level  
* Experience type

### **Certifications**

* Name  
* Issuer  
* Date

---

# **6.4 Evidence Management**

This is one of the most important requirements.

### **FR-03 — Every meaningful career claim should have a source/status**

For example:

Skill: FastAPI

Status:  
Evidence-backed

Evidence:  
Project: AI Document Q\&A

Context:  
Backend API development

Or:

Skill: AWS

Status:  
Candidate-confirmed

Context:  
Personal project  
---

# **6.5 Evidence Status**

We already decided on our categories:

### **🟢 Evidence-backed**

Supporting information exists.

### **🔵 Candidate-confirmed**

Candidate explicitly confirms the information.

### **🟡 Self-declared**

Candidate claims it but has not provided enough evidence.

### **⚪ Needs clarification**

System needs more information.

### **🔴 Unsupported**

No basis for using the claim.

This becomes a **business rule**, not just UI decoration.

---

# **6.6 FR-04 — Candidate Can Correct AI Extraction**

Suppose the resume says:

> "Worked with cloud services."

AI extracts:

> AWS

Candidate says:

> ❌ No, it was Azure.

The candidate must be able to correct it.

The system should then update the profile.

This is important because **AI extraction can be wrong**.

---

# **6.7 Feature Group 3 — Resume Import**

### **FR-05 — Upload existing resume**

Candidate uploads:

* PDF  
* DOCX

Potentially later:

* TXT

The system extracts:

* Experience  
* Skills  
* Projects  
* Education  
* Certifications  
* Achievements

But extraction creates **proposals**, not unquestioned truth.

---

# **6.8 Important Rule**

The workflow should be:

Resume  
  ↓  
AI Extraction  
  ↓  
Proposed Profile  
  ↓  
Candidate Review  
  ↓  
Confirm / Edit / Reject  
  ↓  
Career Profile

NOT:

Resume  
  ↓  
AI Extraction  
  ↓  
Automatically trusted profile

This is crucial.

---

# **6.9 Feature Group 4 — Job Description Analysis**

### **FR-06 — Add Job Description**

MVP:

> Paste JD

Later:

> Upload JD

Later:

> Job URL

---

### **FR-07 — Extract Job Requirements**

System should identify:

### **Job information**

* Job title  
* Company if available  
* Location if available

### **Experience**

* Required years  
* Preferred years

### **Skills**

* Programming languages  
* Frameworks  
* Databases  
* Cloud  
* Tools

### **Qualifications**

* Degree  
* Certification

### **Responsibilities**

* Development  
* Testing  
* Deployment  
* Leadership  
* etc.

---

# **6.10 Required vs Preferred**

This is important.

For example:

REQUIRED

Python  
FastAPI  
PostgreSQL  
2+ years experience

PREFERRED

AWS  
Docker  
Kubernetes

We should not treat every keyword equally.

---

# **6.11 Feature Group 5 — Candidate ↔ JD Matching**

### **FR-08 — Match candidate against requirements**

Example:

| Requirement | Candidate | Result |
| ----- | ----- | ----- |
| Python | Verified | 🟢 Strong |
| FastAPI | Evidence-backed | 🟢 Strong |
| PostgreSQL | Verified | 🟢 Strong |
| Docker | Candidate-confirmed | 🔵 Confirmed |
| AWS | Self-declared | 🟡 Partial |
| Kubernetes | Unsupported | 🔴 Missing |

---

# **6.12 Semantic Matching**

This is where AI becomes genuinely useful.

Suppose JD says:

> "Develop RESTful web services."

Candidate says:

> "Built REST APIs."

A basic keyword checker may not recognize these as strongly related.

Our system should.

Similarly:

> PostgreSQL

and

> Postgres

should be recognized as the same technology.

But there's an important rule:

> **Semantic similarity can identify a potential match; it cannot create candidate experience.**

That's a very important distinction.

---

# **6.13 FR-09 — Gap Analysis**

The system should tell the candidate:

### **Missing skills**

> Kubernetes

### **Partial skills**

> AWS

### **Experience gap**

> Required: 3 years  
>  Candidate: 1.5 years

### **Missing qualification**

> JD requires Bachelor's degree in Computer Science.

etc.

This makes the product useful even **before generating a resume**.

---

# **6.14 Feature Group 6 — Resume Optimization**

### **FR-10 — Generate job-specific resume**

The system should:

* Select relevant experience  
* Prioritize relevant projects  
* Prioritize relevant skills  
* Reword supported content  
* Remove/reduce irrelevant content  
* Improve keyword representation  
* Maintain ATS-readable formatting

---

# **6.15 What the system can change**

Let's establish a clear matrix.

| Change | Allowed? |
| ----- | ----- |
| Reorder sections | ✅ |
| Reorder skills | ✅ |
| Highlight relevant project | ✅ |
| Shorten irrelevant project | ✅ |
| Improve grammar | ✅ |
| Rephrase existing experience | ✅ |
| Use equivalent terminology | ✅ |
| Add unsupported skill | ❌ |
| Increase experience | ❌ |
| Invent responsibility | ❌ |
| Invent project | ❌ |
| Invent certification | ❌ |
| Change employment dates | ❌ |
| Claim professional experience from a course | ❌ |

This table could eventually become part of our **AI safety/validation rules**.

---

# **6.16 FR-11 — Change Tracking**

Every meaningful change should have:

Original  
    ↓  
Proposed  
    ↓  
Reason  
    ↓  
Evidence

For example:

### **Change**

**Original:**

> Worked on backend APIs.

**Proposed:**

> Developed REST APIs using Python and FastAPI.

### **Reason**

> JD emphasizes REST APIs and FastAPI.

### **Evidence**

> Company A — Backend Developer

---

# **6.17 FR-12 — Candidate Approval**

Candidate can:

* Approve  
* Reject  
* Edit

For MVP, I would make approval **explicit**.

No:

> "Generate final resume automatically."

Instead:

> **Review changes → Approve → Generate final resume**

---

# **6.18 FR-13 — Truth Validation Before Final Resume**

Even after the AI generates the resume, we should run another validation step.

Conceptually:

Generated Resume  
       ↓  
Claim Extraction  
       ↓  
Compare with Career Profile  
       ↓  
Evidence Check  
       ↓  
Unsupported Claim?  
       │  
   ┌───┴────┐  
  YES       NO  
   │         │  
   ▼         ▼  
BLOCK     Continue

This is extremely important.

We shouldn't rely on the LLM's first output.

---

# **6.19 Feature Group 7 — Job Alignment / ATS Analysis**

### **FR-14 — Analyze resume against JD**

Instead of pretending to know a company's exact ATS algorithm, we measure things we can reasonably evaluate:

### **Requirement coverage**

> 8/10 important requirements represented.

### **Keyword coverage**

> 14/17 relevant terms represented.

### **Experience alignment**

> Partial.

### **Skills alignment**

> Strong.

### **Formatting checks**

* Standard headings  
* Readable structure  
* No problematic formatting  
* Text is extractable  
* Contact information detectable

---

# **6.20 Don't Call This "Guaranteed ATS Score"**

I would phrase it as:

> **Job Alignment Score**

or:

> **Resume Compatibility Analysis**

And perhaps have:

### **Overall Alignment**

**84%**

with a breakdown.

That is more honest than:

> "84% ATS pass probability."

---

# **6.21 Feature Group 8 — Resume Generation**

Once approved:

### **FR-15 — Generate final resume**

Candidate selects a template.

MVP could have just:

* Clean professional template  
* ATS-friendly template

We don't need 50 templates initially.

---

# **6.22 Feature Group 9 — Resume Versioning**

I'd actually classify this as **MVP+**, not mandatory MVP.

For each job:

Company A  
   │  
   └── Python Developer  
          │  
          ├── JD  
          ├── Match Analysis  
          ├── Resume v1  
          ├── Approved Changes  
          └── Application

This becomes very valuable later.

---

# **6.23 Feature Group 10 — Application Tracking**

Later:

Company A  
Python Developer  
Applied: Sept 13  
Resume: v3  
Status: Applied

Possible statuses:

* Saved  
* Applied  
* Assessment  
* Interview  
* Rejected  
* Offer  
* Withdrawn

Again, useful but not core to proving our primary concept.

---

# **6.24 Auto-Apply**

Definitely **later**.

Why?

Because auto-apply introduces a completely different class of problems:

* Website automation  
* Login/session handling  
* CAPTCHA  
* Application-specific questions  
* Consent  
* Duplicate applications  
* Website changes  
* Terms of service  
* Incorrect answers  
* Resume submission without user awareness

We don't need these problems while proving the core idea.

---

# **6.25 Non-Functional Requirements**

Now let's discuss requirements that aren't visible as features.

## **Security**

Career information is sensitive.

We need:

* Authentication  
* Authorization  
* Secure storage  
* Encryption where appropriate  
* Secure file handling  
* Access control

---

## **Privacy**

The candidate's:

* Resume  
* Career history  
* Contact information  
* Job applications

should be treated as private data.

We should have clear data-retention/deletion policies in a real product.

---

## **Reliability**

If the system generates a resume, we want predictable behavior.

Particularly:

> **No unsupported claims should silently pass validation.**

---

## **Explainability**

Candidate should understand:

> Why was this changed?

> Why is this skill considered a match?

> Why is this requirement considered missing?

---

## **Auditability**

We should eventually be able to answer:

> "Why did the system put this statement into the resume?"

For example:

Resume statement  
       ↓  
Career Profile Claim  
       ↓  
Evidence  
       ↓  
Candidate approval

That's powerful.

---

# **6.26 Our Requirements Matrix**

Here's where I'd currently put everything:

| Feature | MVP | Later |
| ----- | ----- | ----- |
| Account | ✅ |  |
| Career Profile | ✅ |  |
| Resume Upload | ✅ |  |
| Profile Extraction | ✅ |  |
| Candidate Verification | ✅ |  |
| Evidence Status | ✅ |  |
| JD Analysis | ✅ |  |
| Requirement Classification | ✅ |  |
| Candidate-JD Matching | ✅ |  |
| Gap Analysis | ✅ |  |
| Semantic Matching | ✅ |  |
| Resume Optimization | ✅ |  |
| Truth Validation | ✅ |  |
| Change Tracking | ✅ |  |
| Candidate Approval | ✅ |  |
| Job Alignment Analysis | ✅ |  |
| Resume Generation | ✅ |  |
| Multiple Templates |  | ✅ |
| Resume Version History |  | ✅ |
| Application Tracking |  | ✅ |
| Cover Letters |  | ✅ |
| Job URL Parsing |  | ✅ |
| Job Discovery |  | ✅ |
| Auto Apply |  | ✅ |
| Interview Preparation |  | ✅ |
| External Verification |  | ✅ |

---

# **6.27 The MVP in One Picture**

This is the product I would actually build first:

                ┌─────────────────┐  
                 │    CANDIDATE    │  
                 └────────┬────────┘  
                          │  
                          ▼  
                ┌───────────────────┐  
                │ Career Profile    │  
                │ \+ Evidence        │  
                └─────────┬─────────┘  
                          │  
                ┌─────────▼─────────┐  
                │ Existing Resume   │  
                │     Import        │  
                └─────────┬─────────┘  
                          │  
                    Candidate  
                    Verification  
                          │  
                          ▼  
                ┌───────────────────┐  
                │  Trusted Profile  │  
                └─────────┬─────────┘  
                          │  
                          │  
                ┌─────────▼─────────┐  
                │   Job Description │  
                └─────────┬─────────┘  
                          │  
                          ▼  
                ┌───────────────────┐  
                │    JD Analysis    │  
                └─────────┬─────────┘  
                          │  
                          ▼  
                ┌───────────────────┐  
                │ Candidate ↔ JD    │  
                │     Matching      │  
                └─────────┬─────────┘  
                          │  
                          ▼  
                ┌───────────────────┐  
                │  Gap \+ Alignment  │  
                └─────────┬─────────┘  
                          │  
                          ▼  
                ┌───────────────────┐  
                │ Resume Optimizer  │  
                └─────────┬─────────┘  
                          │  
                          ▼  
                ┌───────────────────┐  
                │ Truth Validation  │  
                └─────────┬─────────┘  
                          │  
                          ▼  
                ┌───────────────────┐  
                │ Change Review     │  
                └─────────┬─────────┘  
                          │  
                          ▼  
                ┌───────────────────┐  
                │ Candidate Approve│  
                └─────────┬─────────┘  
                          │  
                          ▼  
                ┌───────────────────┐  
                │ Final Resume      │  
                └───────────────────┘  
---

# **One very important architectural consequence**

Notice something we've established:

**The resume is no longer the main database object.**

The hierarchy should eventually look conceptually like:

Candidate  
   │  
   └── Career Profile  
          │  
          ├── Experience  
          ├── Projects  
          ├── Skills  
          ├── Education  
          ├── Certifications  
          └── Evidence  
                │  
                ▼  
             Job  
                │  
                ├── JD Analysis  
                ├── Match Results  
                ├── Proposed Changes  
                ├── Approved Changes  
                └── Generated Resume

That decision will have a **huge impact on our database design and architecture**.

---

# **One more thing before architecture**

I think we should define the **AI decision boundaries** in detail before we start designing the architecture.

Because we now know *what* the product should do, but we haven't yet answered:

> **Which parts should use an LLM?**

> **Which parts should use deterministic rules?**

> **Which parts should use embeddings/vector search?**

> **Which parts should never be left to AI?**

For example:

**JD extraction → LLM \+ structured validation**

**Skill normalization → database/taxonomy \+ AI**

**Candidate matching → embeddings \+ rules**

**Experience calculation → deterministic code**

**Truth validation → deterministic evidence checks \+ AI semantic comparison**

**Resume wording → LLM**

**Final permission to use a claim → application rules, NOT LLM**

