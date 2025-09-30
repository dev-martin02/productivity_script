#!/usr/bin/env python3
"""
Productivity Script - A friendly CLI tool for focused study sessions
"""
import typer
from rich.prompt import Prompt
from rich.console import Console
from rich.panel import Panel
from features.terminal.util import execute_bash_blocking_script
from features.terminal.index import start_study_mode
from features.google.index import get_tasks

# Initialize Typer app and Rich console
app = typer.Typer(
    name="productivity",
    help="🎯 A friendly productivity tool for focused study sessions",
    rich_markup_mode="rich",
)
console = Console()
@app.command()
def study():
    """
    🎓 Start a focused study session with website blocking and reflection.
    
    This is the main study mode that helps you stay focused by:
    - Setting up a distraction-free environment  
    - Blocking distracting websites
    - Timing your study session
    - Conducting post-session reflection
    """
    start_study_mode()

@app.command()
def tasks():
    """
    📝 View your Google Tasks (requires authentication setup).
    """
    console.print(Panel.fit(
        "[bold blue]📝 Google Tasks Integration[/bold blue]",
        border_style="blue"
    ))
    
    try:
        get_tasks()
    except Exception as e:
        console.print(f"[red]Error accessing Google Tasks: {e}[/red]")
        console.print("[yellow]Make sure you have set up Google API authentication.[/yellow]")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    🎯 Productivity Script - Your friendly study companion!
    
    A beautiful CLI tool that helps you maintain focused study sessions.
    """
    if ctx.invoked_subcommand is None:
        # Check for tasks first

        # Show welcome message when no command is provided
        console.print(Panel.fit(
            "[bold green]🎯 Welcome to Productivity Script![/bold green]\n\n"
            "[bold]Available commands:[/bold]\n"
            "• [cyan]study[/cyan] - Start a focused study session\n"
            "• [cyan]tasks[/cyan] - View your Google Tasks\n\n"
            "[dim]Use --help with any command for more information[/dim]\n"
            "[dim]Example: python3 index.py study --help[/dim]",
            title="🚀 Productivity Script",
            border_style="green"
        ))
        
        
        action = Prompt.ask('What would you like to do ?')
        
        if action.lower() == "study":
            start_study_mode()
        elif action.lower() == "tasks":
            console.print(Panel.fit(
                "[bold blue]📝 Google Tasks Integration[/bold blue]",
                border_style="blue"
            ))
            try:
                get_tasks()
            except Exception as e:
                console.print(f"[red]Error accessing Google Tasks: {e}[/red]")
                console.print("[yellow]Make sure you have set up Google API authentication.[/yellow]")
        elif action.lower() == "exit":
            console.print("[dim]👋 See you later! Stay productive![/dim]")
            raise typer.Exit()

if __name__ == "__main__":
    tasks = get_tasks()
    if len(tasks) > 0:
        console.print(Panel.fit(
            "[bold red]📝 You have tasks to do![/bold red]"))
        # Display the tasks in a list
        for task in tasks:
            console.print(f"[bold]Task: {task['title']}[/bold]")
        
        execute_bash_blocking_script('block')
        console.print('[green]Websites blocked for focus![/green]')

    app()
