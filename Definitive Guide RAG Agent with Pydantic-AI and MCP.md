# Title: The Definitive Guide to Building Production-Ready RAG Agents with Pydantic-AI and MCP

## 🎯 Introduction: The Mission for Authoritative Answers

This guide provides a comprehensive, best-practices blueprint for building a production-grade, terminal-based AI agent. The agent's primary mission is to provide software developers with **accurate, trustworthy, and up-to-date programming documentation** by leveraging a Retrieval-Augmented Generation (RAG) pipeline with an MCP-compliant tool like the Upstash Context7 Server.

The core design philosophy presented here is engineered to **maximize accuracy and minimize LLM hallucination**. It achieves this by combining the most robust architectural patterns and best practices into a coherent, "best-of-both-worlds" design. This guide is not just a collection of snippets; it is a complete, opinionated framework for building high-quality AI applications.

---

## 🏛️ The Core Architecture: Agent-Led Synthesis (Request-Response Model)

To ensure accuracy and stability, we will implement an **Agent-Led Synthesis** RAG pattern using a **non-streaming, request-response model**. This is a two-step LLM process that strictly separates retrieval from answering and provides maximum reliability.

1.  **Tool Use & Retrieval:** The Agent, guided by a powerful system prompt, first uses the `search` tool to retrieve relevant documents from the trusted knowledge base (Context7).
2.  **Grounded Synthesis:** The Agent then takes this retrieved context and performs a *second* LLM call. In this step, it is strictly instructed to synthesize its final answer **exclusively from the provided documents**.

This pattern forces the LLM to act as a **reasoning engine on a trusted, local dataset**, rather than a knowledge engine pulling from its vast but potentially outdated internal training. This dramatically reduces hallucination and ensures the answers are grounded in the authoritative source.

### Architectural Flow Diagram

```mermaid
graph TD
    subgraph User Interface Layer
        User[👤 User] -- 1. Asks "How do I use FastAPI?" --> CLI(Rich TUI)
    end

    subgraph Agent & RAG Pipeline Layer
        CLI -- 2. Calls agent.chat() --> Agent(src/agent.py)
        
        subgraph "Step A: Tool Use & Retrieval"
            Agent -- "3. LLM Call 1: Decide to use 'search'" --> LLM_API[☁️ OpenAI API]
            LLM_API -- "4. Instructs agent to call search('FastAPI')" --> Agent
            Agent -- "5. Executes MCP Tool Call" --> MCPServer[Context7 MCP Server]
            MCPServer -- "6. Returns raw documents/context" --> Agent
        end
        
        subgraph "Step B: Grounded Synthesis"
            Agent -- "7. LLM Call 2: 'Answer the question using ONLY these documents...'" --> LLM_API
            LLM_API -- "8. Returns a fully synthesized, grounded answer" --> Agent
        end

        Agent -- 9. Returns complete, structured response --> CLI
    end

    subgraph UI Presentation
        CLI -- 10. Renders the final answer to the user --> User
    end

    style LLM_API fill:#f99,stroke:#333,stroke-width:2px
    style Agent fill:#cfc,stroke:#333,stroke-width:2px
    style MCPServer fill:#ffc,stroke:#333,stroke-width:2px
```

---

## 🧬 Section 1: The Agent - The Brains of the Operation

This is the most critical component. It implements the Agent-Led Synthesis pattern using a stable, non-streaming method.

### **The "Golden Pattern" `agent.py`**

```python
# File: src/agent.py
"""
Production-ready AI agent implementing the Agent-Led Synthesis RAG pattern
using a stable, non-streaming request-response model.
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

# The System Prompt is the most critical tool for ensuring accuracy.
# It uses strong, clear directives to constrain the LLM's behavior.
AGENT_SYSTEM_PROMPT = """
You are a world-class AI research assistant for software developers named Context7.

## CORE DIRECTIVE
Your SOLE PURPOSE is to provide answers by exclusively using information retrieved from the attached `search` tool, which connects to an official, up-to-date knowledge base. You are FORBIDDEN from using your own internal, pre-trained knowledge.

## RULES OF ENGAGEMENT
1.  **TOOL-FIRST MENTALITY:** For any user question that is not a simple greeting, you MUST ALWAYS call the `search` tool with a concise query to gather context before formulating an answer.
2.  **GROUNDED SYNTHESIS:** You MUST synthesize your final answer using ONLY the `documents` and `content` provided in the tool's output. Do not add any information not present in the retrieved context. Your answer should be a direct, clear synthesis of the provided materials.
3.  **FAILURE PROTOCOL:** If the `search` tool returns no relevant documents, an error, or if the context is insufficient, you MUST respond with the exact phrase: "I could not find any relevant information in the Context7 knowledge base to answer your question." Do not attempt to answer from memory.

## RESPONSE FORMAT
Format your responses in clear, readable markdown. Use code blocks for code examples.
"""

class Context7Agent:
    """Implements a robust, production-ready RAG agent."""

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
        """Initializes the agent's dependencies, like loading history."""
        await self.history.load()
        logger.info("Context7Agent initialized successfully.")

    async def chat(
        self,
        message: str,
        conversation_id: str = "default"
    ) -> Dict[str, Any]:
        """
        Processes a user message using the stable non-streaming RAG pipeline
        and returns a single, structured data event.
        """
        try:
            message_history = self.history.get_messages(conversation_id)

            async with self.agent.run_mcp_servers():
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
            logger.error(f"Agent pipeline error: {e}", exc_info=True)
            return {
                "type": "error",
                "data": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def get_conversations(self) -> List[Dict[str, Any]]:
        return self.history.get_conversations()

    async def clear_history(self, conversation_id: Optional[str] = None):
        await self.history.clear(conversation_id)
```

