"""BookMinder CLI interface."""

import click

from bookminder.apple_books.library import list_recent_books


@click.group()
def main() -> None:
    """BookMinder - Extract content and highlights from Apple Books."""
    pass


@main.group()
def list() -> None:
    """List books from your library."""
    pass


@list.command()
@click.option(
    "--user",
    default=None,
    help="Examine books for specified user (default: current user)",
)
def recent(user: str | None) -> None:
    """Show recently read books with progress."""
    try:
        books = list_recent_books(user_name=user)
        if not books:
            click.echo("No books currently being read")
            return

        for book in books:
            progress = book["reading_progress_percentage"]
            click.echo(f"{book['title']} - {book['author']} ({progress}%)")
    except FileNotFoundError as e:
        if "BKAgentService" in str(e):
            click.echo("Apple Books not found. Has it been opened on this account?")
        else:
            click.echo("Apple Books database not found.")
    except Exception as e:
        click.echo(f"Error reading Apple Books: {e}")
