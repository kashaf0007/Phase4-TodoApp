"""
Schema validation tests
"""
import pytest
from app.schemas.task import TaskCreate, TaskUpdate
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.conversation import ConversationCreate
from app.schemas.message import MessageCreate

def test_task_create_schema():
    """Test TaskCreate schema validation"""
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "user_id": "test_user_id"
    }
    task = TaskCreate(**task_data)
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.user_id == "test_user_id"

def test_task_update_schema():
    """Test TaskUpdate schema validation"""
    update_data = {
        "title": "Updated Task",
        "completed": True
    }
    task_update = TaskUpdate(**update_data)
    assert task_update.title == "Updated Task"
    assert task_update.completed is True

def test_chat_request_schema():
    """Test ChatRequest schema validation"""
    chat_data = {
        "message": "Hello, world!",
        "metadata": {"source": "test"}
    }
    chat_req = ChatRequest(**chat_data)
    assert chat_req.message == "Hello, world!"
    assert chat_req.metadata == {"source": "test"}

def test_conversation_create_schema():
    """Test ConversationCreate schema validation"""
    conv_data = {
        "user_id": "test_user_id"
    }
    conv = ConversationCreate(**conv_data)
    assert conv.user_id == "test_user_id"

def test_message_create_schema():
    """Test MessageCreate schema validation"""
    msg_data = {
        "user_id": "test_user_id",
        "conversation_id": "test_conv_id",
        "role": "user",
        "content": "Test message"
    }
    msg = MessageCreate(**msg_data)
    assert msg.user_id == "test_user_id"
    assert msg.conversation_id == "test_conv_id"
    assert msg.role == "user"
    assert msg.content == "Test message"