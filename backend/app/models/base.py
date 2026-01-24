"""
Base SQLModel class with common fields
"""
from sqlmodel import SQLModel as _SQLModel
from sqlalchemy import Column, DateTime, func
from typing import Optional
import uuid

class SQLModel(_SQLModel):
    class Config:
        arbitrary_types_allowed = True

def generate_uuid():
    return str(uuid.uuid4())

class BaseSQLModel(SQLModel):
    id: Optional[str] = None