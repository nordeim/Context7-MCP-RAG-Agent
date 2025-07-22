<think>
### **Deep Thinking & Planning Phase: Diagnosing the "No Results" Failure**

1.  **Deconstruct the Goal:** The user has implemented my "Hard Enforcement" RAG fix, but it now consistently fails to find documents, always returning the "I could not find any relevant information..." message. This indicates a failure somewhere within the new three-step pipeline in `chat_stream`. The user has requested diagnostic `print` statements to trace the intermediate steps and identify the point of failure.

2.  **Analyze the Failure Mode:** The output is consistent and repeatable. This is good; it's not a random fluke. The agent *is* correctly reaching the fallback condition I coded, which means the main `try/except` block isn't catching a top-level error. The failure must be happening within one of the three RAG steps and is being handled by the `try...except (json.JSONDecodeError, ValueError)` block within the `chat_stream` method.

3.  **Hypothesize Potential Failure Points in the RAG Pipeline:**
    *   **Step 1 Failure (Query Formulation):** Could the `query_formulation_agent` be failing? Maybe it's not returning a clean string. The prompt asks it to return "ONLY the search query string," but LLMs can be verbose. It might be returning something like `"Here is the search query: 'pydantic-ai agents'"`. My `strip().strip('"')` logic might not be robust enough to handle all variations. **This is a strong possibility.**
    *   **Step 2 Failure (Tool Execution):**
        *   **Tool Name Mismatch:** My code hard-codes the tool call as `f"search(query='{search_query}')"`. What if the actual tool name exposed by the `@upstash/context7-mcp@latest` server isn't `search`? What if it's `context7_search` or `query_documents`? If the tool name is wrong, the `agent.run()` call would fail to find a matching tool and might return an empty or error-like result. **This is a very strong possibility and a classic integration bug.**
        *   **Server Not Responding:** The MCP server process starts, but could it be failing internally or not responding to the `call_tool` request correctly? The agent might time out or receive an empty response.
    *   **Step 3 Failure (Parsing the Tool's Output):** The `json.loads(str(retrieval_result.data))` line assumes the tool returns a valid JSON string. If the tool returns a plain text error message (e.g., "Error: No results found") or a malformed JSON, `json.loads` will fail, triggering my fallback condition. **This is also a very strong possibility.**

4.  **Formulate a Diagnostic Plan:** The user's request for `print` statements is exactly the right approach. I will instrument the `chat_stream` method with clear, diagnostic print statements to make the invisible intermediate steps visible.

    *   I'll print the `search_query` right after it's formulated (after stripping). This will validate Step 1.
    *   I'll print the exact `tool_execution_prompt` string I'm constructing. This will validate the tool name and query being passed.
    *   Most importantly, I will print the raw `retrieval_result.data` *before* attempting to parse it as JSON. This will be the "smoking gun" that tells us exactly what the MCP tool is returning. Is it an error? Is it empty? Is it malformed JSON? Is it a success message that isn't JSON?
    *   I will also add a print statement inside the `except` block that triggers the "I could not find..." message, so we know exactly why it's failing.

5.  **Identify Files for Modification:**
    *   `src/agent.py`: This is the only file that needs to be modified. I will be adding `print` statements to the `chat_stream` method.
    *   All other files remain unchanged.

6.  **Execution Plan:**
    *   **Step 1:** Systematically add diagnostic `print` statements with clear labels (e.g., `[DEBUG-STEP-1]`, `[DEBUG-STEP-2]`) to the `chat_stream` method in `src/agent.py`.
    *   **Step 2:** The print statements should use a distinct color or formatting to stand out from the application's normal UI output. I will use `rich.print` with a style for this.
    *   **Step 3:** Generate the complete, updated replacement file for `src/agent.py`.
    *   **Step 4:** Perform a line-by-line validation against the previous "Hard Enforcement" version to confirm that only the diagnostic prints have been added and the core logic remains the same.
    *   **Step 5:** Write a summary report explaining where each print statement has been added and what hypothesis it is designed to test. This will empower the user to run the code and interpret the results themselves to find the definitive root cause.

This plan is safe, targeted, and directly addresses the user's request. It will convert the black box of the RAG pipeline into a glass box, allowing us to pinpoint the exact point of failure.

</think>

### **Execution Phase: Generating the Instrumented Code for Diagnosis**

You are absolutely right to ask for instrumentation. The current behavior indicates a silent failure within our "Hard Enforcement" pipeline. The most effective way to debug this is to add clear, diagnostic print statements to illuminate each step of the process.

I have meticulously updated `src/agent.py` to include this crucial logging. The new version will print the intermediate inputs and outputs, allowing us to see exactly where the logic is breaking down.

Here is the complete and updated replacement file for `src/agent.py` with diagnostics.

```python
"""
Production-ready AI agent with Pydantic AI and MCP integration.
This version implements a robust "Hard Enforcement" Retrieval-Augmented
Generation (RAG) pattern. The application logic now explicitly controls the
multi-step process of query formulation, tool execution, and answer synthesis.
*** THIS VERSION INCLUDES DIAGNOSTIC PRINT STATEMENTS FOR DEBUGGING ***
"""

import asyncio
import json
from typing import List, Dict, Any, Optional, AsyncGenerator
from datetime import datetime
import logging

# Import rich for styled, clear diagnostic printing
from rich import print as rprint

from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from .config import config
from .history import HistoryManager

logger = logging.getLogger(__name__)

class Context7Agent:
    """Production-ready AI agent implementing a hard-enforced RAG pattern."""
    
    def __init__(self):
        """Initialize with correct Pydantic AI v0.5+ patterns and a synthesis-focused system prompt."""
        self.provider = OpenAIProvider(
            api_key=config.openai_api_key,
            base_url=config.openai_base_url
        )
        
        self.model = OpenAIModel(
            model_name=config.openai_model,
            provider=self.provider
        )
        
        self.mcp_server = MCPServerStdio(
            command="npx",
            args=["-y", "@upstash/context7-mcp@latest"]
        )
        
        self.agent = Agent(
            model=self.model,
            mcp_servers=[self.mcp_server],
            system_prompt="""
            You are a helpful AI research assistant. Your task is to provide a clear and comprehensive answer to the user's question based *only* on the provided context documents. Synthesize the information from the various documents into a single, coherent response. If the context is insufficient to answer the question, state that clearly.
            """
        )
        
        self.history = HistoryManager()
    
    async def initialize(self):
        """Initialize the agent and load history."""
        await self.history.load()
    
    async def chat_stream(
        self, 
        message: str, 
        conversation_id: Optional[str] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream chat responses using a hard-enforced, two-step RAG pipeline with diagnostics.
        """
        try:
            rprint("[bold yellow]--- Starting RAG Pipeline ---[/bold yellow]")
            async with self.agent.run_mcp_servers():
                # =====================================================================
                # == STEP 1: FORMULATE SEARCH QUERY                                  ==
                # =====================================================================
                rprint("[bold yellow][DEBUG-STEP-1A][/bold yellow] Formulating search query from user message...")
                query_formulation_prompt = f"""
                Based on the user's request, what is the optimal, concise search query for the Context7 documentation database?
                The user's request is: "{message}"
                Return ONLY the search query string, and nothing else.
                """
                
                query_formulation_agent = Agent(model=self.model)
                query_result = await query_formulation_agent.run(query_formulation_prompt)
                search_query = str(query_result.data).strip().strip('"')

                rprint(f"[bold yellow][DEBUG-STEP-1B][/bold yellow] Formulated Search Query: [cyan]'{search_query}'[/cyan]")

                if not search_query:
                    raise ValueError("LLM failed to formulate a search query.")
                
                # =====================================================================
                # == STEP 2: EXPLICITLY EXECUTE THE TOOL                             ==
                # =====================================================================
                # The name of the tool 'search' is assumed. A common bug is that the tool
                # name is actually different (e.g., 'context7_search').
                tool_execution_prompt = f"search(query='{search_query}')"
                rprint(f"[bold yellow][DEBUG-STEP-2A][/bold yellow] Executing explicit tool call with prompt: [cyan]'{tool_execution_prompt}'[/cyan]")
                
                retrieval_result = await self.agent.run(tool_execution_prompt)
                
                # This is the most critical diagnostic print. It shows the RAW output from the tool.
                rprint(f"[bold yellow][DEBUG-STEP-2B][/bold yellow] Raw data received from tool call:")
                rprint(f"[dim white]{retrieval_result.data}[/dim white]")

                try:
                    retrieved_docs = json.loads(str(retrieval_result.data))
                    if not isinstance(retrieved_docs, list) or not retrieved_docs:
                        # This will trigger if the tool returns an empty list `[]`.
                        raise ValueError("Tool returned no documents or an empty list.")
                except (json.JSONDecodeError, ValueError) as e:
                    # This will trigger if the tool output is not valid JSON or if it's empty.
                    rprint(f"[bold red][DEBUG-FAIL][/bold red] Failed to parse tool output. Reason: {e}")
                    rprint("[bold red]--- RAG Pipeline Failed ---[/bold red]")
                    yield {
                        "type": "content",
                        "data": "I could not find any relevant information in the Context7 knowledge base to answer your question.",
                        "timestamp": datetime.now().isoformat()
                    }
                    return

                rprint(f"[bold green][DEBUG-STEP-2C][/bold green] Successfully parsed {len(retrieved_docs)} document(s) from tool output.")
                
                # =====================================================================
                # == STEP 3: SYNTHESIZE THE FINAL ANSWER                             ==
                # =====================================================================
                rprint("[bold yellow][DEBUG-STEP-3A][/bold yellow] Synthesizing final answer based on retrieved documents...")
                synthesis_prompt = f"""
                Here is the context retrieved from the Context7 documentation database:
                ---
                {json.dumps(retrieved_docs, indent=2)}
                ---
                Based ONLY on the context provided above, provide a comprehensive answer to the user's original question: "{message}"
                """
                
                final_result = await self.agent.run(synthesis_prompt)
                content = str(final_result.data)
                
                rprint("[bold green][DEBUG-STEP-3B][/bold green] Synthesis complete.")
                rprint("[bold green]--- RAG Pipeline Succeeded ---[/bold green]")

                yield {
                    "type": "content",
                    "data": content,
                    "timestamp": datetime.now().isoformat()
                }
                
                await self.history.save_message(conversation_id or "default", message, content)
                
                yield {
                    "type": "complete",
                    "data": content,
                    "timestamp": datetime.now().isoformat()
                }

        except Exception as e:
            logger.error(f"Agent RAG pipeline error: {e}")
            rprint(f"[bold red][DEBUG-FATAL-ERROR][/bold red] An unexpected exception occurred in the RAG pipeline: {e}")
            yield {
                "type": "error",
                "data": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def search_documents(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search documents using MCP tools with proper error handling."""
        try:
            async with self.agent.run_mcp_servers():
                search_prompt = f"""
                Search the Context7 knowledge base for documents about: {query}
                Return up to {limit} most relevant results with titles, sources, and brief summaries.
                """
                result = await self.agent.run(search_prompt)
                response_text = str(result.data)
                try:
                    if response_text.strip().startswith('[') or response_text.strip().startswith('{'):
                        parsed = json.loads(response_text)
                        if isinstance(parsed, list):
                            return parsed
                        else:
                            return [parsed]
                except json.JSONDecodeError:
                    pass
                return [{
                    "title": "Search Results",
                    "content": response_text,
                    "source": "Context7 MCP",
                    "score": 1.0
                }]
        except Exception as e:
            logger.error(f"Search error: {e}")
            return [{"title": "Search Error", "content": f"Unable to search documents: {str(e)}", "source": "Error", "score": 0.0}]
    
    def get_conversations(self) -> List[Dict[str, Any]]:
        """Get all conversation histories."""
        return self.history.get_conversations()
    
    async def clear_history(self, conversation_id: Optional[str] = None):
        """Clear conversation history."""
        await self.history.clear(conversation_id)
```

---

### **Post-Generation Review and Validation**

*   **Line-by-Line "Diff" with Previous File:**
    *   **Imports:** A new import, `from rich import print as rprint`, has been correctly added.
    *   **`__init__`:** Identical. No changes to the core agent setup.
    *   **`chat_stream`:** This method is the focus of the changes. The core three-step logic is preserved, but `rprint` statements have been strategically inserted between each logical step to provide a trace of the execution flow. A new print statement was also added to the `except` block to give the specific reason for parsing failures. This perfectly matches the diagnostic plan.
    *   **Other Methods:** All other methods (`initialize`, `search_documents`, etc.) are identical, ensuring no regressions.

*   **Validation Result:** **Success.** The new file is a perfect, safe, and powerful diagnostic version of the "Hard Enforcement" RAG agent.

### **Summary and How to Interpret the New Output**

I have successfully instrumented the agent's core logic with diagnostic print statements. When you run the application with this updated `src/agent.py` file, you will now see yellow, green, and red debug messages in your terminal that trace the agent's internal thought process.

**Please run the application again and observe the new `[DEBUG-...]` output. Pay closest attention to these two lines:**

1.  **`[DEBUG-STEP-2A] Executing explicit tool call with prompt: ...`**
    *   This tells you what the agent is *trying* to do.

2.  **`[DEBUG-STEP-2B] Raw data received from tool call: ...`**
    *   This is the **most important piece of evidence.** This will show you exactly what the `Context7` MCP server is returning.

Based on this output, you will be able to definitively diagnose the problem:
*   If the "Raw data" is an error message like `"Error: Tool 'search' not found"`, then the hard-coded tool name in the prompt is wrong.
*   If the "Raw data" is an empty string `''` or `None`, then the MCP server is failing to respond correctly.
*   If the "Raw data" is a plain text sentence like `"No results were found."`, then it's not valid JSON, and the `json.loads()` call is correctly failing.
*   If the "Raw data" is an empty JSON list `[]`, our new `ValueError` will correctly catch it and trigger the fallback.

This instrumented code transforms the problem from a mystery into a solvable puzzle. I await the results of your next run.
