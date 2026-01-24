# Implementation Plan: ChatKit Frontend Integration

**Branch**: `006-chatkit-frontend-integration` | **Date**: 2026-01-24 | **Spec**: [link](spec.md)
**Input**: Feature specification from `/specs/006-chatkit-frontend-integration/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan implements a React-based ChatKit frontend that integrates with a FastAPI backend to enable AI-powered chat interactions. The frontend provides a user-friendly interface for interacting with an AI assistant that leverages MCP tools for task management. The implementation follows a stateless architecture where all conversation context is handled by the backend, with the frontend serving only as a presentation layer.

## Technical Context

**Language/Version**: JavaScript/ES6+ for frontend, Python 3.11 for backend
**Primary Dependencies**: React, ChatKit for frontend; FastAPI, OpenAI SDK, SQLModel for backend
**Storage**: Neon Serverless PostgreSQL database for conversation and task persistence
**Testing**: Jest for frontend, pytest for backend
**Target Platform**: Web browser (Chrome, Firefox, Safari, Edge)
**Project Type**: Web application with separate frontend and backend
**Performance Goals**: <3 second page load time, <1 second response time for chat messages
**Constraints**: Stateless frontend (no local chat history), secure API key handling, domain-restricted access
**Scale/Scope**: Support for multiple concurrent users with individual conversation contexts

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Based on the project constitution:
- ✅ Agentic Authority: The backend will use OpenAI Agents SDK for decision-making
- ✅ Tool-Only Side Effects: All state changes will occur via MCP tools
- ✅ Statelessness: The frontend will be stateless with no local chat history
- ✅ Persistent Memory: Conversation context will be handled by the backend/database
- ✅ Single Entry Point Law: The system will use POST /api/{user_id}/chat as the primary endpoint
- ✅ Database Authority: Neon PostgreSQL will be the sole persistence layer
- ✅ Security & Authentication: Better Auth will handle user identity with user_id requirement
- ✅ Frontend Domain Security: Domain allowlist will be enforced for ChatKit access

## Project Structure

### Documentation (this feature)

```text
specs/006-chatkit-frontend-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── task.py
│   │   ├── conversation.py
│   │   └── message.py
│   ├── services/
│   │   └── chat_service.py
│   ├── api/
│   │   └── chat_endpoint.py
│   └── tools/
│       ├── add_task.py
│       ├── list_tasks.py
│       ├── complete_task.py
│       ├── delete_task.py
│       └── update_task.py
└── tests/

frontend/
├── src/
│   ├── components/
│   │   ├── ChatInterface.jsx
│   │   ├── MessageList.jsx
│   │   └── MessageInput.jsx
│   ├── services/
│   │   └── apiService.js
│   └── utils/
│       └── constants.js
└── tests/
```

**Structure Decision**: Web application structure with separate frontend and backend components to maintain clear separation of concerns. The frontend uses React with ChatKit for the UI, while the backend implements the agentic architecture with FastAPI and MCP tools as required by the constitution.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
