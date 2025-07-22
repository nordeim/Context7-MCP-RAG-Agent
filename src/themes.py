"""
Stunning theme system with animations and ASCII art.
"""

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.layout import Layout
from rich.live import Live
from rich.prompt import Prompt
from rich.align import Align
from rich.columns import Columns
import random
import time
from typing import Dict, Any, List

class Theme:
    """Base theme class with color schemes and animations."""
    
    def __init__(self, name: str):
        self.name = name
        self.console = Console()
        self.colors = self._get_colors()
        self.ascii_art = self._get_ascii_art()
    
    def _get_colors(self) -> Dict[str, str]:
        """Get color scheme for the theme."""
        schemes = {
            "cyberpunk": {
                "primary": "#ff00ff",
                "secondary": "#00ffff",
                "accent": "#ffff00",
                "background": "#0a0a0a",
                "text": "#ffffff"
            },
            "ocean": {
                "primary": "#0077be",
                "secondary": "#00cccc",
                "accent": "#ffd700",
                "background": "#001a33",
                "text": "#e6f3ff"
            },
            "forest": {
                "primary": "#228b22",
                "secondary": "#90ee90",
                "accent": "#ffd700",
                "background": "#0f1f0f",
                "text": "#f5f5dc"
            },
            "sunset": {
                "primary": "#ff4500",
                "secondary": "#ff8c00",
                "accent": "#ffd700",
                "background": "#2f1b14",
                "text": "#fff8dc"
            }
        }
        return schemes.get(self.name, schemes["cyberpunk"])
    
    def _get_ascii_art(self) -> str:
        """Get ASCII art banner for the theme."""
        arts = {
            "cyberpunk": """
    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
    ██ ▄▄▄ ██ ▀██ ██ ▄▄▀██ ▄▄▄██ ▄▄▀
    ██ ███ ██ █ █ ██ ██ ██ ▄▄▄██ ▀▀▄
    ██ ▀▀▀ ██ ██▄ ██ ▀▀ ██ ▀▀▀██ ██
    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
    CONTEXT7 AI - CYBERPUNK MODE ACTIVATED
            """,
            "ocean": """
     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
     ▓▓░▓▓░▓▓░▓▓░▓▓░▓▓░▓▓░▓▓░▓▓░▓▓░▓▓░
     ▓▓░▓▓░▓▓░▓▓░▓▓░▓▓░▓▓░▓▓░▓▓░▓▓░▓▓░
     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
     CONTEXT7 AI - OCEAN DEPTH EXPLORER
            """,
            "forest": """
    ╔═══════════════════════════════════╗
    ║ 🌲 🌳 🌲 🌳 🌲 🌳 🌲 🌳 🌲 🌳 ║
    ║    CONTEXT7 AI - FOREST GUARDIAN   ║
    ║ 🌳 🌲 🌳 🌲 🌳 🌲 🌳 🌲 🌳 🌲 ║
    ╚═══════════════════════════════════╝
            """,
            "sunset": """
    ☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️
    🌅 CONTEXT7 AI - SUNSET SAGA 🌅
    ☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️
            """
        }
        return arts.get(self.name, arts["cyberpunk"])
    
    def print_banner(self):
        """Display theme banner with animations."""
        self.console.print(f"\n[{self.colors['primary']}]{self.ascii_art}[/{self.colors['primary']}]\n")
    
    def create_search_table(self, results: List[Dict[str, Any]]) -> Table:
        """Create a styled table for search results."""
        table = Table(
            title=f"[{self.colors['accent']}]Search Results[/{self.colors['accent']}]",
            border_style=self.colors['secondary'],
            header_style=self.colors['primary']
        )
        
        table.add_column("Title", style=self.colors['text'])
        table.add_column("Source", style=self.colors['secondary'])
        table.add_column("Relevance", style=self.colors['accent'])
        
        for result in results[:10]:
            table.add_row(
                result.get('title', 'Unknown'),
                result.get('source', 'Context7'),
                f"{result.get('score', 0):.2f}"
            )
        
        return table
    
    def create_progress_spinner(self) -> Progress:
        """Create a themed progress spinner."""
        return Progress(
            SpinnerColumn(style=self.colors['primary']),
            TextColumn("[{task.description}]", style=self.colors['text']),
            console=self.console
        )

class ThemeManager:
    """Manages theme switching and animations."""
    
    def __init__(self):
        self.themes = {
            "cyberpunk": Theme("cyberpunk"),
            "ocean": Theme("ocean"),
            "forest": Theme("forest"),
            "sunset": Theme("sunset")
        }
        self.current_theme = "cyberpunk"
    
    def set_theme(self, theme_name: str) -> bool:
        """Switch to a new theme."""
        if theme_name in self.themes:
            self.current_theme = theme_name
            return True
        return False
    
    def get_current_theme(self) -> Theme:
        """Get the current theme."""
        return self.themes[self.current_theme]
    
    def list_themes(self) -> List[str]:
        """List available themes."""
        return list(self.themes.keys())
    
    def print_typing_effect(self, text: str, speed: int = 50):
        """Print text with typing animation effect."""
        theme = self.get_current_theme()
        for char in text:
            theme.console.print(char, end="", style=theme.colors['text'])
            time.sleep(1 / speed)
        theme.console.print()
