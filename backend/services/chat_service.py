"""
Chat Service
Handles business logic for chat conversations and message processing.
"""

import sys
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from sqlmodel import Session, select

# Add the backend directory to the Python path to import models
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.models.message import Message
from src.models.conversation import Conversation


class ChatService:
    """
    Service class for handling chat-related operations.
    """

    @staticmethod
    def create_conversation(session: Session, user_id: str) -> Conversation:
        """
        Create a new conversation for a user.
        """
        conversation_id = str(uuid.uuid4())
        conversation = Conversation(
            id=conversation_id,
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    @staticmethod
    def get_conversation(session: Session, conversation_id: str, user_id: str) -> Optional[Conversation]:
        """
        Retrieve a specific conversation for a user.
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        return session.exec(statement).first()

    @staticmethod
    def create_message(
        session: Session,
        user_id: str,
        conversation_id: str,
        role: str,
        content: str
    ) -> Message:
        """
        Create a new message in a conversation.
        """
        message = Message(
            user_id=user_id,
            conversation_id=conversation_id,
            role=role,
            content=content,
            created_at=datetime.utcnow()
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message

    @staticmethod
    def get_messages_for_conversation(
        session: Session,
        conversation_id: str,
        user_id: str,
        limit: int = 50
    ) -> List[Message]:
        """
        Retrieve messages for a specific conversation.
        """
        statement = select(Message).where(
            Message.conversation_id == conversation_id,
            Message.user_id == user_id
        ).order_by(Message.created_at.desc()).limit(limit)
        messages = session.exec(statement).all()
        return list(reversed(messages))  # Return in chronological order

    @staticmethod
    def get_recent_conversations(
        session: Session,
        user_id: str,
        limit: int = 10
    ) -> List[Conversation]:
        """
        Retrieve recent conversations for a user.
        """
        statement = select(Conversation).where(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc()).limit(limit)
        return session.exec(statement).all()