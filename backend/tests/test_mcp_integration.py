"""
MCP integration tests
"""
import pytest
from unittest.mock import AsyncMock, patch
from mcp.server import MCPServer

@pytest.mark.asyncio
async def test_mcp_server_execute_tool():
    """Test executing an MCP tool"""
    server = MCPServer()
    
    # Mock a tool function
    mock_tool = AsyncMock(return_value={"result": "success"})
    
    # Temporarily add the mock tool to the server's tools
    original_tools = server.tools.copy()
    server.tools = {"test_tool": mock_tool}
    
    # Execute the tool
    result = await server.execute_tool("test_tool", {"param": "value"})
    
    # Verify the tool was called with the right parameters
    mock_tool.assert_called_once_with(param="value")
    assert result["success"] is True
    assert result["result"]["result"] == "success"
    
    # Restore original tools
    server.tools = original_tools

@pytest.mark.asyncio
async def test_mcp_server_tool_not_found():
    """Test executing a non-existent tool"""
    server = MCPServer()
    
    # Execute a non-existent tool
    result = await server.execute_tool("nonexistent_tool", {})
    
    # Verify the error response
    assert result["success"] is False
    assert result["error"]["type"] == "tool_not_found"