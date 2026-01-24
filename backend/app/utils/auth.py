"""
Better Auth integration utilities
"""
from typing import Optional
from fastapi import HTTPException, status, Request
from ..config import BETTER_AUTH_SECRET, BETTER_AUTH_URL
import jwt
from datetime import datetime

def verify_auth_token(token: str) -> Optional[str]:
    """
    Verify the Better Auth token and return the user_id if valid
    """
    # This is a simplified implementation
    # In a real implementation, you would call the Better Auth API
    # to verify the token and get the user information

    if not token:
        return None

    try:
        # In a real implementation, you would decode the JWT token
        # using the BETTER_AUTH_SECRET and extract the user_id
        # decoded_token = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"])
        # return decoded_token.get("user_id")

        # For now, we'll just return a mock user_id
        # This would come from token validation in a real implementation
        return "mock_user_id"
    except jwt.InvalidTokenError:
        return None
    except Exception:
        return None

def require_auth(token: str) -> str:
    """
    Require authentication and return the user_id
    Raises HTTPException if authentication fails
    """
    user_id = verify_auth_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing authentication token"
        )
    return user_id

def validate_domain(request: Request) -> bool:
    """
    Validate that the request is coming from an allowed domain
    """
    origin = request.headers.get("origin")
    if not origin:
        # If no origin header, check host header
        origin = request.headers.get("host")

    if not origin:
        return True  # If no origin info, allow by default

    # Extract domain from origin URL
    import re
    domain_match = re.search(r"https?://([^/]+)", origin)
    if domain_match:
        domain = domain_match.group(1)
    else:
        domain = origin

    # Check if domain is in allowlist
    from ..config import DOMAIN_ALLOWLIST
    return domain in DOMAIN_ALLOWLIST