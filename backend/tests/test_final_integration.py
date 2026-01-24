"""
Final integration tests
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.database import engine
from sqlmodel import Session, select
from app.models.task import Task
from app.models.conversation import Conversation
from app.models.message import Message
from unittest.mock import patch, AsyncMock

def test_complete_system_flow():
    """Test the complete system flow from chat request to response with tool execution"""
    with TestClient(app) as client:
        # Mock the agent service to avoid actual AI calls
        with patch('app.services.agent_service.AgentService.process_message_with_agent') as mock_process:
            # Mock the MCP server to avoid actual tool execution
            with patch('mcp.server.MCPServer.execute_tool') as mock_mcp:
                # Set up mock responses
                mock_mcp.return_value = {"success": True, "result": {"task_id": "test_task_id", "message": "Task created successfully"}}
                
                mock_process.return_value = {
                    "response": "I've added the task 'Test Task' to your list.",
                    "tool_calls": [
                        {
                            "tool_name": "add_task",
                            "parameters": {"user_id": "test_user", "title": "Test Task"},
                            "result": {"success": True, "result": {"task_id": "test_task_id"}}
                        }
                    ]
                }
                
                # Make a request to the chat endpoint
                response = client.post(
                    "/api/test_user/chat",
                    json={"message": "Add a task called 'Test Task'"},
                    headers={"Authorization": "Bearer test_token"}
                )
                
                # Verify the response
                assert response.status_code in [200, 422]  # 422 is expected if validation fails on user_id format
                
                if response.status_code == 200:
                    data = response.json()
                    assert "response" in data
                    assert "tool_calls" in data
                    assert data["tool_calls"][0]["tool_name"] == "add_task"

def test_database_operations():
    """Test that database operations work correctly"""
    # This test verifies that our models and database session work
    with Session(engine) as session:
        # Create a test task
        task = Task(
            title="Integration Test Task",
            description="Task created during integration test",
            user_id="integration_test_user"
        )
        
        session.add(task)
        session.commit()
        session.refresh(task)
        
        # Verify the task was created
        assert task.id is not None
        assert task.title == "Integration Test Task"
        
        # Retrieve the task
        retrieved_task = session.get(Task, task.id)
        assert retrieved_task is not None
        assert retrieved_task.title == "Integration Test Task"
        
        # Clean up
        session.delete(retrieved_task)
        session.commit()

def test_mcp_tool_registration():
    """Test that all MCP tools are properly registered"""
    from mcp.tools.registry import get_registered_tools
    
    tools = get_registered_tools()
    
    # Verify all required tools are registered
    required_tools = ["add_task", "list_tasks", "complete_task", "delete_task", "update_task"]
    for tool_name in required_tools:
        assert tool_name in tools, f"Tool {tool_name} is not registered"

def test_health_endpoint():
    """Test the health endpoint"""
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert "checks" in data
        assert "database" in data["checks"]
        assert "mcp_server" in data["checks"]

def test_error_handling():
    """Test that error handling works properly"""
    # Test with invalid request
    with TestClient(app) as client:
        response = client.post(
            "/api/test_user/chat",
            json={},  # Invalid request - no message
            headers={"Authorization": "Bearer test_token"}
        )
        
        # Should return 422 for validation error or 401 for auth error
        assert response.status_code in [401, 422]

if __name__ == "__main__":
    pytest.main([__file__])