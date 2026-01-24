"""
Chat request/response schemas
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatRequest(BaseModel):
    message: str
    metadata: Optional[Dict[str, Any]] = None

class ToolCallLog(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]
    result: Dict[str, Any]

class ChatResponse(BaseModel):
    response: str
    tool_calls: List[ToolCallLog]
    conversation_id: str
    message_id: str

class ErrorResponse(BaseModel):
    error: Dict[str, Any]