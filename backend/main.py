from __future__ import annotations

"""
main.py — FastAPI backend for the Reliance Digital Customer Support Agent.

Exposes:
    POST /api/chat    — send a message to the Foundry agent
    GET  /api/health  — verify Foundry connectivity + agent exists
"""

import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import foundry

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

load_dotenv()  # reads .env from the working directory

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Lifespan — initialise / tear down Foundry client
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(_app: FastAPI):
    foundry.init()
    logger.info("Foundry client ready.")
    yield
    logger.info("Shutting down.")


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Reliance Digital Customer Support Agent — Backend",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    # Allow all origins for local development since there are no sensitive session cookies involved
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    conversation_id: str


class HealthResponse(BaseModel):
    status: str
    agent_name: str
    agent_id: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/api/health", response_model=HealthResponse)
async def health():
    """Check Foundry connectivity and confirm the agent is reachable."""
    try:
        info = foundry.check_health()
        return HealthResponse(**info)
    except Exception as exc:
        logger.exception("Health check failed")
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Send a user message to the Foundry agent and return the reply."""
    if not req.message.strip():
        raise HTTPException(status_code=422, detail="Message must not be empty.")
    try:
        result = foundry.send_message(
            message=req.message,
            conversation_id=req.conversation_id,
        )
        return ChatResponse(**result)
    except Exception as exc:
        logger.exception("Chat request failed")
        raise HTTPException(status_code=502, detail=str(exc)) from exc
