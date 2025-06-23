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
def recent() -> None:
    """Show recently read books with progress."""
    books = list_recent_books()
    for book in books:
        progress = book["reading_progress_percentage"]
        click.echo(f"{book['title']} - {book['author']} ({progress}%)")
