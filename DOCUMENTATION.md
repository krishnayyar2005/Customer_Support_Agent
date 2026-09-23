# Technical Documentation — Reliance Digital Customer Support Agent

This document is a deeper technical companion to `README.md`. It covers
how the project was actually built, end to end: the Foundry agent
configuration, guardrails, the Supabase-backed custom tool, the backend
bridge, the frontend, and the design workflow via Stitch.

---

## 1. Microsoft Foundry Setup

### 1.1 Project and Agent
- **Foundry project:** `Universal-Customer-Support-Agent`
- **Agent:** `Customer-Support-Agent`
- **Model:** `gpt-5-mini`

The agent was created and configured directly in the Foundry portal
(Playground), not through code. This project's backend/frontend only
*calls* this existing agent — it does not create, retrain, or duplicate it.

### 1.2 Instructions Given to the Agent
The agent was configured in Foundry with system instructions establishing
its role and behavior as a Reliance Digital customer support assistant.
At a high level, the instructions direct the agent to:
- Act as an official Reliance Digital customer support assistant.
- Answer customer questions about returns, warranty, cancellations, and
  delivery using the attached knowledge sources.
- Prefer information from Reliance Digital's own documents over general
  knowledge.
- Never invent or guess a Reliance Digital policy that isn't supported by
  the available knowledge sources.
- Clearly distinguish between information sourced from the internal
  documents versus any other source.
- State that information could not be verified when neither the documents
  nor other available sources can answer a question.

### 1.3 Knowledge Source — File Search (RAG)
The agent has **File Search** enabled, pointed at real, downloaded
Reliance Digital policy documents:
- Return Policy
- Warranty Policy
- Cancellation Policy
- Shipping/Delivery information

These are genuine documents, not synthetic/placeholder data. This is the
agent's Retrieval-Augmented Generation (RAG) layer — when a user asks a
policy question, the agent searches these documents first and grounds its
answer in them.

### 1.4 Guardrails
Guardrails are enforced primarily through the agent's system instructions
(Section 1.2) rather than external code:
- **No policy invention:** the agent is instructed never to state a
  Reliance Digital policy unless it is supported by File Search results.
- **Source transparency:** the agent is instructed to distinguish between
  document-grounded answers and any other source of information.
- **Graceful uncertainty:** when no reliable source can answer a question,
  the agent says so explicitly rather than guessing.
- These guardrails live entirely inside the Foundry agent configuration —
  the FastAPI backend does not add its own separate content-filtering
  layer, it simply relays the agent's already-governed responses.

### 1.5 Custom Tool — Supabase (via OpenAPI)
A custom tool was added to the agent in the Foundry portal to let it query
live structured data (e.g. order/product records) stored in **Supabase**,
separate from the static policy documents in File Search.

**How it was set up:**
1. In the Foundry agent configuration, opened **Tools**.
2. Selected **Add tool → Custom tool → OpenAPI**.
3. Provided the Supabase project's REST API (Supabase auto-generates an
   OpenAPI-compatible REST interface over its Postgres tables) as the
   OpenAPI specification for the tool.
4. Foundry parses this spec and exposes the relevant Supabase endpoints to
   the agent as callable tool functions.

**What this enables:** during a conversation, if a user asks something
that requires live structured data (e.g. checking a record stored in
Supabase) rather than a static policy answer, the agent can call this tool
directly, get a real response from Supabase, and use it to answer — in
addition to, not instead of, the File Search policy documents.

This keeps the two knowledge sources cleanly separated:
| Source | Used for |
|---|---|
| File Search (documents) | Static policy questions (returns, warranty, cancellation, delivery terms) |
| Supabase (custom OpenAPI tool) | Live/structured record lookups |

---

## 2. Backend (FastAPI Bridge)

### 2.1 Purpose
The backend does not contain any AI logic itself. It is a thin bridge:
receive a chat message from the frontend → forward it to the existing
Foundry agent → return the agent's response. All RAG, guardrails, and tool
calling (including the Supabase custom tool) happen inside Foundry, not in
this code.

### 2.2 Key Files
- `main.py` — FastAPI app, exposes `POST /api/chat` and `GET /api/health`,
  configures CORS
- `foundry.py` — connects to the Foundry project using
  `AIProjectClient`, retrieves the existing agent by name, and sends
  messages via the Responses API (`openai_client.responses.create(...)`
  with `extra_body={"agent": {"name": ..., "type": "agent_reference"}}`)

### 2.3 Authentication
Uses `azure-identity`'s `DefaultAzureCredential`, which in local
development uses the developer's `az login` session. No API keys or
secrets are stored in code or committed to the repository — Azure/Foundry
config values (project endpoint, agent name, model name) are read from
environment variables via a `.env` file (excluded from git).

### 2.4 Conversation Continuity
Each chat request can include a `conversation_id`. On the first message it
is `null`, and the backend/agent create a new conversation; the returned
`conversation_id` is then reused by the frontend on every following
message so the agent retains multi-turn context.

