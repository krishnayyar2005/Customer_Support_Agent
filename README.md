# Reliance Digital Customer Support Agent

An AI-powered customer support assistant for Reliance Digital that provides policy-based answers for returns, warranty, cancellations, deliveries, and related customer queries.

The application uses Microsoft Azure AI Foundry Agent Service as the AI layer, with File Search (RAG) over Reliance Digital policy documents and a custom Supabase OpenAPI tool for structured data lookups. A FastAPI backend connects the web interface to the existing Foundry agent.

---

## Team Members

| Name           | Student ID |
| -------------- | ---------: |
| Krrish Nayyar  | 2410992947 |
| Ramandeep      | 2410993373 |
| Mridul Chauhan | 2410993161 |
| Kunal Yadav    | 2410993051 |

---

## 1. Project Overview

### Problem Statement

Customers often need quick answers to questions such as:

* What is the return policy?
* How does the warranty work?
* Can an order be cancelled?
* What are the delivery timelines?
* Can a specific order or product record be checked?

Searching through policy documents manually can be slow and inconvenient, especially when customers need an immediate response.

### Proposed Solution

The Reliance Digital Customer Support Agent is a web-based AI assistant that provides conversational customer support.

The system combines:

* Microsoft Azure AI Foundry Agent Service
* `gpt-4.1-mini`
* File Search for Retrieval-Augmented Generation (RAG)
* Reliance Digital policy documents
* Supabase through a custom OpenAPI tool
* FastAPI backend
* HTML, CSS and vanilla JavaScript frontend

The application is designed to prefer information from the configured Reliance Digital knowledge sources and avoid inventing unsupported company policies.

---

## 2. Key Features

### AI Customer Support

Users can ask questions in natural language and receive conversational responses.

### Retrieval-Augmented Generation

The Foundry agent uses File Search to retrieve relevant information from Reliance Digital policy documents before generating an answer.

The current document-based knowledge covers areas such as:

* Return policy
* Warranty policy
* Cancellation policy
* Delivery and shipping information

### Supabase Data Lookup

The Foundry agent also has access to a custom OpenAPI tool connected to Supabase.

This can be used for structured data such as:

* Order records
* Product records
* Other configured customer-support data

This tool is configured inside Azure AI Foundry and is not implemented directly in the FastAPI code.

### Multi-Turn Conversations

The application preserves conversation context using the response ID returned by the Foundry Responses API.

The frontend sends the previous conversation ID with follow-up messages so that the agent can continue the same conversation.

### Local Chat Persistence

The frontend stores the current conversation in browser `localStorage`.

This allows the conversation to remain available after refreshing the page.

### Suggested Questions

The user interface provides predefined questions for common support scenarios, allowing users to start a conversation quickly.

### Responsive Interface

The frontend is built to work on both desktop and mobile screen sizes.

### Error Handling

The frontend displays an inline error message and retry option if the backend cannot be reached.

---

## 3. System Architecture

```text
                    USER
                     │
                     ▼
          ┌──────────────────────┐
          │      Frontend        │
          │ HTML + CSS + JS      │
          │                      │
          │ localhost:3000       │
          └──────────┬───────────┘
                     │
                     │ HTTP POST /api/chat
                     ▼
          ┌──────────────────────┐
          │    FastAPI Backend   │
          │                      │
          │ main.py              │
          │ foundry.py           │
          │                      │
          │ localhost:8000       │
          └──────────┬───────────┘
                     │
                     │ Azure AI Foundry SDK
                     ▼
          ┌──────────────────────────────┐
          │    Azure AI Foundry Agent    │
          │                              │
          │ Customer-Support-Agent       │
          │ Model: gpt-4.1-mini          │
          └──────────────┬───────────────┘
                         │
                ┌────────┴─────────┐
                │                  │
                ▼                  ▼
      ┌──────────────────┐   ┌──────────────────┐
      │   File Search    │   │ Supabase OpenAPI │
      │      (RAG)       │   │  Custom Tool     │
      │                  │   │                  │
      │ Policy Documents │   │ Structured Data  │
      └──────────────────┘   └──────────────────┘
                         │
                         ▼
                 AI-generated response
                         │
                         ▼
                  FastAPI Backend
                         │
                         ▼
                    Frontend
                         │
                         ▼
                       USER
```

---

## 4. Request Flow

When a user sends a message, the following process takes place:

