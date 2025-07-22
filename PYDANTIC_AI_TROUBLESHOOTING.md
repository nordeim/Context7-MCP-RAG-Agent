# The Definitive Pydantic-AI & MCP Production Guide
> **Field-Tested Recipes for Building Robust, Modern AI Agents**

This guide is the distilled wisdom from real-world debugging of `pydantic-ai`. It presents the gold standard patterns for creating a production-ready AI agent that uses MCP for tool-calling. Follow these recipes to build stable, maintainable, and powerful applications.

---

## 0. The Five Golden Rules (Memorize These)

1.  **Trust the Source, Not Just Docs:** API signatures in the installed library (`__init__`) are the ultimate truth. Use them to resolve `TypeError`.
2.  **Pin Your Dependencies:** Prevent surprise API changes from breaking your app. Use version ranges like `"pydantic-ai>=0.5,<1.0"`.
3.  **Unify on `anyio`:** `pydantic-ai` uses `anyio`. Your application **must** also use `anyio` for its main event loop to prevent `TimeoutError` and state corruption. Never mix it with `asyncio`.
4.  **Let the Library Do the Work:** Stop manually building complex message dictionaries. The modern `agent.run()` accepts simple `[{"role": ..., "content": ...}]` dictionaries.
5.  **Handle `KeyboardInterrupt`:** A professional CLI application must exit gracefully on Ctrl-C. Always wrap your main loop in a `try/except KeyboardInterrupt`.

---

## 1. Quick-Fix Matrix: Common Errors & Solutions

| Symptom | Root Cause | The One-Line Fix |
| :--- | :--- | :--- |
| `ImportError: cannot import name 'UserPrompt'` | Class renamed/obsoleted in v0.5+ | **Don't import it.** Use `[{"role": "user", ...}]` dicts. |
| `AssertionError: Expected code to be unreachable` | Manually creating invalid message schemas | **Stop hand-crafting message dicts.** Pass simple dicts to `agent.run()`. |
| `TypeError: 'async for' requires __aiter__` | Misusing the v0.5+ streaming API | **Use `await agent.run(...)`**; it returns the full result directly. |
| `TimeoutError` + `GeneratorExit` + `RuntimeError` | Mixed async backends (`asyncio` vs `anyio`) | Replace `asyncio.run(main)` with **`anyio.run(main)`**. |
| `KeyboardInterrupt` ugly traceback | No graceful shutdown logic | Wrap the main `while True:` loop in a **`try/except KeyboardInterrupt`** block. |

---

## 2. The Gold Standard: The "Unified Agent" Skeleton

This is the recommended, simplified, and robust pattern. The agent has **one** primary entry point (`agent.run()`) for all interactions, and the library handles the routing between chat and tool-calling.

```python
# src/agent.py
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

class UnifiedAgent:
    """
    Implements the modern "Unified Abstraction" pattern.
    All interactions are channeled through the single agent.run() method.
    """
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        # 1. The Provider handles connection details.
        self.provider = OpenAIProvider(api_key=api_key)

        # 2. The Model wraps the provider and model name for the agent.
        self.llm = OpenAIModel(model_name=model, provider=self.provider)

        # 3. The Agent is the primary interface, configured with the model and MCP servers.
        self.agent = Agent(
            model=self.llm,
            mcp_servers=[
                MCPServerStdio(command="npx", args=["-y", "@upstash/context7-mcp@latest"])
            ]
        )

    async def chat(self, user_text: str, history: list[dict] = None) -> str:
        """
        Processes a user query via the unified agent.run() method.
        Note: The MCP server lifecycle is managed externally by the caller.
        """
        history = history or []
        
        # agent.run() is smart enough to either use a tool or just chat.
        result = await self.agent.run(user_text, message_history=history)
        
        return str(result.data)
```

---

## 3. The `anyio` CLI Pattern: Correct Lifecycle Management

This is the correct way to run the agent. The `run_mcp_servers` context manager wraps the **entire session loop**, not individual calls. This is efficient and ensures clean startup and shutdown.

