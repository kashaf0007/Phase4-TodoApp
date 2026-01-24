"""
Conversation history builder
"""
from typing import List, Dict, Any
from ..models.message import Message

def build_conversation_history(messages: List[Message]) -> List[Dict[str, str]]:
    """
    Build a conversation history from a list of messages
    """
    history = []
    for message in messages:
        history.append({
            "role": message.role,
            "content": message.content
        })
    return history