"""Tests for the Context7 Agent."""

import pytest
import asyncio
from src.agent import Context7Agent

@pytest.mark.asyncio
async def test_agent_initialization():
    """Test agent initialization."""
    agent = Context7Agent()
    await agent.initialize()
    assert agent.agent is not None

@pytest.mark.asyncio
async def test_chat_stream():
    """Test chat streaming."""
    agent = Context7Agent()
    await agent.initialize()
    
    chunks = []
    async for chunk in agent.chat_stream("Hello", "test"):
        chunks.append(chunk)
    
    assert len(chunks) > 0
    assert any(c["type"] == "complete" for c in chunks)
