"""
delete_task MCP tool implementation
"""
from sqlmodel import Session
from ...app.models.task import Task
from ...app.services.database import engine
from ...app.utils.exceptions import ResourceNotFoundException, UnauthorizedAccessException
from .base import BaseTool
from typing import Dict, Any
import asyncio

async def delete_task(user_id: str, task_id: str) -> Dict[str, Any]:
    """
    Deletes a task.
    """
    with Session(engine) as session:
        # Get the task
        task = session.get(Task, task_id)

        if not task:
            raise ResourceNotFoundException("task", task_id)

        if task.user_id != user_id:
            raise UnauthorizedAccessException(user_id, task_id)

        # Delete the task
        session.delete(task)
        session.commit()

        return {
            "success": True,
            "message": "Task deleted successfully"
        }

# Register the tool
from .registry import register_tool
register_tool("delete_task")(delete_task)