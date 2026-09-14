Yes. This is probably the **most important product decision so far**, because if we define "verified" poorly, our main differentiator disappears.

The first thing I would change is the terminology:

> **Don't treat information as simply "verified" or "unverified."**

Real-world candidate information has different levels of confidence.

For example, saying:

> "I know Python"

is not the same as:

> "I used Python for 2 years at Company X"

and neither is the same as:

> "Here is a project/repository/certificate that supports my Python experience."

So I recommend a **Career Evidence Model**.

---

# **1\. Four levels of information**

I'd start with four states.

| Level | Meaning | Example | Can AI use it? |
| ----- | ----- | ----- | ----- |
| 🟢 **Verified** | Strong supporting evidence exists | Employment record, documented project, certificate | Yes |
| 🔵 **Candidate-Confirmed** | Candidate explicitly confirms it is true | "I used Docker in my project" | Yes, with appropriate wording |
| 🟡 **Self-Declared** | Candidate claims it, but no supporting evidence | "I know Kubernetes" | Limited |
| 🔴 **Unsupported** | No evidence and candidate hasn't confirmed it | JD mentions Kubernetes but candidate never mentioned it | **No** |

But there's an important distinction:

### **"Verified" should NOT necessarily mean:**

> "We independently proved this person did it."

That would be extremely difficult for an MVP.

Instead, we can define:

> **Verified \= the candidate has provided sufficient evidence or explicitly confirmed the information for use in their job application.**

Later we could introduce stronger external verification.

---

# **2\. What counts as evidence?**

This is where the product becomes interesting.

Suppose the candidate says:

> "I worked with FastAPI."

The system could have evidence such as:

### **Strong evidence**

* Existing resume  
* Employment/project description  
* Portfolio  
* GitHub repository  
* Project documentation  
* Certification  
* Candidate-provided work sample

### **Moderate evidence**

* Candidate explicitly confirms the skill  
* Candidate provides details about where/how they used it

### **Weak evidence**

* AI infers it from another technology  
* JD mentions it  
* Similar skills suggest it

And here's the crucial rule:

> **AI inference should never automatically become candidate fact.**

---

# **3\. Example**

Candidate profile:

### **Experience**

**Backend Developer — Company A**

> Developed APIs using Python and FastAPI.

The system can establish:

Python

   │

   └── Evidence:

       Company A

       Backend Developer

       API development

and:

FastAPI

   │

   └── Evidence:

       Company A

       Backend Developer

       API development

Those can be considered **evidence-backed**.

---

Now suppose the JD says:

> Kubernetes experience required.

The candidate has never mentioned Kubernetes.

The AI might think:

> "Backend developers often use Kubernetes."

But our system must say:

### **🔴 Kubernetes — Unsupported**

> No candidate evidence found.

And it must **not** put Kubernetes in the resume.

---

# **4\. Candidate confirmation is extremely important**

Now suppose the system detects something ambiguous.

For example, the candidate's project description says:

> "Deployed the application to a cloud environment."

The system asks:

> **Which cloud platform did you use?**

Options:

* AWS  
* Azure  
* GCP  
* Other  
* I don't remember

Candidate selects:

> AWS

Now AWS becomes:

### **🔵 Candidate-Confirmed**

And we can use it.

This creates a controlled way for the system to **improve the candidate profile without allowing AI to guess.**

---

# **5\. What AI should be allowed to do**

This is where we establish hard rules.

## **AI CAN:**

### **Extract**

From:

> "Built backend APIs using Python and FastAPI."

AI can extract:

* Python  
* FastAPI  
* Backend development  
* API development

---

### **Normalize**

Candidate says:

> "Postgres"

System can recognize:

> PostgreSQL

But it should preserve the original evidence.

So:

Candidate wording:

Postgres

Normalized skill:

PostgreSQL

Source:

Candidate profile

This is important for matching JDs.

---

### **Reorganize**

If the job heavily emphasizes FastAPI:

The system can move FastAPI-related experience higher.

---

### **Rewrite**

It can improve wording:

> "Made APIs using FastAPI"

→

