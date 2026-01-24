"""
Chat endpoint tests
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_chat_endpoint_exists(client):
    """Test that the chat endpoint exists"""
    # Since the chat endpoint is dynamic based on user_id, we'll test with a mock user_id
    response = client.post("/api/test_user_id/chat", json={"message": "hello"})
    # We expect a 401 because we're not providing auth, but the route should exist
    assert response.status_code in [401, 422]  # 401 for auth failure, 422 for validation issues