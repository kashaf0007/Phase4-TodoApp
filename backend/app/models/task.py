"""
Task model with SQLModel
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING, List
from datetime import datetime
import uuid
from .base import BaseSQLModel
from sqlalchemy import JSON

if TYPE_CHECKING:
    from .conversation import Conversation  # noqa: F401
    from .message import Message  # noqa: F401

def generate_uuid():
    return str(uuid.uuid4())

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=10000)
    completed: bool = Field(default=False)
    user_id: str
    tags: Optional[List[str]] = Field(default=[], sa_type=JSON)  # Store tags as JSON array
    category: Optional[str] = Field(default=None, max_length=100)  # Category name

class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: Optional[str] = Field(default_factory=generate_uuid, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships would go here if needed