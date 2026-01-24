"""
MCP utilities
"""
from typing import Dict, Any
from ..app.utils.logging import log_tool_call

def format_tool_response(success: bool, result: Any = None, error: str = None) -> Dict[str, Any]:
    """
    Format a standard tool response
    """
    response = {"success": success}

    if success:
        response["result"] = result
    else:
        response["error"] = error

    return response

def log_tool_execution(tool_name: str, user_id: str, parameters: Dict[str, Any], result: Dict[str, Any]):
    """
    Log the execution of an MCP tool
    """
    log_tool_call(tool_name, user_id, parameters, result)