"""CLI commands for job description management."""
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from core.services.repository import (
    add_jd,
    delete_jd,
    find_jd_by_id,
    load_or_create,
    save_data,
    update_jd,
)

app = typer.Typer(help="Manage job descriptions in the resume bank")
console = Console()


@app.command("list")
def list_jds():
    """List all job descriptions."""
    data = load_or_create()

    if not data.job_descriptions:
        console.print("[yellow]No job descriptions found.[/yellow]")
        return

    table = Table(title="Job Descriptions")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="green")
    table.add_column("Company")
    table.add_column("Created")

    for jd in data.job_descriptions:
        table.add_row(
            jd.id,
            jd.title,
            jd.company,
            jd.created_at.strftime("%Y-%m-%d"),
        )

    console.print(table)


@app.command("add")
def add_jd_cmd(
    title: str = typer.Argument(..., help="Job title"),
    company: str = typer.Argument(..., help="Company name"),
    text: Optional[str] = typer.Option(None, "--text", "-t", help="Job description text"),
    file: Optional[Path] = typer.Option(None, "--file", "-f", help="Read JD from file"),
    url: str = typer.Option("", "--url", "-u", help="Job posting URL"),
):
    """Add a new job description."""
    data = load_or_create()

    # Get text from file or argument
    if file:
        if not file.exists():
            console.print(f"[red]Error:[/red] File not found: {file}")
            raise typer.Exit(1)
        jd_text = file.read_text()
    elif text:
        jd_text = text
    else:
        console.print("[yellow]Enter job description (Ctrl+D when done):[/yellow]")
        import sys
        jd_text = sys.stdin.read()

    if not jd_text.strip():
        console.print("[red]Error:[/red] Job description text is required")
        raise typer.Exit(1)

    new_data, jd = add_jd(data, title, company, jd_text.strip(), url)
    save_data(new_data)

    console.print(f"[green]Added JD:[/green] {jd.title} at {jd.company} (ID: {jd.id})")


@app.command("show")
def show_jd_cmd(
    jd_id: str = typer.Argument(..., help="Job description ID"),
    full: bool = typer.Option(False, "--full", "-f", help="Show full text"),
):
    """Show details of a job description."""
    data = load_or_create()

    jd = find_jd_by_id(data, jd_id)
    if not jd:
        console.print(f"[red]Error:[/red] JD not found: {jd_id}")
        raise typer.Exit(1)

    console.print(f"\n[bold]{jd.title}[/bold] at {jd.company}")
    console.print(f"  ID: [cyan]{jd.id}[/cyan]")
    console.print(f"  Created: {jd.created_at.strftime('%Y-%m-%d %H:%M')}")
    if jd.url:
        console.print(f"  URL: {jd.url}")

    console.print("\n[bold]Description:[/bold]")
    if full:
        console.print(jd.text)
    else:
        preview = jd.text[:500]
        if len(jd.text) > 500:
            preview += "..."
            console.print(preview)
            console.print(f"\n[dim]({len(jd.text)} chars total - use --full to see all)[/dim]")
        else:
            console.print(preview)

    console.print()


@app.command("delete")
def delete_jd_cmd(
    jd_id: str = typer.Argument(..., help="Job description ID"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    """Delete a job description."""
    data = load_or_create()

    jd = find_jd_by_id(data, jd_id)
    if not jd:
        console.print(f"[red]Error:[/red] JD not found: {jd_id}")
        raise typer.Exit(1)

    if not force:
        confirm = typer.confirm(f"Delete JD '{jd.title}' at {jd.company}?")
        if not confirm:
            console.print("[yellow]Cancelled.[/yellow]")
            return

    new_data = delete_jd(data, jd_id)
    save_data(new_data)

    console.print(f"[green]Deleted JD:[/green] {jd.title} ({jd_id})")


@app.command("edit")
def edit_jd_cmd(
    jd_id: str = typer.Argument(..., help="Job description ID"),
    title: Optional[str] = typer.Option(None, "--title", help="New title"),
    company: Optional[str] = typer.Option(None, "--company", help="New company"),
    url: Optional[str] = typer.Option(None, "--url", help="New URL"),
    text: Optional[str] = typer.Option(None, "--text", help="New description text"),
    file: Optional[Path] = typer.Option(None, "--file", help="Read new text from file"),
):
    """Edit a job description."""
    data = load_or_create()

    jd = find_jd_by_id(data, jd_id)
    if not jd:
        console.print(f"[red]Error:[/red] JD not found: {jd_id}")
        raise typer.Exit(1)

    updates = {}
    if title is not None:
        updates["title"] = title
    if company is not None:
        updates["company"] = company
    if url is not None:
        updates["url"] = url
    if file:
        if not file.exists():
            console.print(f"[red]Error:[/red] File not found: {file}")
            raise typer.Exit(1)
        updates["text"] = file.read_text().strip()
    elif text is not None:
        updates["text"] = text

    if not updates:
        console.print("[yellow]No changes specified.[/yellow]")
        return

    new_data = update_jd(data, jd_id, **updates)
    save_data(new_data)

    console.print(f"[green]Updated JD:[/green] {jd_id}")
