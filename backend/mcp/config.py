"""
MCP server configuration
"""
from ..config import OPENAI_API_KEY, GEMINI_API_KEY

# API Keys
MCP_OPENAI_API_KEY = OPENAI_API_KEY
MCP_GEMINI_API_KEY = GEMINI_API_KEY

# Server configuration
MCP_SERVER_HOST = "localhost"
MCP_SERVER_PORT = 8001

# Tool execution configuration
MCP_TOOL_TIMEOUT = 30  # seconds
MCP_MAX_CONCURRENT_TOOLS = 10