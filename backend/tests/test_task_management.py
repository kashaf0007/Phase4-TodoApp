"""
Task management tests
"""
import pytest
from unittest.mock import Mock, patch
from app.services.task_service import TaskService
from app.models.task import TaskBase

def test_create_task():
    """Test creating a task"""
    mock_session = Mock()
    task_service = TaskService(mock_session)
    
    task_data = TaskBase(
        title="Test Task",
        description="Test Description",
        user_id="test_user"
    )
    
    with patch.object(mock_session, 'add'), \
         patch.object(mock_session, 'commit'), \
         patch.object(mock_session, 'refresh'):
        task_service.create_task(task_data)
        
        # Verify the session methods were called
        assert mock_session.add.called
        assert mock_session.commit.called
        assert mock_session.refresh.called

def test_get_tasks_by_user():
    """Test getting tasks for a user"""
    mock_session = Mock()
    task_service = TaskService(mock_session)
    
    # Mock the exec method to return a list of tasks
    mock_exec_result = Mock()
    mock_exec_result.all.return_value = []
    mock_session.exec.return_value = mock_exec_result
    
    tasks = task_service.get_tasks_by_user("test_user")
    
    # Verify the session methods were called
    assert mock_session.exec.called
    assert len(tasks) == 0  # Since we mocked an empty list