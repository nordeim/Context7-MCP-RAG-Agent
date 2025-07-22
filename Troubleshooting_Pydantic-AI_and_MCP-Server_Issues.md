# Title: The Definitive Troubleshooting Chronicle: From Streaming Errors to a Stable RAG Agent

## 📋 Executive Summary

This guide chronicles the complete, real-world troubleshooting journey of integrating `pydantic-ai==0.4.2` with the Context7 MCP server. It documents a series of critical, and often subtle, errors, from initial type mismatches to complex API usage errors. This document serves as a canonical reference and a "book of errors" to help developers understand the *process* of arriving at a stable solution.

The key lesson learned is that while `pydantic-ai` offers a streaming API, its usage in version `0.4.2` is non-obvious and prone to error. The most robust, stable, and debuggable architecture for this stack is a **non-streaming, request-response model** using the `await agent.run()` method. This guide details the path that led to this critical architectural conclusion.

---

## 🔧 Problem Timeline & Solutions: A Step-by-Step Debugging Journey

This section follows the logical progression of errors encountered when building the agent, from simple configuration mistakes to deep API contract violations.

### **Stage 1: Initial Setup Errors**

These are the common "Day 1" errors that are quickly resolved.

*   **Error 1: `AttributeError: 'list' object has no attribute 'split'`**
    *   **Symptom:** The app crashes instantly on agent initialization.
    *   **Root Cause:** The `model` parameter was passed as `"gpt-4o-mini"` instead of the required provider-prefixed format.
    *   **Solution:** Always use the format `"{provider}:{model_name}"`, e.g., **`model="openai:gpt-4o-mini"`**.

*   **Error 2: `MCPServerError: MCP server is not running`**
    *   **Symptom:** The agent fails when trying to use the `search` tool.
    *   **Root Cause:** The external MCP process was defined but never started.
    *   **Solution:** Wrap all agent calls (`.run()` or `.run_stream()`) in the `async with agent.run_mcp_servers():` context manager.

---

### **Stage 2: The Deep `AssertionError` - A Flawed Hypothesis**

This was the first truly difficult error, which led down an incorrect path.

*   **Symptom:** `AssertionError: Expected code to be unreachable, but got: {'role': 'user', ...}`
*   **Initial (Flawed) Hypothesis:** The library must not want a plain `list[dict]` for `message_history`. It is named `pydantic-ai`, so it must require a list of Pydantic model instances (e.g., `UserMessage`, `AssistantMessage`).
*   **The Flawed Fix:** The `HistoryManager` was modified to import message models from `pydantic-ai` and instantiate them, returning a `list` of Pydantic objects.

---

### **Stage 3: The `ImportError` Cascade - Proving the Hypothesis Wrong**

The attempt to use Pydantic models for history resulted in a cascade of `ImportError` exceptions, each revealing more about the library's true, non-obvious structure.

*   **Error 1: `ModuleNotFoundError: No module named 'pydantic_ai.message'`**
    *   **Analysis:** The module name was wrong. Deeper inspection revealed it should be plural.
    *   **Attempted Fix:** Changed import to `from pydantic_ai.messages import ...`.

*   **Error 2: `ImportError: cannot import name 'Message' from 'pydantic_ai.messages'`**
    *   **Analysis:** The base `Message` class is internal (`_Message`) and not exported.
    *   **Attempted Fix:** Changed import to only `UserMessage` and `AssistantMessage`.

*   **Error 3: `ImportError: cannot import name 'UserMessage' ... Did you mean: 'ModelMessage'?`**
    *   **Analysis:** This was the critical clue. The library uses the non-standard name `ModelMessage` for the AI's responses. However, the error on `UserMessage` was deeply confusing.
    *   **Attempted Fix:** Changed import to `UserMessage` and `ModelMessage`, replacing `AssistantMessage`.

*   **Final Error in Stage: The exact same `ImportError` on `UserMessage`**
    *   **Definitive Conclusion:** The cycle proved that the fundamental assumption from Stage 2 was wrong. The library **does not** want a list of Pydantic models for its `message_history`. The `AssertionError` had a different, unknown cause. The only path forward was to revert `HistoryManager` to return a plain `list[dict]` and abandon this flawed approach entirely.

---

### **Stage 4: The Streaming API Battle - The Final Pivot**

With the `ImportError` resolved by reverting to `list[dict]`, the application could finally run, revealing the final set of errors related to the streaming API.

*   **Error 1: `TypeError: 'async for' requires ... got _AsyncGeneratorContextManager`**
    *   **Analysis:** `agent.run_stream()` returns a context manager, not a direct iterator.
    *   **Solution:** Correctly wrapped the loop: `async with agent.run_stream(...) as stream:`.

*   **Error 2: `TypeError: 'async for' requires ... got StreamedRunResult`**
    *   **Analysis:** The context manager yields a `StreamedRunResult` container object, which is not itself iterable.
    *   **Hypothesis:** The iterator must be in an attribute, likely `.data`.
    *   **Attempted Fix:** Changed loop to `async for chunk in stream.data:`.

*   **Error 3: `AttributeError: 'StreamedRunResult' object has no attribute 'data'`**
    *   **Final, Definitive Analysis:** This error proved that the `StreamedRunResult` object in `v0.4.2` has no obvious public attribute for iteration. The entire streaming approach was brittle and non-obvious.

### **Conclusion: The Strategic Pivot to Stability**

The intractable nature of the streaming API errors led to a final, crucial architectural decision: **abandon streaming in favor of the known-stable, non-streaming `await agent.run()` method.** This prioritizes correctness, stability, and reliability over a single, problematic feature. The final, robust architecture uses a request-response pattern, which is simpler to implement, debug, and maintain.

