"""
Message model definition for the Chat application.
This module defines the Message entity using SQLModel.
"""

from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Message(SQLModel, table=True):
    """
    Message model representing a message in a conversation.

    Attributes:
        id: Unique identifier for each message (Primary Key, Auto Increment)
        user_id: Links the message to a specific user (Not Null, Indexed)
        conversation_id: Links the message to a specific conversation (Not Null, Indexed)
        role: The role of the message sender (user or assistant) (Not Null)
        content: The content of the message (Not Null)
        created_at: Records when the message was created (Auto-generated)
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    conversation_id: str = Field(index=True)  # Links to conversation
    role: str = Field(nullable=False)  # Either 'user' or 'assistant'
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)