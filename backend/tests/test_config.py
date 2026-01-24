"""
Configuration tests
"""
import pytest
from unittest.mock import patch
from app.config import NEON_DATABASE_URL, BETTER_AUTH_SECRET, OPENAI_API_KEY

def test_config_variables_loaded():
    """Test that configuration variables are loaded"""
    assert NEON_DATABASE_URL is not None
    assert BETTER_AUTH_SECRET is not None
    assert OPENAI_API_KEY is not None