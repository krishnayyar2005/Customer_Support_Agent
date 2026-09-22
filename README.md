# Reliance Digital Customer Support Agent

University project — Phase 1 (backend only).

This backend is a thin FastAPI wrapper around an **existing** Microsoft
Azure AI Foundry agent called **Customer-Support-Agent**. The agent already
has its instructions, File Search tool, and Reliance Digital knowledge base
configured in the Foundry portal — this code simply relays user messages to
it and returns the responses.

## Project structure

```
backend/
    main.py            # FastAPI app — /api/chat and /api/health
    foundry.py         # Foundry SDK wrapper (AIProjectClient + Responses API)
    requirements.txt   # Python dependencies
    .env.example       # Environment variable template
```

## Quick start

### 1. Prerequisites

* Python 3.10+
* An Azure AI Foundry project with the **Customer-Support-Agent** agent
  already deployed and working in the Foundry Playground.
* Azure CLI logged in (`az login`) **or** a service principal configured.

### 2. Setup

```bash
cd backend

# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env        # Windows
# cp .env.example .env        # Linux/macOS
# Edit .env and fill in AZURE_AI_PROJECT_ENDPOINT
```

### 3. Run

```bash
uvicorn main:app --reload --port 8000
```

### 4. Test

```bash
# Health check
curl http://localhost:8000/api/health

# First message
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"What is the return policy?\"}"

# Follow-up (use the conversation_id from the response above)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"What about electronics specifically?\", \"conversation_id\": \"<id>\"}"
```

## Auth

By default the backend uses `DefaultAzureCredential`, which tries (in
order): environment variables, managed identity, Azure CLI, etc.

For local development the easiest option is:

```bash
az login
```

For CI/deployment, set `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, and
`AZURE_CLIENT_SECRET` as environment variables.

## What this is NOT

* No frontend yet (Phase 2).
* No custom tools (order lookup, etc.) yet.
* No web search fallback yet.
* No database, auth system, or admin dashboard.
