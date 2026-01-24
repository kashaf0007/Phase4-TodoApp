"""
Custom exception handlers for the application
"""
from typing import Optional
from fastapi import HTTPException, status

class BaseAppException(Exception):
    """Base application exception"""
    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code

class ResourceNotFoundException(BaseAppException):
    """Raised when a requested resource is not found"""
    def __init__(self, resource_type: str, resource_id: str):
        super().__init__(
            message=f"{resource_type} with id {resource_id} not found",
            error_code="RESOURCE_NOT_FOUND"
        )

class UnauthorizedAccessException(BaseAppException):
    """Raised when a user doesn't have permission to access a resource"""
    def __init__(self, user_id: str, resource_id: str):
        super().__init__(
            message=f"User {user_id} does not have permission to access resource {resource_id}",
            error_code="UNAUTHORIZED_ACCESS"
        )

class InvalidParametersException(BaseAppException):
    """Raised when invalid parameters are provided"""
    def __init__(self, details: dict):
        super().__init__(
            message="Invalid parameters provided",
            error_code="INVALID_PARAMETERS"
        )
        self.details = details

def handle_exception(exception: BaseAppException):
    """Convert application exceptions to HTTP responses"""
    if isinstance(exception, ResourceNotFoundException):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "type": exception.error_code,
                    "message": exception.message
                }
            }
        )
    elif isinstance(exception, UnauthorizedAccessException):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": {
                    "type": exception.error_code,
                    "message": exception.message
                }
            }
        )
    elif isinstance(exception, InvalidParametersException):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "type": exception.error_code,
                    "message": exception.message,
                    "details": exception.details
                }
            }
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": {
                    "type": "INTERNAL_ERROR",
                    "message": str(exception)
                }
            }
        )