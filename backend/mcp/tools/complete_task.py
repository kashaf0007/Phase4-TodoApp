"""
complete_task MCP tool implementation
"""
from sqlmodel import Session, select
from ...app.models.task import Task
from ...app.services.database import engine
from ...app.utils.exceptions import ResourceNotFoundException, UnauthorizedAccessException
from .base import BaseTool
from typing import Dict, Any
import asyncio

async def complete_task(user_id: str, task_id: str) -> Dict[str, Any]:
    """
    Marks a task as completed.
    """
    with Session(engine) as session:
        # Get the task
        task = session.get(Task, task_id)

        if not task:
            raise ResourceNotFoundException("task", task_id)

        if task.user_id != user_id:
            raise UnauthorizedAccessException(user_id, task_id)

        # Update the task to completed
        task.completed = True
        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "success": True,
            "message": "Task marked as completed"
        }

# Register the tool
from .registry import register_tool
register_tool("complete_task")(complete_task)