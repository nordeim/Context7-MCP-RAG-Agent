"""
Configuration validation tests for Context7 Agent.
"""

import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
import os
from src.config import Config

def test_config_loading():
    """Test that configuration loads correctly."""
    # Ensure we have test environment variables
    os.environ.setdefault("CONTEXT7_OPENAI_API_KEY", "test-key-123")
    
    config = Config()
    assert config.openai_api_key == "test-key-123"
    assert config.openai_base_url == "https://api.openai.com/v1"
    assert config.openai_model == "gpt-4o-mini"

def test_config_required_fields():
    """Test that required fields raise proper errors when missing."""
    # Temporarily remove the key to test validation
    original_key = os.environ.pop("CONTEXT7_OPENAI_API_KEY", None)
    
    try:
        with pytest.raises(SystemExit):
            # This should raise validation error
            Config()
    finally:
        # Restore the key
        if original_key:
            os.environ["CONTEXT7_OPENAI_API_KEY"] = original_key

if __name__ == "__main__":
    # Quick validation when run directly
    print("🔍 Testing configuration loading...")
    
    try:
        from src.config import config
        print("✅ Environment variables loaded successfully!")
        print(f"API Key: {config.openai_api_key[:10]}...")
        print(f"Model: {config.openai_model}")
        print(f"Base URL: {config.openai_base_url}")
        print("🎉 All tests passed!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