> "Developed REST APIs using FastAPI."

**Provided the underlying claim remains equivalent.**

---

### **Select**

Candidate has 10 projects.

JD is for a backend developer.

System can select the 3 most relevant projects.

---

### **Shorten**

It can remove irrelevant details.

---

# **6\. AI CANNOT do these things automatically**

This is the "truth firewall."

### **❌ Invent a skill**

JD:

> Kubernetes

Candidate:

> Nothing about Kubernetes

AI:

> "Add Kubernetes."

**BLOCKED.**

---

### **❌ Invent experience**

Candidate:

> 1.5 years

JD:

> 3+ years

AI cannot transform this into:

> 3 years experience.

---

### **❌ Invent responsibilities**

Candidate:

> "Worked on API development."

AI cannot create:

> "Designed distributed microservices architecture."

unless supported.

---

### **❌ Invent projects**

Never.

---

### **❌ Invent certifications**

Never.

---

### **❌ Convert learning into professional experience**

Candidate:

> Completed a Kubernetes course.

AI cannot write:

> "Experienced Kubernetes engineer."

---

# **7\. We also need "experience type"**

This is another important part.

The same technology can appear in different contexts.

Suppose a candidate knows Kubernetes because they:

### **A. Used it professionally**

> Company production system

### **B. Used it in a personal project**

> Personal project

### **C. Used it academically**

> University project

### **D. Learned it**

> Online course

These shouldn't all be represented identically.

So we should store:

Skill: Kubernetes

Experience Type:

Professional / Personal / Academic / Learning

Confidence:

Verified / Candidate Confirmed / Self Declared

Evidence:

Project X

Duration:

6 months

Last Used:

2026

Now the system can produce much more truthful resumes.

---

# **8\. This gives us a "Claim" rather than just a "Skill"**

I think this is an important conceptual decision.

Don't simply store:

> Python \= true

Instead store something closer to:

> **Candidate Claim**

For example:

> "Used Python to develop backend APIs at Company A from 2024–2026."

That claim has:

* Skill  
* Context  
* Experience  
* Duration  
* Evidence  
* Source  
* Confidence

Now AI can work with **claims**, rather than loose keywords.

---

# **9\. The evidence hierarchy**

We can establish something like this:

### **Level 1 — External/strong evidence**

Examples:

* Employment documentation  
* Certification  
* Public portfolio/GitHub  
* Candidate-provided project documentation

### **Level 2 — Candidate-confirmed evidence**

Candidate explicitly confirms:

> "Yes, I actually used FastAPI in this project."

### **Level 3 — Self-declared**

Candidate says:

> "I know FastAPI."

No supporting detail.

### **Level 4 — AI inference**

AI thinks:

> "Because you know Django, maybe you know Flask."

This should **never become a fact automatically.**

---

# **10\. How should the resume generator treat them?**

This is where we make the model safe.

### **🟢 Verified**

**Can use normally.**

Example:

> Developed REST APIs using FastAPI.

---

### **🔵 Candidate-confirmed**

**Can use**, but wording should remain faithful to what was confirmed.

Example:

> Worked with Docker in personal projects.

---

### **🟡 Self-declared**

Potentially usable, but we should ask the candidate for clarification before making a strong professional claim.

For example:

> "You listed Kubernetes as a skill. How did you use it?"

Candidate:

> "Only learned it through a course."

System updates the profile.

Now the resume shouldn't say:

> Kubernetes experience.

It might say:

> Kubernetes — Familiarity

depending on the candidate's actual background.

---

### **🔴 Unsupported**

**Never use.**

Even if the JD strongly wants it.

---

# **11\. The candidate should be able to correct the system**

Suppose AI extracts:

> "AWS — Professional experience"

Candidate says:

> ❌ That's wrong. I only completed an AWS course.

The system should allow:

**Correct**

↓

AWS

**Experience type:**

`Learning`

instead of:

`Professional`

This correction should affect future resumes too.

That's another advantage over a one-off ChatGPT prompt.

---

# **12\. We should also track the source**

Every important piece of information should have a source.

For example:

Skill: FastAPI

Status: Verified

