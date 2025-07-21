"""BookMinder CLI interface."""

from collections.abc import Callable
from typing import Any

import click

from bookminder import BookminderError
from bookminder.apple_books.library import (
    SUPPORTED_FILTERS,
    Book,
    list_all_books,
    list_recent_books,
)


@click.group()
def main() -> None:
    """BookMinder - Extract content and highlights from Apple Books."""
    pass


def validate_filter(filter_value: str | None) -> None:
    """Validate filter value against supported filters."""
    if filter_value and filter_value not in SUPPORTED_FILTERS:
        raise click.ClickException(
            f"Invalid filter: '{filter_value}'\n"
            f"Valid filters: {', '.join(sorted(SUPPORTED_FILTERS))}"
        )


# Common options for list commands
def with_common_list_options(func: Callable[..., Any]) -> Callable[..., Any]:
    """Add common options to list subcommands."""
    func = click.option(
        "--user",
        default=None,
        help="Examine books for specified user (default: current user)",
    )(func)
    func = click.option(
        "--filter",
        default=None,
        help="Filter books by attribute (cloud, !cloud, sample, !sample, etc).",
    )(func)
    return func


# This is a test comment to trigger pre-commit hooks.
@main.group(name="list")
def list_cmd() -> None:
    """List books from your library."""
    pass


def format(book: Book) -> str:
    """Format book dictionary for CLI output."""
    progress = book.get("reading_progress_percentage")

    # Format reading status with priority: (Finished) > (Unread) > percentage
    if progress == 100:
        progress_str = " (Finished)"
    elif progress == 0:
        progress_str = " (Unread)"
    elif progress is not None:
        progress_str = f" ({progress}%)"
    else:
        progress_str = ""

    sample_str = " • Sample" if book.get("is_sample") else ""
    cloud_str = " ☁️" if book.get("is_cloud") else ""
    return f"{book['title']} - {book['author']}{progress_str}{sample_str}{cloud_str}"


def format_book_list(books: list[Book], empty_message: str = "No books found") -> str:
    """Format a list of books for display."""
    if not books:
        return empty_message
    return "\n".join(format(book) for book in books)


@list_cmd.command()
@with_common_list_options
def recent(user: str | None, filter: str | None) -> None:
    """Show recently read books with progress."""
    validate_filter(filter)

    try:
        books = list_recent_books(user=user, filter=filter)
        click.echo(format_book_list(
            books, empty_message="No books currently being read"
        ))
    except BookminderError as e:
        click.echo(f"{e}")


@list_cmd.command()
@with_common_list_options
def all(user: str | None, filter: str | None) -> None:
    """Show all books in your library."""
    validate_filter(filter)

    try:
        books = list_all_books(user=user, filter=filter)
        click.echo(format_book_list(books))
    except BookminderError as e:
        click.echo(f"{e}")
