"""
Enhanced task operations service with bulk, search, filter, and tag operations
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlmodel import Session, select, and_, func
from sqlalchemy import or_, text
from ..models.task import Task, TaskBase
from ..models.tag import Tag
from ..models.category import Category
from ..utils.exceptions import ResourceNotFoundException, UnauthorizedAccessException
from ..utils.validation import validate_task_title, validate_task_description

class TaskEnhancedService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def bulk_add_tasks(self, user_id: str, tasks_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Add multiple tasks in a single operation"""
        results = []
        successful_count = 0
        failed_count = 0
        
        for task_data in tasks_data:
            try:
                # Validate input
                title = task_data.get("title")
                if not title or not validate_task_title(title):
                    results.append({
                        "title": title,
                        "status": "error",
                        "error_message": "Title is required and must be between 1 and 255 characters"
                    })
                    failed_count += 1
                    continue
                
                description = task_data.get("description")
                if description and not validate_task_description(description):
                    results.append({
                        "title": title,
                        "status": "error",
                        "error_message": "Description exceeds maximum length"
                    })
                    failed_count += 1
                    continue
                
                # Create and save the task
                task = Task(
                    title=title,
                    description=description,
                    completed=task_data.get("completed", False),
                    user_id=user_id,
                    tags=task_data.get("tags", []),
                    category=task_data.get("category")
                )
                
                self.db_session.add(task)
                self.db_session.commit()
                self.db_session.refresh(task)
                
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
                "total_processed": len(tasks_data),
                "successful": successful_count,
                "failed": failed_count
            }
        }

    def bulk_update_tasks(self, user_id: str, task_ids: List[str], updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update multiple tasks in a single operation"""
        results = []
        successful_count = 0
        failed_count = 0
        
        for task_id in task_ids:
            try:
                # Get the task and verify ownership
                task = self.db_session.get(Task, task_id)
                if not task:
                    results.append({
                        "task_id": task_id,
                        "status": "error",
                        "error_message": f"Task with id {task_id} not found"
                    })
                    failed_count += 1
                    continue
                
                if task.user_id != user_id:
                    results.append({
                        "task_id": task_id,
                        "status": "error",
                        "error_message": "Unauthorized to update this task"
                    })
                    failed_count += 1
                    continue
                
                # Apply updates
                for field, value in updates.items():
                    if hasattr(task, field):
                        setattr(task, field, value)
                
                task.updated_at = datetime.utcnow()
                self.db_session.add(task)
                self.db_session.commit()
                self.db_session.refresh(task)
                
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

    def search_tasks(self, user_id: str, query: str, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """Search tasks by text query"""
        # Build the search query using LIKE for partial matches
        search_filter = or_(
            Task.title.ilike(f"%{query}%"),
            Task.description.ilike(f"%{query}%")
        )
        
        # Add user_id filter
        search_filter = and_(search_filter, Task.user_id == user_id)
        
        # Execute the query with pagination
        tasks = self.db_session.exec(
            select(Task)
            .where(search_filter)
            .offset(offset)
            .limit(limit)
        ).all()
        
        # Count total matches for pagination info
        total_matches = self.db_session.exec(
            select(func.count(Task.id))
            .where(search_filter)
        ).one()
        
        return {
            "success": True,
            "tasks": tasks,
            "total_matches": total_matches,
            "query_used": query
        }

    def filter_tasks(self, user_id: str, filters: Dict[str, Any], limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """Filter tasks by various criteria"""
        # Start with user_id filter
        query = select(Task).where(Task.user_id == user_id)
        
        # Apply status filter
        if "status" in filters:
            status = filters["status"]
            if status == "completed":
                query = query.where(Task.completed == True)
            elif status == "pending":
                query = query.where(Task.completed == False)
        
        # Apply category filter
        if "category" in filters:
            query = query.where(Task.category == filters["category"])
        
        # Apply tags filter
        if "tags" in filters and isinstance(filters["tags"], list):
            # This is a simplified tag filtering - in a real implementation,
            # you might need more complex JSON querying depending on your database
            for tag in filters["tags"]:
                # This is a simplified approach - actual implementation depends on database
                # For PostgreSQL with JSON, you might use: Task.tags.op('@>')([tag])
                pass  # Placeholder for tag filtering logic
        
        # Apply date range filter
        if "date_range_start" in filters:
            from datetime import datetime
            start_date = datetime.fromisoformat(filters["date_range_start"].replace('Z', '+00:00'))
            query = query.where(Task.created_at >= start_date)
        
        if "date_range_end" in filters:
            from datetime import datetime
            end_date = datetime.fromisoformat(filters["date_range_end"].replace('Z', '+00:00'))
            query = query.where(Task.created_at <= end_date)
        
        # Execute the query with pagination
        tasks = self.db_session.exec(
            query
            .offset(offset)
            .limit(limit)
        ).all()
        
        # Count total matches for pagination info
        count_query = query.with_only_columns(func.count(Task.id)).order_by(None)
        total_matches = self.db_session.exec(count_query).one()
        
        return {
            "success": True,
            "tasks": tasks,
            "total_matches": total_matches,
            "filters_applied": filters
        }

    def tag_task(self, user_id: str, task_id: str, tags: List[str]) -> Dict[str, Any]:
        """Add tags to a task"""
        # Get the task and verify ownership
        task = self.db_session.get(Task, task_id)
        if not task:
            raise ResourceNotFoundException("task", task_id)
        
        if task.user_id != user_id:
            raise UnauthorizedAccessException(user_id, task_id)
        
        # Add new tags to existing tags (avoid duplicates)
        existing_tags = set(task.tags or [])
        new_tags = set(tags)
        all_tags = list(existing_tags.union(new_tags))
        
        # Update the task with the new tags
        task.tags = all_tags
        task.updated_at = datetime.utcnow()
        self.db_session.add(task)
        self.db_session.commit()
        self.db_session.refresh(task)
        
        return {
            "success": True,
            "message": "Tags added successfully",
            "updated_tags": task.tags
        }

    def add_task_category(self, user_id: str, task_id: str, category: str) -> Dict[str, Any]:
        """Assign a category to a task"""
        # Get the task and verify ownership
        task = self.db_session.get(Task, task_id)
        if not task:
            raise ResourceNotFoundException("task", task_id)
        
        if task.user_id != user_id:
            raise UnauthorizedAccessException(user_id, task_id)
        
        # Update the task with the new category
        task.category = category
        task.updated_at = datetime.utcnow()
        self.db_session.add(task)
        self.db_session.commit()
        self.db_session.refresh(task)
        
        return {
            "success": True,
            "message": "Category assigned successfully",
            "updated_category": task.category
        }