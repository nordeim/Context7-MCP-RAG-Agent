You are the absolute best AI coding assistant in the world because you are capable of producing insanely good and mind-blowing UI designs, codes and architectures consistently. You are a deep-thinking coding expert recognized for and exemplary work in modern UI design and production quality code generation. You will use an extremely long chain of thoughts to deeply consider the problem and deliberate with yourself via systematic reasoning processes to help come to a correct or most optimal solution before answering. You will carefully explore various options before choosing the best option for producing your final answer. You will thoroughly explore various implementation options before choosing the most optimal option or approach to implement a given request. To produce error-free results or code output, you will come up with a detailed execution plan based on your chosen best option or most optimal solution, then cautiously execute according to the plan to complete your given task. You will double-check and validate any code changes before implementing. You excel in deep thinking and will use a long chain of thoughts to systematically and thoroughly explore various options and approaches to providing an answer or solution, evaluate and validate all possible options, before choosing the best option or approach to give the most optimal solution or answer. You are known to be meticulous and accurate in handling given tasks, and will always aim to be thorough in your investigation and thought processes, to always carefully evaluate and validate your proposed solution or answer so as to provide the most precise and accurate answer and correct solution. When implementing a design, include as many relevant features and interactions as possible. Create a fully-featured implementation that goes beyond the basics, to re-imagine a design that has a *Wow*, *awesome*, and *unbelievably* effects. You will enclose your thoughts and internal monologue inside <think> </think> tags, and then provide your final solution or answer to the given query or question.

Create an awesomely cool and user-friendly AI agent built with Pydantic AI, deeply integrated with the Context7 MCP (Model Context Protocol) server. This agent transforms terminal interactions into an immersive, conversational experience, allowing users to chat naturally about subjects while the AI intelligently searches for and presents relevant documents via MCP. The re-imagined design features a dynamic Terminal User Interface (TUI) with stunning themes, smooth animations, live result streaming, and interactive elements like hotkeys and inline previews. Powered by OpenAI for chat and intent detection, and Node.js for the MCP server, this agent excels in contextual document discovery, analysis, and management. Whether you're exploring "quantum computing" or bookmarking findings, it feels like chatting with a futuristic librarian! Be sure to use the specific syntax for connecting MCP servers to Pydantic AI agents.

## Features

- **Stunning Visual Interface**: 4 beautiful themes (Cyberpunk, Ocean, Forest, Sunset) with gradients, glowing text, smooth animations (e.g., typing effects, particle loaders), rich layouts (panels, tables), and theme-specific ASCII art welcome screens.
- **Powerful Search Capabilities**: AI-powered, real-time document discovery via Context7 MCP, with fuzzy matching, advanced filters (file type, date range, size, tags), and search analytics.
- **Document Management**: Smart syntax-highlighted previews, bookmarks, search history, session management, and AI-recommended similar documents.
- **Context7 Integration**: Full MCP server support for contextual searches (based on meaning, not just keywords), document analysis, auto-indexing, and quantum-mode enhancements.
- **Conversational TUI**: Unified chat interface with intent detection – discuss a subject, and the agent automatically searches MCP, streams results live, and offers interactions (e.g., /preview 1).
- **Additional Perks**: Hotkeys for commands (/theme, /bookmark, /analytics), error alerts, session auto-save/load, and performance optimizations with async operations.

## Features to Implement

  - Conversational chat with OpenAI integration (e.g., natural language responses).
  - Intent detection for subject-based searches (e.g., "Tell me about AI ethics" triggers MCP query).
  - Real-time MCP searches with live streaming results and fuzzy matching.
  - Dynamic TUI layout (split-screen: header, chat, results, footer) using Rich.
  - Theme switching with animations and ASCII art.
  - Animations (typing simulation, particle loaders) for fluid UX.
  - Document previews (syntax-highlighted), bookmarks, and similar recommendations.
  - JSON-based persistence for conversations, searches, bookmarks, and sessions.
  - Hotkeys (/help, /exit, /analytics, etc.) within the chat.
  - Error handling with styled alerts and retries for MCP connections.

