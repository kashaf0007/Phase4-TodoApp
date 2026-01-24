# Data Model: Backend & MCP Architecture

## Overview
This document defines the canonical data models for the Todo AI Chatbot project as specified in the constitution.

## Entity: Task

### Fields
- **user_id** (UUID/String): Foreign key linking the task to a user
- **id** (UUID): Unique identifier for the task
- **title** (String): Title of the task (required, max 255 chars)
- **description** (Text): Detailed description of the task (optional)
- **completed** (Boolean): Whether the task is completed (default: false)
- **created_at** (DateTime): Timestamp when the task was created
- **updated_at** (DateTime): Timestamp when the task was last updated

### Relationships
- Belongs to a User (via user_id)

### Validation Rules
- Title is required and must be between 1-255 characters
- user_id is required and must reference an existing user
- created_at and updated_at are automatically managed by the ORM

### State Transitions
- Initially: completed = false
- On completion: completed = true
- On uncompletion: completed = false

## Entity: Conversation

### Fields
- **user_id** (UUID/String): Foreign key linking the conversation to a user
- **id** (UUID): Unique identifier for the conversation
- **created_at** (DateTime): Timestamp when the conversation was created
- **updated_at** (DateTime): Timestamp when the conversation was last updated

### Relationships
- Belongs to a User (via user_id)
- Has many Messages (via conversation_id)

### Validation Rules
- user_id is required and must reference an existing user
- created_at and updated_at are automatically managed by the ORM

### State Transitions
- Created when the first message in a conversation is added
- Updated when new messages are added to the conversation

## Entity: Message

### Fields
- **user_id** (UUID/String): Foreign key linking the message to a user
- **id** (UUID): Unique identifier for the message
- **conversation_id** (UUID): Foreign key linking the message to a conversation
- **role** (String): Role of the message sender (either "user" or "assistant")
- **content** (Text): Content of the message (required)
- **created_at** (DateTime): Timestamp when the message was created

### Relationships
- Belongs to a User (via user_id)
- Belongs to a Conversation (via conversation_id)

### Validation Rules
- user_id is required and must reference an existing user
- conversation_id is required and must reference an existing conversation
- role must be either "user" or "assistant"
- content is required and must not be empty
- created_at is automatically managed by the ORM

### State Transitions
- Immutable once created (no updates to message content allowed)

## Database Constraints

### Indexes
- Index on Task.user_id for efficient user-specific queries
- Index on Conversation.user_id for efficient user-specific queries
- Index on Message.user_id for efficient user-specific queries
- Index on Message.conversation_id for efficient conversation-specific queries
- Index on Message.created_at for chronological ordering

### Foreign Key Constraints
- Task.user_id references Users.id
- Conversation.user_id references Users.id
- Message.user_id references Users.id
- Message.conversation_id references Conversation.id

## SQLModel Implementation Notes

All models will be implemented using SQLModel with the following characteristics:
- Use of UUID primary keys for global uniqueness
- Automatic timestamp management using SQLModel's field options
- Proper relationship definitions using SQLModel's relationship features
- Validation at both the application and database levels
- Support for both sync and async operations