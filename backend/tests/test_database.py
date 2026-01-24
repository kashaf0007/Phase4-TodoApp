"""
Database connection tests
"""
import pytest
from app.services.database import engine
from sqlmodel import text

def test_database_connection():
    """Test that the database connection works"""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.fetchone()[0] == 1