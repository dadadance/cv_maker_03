"""CLI commands for profile management."""

import typer
from rich.console import Console

from core.models import Profile
from core.services.repository import (
    load_or_create,
    save_data,
    set_profile_field,
    update_profile,
)

app = typer.Typer(help="Manage your profile in the resume bank")
console = Console()


@app.command("show")
def show_profile():
    """Show current profile information."""
    data = load_or_create()
    profile = data.profile

    console.print("\n[bold]Profile[/bold]")
    console.print(f"  Name: [cyan]{profile.name or '(not set)'}[/cyan]")
    console.print(f"  Headline: {profile.headline or '(not set)'}")
    console.print(f"  Location: {profile.location or '(not set)'}")

    console.print("\n[bold]Contact[/bold]")
    if profile.emails:
        console.print(f"  Emails: {', '.join(profile.emails)}")
    else:
        console.print("  Emails: (not set)")

    if profile.phones:
        console.print(f"  Phones: {', '.join(profile.phones)}")
    else:
        console.print("  Phones: (not set)")

    console.print("\n[bold]Links[/bold]")
    console.print(f"  LinkedIn: {profile.linkedin or '(not set)'}")
    console.print(f"  GitHub: {profile.github or '(not set)'}")
    console.print(f"  Portfolio: {profile.portfolio or '(not set)'}")

    if profile.summary:
        console.print("\n[bold]Summary[/bold]")
        console.print(f"  {profile.summary[:200]}{'...' if len(profile.summary) > 200 else ''}")

    console.print()


@app.command("set")
def set_profile_field_cmd(
    field: str = typer.Argument(..., help="Field to set (name, headline, location, linkedin, github, portfolio, summary)"),
    value: str = typer.Argument(..., help="Value to set"),
):
    """Set a single profile field."""
    valid_fields = ["name", "headline", "location", "linkedin", "github", "portfolio", "summary"]

    if field not in valid_fields:
        console.print(f"[red]Error:[/red] Invalid field '{field}'")
        console.print(f"Valid fields: {', '.join(valid_fields)}")
        raise typer.Exit(1)

    data = load_or_create()
    new_data = set_profile_field(data, field, value)
    save_data(new_data)

    console.print(f"[green]Updated profile:[/green] {field} = {value}")


@app.command("add-email")
def add_email_cmd(
    email: str = typer.Argument(..., help="Email address to add"),
):
    """Add an email to profile."""
    data = load_or_create()
    emails = data.profile.emails + [email]
    new_data = set_profile_field(data, "emails", emails)
    save_data(new_data)

    console.print(f"[green]Added email:[/green] {email}")


@app.command("remove-email")
def remove_email_cmd(
    email: str = typer.Argument(..., help="Email address to remove"),
):
    """Remove an email from profile."""
    data = load_or_create()

    if email not in data.profile.emails:
        console.print(f"[red]Error:[/red] Email not found: {email}")
        raise typer.Exit(1)

    emails = [e for e in data.profile.emails if e != email]
    new_data = set_profile_field(data, "emails", emails)
    save_data(new_data)

    console.print(f"[green]Removed email:[/green] {email}")


@app.command("add-phone")
def add_phone_cmd(
    phone: str = typer.Argument(..., help="Phone number to add"),
):
    """Add a phone number to profile."""
    data = load_or_create()
    phones = data.profile.phones + [phone]
    new_data = set_profile_field(data, "phones", phones)
    save_data(new_data)

    console.print(f"[green]Added phone:[/green] {phone}")


@app.command("remove-phone")
def remove_phone_cmd(
    phone: str = typer.Argument(..., help="Phone number to remove"),
):
    """Remove a phone number from profile."""
    data = load_or_create()

    if phone not in data.profile.phones:
        console.print(f"[red]Error:[/red] Phone not found: {phone}")
        raise typer.Exit(1)

    phones = [p for p in data.profile.phones if p != phone]
    new_data = set_profile_field(data, "phones", phones)
    save_data(new_data)

    console.print(f"[green]Removed phone:[/green] {phone}")


@app.command("init")
def init_profile_cmd(
    name: str = typer.Option(..., "--name", "-n", prompt="Your full name", help="Full name"),
    email: str = typer.Option(..., "--email", "-e", prompt="Primary email", help="Primary email"),
    headline: str = typer.Option("", "--headline", "-h", prompt="Professional headline (optional)", help="Professional headline"),
    location: str = typer.Option("", "--location", "-l", prompt="Location (optional)", help="Location"),
):
    """Initialize profile with basic information (interactive)."""
    data = load_or_create()

    profile = Profile(
        name=name,
        emails=[email] if email else [],
        headline=headline,
        location=location,
        phones=data.profile.phones,
        linkedin=data.profile.linkedin,
        github=data.profile.github,
        portfolio=data.profile.portfolio,
        summary=data.profile.summary,
    )

    new_data = update_profile(data, profile)
    save_data(new_data)

    console.print("\n[green]Profile initialized![/green]")
    show_profile()
