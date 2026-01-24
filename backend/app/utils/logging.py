"""
Structured logging utilities
"""
import logging
from typing import Dict, Any
import json
from datetime import datetime

def setup_logging(log_level: str = "INFO"):
    """
    Set up structured logging for the application
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def log_event(event_type: str, user_id: str, details: Dict[str, Any] = None):
    """
    Log an event with structured data
    """
    logger = logging.getLogger(__name__)
    
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "user_id": user_id,
        "details": details or {}
    }
    
    logger.info(json.dumps(log_data))

def log_tool_call(tool_name: str, user_id: str, parameters: Dict[str, Any], result: Dict[str, Any]):
    """
    Log an MCP tool call
    """
    log_event(
        event_type="tool_call",
        user_id=user_id,
        details={
            "tool_name": tool_name,
            "parameters": parameters,
            "result": result
        }
    )