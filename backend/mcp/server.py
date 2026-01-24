"""
MCP (Model Context Protocol) Server Implementation
This server handles the execution of MCP tools for the AI agent.
"""
import asyncio
from typing import Dict, Any
from .tools.registry import get_registered_tools

class MCPServer:
    def __init__(self):
        self.tools = get_registered_tools()
    
    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an MCP tool with the given parameters
        """
        if tool_name not in self.tools:
            return {
                "success": False,
                "error": {
                    "type": "tool_not_found",
                    "message": f"Tool '{tool_name}' not found"
                }
            }
        
        try:
            tool_func = self.tools[tool_name]
            result = await tool_func(**parameters) if asyncio.iscoroutinefunction(tool_func) else tool_func(**parameters)
            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": {
                    "type": "tool_execution_error",
                    "message": str(e)
                }
            }

# Global MCP server instance
mcp_server = MCPServer()

def get_mcp_server():
    """Get the global MCP server instance"""
    return mcp_server