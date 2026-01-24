"""
Error response schemas
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any

class ErrorDetail(BaseModel):
    type: str
    message: str
    details: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    error: ErrorDetail