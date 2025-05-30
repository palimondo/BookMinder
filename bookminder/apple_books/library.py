"""Apple Books library access functions."""

import datetime
import os
import plistlib
import subprocess
from typing import Any

# Path to Apple Books library
BOOKS_PATH = os.path.expanduser(
    "~/Library/Containers/com.apple.BKAgentService/Data/Documents/iBooks/Books"
)
BOOKS_PLIST = os.path.join(BOOKS_PATH, "Books.plist")


def _read_books_plist() -> list[dict[str, Any]]:
    """Read the Books.plist file and extract book data.

    Returns
    -------
        List of book dictionaries from the plist file

    """
    # Use plutil to convert binary plist to XML format which plistlib can read
    result = subprocess.run(
        ["plutil", "-convert", "xml1", "-o", "-", BOOKS_PLIST],
        capture_output=True,
        text=False,
        check=True,
    )

    # Parse the XML plist data
    plist_data = plistlib.loads(result.stdout)
    books = plist_data.get("Books", [])
    return books if isinstance(books, list) else []


def list_books(sort_by: str | None = None) -> list[dict[str, Any]]:
    """List books from the Apple Books library.

    Args:
    ----
        sort_by: Optional field to sort by, e.g. 'updated'

    Returns:
    -------
        List of book dictionaries with metadata

    """
    raw_books = _read_books_plist()

    # Convert to our standardized format
    books = []
    for book in raw_books:
        # Create standardized book entry
        book_entry = {
            "title": book.get("itemName", "Unknown"),
            "path": book.get("path", ""),
            "author": book.get("artistName", "Unknown"),
            "updated": book.get("updateDate", datetime.datetime.min),
        }
        books.append(book_entry)

    # Sort books if requested
    if sort_by == "updated" and books:
        books.sort(key=lambda b: b["updated"], reverse=True)

    return books


def find_book_by_title(title: str) -> dict[str, Any] | None:
    """Find a book by its title.

    Args:
    ----
        title: The title to search for

    Returns:
    -------
        Book dictionary if found, None otherwise

    """
    books = list_books()
    for book in books:
        if book["title"] == title:
            return book
    return None
