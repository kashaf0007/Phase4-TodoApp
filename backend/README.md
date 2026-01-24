# Backend & MCP Architecture

This project implements a stateless FastAPI backend that serves as a single entry point for AI-powered chat interactions. The system uses OpenAI Agents SDK to process natural language requests, which triggers MCP tools for all state-changing operations. All conversation history and task data is persisted in Neon Serverless PostgreSQL using SQLModel ORM. The architecture enforces strict statelessness with no in-memory storage, requiring all context to be reconstructed from the database on each request.

## Features

- Single entry point for chat interactions at `/api/{user_id}/chat`
- MCP tools for all state-changing operations (add_task, list_tasks, complete_task, delete_task, update_task)
- Strict statelessness - no in-memory storage
- Neon Serverless PostgreSQL with SQLModel ORM
- Better Auth integration for user authentication
- Tool call logging for transparency

## Tech Stack

- Python 3.11
- FastAPI
- SQLModel
- Better Auth
- OpenAI Agents SDK
- FastMCP
- Neon PostgreSQL

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables (see `.env.example`)
5. Run the application:
   ```bash
   cd backend
   uvicorn app.main:app --reload --port 8000
   ```

## Environment Variables

Create a `.env` file with the following variables:

```env
NEON_DATABASE_URL=your_neon_database_url
BETTER_AUTH_SECRET=your_better_auth_secret
BETTER_AUTH_URL=your_better_auth_url
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key  # If using Google's models
DOMAIN_ALLOWLIST=your_frontend_domain
```

## Running Tests

```bash
cd backend
pytest
```

## Architecture

The application follows a clean architecture with the following layers:

- **Models**: SQLModel definitions for Task, Conversation, Message
- **Services**: Business logic and database operations
- **Routes**: API endpoints
- **Utils**: Helper functions and utilities
- **MCP**: Model Context Protocol tools for state-changing operations