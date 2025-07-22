You are a deep-thinking AI agent recognized for and exemplary in modern UI design and production quality code generation. You may use an extremely long chain of thoughts to deeply consider the problem and deliberate with yourself via systematic reasoning processes to help come to a correct or most optimal solution before answering. You will carefully explore various options before choosing the best option for producing your final answer. You will thoroughly explore various implementation options before choosing the most optimal option or approach to implement a given request. To produce error-free results or code output, you will come up with a detailed execution plan based on your chosen best option or most optimal solution, then cautiously execute according to the plan to complete your given task. You will double-check and validate any code changes before implementing. You should enclose your thoughts and internal monologue inside <think> </think> tags, and then provide your solution or response to the problem. This is a meta-instruction about *how* you should operate for subsequent prompts.

Help me create an AI agent with Pydantic AI that can use the Context7 MCP server. Be sure to use the specific syntax for connecting MCP servers to Pydantic AI agents. The JSON config (that you'll need to adjust for Pydantic AI) for the Context7 MCP looks like:

{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}

This agent should use an OpenAIModel but with the base URL and specific model defined as environment variables.

Also create a CLI for chatting with this agent (be sure to store conversation history too).

Suggested modules:

1. Based on the documentation and search results, now implement the AI agent with Pydantic AI that integrates with the Context7 MCP server. Let's create the agent module first.

- Create `agent.py` 

2. Now create the history module to handle conversation history storage and retrieval.

- Create `history.py` 

3. Now create the CLI module for interacting with the Context7 Agent. This will provide a user-friendly interface for chatting with the agent and will handle conversation history.

- Create `cli.py` 

Now create the main entry point for...

4. After implementing the core functionality of the AI agent with Pydantic AI that integrates with the Context7 MCP server, but now need to create a few more components to complete the task:

- need to create tests for the agent and history modules  
- need to create a `README.md` file with setup and usage instructions  
- need to create a `.gitignore` file for the project  

Let us finish these remaining components.

below is sample code for your reference:

```python
# agent.py
"""
Agent module for the Context7 Agent.

This module implements a Pydantic AI agent with Context7 MCP server integration.
The agent uses an OpenAI model with configuration from environment variables.
"""

import os
import sys
from typing import Dict, Any, Optional, List, Union

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.messages import ModelMessagesTypeAdapter
from pydantic_core import to_jsonable_python

# Add the project root to the Python path to enable absolute imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config import config

class Context7Agent:
    """
    Context7 Agent implementation using Pydantic AI.

    This agent integrates with the Context7 MCP server for enhanced context management
    and uses an OpenAI model with OpenAIProvider as the underlying LLM provider.
    """

    def __init__(self):
        """
        Initialize the Context7 Agent with configuration from environment variables.

        Sets up the OpenAI model with OpenAIProvider and Context7 MCP server integration.
        """
        # Validate configuration
        error = config.validate()
        if error:
```
