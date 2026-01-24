# Implementation Plan: Enhanced MCP Tools with Advanced Capabilities

**Branch**: `005-enhanced-mcp-tools` | **Date**: 2026-01-24 | **Spec**: [link]
**Input**: Feature specification from `/specs/005-enhanced-mcp-tools/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement enhanced MCP tools that extend the existing task management capabilities with bulk operations, search and filtering, and task categorization and tagging. The implementation will maintain the stateless architecture while adding advanced features to the agent's tool set, enabling more sophisticated task management operations through natural language commands.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, SQLModel, Better Auth, OpenAI Agents SDK, FastMCP, Neon PostgreSQL driver
**Storage**: Neon Serverless PostgreSQL database with SQLModel ORM
**Testing**: pytest for unit and integration tests
**Target Platform**: Linux server (cloud deployment)
**Project Type**: Web application with stateless backend architecture
**Performance Goals**: <5 second response time for enhanced operations, bulk operations process 5+ tasks efficiently
**Constraints**: Strict statelessness (no in-memory storage), all DB operations through MCP tools only, user_id required for all operations
**Scale/Scope**: Multi-user SaaS application with proper data isolation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Phase 0 Status
✅ All constitutional requirements validated before research phase

### Post-Phase 1 Design Status
✅ All constitutional requirements validated after design phase

### Article I — Agentic Authority
✅ Agent will make all business logic decisions
✅ Backend will not contain hard-coded intent detection
✅ Agent will select and invoke MCP tools autonomously

### Article II — Tool-Only Side Effects
✅ All state-changing actions will occur exclusively via MCP tools
✅ Agent cannot directly manipulate the database
✅ MCP tools act as the only bridge between AI reasoning and persistence

### Article III — Statelessness
✅ FastAPI server will remain stateless
✅ No in-memory session storage, global variables, or cached conversation state
✅ Every request will be independently reproducible using database state alone

### Article IV — Persistent Memory
✅ Conversation context will be reconstructed on each request using database records
✅ All user and assistant messages will be stored before and after agent execution

### 4.2 Single Entry Point Law
✅ System exposes one primary conversational endpoint: POST /api/{user_id}/chat
✅ All user intentions flow through this endpoint

### 6.1 Mandatory Tool Set
✅ MCP Server will expose exactly 5 original tools: add_task, list_tasks, complete_task, delete_task, update_task
✅ MCP Server will additionally expose 6 enhanced tools: bulk_add_tasks, bulk_update_tasks, search_tasks, filter_tasks, tag_task, add_task_category

### 6.2 Tool Purity Rule
✅ MCP tools will be stateless, accept explicit parameters, perform single responsibility, return structured output

### 6.3 Tool Invocation Transparency
✅ Every tool invocation will be logged and returned in the API response under tool_calls

### 7.1 Intent-to-Tool Mapping
✅ Agent will map natural language intent to appropriate enhanced MCP tools
✅ Backend will not enforce or validate tool selection

### 7.2 Multi-Step Reasoning
✅ Agent will chain tools when needed (e.g., filter_tasks → bulk_update_tasks)

### 7.3 Confirmation Mandate
✅ Every successful operation will be confirmed with friendly natural-language response

### 7.4 Error Dignity Clause
✅ Errors will be explained without technical jargon and guide users toward next action

### 8. Stateless Conversation Flow Law
✅ Each request follows the required order: receive → fetch history → build input → persist user message → execute agent → persist response → return response

## Project Structure

### Documentation (this feature)

```text
specs/005-enhanced-mcp-tools/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── enhanced-mcp-tools-api-spec.md    # API contract for enhanced tools
│   └── enhanced-mcp-contracts-spec.md    # API contract for enhanced MCP tools
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Contains the single /api/{user_id}/chat endpoint
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py             # Task model with SQLModel (enhanced with tags/category)
│   │   ├── conversation.py     # Conversation model with SQLModel
│   │   └── message.py          # Message model with SQLModel
│   ├── routes/
│   │   ├── __init__.py
│   │   └── chat.py             # Chat endpoint implementation
│   ├── services/
│   │   ├── __init__.py
│   │   ├── database.py         # Database session management
│   │   ├── task_enhanced_service.py  # Enhanced task operations (bulk, search, filter, tag)
│   │   └── agent_service.py    # Agent orchestration
│   └── utils/
│       ├── __init__.py
│       └── auth.py             # Better Auth integration
├── mcp/
│   ├── __init__.py
│   ├── server.py               # MCP server implementation
│   └── tools/
│       ├── __init__.py
│       ├── add_task.py         # add_task MCP tool
│       ├── list_tasks.py       # list_tasks MCP tool
│       ├── complete_task.py    # complete_task MCP tool
│       ├── delete_task.py      # delete_task MCP tool
│       ├── update_task.py      # update_task MCP tool
│       ├── bulk_add_tasks.py   # Enhanced bulk add tasks MCP tool
│       ├── bulk_update_tasks.py # Enhanced bulk update tasks MCP tool
│       ├── search_tasks.py     # Enhanced search tasks MCP tool
│       ├── filter_tasks.py     # Enhanced filter tasks MCP tool
│       ├── tag_task.py         # Enhanced tag task MCP tool
│       └── add_task_category.py # Enhanced add task category MCP tool
├── tests/
│   ├── __init__.py
│   ├── test_chat_endpoint.py   # Tests for the chat endpoint
│   ├── test_enhanced_mcp_tools.py # Tests for enhanced MCP tools
│   └── conftest.py             # Pytest fixtures
├── requirements.txt
├── pyproject.toml
└── README.md
```

**Structure Decision**: Web application with separate backend directory containing FastAPI application, MCP server, and all related modules. The structure extends the existing architecture with enhanced MCP tools while maintaining separation of concerns between models, services, and tools.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