```python
# src/cli.py
import anyio
from rich.prompt import Prompt
from agent import UnifiedAgent # Assuming the class from above

async def main():
    agent = UnifiedAgent(api_key="sk-...")
    history = []

    # The context manager wraps the entire loop, managing the MCP server's lifecycle.
    async with agent.agent.run_mcp_servers():
        print("Agent is ready. Ask a question or use a tool (e.g., 'calculate 10+5').")
        while True:
            # The lambda wrapper is essential for anyio.to_thread.run_sync
            user_input = await anyio.to_thread.run_sync(
                lambda: Prompt.ask("[bold cyan]You[/bold cyan]")
            )
            if user_input.lower() == "/exit":
                break

            reply = await agent.chat(user_input, history)
            
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": reply})
            print(f"[green]Agent:[/green] {reply}")

if __name__ == "__main__":
    try:
        anyio.run(main)
    except KeyboardInterrupt:
        print("\nGoodbye!")
```

---

## 4. Pre-Flight Checklist & Commands

Run these checks to validate your environment before you start coding.

```bash
# Recommended installation with a safe version range
pip install "pydantic-ai>=0.5,<1.0" anyio openai rich
```

| Step | Command | Purpose |
| :--- | :--- | :--- |
| **1. Check Versions** | `pip show pydantic-ai openai anyio` | Verify you have the correct, compatible libraries installed. |
| **2. Verify MCP Import** | `python -c "from pydantic_ai.mcp import MCPServerStdio; print('OK')"` | Confirms `pydantic-ai` is installed correctly. |
| **3. Test `anyio`** | `python -c "import anyio; print(f'anyio v{anyio.__version__} OK')"` | Confirms your async backend is ready. |
| **4. Pin Dependencies** | `pip freeze > requirements.txt` | Lock your working set of libraries for reproducible builds. |

---

## 5. Emergency Bypass (The Last Resort)

Only use this pattern for debugging or if you encounter a specific, reproducible bug in `agent.run()` that you cannot otherwise solve. **This should not be part of your standard architecture.**

```python
# Fallback direct OpenAI call for debugging
import openai

async def direct_openai_call(prompt: str) -> str:
    client = openai.AsyncOpenAI() # Assumes OPENAI_API_KEY is an env var
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

---

## 6. TL;DR Pocket Reference

| Task | The Gold Standard Code Snippet |
| :--- | :--- |
| **Create Agent** | `agent = Agent(model=OpenAIModel(...), mcp_servers=[...])` |
| **Run Agent with MCP** | `async with agent.run_mcp_servers(): await agent.run(...)` |
| **CLI Event Loop** | `anyio.run(main_function)` |
| **Threaded Input** | `await anyio.to_thread.run_sync(lambda: Prompt.ask(...))` |
| **Graceful Exit** | `try: anyio.run(main) except KeyboardInterrupt: ...` |
| **Message History** | Pass as `message_history=[{"role": ..., "content": ...}]` |

> *This guide codifies stability. Build with these patterns to create professional, modern AI agents.*

---
https://drive.google.com/file/d/1FLYoDd_1c5fNum_xTFxUZbOtTPifHbv8/view?usp=sharing, https://drive.google.com/file/d/1MWIHeVXwIVEdL8aICjRgHi343QpZ_R8f/view?usp=sharing, https://drive.google.com/file/d/1MzLZk57RAumnqOrHJL60aJv19Y-sh1lD/view?usp=sharing, https://aistudio.google.com/app/prompts?state=%7B%22ids%22:%5B%221RA9Qel0AfhGyunYsDWPyesabwvuvP2hi%22%5D,%22action%22:%22open%22,%22userId%22:%22108686197475781557359%22,%22resourceKeys%22:%7B%7D%7D&usp=sharing, https://drive.google.com/file/d/1Rge-RBbQKH91OnCVcYGggTzm1v47Q3p1/view?usp=sharing, https://drive.google.com/file/d/1Ueg9XjXTmIYayAnH8hFvcRbpgQtxmX8F/view?usp=sharing, https://drive.google.com/file/d/1u5kMEBKosFvErgcS5yXHa-XRX2ZSDBUf/view?usp=sharing

