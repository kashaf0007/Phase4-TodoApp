# Data Model: Enhanced MCP Tools with Advanced Capabilities

## Overview
This document defines the extended data models for the Enhanced MCP Tools feature, building upon the canonical data models specified in the constitution.

## Entity: Task (Extended)

### Fields
- **user_id** (UUID/String): Foreign key linking the task to a user
- **id** (UUID): Unique identifier for the task
- **title** (String): Title of the task (required, max 255 chars)
- **description** (Text): Detailed description of the task (optional)
- **completed** (Boolean): Whether the task is completed (default: false)
- **created_at** (DateTime): Timestamp when the task was created
- **updated_at** (DateTime): Timestamp when the task was last updated
- **tags** (JSON/Array): Array of tags associated with the task (optional)
- **category** (String): Category assigned to the task (optional)

### Relationships
- Belongs to a User (via user_id)

### Validation Rules
- Title is required and must be between 1-255 characters
- user_id is required and must reference an existing user
- created_at and updated_at are automatically managed by the ORM
- tags must be an array of valid tag names (max 10 tags, max 50 chars each)
- category must be a valid category name (max 100 chars)

### State Transitions
- Initially: completed = false
- On completion: completed = true
- On uncompletion: completed = false

## Entity: Tag

### Fields
- **id** (UUID): Unique identifier for the tag
- **name** (String): Name of the tag (required, unique per user)
- **user_id** (UUID/String): Foreign key linking the tag to a user
- **created_at** (DateTime): Timestamp when the tag was created

### Relationships
- Belongs to a User (via user_id)
- Many-to-many relationship with Task (via task_tags junction table)

### Validation Rules
- Name is required and must be between 1-50 characters
- Name must be unique per user
- user_id is required and must reference an existing user
- created_at is automatically managed by the ORM

### State Transitions
- Immutable once created (tags are soft-deleted by removing from tasks)

## Entity: Category

### Fields
- **id** (UUID): Unique identifier for the category
- **name** (String): Name of the category (required, unique per user)
- **user_id** (UUID/String): Foreign key linking the category to a user
- **parent_id** (UUID): Foreign key linking to parent category (optional, for hierarchy)
- **created_at** (DateTime): Timestamp when the category was created
- **updated_at** (DateTime): Timestamp when the category was last updated

### Relationships
- Belongs to a User (via user_id)
- Parent-child relationship with other Categories (via parent_id)
- One-to-many relationship with Task (via category field)

### Validation Rules
- Name is required and must be between 1-100 characters
- Name must be unique per user
- user_id is required and must reference an existing user
- parent_id must reference an existing category of the same user or be null
- created_at and updated_at are automatically managed by the ORM

### State Transitions
- Created when first assigned to a task or created explicitly
- Updated when renamed or moved in hierarchy
- Deleted when no tasks are assigned to it

## Database Constraints

### Indexes
- Index on Task.user_id for efficient user-specific queries
- Index on Task.tags for efficient tag-based queries (GIN index for JSON)
- Index on Task.category for efficient category-based queries
- Index on Task.created_at for chronological ordering
- Index on Tag.user_id and name for efficient tag lookup
- Index on Category.user_id and name for efficient category lookup

### Foreign Key Constraints
- Task.user_id references Users.id
- Tag.user_id references Users.id
- Category.user_id references Users.id
- Category.parent_id references Category.id

## SQLModel Implementation Notes

All models will be implemented using SQLModel with the following characteristics:
- Use of UUID primary keys for global uniqueness
- Automatic timestamp management using SQLModel's field options
- Proper relationship definitions using SQLModel's relationship features
- Validation at both the application and database levels
- Support for both sync and async operations
- Extended Task model to include tags and category fields