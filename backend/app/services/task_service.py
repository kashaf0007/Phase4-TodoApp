"""
Task operations service
"""
from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select
from ..models.task import Task, TaskBase
from ..utils.exceptions import ResourceNotFoundException, UnauthorizedAccessException
from ..utils.validation import validate_task_title, validate_task_description

class TaskService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_task(self, task_data: TaskBase) -> Task:
        """Create a new task"""
        # Validate input
        if not validate_task_title(task_data.title):
            from ..utils.exceptions import InvalidParametersException
            raise InvalidParametersException({"title": "Title must be between 1 and 255 characters"})
        
        if task_data.description and not validate_task_description(task_data.description):
            from ..utils.exceptions import InvalidParametersException
            raise InvalidParametersException({"description": "Description exceeds maximum length"})
        
        # Create and save the task
        task = Task.model_validate(task_data)
        self.db_session.add(task)
        self.db_session.commit()
        self.db_session.refresh(task)
        return task

    def get_task_by_id(self, task_id: str, user_id: str) -> Task:
        """Get a task by ID, ensuring it belongs to the user"""
        task = self.db_session.get(Task, task_id)
        if not task:
            raise ResourceNotFoundException("task", task_id)
        
        if task.user_id != user_id:
            raise UnauthorizedAccessException(user_id, task_id)
        
        return task

    def get_tasks_by_user(self, user_id: str, completed: Optional[bool] = None) -> List[Task]:
        """Get all tasks for a user, optionally filtered by completion status"""
        query = select(Task).where(Task.user_id == user_id)
        
        if completed is not None:
            query = query.where(Task.completed == completed)
        
        tasks = self.db_session.exec(query).all()
        return tasks

    def update_task(self, task_id: str, user_id: str, update_data: dict) -> Task:
        """Update a task, ensuring it belongs to the user"""
        task = self.get_task_by_id(task_id, user_id)
        
        # Validate input if updating title or description
        if "title" in update_data and update_data["title"] is not None:
            if not validate_task_title(update_data["title"]):
                from ..utils.exceptions import InvalidParametersException
                raise InvalidParametersException({"title": "Title must be between 1 and 255 characters"})
        
        if "description" in update_data and update_data["description"] is not None:
            if not validate_task_description(update_data["description"]):
                from ..utils.exceptions import InvalidParametersException
                raise InvalidParametersException({"description": "Description exceeds maximum length"})
        
        # Update the task
        for field, value in update_data.items():
            setattr(task, field, value)
        
        task.updated_at = datetime.utcnow()
        self.db_session.add(task)
        self.db_session.commit()
        self.db_session.refresh(task)
        return task

    def delete_task(self, task_id: str, user_id: str) -> bool:
        """Delete a task, ensuring it belongs to the user"""
        task = self.get_task_by_id(task_id, user_id)
        
        self.db_session.delete(task)
        self.db_session.commit()
        return True

    def complete_task(self, task_id: str, user_id: str) -> Task:
        """Mark a task as completed"""
        return self.update_task(task_id, user_id, {"completed": True})