Source:

Project: AI Document Q\&A

Evidence:

"Built REST APIs using FastAPI..."

Added by:

Candidate

Last confirmed:

September 2026

Or:

Skill: Kubernetes

Status: Unsupported

Source:

None

Reason:

Only appeared in JD

This is what gives us **traceability**.

---

# **13\. Now imagine the JD matching process**

JD says:

> Required: FastAPI, Docker, Kubernetes

Candidate profile says:

### **FastAPI**

🟢 Verified  
 Evidence: Company A

### **Docker**

🔵 Candidate-confirmed  
 Evidence: Personal Project

### **Kubernetes**

🔴 Unsupported

The system reports:

### **Job requirement analysis**

| Requirement | Status | Evidence |
| ----- | ----- | ----- |
| FastAPI | 🟢 Strong | Company A |
| Docker | 🔵 Confirmed | Personal Project |
| Kubernetes | 🔴 Missing | None |

This is much more meaningful than:

> ATS Match: 75%

---

# **14\. And this leads to a better scoring system**

Eventually we could have multiple dimensions rather than one magical score.

For example:

### **Requirement Match**

**82%**

How many important requirements are supported?

### **Evidence Strength**

**91%**

How much of the matched information is evidence-backed?

### **Resume Coverage**

**87%**

How much of the relevant candidate experience is represented?

### **Experience Fit**

**70%**

How closely does experience level match the JD?

That is much more useful than one generic "ATS score."

---

# **15\. One subtle but important issue: candidate confirmation ≠ factual verification**

We should be honest here.

If a candidate says:

> "I have 5 years of Kubernetes experience."

we can't necessarily know that's true.

So the system shouldn't claim:

> **"We verified that you have 5 years of Kubernetes experience."**

Instead:

> **"Candidate-confirmed."**

This distinction is critical if we ever make this a real product.

---

# **16\. Therefore, our terminology should be:**

I recommend these statuses:

### **🟢 Evidence-backed**

There is supporting information in the candidate's supplied materials.

### **🔵 Candidate-confirmed**

Candidate explicitly confirms the claim.

### **🟡 Self-declared**

Candidate has stated it but hasn't provided enough supporting context.

### **🔴 Unsupported**

There is no basis to make the claim.

And perhaps a fifth temporary state:

### **⚪ Needs clarification**

The system found ambiguous information and asks the candidate.

For example:

> "You mention 'cloud deployment.' Which platform?"

---

# **17\. The Golden Rule**

Now we can establish our most important product rule:

> ### **The AI can transform, organize, prioritize, and rephrase candidate information, but it cannot increase the factual strength of a claim without explicit candidate confirmation or supporting evidence.**

That's much stronger than:

> "Please don't hallucinate."

Because now the product has a defined data model and decision process behind it.

---

# **18\. Our "Truth Layer"**

So our product now has a conceptual component:

             CANDIDATE PROFILE

                     │

                     ▼

             ┌───────────────┐

             │  TRUTH LAYER  │

             └───────┬───────┘

                     │

        ┌────────────┼────────────┐

        ▼            ▼            ▼

   Evidence     Candidate     Confidence

                Confirmation

        │            │            │

        └────────────┼────────────┘

                     ▼

                  AI ENGINE

                     │

                     ▼

              Proposed Resume

                     │

                     ▼

               VALIDATION

                     │

              ┌──────┴──────┐

              ▼             ▼

           Allowed        Blocked

              │             │

              ▼             ▼

       Candidate Review   Unsupported

This is beginning to look like a **real system**, rather than a clever prompt.

---

# **One thing I would NOT do in the MVP**

I wouldn't require candidates to upload:

* employment letters  
* salary slips  
* certificates  
* government IDs  
* employer verification documents

That introduces **privacy, security, legal, and user-friction problems** very early.

For the MVP, evidence can simply come from:

* Existing resume  
* Candidate-entered profile  
* Projects  
* Portfolio/GitHub links  
* Candidate confirmations

Later, external verification can become an optional feature.

---