1. The user enters a question in the web interface.
2. The frontend sends a `POST /api/chat` request to the FastAPI backend.
3. The request contains the user's message and, when available, the previous conversation ID.
4. The FastAPI backend forwards the request to the configured Azure AI Foundry agent.
5. The Foundry agent processes the request using its configured instructions and tools.
6. For policy questions, File Search retrieves relevant Reliance Digital documents.
7. For configured structured-data requests, the agent can use the Supabase OpenAPI tool.
8. The agent generates a response.
9. The backend returns the response and conversation ID to the frontend.
10. The frontend displays the response.
11. The conversation is saved locally in `localStorage`.

---

## 5. Technology Stack

| Component         | Technology                                  |
| ----------------- | ------------------------------------------- |
| Frontend          | HTML5, CSS3, Vanilla JavaScript             |
| Frontend Server   | Node.js HTTP server                         |
| Backend           | Python + FastAPI                            |
| AI Platform       | Microsoft Azure AI Foundry                  |
| AI Agent          | Azure AI Foundry Agent Service              |
| Model             | `gpt-4.1-mini`                              |
| RAG               | Foundry File Search                         |
| Knowledge Sources | Reliance Digital policy documents           |
| Structured Data   | Supabase                                    |
| Custom Tool       | OpenAPI                                     |
| Azure SDK         | `azure-ai-projects`                         |
| Authentication    | `azure-identity` / `DefaultAzureCredential` |
| Local Persistence | Browser `localStorage`                      |

---

## 6. Repository Structure

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

### Backend Files

`main.py`

The main FastAPI application.

It provides:

* `GET /api/health`
* `POST /api/chat`

It also configures CORS and validates incoming requests.

`foundry.py`

Contains the Azure AI Foundry integration.

It:

* Creates the Azure AI Project client
* Authenticates using `DefaultAzureCredential`
* Retrieves the configured agent
* Sends messages through the Foundry/OpenAI-compatible Responses API
* Maintains multi-turn conversation context

`requirements.txt`

Contains the Python packages required by the backend.

`.env.example`

Contains the environment variables required to connect the backend to Azure AI Foundry.

### Frontend Files

`index.html`

Contains the main customer support interface and chat layout.

`style.css`

Contains the custom styling and responsive layout.

`app.js`

Contains the frontend application logic, including:

* Sending messages
* Receiving API responses
* Conversation handling
* Loading state
* Error state
* Retry functionality
* Suggested questions
* `localStorage` persistence
* Clear conversation functionality

`server.js`

A lightweight Node.js HTTP server used to serve the static frontend locally.

---

# 7. Azure AI Foundry Configuration

The backend does not create a new AI model or create the agent dynamically.

The project calls an existing Azure AI Foundry agent that has already been configured in the Foundry portal.

### Foundry Project

```text
Universal-Customer-Support-Agent
```

### Agent

```text
Customer-Support-Agent
```

### Model

```text
gpt-4.1-mini
```

The model deployment name must match the deployment configured in the Foundry project.

---

## 8. Foundry Agent Tools

### File Search

File Search provides the RAG component of the application.

The agent can search the configured Reliance Digital documents and use retrieved information when answering support questions.

Example knowledge areas:

```text
Return Policy
Warranty Policy
Cancellation Policy
Delivery / Shipping Information
```

### Supabase OpenAPI Tool

A custom OpenAPI tool is configured inside the Foundry agent to access structured data stored in Supabase.

This allows the agent to perform configured lookups without placing database logic directly in the frontend or FastAPI application.

The architecture therefore separates:

```text
File Search
    ↓
Policy / Knowledge Questions

Supabase OpenAPI Tool
    ↓
Structured Data / Record Lookups
```

---

# 9. Prerequisites

Before running the project locally, install the following.

### Required

* Python 3.10 or newer
* Node.js
* Azure CLI
* An Azure account with access to the configured Azure AI Foundry project
* Access to the existing Foundry agent and model deployment

### Azure CLI Login

Run:

```bash
az login
```

This allows `DefaultAzureCredential` to use the logged-in Azure identity during local development.

---

# 10. Backend Setup

Open a terminal in the project directory.

```bash
cd backend
```

Create a Python virtual environment:

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 11. Backend Environment Variables

Create a file named:

```text
backend/.env
```

Use the following configuration:

