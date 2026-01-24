"""
bulk_update_tasks MCP tool implementation
"""
from sqlmodel import Session, select
from ...app.models.task import Task
from ...app.services.database import engine
from ...app.utils.exceptions import ResourceNotFoundException, UnauthorizedAccessException
from .base import BaseTool
from typing import Dict, Any, List
import asyncio

async def bulk_update_tasks(user_id: str, task_ids: List[str], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Updates multiple tasks for a user in a single operation.
    """
    # Validate inputs
    if not task_ids or not isinstance(task_ids, list):
        from ...app.utils.exceptions import InvalidParametersException
        raise InvalidParametersException({"task_ids": "task_ids must be a non-empty list"})

    if not updates or not isinstance(updates, dict):
        raise InvalidParametersException({"updates": "updates must be a non-empty object"})

    # Process updates in the database
    with Session(engine) as session:
        results = []
        successful_count = 0
        failed_count = 0

        for task_id in task_ids:
            try:
                # Get the task
                task = session.get(Task, task_id)

                if not task:
                    raise ResourceNotFoundException("task", task_id)

                if task.user_id != user_id:
                    raise UnauthorizedAccessException(user_id, task_id)

                # Apply updates
                for field, value in updates.items():
                    if hasattr(task, field):
                        setattr(task, field, value)

                # Update the timestamp
                from datetime import datetime
                task.updated_at = datetime.utcnow()

                session.add(task)
                session.commit()
                session.refresh(task)

                results.append({
                    "task_id": task.id,
                    "status": "success"
                })
                successful_count += 1

            except Exception as e:
                results.append({
                    "task_id": task_id,
                    "status": "error",
                    "error_message": str(e)
                })
                failed_count += 1

        return {
            "success": failed_count == 0,  # Overall success only if no failures
            "results": results,
            "summary": {
                "total_processed": len(task_ids),
                "successful": successful_count,
                "failed": failed_count
            }
        }

# Register the tool
from .registry import register_tool
register_tool("bulk_update_tasks")(bulk_update_tasks)