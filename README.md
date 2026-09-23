# Reliance Digital Customer Support Agent

An AI-powered customer support assistant for Reliance Digital that answers customer queries about returns, warranty, cancellations, delivery, and related support topics using real Reliance Digital policy documents.

## Team Members

| Name           | Student ID |
| -------------- | ---------: |
| Krrish Nayyar  | 2410992947 |
| Ramandeep      | 2410993373 |
| Mridul Chauhan | 2410993161 |
| Kunal Yadav    | 2410993051 |

## Project Overview

### Problem

Customers often need quick answers to common support questions such as:

* Return and refund policies
* Warranty information
* Order cancellation
* Delivery and shipping timelines
* Order or product-related information

Manually searching through policy documents can be slow and inconvenient.

### Solution

We developed a web-based AI customer support agent that combines:

* Microsoft Azure AI Foundry Agent Service
* `gpt-4.1-mini`
* Retrieval-Augmented Generation (RAG) using Foundry File Search
* Reliance Digital policy documents
* Supabase through a custom OpenAPI tool
* FastAPI backend
* HTML, CSS and Vanilla JavaScript frontend

The agent is designed to use the available knowledge sources and avoid generating unsupported policy information.

## Architecture

```text
User
 │
 ▼
Frontend
HTML / CSS / JavaScript
 │
 │ POST /api/chat
 ▼
FastAPI Backend
 │
 │ Azure AI Foundry SDK
 ▼
Azure AI Foundry Agent
(Customer-Support-Agent)
 │
 ├──────────────► File Search (RAG)
 │                Reliance Digital Policies
 │
 └──────────────► Supabase OpenAPI Tool
                  Structured Data
 │
 ▼
gpt-4.1-mini
 │
 ▼
Response → Backend → Frontend → User
```

## Request Flow

1. User enters a question in the frontend.
2. Frontend sends the message to `POST /api/chat`.
3. FastAPI forwards the request to the Azure AI Foundry agent.
4. The agent uses File Search or the configured Supabase tool when required.
5. `gpt-4.1-mini` generates the response.
6. Backend returns the response and conversation ID.
7. Frontend displays the response and stores conversation data locally.

## Technology Stack

| Layer          | Technology                                  |
| -------------- | ------------------------------------------- |
| Frontend       | HTML, CSS, Vanilla JavaScript               |
| Backend        | Python, FastAPI                             |
| AI Platform    | Microsoft Azure AI Foundry                  |
| AI Agent       | Azure AI Foundry Agent Service              |
| Model          | `gpt-4.1-mini`                              |
| RAG            | Foundry File Search                         |
| Knowledge Base | Reliance Digital policy documents           |
| Database       | Supabase                                    |
| Custom Tool    | OpenAPI                                     |
| SDK            | `azure-ai-projects`                         |
| Authentication | `azure-identity` / `DefaultAzureCredential` |
| Local Storage  | Browser `localStorage`                      |

## Project Structure

```text
Customer_Support_Agent-main/
│
├── README.md
├── DOCUMENTATION.md
│
├── backend/
│   ├── main.py
│   ├── foundry.py
│   ├── requirements.txt
│   ├── .env.example
│   └── .gitignore
│
└── frontend/
    ├── index.html
    ├── style.css
    ├── app.js
    └── server.js
```

## Azure AI Foundry Configuration

The project uses an existing Azure AI Foundry agent rather than creating a new model or RAG system from scratch.

**Foundry Project**

```text
Universal-Customer-Support-Agent
```

**Agent**

```text
Customer-Support-Agent
```

**Model**

```text
gpt-4.1-mini
```

### Knowledge Sources

The agent uses Reliance Digital documents through File Search, including:

* Return Policy
* Warranty Policy
* Cancellation Policy
* Delivery / Shipping Information

### Supabase Integration

A custom OpenAPI tool connects the Foundry agent with Supabase for configured structured-data lookups such as order and product information.

## How to Run

### Prerequisites

Install:

* Python 3.10+
* Node.js
* Azure CLI

Log in to Azure:

```bash
az login
```

### 1. Start Backend

Open a terminal:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create `backend/.env`:

```env
AZURE_AI_PROJECT_ENDPOINT=<your-foundry-project-endpoint>
FOUNDRY_AGENT_NAME=Customer-Support-Agent
FOUNDRY_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

Run:

```bash
uvicorn main:app --reload --port 8000
```

Backend:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

### 2. Start Frontend

Open a second terminal:

```bash
cd frontend
node server.js
```

Frontend:

```text
http://localhost:3000
```

Open the frontend in your browser and start chatting.

> Make sure `frontend/app.js` points to the backend URL:
>
> ```javascript
> const API_BASE_URL = "http://localhost:8000";
> ```

## API Endpoints

### `GET /api/health`

Checks backend and Foundry agent connectivity.

### `POST /api/chat`

Sends a user message to the AI agent.

Example:

```json
{
  "message": "What is the return policy?",
  "conversation_id": null
}
```

Response:

```json
{
  "reply": "The return policy information...",
  "conversation_id": "..."
}
```

The `conversation_id` is used for multi-turn conversations.

## Deployment

The application can be deployed as two parts:

* **Backend:** Python FastAPI application on a server or Azure App Service
* **Frontend:** Static HTML/CSS/JavaScript hosting such as Azure Static Web Apps, GitHub Pages, Netlify, or Vercel

For deployment, update the frontend API URL from:

```javascript
const API_BASE_URL = "http://localhost:8000";
```

to the deployed backend URL.

The backend environment variables must also be configured on the hosting platform.

For production, CORS should be restricted to the actual frontend domain instead of allowing all origins.

## Testing

The following flows were tested:

| Test                                  | Result |
| ------------------------------------- | ------ |
| Backend health check                  | Passed |
| Policy-based questions                | Passed |
| Unsupported questions                 | Passed |
| Multi-turn conversation               | Passed |
| Frontend error handling               | Passed |
| Chat persistence using `localStorage` | Passed |
| Responsive desktop/mobile layout      | Passed |

## Known Limitations

* Chat history is stored only in browser `localStorage`.
* There is currently no customer authentication/account system.
* Supabase data is limited to the configured demonstration data.
* There is no direct integration with Reliance Digital's private internal systems.
* Production deployment requires updating the frontend API URL.
* The current development CORS configuration should be restricted for production use.

## Future Improvements

* Customer authentication and user accounts
* Server-side conversation history
* Real order tracking integration
* More Reliance Digital knowledge documents
* Automated backend/frontend testing
* Production logging and monitoring
* Rate limiting and access control

## Documentation

Additional technical details are available in:

```text
DOCUMENTATION.md
```

This includes deeper information about the Foundry agent, File Search, Supabase integration, authentication, backend implementation, and frontend behavior.

## Acknowledgments

* **Microsoft Azure AI Foundry** — Agent Service and AI infrastructure
* **GPT-4.1-mini** — language model used by the agent
* **Azure AI Foundry File Search** — RAG and document retrieval
* **Supabase** — structured data storage
* **FastAPI** — backend framework
* **azure-ai-projects** — Azure AI Foundry SDK
* **azure-identity** — Azure authentication
* **Google Stitch** — frontend design workflow
* **Reliance Digital policy documents** — knowledge sources used by the application

## Disclaimer

This is an educational and demonstration project. It is not an official Reliance Digital customer-support system. Reliance Digital policy documents are used as publicly available knowledge sources for demonstration purposes.
