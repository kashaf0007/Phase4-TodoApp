"""
Conversation flow tests
"""
import pytest
from unittest.mock import Mock, AsyncMock
from app.services.conversation_service import ConversationService
from app.services.message_service import MessageService
from app.models.conversation import ConversationBase
from app.models.message import MessageBase

def test_conversation_creation():
    """Test creating a conversation"""
    mock_session = Mock()
    conversation_service = ConversationService(mock_session)
    
    conversation_data = ConversationBase(user_id="test_user")
    conversation_service.create_conversation(conversation_data)
    
    # Verify the session methods were called
    assert mock_session.add.called
    assert mock_session.commit.called

def test_message_persistence():
    """Test persisting messages"""
    mock_session = Mock()
    message_service = MessageService(mock_session)
    
    message_data = MessageBase(
        user_id="test_user",
        conversation_id="test_conv",
        role="user",
        content="test message"
    )
    message_service.create_message(message_data)
    
    # Verify the session methods were called
    assert mock_session.add.called
    assert mock_session.commit.called