# MCP Tools Specification: Backend & MCP Architecture

## Overview
This document specifies the Model Context Protocol (MCP) tools that the AI agent will use to interact with the backend system. These tools provide the only interface for state-changing operations as required by the constitution.

## Tool: add_task

### Description
Creates a new task for a user.

### Parameters
```json
{
  "user_id": "string (required)",
  "title": "string (required)",
  "description": "string (optional)"
}
```

### Response
```json
{
  "success": "boolean",
  "task_id": "string",
  "message": "string (optional)"
}
```

### Example Request
```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

### Example Response
```json
{
  "success": true,
  "task_id": "987e6543-e21b-32d3-a456-426614174999",
  "message": "Task created successfully"
}
```

## Tool: list_tasks

### Description
Retrieves all tasks for a user, optionally filtered by completion status.

### Parameters
```json
{
  "user_id": "string (required)",
  "completed": "boolean (optional, default: null)"
}
```

### Response
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

### Example Request
```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "completed": false
}
```

### Example Response
```json
{
  "success": true,
  "tasks": [
    {
      "id": "987e6543-e21b-32d3-a456-426614174999",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2023-10-02T15:00:00Z",
      "updated_at": "2023-10-02T15:00:00Z"
    }
  ],
  "count": 1
}
```

## Tool: complete_task

### Description
Marks a task as completed.

### Parameters
```json
{
  "user_id": "string (required)",
  "task_id": "string (required)"
}
```

### Response
```json
{
  "success": "boolean",
  "message": "string (optional)"
}
```

### Example Request
```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "task_id": "987e6543-e21b-32d3-a456-426614174999"
}
```

### Example Response
```json
{
  "success": true,
  "message": "Task marked as completed"
}
```

## Tool: delete_task

### Description
Deletes a task.

### Parameters
```json
{
  "user_id": "string (required)",
  "task_id": "string (required)"
}
```

### Response
```json
{
  "success": "boolean",
  "message": "string (optional)"
}
```

### Example Request
```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "task_id": "987e6543-e21b-32d3-a456-426614174999"
}
```

### Example Response
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

## Tool: update_task

### Description
Updates properties of a task.

### Parameters
```json
{
  "user_id": "string (required)",
  "task_id": "string (required)",
  "title": "string (optional)",
  "description": "string (optional)",
  "completed": "boolean (optional)"
}
```

### Response
```json
{
  "success": "boolean",
  "message": "string (optional)"
}
```

### Example Request
```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "task_id": "987e6543-e21b-32d3-a456-426614174999",
  "title": "Buy groceries and cook dinner",
  "completed": false
}
```

### Example Response
```json
{
  "success": true,
  "message": "Task updated successfully"
}
```

## Common Error Responses

### Invalid Parameters
```json
{
  "success": false,
  "error": {
    "type": "invalid_parameters",
    "message": "One or more parameters are invalid",
    "details": {
      "field": "error_message"
    }
  }
}
```

### Resource Not Found
```json
{
  "success": false,
  "error": {
    "type": "resource_not_found",
    "message": "The requested resource was not found",
    "details": {
      "resource_type": "task|conversation|message",
      "resource_id": "string"
    }
  }
}
```

### Unauthorized Access
```json
{
  "success": false,
  "error": {
    "type": "unauthorized_access",
    "message": "User does not have permission to access this resource",
    "details": {
      "user_id": "string",
      "resource_id": "string"
    }
  }
}
```

## Tool Execution Guarantees

1. **Statelessness**: Each tool operates independently without relying on in-memory state
2. **Deterministic Output**: Same inputs always produce the same output structure
3. **Explicit Parameters**: All required parameters must be provided explicitly
4. **Structured Response**: All tools return a consistent response structure with success flag
5. **Logging**: All tool executions are logged with parameters and results