# **So our product foundation now looks like this**

                CANDIDATE

                     │

                     ▼

           VERIFIED CAREER PROFILE

                     │

                     ▼

              CAREER EVIDENCE

                     │

       ┌─────────────┼─────────────┐

       ▼             ▼             ▼

   Experience      Skills       Projects

       │             │             │

       └─────────────┼─────────────┘

                     ▼

              JOB DESCRIPTION

                     │

                     ▼

              JD REQUIREMENTS

                     │

                     ▼

            CANDIDATE ↔ JD MATCH

                     │

                     ▼

             TRUTHFUL OPTIMIZER

                     │

                     ▼

            VALIDATED RESUME

                     │

                     ▼

              CHANGE REVIEW

                     │

                     ▼

               APPROVAL

                     │

                     ▼

                 APPLY

And **now** I think we're ready for Step 5\.

# **Step 5 — Complete User Journey**

We'll design the actual experience from the moment a candidate opens the application:

**1\. Sign up**  
 → **2\. Build Career Profile**  
 → **3\. Import existing resume**  
 → **4\. Extract and classify information**  
 → **5\. Candidate verifies/corrects it**  
 → **6\. Paste/upload a JD**  
 → **7\. JD gets analyzed**  
 → **8\. Match \+ gap analysis**  
 → **9\. Resume optimization**  
 → **10\. Every change gets explained**  
 → **11\. Truth validation**  
 → **12\. Candidate approval**  
 → **13\. Generate final resume**  
 → **14\. Apply**  
 → **15\. Store application \+ resume version**

And we'll also identify **where the AI is used and where AI is explicitly NOT trusted** at each step.

That will give us the foundation we need before we finally move into the technical architecture.

Absolutely. Now we can move to **Step 5: Complete User Journey**.

This is where we take everything we've defined so far and ask:

> **"If I am a candidate using this product from beginning to end, what exactly happens?"**

I want to design this carefully because later our **database, APIs, AI components, frontend screens, and architecture** will all come from this workflow.

---

# **Step 5 — Complete User Journey**

At a high level:

Candidate  
   ↓  
Create Career Profile  
   ↓  
Import Existing Resume  
   ↓  
Review & Confirm Information  
   ↓  
Career Profile becomes Source of Truth  
   ↓  
Add Job Description  
   ↓  
Analyze Job  
   ↓  
Match Candidate ↔ Job  
   ↓  
Identify Gaps  
   ↓  
Optimize Resume  
   ↓  
Validate Changes  
   ↓  
Candidate Reviews Changes  
   ↓  
Approve  
   ↓  
Generate Job-Specific Resume  
   ↓  
Apply  
   ↓  
Save Application \+ Resume Version

Let's go through each stage.

---

# **5.1 Sign Up / Create Account**

The candidate creates an account.

At this stage we don't need to ask for everything.

We could simply collect:

* Name  
* Email  
* Password/login  
* Optional location

Then:

> **"Let's build your career profile."**

---

# **5.2 Create Career Profile**

This is the **heart of our product**.

Instead of treating the resume as the primary object, we're creating a persistent career profile.

The candidate can enter:

### **Personal Information**

* Name  
* Email  
* Phone  
* Location  
* LinkedIn  
* GitHub  
* Portfolio

### **Education**

* Degree  
* Institution  
* Field  
* Graduation date

### **Experience**

* Company  
* Job title  
* Start/end dates  
* Responsibilities  
* Achievements  
* Technologies used

### **Projects**

* Project name  
* Description  
* Technologies  
* Role  
* Outcomes

### **Skills**

* Programming languages  
* Frameworks  
* Databases  
* Cloud  
* Tools

### **Certifications**

* Certification  
* Issuer  
* Date

### **Achievements**

etc.

---

# **5.3 But We Don't Want Candidates to Enter Everything Manually**

This would create too much friction.

So we should allow:

> **Upload your existing resume**

For example:

resume.pdf

The system reads it and proposes:

### **Extracted Experience**

**ABC Technologies**

Python Developer

2024–Present

> Developed backend APIs using Python and FastAPI...

Candidate sees:

> **Is this information correct?**

✅ Yes  
 ✏️ Edit  
 ❌ Delete

