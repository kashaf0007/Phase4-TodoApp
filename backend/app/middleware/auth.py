"""
Authentication middleware
"""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from .auth import verify_auth_token, validate_domain
from ..utils.exceptions import UnauthorizedAccessException

async def auth_middleware(request: Request, call_next):
    """
    Middleware to handle authentication for all requests
    """
    # Validate domain for security
    if not validate_domain(request):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "error": {
                    "type": "FORBIDDEN_DOMAIN",
                    "message": "Requests from this domain are not allowed"
                }
            }
        )
    
    # Extract token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        # For certain endpoints, we might allow unauthenticated access
        # For now, we'll require authentication for all endpoints
        pass  # We'll handle auth in individual endpoints
    
    token = auth_header.split(" ")[1] if auth_header else None
    
    # Verify the token
    user_id = verify_auth_token(token) if token else None
    
    # Add user_id to request state for use in endpoints
    request.state.user_id = user_id
    
    response = await call_next(request)
    return response