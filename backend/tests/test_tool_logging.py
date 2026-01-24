"""
Tool logging tests
"""
import pytest
from unittest.mock import patch
from app.utils.tool_logger import log_mcp_tool_call

def test_tool_call_logging():
    """Test that tool calls are logged correctly"""
    with patch('app.utils.tool_logger.log_tool_call') as mock_log:
        tool_name = "test_tool"
        user_id = "test_user"
        parameters = {"param1": "value1"}
        result = {"success": True, "data": "result"}
        
        log_mcp_tool_call(tool_name, user_id, parameters, result)
        
        # Verify the logging function was called with correct parameters
        mock_log.assert_called_once_with(tool_name, user_id, parameters, result)