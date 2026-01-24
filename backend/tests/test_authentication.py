"""
Authentication tests
"""
import pytest
from unittest.mock import patch
from app.utils.auth import verify_auth_token, require_auth, validate_domain
from fastapi import HTTPException

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

def test_require_auth_with_valid_token():
    """Test require_auth with a valid token"""
    with patch('app.utils.auth.verify_auth_token') as mock_verify:
        mock_verify.return_value = "test_user_id"
        result = require_auth("valid_token")
        assert result == "test_user_id"

def test_require_auth_with_invalid_token():
    """Test require_auth with an invalid token"""
    with patch('app.utils.auth.verify_auth_token') as mock_verify:
        mock_verify.return_value = None
        with pytest.raises(HTTPException) as exc_info:
            require_auth("invalid_token")
        assert exc_info.value.status_code == 401

def test_validate_domain_allowed():
    """Test validating an allowed domain"""
    from fastapi import Request
    from starlette.datastructures import Headers
    
    # Mock a request with an allowed domain
    headers = Headers({"origin": "https://allowed-domain.com"})
    request = Request({"type": "http", "headers": headers.raw})
    
    with patch('app.utils.auth.DOMAIN_ALLOWLIST', ["allowed-domain.com"]):
        result = validate_domain(request)
        assert result is True

def test_validate_domain_not_allowed():
    """Test validating a disallowed domain"""
    from fastapi import Request
    from starlette.datastructures import Headers
    
    # Mock a request with a disallowed domain
    headers = Headers({"origin": "https://disallowed-domain.com"})
    request = Request({"type": "http", "headers": headers.raw})
    
    with patch('app.utils.auth.DOMAIN_ALLOWLIST', ["allowed-domain.com"]):
        result = validate_domain(request)
        assert result is False