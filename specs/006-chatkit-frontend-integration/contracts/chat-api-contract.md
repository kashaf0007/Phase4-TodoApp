# API Contract: Chat Endpoint

## POST /api/{user_id}/chat

### Description
Main entry point for chat interactions with the AI assistant. This endpoint handles all user messages and routes them to the appropriate MCP tools based on the agent's interpretation.

### Path Parameters
- `user_id` (string, required): The authenticated user's unique identifier

### Request Body
```json
{
  "message": "string (required): The user's message to the AI assistant",
  "conversation_id": "string (optional): ID of the conversation to continue"
}
```

### Response Body
```json
{
  "response": "string: The AI assistant's response to the user",
  "conversation_id": "string: The conversation ID for this exchange",
  "tool_calls": [
    {
      "tool_name": "string: Name of the MCP tool called",
      "parameters": "object: Parameters passed to the tool",
      "result": "any: Result returned by the tool"
    }
  ],
  "confirmation": "string (optional): Friendly confirmation message for user actions",
  "error": "string (optional): Human-readable error message if applicable"
}
```

### Success Response
- Status Code: 200 OK
- Content-Type: application/json

### Error Responses
- 400 Bad Request: Invalid request format
- 401 Unauthorized: Missing or invalid authentication
- 403 Forbidden: Access denied due to domain restrictions
- 500 Internal Server Error: Backend processing error

### Security
- Requires authenticated user_id
- Domain-restricted access based on allowlist
- API keys handled server-side, never exposed to frontend