```env
AZURE_AI_PROJECT_ENDPOINT=<your-foundry-project-endpoint>

FOUNDRY_AGENT_NAME=Customer-Support-Agent

FOUNDRY_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

### Example

```env
AZURE_AI_PROJECT_ENDPOINT=https://<resource>.services.ai.azure.com/api/projects/<project>

FOUNDRY_AGENT_NAME=Customer-Support-Agent

FOUNDRY_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

Do not commit the real `.env` file to GitHub.

The project already includes `.env` in `.gitignore`.

---

# 12. Run the Backend

From the `backend` directory:

```bash
uvicorn main:app --reload --port 8000
```

The backend will be available at:

```text
http://localhost:8000
```

FastAPI automatically provides interactive API documentation at:

```text
http://localhost:8000/docs
```

---

# 13. Backend Health Check

Open:

```text
http://localhost:8000/api/health
```

A successful response should look similar to:

```json
{
  "status": "ok",
  "agent_name": "Customer-Support-Agent",
  "agent_id": "..."
}
```

This endpoint checks that:

* The Azure AI Foundry client is initialized
* The project is reachable
* The configured agent exists

---

# 14. Frontend Setup

The frontend does not require a framework or compilation step.

Open another terminal:

```bash
cd frontend
```

Run the included Node.js server:

```bash
node server.js
```

The frontend will be available at:

```text
http://localhost:3000
```

Open that address in a browser.

---

# 15. Frontend and Backend Connection

The current frontend uses:

```javascript
const API_BASE_URL = "http://localhost:8000";
```

This means:

```text
Frontend
http://localhost:3000
        │
        ▼
Backend
http://localhost:8000
```

When deploying the application, this value must be changed to the public URL of the deployed backend.

For example:

```javascript
const API_BASE_URL = "https://your-backend-app.azurewebsites.net";
```

Without this change, a deployed frontend will still try to contact `localhost`.

---

# 16. API Documentation

## GET `/api/health`

Checks the Foundry connection and configured agent.

### Request

```http
GET /api/health
```

### Response

```json
{
  "status": "ok",
  "agent_name": "Customer-Support-Agent",
  "agent_id": "agent-id"
}
```

---

## POST `/api/chat`

Sends a message to the customer support agent.

### Request

```http
POST /api/chat
Content-Type: application/json
```

### Request Body

```json
{
  "message": "What is the return policy?",
  "conversation_id": null
}
```

For a follow-up message:

```json
{
  "message": "What about the warranty?",
  "conversation_id": "previous-response-id"
}
```

### Response

```json
{
  "reply": "The return policy information...",
  "conversation_id": "new-response-id"
}
```

The returned `conversation_id` is used for the next message so that the conversation can continue with context.

---

# 17. Running the Complete Project Locally

Open two terminals.

### Terminal 1 — Backend

```bash
cd backend
.venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

### Terminal 2 — Frontend

```bash
cd frontend
node server.js
```

Then open:

```text
http://localhost:3000
```

The expected architecture is:

```text
Browser
  ↓
Frontend :3000
  ↓
FastAPI :8000
  ↓
Azure AI Foundry
  ↓
Customer-Support-Agent
  ↓
gpt-4.1-mini
  ↓
File Search / Supabase
```

---

# 18. Deployment

The project consists of two independently deployable parts:

```text
Frontend
    +
Backend
```

The Azure AI Foundry agent and its tools are external services configured in Azure.

A production deployment can therefore be structured as:

```text
                ┌─────────────────────┐
                │   Static Frontend   │
                │                     │
                │ index.html          │
                │ style.css           │
                │ app.js              │
                └──────────┬──────────┘
                           │
                           │ HTTPS
                           ▼
                ┌─────────────────────┐
                │    FastAPI API      │
                │    Azure App        │
                │    Service          │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Azure AI Foundry    │
                │ Customer-Support    │
                │ Agent               │
                └──────────┬──────────┘
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
            File Search          Supabase
```

---

# 19. Backend Deployment to Azure App Service

The FastAPI backend can be deployed as a Python web application.

### Step 1 — Create the App Service

Create an Azure App Service configured for Python.

Use a Python runtime compatible with the project.

### Step 2 — Deploy the Backend

Deploy the contents of the `backend` directory.

The application entry point is:

```text
main:app
```

A typical startup command is:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Step 3 — Configure Application Settings

Set the following environment variables in Azure App Service:

```env
AZURE_AI_PROJECT_ENDPOINT=<your-foundry-project-endpoint>
FOUNDRY_AGENT_NAME=Customer-Support-Agent
FOUNDRY_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

