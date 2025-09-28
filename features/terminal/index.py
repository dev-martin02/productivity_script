#!/usr/bin/env python3
from datetime import date
import subprocess
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.panel import Panel
from features.terminal.util import countdown_timer, bell_notification_sound

# Initialize console
console = Console()

def create_folder(subject: str) -> Path:
    """Create a study folder for the given subject."""
    home_directory = Path.home()
    desktop_path = home_directory / "Desktop" / "study" / subject
    desktop_path.mkdir(parents=True, exist_ok=True)
    return desktop_path

def write_to_file(subject: str, content: str):
    """Write content to a reflection file for the subject."""
    folder_path = create_folder(subject)
    file_name = f'reflection-{date.today()}.txt'
    full_path = folder_path / file_name
    
    with open(full_path, 'a', encoding='utf-8') as file:
        file.write(content)

def conduct_reflection(subject: str):
    """Conduct post-session reflection questions."""
    console.print("\n" + "="*50)
    console.print("[bold cyan]📝 Session Reflection[/bold cyan]")
    console.print("="*50)
    
    after_session = [
        'What did you learn today?', 
        'How would you rate your performance today? (on scale of 1 to 5)',
        'Why do you think it was like that?', 
        'What would you do next time?'
    ]
    
    reflection_content = f"\n--- Reflection for {date.today()} ---\n"
    
    for question in after_session:
        response = Prompt.ask(f"[bold yellow]{question}[/bold yellow]")
        reflection_content += f"{question} {response}\n"
    
    write_to_file(subject, reflection_content)
    console.print(f"[green]✅ Reflection saved to ~/Desktop/study/{subject}/[/green]")

def before_study_session():
    """Interactive pre-study session setup."""
    console.print(Panel.fit(
        "[bold green]🎯 Welcome to Study Mode![/bold green]\n"
        "Let's set up your focused study session!",
        border_style="green"
    ))
    
    # Ask the three main questions
    questions = [
        'What subject would you focus on today?', 
        'What exactly you would work on?', 
        'How long would you like your session to last (in minutes)?'
    ]
    
    subject = ""
    focus_on = ""
    session_time = 0
    
    for index, question in enumerate(questions):
        if index == 0:
            subject = Prompt.ask(f"[bold cyan]{question}[/bold cyan]")
        elif index == 1:
            focus_on = Prompt.ask(f"[bold cyan]{question}[/bold cyan]") 
        elif index == 2:
            session_time = IntPrompt.ask(f"[bold cyan]{question}[/bold cyan]")
    
    # Show session summary
    console.print(Panel(
        f"[bold]Subject:[/bold] {subject}\n"
        f"[bold]Focus:[/bold] {focus_on}\n"
        f"[bold]Duration:[/bold] {session_time} minutes",
        title="📋 Session Summary",
        border_style="blue"
    ))
    
    # Preparation phase
    prep_time = 2 * 60  # 2 minutes in seconds
    console.print(Panel(
        "[bold yellow]🛠️ Preparation Time![/bold yellow]\n\n"
        "Use this time to prepare your setups and gather all your resources!\n"
        "[dim]You can press CTRL + C to end this time at anytime[/dim]",
        border_style="yellow"
    ))
    
    try:
        countdown_timer(prep_time, "Preparation time")
        console.print("[green]Preparation complete![/green]")
    except KeyboardInterrupt:
        console.print("\n[yellow]Timer stopped by user.[/yellow]")
    
    console.print("[blue]Blocking websites...[/blue]")
    
    return subject, session_time

def study_session(subject: str, session_minutes: int):
    """Main study session with countdown timer."""
    to_seconds = session_minutes * 60 
    remaining_seconds = to_seconds
    
    # Start website blocking
    execute_bash_script('start')
    bell_notification_sound()
    
    console.print(Panel(
        f"[bold green]🚀 Study Session Started![/bold green]\n"
        f"Subject: {subject}\n"
        f"Duration: {session_minutes} minutes\n"
        f"Stay focused! 💪",
        border_style="green"
    ))
    
    try:
        countdown_timer(remaining_seconds, f"Study Session: {subject}")
        
        console.print(Panel(
            "[bold green]🎉 Time's up![/bold green]\n"
            "Great job on completing your study session!",
            border_style="green"
        ))
        bell_notification_sound()
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Session interrupted by user[/yellow]")
    
    finally:
        # Always unblock websites
        console.print("[blue]Unblocking websites...[/blue]")
        execute_bash_script('end')
    
    # Reflection phase
    if Confirm.ask("Would you like to do a quick reflection on your session?", default=True):
        conduct_reflection(subject)
    
    console.print(Panel.fit(
        "[bold green]✨ Session Complete![/bold green]\n"
        "Keep up the great work!",
        border_style="green"
    ))

def start_study_mode():
    """Main function to start the complete study mode experience."""
    try:
        subject, session_time = before_study_session()
        study_session(subject, session_time)
    except KeyboardInterrupt:
        console.print("\n[red]Study mode cancelled by user[/red]")
        console.print("[blue]Ensuring websites are unblocked...[/blue]")
        execute_bash_script('end')
    except Exception as e:
        console.print(f"[red]An error occurred: {e}[/red]")
        console.print("[blue]Ensuring websites are unblocked...[/blue]")
        execute_bash_script('end')

if __name__ == "__main__":
    start_study_mode()