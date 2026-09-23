# Reliance Digital Customer Support Agent

## Team Members
<!-- TODO: Add your name(s) and roll number(s)/student ID(s) here -->
- [Your Name]

## Problem Statement and Solution Overview

**Problem:** Customers of Reliance Digital need quick, accurate answers to
common support questions — returns, warranty, cancellations, and delivery
timelines — without waiting for a human agent or manually searching
through policy documents.

**Solution:** A web-based AI customer support chat assistant that answers
customer questions using Reliance Digital's real policy documents. The
assistant is built on Microsoft Foundry's Agent Service, using Retrieval-
Augmented Generation (RAG) via File Search over real, downloaded Reliance
Digital policy PDFs (return policy, warranty policy, cancellation policy,
delivery/shipping information). The agent answers strictly from these
documents where possible, and is designed to say when it cannot verify an
answer rather than inventing information.

This project does not build a new AI model or a new RAG pipeline from
scratch — it uses an existing, already-configured Foundry agent, and
focuses on building a working application (backend + frontend) around it.

## Solution Architecture / Data Flow

```
 ┌────────────┐      HTTP (fetch)      ┌───────────────┐      Foundry SDK      ┌──────────────────────────┐
 │  Frontend  │ ───────────────────▶  │ FastAPI Backend│ ───────────────────▶ │ Existing Foundry Agent    │
 │ (HTML/CSS/ │  POST /api/chat        │   (main.py,     │  responses.create()  │ "Customer-Support-Agent"  │
 │  vanilla   │ ◀───────────────────  │   foundry.py)   │ ◀─────────────────── │ + File Search (real docs) │
 │    JS)     │      JSON reply        └───────────────┘      JSON response    └──────────────────────────┘
 └────────────┘
```

**Flow of a request:**
1. User types a question or clicks a suggested question in the browser.
2. Frontend sends `POST /api/chat` with the message and the current
   `conversation_id` (or `null` for a new conversation).
3. FastAPI backend authenticates to Azure (via `DefaultAzureCredential`)
   and forwards the message to the existing Foundry agent using the
   Responses API, referencing the agent by name.
4. The Foundry agent searches its attached Reliance Digital documents
   (File Search / RAG) to find a grounded answer. If the answer isn't in
   the documents, it says so rather than fabricating a policy.
5. The backend returns the agent's reply and a `conversation_id` to the
   frontend.
6. The frontend displays the reply and stores the `conversation_id` so
   follow-up messages keep context (multi-turn conversation).
7. The current conversation is also saved to the browser's `localStorage`
   so it survives a page refresh.

## Technology Stack and AI Services/Models Used

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, vanilla JavaScript (no framework, no build step) |
| Backend | Python, FastAPI |
| AI Platform | Microsoft Azure AI Foundry — Agent Service |
| Model | `gpt-5-mini` |
| Retrieval (RAG) | Foundry File Search, over real Reliance Digital policy PDFs |
| SDK | `azure-ai-projects` (v2.x, Responses API) |
| Authentication | `azure-identity` — `DefaultAzureCredential` (Azure CLI login for local dev; no API keys stored) |

## Setup Instructions

### Prerequisites
- Python 3.10+
- Azure account with access to the Foundry project (`Universal-Customer-
  Support-Agent`), with the Azure AI Developer/User role
- Azure CLI installed and logged in (`az login`)

### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```
Copy `.env.example` to `.env` and fill in:
```
AZURE_AI_PROJECT_ENDPOINT=<your Foundry project endpoint>
FOUNDRY_AGENT_NAME=Customer-Support-Agent
FOUNDRY_MODEL_DEPLOYMENT_NAME=gpt-5-mini
```
Run:
```bash
uvicorn main:app --reload --port 8080
```
Verify at `http://localhost:8080/docs`.

### Frontend
No build step — plain static files.
- Serve `frontend/index.html` with any static file server (e.g. the "Go
  Live" extension), with the backend already running.
- Confirm the base API URL in `app.js` matches your backend's port.

## Testing and Results

Manual end-to-end testing was performed for each core flow:

| Test | Result |
|---|---|
| `GET /api/health` reaches the Foundry agent | Passed — confirms agent connectivity |
| Ask a question answered by the documents (e.g. return policy) | Passed — agent answers correctly, grounded in real policy documents, matching Foundry Playground output |
| Ask a question not covered by the documents | Passed — agent states it cannot verify the information rather than inventing an answer |
| Multi-turn conversation (follow-up question using `conversation_id`) | Passed — agent retains context across turns |
| Error handling (backend unreachable) | Passed — frontend shows an inline error with a retry option |
| Chat persistence across page refresh | Passed — conversation restored from `localStorage` |
| Responsive layout (desktop and mobile widths, ~375–414px) | Passed — layout adapts correctly, no overflow |

<!-- TODO: consider adding 1–2 screenshots of the working app here for your submission -->

## Known Limitations and Future Improvements

**Limitations:**
- Chat history is stored only in the browser's `localStorage`, so it is
  local to one device/browser and is lost if browser storage is cleared.
- No user accounts — each browser session is anonymous, so there's no way
  to track a specific customer's order/support history.
- Custom demonstration tools (e.g. order lookup) use hardcoded sample data
  rather than a real Reliance Digital backend system, since there is no
  access to real internal systems.
- Web search fallback (for questions outside the document set) depends on
  Foundry's supported web-search capability being enabled on the agent; if
  disabled, out-of-scope questions will only receive the "cannot verify"
  response rather than a web-grounded one.

**Future Improvements:**
- Add a persistent, server-side chat history tied to a real user account
  system.
- Expand the Reliance Digital knowledge base with more policy documents as
  they become available.
- Add richer custom tools (e.g. real order tracking) if integrated with
  real backend systems.
- Add automated tests (e.g. pytest for the backend endpoints) rather than
  relying solely on manual testing.

## Acknowledgments

- **Microsoft Azure AI Foundry** — Agent Service, File Search, and hosting
  for the underlying AI agent and model (`gpt-5-mini`).
- **FastAPI** — Python web framework used for the backend.
- **azure-ai-projects** and **azure-identity** — official Microsoft Python
  SDKs used to connect to the Foundry agent and authenticate.
- Reliance Digital policy documents (Return Policy, Warranty Policy,
  Cancellation Policy, Delivery/Shipping information) used as the
  knowledge source — real, publicly available Reliance Digital documents,
  used here for educational/demonstration purposes only.
