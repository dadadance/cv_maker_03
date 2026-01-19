"""CLI commands for experience management."""
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from core.services.repository import (
    add_experience,
    add_version,
    delete_experience,
    delete_version,
    find_experience_by_id,
    find_version_by_id,
    load_or_create,
    save_data,
    update_version,
)

app = typer.Typer(help="Manage work experiences in the resume bank")
console = Console()


@app.command("list")
def list_experiences():
    """List all experiences in the resume bank."""
    data = load_or_create()

    if not data.experiences:
        console.print("[yellow]No experiences found.[/yellow]")
        return

    table = Table(title="Experiences")
    table.add_column("ID", style="cyan")
    table.add_column("Company", style="green")
    table.add_column("Period")
    table.add_column("Versions", justify="right")

    for exp in data.experiences:
        end = "Present" if exp.is_current else (exp.end_date or "?")
        period = f"{exp.start_date} - {end}"
        table.add_row(
            exp.id,
            exp.company,
            period,
            str(len(exp.versions)),
        )

    console.print(table)


@app.command("add")
def add_experience_cmd(
    company: str = typer.Argument(..., help="Company name"),
    start_date: str = typer.Argument(..., help="Start date (YYYY-MM)"),
    end_date: Optional[str] = typer.Option(None, "--end", "-e", help="End date (YYYY-MM), omit for current"),
    current: bool = typer.Option(False, "--current", "-c", help="Mark as current position"),
    location: str = typer.Option("", "--location", "-l", help="Location"),
    url: str = typer.Option("", "--url", "-u", help="Company URL"),
):
    """Add a new work experience."""
    data = load_or_create()

    new_data, exp = add_experience(
        data,
        company=company,
        start_date=start_date,
        end_date=end_date,
        is_current=current,
        location=location,
        company_url=url,
    )
    save_data(new_data)

    console.print(f"[green]Added experience:[/green] {exp.company} (ID: {exp.id})")
    console.print("[dim]Tip: Add a version with 'experience version add'[/dim]")


@app.command("show")
def show_experience_cmd(
    exp_id: str = typer.Argument(..., help="Experience ID"),
):
    """Show details of an experience including all versions."""
    data = load_or_create()

    exp = find_experience_by_id(data, exp_id)
    if not exp:
        console.print(f"[red]Error:[/red] Experience not found: {exp_id}")
        raise typer.Exit(1)

    end = "Present" if exp.is_current else (exp.end_date or "?")

    console.print(f"\n[bold]{exp.company}[/bold]")
    console.print(f"  ID: [cyan]{exp.id}[/cyan]")
    console.print(f"  Period: {exp.start_date} - {end}")
    if exp.location:
        console.print(f"  Location: {exp.location}")
    if exp.company_url:
        console.print(f"  URL: {exp.company_url}")

    if exp.versions:
        console.print(f"\n  [bold]Versions ({len(exp.versions)}):[/bold]")
        for v in exp.versions:
            default_marker = " [green](default)[/green]" if v.is_default else ""
            console.print(f"    [{v.id}] {v.title}{default_marker}")
            if v.bullets:
                for bullet in v.bullets[:3]:
                    console.print(f"      • {bullet[:60]}...")
                if len(v.bullets) > 3:
                    console.print(f"      [dim]... and {len(v.bullets) - 3} more[/dim]")
    else:
        console.print("\n  [yellow]No versions yet.[/yellow]")

    console.print()