Do not upload or commit a development `.env` file containing secrets.

### Step 4 — Azure Authentication

The backend uses:

```python
DefaultAzureCredential()
```

For local development, this can use the Azure CLI login:

```bash
az login
```

In Azure, the application should use an appropriate managed identity or other supported Azure identity mechanism, with the necessary permissions to access the Azure AI Foundry project.

### Step 5 — Test the Deployed API

After deployment, test:

```text
https://<your-backend-domain>/api/health
```

The endpoint should return the configured agent information when the backend can successfully connect to Foundry.

---

# 20. Frontend Deployment

Because the frontend is plain HTML, CSS and JavaScript, it does not require a build process.

The following files are enough to deploy the UI:

```text
frontend/index.html
frontend/style.css
frontend/app.js
```

They can be hosted on a static web hosting platform.

Examples include:

* Azure Static Web Apps
* GitHub Pages
* Netlify
* Vercel
* Any web server capable of serving static files

The important configuration change is in:

```text
frontend/app.js
```

Replace:

```javascript
const API_BASE_URL = "http://localhost:8000";
```

with the public backend URL:

```javascript
const API_BASE_URL = "https://<your-backend-domain>";
```

---

# 21. CORS Configuration for Deployment

The current backend contains:

```python
allow_origins=["*"]
```

This is convenient for development because it allows requests from any origin.

For production, it is better to replace the wildcard with the actual frontend domain.

For example:

```python
allow_origins=[
    "https://your-frontend-domain.com"
]
```

This limits API requests to the intended frontend origin.

---

# 22. Security Considerations

The project follows several basic security practices:

* Azure authentication is handled through `DefaultAzureCredential`
* Azure credentials are not hardcoded into Python source files
* `.env` is excluded from Git
* The frontend does not directly access Azure AI Foundry credentials
* API communication happens through the FastAPI backend

For production deployment, additional hardening is recommended:

* Restrict CORS to the real frontend domain
* Use HTTPS for the frontend and backend
* Use managed identity where possible
* Store secrets in Azure configuration/secret-management services
* Do not expose detailed internal exceptions to end users
* Add authentication and authorization if the application is used by real customers
* Add request rate limiting and abuse protection

---

# 23. Important Development Configuration Note

The model used by this project is:

```text
gpt-4.1-mini
```

Make sure the same model deployment name is used consistently in:

```text
backend/.env
backend/.env.example
backend/foundry.py
Azure AI Foundry
```

The current `foundry.py` contains a fallback/default value, so it should also be updated from:

```python
"gpt-5-mini"
```

to:

```python
"gpt-4.1-mini"
```

when configuring this project for the final environment.

---

# 24. Testing

The application can be tested at multiple levels.

### Backend Health Test

```text
GET /api/health
```

Expected result:

```text
status = ok
```

### Policy Question Test

Example:

```text
What is the return policy?
```

The agent should use the configured Reliance Digital policy knowledge source.

### Unsupported Question Test

Ask a question that is not covered by the configured knowledge sources.

The agent should avoid inventing a Reliance Digital policy and should indicate when the information cannot be verified.

### Multi-Turn Test

Example:

```text
User: What is the return policy?

User: Does that apply to opened products?
```

The second question should be sent using the conversation ID from the first response.

### Frontend Persistence Test

1. Open the application.
2. Send several messages.
3. Refresh the browser.
4. Verify that the previous messages are restored.

### Error Handling Test

Stop the backend and attempt to send a message.

The frontend should show an error state and provide a retry option.

---

# 25. Known Limitations

### Browser-Only Chat History

Conversation history is stored in browser `localStorage`.

Therefore:

* History is local to a browser/device
* Clearing browser storage removes the saved messages
* There is currently no centralized account-based history

### No Customer Authentication

The current application does not provide a complete customer login/account system.

### Supabase Integration Depends on Foundry Configuration

The Supabase functionality is configured as a custom OpenAPI tool in the Foundry agent.

The backend does not directly perform Supabase queries.

### No Direct Reliance Digital Internal System Integration

Any structured customer/order data available through the demonstration setup depends on the configured Supabase data source.

The project does not connect directly to Reliance Digital's private internal order-management infrastructure.

### Frontend API URL

The frontend currently contains a local backend URL.

This must be changed before production deployment.

### Development CORS Policy

The backend currently permits all origins for development.

A production deployment should restrict this.

---