---

# **5.4 This Is Where Our Truth Model Starts**

Suppose the system extracts:

> FastAPI

It shouldn't immediately assume:

> "Verified professional skill."

Instead it can say:

### **FastAPI**

**Found in:** ABC Technologies experience

**Status:** Evidence-backed

The candidate confirms:

> ✓ Confirm

Now that information becomes part of their trusted profile.

---

# **5.5 Candidate Profile After Verification**

We could conceptually have:

CAREER PROFILE

Python  
🟢 Evidence-backed  
Evidence: ABC Technologies

FastAPI  
🟢 Evidence-backed  
Evidence: ABC Technologies

PostgreSQL  
🟢 Evidence-backed  
Evidence: Project X

Docker  
🔵 Candidate-confirmed  
Evidence: Personal Project

AWS  
🟡 Self-declared  
No supporting evidence

Kubernetes  
🔴 Unsupported

The candidate can correct anything.

This is extremely important.

---

# **5.6 Candidate Adds a New Job**

Now the candidate finds:

> **Python Backend Developer**

They paste the JD.

Later, we could allow:

> Upload JD PDF

or:

> Job URL

But for the MVP, I'd start with:

### **Paste JD**

It's much simpler.

---

# **5.7 JD Analysis**

The system reads the JD and converts it into structured requirements.

Instead of treating the JD as one giant block of text, conceptually we want:

JOB

Title:  
Python Backend Developer

Experience:  
2+ years

Required Skills:  
Python  
FastAPI  
PostgreSQL  
REST APIs  
Docker

Preferred:  
AWS  
Kubernetes

Responsibilities:  
API development  
Database integration  
Testing  
Deployment

This gives us a structured representation of the job.

---

# **5.8 Candidate ↔ Job Matching**

Now the interesting part happens.

The system compares:

### **Job**

Python  
FastAPI  
PostgreSQL  
Docker  
AWS  
Kubernetes

against:

### **Candidate**

Python ✓  
FastAPI ✓  
PostgreSQL ✓  
Docker ✓  
AWS 🟡  
Kubernetes ✗

And produces something like:

### **Strong Match**

🟢 Python  
 🟢 FastAPI  
 🟢 PostgreSQL  
 🟢 Docker

### **Partial**

🟡 AWS

### **Missing**

🔴 Kubernetes

---

# **5.9 But We Should Go Beyond Skill Matching**

Suppose the JD says:

> "Build scalable REST APIs using Python/FastAPI."

Candidate profile:

> "Developed REST APIs using FastAPI for internal applications."

That's a strong semantic match even though the wording isn't identical.

So the system should understand:

> **Same concept, different wording.**

This is where AI/ML will become useful later.

---

# **5.10 Experience Matching**

Suppose:

### **JD**

> 3+ years experience

### **Candidate**

> 1.5 years professional experience

The system should explicitly show:

### **⚠️ Experience Gap**

> Required: 3+ years  
>  Candidate: 1.5 years

And importantly:

**It must not modify the candidate's resume to hide this gap.**

This is part of our truth principle.

---

# **5.11 Requirement Classification**

I'd also classify requirements.

For example:

### **🔴 Must Have**

Usually things like:

* Required technologies  
* Required years  
* Required degree  
* Required certification

### **🟡 Preferred**

Things like:

* Nice-to-have technologies  
* Optional experience

### **🔵 Contextual**

Things like:

* Communication  
* Problem solving  
* Teamwork

This helps determine what should receive the most attention in the resume.

---

# **5.12 Resume Optimization**

Now we finally generate a job-specific resume.

But remember:

> **We're not creating a new candidate.**

We're selecting and presenting the most relevant information.

For example, candidate has:

### **5 Projects**

1. AI Document Q\&A  
2. E-commerce API  
3. Image Classification  
4. Chat Application  
5. Portfolio Website

For a Python backend JD, perhaps:

**Prioritize:**

1. AI Document Q\&A  
2. E-commerce API  
3. Chat Application

And reduce emphasis on:

> Portfolio Website

That's legitimate optimization.

---

