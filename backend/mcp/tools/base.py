"""
Base tool class for MCP tools
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseTool(ABC):
    """
    Abstract base class for all MCP tools
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the tool"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """A description of what the tool does"""
        pass
    
    @property
    @abstractmethod
    def parameters(self) -> Dict[str, Any]:
        """JSON schema for the tool's parameters"""
        pass
    
    @abstractmethod
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool with the given parameters
        """
        pass