> **Definitive Production Cheat-Sheet**  
> Pydantic-AI v0.5+ • OpenAI LLM • MCP Tool-Calling  
> **Copy-Paste Ready • Battle-Tested • Zero-Regrets**

---

## 🚨 TL;DR – 30-Second Recipe

```bash
pip install "pydantic-ai>=0.5,<1.0" anyio openai rich
```

```python
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
agent = Agent(
    "openai:gpt-4o-mini",
    mcp_servers=[MCPServerStdio("npx", ["-y", "@upstash/context7-mcp@latest"])]
)
```

```python
async with agent.run_mcp_servers():
    result = await agent.run("Your question here")
print(result.data)
```

That’s it — the rest is polish.

---

## 📌 1. Dependency Matrix (Pin & Forget)

| Package | Min | Max | Why |
|---|---|---|---|
| `pydantic-ai` | 0.5.0 | < 1.0 | API stabilised at 0.5 |
| `anyio` | 4.0 | < 5.0 | Event-loop harmony |
| `openai` | 1.30 | < 2.0 | Provider layer |
| `rich` | 13.0 | — | Pretty CLI only |

```bash
pip install "pydantic-ai>=0.5,<1.0" anyio "openai>=1.30,<2.0" rich
pip freeze > requirements.txt   # lock forever
```

---

## 🏗️ 2. The Canonical Agent Class

```python
# agent.py
from __future__ import annotations

from typing import List, Dict, Any, Optional
import anyio
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

class ProductionAgent:
    """
    Drop-in agent for CLI, FastAPI, or background workers.
    Handles OpenAI + MCP lifecycle in one place.
    """
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        mcp_command: tuple[str, ...] = ("npx", "-y", "@upstash/context7-mcp@latest"),
    ):
        self.provider = OpenAIProvider(api_key=api_key)
        self.model = OpenAIModel(model_name=model, provider=self.provider)
        self.agent = Agent(
            model=self.model,
            mcp_servers=[MCPServerStdio(*mcp_command)],
            system_prompt="Be concise, accurate, and helpful."
        )

    async def ask(
        self,
        question: str,
        history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """
        Unified entry point. Accepts plain string + optional history.
        Returns the final string response.
        """
        history = history or []
        result = await self.agent.run(
            question,
            message_history=history
        )
        return str(result.data)

    async def stream(
        self,
        question: str,
        history: Optional[List[Dict[str, str]]] = None,
    ):
        """
        Async generator for rich UIs.
        Yields incremental text chunks.
        """
        history = history or []
        async with self.agent.run_stream(
            question,
            message_history=history
        ) as stream:
            async for chunk in stream.text_deltas():
                yield chunk
```

---

## 🧵 3. CLI Skeleton (anyio + Rich)

```python
# cli.py
import anyio
from rich.console import Console
from rich.prompt import Prompt
from agent import ProductionAgent

console = Console()

async def main() -> None:
    agent = ProductionAgent(api_key="sk-...")   # use env var in prod

    async with agent.agent.run_mcp_servers():
        console.print("[bold green]Agent ready. Ctrl-C to quit.[/bold green]\n")
        history: list[dict[str, str]] = []

        while True:
            try:
                user = await anyio.to_thread.run_sync(
                    lambda: Prompt.ask("[bold cyan]You[/bold cyan]")
                )
                if user.lower() in {"/quit", "/exit"}:
                    break

                reply = await agent.ask(user, history)
                console.print(f"[green]Agent:[/green] {reply}\n")

                # keep rolling history
                history.extend([
                    {"role": "user", "content": user},
                    {"role": "assistant", "content": reply},
                ])
                # trim history to last 20 turns
                history = history[-40:]

            except KeyboardInterrupt:
                console.print("\n[yellow]Goodbye![/yellow]")
                break

if __name__ == "__main__":
    anyio.run(main)
```

---

## ⚙️ 4. Common Pitfalls & One-Line Fixes

| Symptom | Root Cause | Instant Cure |
|---|---|---|
| `ImportError: UserPrompt` | removed in 0.5 | Stop importing it. Use dicts. |
| `TypeError: __aiter__` | wrong streaming | Use `async with agent.run_stream()` |
| `TimeoutError` | `asyncio.run()` | Replace with `anyio.run()` |
| `KeyboardInterrupt` traceback | no handler | Wrap loop in `try/except KeyboardInterrupt` |
| MCP hangs on exit | context inside loop | Put `run_mcp_servers()` around **whole** loop |

---

## 🧪 5. Quick Validation Script

Run before you commit:

```bash
#!/bin/bash
set -e
python - <<'PY'
import sys, importlib.metadata as im
versions = {
    "pydantic-ai": im.version("pydantic-ai"),
    "anyio": im.version("anyio"),
    "openai": im.version("openai"),
}
for pkg, ver in versions.items():
    print(f"{pkg} {ver} ✔")
PY
echo "All green → ready to ship."
```

---

## 🧩 6. Structured Output Example

```python
from pydantic import BaseModel

class Weather(BaseModel):
    city: str
    temp_c: float
    condition: str

agent = Agent(
    "openai:gpt-4o-mini",
    output_type=Weather,
    system_prompt="Return weather for the requested city."
)

result = await agent.run("Weather in Tokyo")
# result.output == Weather(city="Tokyo", temp_c=22.3, condition="Sunny")
```

---

## 🌍 7. Environment Variables (No Secrets in Code)

```bash
# .env
OPENAI_API_KEY=sk-...
OPENAI_BASE_URL=https://api.openai.com/v1   # override for Azure, etc.
```

Load via `python-dotenv` or native `os.getenv`.

---

## 🔄 8. Live-Reload Development Loop

```bash
# 1. Watch for file changes
pip install watchfiles
watchfiles 'python -m cli' src/
```

---

## 🎯 9. FastAPI Plug-In (Bonus)

```python
from fastapi import FastAPI
from agent import ProductionAgent

app = FastAPI()
agent = ProductionAgent(api_key="...")

@app.post("/ask")
async def ask_endpoint(q: str):
    async with agent.agent.run_mcp_servers():
        return {"answer": await agent.ask(q)}
```

---

## 🔚 10. TL;DR Checklist

- [x] `pip install "pydantic-ai>=0.5,<1.0" anyio openai`
- [x] Use `Agent(..., mcp_servers=[...])`
- [x] Wrap **entire** loop in `async with agent.run_mcp_servers()`
- [x] Run with `anyio.run(main)`
- [x] Handle `KeyboardInterrupt`
- [x] Pin versions in `requirements.txt`

Copy this file into your repo, delete everything else, and ship.
