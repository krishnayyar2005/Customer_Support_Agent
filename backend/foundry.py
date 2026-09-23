from __future__ import annotations

"""
foundry.py — Thin wrapper around the existing Azure AI Foundry agent.

Connects to the Foundry project, verifies the agent exists, and exposes
a send_message() function that relays user messages to the agent and
returns the response text + a conversation handle (previous_response_id).
"""

import os
import logging

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Module-level singletons (initialised lazily via init())
# ---------------------------------------------------------------------------
_project_client: AIProjectClient | None = None
_openai_client = None  # openai-compatible client from Foundry
_agent_name: str = ""
_model_deployment: str = ""


def init() -> None:
    """
    Initialise the Foundry project client and OpenAI-compatible client.
    Must be called once at startup (e.g. in a FastAPI lifespan handler).
    """
    global _project_client, _openai_client, _agent_name, _model_deployment

    endpoint = os.environ.get("AZURE_AI_PROJECT_ENDPOINT", "")
    if not endpoint:
        raise RuntimeError(
            "AZURE_AI_PROJECT_ENDPOINT is not set. "
            "Copy .env.example to .env and fill in the project endpoint."
        )

    _agent_name = os.environ.get("FOUNDRY_AGENT_NAME", "Customer-Support-Agent")
    _model_deployment = os.environ.get("FOUNDRY_MODEL_DEPLOYMENT_NAME", "gpt-5-mini")

    # DefaultAzureCredential automatically uses the developer's 'az login' session locally, avoiding hardcoded secrets
    credential = DefaultAzureCredential()

    _project_client = AIProjectClient(
        endpoint=endpoint,
        credential=credential,
    )

    _openai_client = _project_client.get_openai_client()

    logger.info(
        "Foundry client initialised — endpoint=%s  agent=%s  model=%s",
        endpoint, _agent_name, _model_deployment,
    )


# ---------------------------------------------------------------------------
# Health check — verifies the agent exists without sending a chat message
# ---------------------------------------------------------------------------

def check_health() -> dict:
    """
    Verify that the Foundry project is reachable and the agent exists.
    Returns a dict with status info; raises on failure.
    """
    if _project_client is None:
        raise RuntimeError("Foundry client not initialised — call init() first.")

    agent = _project_client.agents.get(_agent_name)
    if agent is None:
        raise RuntimeError(
            f"Agent '{_agent_name}' not found in the Foundry project. "
            "Check FOUNDRY_AGENT_NAME in your .env file."
        )

    return {
        "status": "ok",
        "agent_name": agent.name,
        "agent_id": getattr(agent, "id", "unknown"),
    }


# ---------------------------------------------------------------------------
# Chat — relay a message to the existing Foundry agent
# ---------------------------------------------------------------------------

def send_message(message: str, conversation_id: str | None = None) -> dict:
    """
    Send *message* to the Foundry agent.

    Parameters
    ----------
    message : str
        The user's message.
    conversation_id : str | None
        The ``response.id`` from a previous turn (used as
        ``previous_response_id`` to maintain multi-turn context).
        Pass None for the first message in a new conversation.

    Returns
    -------
    dict with keys:
        reply            – the agent's text response
        conversation_id  – the response id to pass back on the next turn
    """
    if _openai_client is None:
        raise RuntimeError("Foundry client not initialised — call init() first.")

    kwargs: dict = {
        "model": _model_deployment,
        "input": message,
        "extra_body": {
            # Route the request to the pre-configured Foundry agent by name, rather than redefining instructions here
            "agent_reference": {
                "name": _agent_name,
                "type": "agent_reference",
            }
        },
    }

    if conversation_id is not None:
        # Pass the previous response ID back so Foundry maintains multi-turn conversation history
        kwargs["previous_response_id"] = conversation_id

    try:
        response = _openai_client.responses.create(**kwargs)
        reply = getattr(response, "output_text", None) or "I'm sorry, I couldn't generate a response."
        conv_id = getattr(response, "id", conversation_id or "fallback-id")
    except Exception as exc:
        logger.error("FOUNDRY CALL FAILED: %s: %s", type(exc).__name__, str(exc), exc_info=True)
        reply = f"[DEBUG] {type(exc).__name__}: {str(exc)}"
        conv_id = conversation_id or "fallback-id"

    return {
        "reply": reply,
        "conversation_id": conv_id,
    }
