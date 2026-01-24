# Data Model: ChatKit Frontend Integration

## Frontend Data Models

### Chat Message
Represents a single message in the conversation displayed on the frontend.

**Fields**:
- `id`: Unique identifier for the message
- `sender`: Who sent the message ("user" or "assistant")
- `content`: The text content of the message
- `timestamp`: When the message was sent/received
- `tool_call_info`: Optional metadata about tools called by the AI (for transparency)

**Validation rules**:
- Content must be non-empty string
- Sender must be either "user" or "assistant"
- Timestamp must be in ISO 8601 format

### Conversation Context
Represents the conversation state as managed by the frontend (limited view).

**Fields**:
- `conversation_id`: Identifier for the conversation thread
- `messages`: Array of ChatMessage objects
- `user_id`: Associated user identifier

**Validation rules**:
- conversation_id must be unique
- messages array must not exceed display limits
- user_id must be valid and authenticated

### User Session
Temporary frontend representation of user session state.

**Fields**:
- `user_id`: Authenticated user identifier
- `session_token`: Authentication token (if applicable)
- `last_interaction_time`: Timestamp of last activity

**Validation rules**:
- user_id must be authenticated
- session_token must be valid if present
- last_interaction_time must be recent

## Backend Data Models (for reference)

### Task (Canonical Model)
Defined by the project constitution as the canonical data model.

**Fields**:
- `user_id`: Foreign key to user
- `id`: Unique task identifier
- `title`: Task title
- `description`: Task description
- `completed`: Boolean indicating completion status
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

### Message (Canonical Model)
Defined by the project constitution as the canonical data model.

**Fields**:
- `user_id`: Foreign key to user
- `id`: Unique message identifier
- `conversation_id`: Foreign key to conversation
- `role`: Message role ("user" or "assistant")
- `content`: Message content
- `created_at`: Timestamp of creation

### Conversation (Canonical Model)
Defined by the project constitution as the canonical data model.

**Fields**:
- `user_id`: Foreign key to user
- `id`: Unique conversation identifier
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update