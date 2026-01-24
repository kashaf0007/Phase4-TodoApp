"""
Tag model with SQLModel
"""
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class TagBase(SQLModel):
    name: str = Field(min_length=1, max_length=50)
    user_id: str

class Tag(TagBase, table=True):
    __tablename__ = "tags"
    
    id: Optional[str] = Field(default_factory=generate_uuid, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)