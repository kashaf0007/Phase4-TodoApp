"""
Category model with SQLModel
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class CategoryBase(SQLModel):
    name: str = Field(min_length=1, max_length=100)
    user_id: str
    parent_id: Optional[str] = Field(default=None)

class Category(CategoryBase, table=True):
    __tablename__ = "categories"
    
    id: Optional[str] = Field(default_factory=generate_uuid, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)