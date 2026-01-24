"""
Agent orchestration service
"""
from typing import Dict, Any, List
from ...mcp.server import get_mcp_server
from ..utils.logging import log_tool_call
from ..schemas.chat import ToolCallLog

class AgentService:
    def __init__(self):
        self.mcp_server = get_mcp_server()

    async def process_message_with_agent(self, user_id: str, message: str, conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Process a user message with the AI agent and execute MCP tools as needed
        """
        # In a real implementation, this would call the OpenAI Agents SDK
        # For now, we'll simulate the agent behavior
        
        # This is a simplified simulation of what the agent would do
        # In reality, the agent would analyze the message and decide which tools to call
        tool_calls = []
        response = ""
        
        # Simple intent detection for demo purposes (in real implementation, this would be handled by the AI agent)
        if "add" in message.lower() and "task" in message.lower():
            # Simulate calling add_task tool
            title = message.replace("add", "").replace("task", "").strip()
            if not title:
                title = "Untitled task"
            
            tool_params = {
                "user_id": user_id,
                "title": title,
                "description": f"Task created from message: {message}"
            }
            
            # Execute the tool
            tool_result = await self.mcp_server.execute_tool("add_task", tool_params)
            
            # Log the tool call
            tool_call_log = ToolCallLog(
                tool_name="add_task",
                parameters=tool_params,
                result=tool_result
            )
            tool_calls.append(tool_call_log)
            
            if tool_result["success"]:
                response = f"I've added the task '{title}' to your list."
            else:
                response = f"Sorry, I couldn't add the task: {tool_result.get('error', {}).get('message', 'Unknown error')}"
        
        elif "list" in message.lower() and "task" in message.lower():
            # Simulate calling list_tasks tool
            tool_params = {
                "user_id": user_id
            }
            
            # Execute the tool
            tool_result = await self.mcp_server.execute_tool("list_tasks", tool_params)
            
            # Log the tool call
            tool_call_log = ToolCallLog(
                tool_name="list_tasks",
                parameters=tool_params,
                result=tool_result
            )
            tool_calls.append(tool_call_log)
            
            if tool_result["success"]:
                tasks = tool_result["result"]["tasks"]
                if tasks:
                    task_list = "\n".join([f"- {task['title']}" for task in tasks])
                    response = f"Here are your tasks:\n{task_list}"
                else:
                    response = "You don't have any tasks."
            else:
                response = f"Sorry, I couldn't retrieve your tasks: {tool_result.get('error', {}).get('message', 'Unknown error')}"
        
        else:
            # Default response for unrecognized intents
            response = f"I received your message: '{message}'. I can help you manage tasks using commands like 'add task' or 'list tasks'."
        
        return {
            "response": response,
            "tool_calls": tool_calls
        }