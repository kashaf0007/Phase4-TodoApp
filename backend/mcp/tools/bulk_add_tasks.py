"""
bulk_add_tasks MCP tool implementation
"""
from sqlmodel import Session
from ...app.models.task import Task
from ...app.services.database import engine
from ...app.utils.validation import validate_task_title
from ...app.utils.exceptions import InvalidParametersException
from .base import BaseTool
from typing import Dict, Any, List
import asyncio

async def bulk_add_tasks(user_id: str, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Creates multiple tasks for a user in a single operation.
    """
    # Validate inputs
    if not tasks or not isinstance(tasks, list):
        raise InvalidParametersException({"tasks": "Tasks must be a non-empty list"})

    for i, task_data in enumerate(tasks):
        if not isinstance(task_data, dict):
            raise InvalidParametersException({f"tasks[{i}]": "Each task must be an object"})

        title = task_data.get("title")
        if not title or not validate_task_title(title):
            raise InvalidParametersException({f"tasks[{i}].title": "Title is required and must be between 1-255 characters"})

    # Process tasks in the database
    with Session(engine) as session:
        results = []
        successful_count = 0
        failed_count = 0

        for i, task_data in enumerate(tasks):
            try:
                # Create and save the task
                task = Task(
                    title=task_data["title"],
                    description=task_data.get("description"),
                    completed=task_data.get("completed", False),
                    user_id=user_id,
                    tags=task_data.get("tags", []),
                    category=task_data.get("category")
                )

                session.add(task)
                session.commit()
                session.refresh(task)

                results.append({
                    "task_id": task.id,
                    "title": task.title,
                    "status": "success"
                })
                successful_count += 1

            except Exception as e:
                results.append({
                    "title": task_data.get("title"),
                    "status": "error",
                    "error_message": str(e)
                })
                failed_count += 1

        return {
            "success": failed_count == 0,  # Overall success only if no failures
            "results": results,
            "summary": {
                "total_processed": len(tasks),
                "successful": successful_count,
                "failed": failed_count
            }
        }

# Register the tool
from .registry import register_tool
register_tool("bulk_add_tasks")(bulk_add_tasks)