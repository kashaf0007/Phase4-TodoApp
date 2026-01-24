"""
Message operations service
"""
from typing import List
from sqlmodel import Session, select
from datetime import datetime
from ..models.message import Message, MessageBase
from ..utils.exceptions import ResourceNotFoundException, UnauthorizedAccessException

class MessageService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_message(self, message_data: MessageBase) -> Message:
        """Create a new message"""
        message = Message.model_validate(message_data)
        self.db_session.add(message)
        self.db_session.commit()
        self.db_session.refresh(message)
        return message

    def get_message_by_id(self, message_id: str, user_id: str) -> Message:
        """Get a message by ID, ensuring it belongs to the user"""
        message = self.db_session.get(Message, message_id)
        if not message:
            raise ResourceNotFoundException("message", message_id)
        
        if message.user_id != user_id:
            raise UnauthorizedAccessException(user_id, message_id)
        
        return message

    def get_messages_by_conversation(self, conversation_id: str, user_id: str) -> List[Message]:
        """Get all messages for a conversation, ensuring user has access"""
        # First verify the user has access to this conversation
        from .conversation_service import ConversationService
        conversation_service = ConversationService(self.db_session)
        conversation_service.get_conversation_by_id(conversation_id, user_id)
        
        # Get messages for the conversation
        query = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc())
        
        messages = self.db_session.exec(query).all()
        return messages

    def get_messages_by_user(self, user_id: str) -> List[Message]:
        """Get all messages for a user"""
        query = select(Message).where(Message.user_id == user_id).order_by(Message.created_at.asc())
        messages = self.db_session.exec(query).all()
        return messages