"""Apple Books library access functions."""

import datetime
import plistlib
import subprocess
from pathlib import Path
from typing import Any, TypedDict

BOOKS_PATH = (
    Path.home()
    / "Library/Containers/com.apple.BKAgentService/Data/Documents/iBooks/Books"
)
BOOKS_PLIST = BOOKS_PATH / "Books.plist"


class Book(TypedDict):
    """Book metadata from Apple Books library."""

    title: str
    path: str
    author: str
    updated: datetime.datetime


def _read_books_plist() -> list[dict[str, Any]]:
    """Read the Books.plist file and extract book data.

    Returns
    -------
        List of book dictionaries from the plist file

    """
    # Use plutil to convert binary plist to XML format which plistlib can read
    result = subprocess.run(
        ["plutil", "-convert", "xml1", "-o", "-", str(BOOKS_PLIST)],
        capture_output=True,
        text=False,
        check=True,
    )

    plist_data = plistlib.loads(result.stdout)
    books = plist_data.get("Books", [])
    return books if isinstance(books, list) else []


def list_books(sort_by: str | None = None) -> list[Book]:
    """List books from the Apple Books library.

    Args:
    ----
        sort_by: Optional field to sort by, e.g. 'updated'

    Returns:
    -------
        List of Book objects with metadata

    """
    raw_books = _read_books_plist()

    books: list[Book] = [
        Book(
            title=book.get("itemName", "Unknown"),
            path=book.get("path", ""),
            author=book.get("artistName", "Unknown"),
            updated=book.get("updateDate", datetime.datetime.min),
        )
        for book in raw_books
    ]

    if sort_by == "updated":
        books.sort(key=lambda b: b["updated"], reverse=True)

    return books


def find_book_by_title(title: str) -> Book | None:
    """Find a book by its title.

    Args:
    ----
        title: The title to search for

    Returns:
    -------
        Book object if found, None otherwise

    """
    return next((book for book in list_books() if book["title"] == title), None)
