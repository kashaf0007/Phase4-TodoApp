"""
Authorization tests
"""
import pytest
from app.utils.exceptions import UnauthorizedAccessException, ResourceNotFoundException

def test_unauthorized_access_exception():
    """Test UnauthorizedAccessException"""
    exception = UnauthorizedAccessException("user123", "resource456")
    
    assert exception.message == "User user123 does not have permission to access resource resource456"
    assert exception.error_code == "UNAUTHORIZED_ACCESS"

def test_resource_not_found_exception():
    """Test ResourceNotFoundException"""
    exception = ResourceNotFoundException("task", "task123")
    
    assert exception.message == "task with id task123 not found"
    assert exception.error_code == "RESOURCE_NOT_FOUND"

def test_invalid_parameters_exception():
    """Test InvalidParametersException"""
    details = {"field1": "error1", "field2": "error2"}
    exception = InvalidParametersException(details)
    
    assert exception.message == "Invalid parameters provided"
    assert exception.error_code == "INVALID_PARAMETERS"
    assert exception.details == details