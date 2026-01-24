# Quickstart Guide: Enhanced MCP Tools with Advanced Capabilities

## Overview
This guide provides step-by-step instructions to set up and use the enhanced MCP tools that extend the existing task management capabilities with bulk operations, search and filtering, and task categorization and tagging.

## Prerequisites
- Python 3.11+
- pip package manager
- Git
- Existing backend & MCP architecture setup
- Neon PostgreSQL account
- Better Auth account
- OpenAI API key (or equivalent for chosen LLM provider)

## Setup Instructions

### 1. Navigate to the Backend Directory
```bash
cd backend
```

### 2. Install Additional Dependencies (if any)
```bash
pip install -r requirements.txt
```

### 3. Update Environment Variables
Ensure your `.env` file includes all required variables from the base setup:
```env
NEON_DATABASE_URL=your_neon_database_url
BETTER_AUTH_SECRET=your_better_auth_secret
BETTER_AUTH_URL=your_better_auth_url
OPENAI_API_KEY=your_openai_api_key  # Or equivalent for your chosen LLM provider
GEMINI_API_KEY=your_gemini_api_key  # If using Google's models
DOMAIN_ALLOWLIST=your_frontend_domain
```

### 4. Update Database Schema
Run the database migration to add support for tags and categories:

```bash
# This would typically involve alembic migrations or similar
# For now, ensure your existing models support the extended fields
python -m backend.mcp.database.setup
```

### 5. Run the Application
Start the FastAPI server:

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### 6. Run the MCP Server with Enhanced Tools
In a separate terminal, start the MCP server with the enhanced tools:

```bash
cd backend
python -m mcp.server
```

## Using Enhanced Features

### Bulk Operations
Perform bulk operations using the enhanced tools:

#### Bulk Adding Tasks
The agent can use `bulk_add_tasks` to create multiple tasks at once:
```json
{
  "user_id": "user-123",
  "tasks": [
    {"title": "Task 1", "description": "Description 1"},
    {"title": "Task 2", "description": "Description 2"},
    {"title": "Task 3", "description": "Description 3"}
  ]
}
```

#### Bulk Updating Tasks
The agent can use `bulk_update_tasks` to update multiple tasks:
```json
{
  "user_id": "user-123",
  "task_ids": ["task-1", "task-2", "task-3"],
  "updates": {
    "completed": true
  }
}
```

### Search and Filtering
Use enhanced search and filtering capabilities:

#### Searching Tasks
The agent can use `search_tasks` to find tasks by content:
```json
{
  "user_id": "user-123",
  "query": "groceries",
  "limit": 10
}
```

#### Filtering Tasks
The agent can use `filter_tasks` to get tasks based on criteria:
```json
{
  "user_id": "user-123",
  "filters": {
    "status": "pending",
    "category": "work",
    "tags": ["important"]
  }
}
```

### Categorization and Tagging
Organize tasks with tags and categories:

#### Tagging a Task
The agent can use `tag_task` to add tags:
```json
{
  "user_id": "user-123",
  "task_id": "task-123",
  "tags": ["shopping", "urgent"]
}
```

#### Categorizing a Task
The agent can use `add_task_category` to assign a category:
```json
{
  "user_id": "user-123",
  "task_id": "task-123",
  "category": "personal"
}
```

## API Usage

### Interacting with Enhanced Features
The enhanced features work through the same single endpoint as before, but with the agent now having access to additional tools:

```bash
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {auth_token}" \
  -d '{"message": "Add these tasks: buy groceries, schedule appointment, call mom"}'
```

## Development

### Running Tests
```bash
cd backend
pytest tests/test_enhanced_mcp_tools.py
```

### Running All Tests
```bash
cd backend
pytest
```

## Architecture Overview

### Key Components
1. **Enhanced MCP Tools** (`mcp/tools/`): New tools for bulk operations, search, filtering, tagging, and categorization
2. **Extended Data Models** (`app/models/task.py`): Task model with tags and category fields
3. **Enhanced Services** (`app/services/task_enhanced_service.py`): Services for bulk operations, search, and filtering
4. **Agent Integration**: Agent now has access to the new tools for decision-making

### Flow for Enhanced Operations
1. User sends message requesting enhanced operation (e.g., "Add these tasks: ...")
2. Agent recognizes the need for bulk operation
3. Agent selects and calls `bulk_add_tasks` tool
4. Tool processes multiple tasks in a single operation
5. Results with summary statistics are returned to the agent
6. Agent forms appropriate response to the user

## Troubleshooting

### Common Issues

#### Enhanced Tools Not Available
- Verify that the new MCP tools are registered with the MCP server
- Check that the agent has access to the new tools in its configuration

#### Database Schema Issues
- Ensure the Task model has been extended with tags and category fields
- Verify that the database schema supports JSON fields for tags if using JSON storage

#### Partial Failures in Bulk Operations
- Check the response summary for details on successful vs failed operations
- Implement retry logic for failed individual operations if needed

### Useful Commands

#### Check Enhanced Tool Registration
```bash
# This should list all tools including the new enhanced ones
python -c "from backend.mcp.tools import get_registered_tools; print(list(get_registered_tools().keys()))"
```

#### Test Enhanced Tool Execution
```bash
curl -X POST http://localhost:8000/api/test-user/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test-token" \
  -d '{"message": "Show me all tasks tagged as urgent"}'
```

## Next Steps
- Review the enhanced MCP tools in `backend/mcp/tools/`
- Examine the extended data models in `backend/app/models/`
- Look at the enhanced services in `backend/app/services/`
- Test the new capabilities through the chat interface