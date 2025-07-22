# File: src/agent.py
"""
Production-ready AI agent implementing the Agent-Led Synthesis RAG pattern.
This version uses a robust, non-streaming request-response model for stability.
*** FINAL CORRECTED VERSION ***
"""
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio

from .config import config
from .history import HistoryManager

logger = logging.getLogger(__name__)

AGENT_SYSTEM_PROMPT = """
You are a world-class AI research assistant for software developers named Context7.

## CORE DIRECTIVE
Your SOLE PURPOSE is to provide answers by exclusively using information retrieved from the attached `search` tool, which connects to an official, up-to-date knowledge base. You are FORBIDDEN from using your own internal, pre-trained knowledge, as it is considered unreliable for this task.

## RULES OF ENGAGEMENT
1.  **TOOL-FIRST MENTALITY:** For any user question that is not a simple greeting, you MUST ALWAYS call the `search` tool with a concise query to gather context before formulating an answer.
2.  **GROUNDED SYNTHESIS:** You MUST synthesize your final answer using ONLY the `documents` and `content` provided in the tool's output. Do not add any information not present in the retrieved context. Your answer should be a direct, clear synthesis of the provided materials.
3.  **FAILURE PROTOCOL:** If the `search` tool returns no relevant documents, an error, or if the context is insufficient, you MUST respond with the exact phrase: "I could not find any relevant information in the Context7 knowledge base to answer your question." Do not attempt to answer from memory.

## RESPONSE FORMAT
Format your responses in clear, readable markdown. Use code blocks for code examples.
"""

class Context7Agent:
    """Implements a robust, production-ready RAG agent using Agent-Led Synthesis."""
    
    def __init__(self):
        """Initializes the agent using the Golden Pattern for Pydantic-AI v0.4.2."""
        self.mcp_server = MCPServerStdio(
            command="npx",
            args=["-y", "@upstash/context7-mcp@latest"]
        )

        self.agent = Agent(
            model=f"openai:{config.openai_model}",
            mcp_servers=[self.mcp_server],
            system_prompt=AGENT_SYSTEM_PROMPT
        )
        
        self.history = HistoryManager()
    
    async def initialize(self):
        """Initializes the agent's dependencies, such as loading history."""
        await self.history.load()
        logger.info("Context7Agent initialized successfully.")
    
    async def chat(
        self, 
        message: str, 
        conversation_id: str = "default"
    ) -> Dict[str, Any]:
        """
        Processes a user message using a non-streaming request-response pattern.
        Returns a single dictionary with the complete response.
        """
        try:
            message_history = self.history.get_messages(conversation_id)
            
            async with self.agent.run_mcp_servers():
                # Use the simple, reliable `run` method.
                result = await self.agent.run(message, message_history=message_history)
                full_response = str(result.data)

            await self.history.add_message(conversation_id, "user", message)
            await self.history.add_message(conversation_id, "assistant", full_response)
            
            return {
                "type": "complete",
                "data": full_response,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Agent RAG pipeline error: {e}", exc_info=True)
            return {
                "type": "error",
                "data": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_conversations(self) -> List[Dict[str, Any]]:
        """Gets metadata for all conversations, for use in the UI."""
        return self.history.get_conversations()
    
    async def clear_history(self, conversation_id: Optional[str] = None):
        """Clears history for a specific conversation or all conversations."""
        await self.history.clear(conversation_id)
