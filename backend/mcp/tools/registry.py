"""
Tool registration utilities for MCP
"""
from typing import Dict, Callable, Any
import asyncio

# Dictionary to hold registered tools
_registered_tools: Dict[str, Callable[..., Any]] = {}

def register_tool(name: str):
    """
    Decorator to register an MCP tool
    """
    def decorator(func):
        _registered_tools[name] = func
        return func
    return decorator

def get_registered_tools() -> Dict[str, Callable[..., Any]]:
    """
    Get all registered tools
    """
    return _registered_tools

def get_tool(name: str) -> Callable[..., Any]:
    """
    Get a specific registered tool by name
    """
    if name not in _registered_tools:
        raise ValueError(f"Tool '{name}' is not registered")
    return _registered_tools[name]

# Import all tools to ensure they are registered
def register_all_tools():
    """
    Import and register all tools
    """
    try:
        from . import add_task, list_tasks, complete_task, delete_task, update_task
    except ImportError as e:
        print(f"Error importing tools: {e}")