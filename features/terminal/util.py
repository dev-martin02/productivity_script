import subprocess
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, TimeElapsedColumn, BarColumn, TextColumn
import time

console = Console()

def bell_notification_sound():
    """Play a notification sound."""
    sound_path = Path(__file__).parent.parent / "sound" / "bell-notification.mp3"
    
    if sound_path.exists():
        try:
            with open("/dev/null", 'w') as null_file:
                subprocess.run(
                    ['mpv', "--really-quiet", str(sound_path)], 
                    stdout=null_file, 
                    stderr=null_file
                )
        except FileNotFoundError:
            console.print("[yellow]mpv not found. Install it to enable notification sounds.[/yellow]")


def countdown_timer(duration_seconds: int, description: str = "Timer"):
    """Display a countdown timer with progress bar."""
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task(description, total=duration_seconds)
        
        while duration_seconds > 0:
            minutes = duration_seconds // 60
            seconds = duration_seconds % 60
            progress.update(task, advance=1, description=f"{description}: {minutes:02d}:{seconds:02d}")
            time.sleep(1)
            duration_seconds -= 1

def execute_bash_blocking_script(mode: str):
    """Execute the website blocking script."""
    script_path = Path(__file__).parent.parent / "sitesManager.sh"
    
    try:
        result = subprocess.run(
            ['sudo', str(script_path), mode], 
            check=True, 
            capture_output=True, 
            text=True
        )
        if result.stdout:
            console.print(f"[green]{result.stdout}[/green]")
        if result.stderr:
            console.print(f"[yellow]Warning: {result.stderr}[/yellow]")
    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error executing script: {e}[/red]")
        if e.stderr:
            console.print(f"[red]Details: {e.stderr}[/red]")
