"""
Tool call logging
"""
from typing import Dict, Any
from ..utils.logging import log_tool_call

def log_mcp_tool_call(tool_name: str, user_id: str, parameters: Dict[str, Any], result: Dict[str, Any]):
    """
    Log an MCP tool call with structured data
    """
    log_tool_call(tool_name, user_id, parameters, result)