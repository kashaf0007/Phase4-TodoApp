# Quickstart Guide: Backend & MCP Architecture

## Overview
This guide provides step-by-step instructions to set up and run the stateless FastAPI backend with MCP tools for the Todo AI Chatbot project.

## Prerequisites
- Python 3.11+
- pip package manager
- Git
- Neon PostgreSQL account
- Better Auth account
- OpenAI API key (or equivalent for chosen LLM provider)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root with the following variables:

```env
NEON_DATABASE_URL=your_neon_database_url
BETTER_AUTH_SECRET=your_better_auth_secret
BETTER_AUTH_URL=your_better_auth_url
OPENAI_API_KEY=your_openai_api_key  # Or equivalent for your chosen LLM provider
GEMINI_API_KEY=your_gemini_api_key  # If using Google's models
DOMAIN_ALLOWLIST=your_frontend_domain
```

### 5. Set Up Database
Run the database migration to create the required tables:

```bash
python -m backend.mcp.database.setup
```

### 6. Run the Application
Start the FastAPI server:

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### 7. Run the MCP Server
In a separate terminal, start the MCP server:

```bash
cd backend
python -m mcp.server
```

## API Usage

### Send a Chat Message
```bash
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {auth_token}" \
  -d '{"message": "Add a task to buy groceries"}'
```

## Development

### Running Tests
```bash
cd backend
pytest
```

### Running Specific Test Files
```bash
cd backend
pytest tests/test_chat_endpoint.py
pytest tests/test_mcp_tools.py
```

### Code Formatting
```bash
cd backend
black .
```

### Linting
```bash
cd backend
flake8 .
```

## Architecture Overview

### Key Components
1. **FastAPI Application** (`app/main.py`): Single entry point at `/api/{user_id}/chat`
2. **MCP Server** (`mcp/server.py`): Handles tool execution
3. **Data Models** (`app/models/`): SQLModel definitions for Task, Conversation, Message
4. **Database Service** (`app/services/database.py`): Session management
5. **Authentication Utility** (`app/utils/auth.py`): Better Auth integration

### Flow for a Chat Request
1. User sends message to `/api/{user_id}/chat`
2. Authentication middleware validates token and user_id
3. Conversation history is fetched from Neon PostgreSQL
4. User message is persisted to database
5. OpenAI Agent is invoked with conversation history and new message
6. Agent selects and executes appropriate MCP tools
7. Assistant response is persisted to database
8. Response with tool calls is returned to user

## Troubleshooting

### Common Issues

#### Database Connection Issues
- Verify NEON_DATABASE_URL is correctly set
- Check that Neon PostgreSQL is accessible
- Ensure required tables exist

#### Authentication Issues
- Confirm Better Auth is properly configured
- Verify that user_id in path matches authenticated user
- Check that domain allowlist is properly set

#### MCP Server Not Responding
- Ensure MCP server is running on the expected port
- Verify that the agent can connect to the MCP server
- Check that all required tools are registered

### Useful Commands

#### Check Database Connection
```bash
python -c "from backend.app.services.database import get_db_session; print('DB connection successful' if get_db_session() else 'DB connection failed')"
```

#### Verify MCP Tools
```bash
# This should list all registered tools
python -c "from backend.mcp.tools import get_registered_tools; print(get_registered_tools())"
```

#### Test Authentication
```bash
curl -X GET http://localhost:8000/health
```

## Next Steps
- Explore the API documentation at `http://localhost:8000/docs`
- Review the data models in `backend/app/models/`
- Examine the MCP tools in `backend/mcp/tools/`
- Look at the test suite in `backend/tests/`