# OpenAPI Specification: Chat Endpoint

## Overview
This document specifies the API contract for the single entry point of the Todo AI Chatbot application.

## Endpoint: POST /api/{user_id}/chat

### Description
The primary conversational endpoint that handles all user interactions with the AI assistant. This endpoint receives user messages, orchestrates the conversation flow, executes agent reasoning with MCP tools, and returns responses with tool call logs.

### Path Parameters
- **user_id** (string, required): The unique identifier of the authenticated user

### Request Body
```json
{
  "message": "string (required)",
  "metadata": {
    "timestamp": "string (optional)",
    "source": "string (optional)"
  }
}
```

### Response Schema
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

### HTTP Status Codes
- **200 OK**: Successful response from the AI assistant
- **400 Bad Request**: Invalid request format or missing required fields
- **401 Unauthorized**: Invalid or missing authentication
- **403 Forbidden**: User does not have permission to access this resource
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Unexpected server error

### Authentication
- Requires valid Better Auth token in Authorization header
- user_id in path must match authenticated user

### Example Request
```http
POST /api/123e4567-e89b-12d3-a456-426614174000/chat
Authorization: Bearer <auth_token>
Content-Type: application/json

{
  "message": "Add a task to buy groceries"
}
```

### Example Response
```http
HTTP/1.1 200 OK
Content-Type: application/json

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

### Error Response Schema
```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": {}
  }
}
```

### Security Requirements
- All requests must include a valid Better Auth token
- The user_id in the path must match the authenticated user's ID
- Requests from unauthorized domains will be rejected