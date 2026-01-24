# Research Findings: Backend & MCP Architecture

## Overview
This document captures research findings for implementing the stateless FastAPI backend with MCP tools for the Todo AI Chatbot project.

## Decision: MCP Tool Implementation
**Rationale**: MCP (Model Context Protocol) tools provide a standardized way for AI agents to interact with external systems. Using MCP ensures that all state-changing operations go through a controlled interface, maintaining the required separation between AI reasoning and data persistence.

**Alternatives considered**: 
- Direct database calls from the agent
- Custom RPC mechanism
- REST API calls from the agent

## Decision: FastAPI for the Backend Framework
**Rationale**: FastAPI provides excellent performance, async support, automatic API documentation, and strong typing capabilities. It's ideal for building stateless APIs that serve as orchestration layers between the frontend and AI agents.

**Alternatives considered**:
- Flask (simpler but less performant and fewer built-in features)
- Django (too heavy for a stateless API layer)
- Node.js/Express (would require changing the tech stack from Python)

## Decision: Neon Serverless PostgreSQL for Database
**Rationale**: Neon's serverless PostgreSQL offers automatic scaling, branching capabilities, and seamless integration with Python applications. It meets the requirement for exclusive use of Neon PostgreSQL as specified in the constitution.

**Alternatives considered**:
- Standard PostgreSQL (requires manual scaling and management)
- SQLite (not suitable for multi-user SaaS application)
- Cloud alternatives like Supabase (would require different integration patterns)

## Decision: SQLModel for ORM
**Rationale**: SQLModel combines the power of SQLAlchemy with the ease of Pydantic, offering type hints, validation, and a clean syntax. It's specifically designed to work well with FastAPI applications.

**Alternatives considered**:
- Pure SQLAlchemy (more verbose, less integration with FastAPI)
- Tortoise ORM (async-first but less mature)
- Peewee (simpler but less feature-rich)

## Decision: Better Auth for Authentication
**Rationale**: Better Auth provides a modern, easy-to-integrate authentication solution that works well with Python backends. It ensures that user_id is available for all operations as required by the constitution.

**Alternatives considered**:
- OAuth providers directly (requires more setup and maintenance)
- Custom JWT implementation (security concerns and complexity)
- Firebase Auth (would require different integration patterns)

## Decision: Stateless Architecture Pattern
**Rationale**: The stateless architecture ensures scalability, reliability, and consistency. Each request can be processed independently, making the system more robust and easier to reason about. This aligns with the constitutional requirement of no in-memory storage.

**Alternatives considered**:
- Session-based storage (violates statelessness requirement)
- Redis caching (adds complexity and potential points of failure)
- WebSocket connections with in-memory state (violates statelessness requirement)

## Decision: OpenAI Agents SDK for AI Logic
**Rationale**: The OpenAI Agents SDK provides a robust framework for creating AI agents that can use tools. It handles the complexity of tool calling, reasoning, and response generation, allowing us to focus on implementing the tools themselves.

**Alternatives considered**:
- LangChain (different ecosystem, potentially more complex)
- Anthropic Claude (different API, would require different implementation)
- Custom LLM integration (much more complex and error-prone)

## Decision: Single Endpoint Architecture
**Rationale**: Having a single `/api/{user_id}/chat` endpoint simplifies the API surface and forces a clean separation between the frontend and backend logic. The agent handles all intent detection and tool selection internally.

**Alternatives considered**:
- Multiple REST endpoints for different operations (violates single entry point law)
- GraphQL API (adds complexity without significant benefits)
- Multiple chat endpoints (unnecessary complexity)

## Key Unknowns Resolved
- MCP server setup and integration with FastAPI
- Proper tool logging mechanisms
- Conversation reconstruction from database
- Error handling patterns for AI responses
- Rate limiting and security considerations