# **5.13 Keyword Optimization**

Suppose the candidate's profile says:

> "Built APIs."

JD says:

> "Develop RESTful APIs."

If the candidate actually built REST APIs, we can optimize the wording to:

> **"Developed RESTful APIs..."**

That's good.

But if the candidate only built GraphQL APIs?

Then we shouldn't convert it to REST.

---

# **5.14 Change Tracking**

This is one of our key differentiators.

Instead of silently generating the final resume, we show:

### **Change \#1**

**Original**

> Developed backend APIs using Python.

**New**

> Developed REST APIs using Python and FastAPI.

**Why?**

> JD specifically mentions REST APIs and FastAPI.

**Evidence**

> ABC Technologies — Backend Developer

---

### **Change \#2**

**Original**

> Worked on multiple projects.

**New**

> Developed an AI-powered document Q\&A system using Python and FastAPI.

**Why?**

> More directly demonstrates skills required by the JD.

**Evidence**

> AI Document Q\&A project.

---

# **5.15 Unsupported Information Gets Blocked**

Suppose AI wants to add:

> Kubernetes

The validation layer says:

Kubernetes  
    ↓  
Candidate profile  
    ↓  
No supporting claim  
    ↓  
BLOCK

Candidate sees:

### **❌ Not added**

> Kubernetes

**Reason:** No supporting candidate information.

This is a critical feature.

---

# **5.16 Candidate Approval**

Now the candidate reviews the proposed changes.

They can:

### **✓ Approve**

Accept the change.

### **✏️ Edit**

Modify the suggested wording.

### **❌ Reject**

Keep the original.

### **🚫 Reject & Remember**

Potentially useful later:

> "Don't use this wording again."

This could help personalize the candidate's preferences.

---

# **5.17 Generate Final Resume**

After approval:

> **Generate Resume**

The system creates the final job-specific version.

For example:

Riya Jogi  
Python Backend Developer

SUMMARY  
...

SKILLS  
Python | FastAPI | PostgreSQL | Docker | REST APIs

EXPERIENCE  
ABC Technologies  
...

PROJECTS  
AI Document Q\&A  
...

The important point:

> **Every statement in this resume can be traced back to the candidate profile.**

---

# **5.18 ATS / Job Compatibility Analysis**

Now we provide analysis.

But I'd avoid calling it simply:

> **"ATS Score: 93%"**

Instead, perhaps:

### **Job Alignment**

**88%**

### **Required Skills**

**5 / 6 supported**

### **Important Keywords**

**14 / 16 covered**

### **Experience**

**Partial match**

### **Education**

**Strong match**

### **Missing**

**Kubernetes**

And explain everything.

---

# **5.19 Candidate Makes Final Decision**

Now the candidate can choose:

### **Download**

Download the resume.

### **Apply**

Submit application.

### **Edit**

Go back.

### **Save**

Keep this resume version.

---

# **5.20 Application Record**

If they apply, we save:

Application

Company:  
ABC Technologies

Position:  
Python Backend Developer

Applied:  
September 13, 2026

Resume:  
Resume Version \#7

Match:  
88%

Important gaps:  
Kubernetes

Status:  
Applied

Now the candidate has a history.

---

# **5.21 Why This History Matters**

Suppose two weeks later they get an interview.

They can see:

> **Which resume did I send?**

And:

> **What did the resume say?**

They can prepare accordingly.

Eventually we could even provide:

> "Based on the resume you submitted, here are likely interview questions."

That becomes a future feature.

---

# **5.22 Multiple Jobs**

Now we see the power of the system.

Candidate profile:

            CAREER PROFILE  
                   │  
       ┌───────────┼───────────┐  
       ▼           ▼           ▼  
      JD1         JD2         JD3  
       │           │           │  
       ▼           ▼           ▼  
   Resume 1    Resume 2    Resume 3  
       │           │           │  
       ▼           ▼           ▼  
    Company A   Company B   Company C

One source of truth.

Many job-specific outputs.

---

# **5.23 What AI Does vs What the System Does**

This distinction will be **extremely important when we eventually build the architecture.**

