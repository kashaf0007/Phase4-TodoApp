"""
Pytest fixtures for the backend application
"""
import pytest
from app.main import app
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    with TestClient(app) as test_client:
        yield test_client