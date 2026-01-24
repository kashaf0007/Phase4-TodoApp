# Feature Specification: Backend & MCP Architecture

**Feature Branch**: `004-backend-mcp-architecture`
**Created**: 2026-01-24
**Status**: Draft
**Input**: User description: "Backend & MCP Architecture 1. Framework & Server Backend: Python FastAPI Chat Endpoint: /api/{user_id}/chat (single entry point) Statelessness: No in-memory storage, global variables, or cached conversation state Each request must reconstruct conversation from Neon DB Conversation Flow: Receive user message Fetch conversation history from Neon PostgreSQL Build agent input (history + new message) Persist user message Execute agent via MCP tools Persist assistant response Return response to frontend 2. Database & Models DB: Neon Serverless PostgreSQL (exclusive) ORM: SQLModel Data Models: ModelFields Taskuser_id, id, title, description, completed, created_at, updated_at Conversationuser_id, id, created_at, updated_at Messageuser_id, id, conversation_id, role (user Persistence Rule: All state-changing actions must pass only through MCP tools. 3. MCP Server Core Role: Stateless execution of task-related tools Mandatory Tools: add_task, list_tasks, complete_task, delete_task, update_task Tool Rules: Stateless, deterministic, single responsibility Accept explicit parameters Return structured output Tool Logging: Every tool call must be logged and returned in API response under tool_calls FastMCP Integration: FastMCP is part of MCP server for tool execution orchestration 4. Authentication & Security Auth Provider: Better Auth Requirement: user_id mandatory for all operations Frontend Security: ChatKit domain allowlist enforced API Keys: Gemini API keys are used in OpenAI Agents for reasoning and decision-making"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Interacts with Chat Interface (Priority: P1)

User sends a message to the chat interface and receives an intelligent response from the assistant powered by MCP tools.

**Why this priority**: This is the core functionality that enables the primary value proposition of the system - allowing users to interact with an AI assistant that can perform tasks.

**Independent Test**: Can be fully tested by sending a message to the API endpoint and verifying that a response is received with appropriate tool calls logged.

**Acceptance Scenarios**:

1. **Given** a user is authenticated and connected to the chat endpoint, **When** the user sends a message requesting a task, **Then** the system returns a response with the task completed and tool calls logged.
2. **Given** a user has an existing conversation history, **When** the user sends a new message, **Then** the system retrieves the conversation history and incorporates it into the agent's context before responding.

---

### User Story 2 - User Manages Tasks (Priority: P2)

User can create, view, update, and delete tasks through the chat interface using natural language commands.

**Why this priority**: This represents the core functionality of the task management system that users will interact with daily.

**Independent Test**: Can be tested by sending natural language commands to create, list, update, and delete tasks, verifying that the appropriate MCP tools are called and the database is updated.

**Acceptance Scenarios**:

1. **Given** a user wants to add a new task, **When** the user sends a message like "Add a task to buy groceries", **Then** the system creates a new task in the database and confirms to the user.

---

### User Story 3 - User Authenticates and Maintains Session (Priority: P3)

User authenticates via Better Auth and their identity is verified for all operations.

**Why this priority**: Security and user identification are foundational for maintaining proper data separation and access controls.

**Independent Test**: Can be tested by verifying that all API calls require a valid user_id and that unauthorized requests are rejected.

**Acceptance Scenarios**:

1. **Given** an unauthenticated user attempts to access the chat endpoint, **When** they make a request without proper authentication, **Then** the system rejects the request with an appropriate error.

---

### Edge Cases

- What happens when the Neon database is temporarily unavailable during a conversation?
- How does the system handle malformed user inputs that could cause tool execution errors?
- What occurs when a user attempts to access another user's conversation data?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a single chat endpoint at /api/{user_id}/chat that handles all user interactions
- **FR-002**: System MUST be stateless - no in-memory storage, global variables, or cached conversation state between requests
- **FR-003**: System MUST reconstruct conversation context from Neon PostgreSQL database on each request
- **FR-004**: System MUST persist all user messages to the Neon PostgreSQL database
- **FR-005**: System MUST execute agent responses via MCP tools (add_task, list_tasks, complete_task, delete_task, update_task)
- **FR-006**: System MUST log all tool calls executed and return them in the API response under tool_calls
- **FR-007**: System MUST authenticate all requests using Better Auth and validate user_id
- **FR-008**: System MUST use Neon Serverless PostgreSQL exclusively for data persistence
- **FR-009**: System MUST use SQLModel as the ORM for database interactions
- **FR-010**: System MUST enforce that all state-changing actions pass only through MCP tools
- **FR-011**: System MUST accept explicit parameters for all MCP tools
- **FR-012**: System MUST return structured output from all MCP tools
- **FR-013**: System MUST implement FastMCP for tool execution orchestration

### Key Entities *(include if feature involves data)*

- **Task**: Represents a user's task with fields: user_id, id, title, description, completed, created_at, updated_at
- **Conversation**: Represents a conversation thread with fields: user_id, id, created_at, updated_at
- **Message**: Represents individual messages within conversations with fields: user_id, id, conversation_id, role (user/assistant), content, created_at

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can initiate and continue conversations with the AI assistant with responses delivered in under 5 seconds
- **SC-002**: System maintains data integrity with 99.9% uptime for database operations
- **SC-003**: All user requests are properly authenticated and authorized with zero unauthorized access incidents
- **SC-004**: At least 95% of user requests result in successful task completion through MCP tools
- **SC-005**: Tool execution logs are captured and returned with 100% accuracy for debugging and audit purposes
