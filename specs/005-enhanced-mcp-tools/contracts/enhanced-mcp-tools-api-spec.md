# Enhanced MCP Tools API Specification

## Overview
This document specifies the API contracts for the enhanced MCP tools that extend the existing task management capabilities with bulk operations, search and filtering, and task categorization and tagging.

## Enhanced Tool: bulk_add_tasks

### Description
Creates multiple tasks for a user in a single operation.

### Parameters
```json
{
  "user_id": "string (required)",
  "tasks": [
    {
      "title": "string (required)",
      "description": "string (optional)",
      "completed": "boolean (optional, default: false)"
    }
  ]
}
```

### Response
```json
{
  "success": "boolean",
  "results": [
    {
      "task_id": "string",
      "title": "string",
      "status": "string (success|error)",
      "error_message": "string (optional)"
    }
  ],
  "summary": {
    "total_processed": "integer",
    "successful": "integer",
    "failed": "integer"
  }
}
```

### Example Request
```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "tasks": [
    {
      "title": "Buy groceries",
      "description": "Milk, eggs, bread"
    },
    {
      "title": "Schedule appointment",
      "description": "With the dentist"
    },
    {
      "title": "Call mom",
      "completed": false
    }
  ]
}
```

### Example Response
```json
{
  "success": true,
  "results": [
    {
      "task_id": "987e6543-e21b-32d3-a456-426614174999",
      "title": "Buy groceries",
      "status": "success"
    },
    {
      "task_id": "876e5432-d10a-21c2-z345-315503063888",
      "title": "Schedule appointment",
      "status": "success"
    },
    {
      "task_id": "765d4321-c09z-10b1-y234-204492952777",
      "title": "Call mom",
      "status": "success"
    }
  ],
  "summary": {
    "total_processed": 3,
    "successful": 3,
    "failed": 0
  }
}
```

## Enhanced Tool: bulk_update_tasks

### Description
Updates multiple tasks for a user in a single operation.

### Parameters
```json
{
  "user_id": "string (required)",
  "task_ids": "array of strings (required)",
  "updates": {
    "title": "string (optional)",
    "description": "string (optional)",
    "completed": "boolean (optional)"
  }
}
```

### Response
```json
{
  "success": "boolean",
  "results": [
    {
      "task_id": "string",
      "status": "string (success|error)",
      "error_message": "string (optional)"
    }
  ],
  "summary": {
    "total_processed": "integer",
    "successful": "integer",
    "failed": "integer"
  }
}
```

### Example Request
```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "task_ids": [
    "987e6543-e21b-32d3-a456-426614174999",
    "876e5432-d10a-21c2-z345-315503063888"
  ],
  "updates": {
    "completed": true
  }
}
```

### Example Response
```json
{
  "success": true,
  "results": [
    {
      "task_id": "987e6543-e21b-32d3-a456-426614174999",
      "status": "success"
    },
    {
      "task_id": "876e5432-d10a-21c2-z345-315503063888",
      "status": "success"
    }
  ],
  "summary": {
    "total_processed": 2,
    "successful": 2,
    "failed": 0
  }
}
```

## Enhanced Tool: search_tasks

### Description
Finds tasks based on text search criteria.

### Parameters
```json
{
  "user_id": "string (required)",
  "query": "string (required)",
  "limit": "integer (optional, default: 20, max: 100)",
  "offset": "integer (optional, default: 0)"
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
      "updated_at": "string (ISO 8601 datetime)",
      "tags": "array of strings",
      "category": "string (optional)"
    }
  ],
  "total_matches": "integer",
  "query_used": "string"
}
```

### Example Request
```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "query": "groceries",
  "limit": 10,
  "offset": 0
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
      "updated_at": "2023-10-02T15:00:00Z",
      "tags": ["shopping", "urgent"],
      "category": "personal"
    }
  ],
  "total_matches": 1,
  "query_used": "groceries"
}
```

## Enhanced Tool: filter_tasks

### Description
Returns tasks based on filter criteria.

### Parameters
```json
{
  "user_id": "string (required)",
  "filters": {
    "status": "string (optional) - 'completed', 'pending', or 'all'",
    "category": "string (optional)",
    "tags": "array of strings (optional)",
    "date_range_start": "string (ISO 8601 date, optional)",
    "date_range_end": "string (ISO 8601 date, optional)"
  },
  "limit": "integer (optional, default: 20, max: 100)",
  "offset": "integer (optional, default: 0)"
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
      "updated_at": "string (ISO 8601 datetime)",
      "tags": "array of strings",
      "category": "string (optional)"
    }
  ],
  "total_matches": "integer",
  "filters_applied": "object"
}
```

### Example Request
```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "filters": {
    "status": "pending",
    "category": "work",
    "tags": ["important"]
  },
  "limit": 10
}
```

### Example Response
```json
{
  "success": true,
  "tasks": [
    {
      "id": "876e5432-d10a-21c2-z345-315503063888",
      "title": "Prepare quarterly report",
      "description": "Compile data and create presentation",
      "completed": false,
      "created_at": "2023-10-01T09:00:00Z",
      "updated_at": "2023-10-01T09:00:00Z",
      "tags": ["important", "report"],
      "category": "work"
    }
  ],
  "total_matches": 1,
  "filters_applied": {
    "status": "pending",
    "category": "work",
    "tags": ["important"]
  }
}
```

## Enhanced Tool: tag_task

### Description
Adds tags to an existing task.

### Parameters
```json
{
  "user_id": "string (required)",
  "task_id": "string (required)",
  "tags": "array of strings (required)"
}
```

### Response
```json
{
  "success": "boolean",
  "message": "string (optional)",
  "updated_tags": "array of strings"
}
```

### Example Request
```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "task_id": "987e6543-e21b-32d3-a456-426614174999",
  "tags": ["shopping", "urgent"]
}
```

### Example Response
```json
{
  "success": true,
  "message": "Tags added successfully",
  "updated_tags": ["shopping", "urgent", "recurring"]
}
}
```

## Enhanced Tool: add_task_category

### Description
Assigns a category to a task.

### Parameters
```json
{
  "user_id": "string (required)",
  "task_id": "string (required)",
  "category": "string (required)"
}
```

### Response
```json
{
  "success": "boolean",
  "message": "string (optional)",
  "updated_category": "string"
}
```

### Example Request
```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "task_id": "987e6543-e21b-32d3-a456-426614174999",
  "category": "personal"
}
```

### Example Response
```json
{
  "success": true,
  "message": "Category assigned successfully",
  "updated_category": "personal"
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