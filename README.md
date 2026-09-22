# Reliance Digital Customer Support Agent

A simple, working web application that turns an existing Microsoft Foundry
AI agent into a polished customer support chat experience for Reliance
Digital — built as a university project.

## Overview

This project is **not** a new AI system. It is a thin, focused bridge
between a working Foundry agent and a clean chat interface:

```
User → Frontend (HTML/CSS/JS) → FastAPI Backend → Existing Foundry Agent
       ↑                                                    ↓
       └──────────────────── Response ─────────────────────┘
```

The existing Foundry agent (`Customer-Support-Agent`, model `gpt-5-mini`,
inside the `Universal-Customer-Support-Agent` project) already has its own
instructions, File Search, and real Reliance Digital policy documents
(return, warranty, cancellation, delivery) attached. This project does not
recreate, replace, or duplicate any of that — it only calls it.

## Features

- Chat interface with Reliance Digital branding
- Real-time responses grounded in real Reliance Digital policy documents
  via the agent's existing File Search
- Suggested question tiles for common queries (returns, warranty,
  cancellation, delivery)
- Loading indicator while waiting for a response
- Inline error handling with a retry option
- Multi-turn conversation memory (via conversation_id passed to the agent)
- "Clear conversation" to reset the chat
- Chat persistence — the current conversation survives a page refresh
  (stored in browser localStorage; not synced across devices)
- Responsive layout for desktop and mobile

## Tech Stack

- **Frontend:** Plain HTML, CSS, and vanilla JavaScript (no framework, no
  build step)
- **Backend:** Python, FastAPI
- **AI:** Microsoft Foundry Agent Service (existing agent, `gpt-5-mini`,
  called via `azure-ai-projects` v2.x using the Responses API)
- **Auth:** Azure `DefaultAzureCredential` (Azure CLI login for local
  development — no API keys used or stored)

## Project Structure

```
Customer_Support_Agent/
    backend/
        main.py            # FastAPI app: /api/chat, /api/health
        foundry.py         # Connects to the existing Foundry agent
        requirements.txt
        .env.example
    frontend/
        index.html
        style.css
        app.js
    README.md
```

## Prerequisites

- Python 3.10+
- An Azure account with access to the `Universal-Customer-Support-Agent`
  Foundry project (Azure AI Developer/User role)
- Azure CLI installed, and logged in via `az login`

## Setup

### 1. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your Foundry project details:

```
AZURE_AI_PROJECT_ENDPOINT=<your Foundry project endpoint>
FOUNDRY_AGENT_NAME=Customer-Support-Agent
FOUNDRY_MODEL_DEPLOYMENT_NAME=gpt-5-mini
```

Run the backend:

```bash
uvicorn main:app --reload --port 8080
```

Verify it's working by opening `http://localhost:8080/docs` and testing
`/api/health`.

### 2. Frontend

The frontend is plain static files — no build step required.

- Open `frontend/index.html` with a static file server (e.g. the "Go Live"
  extension in your editor, or any simple local static server)
- Make sure the base URL in `app.js` matches the port your backend is
  actually running on (default: `8080`)

Open the served URL in a browser. The backend must be running for the chat
to work.

## Environment Variables

| Variable | Description |
|---|---|
| `AZURE_AI_PROJECT_ENDPOINT` | Endpoint URL of the Foundry project |
| `FOUNDRY_AGENT_NAME` | Name of the existing agent (`Customer-Support-Agent`) |
| `FOUNDRY_MODEL_DEPLOYMENT_NAME` | Model deployment name (`gpt-5-mini`) |

No API keys are used. Authentication is handled via Azure
`DefaultAzureCredential`, which uses your local `az login` session in
development.

## API

### `GET /api/health`
Confirms the backend can reach the Foundry project and see the agent.

### `POST /api/chat`
```json
{
  "message": "What is the return policy?",
  "conversation_id": null
}
```
Returns:
```json
{
  "reply": "...",
  "conversation_id": "..."
}
```
Pass the returned `conversation_id` on subsequent calls to continue the
same conversation.

## Notes

- All policy answers come from real Reliance Digital documents already
  attached to the Foundry agent's File Search — no fake or placeholder
  policy data is used.
- The agent is designed to say when it cannot verify an answer rather than
  inventing a policy.
- This project intentionally does not include: authentication, a customer
  account system, an admin dashboard, ticket management, payment
  integration, or a database — kept simple by design for the scope of this
  project.