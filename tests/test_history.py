"""Tests for history management."""

import pytest
import asyncio
import tempfile
import json
from pathlib import Path
from src.history import HistoryManager

@pytest.mark.asyncio
async def test_history_save_load():
    """Test saving and loading history."""
    with tempfile.TemporaryDirectory() as tmpdir:
        history_path = Path(tmpdir) / "test_history.json"
        
        manager = HistoryManager()
        manager.history_path = history_path
        
        await manager.save_message("test", "Hello", "Hi there")
        await manager.load()
        
        messages = manager.get_messages("test")
        assert len(messages) == 1
        assert messages[0]["user"] == "Hello"