### 2.5 CORS
Configured to allow requests from the frontend's local origin during
development (`allow_origins=["*"]` for local dev, since there is no
sensitive cookie/session data — `allow_credentials=False` accordingly).

---

## 3. Frontend

### 3.1 Technology
Built in plain HTML, CSS, and vanilla JavaScript — no framework, no build
step. This was a deliberate simplification after an initial React/Vite
version proved harder to preview with simple static-file tools; plain
HTML/CSS/JS runs directly with any static file server with zero
compilation.

### 3.2 Design Workflow — Stitch via MCP
The visual design was created in **Google Stitch**, an AI UI design tool,
based on a detailed design brief (Reliance Digital branding, chat layout,
suggested questions, loading/error states — deliberately avoiding generic
"AI-generated" visual clichés like glassmorphism/gradients in favor of a
flatter, more intentional style).

Stitch was connected to the Antigravity IDE as an **MCP (Model Context
Protocol) server**. This allowed Antigravity to:
- Pull the generated Stitch design directly into the coding environment
- Use it as the literal implementation spec when building the HTML/CSS,
  rather than the developer manually re-describing or screenshotting the
  design

This MCP connection is what let the build step ("implement this Stitch
design as a working one-to-one frontend") happen directly inside
Antigravity, referencing the live design rather than a static export.

### 3.3 Key Files
- `index.html` — page structure
- `style.css` — styling, including Reliance Digital brand colors, layout,
  and responsive breakpoints for mobile
- `app.js` — all interactivity: sending messages, rendering chat bubbles,
  handling loading/error states, calling the backend via `fetch()`,
  localStorage persistence

### 3.4 Core Frontend Behavior
- On load: restores any saved conversation from `localStorage`, or shows
  the empty state with 4 suggested question tiles
- Sending a message (via typed input, Enter key, or a suggested-question
  click) immediately renders the user's message, shows a loading
  indicator, calls `POST /api/chat`, then renders the real reply
- Errors from the backend are shown inline with a retry action
- "Clear conversation" resets both the visible chat and the saved
  `localStorage` state
- Layout is responsive: suggested-question grid collapses to a single
  column on mobile widths, header remains usable at narrow widths

### 3.5 Persistence
The current conversation (messages + `conversation_id`) is saved to the
browser's `localStorage` after each update, so a page refresh restores the
same conversation rather than resetting it. This is local-only (per
browser/device) — there is no server-side or account-based history.

---

## 4. Data Flow Summary

```
User types/selects a question
        │
        ▼
Frontend (fetch POST /api/chat)
        │
        ▼
FastAPI backend (auth via DefaultAzureCredential)
        │
        ▼
Foundry Agent "Customer-Support-Agent" (gpt-5-mini)
        │
        ├──▶ File Search over real Reliance Digital policy documents
        │        (returns / warranty / cancellation / delivery)
        │
        └──▶ Custom OpenAPI tool → Supabase
                 (live structured data lookups, when relevant)
        │
        ▼
Agent composes a grounded response
 (or states it cannot verify the answer)
        │
        ▼
Backend returns { reply, conversation_id }
        │
        ▼
Frontend renders the reply, saves state to localStorage
```

---

## 5. Development Notes and Issues Resolved

For transparency, a few real issues were hit and fixed during development:
- **Windows venv/permission errors** caused by developing inside a
  OneDrive-synced folder — resolved by understanding OneDrive was locking
  files during venv creation; recommended fix is developing outside
  OneDrive-synced paths.
- **PowerShell execution policy** blocked running `activate.ps1` — fixed
  with `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy
  RemoteSigned`.
- **CORS blocking all frontend requests** after moving from the React dev
  server to a static file server on a different port — fixed by updating
  the backend's `allow_origins` configuration.
- **Duplicate message sends** caused by a send handler firing from
  multiple bound events — fixed by consolidating the send logic and adding
  an in-flight guard.
- **Cramped, non-responsive layout** in the initial build — fixed with a
  consistent spacing scale, proper full-width header layout, and mobile
  breakpoints.

---

## 6. Acknowledgments / Third-Party Resources

- **Microsoft Azure AI Foundry** — Agent Service, File Search (RAG), and
  custom tool (OpenAPI) support
- **`gpt-5-mini`** — underlying language model, via Foundry
- **FastAPI** — backend web framework
- **`azure-ai-projects`, `azure-identity`** — official Microsoft SDKs for
  connecting to and authenticating with the Foundry project
- **Supabase** — hosted Postgres database with an auto-generated REST/
  OpenAPI interface, used as a custom tool data source for the agent
- **Google Stitch** — AI UI design tool used to generate the frontend
  visual design, connected via MCP into the Antigravity IDE
- **Antigravity IDE** — used to implement, run, and self-test both the
  backend and frontend code
- Reliance Digital policy documents (Return, Warranty, Cancellation,
  Delivery) — real, publicly available documents used as the RAG
  knowledge source, for educational/demonstration purposes only