# 26. Future Improvements

Possible future improvements include:

* User authentication and customer accounts
* Server-side conversation storage
* Persistent customer support history
* Real order-tracking integration
* Real-time shipment information
* Larger and continuously updated knowledge bases
* Automated backend and frontend tests
* Production-grade logging and monitoring
* Role-based access control
* Rate limiting and abuse prevention
* Better source citations in AI responses
* Deployment through CI/CD pipelines

---

# 27. Troubleshooting

## Backend does not start

Check that the virtual environment is active:

```bash
.venv\Scripts\activate
```

Then install dependencies again:

```bash
pip install -r requirements.txt
```

---

## Azure authentication error

Run:

```bash
az login
```

Then verify that the logged-in account has access to the Azure AI Foundry project.

---

## `AZURE_AI_PROJECT_ENDPOINT` error

Make sure `backend/.env` exists and contains:

```env
AZURE_AI_PROJECT_ENDPOINT=<your-foundry-project-endpoint>
```

---

## Agent not found

Check:

```env
FOUNDRY_AGENT_NAME=Customer-Support-Agent
```

The value must match the agent configured in Azure AI Foundry.

---

## Wrong model deployment

Check:

```env
FOUNDRY_MODEL_DEPLOYMENT_NAME=gpt-4.1-mini
```

The deployment name must match the actual model deployment configured in the Foundry project.

---

## Frontend cannot connect to backend

Check that the backend is running:

```text
http://localhost:8000/api/health
```

Then check `frontend/app.js`:

```javascript
const API_BASE_URL = "http://localhost:8000";
```

For a deployed application, replace the localhost URL with the deployed backend URL.

---

## CORS error

For local development, the current backend allows all origins.

For production, make sure the frontend domain is included in the backend's `allow_origins` configuration.

---

# 28. Technical Documentation

Additional implementation details are available in:

```text
DOCUMENTATION.md
```

That document contains deeper information about:

* Azure AI Foundry configuration
* Agent instructions
* File Search
* Supabase OpenAPI integration
* Backend implementation
* Authentication
* Conversation handling
* Frontend behavior
* Design workflow
* Development issues and resolutions

---

# 29. Design and Development Workflow

The frontend design was developed using Google Stitch and implemented using the generated design as the visual reference.

The project was implemented using a lightweight HTML/CSS/JavaScript frontend instead of a large frontend framework.

This keeps the application simple to deploy and avoids the need for a frontend build system.

---

# 30. Acknowledgments

This project uses the following technologies and resources:

* **Microsoft Azure AI Foundry** — AI agent platform and agent tooling
* **`gpt-4.1-mini`** — language model used by the configured Foundry agent
* **Azure AI Foundry File Search** — Retrieval-Augmented Generation over policy documents
* **Supabase** — structured data storage exposed through the custom OpenAPI tool
* **FastAPI** — backend API framework
* **`azure-ai-projects`** — Azure AI Foundry Python SDK
* **`azure-identity`** — Azure authentication
* **Google Stitch** — frontend design workflow
* **Reliance Digital policy documents** — knowledge sources used for customer-support responses

---

# 31. Disclaimer

This project is an educational and demonstration application.

The Reliance Digital policy documents used as knowledge sources are publicly available documents used for demonstration purposes. The application should not be treated as an official Reliance Digital customer-support system unless it is formally integrated and authorized by Reliance Digital.

---

# 32. Quick Start

For a quick local run:

### 1. Login to Azure

```bash
az login
```

### 2. Start the backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 3. Start the frontend

Open another terminal:

```bash
cd frontend
node server.js
```

### 4. Open the application

```text
http://localhost:3000
```

### 5. Test the backend

```text
http://localhost:8000/api/health
```

---

## Project Summary

The Reliance Digital Customer Support Agent combines a simple web interface with a FastAPI backend and an existing Azure AI Foundry agent.

The overall system is:

```text
HTML/CSS/JavaScript
        ↓
     FastAPI
        ↓
Azure AI Foundry Agent
        ↓
  ┌───────────────┐
  │               │
  ▼               ▼
File Search     Supabase
   RAG         OpenAPI Tool
  │               │
  └───────┬───────┘
          ▼
    gpt-4.1-mini
          ▼
    Support Response
```

The project demonstrates how an existing AI agent can be integrated into a complete customer-support web application while keeping the frontend, backend, AI agent, retrieval layer, and structured data layer separated into clear components.
