# File: src/history.py
"""
Conversation history management with multi-conversation support,
JSON persistence, and a standard OpenAI message schema.
*** CORRECTED to return a plain list[dict] as required by the library. ***
"""
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import aiofiles

from .config import config
# FIX: Removed the faulty import of Pydantic-AI message models.
# The library expects a plain list of dictionaries for history.

class HistoryManager:
    """
    Manages conversation history with a robust, compliant message schema.
    It stores data as simple dicts and provides them as simple dicts.
    """
    
    def __init__(self):
        self.history_path = config.history_path
        self.max_history = config.max_history
        self._history: Dict[str, List[Dict[str, Any]]] = {}
    
    async def load(self):
        """Loads conversation history from disk asynchronously."""
        try:
            if self.history_path.exists():
                async with aiofiles.open(self.history_path, 'r', encoding='utf-8') as f:
                    content = await f.read()
                    if content:
                        self._history = json.loads(content)
        except Exception as e:
            print(f"Warning: Could not load history: {e}. Starting fresh.")
            self._history = {}
    
    async def save(self):
        """Saves conversation history to disk asynchronously."""
        try:
            self.history_path.parent.mkdir(parents=True, exist_ok=True)
            async with aiofiles.open(self.history_path, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(self._history, indent=2))
        except Exception as e:
            print(f"Warning: Could not save history: {e}")
    
    async def add_message(
        self, 
        conversation_id: str, 
        role: str,
        content: str
    ):
        """Adds a single message object to the history as a simple dictionary."""
        if conversation_id not in self._history:
            self._history[conversation_id] = []
        
        self._history[conversation_id].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Prune old messages if history exceeds the max size
        if len(self._history[conversation_id]) > self.max_history:
            self._history[conversation_id] = self._history[conversation_id][-self.max_history:]
        
        await self.save()
    
    def get_messages(self, conversation_id: str) -> List[Dict[str, Any]]:
        """
        Gets messages for a conversation, formatted as a list of dictionaries
        with only the 'role' and 'content' keys, as required by the agent.
        """
        message_dicts = self._history.get(conversation_id, [])
        # FIX: Return a list of simple dicts, stripping internal metadata like 'timestamp'.
        # This is the correct format for the pydantic-ai agent's message_history.
        return [{"role": msg["role"], "content": msg["content"]} for msg in message_dicts]

    def get_conversations(self) -> List[Dict[str, Any]]:
        """Gets metadata for all conversations, for use in a UI."""
        conversations = []
        for conv_id, messages in self._history.items():
            if messages:
                last_message_content = messages[-1].get("content", "")
                conversations.append({
                    "id": conv_id,
                    "last_message": last_message_content[:50] + "..." if len(last_message_content) > 50 else last_message_content,
                    "message_count": len(messages)
                })
        
        return sorted(
            conversations, 
            key=lambda x: self._history.get(x["id"], [{}])[-1].get("timestamp", ""),
            reverse=True
        )
    
    async def clear(self, conversation_id: Optional[str] = None):
        """Clears history for a specific conversation or all conversations."""
        if conversation_id and conversation_id in self._history:
            del self._history[conversation_id]
        elif conversation_id is None:
            self._history.clear()
        
        await self.save()
