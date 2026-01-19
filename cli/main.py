"""CV Maker CLI - Main entry point."""
import typer
from rich.console import Console

from cli.commands import experience, jd, profile, resume, skill

app = typer.Typer(
    name="cvmaker",
    help="CV Maker - AI-powered resume builder with JSON-based storage",
    no_args_is_help=True,
)
console = Console()

# Register subcommand groups
app.add_typer(profile.app, name="profile")
app.add_typer(skill.app, name="skill")
app.add_typer(experience.app, name="experience")
app.add_typer(jd.app, name="jd")
app.add_typer(resume.app, name="resume")


@app.command()
def version():
    """Show version information."""
    console.print("[bold green]CV Maker[/bold green] v0.1.0")


@app.command()
def status():
    """Show current data status (skills, experiences, resumes count)."""
    from core.services.repository import load_or_create

    data = load_or_create()

    console.print("\n[bold]CV Maker Status[/bold]\n")
    console.print(f"  Profile: [cyan]{data.profile.name or '(not set)'}[/cyan]")
    console.print(f"  Skills: [cyan]{len(data.skills)}[/cyan]")
    console.print(f"  Experiences: [cyan]{len(data.experiences)}[/cyan]")
    console.print(f"  Job Descriptions: [cyan]{len(data.job_descriptions)}[/cyan]")
    console.print(f"  Resumes: [cyan]{len(data.resumes)}[/cyan]")
    console.print()


@app.command()
def init():
    """Initialize a new resume bank with sample data."""
    from core.services.repository import load_or_create

    data = load_or_create()

    if data.profile.name or data.skills or data.experiences:
        console.print("[yellow]Data already exists. Use individual commands to modify.[/yellow]")
        return

    console.print("[green]Resume bank initialized![/green]")
    console.print("Run 'profile init' to set up your profile.")


if __name__ == "__main__":
    app()
