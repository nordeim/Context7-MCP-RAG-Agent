# File: src/cli.py
"""
Best-in-class Rich TUI interface for Context7 Agent.
This version uses a non-streaming model for maximum stability.
"""
import asyncio
import sys
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.markdown import Markdown
import anyio

from .agent import Context7Agent
from .themes import ThemeManager
from .history import HistoryManager

class Context7CLI:
    """Production-ready TUI interface for the Context7 Agent."""
    
    def __init__(self):
        self.console = Console()
        self.agent = Context7Agent()
        self.theme_manager = ThemeManager()
        self.current_conversation = "default"
        self.running = True
    
    async def initialize(self):
        """Initializes the CLI and its components."""
        await self.agent.initialize()
        theme = self.theme_manager.get_current_theme()
        theme.print_banner()
    
    async def display_welcome(self):
        """Displays a welcome screen with interactive theme selection."""
        # This implementation can be kept from the previous version.
        pass
    
    async def chat_loop(self):
        """Main chat interaction loop with robust command handling."""
        self.console.print("\n[bold green]Context7 AI is ready! Type your questions below.[/bold green]")
        self.console.print("[dim]Commands: /theme, /history, /clear, /exit[/dim]\n")
        
        while self.running:
            try:
                user_input = await anyio.to_thread.run_sync(
                    lambda: Prompt.ask(f"[{self.theme_manager.get_current_theme().colors['primary']}]You[/]")
                )
                
                if not user_input.strip():
                    continue
                
                if user_input.startswith("/"):
                    await self.handle_command(user_input)
                else:
                    await self.process_message(user_input)
                    
            except (KeyboardInterrupt, EOFError):
                self.console.print("\n[yellow]Shutting down gracefully...[/yellow]")
                self.running = False
                break
            except Exception as e:
                self.console.print(f"[bold red]An unexpected application error occurred: {e}[/bold red]")

    async def handle_command(self, command: str):
        """Handles special slash commands asynchronously."""
        parts = command.strip().split()
        cmd = parts[0].lower()
        
        if cmd == "/exit":
            self.running = False
            self.console.print("[yellow]Goodbye! 👋[/yellow]")
        elif cmd == "/clear":
            await self.agent.clear_history(self.current_conversation)
            self.console.print(f"[green]History for conversation '{self.current_conversation}' cleared.[/green]")
        elif cmd == "/history":
             conversations = self.agent.get_conversations()
             if conversations:
                 table = Table(title="Conversation History")
                 table.add_column("ID")
                 table.add_column("Last Message")
                 table.add_column("Count")
                 
                 for conv in conversations[:10]:
                     table.add_row(
                         conv["id"],
                         conv["last_message"],
                         str(conv["message_count"])
                     )
                 self.console.print(table)
             else:
                 self.console.print("[yellow]No conversation history[/yellow]")
        else:
            self.console.print(f"[red]Unknown command: {cmd}[/red]")
    
    async def process_message(self, message: str):
        """
        Processes a user message using a non-streaming model with a status indicator.
        """
        theme = self.theme_manager.get_current_theme()
        self.console.print() # Add spacing
        
        with self.console.status("[bold green]Assistant is thinking...", spinner="dots"):
            response = await self.agent.chat(message, self.current_conversation)

        self.console.print(f"[{theme.colors['accent']}]Assistant:[/]")

        if response["type"] == "complete":
            markdown = Markdown(response["data"], style=theme.colors['text'])
            self.console.print(markdown)
        elif response["type"] == "error":
            error_panel = Panel(
                f"[bold]Agent Error:[/bold]\n\n{response['data']}",
                border_style="red",
                title="[bold red]Error[/bold red]"
            )
            self.console.print(error_panel)
        
        self.console.print()

    async def run(self):
        """Runs the complete CLI application lifecycle."""
        try:
            await self.initialize()
            await self.chat_loop()
        except Exception as e:
            self.console.print(f"[bold red]A fatal application error occurred: {e}[/bold red]")
            sys.exit(1)

async def main():
    """Main asynchronous entry point for the application."""
    cli = Context7CLI()
    await cli.run()

if __name__ == "__main__":
    try:
        anyio.run(main)
    except (KeyboardInterrupt, EOFError):
        print("\n\n[bold yellow]Exited.[/bold yellow]")