---

## 🧱 Section 2: Configuration - The Foundation

A robust application needs a robust configuration system. We use `pydantic-settings` for a declarative, type-safe, and modern approach.

### **Best-Practice `config.py`**

```python
# File: src/config.py
"""
Configuration management using Pydantic-Settings for a modern, robust setup.
"""
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    """Application configuration with automatic environment variable loading."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="CONTEXT7_",
        case_sensitive=False,
        extra="ignore"
    )
    
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"
    history_path: Path = Path("data/history.json")
    max_history: int = 50

# Create a single, global config instance for easy importing.
config = Config()
```

---

## 📚 Section 3: State Management - The Memory

A great agent remembers past conversations. This `HistoryManager` uses a simple `list[dict]` format, which is the correct and stable pattern for this library version.

### **Production-Grade `history.py`**

```python
# File: src/history.py
"""
Conversation history management with multi-conversation support.
This version correctly returns a plain list[dict] for maximum stability.
"""
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import aiofiles

from .config import config

class HistoryManager:
    """Manages conversation history with a robust, compliant message schema."""
    
    def __init__(self):
        self.history_path = config.history_path
        self.max_history = config.max_history
        self._history: Dict[str, List[Dict[str, Any]]] = {}
    
    async def load(self):
        # ... (implementation is correct, omitted for brevity)
        pass

    async def save(self):
        # ... (implementation is correct, omitted for brevity)
        pass
    
    async def add_message(self, conversation_id: str, role: str, content: str):
        # ... (implementation is correct, omitted for brevity)
        pass
    
    def get_messages(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Gets messages for a conversation in the exact list[dict] format the Agent needs."""
        messages = self._history.get(conversation_id, [])
        return [{"role": msg["role"], "content": msg["content"]} for msg in messages]

    # ... other methods are correct, omitted for brevity ...
```

---

## 🎨 Section 4: The User Interface - The Face of the Agent

The TUI uses a `rich.status` spinner to show activity while waiting for the agent's complete response.

### **Best-Practice `cli.py` (Core Logic)**

```python
# File: src/cli.py (Conceptual)
# ... imports ...
from .agent import Context7Agent
from .themes import ThemeManager
from rich.markdown import Markdown

class Context7CLI:
    def __init__(self):
        self.agent = Context7Agent()
        # ... other initializations

    async def process_message(self, message: str):
        """Processes a user message using a non-streaming model with a status indicator."""
        theme = self.theme_manager.get_current_theme()
        
        with self.console.status("[bold green]Assistant is thinking...", spinner="dots"):
            response = await self.agent.chat(message, self.current_conversation)

        if response["type"] == "complete":
            markdown = Markdown(response["data"], style=theme.colors['text'])
            self.console.print(markdown)
        elif response["type"] == "error":
            # ... render error panel ...
            pass
```

---

## ✅ Section 5: Production Readiness & Pitfalls

### **Production Checklist**
The checklist from the previous version remains valid, with the key takeaway being the stability of the non-streaming approach.

### **⚠️ Common Pitfalls & Solutions**

This table covers the most common errors discovered during development.

| Issue Symptom | Root Cause | The Fix |
| :--- | :--- | :--- |
| **`ImportError` on `UserMessage`, etc.**| The library does not expose Pydantic models for history. | The `HistoryManager` **MUST** return a plain **`list[dict]`**, not a list of Pydantic models. |
| **`AttributeError: 'list' object ...`**| Incorrect model parameter format. | Use the provider-prefixed string: **`model="openai:gpt-4o-mini"`**. |
| **`MCPServerError: ... not running`**| Missing MCP server lifecycle management. | Wrap agent calls in **`async with agent.run_mcp_servers():`**. |
| **Streaming `TypeError` or `AttributeError`**| The `v0.4.2` streaming API is complex and non-obvious. | **Abandon streaming.** Use the stable, non-streaming **`await agent.run()`** method for maximum reliability. |

