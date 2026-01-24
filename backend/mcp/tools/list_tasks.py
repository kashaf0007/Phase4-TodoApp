"""
list_tasks MCP tool implementation
"""
from sqlmodel import Session, select
from ...app.models.task import Task
from ...app.services.database import engine
from .base import BaseTool
from typing import Dict, Any, Optional
import asyncio

async def list_tasks(user_id: str, completed: Optional[bool] = None) -> Dict[str, Any]:
    """
    Retrieves all tasks for a user, optionally filtered by completion status.
    """
    with Session(engine) as session:
        # Build query based on whether we're filtering by completion status
        query = select(Task).where(Task.user_id == user_id)

        if completed is not None:
            query = query.where(Task.completed == completed)

        tasks = session.exec(query).all()

        # Format tasks for response
        formatted_tasks = []
        for task in tasks:
            formatted_tasks.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None
            })

        return {
            "success": True,
            "tasks": formatted_tasks,
            "count": len(formatted_tasks)
        }

# Register the tool
from .registry import register_tool
register_tool("list_tasks")(list_tasks)