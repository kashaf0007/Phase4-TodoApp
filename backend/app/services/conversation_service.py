"""
Conversation operations service
"""
from typing import List
from sqlmodel import Session, select
from datetime import datetime
from ..models.conversation import Conversation, ConversationBase
from ..utils.exceptions import ResourceNotFoundException, UnauthorizedAccessException

class ConversationService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_conversation(self, conversation_data: ConversationBase) -> Conversation:
        """Create a new conversation"""
        conversation = Conversation.model_validate(conversation_data)
        self.db_session.add(conversation)
        self.db_session.commit()
        self.db_session.refresh(conversation)
        return conversation

    def get_conversation_by_id(self, conversation_id: str, user_id: str) -> Conversation:
        """Get a conversation by ID, ensuring it belongs to the user"""
        conversation = self.db_session.get(Conversation, conversation_id)
        if not conversation:
            raise ResourceNotFoundException("conversation", conversation_id)
        
        if conversation.user_id != user_id:
            raise UnauthorizedAccessException(user_id, conversation_id)
        
        return conversation

    def get_conversations_by_user(self, user_id: str) -> List[Conversation]:
        """Get all conversations for a user"""
        query = select(Conversation).where(Conversation.user_id == user_id)
        conversations = self.db_session.exec(query).all()
        return conversations

    def update_conversation(self, conversation_id: str, user_id: str) -> Conversation:
        """Update a conversation's updated_at timestamp"""
        conversation = self.get_conversation_by_id(conversation_id, user_id)
        
        conversation.updated_at = datetime.utcnow()
        self.db_session.add(conversation)
        self.db_session.commit()
        self.db_session.refresh(conversation)
        return conversation