"""CLI commands for skill management."""
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from core.models import SkillCategory, SkillLevel
from core.services.repository import (
    add_skill,
    delete_skill,
    find_skill_by_id,
    find_skill_by_name,
    load_or_create,
    save_data,
    update_skill,
)

app = typer.Typer(help="Manage skills in the resume bank")
console = Console()


@app.command("list")
def list_skills():
    """List all skills in the resume bank."""
    data = load_or_create()

    if not data.skills:
        console.print("[yellow]No skills found.[/yellow]")
        return

    table = Table(title="Skills")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Category")
    table.add_column("Level")
    table.add_column("Years", justify="right")

    for skill in data.skills:
        table.add_row(
            skill.id,
            skill.name,
            skill.category.value,
            skill.level.value,
            str(skill.years),
        )

    console.print(table)


@app.command("add")
def add_skill_cmd(
    name: str = typer.Argument(..., help="Name of the skill"),
    category: SkillCategory = typer.Option(
        SkillCategory.OTHER,
        "--category", "-c",
        help="Skill category",
    ),
    level: SkillLevel = typer.Option(
        SkillLevel.MID,
        "--level", "-l",
        help="Proficiency level",
    ),
    years: int = typer.Option(
        0,
        "--years", "-y",
        help="Years of experience",
    ),
):
    """Add a new skill to the resume bank."""
    data = load_or_create()

    # Check if skill already exists
    existing = find_skill_by_name(data, name)
    if existing:
        console.print(f"[red]Error:[/red] Skill '{name}' already exists (ID: {existing.id})")
        raise typer.Exit(1)

    new_data, skill = add_skill(data, name, category, level, years)
    save_data(new_data)

    console.print(f"[green]Added skill:[/green] {skill.name} (ID: {skill.id})")


@app.command("edit")
def edit_skill_cmd(
    skill_id: str = typer.Argument(..., help="ID of the skill to edit"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="New name"),
    category: Optional[SkillCategory] = typer.Option(None, "--category", "-c", help="New category"),
    level: Optional[SkillLevel] = typer.Option(None, "--level", "-l", help="New level"),
    years: Optional[int] = typer.Option(None, "--years", "-y", help="New years"),
):
    """Edit an existing skill."""
    data = load_or_create()

    skill = find_skill_by_id(data, skill_id)
    if not skill:
        console.print(f"[red]Error:[/red] Skill not found: {skill_id}")
        raise typer.Exit(1)

    updates = {}
    if name is not None:
        updates["name"] = name
    if category is not None:
        updates["category"] = category
    if level is not None:
        updates["level"] = level
    if years is not None:
        updates["years"] = years

    if not updates:
        console.print("[yellow]No changes specified.[/yellow]")
        return

    new_data = update_skill(data, skill_id, **updates)
    save_data(new_data)

    console.print(f"[green]Updated skill:[/green] {skill_id}")


@app.command("delete")
def delete_skill_cmd(
    skill_id: str = typer.Argument(..., help="ID of the skill to delete"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    """Delete a skill from the resume bank."""
    data = load_or_create()

    skill = find_skill_by_id(data, skill_id)
    if not skill:
        console.print(f"[red]Error:[/red] Skill not found: {skill_id}")
        raise typer.Exit(1)

    if not force:
        confirm = typer.confirm(f"Delete skill '{skill.name}' ({skill_id})?")
        if not confirm:
            console.print("[yellow]Cancelled.[/yellow]")
            return

    new_data = delete_skill(data, skill_id)
    save_data(new_data)

    console.print(f"[green]Deleted skill:[/green] {skill.name} ({skill_id})")


@app.command("show")
def show_skill_cmd(
    skill_id: str = typer.Argument(..., help="ID of the skill to show"),
):
    """Show details of a specific skill."""
    data = load_or_create()

    skill = find_skill_by_id(data, skill_id)
    if not skill:
        console.print(f"[red]Error:[/red] Skill not found: {skill_id}")
        raise typer.Exit(1)

    console.print(f"\n[bold]Skill:[/bold] {skill.name}")
    console.print(f"  ID: [cyan]{skill.id}[/cyan]")
    console.print(f"  Category: {skill.category.value}")
    console.print(f"  Level: {skill.level.value}")
    console.print(f"  Years: {skill.years}")
    console.print()
