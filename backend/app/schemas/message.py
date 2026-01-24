"""
Message schemas
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class MessageBase(BaseModel):
    user_id: str
    conversation_id: str
    role: Literal["user", "assistant"]
    content: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True