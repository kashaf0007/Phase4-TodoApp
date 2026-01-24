---
id: 2
title: "backend-mcp-architecture-plan"
stage: "plan"
date_iso: "2026-01-24"
surface: "agent"
model: "claude-sonnet-4"
feature: "004-backend-mcp-architecture"
branch: "004-backend-mcp-architecture"
user: "Kashaf Aman"
command: "/sp.plan Project Setup"
labels: ["architecture", "mcp", "fastapi", "database"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files_yaml:
  - "specs/004-backend-mcp-architecture/plan.md"
  - "specs/004-backend-mcp-architecture/research.md"
  - "specs/004-backend-mcp-architecture/data-model.md"
  - "specs/004-backend-mcp-architecture/quickstart.md"
  - "specs/004-backend-mcp-architecture/contracts/chat-api-spec.md"
  - "specs/004-backend-mcp-architecture/contracts/mcp-tools-spec.md"
tests_yaml: []
prompt_text: |
  /sp.plan Project Setup

  Initialize Python FastAPI Project

  Create a new FastAPI project structure (app/, models/, routes/, services/, mcp/)

  Setup virtual environment and dependencies (fastapi, uvicorn, sqlmodel, pydantic, httpx)

  Setup Neon PostgreSQL

  Provision Neon Serverless database

  Configure connection string in environment variables

  Test connection with a simple SQLModel query

  Install Authentication

  Integrate Better Auth for user identity management

  Ensure user_id is required for all endpoints

  Phase 2: Database Models

  Define SQLModel Models

  Task: user_id, id, title, description, completed, created_at, updated_at

  Conversation: user_id, id, created_at, updated_at

  Message: user_id, id, conversation_id, role, content, created_at

  Migrations & Schema

  Use SQLModel to create tables in Neon DB

  Validate schema matches canonical data model

  Persistence Rules

  Enforce that no direct DB manipulation occurs outside MCP tools

  Phase 3: MCP Server & Tools

  FastMCP Integration

  Set up FastMCP as part of MCP server

  Ensure it handles stateless, deterministic execution of tools

  Implement Mandatory Tools

  add_task(user_id, title, description) → returns structured task object

  list_tasks(user_id) → returns array of tasks

  complete_task(user_id, task_id) → marks task completed

  delete_task(user_id, task_id) → deletes task

  update_task(user_id, task_id, fields) → updates specified fields

  Tool Rules Enforcement

  Stateless execution: tools do not store any state

  Single responsibility: each tool only performs its designated function

  Explicit parameters required

  Structured, deterministic output

  Tool Logging

  Each tool call logged with: tool name, parameters, timestamp, result

  Returned under tool_calls in API response

  Phase 4: FastAPI Endpoint & Stateless Flow

  Single Entry Endpoint

  POST /api/{user_id}/chat as only conversational endpoint

  Receive user message and user_id

  Stateless Request Flow

  Fetch conversation history from Neon DB

  Build agent input (history + new message)

  Persist user message in Message table

  Execute agent via MCP tools

  Persist assistant response in Message table

  Return assistant response and tool call log to frontend

  Error Handling

  Gracefully handle missing tasks, invalid input, or DB errors

  Return user-friendly, non-technical messages

  Phase 5: Security & API Keys

  Authentication

  Validate Better Auth token per request

  Ensure user_id matches authenticated session

  Frontend Security

  Enforce domain allowlist for ChatKit React frontend

  OpenAI / Gemini API

  Configure Gemini API key usage in agent execution

  Ensure keys are secure, not exposed to frontend

  Phase 6: Testing & Validation

  Unit Tests

  Test each MCP tool independently

  Verify stateless execution and correct outputs

  Integration Tests

  Test full request flow: /chat → DB → MCP → Agent → Response

  Validate tool_calls logging

  Security Tests

  Validate auth enforcement

  Test domain allowlist

  Performance Check

  Ensure stateless architecture handles concurrent users

  Validate DB operations are efficient
response_text: |
  Completed implementation planning for the Backend & MCP Architecture feature. Created comprehensive documentation including:
  
  1. Updated implementation plan (plan.md) with technical context, constitution check, and project structure
  2. Research findings (research.md) covering key decisions about MCP tools, FastAPI, Neon PostgreSQL, SQLModel, Better Auth, and stateless architecture
  3. Data model definitions (data-model.md) for Task, Conversation, and Message entities
  4. API contracts for the chat endpoint and MCP tools (in contracts/ directory)
  5. Quickstart guide with setup instructions and architecture overview
  
  All artifacts align with the constitutional requirements for stateless architecture, MCP-only side effects, and agentic authority. The plan provides a clear roadmap for implementing the FastAPI backend with MCP tools integration.
outcome: "Plan successfully created with all required artifacts for Backend & MCP Architecture implementation."
evaluation: "All required planning artifacts have been created and reviewed for compliance with constitutional requirements."
---

# Prompt History Record: Backend & MCP Architecture Plan

## Summary
This PHR documents the creation of the implementation plan for the Backend & MCP Architecture feature (branch 004-backend-mcp-architecture). The planning session resulted in comprehensive documentation covering technical context, research findings, data models, API contracts, and setup instructions.

## Artifacts Created
- Implementation plan (plan.md)
- Research findings (research.md)
- Data model definitions (data-model.md)
- API contracts for chat endpoint and MCP tools
- Quickstart guide (quickstart.md)

## Constitutional Compliance
All artifacts comply with the constitutional requirements for:
- Stateless architecture (no in-memory storage)
- MCP-only side effects for all state-changing operations
- Agentic authority for business logic decisions
- Single entry point for chat interactions
- Tool purity and invocation transparency