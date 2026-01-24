"""
add_task MCP tool implementation
"""
from sqlmodel import Session, select
from ...app.models.task import Task, TaskBase
from ...app.services.database import engine
from ...app.utils.validation import validate_task_title
from ...app.utils.exceptions import InvalidParametersException
from .base import BaseTool
from typing import Dict, Any
import asyncio

async def add_task(user_id: str, title: str, description: str = None) -> Dict[str, Any]:
    """
    Creates a new task for a user.
    """
    # Validate inputs
    if not title or not validate_task_title(title):
        raise InvalidParametersException({"title": "Title is required and must be between 1-255 characters"})

    if description and len(description) > 10000:  # Max length validation
        raise InvalidParametersException({"description": "Description exceeds maximum length of 10000 characters"})

    # Create task data
    task_data = TaskBase(
        title=title,
        description=description,
        user_id=user_id
    )

    # Create and save the task in the database
    with Session(engine) as session:
        task = Task.model_validate(task_data)
        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "success": True,
            "task_id": task.id,
            "message": "Task created successfully"
        }

# Register the tool
from .registry import register_tool
register_tool("add_task")(add_task)