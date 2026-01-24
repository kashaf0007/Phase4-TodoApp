"""
update_task MCP tool implementation
"""
from sqlmodel import Session
from ...app.models.task import Task
from ...app.services.database import engine
from ...app.utils.exceptions import ResourceNotFoundException, UnauthorizedAccessException
from ...app.utils.validation import validate_task_title, validate_task_description
from .base import BaseTool
from typing import Dict, Any, Optional
import asyncio

async def update_task(
    user_id: str,
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Updates properties of a task.
    """
    with Session(engine) as session:
        # Get the task
        task = session.get(Task, task_id)

        if not task:
            raise ResourceNotFoundException("task", task_id)

        if task.user_id != user_id:
            raise UnauthorizedAccessException(user_id, task_id)

        # Validate inputs if they are provided
        if title is not None:
            if not validate_task_title(title):
                from ...app.utils.exceptions import InvalidParametersException
                raise InvalidParametersException({"title": "Title must be between 1-255 characters"})

        if description is not None:
            if not validate_task_description(description):
                from ...app.utils.exceptions import InvalidParametersException
                raise InvalidParametersException({"description": "Description exceeds maximum length"})

        # Update the task with provided fields
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed

        # Update the timestamp
        from datetime import datetime
        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "success": True,
            "message": "Task updated successfully"
        }

# Register the tool
from .registry import register_tool
register_tool("update_task")(update_task)