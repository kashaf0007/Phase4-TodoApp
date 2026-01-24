"""
Conversation schemas
"""
from pydantic import BaseModel
from datetime import datetime

class ConversationBase(BaseModel):
    user_id: str

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True