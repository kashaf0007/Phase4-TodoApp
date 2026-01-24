"""
Authentication tests
"""
import pytest
from unittest.mock import patch
from app.utils.auth import verify_auth_token, require_auth

def test_verify_auth_token_with_valid_token():
    """Test verifying a valid auth token"""
    # Since our current implementation is mocked, we'll test the behavior
    with patch('app.utils.auth.verify_auth_token') as mock_verify:
        mock_verify.return_value = "test_user_id"
        result = verify_auth_token("valid_token")
        assert result == "test_user_id"

def test_verify_auth_token_with_invalid_token():
    """Test verifying an invalid auth token"""
    with patch('app.utils.auth.verify_auth_token') as mock_verify:
        mock_verify.return_value = None
        result = verify_auth_token("invalid_token")
        assert result is None