### Stunning Visual Interface
- **4 Beautiful Themes**: Cyberpunk, Ocean, Forest, and Sunset
- **Smooth Animations**: Fluid transitions and loading effects
- **Rich Terminal UI**: Gradients, glowing text, and modern layouts
- **ASCII Art**: Theme-specific welcome screens

### Powerful Search Capabilities
- **AI-Powered Search**: Intelligent document discovery with Context7
- **Real-time Results**: Live search with instant feedback
- **Advanced Filters**: File type, date range, size, and tags
- **Fuzzy Matching**: Find documents even with typos
- **Search Analytics**: Track and analyze your search patterns

### Document Management
- **Smart Previews**: Syntax-highlighted document previews
- **Bookmarks**: Save and organize important documents
- **Search History**: Access and replay previous searches
- **Session Management**: Save and restore your work sessions
- **Similar Documents**: AI-powered document recommendations

### Context7 Integration
- **MCP Server**: Deep integration with Context7 Model Context Protocol
- **Document Analysis**: AI-powered content understanding
- **Contextual Search**: Find documents based on meaning, not just keywords
- **Auto-indexing**: Automatic document discovery and indexing

## 🚀 Installation

### Prerequisites
- Python 3.11 or higher
- Node.js and npm (for Context7 MCP server)
- OpenAI API key or compatible endpoint

# Project Structure
First, let's create the project structure:

context7-agent/
├── src/
│   ├── __init__.py
│   ├── agent.py
│   ├── cli.py
│   ├── config.py
│   ├── history.py
│   ├── themes.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_agent.py
│   └── test_history.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── pyproject.toml


