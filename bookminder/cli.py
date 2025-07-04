"""BookMinder CLI interface."""

from pathlib import Path

import click

from bookminder import BookminderError
from bookminder.apple_books.library import list_recent_books


@click.group()
def main() -> None:
    """BookMinder - Extract content and highlights from Apple Books."""
    pass


# This is a test comment to trigger pre-commit hooks.
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
@click.option(
    "--flag",
    default=None,
    type=click.Choice(["cloud", "local"]),
    help="Filter books by a specific flag.",
)
def recent(user: str | None, flag: str | None) -> None:
    """Show recently read books with progress."""
    # Convert user parameter to Path early
    if user:
        user_path = Path(user)
        if not user_path.is_absolute():
            user_path = Path(f"/Users/{user}")
    else:
        user_path = Path.home()

    try:
        books = list_recent_books(user_home=user_path, flag=flag)
        if not books:
            click.echo("No books currently being read")
            return

        for book in books:
            progress = book.get("reading_progress_percentage")
            progress_str = f" ({progress}%)" if progress is not None else ""
            cloud_str = " ☁️" if book.get("is_cloud") else ""
            click.echo(f"{book['title']} - {book['author']}{progress_str}{cloud_str}")

    except BookminderError as e:
        click.echo(f"{e}")
