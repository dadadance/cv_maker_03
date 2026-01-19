"""CLI commands for resume management."""
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from core.services.repository import (
    add_resume,
    delete_resume,
    find_jd_by_id,
    find_resume_by_id,
    find_skill_by_id,
    find_version_by_id,
    load_or_create,
    save_data,
    update_resume,
)

app = typer.Typer(help="Manage resumes in the resume bank")
console = Console()


@app.command("list")
def list_resumes():
    """List all resumes."""
    data = load_or_create()

    if not data.resumes:
        console.print("[yellow]No resumes found.[/yellow]")
        return

    table = Table(title="Resumes")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("JD")
    table.add_column("Versions", justify="right")
    table.add_column("Skills", justify="right")
    table.add_column("Updated")

    for resume in data.resumes:
        jd_info = "-"
        if resume.jd_id:
            jd = find_jd_by_id(data, resume.jd_id)
            if jd:
                jd_info = f"{jd.title[:20]}..."

        table.add_row(
            resume.id,
            resume.name,
            jd_info,
            str(len(resume.selected_versions)),
            str(len(resume.selected_skills)),
            resume.updated_at.strftime("%Y-%m-%d"),
        )

    console.print(table)


@app.command("create")
def create_resume_cmd(
    name: str = typer.Argument(..., help="Resume name"),
    jd_id: Optional[str] = typer.Option(None, "--jd", help="Job description ID to tailor for"),
    summary: str = typer.Option("", "--summary", "-s", help="Custom summary"),
):
    """Create a new resume."""
    data = load_or_create()

    # Validate JD if provided
    if jd_id:
        jd = find_jd_by_id(data, jd_id)
        if not jd:
            console.print(f"[red]Error:[/red] JD not found: {jd_id}")
            raise typer.Exit(1)

    new_data, resume = add_resume(
        data,
        name=name,
        jd_id=jd_id,
        custom_summary=summary,
    )
    save_data(new_data)

    console.print(f"[green]Created resume:[/green] {resume.name} (ID: {resume.id})")
    console.print("[dim]Tip: Add versions with 'resume add-version' and skills with 'resume add-skill'[/dim]")


@app.command("show")
def show_resume_cmd(
    resume_id: str = typer.Argument(..., help="Resume ID"),
):
    """Show details of a resume."""
    data = load_or_create()

    resume = find_resume_by_id(data, resume_id)
    if not resume:
        console.print(f"[red]Error:[/red] Resume not found: {resume_id}")
        raise typer.Exit(1)

    console.print(f"\n[bold]{resume.name}[/bold]")
    console.print(f"  ID: [cyan]{resume.id}[/cyan]")
    console.print(f"  Created: {resume.created_at.strftime('%Y-%m-%d %H:%M')}")
    console.print(f"  Updated: {resume.updated_at.strftime('%Y-%m-%d %H:%M')}")

    if resume.jd_id:
        jd = find_jd_by_id(data, resume.jd_id)
        if jd:
            console.print(f"  Target JD: {jd.title} at {jd.company} ({jd.id})")

    console.print(f"  Show GitHub: {'Yes' if resume.show_github else 'No'}")
    console.print(f"  Show LinkedIn: {'Yes' if resume.show_linkedin else 'No'}")

    if resume.custom_summary:
        console.print("\n[bold]Summary:[/bold]")
        console.print(f"  {resume.custom_summary[:200]}...")

    if resume.selected_versions:
        console.print(f"\n[bold]Experience Versions ({len(resume.selected_versions)}):[/bold]")
        for vid in resume.selected_versions:
            result = find_version_by_id(data, vid)
            if result:
                exp, v = result
                console.print(f"  • {v.title} at {exp.company} ({vid})")
            else:
                console.print(f"  • [red]{vid} (not found)[/red]")

    if resume.selected_skills:
        console.print(f"\n[bold]Skills ({len(resume.selected_skills)}):[/bold]")
        skill_names = []
        for sid in resume.selected_skills:
            skill = find_skill_by_id(data, sid)
            if skill:
                skill_names.append(skill.name)
            else:
                skill_names.append(f"[red]{sid}[/red]")
        console.print(f"  {', '.join(skill_names)}")

    console.print()


