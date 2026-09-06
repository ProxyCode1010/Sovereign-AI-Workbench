# Sovereign AI Workbench
### Self-Hosted, Air-Gapped AI Assistant for Industrial & Government Organizations

**Project Documentation — v1.0**

---

## Table of Contents

1. [What This Project Is (Plain-Language Overview)](#1-what-this-project-is)
2. [The Problem It Solves](#2-the-problem-it-solves)
3. [How It Works — The Big Picture](#3-how-it-works--the-big-picture)
4. [System Architecture Diagram](#4-system-architecture-diagram)
5. [The Four Demo Capabilities](#5-the-four-demo-capabilities)
6. [Folder Structure](#6-folder-structure)
7. [File-by-File Explanation](#7-file-by-file-explanation)
8. [How Model Routing Works](#8-how-model-routing-works)
9. [How to Run the Project (Step-by-Step)](#9-how-to-run-the-project)
10. [How to Test Each Feature](#10-how-to-test-each-feature)
11. [Proving the "Air-Gapped" Claim](#11-proving-the-air-gapped-claim)
12. [Known Limitations](#12-known-limitations)
13. [Glossary of Terms](#13-glossary-of-terms)

---

## 1. What This Project Is

Imagine an assistant like ChatGPT or Claude — one that can read documents, write reports, generate code, and answer questions — but instead of running on someone else's computer over the internet, it runs **entirely on your own machine, inside your own building, with no internet connection required or allowed.**

Nothing you type, upload, or generate ever leaves the computer it's running on. No cloud company, no external server, and no internet service provider ever sees your data.

This matters enormously for organizations like refineries, defence manufacturers, and government offices, where the documents being worked on — engineering drawings, financial negotiations, inspection reports, internal strategy — are far too sensitive to risk uploading to a public AI tool, even accidentally.

**In one sentence:** This is a private, offline version of an AI assistant that can read scans, write documents, run code, and answer questions using only your organization's own data and your own computer's processing power.

---

## 2. The Problem It Solves

Large organizations generate enormous amounts of routine but sensitive paperwork every day:
- Approval notes for repairs and inspections
- Engineering calculations
- Board presentations and financial summaries
- Scanned inspection reports and handwritten notes
- Vendor negotiations and internal correspondence

Company policy usually **forbids** putting this kind of data into any public AI tool, because once it's typed into a cloud chatbot, the organization loses control over where that data goes. As a result, employees either:
- Do everything manually (slow, low productivity), **or**
- Secretly paste confidential material into public AI tools anyway (a serious security risk)

Neither option is acceptable. This project provides a third option: **a genuinely useful AI assistant that never sends a single byte of data outside the building.**

---

## 3. How It Works — The Big Picture

Think of the system as three cooperating parts, all running on the same computer:

| Part | What it does | Everyday analogy |
|---|---|---|
| **The Brain (AI Models)** | Reads text/images and generates answers, code, or documents | A team of specialist employees — one good at writing code, one good at reading scanned documents, one good at general writing |
| **The Memory (Database)** | Stores the organization's manuals, SOPs, and past reports so the AI can search them | A searchable filing cabinet |
| **The Hands (Tools)** | Lets the AI actually *do* things — run code safely, write Word documents, read PDFs | A set of office equipment the AI is allowed to use |

A person interacts with all of this through a simple webpage running in their browser. Behind that webpage, a "traffic controller" (the backend) decides which specialist AI model should handle each request, fetches any relevant company documents, and produces a final result — whether that's an answer, a piece of code, or a downloadable Word file.

Everything — the webpage, the AI models, the database, and the code-execution sandbox — runs inside isolated compartments called **containers** (via a technology called Docker), all on one physical machine, with no path out to the internet.

---

## 4. System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         YOUR COMPUTER                            │
│                    (no internet required)                        │
│                                                                   │
│   ┌───────────────┐                                              │
│   │   Browser     │   You interact here                          │
│   │  (index.html) │                                              │
│   └───────┬───────┘                                              │
│           │  (talks to)                                          │
│           ▼                                                      │
│   ┌───────────────────────────────────────────────────────┐      │
│   │              BACKEND  (sw_backend container)           │      │
│   │                                                         │      │
│   │   ┌───────────┐   ┌────────────┐   ┌────────────────┐  │      │
│   │   │  Router   │──▶│   Agent    │──▶│  Tools:        │  │      │
│   │   │ (picks    │   │ (plans &   │   │  - Sandbox     │  │      │
│   │   │  model)   │   │  executes) │   │  - Word/Excel  │  │      │
│   │   └───────────┘   └────────────┘   │  - OCR/Vision  │  │      │
│   │                                     │  - RAG search  │  │      │
│   │                                     └────────────────┘  │      │
│   └───────┬───────────────────────┬─────────────────────────┘     │
│           │                       │                                │
│           ▼                       ▼                                │
│   ┌───────────────┐      ┌─────────────────┐                       │
│   │    Ollama     │      │    Postgres      │                      │
│   │ (runs the AI  │      │  (pgvector DB —  │                      │
│   │   models)     │      │  stores manuals) │                      │
│   └───────────────┘      └─────────────────┘                       │
│                                                                     │
│           ┌──────────────────────────┐                             │
│           │   Sandbox container       │  (spun up per code task,   │
│           │  (runs generated code,    │   destroyed after)         │
│           │   NO network access)      │                            │
│           └──────────────────────────┘                             │
│                                                                     │
└─────────────────────────────────────────────────────────────────┘
              ▲
              │
        NO CONNECTION
        (network guard +
         Docker isolation
         block all outbound
         internet traffic)
```

---

## 5. The Four Demo Capabilities

The system is built to demonstrate four specific things, matching the original problem statement:

### 5.1 Grounded Question-Answering (RAG)
You ask a question like *"What is the SOP for valve isolation?"* The system searches only the organization's own uploaded manuals, finds the relevant passage, and answers using **only** that information — with the source document named, so answers can be verified and never invented.

### 5.2 Coding Agent with Verified Execution
You describe a task in plain English (e.g., "write a function to calculate pipe wall thickness"). The system writes real Python code, then **actually runs it** inside a locked-down, network-disabled sandbox to prove the code works — rather than just showing code and hoping it's correct.

### 5.3 Scanned Document Understanding (Vision + OCR)
You upload a photo or scan of an inspection report, engineering drawing, or handwritten note. The system reads the text (using OCR) and interprets the image (using a vision AI model), extracting genuine findings rather than guessing.

### 5.4 End-to-End Agentic Task
Combining all of the above: scan an inspection report → extract findings → draft a formal Word document approval note automatically, with no manual typing required.

---

## 6. Folder Structure

```
sovereign-workbench/
├── docker-compose.yml          <- Master file: defines all running services
├── .env                        <- Configuration values (model names, ports)
│
├── backend/                    <- All the "brain" and "traffic control" logic
│   ├── main.py                 <- Entry point; starts the web server
│   ├── config.py                <- Central settings (which models, which folders)
│   ├── model_router.py          <- Decides which AI model handles each request
│   ├── network_guard.py         <- Blocks any accidental internet connection
│   │
│   ├── agent/
│   │   ├── executor.py          <- Runs the actual end-to-end tasks
│   │   └── tools/                <- Individual "skills" the agent can use
│   │       ├── rag_search.py         (search company documents)
│   │       ├── vision_ocr.py         (read scanned images)
│   │       ├── code_sandbox.py       (run code safely)
│   │       ├── docx_writer.py        (create Word documents)
│   │       ├── xlsx_writer.py        (create Excel sheets)
│   │       ├── pptx_writer.py        (create PowerPoint slides)
│   │       └── file_tools.py         (read/write files)
│   │
│   ├── rag/
│   │   ├── db.py                 <- Talks to the document database
│   │   ├── embeddings.py         <- Converts text into searchable "fingerprints"
│   │   └── ingest.py             <- Loads company manuals into the database
│   │
│   ├── api/
│   │   └── routes.py             <- Defines the web addresses the app responds to
│   │
│   └── sandbox_runner/
│       └── Dockerfile.sandbox    <- Blueprint for the code-execution sandbox
│
├── frontend/
│   ├── index.html                <- The webpage layout you see and click on
│   └── app.js                    <- Makes the webpage interactive
│
├── data/
│   ├── uploads/                  <- Files you upload (scans, images)
│   ├── outputs/                  <- Generated files (Word docs, logs)
│   └── knowledge_base/           <- Company manuals/SOPs to be searched
│
└── scripts/
    └── init_db.sql               <- Sets up the database tables on first run
```

---

## 7. File-by-File Explanation

This section explains, in plain terms, what each important file actually does and why it exists.

### `docker-compose.yml`
The master control file. It tells the computer: "start a database, start the backend program, connect them together, and don't let them talk to the internet." Think of it as the building's floor plan — it defines which rooms exist and which doors connect them.

### `backend/main.py`
The very first thing that runs when the backend starts. Its job is small but critical: it turns on the "no internet" safety switch (`network_guard`) *before* anything else happens, then starts the web server that the browser talks to.

### `backend/config.py`
A single place listing all the adjustable settings — which AI model handles coding tasks, which handles general questions, where uploaded files are stored, and which network addresses are allowed. Changing behavior across the whole app usually means editing one line here.

### `backend/network_guard.py`
The security guard of the system. It intercepts every attempt the program makes to connect to *any* address, and only allows connections to the database and the AI model service — both of which live on the same machine. Any attempt to reach the outside internet is blocked and logged. This file is the technical proof behind the "air-gapped" claim.

### `backend/model_router.py`
The receptionist of the system. Every time a request comes in, this file decides: *"Is this a coding question, a request to read an image, or a general question?"* It does this in two stages:
1. **Fast check** — looks for obvious keywords ("write a function" → coding).
2. **Smart check** — if the fast check is unsure, it asks a small AI model to genuinely think about what the person is asking, before deciding.

Once decided, it sends the request to whichever specialist AI model is right for the job.

### `backend/agent/executor.py`
The project manager. This file contains the actual step-by-step logic for each of the four demo capabilities — for example, "given a scanned image, extract text, then summarize findings, then write a Word document." It calls on the router to pick models, and on the tools folder to actually perform actions.

### `backend/agent/tools/` (folder)
Each file here is one "skill" the AI is allowed to use, similar to giving an employee specific tools (a stapler, a calculator, a filing cabinet):
- **`rag_search.py`** — searches the company's own documents
- **`vision_ocr.py`** — reads text and interprets scanned images/photos
- **`code_sandbox.py`** — safely runs AI-generated code in an isolated container so it can't damage anything or access the internet
- **`docx_writer.py` / `xlsx_writer.py` / `pptx_writer.py`** — generate real Word, Excel, and PowerPoint files
- **`file_tools.py`** — basic reading and writing of files on disk

### `backend/rag/` (folder)
This is the "memory" system, formally called RAG (Retrieval-Augmented Generation):
- **`ingest.py`** — reads company manuals/SOPs and breaks them into small searchable chunks
- **`embeddings.py`** — converts each chunk of text into a numerical "fingerprint" that captures its meaning, so similar meanings can be found even if the exact words differ
- **`db.py`** — stores and searches those fingerprints in the database

### `backend/api/routes.py`
The switchboard. It defines the specific web addresses (like `/api/agent/code-task`) that the browser can call, and connects each one to the right function in `executor.py`.

### `backend/sandbox_runner/Dockerfile.sandbox`
The blueprint for a deliberately minimal, isolated mini-computer that gets created fresh every time AI-generated code needs to run. It has no internet access and is destroyed immediately after running the code, so nothing malicious or broken can persist or spread.

### `frontend/index.html` and `frontend/app.js`
The webpage. `index.html` is the visual layout (boxes, buttons, text areas). `app.js` is what makes clicking those buttons actually do something — it sends your request to the backend and displays the result, including a live "which AI model is handling this" indicator.

### `scripts/init_db.sql`
A one-time setup script that creates the database's storage structure (tables) the very first time the system starts, similar to setting up empty filing cabinets before any files are placed inside.

### `data/knowledge_base/`
This is where the organization's actual manuals, SOPs, and past correspondence live as plain text or PDF files. Anything placed here becomes searchable by the assistant. Nothing here is ever sent anywhere outside the machine.

### `data/outputs/`
Every generated deliverable — Word approval notes, log files — is saved here, ready to be opened or shared internally.

---

## 8. How Model Routing Works

The system uses **more than one AI model**, each specialized for a different kind of work, rather than one giant model trying to do everything (which would need far more computing power than a typical workstation has).

| If the request involves... | The system picks... | Because... |
|---|---|---|
| Writing, fixing, or debugging code | `qwen2.5-coder` (a coding-specialist model) | It's specifically trained to write good code |
| Reading a scanned image, photo, or drawing | `moondream` (a vision-capable model) | It's the only model that can "see" images at all |
| General questions, summaries, SOP lookups | `qwen2.5-instruct` (a general-purpose model) | It's better at natural conversation and factual answers |
| Any search of company documents | `nomic-embed-text` (an embedding model) | It converts your question into a searchable fingerprint first |

**How the decision is made**, step by step:
1. The system first checks for obvious signal words (e.g., "function," "script" → clearly a coding task).
2. If there's an image attached, it's automatically routed to the vision model — no guessing needed.
3. If neither of the above gives a clear answer, the system asks the general AI model itself to read the request and decide which category it belongs to — genuine reasoning, not just keyword-spotting.

This decision, and which method was used to make it, is shown live in the web interface for every request, so it's fully visible and auditable rather than hidden.

---

## 9. How to Run the Project

*(Assumes Docker Desktop and Ollama are already installed — see setup notes separately if not.)*

**Every day, to start the system:**
```
docker compose up -d
```
Wait about 10 seconds, then open `frontend/index.html` in a web browser.

**To check everything is running correctly:**
```
docker ps
```
You should see two containers running: `sw_postgres` and `sw_backend`.

**To stop the system at the end of the day:**
```
docker compose down
```
No data is lost — all uploaded files, generated documents, and the document database remain safely stored on disk.

---

## 10. How to Test Each Feature

| Feature | What to do | What you should see |
|---|---|---|
| **Ask the knowledge base** | Type a question like *"What is the SOP for valve isolation?"* and click Ask | A detailed, accurate answer with the source document named below it |
| **Coding agent** | Type a task like *"write a function to calculate X"* and click Run | Generated code, followed by proof it actually ran successfully (or an honest error if it didn't) |
| **Scanned document → approval note** | Upload an inspection report image, then click Generate | A list of extracted findings, a recommendation, and a downloadable Word file |

---

## 11. Proving the "Air-Gapped" Claim

This is the most important thing to demonstrate to any evaluator, since claiming "no data leaves the building" is only meaningful if it can be shown, not just stated.

**Three ways to prove it live:**

1. **Show the audit log** — every connection attempt the backend makes is recorded. Only connections to the database and the AI model service (both on the same machine) will ever appear; anything else is blocked and clearly logged as "BLOCKED."

2. **Attempt a deliberate outside connection** — running a command that tries to reach a real internet address (like google.com) from inside the backend will fail instantly with an error explicitly stating the connection was refused for air-gap reasons.

3. **Docker network settings** — the technical configuration itself can be inspected to show the network the system runs on has no route to the outside internet at all, at the infrastructure level — not just something the application chooses not to do, but something it structurally cannot do.

---

## 12. Known Limitations

Being transparent about current limitations is important, both for honesty and because it shows a mature understanding of the system's boundaries:

- **Small AI models are less capable than large cloud AI systems.** They can occasionally make mistakes on highly specialized engineering formulas or produce inconsistent answers to the same question. This is a deliberate tradeoff to allow the system to run on modest, affordable hardware rather than requiring expensive cloud-scale computers.
- **The vision model is best at describing images generally**, but for documents with clean, readable text, the system relies more on direct text extraction (OCR) for accuracy, only falling back to the vision model's interpretation when no readable text is found.
- **Retrieval quality depends on how much material has been added** to the knowledge base — the more manuals and SOPs ingested, the better and more specific the answers become.

---

## 13. Glossary of Terms

| Term | Plain-language meaning |
|---|---|
| **Air-gapped** | Physically or logically disconnected from the internet — no path in or out |
| **Docker / Container** | A way of running a program in its own sealed compartment, isolated from everything else on the computer |
| **RAG (Retrieval-Augmented Generation)** | Letting an AI search your own documents first, then answer based only on what it found, instead of guessing from memory |
| **Embedding** | Converting a piece of text into a list of numbers that represents its meaning, so a computer can compare how similar two pieces of text are |
| **Sandbox** | A safe, isolated, temporary environment where code can be run without any risk of it affecting the rest of the system |
| **OCR (Optical Character Recognition)** | Technology that reads text out of an image or scanned document |
| **Vision model** | An AI model that can look at and describe or interpret images, not just text |
| **Model routing** | Automatically deciding which specialized AI model should handle a given request |
| **Ollama** | The software used to run AI models locally on a computer, without needing the internet |
| **Postgres / pgvector** | The database technology used to store and search the organization's documents |

---

*End of Documentation.*