### **AI can:**

* Understand JD  
* Extract requirements  
* Identify semantic similarities  
* Classify skills  
* Suggest wording  
* Rank relevant experiences  
* Generate resume content from approved information

### **System rules should control:**

* Candidate profile  
* Evidence  
* Permissions  
* Unsupported claims  
* Version history  
* Candidate approval  
* Application records

In other words:

> **LLM \= intelligence**

> **Application logic \= authority**

We should never let the LLM be the final authority over candidate truth.

---

# **5.24 The Complete Journey**

Putting everything together:

                        CANDIDATE  
                            │  
                            ▼  
                     Create Account  
                            │  
                            ▼  
                  Build Career Profile  
                            │  
                            ▼  
                    Upload Existing CV  
                            │  
                            ▼  
                    Extract Information  
                            │  
                            ▼  
                  Candidate Verification  
                            │  
                            ▼  
                 ┌─────────────────────┐  
                 │  SOURCE OF TRUTH    │  
                 │  CAREER PROFILE     │  
                 └──────────┬──────────┘  
                            │  
                            │  
                     New Job / JD  
                            │  
                            ▼  
                      Analyze JD  
                            │  
                            ▼  
                  Extract Requirements  
                            │  
                            ▼  
                Candidate ↔ Job Matching  
                            │  
                 ┌──────────┴──────────┐  
                 ▼                     ▼  
              Matches                 Gaps  
                 │                     │  
                 └──────────┬──────────┘  
                            ▼  
                    Resume Optimization  
                            │  
                            ▼  
                    Truth Validation  
                            │  
                 ┌──────────┴──────────┐  
                 ▼                     ▼  
              Allowed                Blocked  
                 │                  Unsupported  
                 ▼  
              Changes  
                 │  
                 ▼  
           Candidate Review  
                 │  
        ┌────────┼────────┐  
        ▼        ▼        ▼  
      Approve   Edit    Reject  
        │  
        ▼  
      Final Resume  
        │  
        ▼  
   Job Alignment Analysis  
        │  
        ▼  
      Candidate  
        │  
   ┌────┴─────┐  
   ▼          ▼  
 Download    Apply  
                │  
                ▼  
       Application Record  
                │  
                ▼  
          Resume Version  
---

# **One thing I want to change from our earlier thinking**

After mapping the journey, I think our **MVP should NOT start with auto-apply**.

The MVP should prove the most difficult and valuable part:

> **Can we reliably take a candidate's real career information \+ a JD and produce a more relevant resume without introducing unsupported claims?**

If we can prove that, the rest can be built around it.

---

# **Proposed MVP**

I'd define our first version as just **6 major capabilities**:

### **1\. Career Profile**

Candidate creates their structured profile.

### **2\. Resume Import**

Candidate uploads an existing resume and the system helps populate the profile.

### **3\. JD Analysis**

Paste a JD and get structured requirements.

### **4\. Candidate ↔ JD Match**

Show:

* Matches  
* Partial matches  
* Gaps  
* Experience mismatch  
* Important keywords

### **5\. Truthful Resume Optimization**

Generate a job-specific resume using only candidate-supported information.

### **6\. Change Review**

Show:

> Original → Proposed → Reason → Evidence

Candidate approves/rejects.

Then generate the final resume.

---

# **Features for Version 2**

After MVP:

* Resume version history  
* Application tracking  
* Job URL ingestion  
* Cover letters  
* Multiple resume templates  
* Better ATS analysis  
* Candidate preferences  
* Skill gap recommendations

---

# **Version 3**

Eventually:

* Job discovery  
* Auto-apply  
* Browser automation  
* Application form filling  
* Interview preparation  
* Interview question generation  
* Career recommendations  
* External verification  
* LinkedIn/GitHub integration

---

# **And now we have enough to discuss architecture**

We've gone from:

> **"I have an idea for an AI resume tool."**

to:

> **"I have a candidate-centric career intelligence system with a verified source of truth, evidence-backed claims, JD analysis, candidate-job matching, controlled AI generation, explainable changes, and candidate approval."**

That's a substantially stronger project.