@app.command("delete")
def delete_resume_cmd(
    resume_id: str = typer.Argument(..., help="Resume ID"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    """Delete a resume."""
    data = load_or_create()

    resume = find_resume_by_id(data, resume_id)
    if not resume:
        console.print(f"[red]Error:[/red] Resume not found: {resume_id}")
        raise typer.Exit(1)

    if not force:
        confirm = typer.confirm(f"Delete resume '{resume.name}'?")
        if not confirm:
            console.print("[yellow]Cancelled.[/yellow]")
            return

    new_data = delete_resume(data, resume_id)
    save_data(new_data)

    console.print(f"[green]Deleted resume:[/green] {resume.name} ({resume_id})")


@app.command("add-version")
def add_version_to_resume_cmd(
    resume_id: str = typer.Argument(..., help="Resume ID"),
    version_ids: list[str] = typer.Argument(..., help="Version IDs to add"),
):
    """Add experience versions to a resume."""
    data = load_or_create()

    resume = find_resume_by_id(data, resume_id)
    if not resume:
        console.print(f"[red]Error:[/red] Resume not found: {resume_id}")
        raise typer.Exit(1)

    # Validate versions
    for vid in version_ids:
        if not find_version_by_id(data, vid):
            console.print(f"[red]Error:[/red] Version not found: {vid}")
            raise typer.Exit(1)

    # Merge with existing, avoiding duplicates
    new_versions = list(set(resume.selected_versions + version_ids))
    new_data = update_resume(data, resume_id, selected_versions=new_versions)
    save_data(new_data)

    console.print(f"[green]Added {len(version_ids)} version(s) to resume[/green]")


@app.command("remove-version")
def remove_version_from_resume_cmd(
    resume_id: str = typer.Argument(..., help="Resume ID"),
    version_ids: list[str] = typer.Argument(..., help="Version IDs to remove"),
):
    """Remove experience versions from a resume."""
    data = load_or_create()

    resume = find_resume_by_id(data, resume_id)
    if not resume:
        console.print(f"[red]Error:[/red] Resume not found: {resume_id}")
        raise typer.Exit(1)

    new_versions = [v for v in resume.selected_versions if v not in version_ids]
    new_data = update_resume(data, resume_id, selected_versions=new_versions)
    save_data(new_data)

    console.print(f"[green]Removed {len(version_ids)} version(s) from resume[/green]")


@app.command("add-skill")
def add_skill_to_resume_cmd(
    resume_id: str = typer.Argument(..., help="Resume ID"),
    skill_ids: list[str] = typer.Argument(..., help="Skill IDs to add"),
):
    """Add skills to a resume."""
    data = load_or_create()

    resume = find_resume_by_id(data, resume_id)
    if not resume:
        console.print(f"[red]Error:[/red] Resume not found: {resume_id}")
        raise typer.Exit(1)

    # Validate skills
    for sid in skill_ids:
        if not find_skill_by_id(data, sid):
            console.print(f"[red]Error:[/red] Skill not found: {sid}")
            raise typer.Exit(1)

    # Merge with existing, avoiding duplicates
    new_skills = list(set(resume.selected_skills + skill_ids))
    new_data = update_resume(data, resume_id, selected_skills=new_skills)
    save_data(new_data)

    console.print(f"[green]Added {len(skill_ids)} skill(s) to resume[/green]")


@app.command("remove-skill")
def remove_skill_from_resume_cmd(
    resume_id: str = typer.Argument(..., help="Resume ID"),
    skill_ids: list[str] = typer.Argument(..., help="Skill IDs to remove"),
):
    """Remove skills from a resume."""
    data = load_or_create()

    resume = find_resume_by_id(data, resume_id)
    if not resume:
        console.print(f"[red]Error:[/red] Resume not found: {resume_id}")
        raise typer.Exit(1)

    new_skills = [s for s in resume.selected_skills if s not in skill_ids]
    new_data = update_resume(data, resume_id, selected_skills=new_skills)
    save_data(new_data)

    console.print(f"[green]Removed {len(skill_ids)} skill(s) from resume[/green]")


@app.command("set-summary")
def set_summary_cmd(
    resume_id: str = typer.Argument(..., help="Resume ID"),
    summary: str = typer.Argument(..., help="New summary text"),
):
    """Set custom summary for a resume."""
    data = load_or_create()

    resume = find_resume_by_id(data, resume_id)
    if not resume:
        console.print(f"[red]Error:[/red] Resume not found: {resume_id}")
        raise typer.Exit(1)

    new_data = update_resume(data, resume_id, custom_summary=summary)
    save_data(new_data)

    console.print(f"[green]Updated summary for resume:[/green] {resume_id}")
