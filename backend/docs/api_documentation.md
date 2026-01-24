# API Documentation: Todo AI Chatbot Backend

## Overview

The Todo AI Chatbot Backend provides a single entry point for AI-powered chat interactions. The system uses OpenAI Agents SDK to process natural language requests, which triggers MCP tools for all state-changing operations. All conversation history and task data is persisted in Neon Serverless PostgreSQL using SQLModel ORM.

## Base URL

```
https://api.yourdomain.com
```

## Authentication

All endpoints require authentication using Better Auth. Include the authentication token in the Authorization header:

```
Authorization: Bearer <your_auth_token>
```

## Rate Limiting

The API implements rate limiting to prevent abuse. Standard limits apply per authenticated user.

## Endpoints

### POST /api/{user_id}/chat

The primary conversational endpoint that handles all user interactions with the AI assistant.

#### Path Parameters

| Parameter | Type   | Description                      |
|-----------|--------|----------------------------------|
| user_id   | string | The unique identifier of the user |

#### Request Body

```json
{
  "message": "string (required)",
  "metadata": {
    "timestamp": "string (optional)",
    "source": "string (optional)"
  }
}
```

#### Response

```json
{
  "response": "string",
  "tool_calls": [
    {
      "tool_name": "string",
      "parameters": {},
      "result": {}
    }
  ],
  "conversation_id": "string",
  "message_id": "string"
}
```

#### Example Request

```bash
curl -X POST https://api.yourdomain.com/api/123e4567-e89b-12d3-a456-426614174000/chat \
  -H "Authorization: Bearer <auth_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy groceries"
  }'
```

#### Example Response

```json
{
  "response": "I've added the task 'buy groceries' to your list.",
  "tool_calls": [
    {
      "tool_name": "add_task",
      "parameters": {
        "user_id": "123e4567-e89b-12d3-a456-426614174000",
        "title": "buy groceries",
        "description": null
      },
      "result": {
        "success": true,
        "task_id": "987e6543-e21b-32d3-a456-426614174999"
      }
    }
  ],
  "conversation_id": "555e4567-e89b-12d3-a456-426614174888",
  "message_id": "777e4567-e89b-12d3-a456-426614174777"
}
```

#### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200  | Successful response from the AI assistant |
| 400  | Invalid request format or missing required fields |
| 401  | Invalid or missing authentication |
| 403  | User does not have permission to access this resource |
| 429  | Rate limit exceeded |
| 500  | Unexpected server error |

## MCP Tools

The backend exposes the following MCP tools that the AI agent can use:

### add_task

Creates a new task for a user.

#### Parameters
```json
{
  "user_id": "string (required)",
  "title": "string (required)",
  "description": "string (optional)"
}
```

#### Response
```json
{
  "success": "boolean",
  "task_id": "string",
  "message": "string (optional)"
}
```

### list_tasks

Retrieves all tasks for a user, optionally filtered by completion status.

#### Parameters
```json
{
  "user_id": "string (required)",
  "completed": "boolean (optional, default: null)"
}
```

#### Response
```json
{
  "success": "boolean",
  "tasks": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "completed": "boolean",
      "created_at": "string (ISO 8601 datetime)",
      "updated_at": "string (ISO 8601 datetime)"
    }
  ],
  "count": "integer"
}
```

### complete_task

Marks a task as completed.

#### Parameters
```json
{
  "user_id": "string (required)",
  "task_id": "string (required)"
}
```

#### Response
```json
{
  "success": "boolean",
  "message": "string (optional)"
}
```

### delete_task

Deletes a task.

#### Parameters
```json
{
  "user_id": "string (required)",
  "task_id": "string (required)"
}
```

#### Response
```json
{
  "success": "boolean",
  "message": "string (optional)"
}
```

### update_task

Updates properties of a task.

#### Parameters
```json
{
  "user_id": "string (required)",
  "task_id": "string (required)",
  "title": "string (optional)",
  "description": "string (optional)",
  "completed": "boolean (optional)"
}
```

#### Response
```json
{
  "success": "boolean",
  "message": "string (optional)"
}
```

## Error Handling

All error responses follow the same structure:

```json
{
  "error": {
    "type": "string",
    "message": "string",
    "details": {}
  }
}
```

### Common Error Types

- `RESOURCE_NOT_FOUND`: The requested resource was not found
- `UNAUTHORIZED_ACCESS`: User does not have permission to access the resource
- `INVALID_PARAMETERS`: One or more parameters are invalid
- `INTERNAL_ERROR`: An internal server error occurred
- `TOOL_NOT_FOUND`: The requested tool does not exist
- `TOOL_EXECUTION_ERROR`: An error occurred while executing the tool

## Health Check

### GET /health

Returns the health status of the application.

#### Response

```json
{
  "status": "healthy",
  "checks": {
    "database": "connected",
    "mcp_server": "available"
  }
}
```

## Security

- All requests must include a valid Better Auth token
- The user_id in the path must match the authenticated user's ID
- Requests from unauthorized domains will be rejected
- Input sanitization is performed on all user inputs
- SQL injection prevention through parameterized queries
- XSS protection through output encoding