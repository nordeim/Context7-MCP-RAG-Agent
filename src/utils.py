"""
Utility functions for the Context7 Agent.
"""

import re
from typing import List, Dict, Any
import hashlib

def extract_code_blocks(text: str) -> List[Dict[str, str]]:
    """Extract code blocks from text."""
    pattern = r'```(\w+)?\n(.*?)\n```'
    matches = re.findall(pattern, text, re.DOTALL)
    
    return [
        {"language": lang or "text", "code": code.strip()}
        for lang, code in matches
    ]

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage."""
    return re.sub(r'[^\w\s-]', '', filename).strip()

def generate_conversation_id(query: str) -> str:
    """Generate a unique conversation ID from query."""
    return hashlib.md5(query.encode()).hexdigest()[:8]

def format_search_result(result: Dict[str, Any]) -> str:
    """Format a search result for display."""
    title = result.get('title', 'Untitled')
    source = result.get('source', 'Unknown')
    score = result.get('score', 0)
    snippet = result.get('snippet', '')[:200] + "..."
    
    return f"""
📄 **{title}**
Source: {source} | Relevance: {score:.2f}
{snippet}
    """.strip()

def fuzzy_match(query: str, text: str) -> float:
    """Simple fuzzy matching score."""
    query_words = query.lower().split()
    text_words = text.lower().split()
    
    matches = sum(1 for qw in query_words if any(qw in tw for tw in text_words))
    return matches / len(query_words) if query_words else 0