@app.command("delete")
def delete_experience_cmd(
    exp_id: str = typer.Argument(..., help="Experience ID"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    """Delete an experience and all its versions."""
    data = load_or_create()

    exp = find_experience_by_id(data, exp_id)
    if not exp:
        console.print(f"[red]Error:[/red] Experience not found: {exp_id}")
        raise typer.Exit(1)

    if not force:
        confirm = typer.confirm(
            f"Delete experience '{exp.company}' and all {len(exp.versions)} version(s)?"
        )
        if not confirm:
            console.print("[yellow]Cancelled.[/yellow]")
            return

    new_data = delete_experience(data, exp_id)
    save_data(new_data)

    console.print(f"[green]Deleted experience:[/green] {exp.company} ({exp_id})")


# --- Version subcommands ---


version_app = typer.Typer(help="Manage experience versions")
app.add_typer(version_app, name="version")


@version_app.command("add")
def add_version_cmd(
    exp_id: str = typer.Argument(..., help="Experience ID to add version to"),
    title: str = typer.Argument(..., help="Job title for this version"),
    description: str = typer.Option("", "--desc", "-d", help="Role description"),
    bullets: Optional[list[str]] = typer.Option(None, "--bullet", "-b", help="Achievement bullets (repeat for multiple)"),
    skills: Optional[list[str]] = typer.Option(None, "--skill", "-s", help="Skill IDs (repeat for multiple)"),
    default: bool = typer.Option(False, "--default", help="Set as default version"),
):
    """Add a new version to an experience."""
    data = load_or_create()

    exp = find_experience_by_id(data, exp_id)
    if not exp:
        console.print(f"[red]Error:[/red] Experience not found: {exp_id}")
        raise typer.Exit(1)

    new_data, version = add_version(
        data,
        exp_id=exp_id,
        title=title,
        description=description,
        bullets=bullets or [],
        skills=skills or [],
        is_default=default,
    )
    save_data(new_data)

    console.print(f"[green]Added version:[/green] {version.title} (ID: {version.id})")


@version_app.command("show")
def show_version_cmd(
    version_id: str = typer.Argument(..., help="Version ID"),
):
    """Show details of a specific version."""
    data = load_or_create()

    result = find_version_by_id(data, version_id)
    if not result:
        console.print(f"[red]Error:[/red] Version not found: {version_id}")
        raise typer.Exit(1)

    exp, v = result
    default_marker = " [green](default)[/green]" if v.is_default else ""

    console.print(f"\n[bold]{v.title}[/bold]{default_marker}")
    console.print(f"  ID: [cyan]{v.id}[/cyan]")
    console.print(f"  Experience: {exp.company} ({exp.id})")
    console.print(f"  Created: {v.created_at}")

    if v.description:
        console.print("\n  [bold]Description:[/bold]")
        console.print(f"    {v.description}")

    if v.bullets:
        console.print(f"\n  [bold]Achievements ({len(v.bullets)}):[/bold]")
        for i, bullet in enumerate(v.bullets, 1):
            console.print(f"    {i}. {bullet}")

    if v.skills:
        console.print(f"\n  [bold]Skills:[/bold] {', '.join(v.skills)}")

    console.print()


@version_app.command("delete")
def delete_version_cmd(
    version_id: str = typer.Argument(..., help="Version ID"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    """Delete a version from an experience."""
    data = load_or_create()

    result = find_version_by_id(data, version_id)
    if not result:
        console.print(f"[red]Error:[/red] Version not found: {version_id}")
        raise typer.Exit(1)

    exp, v = result

    if not force:
        confirm = typer.confirm(f"Delete version '{v.title}' from {exp.company}?")
        if not confirm:
            console.print("[yellow]Cancelled.[/yellow]")
            return

    new_data = delete_version(data, version_id)
    save_data(new_data)

    console.print(f"[green]Deleted version:[/green] {v.title} ({version_id})")


@version_app.command("set-default")
def set_default_version_cmd(
    version_id: str = typer.Argument(..., help="Version ID to set as default"),
):
    """Set a version as the default for its experience."""
    data = load_or_create()

    result = find_version_by_id(data, version_id)
    if not result:
        console.print(f"[red]Error:[/red] Version not found: {version_id}")
        raise typer.Exit(1)

    exp, v = result

    # Unset all defaults for this experience, then set the chosen one
    new_data = data
    for ver in exp.versions:
        if ver.id == version_id:
            new_data = update_version(new_data, ver.id, is_default=True)
        else:
            new_data = update_version(new_data, ver.id, is_default=False)

    save_data(new_data)
    console.print(f"[green]Set default:[/green] {v.title} ({version_id})")