The JSON config (that you'll need to adjust for Pydantic AI) for the Context7 MCP looks like:

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

# Pydantic-AI & MCP Server Troubleshooting Guide

Quick reference for resolving common Pydantic-AI integration issues based on real-world debugging experience.

## 🔍 Error Pattern Quick Reference

### Initialization Errors

| Error Message | Cause | Solution |
|---------------|--------|----------|
| `TypeError: OpenAIModel.__init__() got unexpected keyword argument 'model'` | API signature changed - model parameter moved | Use `model_name` parameter in `OpenAIModel` constructor |
| `TypeError: OpenAIProvider.__init__() got unexpected keyword argument 'client'` | Provider doesn't accept pre-initialized client | Pass `api_key` and `base_url` directly |
| `TypeError: OpenAIProvider.__init__() got unexpected keyword argument 'model'` | Model parameter belongs to Agent, not Provider | Remove model from Provider, use in Agent |
| `TypeError: MCPServerStdio.__init__() missing 1 required positional argument: 'args'` | Missing argument unpacking | Use `**config_dict` to unpack configuration |
| `UserError: Unknown keyword arguments: 'provider', 'llm_model'` | Agent constructor signature changed | Use `model` parameter instead of `llm_model` |

### Import/Module Errors

| Error Message | Cause | Solution |
|---------------|--------|----------|
| `ModuleNotFoundError: No module named 'pydantic_ai.llm'` | Package reorganization | Import from `pydantic_ai.models.openai` |
| `ImportError: cannot import name 'OpenAI'` | Class renamed | Use `OpenAIModel` instead of `OpenAI` |

### MCP Server Lifecycle Errors

| Error Message | Cause | Solution |
|---------------|--------|----------|
| `AttributeError: 'MCPServerStdio' object has no attribute 'start'` | Manual lifecycle deprecated | Use async context manager: `async with agent.run_mcp_servers()` |
| `AttributeError: 'MCPServerStdio' object has no attribute 'terminate'` | Manual cleanup deprecated | Let Agent manage lifecycle via context manager |

### Message Formatting Errors

| Error Message | Cause | Solution |
|---------------|--------|----------|
| `ValidationError: Missing 'kind' discriminator` | Incorrect message structure | Use Pydantic model objects, not dicts |
| `ValidationError: Missing 'parts' field` | Message format too simplistic | Use proper `UserPromptPart`, `SystemPromptPart` objects |
| `ValidationError: Missing 'part_kind' discriminator` | Nested structure missing | Use library's internal message classes |
| `AssertionError: Expected code to be unreachable` | Manual dict creation incorrect | Use official Pydantic model objects |

### Async Runtime Errors

| Error Message | Cause | Solution |
|---------------|--------|----------|
| `TimeoutError` + `GeneratorExit` + `RuntimeError` | Async backend conflict | Unify on `anyio` (not `asyncio`) |
| `TypeError: anyio.to_thread.run_sync() got unexpected keyword argument 'console'` | Wrong async API usage | Use lambda wrapper: `lambda: func(arg, kwarg=value)` |
| `TypeError: PromptBase.ask() takes from 1 to 2 positional arguments but 3 were given` | Incorrect threading call | Use keyword arguments properly in thread wrapper |

## 🛠️ Defensive Initialization Pattern

```python
# Safe initialization pattern based on debugging experience
import openai
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio

class SafeAgent:
    def __init__(self, api_key: str, model_name: str = "gpt-4o-mini", base_url: str = None):
        # 1. Provider for sync operations
        self.provider = OpenAIProvider(
            api_key=api_key,
            base_url=base_url or "https://api.openai.com/v1"
        )
        
        # 2. Dedicated async client for async operations
        self.async_client = openai.AsyncOpenAI(
            api_key=api_key,
            base_url=base_url or "https://api.openai.com/v1"
        )
        
        # 3. Model for pydantic-ai integration
        self.llm = OpenAIModel(
            model_name=model_name,
            provider=self.provider
        )
        
        # 4. Agent with MCP servers
        self.agent = Agent(
            model=self.llm,
            mcp_servers=[MCPServerStdio(**mcp_config)]
        )
```

## 📊 Version Compatibility Matrix

| Pydantic-AI Version | OpenAI Model Class | Provider Pattern | Recommended Approach |
|---------------------|--------------------|------------------|---------------------|
| 0.4.x and earlier | `OpenAI` | Direct client | Legacy - avoid |
| 0.5.x+ | `OpenAIModel` | With `OpenAIProvider` | Use current pattern |
| 0.6.x+ (future) | Check source code | Check source code | Always verify |

## 🔄 Async Runtime Best Practices

### 1. Unify Async Backend
```python
# ❌ Don't mix async backends
import asyncio
# ... later use anyio.to_thread.run_sync()

# ✅ Use anyio consistently
import anyio
# ... use anyio.to_thread.run_sync()
# ... use anyio.run() as entry point
```

### 2. Context Manager Pattern
```python
# ✅ Proper MCP server lifecycle
async def run(self):
    async with self.agent.run_mcp_servers():
        await self.main_loop()

# Entry point
if __name__ == "__main__":
    anyio.run(MyApp().run)
```

### 3. Threading Safe Calls
```python
# ✅ Safe blocking calls in async context
user_input = await anyio.to_thread.run_sync(
    lambda: Prompt.ask("[bold]You[/bold]", console=console)
)
```

## 🎯 Message Formatting Checklist

When sending messages to Pydantic-AI:

- [ ] **Don't use raw dictionaries** - Use Pydantic model objects
- [ ] **Use proper message types**:
  - `UserPromptPart` for user messages
  - `SystemPromptPart` for system messages
  - `TextPart` for text content
- [ ] **Avoid manual schema construction** - Let the library handle validation
- [ ] **Test with simple messages first** - Verify basic functionality

## 🔧 Quick Debug Commands

```bash
# Check installed versions
pip show pydantic-ai openai anyio

# Verify class signatures
python -c "from pydantic_ai.models.openai import OpenAIModel; help(OpenAIModel.__init__)"

# Test MCP server connection
python -c "from pydantic_ai.mcp import MCPServerStdio; print('MCP server import OK')"

# Check async backend compatibility
python -c "import anyio; print('anyio version:', anyio.__version__)"
```

## 🚨 Emergency Bypass Strategy

When Pydantic-AI abstractions fail:

1. **Identify the stable layer** - Usually the underlying OpenAI client
2. **Bypass problematic methods** - Use direct client calls
3. **Maintain MCP integration** - Keep using Agent for server lifecycle
4. **Document the workaround** - Note why bypass was necessary

```python
# Emergency bypass example
async def generate_response_bypass(self, messages):
    # When agent.run() fails, use direct OpenAI client
    response = await self.async_client.chat.completions.create(
        model=self.model_name,
        messages=messages
    )
    return response.choices[0].message.content
```

## 📋 Pre-flight Checklist

Before running Pydantic-AI applications:

- [ ] Verify all imports work without errors
- [ ] Check constructor signatures match current API
- [ ] Ensure async backend consistency (anyio)
- [ ] Test MCP server lifecycle with context manager
- [ ] Validate message formatting with simple test
- [ ] Confirm environment variables are set
- [ ] Test file I/O error handling (history.json)

## 🔍 Common Log Patterns

Watch for these patterns in logs:

- `"TypeError: ... got unexpected keyword argument"` → API drift
- `"ValidationError: Missing 'kind' discriminator"` → Message format issue
- `"AttributeError: ... has no attribute 'start'"` → MCP lifecycle change
- `"TimeoutError"` + `"GeneratorExit"` → Async backend conflict
- `"AssertionError: Expected code to be unreachable"` → Abstraction misuse

## 📚 Reference Commands

```bash
# Get current API signatures
python -c "
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.mcp import MCPServerStdio
print('Agent:', Agent.__init__.__annotations__)
print('OpenAIModel:', OpenAIModel.__init__.__annotations__)
print('OpenAIProvider:', OpenAIProvider.__init__.__annotations__)
"
```

Remember: When in doubt, check the source code. The installed library is the ultimate source of truth.






#######################################################################################################
### Context7 MCP Integration

```python
class Context7MCPIntegration:
    """
    Handles integration with Context7 Model Context Protocol server.
    
    Implements:
    - Connection management
    - Protocol handling
    - Request/response processing
    - Error recovery
    """
    
    def __init__(self):
        self.connection_pool = MCPConnectionPool()
        self.protocol_handler = MCPProtocolHandler()
        self.request_queue = asyncio.Queue()
        self.response_handlers = {}
    
    async def connect(self):
        """Establish connection to Context7 MCP server."""
        # Start MCP server process
        self.process = await asyncio.create_subprocess_exec(
            "npx",
            "-y",
            "@upstash/context7-mcp@latest",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Initialize protocol
        await self.protocol_handler.initialize(
            self.process.stdin,
            self.process.stdout
        )
        
        # Start message processing
        asyncio.create_task(self._process_messages())
    
    async def search(
        self,
        query: str,
        options: SearchOptions
    ) -> List[Document]:
        """Perform search through MCP."""
        # Create request
        request = MCPRequest(
            id=str(uuid.uuid4()),
            method="search",
            params={
                "query": query,
                "filters": options.filters,
                "limit": options.limit,
                "quantum_mode": options.quantum_enabled
            }
        )
        
        # Send request
        response = await self._send_request(request)
        
        # Process response
        documents = []
        for doc_data in response.result.get("documents", []):
            documents.append(Document(
                id=doc_data["id"],
                title=doc_data["title"],
                content=doc_data["content"],
                metadata=doc_data.get("metadata", {}),
                neural_properties=self._extract_neural_properties(doc_data)
            ))
        
        return documents
    
    def _extract_neural_properties(
        self,
        doc_data: Dict
    ) -> NeuralProperties:
        """Extract neural properties from document data."""
        return NeuralProperties(
            embedding=doc_data.get("embedding", []),
            semantic_density=doc_data.get("semantic_density", 0.5),
            information_entropy=doc_data.get("entropy", 0.5),
            neural_activation=doc_data.get("activation", 0.0)
        )
```

